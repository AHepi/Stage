# B2. Light and Color as Meaning

> **What this file is for**
> 1. It tells the pipeline how to turn story meaning (desire, threat, secrecy, grief, a story value changing) into concrete light and color choices for every scene and shot.
> 2. It gives a fixed vocabulary, a translation table, "If... then consider... because..." rules, a checklist, and a list of common mistakes.
> 3. It shows how to write a per-location lighting plan and a text color script, with a full color script for *The Catch*.
> 4. It explains which lighting and color words AI image and video models follow, which they ignore, and how to keep light consistent across separately generated shots.
> 5. Read it after the scene breakdown exists (beats and story value changes known) and before shot prompts are written.

---

## 0. How to use this file

**Order of work for an LLM running the pipeline:**

1. **Inventory.** Pull every light and color word out of the scene text (Section 5.1 shows this for *The Catch*). These are script-mandated and cannot be dropped.
2. **Location lighting plan.** For each location, write one lighting plan (Section 5): the story-world sources, their color, direction, hardness, and what stays dark.
3. **Color script.** Write one line per sequence (Section 8) so the whole film's light and color arc is visible at once before any shot is designed.
4. **Per-shot light spec.** For each shot, fill the LIGHT and COLOR fields (Section 9). Only record what differs from the location plan.
5. **Check.** Run the checklist (Section 11) and the mistakes list (Section 12).
6. **Prompt.** Translate into plain model-friendly phrases (Section 13).

**For the non-technical user:** you do not need to know any of this in advance. Ask the LLM to "run the light and color pass from B2 on scene X" and it should produce the plan, then check it against Section 11. If a result looks generic, ask it to run Section 12 on its own output.

### 0.1 Words this file uses (one word per concept)

Each term below is used with exactly this meaning throughout. Where the film trade uses two names for the same thing, the second is given once and then dropped.

| Term | Plain definition |
|---|---|
| **Source** | Where the light seems to come from inside the story world (a window, a lamp, a torch, a screen, the sky). |
| **Key** | The main light on a subject; it decides which side of the face is bright and where the shadows fall. |
| **Fill** | A weaker light on the shadow side that controls how dark the shadows get. |
| **Backlight** | A light behind the subject, pointing roughly toward the camera. |
| **Rim** | The thin bright edge that a backlight draws around a head, shoulder or object, separating it from the background. |
| **Practical** | A light source that is visible in the frame and really works: a lamp, a torch, a monitor, a traffic light. |
| **Motivated light** | Film light placed so that it seems to come from a source in the scene, even when the actual lamp is hidden. |
| **Hard light** | Light from a source that looks small from where the subject stands (a bare bulb, a torch beam, or the sun, which is huge but so far away it looks tiny); it makes crisp-edged shadows. |
| **Soft light** | Light from a source that looks large from where the subject stands (overcast sky, a big window, light bounced off a wall); it makes gradual, blurry-edged shadows. |
| **Direction** | Where the key comes from relative to the face: front, side, back, top, or under. |
| **Frame-left / frame-right** | The left or right side of the picture as the audience sees it. (Crew say "camera left", which means the same thing; this file says frame-left.) |
| **Falloff** | How quickly light gets dimmer with distance from its source. For a small source, light obeys the inverse-square law: twice as far from the source gets a quarter of the light. (Large soft sources and focused beams, such as a flashlight's, dim more slowly close up, but the rule of thumb holds.) So a source placed close to the subject leaves a bright pool with dark around it; a distant source (the sun) lights near and far things almost equally. |
| **Spill** | Stray light that leaks from a source onto areas it was not aimed at (the faint glow around a flashlight beam, light from a doorway on the floor outside). |
| **Raking light** | Light that skims across a surface at a low angle, so every bump and hole throws a shadow and texture jumps out. |
| **Specular highlight** | A small, bright, mirror-like reflection of a light source on a shiny or wet surface (the glints on wet brick, the shine on a steel sill). |
| **Haze** | A thin artificial smoke that crews add to the air so that beams of light become visible and distant things fade slightly. |
| **Exposure** | How bright the camera records the scene overall. "Underexposed" means recorded darker than normal, which can be a mistake or a deliberate choice. |
| **White balance** | The camera setting that decides which light counts as "white". A 3,200 K lamp looks neutral on a camera balanced for 3,200 K and orange on one balanced for daylight, so "warm" and "cool" are always relative to the chosen white. |
| **Key-to-fill ratio** | How much brighter the lit side of a face is than the shadow side; a low ratio looks gentle and open, a high ratio looks dramatic and hidden. |
| **High-key** | A bright image with little shadow and low contrast overall. |
| **Low-key** | A dark image dominated by shadow, with a few bright areas. |
| **Chiaroscuro** | Italian for "light-dark": strong, sculptural contrast between lit forms and deep shadow, as in Caravaggio's paintings. |
| **Silhouette** | A subject seen as a dark shape against a brighter background, with little or no detail inside the shape. |
| **Bounce** | Light reflected off a surface (a white card, a wall, a ceiling) to make it softer or to add gentle fill. |
| **Negative fill** | Black material placed on the shadow side to soak up stray light and make the shadow side darker. |
| **Eye light** | The small, mirror-like reflection of a light source in a person's eye (photographers call it a catchlight), and by extension any small light placed to create it; it makes a face look alive and attentive. The classic eye light is a small lamp on or just above the camera: Lucien Ballard devised one for Merle Oberon on *The Lodger* (1944) to soften her facial scars, and it put a highlight in her eyes, so crews still call an on-camera light an "Obie". |
| **Tungsten** | Ordinary filament bulbs and film lamps built the same way; they give warm, orange-leaning light (about 2,700-3,200 K; see Temperature below). |
| **Film noir** | American crime films of the 1940s and 1950s known for hard, low-key light, deep shadows and night streets; "noir" for short. |
| **Temperature** | How orange or blue a white light looks, measured in kelvin (K); low numbers look orange ("warm"), high numbers look blue ("cool"). |
| **Hue** | Which color something is: red, yellow, green, blue and so on. |
| **Saturation** | How pure and intense a color is; low saturation drifts toward grey. |
| **Value** | How light or dark a color or a whole frame is, regardless of hue. (Bruce Block calls this "brightness".) |
| **Palette** | The limited set of hues, saturations and values a scene or film is allowed to use. |
| **Accent** | A small area of color that differs sharply from the palette around it and so pulls the eye. |
| **Motif** | A color, light or object that returns with a consistent story meaning. |
| **Color script** | A sequence-by-sequence plan of the film's color and light, made before shots are designed, so the emotional arc is visible at a glance. |
| **Grade** | The color adjustment applied to finished footage to unify or shift its look (also called color grading or color correction). |
| **Story value** | A quality in a character's life that can swing between positive and negative within a scene (safety and danger, trust and betrayal), after Robert McKee. This file always writes "story value" to keep it apart from color value. |
| **Light cue** | A change in light during a shot or scene that the story causes (a door opens, a fire starts, a screen switches off). |

**Note on "torch".** *The Catch* uses British English: "torch" means a handheld electric flashlight. The script confirms it ("She puts the torch between her teeth"). In prompts, write "flashlight", because many models trained mostly on American text will draw a burning stick for "torch".

---

## 1. Core principles

1. **Light decides what the audience is allowed to see.** Its first job is attention (where to look), its second is emotion, its third is beauty. A beautiful frame that sends the eye to the wrong place has failed.
2. **Every light needs a source in the story, or a deliberate reason not to have one.** Motivated light feels truthful, so audiences stop noticing it and feel the scene instead. Unmotivated light (a glowing rim from nowhere, a face lit in a pitch-black room) is a stylistic statement and should be used on purpose, for example in a dream or a moment outside time.
3. **Meaning comes from change and contrast, not from absolute levels.** Bruce Block's principle of contrast and affinity (*The Visual Story*) says that contrast in a visual component raises visual intensity and affinity (similarity) lowers it. A dark scene means little if the whole film is dark; it means a great deal after a run of bright ones. Plan light across the film, not shot by shot.
4. **The film defines its own color meanings.** Color associations are cultural and depend on context. A film teaches its audience what red means by using it consistently, then may break that rule once, at a turning point, for effect. Books of color associations give starting hypotheses, not laws.
5. **Hardness comes from the source's apparent size, not its brightness.** A source that looks small from the subject's position (bare bulb, torch, or the distant sun) makes hard light; one that looks large (overcast sky, a lit wall, a big window close by) makes soft light. Moving a source closer makes it softer as well as brighter. Hard light tends to feel exposed, harsh, truthful or dangerous; soft light tends to feel gentle, forgiving, intimate or melancholy.
6. **Direction carries attitude.** Front light flattens and reveals; side light sculpts and divides; backlight separates, idealizes or hides; top light shadows the eyes and feels institutional or oppressive; under light feels unnatural unless a low source (fire, screen, torch on the ground) explains it.
7. **What is dark is designed as carefully as what is lit.** Decide what the audience must not see yet. Darkness is where suspense, secrecy and imagination live.
8. **Faces are usually the destination.** Keep eye light on a character we should read and trust. Remove it only when withholding their inner life is the point.
9. **Light, costume, set and grade make color together.** A red coat under green light turns muddy brown. Coordinate surface colors with the light that will fall on them, and decide in advance which colors must survive the grade.
10. **Restraint beats emphasis.** One clear light idea per scene. A motif works because it is rare; used everywhere, it becomes wallpaper. When the light "says" the theme out loud (lightning at the revelation, a halo on the saint), the audience feels pushed.
11. **Plan light per location, vary it per beat.** A location's lighting plan keeps shots consistent; beat-level changes (a light cue at the turning point) carry the drama.
12. **For AI generation, describe the visible result, not the rig.** Models follow "the right half of her face falls into deep shadow" more reliably than "8:1 key-to-fill with negative fill".

---

## 2. Lighting vocabulary and what each choice does

### 2.1 The basic kit (definitions are in Section 0.1)

| Element | What it tends to do emotionally | Notes for the breakdown |
|---|---|---|
| Key | Sets the whole mood through its direction and hardness | Always state key direction and source. |
| Fill | Little fill = drama, secrecy, danger; lots of fill = openness, comedy, safety | State fill as "none", "low", "medium", "high". |
| Backlight and rim | Separates figure from background; can make a figure heroic, holy, unreal, or (with no key) anonymous | Essential for dark figures against dark backgrounds, such as the figure in *The Catch*. |
| Practical | Grounds the scene in reality and gives motivation for the key | List every practical in frame. |
| Motivated light | Makes stylized light feel natural | Name the motivating source. |
| Bounce | Gentle fill, warm or cool depending on the surface | A pale ceiling bounces light; a sooted ceiling does not (Example 6). |
| Negative fill | Deepens shadow on one side without dimming the key | For AI, describe the result: "the shadow side falls to near black". |
| Falloff | Sources close to the subject give pools of light with dark around them: isolation, search, intimacy | Torches, lamps, candles, screens. |

### 2.2 Direction

| Direction | Look | Typical meaning | Risk |
|---|---|---|---|
| Front | Flat, few shadows | Openness, nothing to hide; also institutional, interrogation, or flash-photo harshness | Flat and dull if used everywhere. |
| Side (about 90°) | Face split into light and dark | Conflict, divided loyalty, a secret, a decision | "Two-faced villain" cliché if used as a label. |
| Three-quarter (about 30-60°) | Modeled, natural | The default for drama; reads as normal life | Invisible, which is often right. |
| Back | Rim, halo, or silhouette | Mystery, arrival, idealization, anonymity, the unknown | Backlit halo on a good character is often heavy-handed. |
| Top | Dark eye sockets, bright forehead and nose | Oppression, authority, institutional or overhead fluorescent life; withholding the eyes | Hard to read faces; use when that is the point. |
| Under | Shadows cast upward | Unnatural, menace, the campfire-story face; natural if motivated by a screen, fire, or torch below | Unmotivated under light is a horror cliché. |

### 2.3 Contrast level

**Key-to-fill ratio.** Photographers measure the difference between lit and shadow sides in *stops*; each stop is a doubling of light. Books define the ratio slightly differently, so treat these numbers as rough bands:

| Band | Approximate ratio | Look | Typical use |
|---|---|---|---|
| Low contrast | about 2:1 (one stop) | Gentle, open, even | Comedy, commercials, safety, the "normal" baseline |
| Medium | about 4:1 (two stops) | Clearly modeled | Most drama |
| High | about 8:1 (three stops) | Moody, one side dark | Tension, secrecy, night interiors |
| Extreme | 16:1 and beyond | Shadow side goes black | Noir, horror, revelation from darkness |

**High-key vs low-key.** High-key frames are bright overall with soft shadows (hospital corridors, sitcoms, daylight offices). Low-key frames are mostly dark with selected bright areas (film noir, crime, night searches). High-key is not automatically "happy": a bright, shadowless hospital can feel cold, exposed and airless. Low-key is not automatically "sad": it can be warm and intimate (a lamp-lit kitchen).

**Chiaroscuro** is low-key with sculpted form: the light shapes bodies against deep shadow. Its painting roots (Caravaggio, Rembrandt) matter for AI prompts, because the word may pull a model toward an oil-painting look rather than a photograph.

**Silhouette** removes detail and identity and leaves shape and gesture. Use it when who someone is matters less than what they are doing, or when identity must be withheld. Roger Deakins silhouettes soldiers against a dusk sky as they descend toward the tunnel in *Sicario* (2015), and silhouettes Bond and an assassin against a glowing advertising screen in the Shanghai fight in *Skyfall* (2012).

### 2.4 The named portrait patterns

These describe where the key sits and the shadow shape it leaves on the face. They are shorthand; the story reason matters more than the pattern name.

| Pattern | Key position | Shadow signature | Tends to feel |
|---|---|---|---|
| Butterfly (also called Paramount lighting) | High and directly in front | Small butterfly-shaped shadow under the nose; face symmetrical | Glamorous, idealized, poised; classic studio-era star portraits |
| Loop | 30-45° to the side, a little high | Nose shadow makes a small loop toward the cheek, not touching the cheek shadow | Natural, pleasant, everyday; the invisible default |
| Rembrandt | 45-60° to the side and higher | Nose shadow joins the cheek shadow, leaving a small lit triangle under the eye on the dark side | Weighty, reflective, painterly, serious |
| Split | 90° to the side | Exactly half the face lit | Division, secrecy, a mind in conflict; menace |

Two more words appear in lighting books: **broad lighting** (the side of the face turned toward the camera is lit, which widens and opens the face) and **short lighting** (the side turned away from the camera is lit, which sculpts and narrows the face and is common in drama).

**Eye light.** The eye light is the smallest and most important light in a close-up. With it, a face reads as present and alive; without it, the eyes become dark pools and the character becomes unreadable. Gordon Willis kept Marlon Brando's eyes in shadow in much of *The Godfather* (1972), so that the Don's thoughts stay hidden from us. The top light began partly as a practical need (Brando's aging make-up held up best lit from above), and Willis turned the constraint into meaning. That is a useful habit: when a location forces a lighting choice on you, ask what it can mean.

---

## 3. What real practitioners did (stated carefully)

These are reference points, not styles to copy. Each entry names films and a transferable lesson. Claims marked "reported" come from interviews and articles listed in Sources.

**Gordon Willis** (*Klute* 1971, *The Godfather* 1972, *The Godfather Part II* 1974, *The Parallax View* 1974, *All the President's Men* 1976, *Annie Hall* 1977, *Manhattan* 1979). Willis lit from above and underexposed, so eye sockets fall into darkness; *The Godfather* opens in the Don's dim office and cuts to the bright wedding outside, two worlds defined by light. The nickname "Prince of Darkness" is reported to have come from his friend Conrad Hall. In *All the President's Men* the brightly lit open newsroom contrasts with the dark parking-garage meetings with the informant. He described his principle as relativity: "I like going from light to dark, dark to light, big to small, small to big." **Lesson:** withholding the eyes withholds access to a person; two lighting worlds can carry a film's central opposition.

**Vittorio Storaro** (*The Conformist* 1970, *Last Tango in Paris* 1972, *Apocalypse Now* 1979, *Reds* 1981, *The Last Emperor* 1987). For *Apocalypse Now*, Storaro described superimposing artificial light and color (flares, colored smoke, searchlights) over natural light to show one culture imposing itself on another; Kurtz is largely a head emerging from darkness. For *The Last Emperor*, Storaro described a journey through the spectrum across Pu Yi's life: childhood dominated by warm reds, oranges and yellows, the Manchuria section using indigo, the imprisonment scenes almost without color, and old age more balanced (TCM article). His three-volume *Writing with Light* (first volume 2002) sets out his personal theory of light and color, which draws on Goethe's *Theory of Colours* and assigns psychological meanings to each color. **Lesson:** derive a color system from the theme and apply it with discipline. **Caution:** his color meanings are personal and should not be copied as universal.

**Roger Deakins** (*The Assassination of Jesse James by the Coward Robert Ford* 2007, *No Country for Old Men* 2007, *Skyfall* 2012, *Prisoners* 2013, *Sicario* 2015, *Blade Runner 2049* 2017, *1917* 2019; *O Brother, Where Art Thou?* 2000, widely cited as the first feature to be fully digitally color graded). On his own website Deakins describes lighting the *Jesse James* saloon scene with "one large soft source through the window" (in practice, five big 18K HMI lamps, powerful daylight-colored film lights, placed about 25 feet outside and pushed through a large frame of diffusion, a translucent material that spreads and softens light, plus frosted glass on the window itself, so the story sees one window), and building "a very controlled pool of light" for the undertaker scene from a single 10-by-5-foot soft box (a lamp enclosed in a fabric box whose front panel diffuses the light) fitted with a two-foot snoot (a tube or skirt around the light that stops it spilling onto the background). He is known for motivated, often single-source light, negative fill, and letting areas fall into shadow; for flares lighting the ruined town at night in *1917*; and for the orange haze of Las Vegas in *Blade Runner 2049*. **Lesson:** find the source, commit to it, and let the rest go dark.

**Conrad Hall** (*Cool Hand Luke* 1967, *In Cold Blood* 1967, *Butch Cassidy and the Sundance Kid* 1969, *American Beauty* 1999, *Road to Perdition* 2002). In *In Cold Blood*, light through a rain-streaked window throws the shadows of water drops onto Robert Blake's face so they read as tears. Hall noticed the effect during rehearsal, called it "purely a visual accident", and pointed it out to director Richard Brooks, who adjusted the blocking (where the actors stand and move) so the shadow "tears" stayed on Blake's face through the scene. *Road to Perdition* uses rain, windows and night silhouettes heavily. **Lesson:** weather and real conditions can do emotional work; watch for what the location gives you.

**Robby Müller** (*The American Friend* 1977, *Paris, Texas* 1984, *Repo Man* 1984, *Down by Law* 1986, *Dead Man* 1995, *Breaking the Waves* 1996, *Dancer in the Dark* 2000). He is known for natural and available light and for keeping, on *Paris, Texas*, the mixed colors of fluorescent, tungsten and neon sources instead of correcting them to a neutral white; the film's uncorrected green fluorescent light is its best-known example. Wim Wenders, recalling their work on *The American Friend* in a video for a 2016 Müller exhibition at the EYE Filmmuseum (quoted by the Criterion Collection), said Müller insisted of the artificial light sources on location, "We're going to keep them all," and fought to stop the processing lab from "correcting" the colors: "The things that other people took out as mistakes we used as a virtue." **Lesson:** the "wrong" colors of real sources (green fluorescents, orange sodium streetlights) carry the truth of a place. A hospital does not need to look pretty.

**Bradford Young** (*Pariah* 2011, *Selma* 2014, *A Most Violent Year* 2014, *Arrival* 2016). Young became the first African American nominated for the Academy Award for cinematography, for *Arrival*. He favors available light, often shoots into the light, and works with low light levels and dense, dark frames; in *Pariah* a night bedroom scene is lit only by Christmas lights and a lamp with a red shade. His dark images are deliberate, not accidents of exposure, and they are built around rendering Black skin richly rather than exposing for a pale-skinned default. In *Arrival* the alien visitors are seen through haze behind a glowing white screen: soft, low contrast, withholding. **Lesson:** darkness can be rich rather than empty, and exposure must be chosen for the skin being photographed, not for a default.

**Greig Fraser** (*Zero Dark Thirty* 2012, *Lion* 2016, *Rogue One* 2016, *Dune* 2021, *The Batman* 2022, *Dune: Part Two* 2024). For the Harkonnen home world, Giedi Prime, in *Dune: Part Two*, Fraser used ARRI ALEXA digital cinema cameras modified to record near-infrared (light just beyond red, invisible to the eye), so the planet's exteriors under its "black sun" render in stark black-and-white: foliage glows pale and skin looks paler than it is. Frame.io's account says the choice was made mainly to create contrast between places, because "the sunlit sand of the Giedi Prime arena might otherwise have looked too much like the sunlit sand of Arrakis." He was also one of the cinematographers on the first season of *The Mandalorian* (2019), which helped establish shooting inside large LED screens that light the actors with the image of their surroundings, so the light on faces matches the world behind them. **Lesson:** one global rule can make a world feel physically different, and light can mark which "world" we are in; and light on a face should come from the world around it.

**Other reference points.** John Alton's *Painting with Light* (1949) is the classic noir lighting text. *Barry Lyndon* (1975, John Alcott) was lit largely by candles for its night interiors. *Days of Heaven* (1978, Néstor Almendros, with additional photography by Haskell Wexler) is famous for scenes shot in the short window after sunset.

**Two worlds coded by light, set and costume together.** Two widely documented examples show that a color system is built by the production designer, costume designer and cinematographer at once, not added in the grade. In *The Matrix* (1999; cinematographer Bill Pope, production designer Owen Paterson) the design team biased scenes inside the simulation toward the green of the on-screen code and scenes in the "real world" toward blue, and changed sets, hair and costume texture between the two worlds as well. In *Traffic* (2000), Steven Soderbergh (who also shot it) gave each storyline its own look so audiences would always know which story they were in: cold blue for the Ohio and Washington story (tungsten film with no correcting filter), warm and diffused for the San Diego story, and yellow, grainy, high-contrast for the Mexico story (tobacco-colored filters). **Lesson:** a world code works when it answers a real story need (which world, which storyline); used without that need, it becomes a filter.

---

## 4. Color: the working vocabulary

### 4.1 Temperature

Temperature describes white light. The naming is backwards from intuition: **higher kelvin looks bluer ("cooler"), lower kelvin looks more orange ("warmer").** Approximate values:

| Source | Approx. kelvin | Look |
|---|---|---|
| Candle, oil lamp, fire | 1,800-2,000 K | Deep orange |
| Low-pressure sodium streetlight (older British and European streets) | about 1,800 K | Yellow-orange from a single wavelength: every other surface color turns grey-brown, and a red coat looks dark |
| High-pressure sodium streetlight | about 2,000-2,200 K | Orange-yellow, usually with a slight green cast on camera; colors survive, muddied |
| Household incandescent bulb | about 2,700 K | Warm orange-yellow |
| Film tungsten lamp | 3,200 K | Warm |
| Cool-white fluorescent | about 4,000 K, often with a green tint on camera | Cold, slightly sick |
| White LED streetlight (now common on British streets, replacing sodium) | about 3,000-4,000 K (some early installations bluer) | Clean white to cold white; flat, sharply edged pools |
| Noon daylight (film convention) | about 5,600 K | Neutral white |
| LED flashlight | often 5,000-6,500 K | Clinical white-blue |
| Overcast sky | about 6,500-7,500 K | Cool grey |
| Open shade, blue sky | 8,000 K and above | Blue |

Mixed temperatures in one frame create contrast: a warm lamp inside against a blue window outside says "shelter inside, cold world outside". Robby Müller's lesson is that you can keep mismatched sources as a truthful texture rather than correcting them away.

**Warm and cool are relative to white balance.** A camera (or a grade) chooses one source as "white", and every other source looks warm or cool against it. Film crews usually balance for the dominant source of a scene, so that source looks neutral and the others carry the color. **Rule for the breakdown:** in each location plan, name the source that reads as neutral white; then describe every other source as warmer or cooler than it. For an AI prompt this becomes plain words ("the lamp looks orange against the white daylight from the window").

**Green and magenta.** Temperature is only the orange-to-blue axis. Many real sources also lean green (older fluorescent tubes, sodium and mercury-vapor streetlights, some cheap LEDs) or magenta (some LED lamps). Crews correct a green-leaning source with a magenta filter and a magenta-leaning one with a green filter; leaving the tint in, as Müller did, is a choice. That tint is part of what makes hospitals and car parks feel like themselves.

**Night convention.** Films often render night as blue. Real moonlight is reflected sunlight and is, if anything, slightly warmer than daylight, but in dim light human vision loses color and shifts toward blue-green sensitivity (the Purkinje effect), which is one reason audiences accept blue as "night". It is a convention, so you may break it.

### 4.2 Hue, saturation, value

- **Hue** is the color family. **Saturation** is its intensity. **Value** is its lightness.
- Most emotional reading of a frame comes from **value and saturation**, not from hue. A desaturated, dark red reads very differently from a bright, saturated red.
- A useful habit: design a scene's value pattern first (where the light and dark masses are), then saturation, then hue.

### 4.3 Schemes

| Scheme | Definition | Tends to feel |
|---|---|---|
| Monochromatic | One hue in several values and saturations | Unified, controlled, sometimes oppressive |
| Analogous | Neighboring hues (yellow, orange, red) | Harmonious, calm, "one mood" |
| Complementary | Opposites on the color wheel (red/green, blue/orange, yellow/violet) | Tension, vibration, opposition |
| Split-complementary | One hue plus the two neighbors of its opposite | Contrast with less strain |
| Accent on neutral | Near-grey palette plus one saturated accent | The accent becomes meaning; ideal for motifs |

### 4.4 Contrast and affinity (Bruce Block)

Block (*The Visual Story*) breaks color into hue, saturation and brightness (this file says value), plus warm and cool. He also treats the overall pattern of light and dark in the frame, from black through grey to white, as a separate visual component he calls **tone**; the frame-value column of the color script (Section 8.2) is a rough tone plan. For each he distinguishes **contrast** (the differences are large) from **affinity** (the differences are small). Affinity of hue means colors that are the same or neighbors on the wheel; maximum contrast of hue means opposites such as red and green or blue and orange. Affinity of saturation means all colors are equally pure or equally grey; contrast of saturation puts vivid colors next to greyed ones. His central principle: contrast increases visual intensity and affinity decreases it. He pairs this with a story-intensity graph: the visual intensity should rise and fall with the story's intensity, or deliberately counter it.

Practical consequence: **choose the climax's contrast first, then keep earlier scenes lower so there is somewhere to go.** Contrast can be carried by different components, so a film that must open in extreme tonal contrast (a flashlight in a black tunnel) can still save its peak for another component: *The Catch* color script (Section 8.5) opens at extreme light-dark contrast but minimum saturation, and peaks in saturation and hue contrast (red fire against a green display) at the climax. **If** the opening already uses the maximum of one component, **then** pick a different component for the climax and write in the color script which one it is.

### 4.5 Simultaneous contrast: colors change their neighbors

Josef Albers (*Interaction of Color*, 1963) and Johannes Itten (*The Art of Color*, 1961) showed that a color's appearance depends on what surrounds it: the same grey looks warm next to blue and cool next to orange. So a color's meaning in a frame also depends on its neighbors. A small red tag on grey brick looks far redder than the same tag on a red door.

### 4.6 Associations: cultural, contextual, and learned inside the film

Patti Bellantoni's *If It's Purple, Someone's Gonna Die: The Power of Color in Visual Storytelling* (Focal Press, 2005) is the most-cited book on color associations in film. **What it claims, fairly stated:** drawing on what the publisher describes as twenty-five years of research on color and behavior, and on teaching (she studied with Josef Albers and has taught at the AFI Conservatory), she argues that colors reliably push audiences toward certain feelings, and she organizes more than sixty films under six colors, and includes conversations with production designers and cinematographers. Each color gets two chapters with paired sets of qualities: red (powerful, lusty, defiant; anxious, angry, romantic), yellow (exuberant, obsessive, daring; innocent, cautionary, idyllic), blue (powerless, cerebral, warm; melancholy, cold, passive), orange (warm, naive, romantic; exotic, toxic, natural earth), green (healthy, ambivalent, vital; poisonous, ominous, corrupt), and purple (asexual, illusory, fantastic; mystical, ominous, ethereal). Her own structure admits that each color cuts both ways, and so do her part titles: red is "the caffeinated color", yellow "the contrary color", blue "the detached color", orange "the sweet and sour color", green "the split personality color", purple "the beyond-the-body color".

**Limits, fairly stated:** the evidence is observational and drawn from classroom work and selected films, not from controlled studies; the film sample is mostly American and European; the title is a memorable pattern in chosen examples, not a rule; and many associations are cultural (white is a color of mourning in parts of East Asia; red signals luck and celebration in China; green has religious meaning in Islam). Use her lists as **hypotheses to test** against the story's own system. The stronger rule is Block's and Shyamalan's practice: the film teaches its own code. In *The Sixth Sense* (1999) red is kept out of most of the film and used, in M. Night Shyamalan's words on the DVD featurette "Rules and Clues", for "anything in the real world that has been tainted by the other world"; the audience learns that, it is not born knowing it.

**If/then for associations.** If the breakdown wants a color to mean something, then (a) write the meaning in the motif table (Section 8.4), (b) find or plan its first appearance at a moment where the story makes that meaning obvious, and (c) only after that use the color without explanation. If the color's first appearance cannot teach it, then do not rely on the association at all.

### 4.7 Surfaces times light

A surface can only reflect colors that are in the light hitting it. Under orange sodium light, blue clothes go near black; under green-tinted fluorescent light, red goes muddy. So:

- Decide the motif colors first (Section 8.4), then check each against every location's light. If a motif must read under a location's light, either change the light or make the object self-lit (a practical).
- Costume colors for principals should be chosen for the locations they spend most time in.

**How the three departments share one palette (practice).** On a real production the production designer (sets and props), the costume designer and the cinematographer agree a palette before shooting, and test paint and fabric under the actual lamps. Four working habits carry over to AI generation:

1. **Faces lead.** Set walls and large props are usually kept at least a little darker (or, in a bright scene, clearly lighter) than the faces in front of them, so skin is not lost against a background of the same value. **If** a background surface is the same value and hue as a principal's skin, **then** darken or cool the background in the location plan.
2. **No pure white, no pure black in fabric.** Costume departments often dye bright white garments to an off-white and choose very dark greys or navies over dead black, so the fabric keeps visible detail. **If** a costume is white (the pressure suit) or black (the figure is the exception: its flatness is the point), **then** describe texture and seams in the prompt so the model renders cloth, not a glowing or empty shape (Rule 28).
3. **Reserve the motif hue.** **If** a color is a motif, **then** keep it out of set dressing and background costume in every location where it does not carry that meaning (no stray red props before the fire; no blue shirts on extras near Iona).
4. **One principal, one color family.** **If** a character's costume color is part of an arc (Iona's blue shirt becomes the labeled sleeve), **then** write that color into the character's description once and repeat it verbatim in every prompt, because image models drift costume colors between separately generated shots.

### 4.8 The teal-and-orange default

Skin tones sit in the orange range; their complementary color is teal. Since digital grading became standard (*O Brother, Where Art Thou?*, 2000, is usually cited as the first fully digitally graded feature), many films push shadows and backgrounds toward teal so that skin "pops". Todd Miro's blog post "Teal and Orange - Hollywood, Please Stop the Madness" (March 2010) popularized the complaint. The problem is not the colors; it is the **default**: when every film and every location gets the same split, color stops carrying any meaning specific to the story, and places lose their own light. AI models often reach for this look when asked for "cinematic" or "movie still". **Rule:** only use a warm/cool split if the story contains that opposition, and then define which side is which and why. **Prompt consequence:** do not put the words "cinematic", "epic" or "blockbuster" in lighting prompts; name the actual sources and their colors instead, so the model has something specific to follow.

---

## 5. Light as a per-location plan: time, weather, practical sources

A **location lighting plan** is written once per location and reused by every shot there. It keeps separately designed (or separately generated) shots consistent, and it forces each light to have a source.

### 5.1 First step: inventory what the text already says

Before designing, list every light and color word in the text. These are script-mandated. For *The Catch*, the inventory includes:

- Tunnel and shaft: "Torchlight on wet brick"; Jude "turns the tag to the light"; Iona "puts the light under the floor frame"; "Four bright bolt holes"; "Her light goes onto each rung before her hand does"; "A band of yellow paint circles the whole shaft at head height"; "Gates go by with lines of light under them"; the sill "worn bright by other people's sleeves".
- Cage: "Floors go by. Light, brick, light, brick."; "the grey maintenance opening"; "Another shot sparks off the grid"; "the bright sill"; "round red beads"; "BLACK. A dark with nothing in it."; "Its red tag whips against the upside-down gate."
- Passage: "the green sign is backwards too".
- Drive: "A red light. Iona finds his eyes in the mirror."
- Kitchen: "Iona holds the lamp."; "A pot of mint on the windowsill"; "an old white scar low on his belly".
- Quarantine: "Police lights beyond frosted windows" (twice); "OSTREL, stitched on it in blue"; "a grey box with a needle in it"; monitors; "Both are furred with grey growth"; "The cage is a small bright box"; "a pale strip"; "A thin WHITE JET"; "a little white crust from the jet"; "stars, slowly turning"; "The recording cuts to black"; "A pale curved surface swings up to meet it" (the ship's hull on the monitor); "A huge black thumb".
- Receiving room: "Through the tall opening with the bright sill: the dark of the shaft"; "A yellow line painted across the floor"; "Its red light comes on" (suit camera); "a white pressure suit"; "a black thumbprint on the card".
- Ship: "lamps on"; "Stars. Below her feet."; "A long dim chamber"; "Three green lights answer on her wrist"; "the metal round them scorched"; "At the end of the chamber, something black comes into the light."; "Burnt grey" (the spent cell); "A light on the shell turns RED" / "GREEN"; "The pale strip dims" (when the figure gives up its own cell); "Behind the cloth, something cloudy moves"; "A white line opens in its casing"; "It looks back at the green line on her visor"; "Light fills the shelves. The cabinet's back glows red"; "The white glare stops"; "a shower of sparks"; "Smoke cuts off" (the room behind the shutter is still "the burning room"); "Two outlines. Hers green. Its own red."; "a glass VESSEL of dark water"; "an ANIMAL. Almost clear"; "the enormous black hand goes dead"; "a lit loop of tube"; "so cold it whitens as it goes"; "two outlines turn green"; "A loose screw rises off the deck beside her boot and hangs in her lamplight"; "Her projected outline turns red"; "The whole outline clears the hull's last projection. Turns green."; "The ship is gone. The stars are gone."; "one pale limb wound tight round its socket"; "Then stars."; "The last light along its side goes out"; "Her lit gloves".
- Ending: "The cloudy growth behind the scrap of shirt fills half the container now."; "The lights low."; "The pale limb comes out through the sealed sleeve again."; "Three uneven strokes in the dark."

This inventory shows the author has already built a color language: red and green as signals, yellow as painted lines, black as the engines and the figure, grey as the growth nothing eats, a cold white as the figure's leaking fluid, and pale, almost clear as the animal that turns out to be inside the black (Rule 25a covers how to light it). The design's job is to make that language consistent and let it carry meaning.

**How to run the inventory (If/then).** If a line names a light source, a color, a brightness word (bright, dim, pale, glare, dark, black) or a light change, then copy it verbatim into the inventory with its scene number. If a color word describes an object (the blue sleeve, the black cell), then the object must keep that color under every light it appears in (Section 4.7). If a line names darkness ("BLACK", "the dark of the shaft"), then treat it as a lighting instruction too: something must stay dark there.

**For prose, sort literal from figurative light.** *The Long Places* is full of both. Literal: "She filled each small lamp to the first knuckle of her thumb"; "over each niche the ceiling was black"; "The grey came down the corridor thin as skimmed milk". Figurative: "a question is a lamp you hold up on somebody". Literal lines go into the lighting plan. Figurative lines go into the scene's meaning notes, where they can guide a choice (for example, a character who avoids asking questions might also avoid lifting the lamp toward faces), but they are never drawn literally.

### 5.2 Time of day and weather

| Condition | Light character | Tends to feel | Watch-out |
|---|---|---|---|
| Pre-dawn / blue hour | Soft, cool, directionless sky; warm practicals read strongly against it | Suspended, fragile, "not yet" | Very short in reality; keep continuity across a scene. |
| Sunrise / golden hour | Low, warm, hard, long shadows | Hope, nostalgia, romance, endings | The most clichéd "beautiful" light; use with reason. |
| Midday sun | Hard top light, short shadows, high contrast | Exposure, heat, judgment, nowhere to hide | Harsh on faces; eyes go dark. |
| Overcast | Huge soft source, low contrast, cool | Melancholy, neutrality, fairness, documentary truth | Can look flat if nothing in frame is darker. |
| Rain | Specular highlights on wet surfaces, reflections, soft sky | Cleansing, grief, pressure, noir | Wet surfaces reflect practicals, which helps night shots. |
| Fog / haze | Light becomes visible as beams; background fades | Mystery, the unknown, spirituality | "God rays" (visible shafts of light slanting through haze from a window) in every interior is a cliché. Use haze only where the place would really have dust, smoke or damp air (the smoke in the collection room after the fire starts; brick dust in the shaft). |
| Night exterior | Pools from streetlights, windows, cars; dark between | Danger, loneliness, freedom | Decide the city's streetlight color and keep it. |
| Night interior | Practicals and screens; strong falloff | Intimacy, secrecy, insomnia | Too dark to read the beat is the most common failure. |

### 5.3 Lighting plan format

```
LOCATION: <name>                 TIME/WEATHER: <...>
STORY JOB OF THIS PLACE: <one sentence: what the place means>
SOURCES (story world): <each source, color temperature, hard/soft, direction>
NEUTRAL WHITE: <which source reads as plain white; all others described as warmer or cooler>
KEY RULE: <where the key comes from for most shots>
CONTRAST: <low / medium / high / extreme>   FILL: <none/low/medium/high>
WHAT STAYS DARK: <areas the audience must not see clearly>
PALETTE: <dominant hue(s)> + ACCENT: <motif color(s) allowed here>
LIGHT CUES: <script-caused changes in light and when they happen>
CONTINUITY LOCKS: <things that must not change between shots>
```

### 5.4 Lighting plans for key locations in *The Catch*

**Loading tunnel, written out in full:**

```
LOCATION: Loading tunnel                TIME/WEATHER: Night; old rainwater, wet brick
STORY JOB OF THIS PLACE: the threshold of the job; a professional reading danger by touch
SOURCES: Iona's handheld flashlight (cool white, about 5,500 K, hard, fast falloff);
         faint cool spill from the tunnel mouth so the cage has a shape
NEUTRAL WHITE: the flashlight
KEY RULE: the key is wherever the torch points; faces lit mainly by spill from the beam's pool
         and by glints off wet brick and steel
CONTRAST: extreme    FILL: none
WHAT STAYS DARK: the shaft above; most of Jude's face
PALETTE: grey-black brick, wet highlights, steel + ACCENT: the red tag (only saturated color)
LIGHT CUES: the torch goes under the floor frame and finds the empty brackets
CONTINUITY LOCKS: the torch moves with Iona; nothing else in the tunnel is bright
```

The flashlight type is a design choice the script leaves open. A modern LED torch gives cool, clinical white (as above); an older incandescent torch gives a warm, yellowish beam with a soft edge (about 2,800-3,000 K). Choose once, because the same torch lights the shaft and every rung. A cool beam fits a professional with modern kit and keeps warmth rationed for later (Section 8.5).

**Quarantine rooms, written out in full** (the location the film returns to most, in three states):

```
LOCATION: Quarantine rooms (Iona's room, Jude's and Eli's rooms, glass partition, demonstration room)
TIME/WEATHER: morning and day (8, 9, 10, 22); night (11, 23); dawn (12, observation room)
STORY JOB OF THIS PLACE: care that is also containment; everyone is visible and nobody can touch
SOURCES: frosted daylight through high windows (soft, cool-neutral); ceiling panels (flat,
         even, about 4,000 K, faint green); monitors and tablets (cool blue-white, soft, close);
         the grey needle boxes (unlit objects, not sources); police lights beyond frosted
         windows in 8 (soft blue flashes, faint by day); a small over-bed reading light
         (warm, about 3,000 K, soft) that is switched on only in 23, when "The lights low."
         leaves it as the room's main source; a small cool status light on the vessel's
         monitoring equipment in 22-23 (a design choice; the script names no such light)
NEUTRAL WHITE: the ceiling panels
KEY RULE: day: soft top light plus window light; faces fully readable, low contrast.
          night: ceiling panels dimmed to a low, even night level; the key on a face is
          whatever screen that character is looking at.
CONTRAST: day low; night medium   FILL: day high; night low
WHAT STAYS DARK: by day almost nothing. At night, still nothing is hidden in Iona's room:
         the script says "She can see every corner of it", so corners are dim but readable
PALETTE: white, pale grey, faint green; skin + ACCENT: blue OSTREL stitching on the blanket (8), grey growth
         on the monitor (9, 10), later the rings (22)
LIGHT CUES: 10 - the screen goes dark when Jude switches it off; 11 - the needle climbs in an
         unchanged room: the light must NOT change when the figure arrives; 23 - "The lights low."
CONTINUITY LOCKS: glass reflections kept low enough that faces through the glass are readable;
         window side of each room fixed; same panel color in every room
```

In 11, resist the stock horror moves (a flicker, a light failure, a cold color shift, a figure lurking in a dark corner) when the figure appears: the script's horror is that "The room is empty. She can see every corner of it", and then the figure is simply there. Unchanged, dim, even light, with nowhere for anything to hide, makes that worse, not better.

**The ship, written out in full:**

```
LOCATION: The ship (service cavity, human rooms, collection room, outer recess, ledge)
TIME/WEATHER: no day or night; the ship's power is the weather
STORY JOB OF THIS PLACE: an alien place that has been caring for humans badly but sincerely
SOURCES: Iona's suit lamps (cool white, hard, move with her head; the main key);
         stars below through low windows (points, no fill); instrument lights (radio green,
         shell red/green, visor graphics); the figure's pale strip (soft, weak, moves);
         the ship's own dim ambient light, tied to its hum; Nell's bedside light (see below)
NEUTRAL WHITE: Iona's suit lamps
KEY RULE: low-key; her lamps light whatever she looks at; the ship's ambient light is just
          enough to show shapes at the chamber's far end
CONTRAST: high to extreme   FILL: low
WHAT STAYS DARK: the chamber's far end until "something black comes into the light";
         the inside of the figure until the chest opens
PALETTE: blue-black, matte black, glass + ACCENT: signal red and green only on lights and
         displays; the blue sleeve in the collection room
LIGHT CUES: the pale strip dims when the figure gives up its cell; the hum wavers and misses
         a beat (let the ship's ambient light dip with it, once each time, no flicker loop);
         the fire; "The last light along its side goes out."
CONTINUITY LOCKS: Iona's white pressure suit is the brightest surface in every shot: set
         exposure for her face and keep visible fabric detail in the suit; a small light inside
         her helmet (or the glow of her visor display) lights her face in every close-up
```

Two ship details need a decision. First, **Nell's warm light**: give Nell's room a warmer, softer light than human quarantine ever had, because the ship has cared for her for nineteen years, but motivate it with an ordinary human object the ship has fetched for her (Nell says "It brings what I draw, if it can find it"), such as a bedside lamp from our world, not an unexplained golden glow. Second, **the helmet**: a visor reflects everything in front of it. In each helmet close-up decide whether the visor shows the face (light inside the helmet, dark surroundings) or the world (bright reflections, face hidden). The fire scene needs the face.

**The other locations, in short form** (sequence numbers refer to the color script in 8.5):

| Location | Sources (story world) | Key rule | What stays dark | Notes |
|---|---|---|---|---|
| Freight shaft (2) | Flashlight in Iona's teeth; thin warm lines under each landing gate (about 2,700-3,000 K) | Light moves with her head: "Her light goes onto each rung before her hand does" | Above, below, between gates | The warm slits are other people's ordinary lives, glimpsed and passed. The yellow stripe appears only when the torch finds it. |
| Treatment floor, night (3) | Ceiling fluorescents, about 4,000 K, slight green cast | Top light, fill from white floors; high-key but cold | Almost nothing, which is the point | Plan window reflections so Eli is readable through the glass. |
| Street and car (6) | One streetlight type, chosen once: white LED (cool, modern Britain; recommended) or low-pressure sodium (yellow-orange, drains every other color); shop signs; dashboard glow; headlights; the bus; one red traffic light | Pools of streetlight passing over faces; the dashboard glow as a faint light from below on the driver | Back seat between pools | Recommended: white LED, so the red traffic light is the only saturated color, which keeps red as the limit. If you choose sodium instead, the whole street goes one orange and the scene becomes a warm/cool split: name the opposition it stands for (Rule 16) or do not choose it. The script does not say where Eli sits, but the likeliest reading reconciles its two clues: Jude has the back seat, so Eli is in the front passenger seat, "twisted round" to hold the sleeve on Jude; his face then points toward the back of the car, where the rear-view mirror can catch his eyes, and Iona chooses the mirror rather than turning to look at him. Record the decision in the plan, because it decides the mirror shot. See Example 3. |
| Saye's kitchen (7) | The lamp Iona holds (warm, about 2,700 K); the window before dawn (see note) | Lamp is key for everyone; window is a cool backlight | Room corners; the empty walls | The mint is the only living color. It sits on the windowsill, so against a bright window it becomes a dark silhouette and its green is lost: let the lamp reach the pot, or let the green first read when Saye holds the leaf out into the lamplight. "Before dawn" at four in the morning may still be full dark: either a faint blue sky, or a black window that reflects the lamp and the room. The black mirror-window would double the scene's mirror idea; use it only if it stays in the background and is never pointed at. See Example 2. |
| Quarantine (8-12, 22-23) | See the full plan above | Day flat and even; night screen-lit faces in a dimmed room | Little by day; at night corners dim but readable | If the setting is British, as "torch" and "night bus" suggest, emergency vehicles use blue warning lights; a red-and-blue light bar reads as American. Frosted glass softens and spreads the flashes but does not slow them; by day they are faint, so they read best on the ceiling or on the shadow side of the room. |
| Receiving room, the passage (13, 21) | Frosted daylight; police lights beyond frosted windows (13); work lights | Flat, even, observed | "Through the tall opening with the bright sill: the dark of the shaft" | Same concrete as the maintenance passage (5), now bright: the place of the escape becomes the place of the decision. Keep the dark shaft visible through the opening in the wides, as the one dark shape in a bright room. |
| Ship (14-19) | See the full plan above | Low-key; her lamps light whatever she looks at | The chamber's far end; the figure until it arrives | The collection-room fire is the film's hottest, most saturated light (Example 4). |
| Beside the ship, the void (20) | Helmet lamp; stars; visor graphics; the ship's own lights until they go out | Visor graphics are the only color; stars are points, not a glowing nebula | Everything else | "BLACK. Not distance. Not sky. Nothing." means black with no stars and no ambient light; only her lit gloves and the vessel remain ("Her own two gloves in her helmet light"). |

---

## 6. Translation table: story meaning to light and color

Use this table to propose choices. Always check the choice against the film's own system (Section 8) before adopting it.

| Story meaning / story value change | Light choices | Color choices | Reference (film or *The Catch*) | Watch-out |
|---|---|---|---|---|
| Safety, home, belonging | Soft, warm practicals; medium-low contrast; eye light on everyone | Warm analogous palette; moderate saturation | Saye's lamp over the kitchen table | Warm glow on everything reads as a greeting card. |
| Threat hidden | Low-key; strong falloff; unseen areas; backlight without key | Desaturated, cool or neutral | Loading tunnel: only the torch pool | Too dark to read what matters. |
| Threat revealed | A light cue that exposes: door opens, torch finds it, flash | A sudden accent appears | Torch finds the empty brake brackets | Lightning-flash reveal is a cliché. |
| Secret or withholding | Top light or side light; eyes in shadow; the hidden hand kept dark | Muted | Willis on Brando; Eli's hand behind Jude's back in the cage | Keep the secret readable as a secret: we should see that something is hidden. |
| Revelation of truth | Flat, even, often top-down light; everything visible | Neutral, low saturation | The flat security-camera footage in the partition scene | Flat is not dull if it contrasts with what came before. |
| Intimacy | Close, soft source; low fill but warm bounce; two faces sharing one source | Warm, low contrast of hue | Quarantine, day (22): the two chairs drawn up to the glass, both faces in the same soft window light | Candle equals romance is a cliché. |
| Isolation | Pools of light separated by dark; the character outside the pool | Cool, desaturated; one small warm accent that they cannot reach | Iona alone in her room watching Jude on a tablet | Sad blue wash on everything. |
| Institutional control | Top light, flat fluorescents, even exposure, no shadows | White, grey, pale green; low saturation | Treatment floor; quarantine | Flickering fluorescent tubes are a horror cliché. |
| Contamination, wrongness, the uncanny | Normal light that is subtly off: wrong direction, wrong side, wrong color for the source | A familiar color that no longer means what it did (a green leaf that no longer tastes of mint) | The mint that tastes "Not mint"; backwards green exit sign | Heavy green tint for "sick". |
| Moral division, a choice | Split or strong side light; two sources of different color on one face | Complementary pair on one face | Iona between the green way home on her visor and the red fire | Split light as a permanent "villain" label. |
| Power, dominance | Figure higher, backlit or top-lit; others in its light or shadow | Deep, saturated, dark values | The figure standing "Taller than the door" in Iona's room | Backlit silhouette plus smoke as default villain entrance. |
| Powerlessness, being observed | Lit by others' devices: monitors, tablets, security cameras | Screen color on the face | Iona lit by the tablet as Jude vanishes | Screen-glow faces everywhere. |
| Grief, loss | Soft, low contrast; light that leaves (a light going out) | Desaturated; one remembered color | "The last light along its side goes out." | Rain-on-window grief. |
| Hope, return | Light increases or warms; a source reappears | Saturation or warmth rises a step | Receiving room after the void | Sunrise as the default "hope". |
| The other world, the unknown | Unfamiliar source (no visible origin); stars below instead of above | A hue the film has not used yet | Ship: "Stars. Below her feet." | Glowing magic blue. |
| Care | The carer is the source, or the carer holds the light for someone | Warm light on the cared-for | Iona holds the lamp; Iona's helmet lamp on the animal | The halo. |
| Sacrifice | A chosen color is removed or a light goes out on the character | Accent disappears | Iona deletes the green way home | Slow-motion backlit sacrifice. |
| Relief / aftermath | Contrast drops; light becomes even and quiet | Saturation falls | Ending: "The lights low." | Relief that looks like the opening. |
| Peace with an open question | Calm, low light overall, but the unresolved thing stays lit and readable | Warm or neutral dominant; one cool, pale accent on the unresolved thing | Final scene: "The cloudy growth behind the scrap of shirt fills half the container now." | Letting the whole frame go cosy and golden, which tells the audience the story is over when the script says something is still growing. |
| Unchanged world, changed person | Keep the light exactly as it was; change only the face or the action | Keep the palette exactly as it was | The mint: "Nothing has happened to the mint." | Adding a light cue or a color shift to "help" the moment. |
| Story value turning positive to negative | Contrast rises, source narrows, warm to cool | Accent turns from green to red | On the ledge, after the outlines have gone green, "Her projected outline turns red"; the shell light "turns RED" when Eli joins Nell on the bed | Mid-shot changes without a source. |
| Story value turning negative to positive | Contrast falls, a warm source appears, eye light returns | Red accent turns green | Visor outlines turn green when she takes the vessel | Too-neat sync with dialogue. |

---

## 7. Decision rules

Each rule is written "If... then consider... because...". "Consider" is deliberate: the rule proposes; the story decides. In practice, **apply a "consider" rule by default unless the script contradicts it or a higher-priority rule below conflicts with it,** and name the rule you applied (or overrode) in the shot's WHY line.

**When rules conflict, use this order (highest first):**
- **Level 1.** Light and color the script states (Rule 3; the inventory in Section 5.1). Never drop or contradict them.
- **Level 2.** Readability of the beat: the audience can see what the beat needs (Rules 5, 23, 24, 27).
- **Level 3.** The film's own motif code (Section 8.4): a motif color appears only where its meaning applies.
- **Level 4.** The color script's curve (Section 8.5): the scene's value, saturation and contrast sit where the row says.
- **Level 5.** Location continuity (the location plan and Rules 20-22).
- **Level 6.** The translation table's defaults (Section 6).

Example: Rule 10 (a light cue at the turn) against the mint beat in the kitchen. The script says "Nothing has happened to the mint", so level 1 wins and the light does not change.

**Sources and motivation**

1. **If** a scene is set at night indoors, **then consider** naming one practical as the key and letting everything else fall off from it, **because** a single clear source reads as real and gives the scene a center.
2. **If** a character carries the light (torch, lamp, phone), **then consider** making their light the key for everything they look at, **because** the audience then sees only what the character chooses to see, which ties attention to point of view.
3. **If** a light source is mentioned in the text, **then** it must appear or be clearly motivated in the shots, **because** script-mandated light is part of the story, not decoration.
4. **If** you want an unmotivated light (a glow with no source), **then consider** confining it to a moment the story marks as outside ordinary time (the turn, the void, a dream), **because** audiences sense sourceless light as unreal and you should spend that feeling deliberately.

**Faces and eyes**

5. **If** the audience must read a character's thought, **then** keep an eye light and a fill level that shows the eyes, **because** the eyes carry most of a close-up's information.
6. **If** a character is hiding something from another character but not from the audience, **then consider** hiding a body part or object, not the face, **because** we must see that they are hiding, and we need their face to see it. (Eli's hand, not Eli's eyes.)
7. **If** a character is withholding from the audience too, **then consider** top light or side light that loses one or both eyes, **because** withheld eyes withhold interiority.
8. **If** two characters mirror each other, **then consider** lighting them symmetrically from a single source between them, **because** mirrored light makes the mirror visible (Example 2).

**Contrast and structure**

9. **If** a sequence is building toward a climax, **then** give it a saturation score at least one point lower (on the 1-5 color-script scale) than the climax it leads to, or a contrast band at least one band lower (low, medium, high, extreme), in whichever component the color script says the climax peaks in, **because** Block's contrast principle means intensity needs somewhere to rise to.
10. **If** a scene contains a turning point **and** a story-world source can plausibly change at that moment (a door opens, a screen switches off, a lamp is set down, a machine falters, a signal light changes), **then consider** a single light cue at the turn, **because** a change in light marks the story value change without dialogue. **If** no source can change, or the script's point is that the world has not changed (the mint in the kitchen; the figure's arrival in Iona's room in 11), **then** keep the light fixed and let the face, the staging and the edit carry the turn.
11. **If** a revelation is emotionally large, **then consider** making it happen in the flattest, least dramatic light available, **because** truth that arrives in ordinary light feels undeniable, and the contrast with prior drama does the work.
12. **If** a scene is already loud (gunfire, falling, shouting), **then consider** simplifying the light to one rhythm or one source, **because** visual chaos on top of story chaos reduces clarity, not intensity.
13. **If** the story has two worlds (inside/outside, human/alien, before/after), **then consider** giving each a distinct lighting logic and letting them meet only at boundaries, **because** the audience learns the code and feels crossings. (Willis's dark office versus the bright wedding in *The Godfather*.)

**Color**

14. **If** a color is going to be a motif, **then** keep the rest of the palette low in saturation around it, **because** an accent only reads against affinity.
15. **If** a motif color must be visible under a location's light, **then** check surface times light: make the object self-lit, or change the location's light, **because** colored light can erase a surface color.
16. **If** you are tempted to use a warm/cool split, **then** name the opposition in the story it represents, **because** otherwise it is the teal-and-orange default.
17. **If** a color meaning is borrowed from a book of associations, **then** confirm that the film's earlier scenes have taught it, **because** color meaning is learned in context.
18. **If** a motif appears at a turning point, **then consider** inverting it once (the "safe" green that proves danger), **because** a single inversion lands harder than repetition.
19. **If** the setting is a real culture or place, **then** check the real colors of its signals (British emergency lights are blue; streetlights differ by city and decade), **because** wrong local color breaks belief.

**Consistency and continuity**

20. **If** a scene covers more than one shot, **then** fix the key side relative to the set (for example, "the window is frame-left in the wide"), and keep it when the camera turns, **because** accidental key flips read as continuity errors.
21. **If** the story itself contains a reversal of the world (such as the mirror turn in *The Catch*), **then consider** a deliberate, consistent flip of one lighting convention at that moment (the side the key comes from on the protagonist in her close-ups), **because** a subtle, lawful flip can make the audience feel wrongness before they notice it. Keep it lawful or it will look like an error. To make it lawful: write in the color script the key side for the protagonist's close-ups before the turn (for example, frame-left in sequences 1-4) and after it (frame-right from the BLACK in sequence 4 onward), apply it to every close-up in every later sequence, and check it on every shot. **If** the pipeline cannot hold the key side reliably (AI models follow direction only partly, Section 13.2), **then** skip this rule; an inconsistent flip is worse than none, and the script's backwards letters already carry the wrongness.
22. **If** time passes within a location (night to dawn), **then** plan the light's progression in steps and assign each shot a step, **because** random drift reads as error.

**Darkness and exposure**

23. **If** a scene is very dark, **then** keep at least one readable element per shot (a rim, an eye light, a lit hand), **because** "too dark to follow" breaks story comprehension.
24. **If** the scene includes dark skin tones in low light, **then** set exposure and fill to render that skin richly, and prefer soft bounce and careful eye light over simply adding front light, **because** defaults that expose for pale skin flatten or lose darker skin (a lesson drawn from cinematographers such as Bradford Young). **In a prompt,** name the skin tone and describe the light on it ("deep brown skin, warm highlights on the cheekbones and forehead, a soft sheen, detail visible on the shadow side of the face"). **When checking a generated frame,** reject it if darker skin has gone grey, ashy, flat or lost in the shadows while lighter skin in the same frame looks correct.
25. **If** an object is matte black (the figure, the puck, the engines), **then** light it with backlight or rim, and put it against something slightly lighter, **because** matte black only shows its shape by its edges.
25a. **If** an object is transparent or almost clear (the animal, "Almost clear"; the glass vessel of "dark water"; the clear shells; the cracked transparent cover), **then** light it from behind or from the side so its edges, limbs and inner structure catch thin lines of light against something darker, **because** a clear object lit from the front shows only reflections of the lamp and disappears. In a helmet-lamp scene (19, 20), that means angling the vessel so her lamp skims across it, not straight into it; in 19 the script's own "lit loop of tube" inside the open chest can serve as the backlight while the vessel still hangs in its mount.

**Machines, suits and screens**

26. **If** a place's light comes from a machine (a ship, a factory, a generator), **then** tie its light to the machine's state: when the script says the power falters ("The hum under the floor wavers", "The hum misses a beat"), dip the light once at that moment, and when the machine dies, let its lights die ("The last light along its side goes out"), **because** light that follows the machine is motivated and needs no explanation. Do not add flicker at any other time.
27. **If** a character wears a helmet with a visor, **then** in every close-up give the face its own motivated light inside the helmet (a small interior lamp or the glow of the visor display) and decide whether the visor shows the face or reflections of the world, **because** a visor otherwise turns into a mirror and the audience loses the face exactly when it matters.
28. **If** one costume or object is much brighter than everything else in the frame (a white pressure suit in a dark ship), **then** set the exposure for the face and keep detail in the bright object ("white suit with visible fabric seams"), **because** otherwise the object glows as a featureless white shape and pulls the eye away from the face.
29. **If** a screen or display lights a face, **then** match the light's color to what is on the screen (the green way home, the grey dish footage), and let it change when the picture changes, **because** screen light that does not follow the picture looks like a generic "blue glow".

---

## 8. Color scripts

### 8.1 Where the practice comes from

A color script is a row of small paintings, one per scene or sequence, that shows the whole film's color and light arc before production. Ralph Eggleston (1965-2022) brought the practice to Pixar on *Toy Story* (1995). He had already used quick pastels as art director of *FernGully: The Last Rainforest* (1992) to show producers a sequence's color and mood fast, and he called color scripts "an efficient way to convey color, light, emotion, and mood" (Cartoon Brew obituary). For *Toy Story* he made small pastel drawings of each scene, concentrating on the basic color; director John Lasseter, who had never seen a color script before, recalled in the MoMA audio guide that "I could see how the colors got more intense when the emotions were more intense, and when things got somber, it got very muted." He went on to be production designer of *Finding Nemo*, *WALL-E*, *Inside Out* and *Incredibles 2*. Lou Romano, production designer of *The Incredibles* (2004), painted its color script in flat, abstract shapes of strong color rather than rendered scenes (early versions in gouache, an opaque water-based paint, the final one digitally); in an interview he described a color script as "part inspiration and part continuity", adding that "those big ideas should always be clear and present, especially when surrounded by all the secondary beats and details." The Museum of Modern Art showed Pixar color scripts (in *Pixar: 20 Years of Animation*, 2005-2006), and Amid Amidi's *The Art of Pixar: The Complete Colorscripts and Select Art from 25 Years of Animation* (Chronicle Books, 2011) reproduces them.

The point is not the paintings. It is seeing, at a glance, whether the color and light rise and fall with the story, where the peaks are, and whether any stretch is monotonous.

### 8.2 A text color script an LLM can write and an image model can follow

Write one row per sequence with these fields. Keep cells short; the per-shot spec adds detail later.

| Field | What to write |
|---|---|
| # / Sequence | Number and short name |
| Story value change | The story value at the start and end (for example, "control to danger") |
| Frame value (1-5) | 1 = very dark (mostly black, small lit areas); 2 = dark; 3 = middle (about half light, half shadow); 4 = light; 5 = very light (mostly bright, few shadows). The swatch prompt below uses these same five words. |
| Saturation (1-5) | 1 = near grey; 2 = muted (colors present but greyed); 3 = moderate (ordinary everyday color); 4 = strong; 5 = vivid (the film's most intense color, used once or twice) |
| Temperature | Warm / neutral / cool, or a mix ("cool with warm pocket") |
| Dominant | The main hue family of the frame |
| Accent / motif | The one or two colors allowed to stand out, and which motif they are |
| Key source | The story-world source that lights faces |
| Contrast | Low / medium / high / extreme |
| Out | How the light leaves the sequence (cut to black, light cue, match) |

**Optional visual strip.** To see the script as images, ask an image model for one flat, abstract swatch image per row. Write it in positive terms only (models tend to add whatever a prompt says to leave out, Section 13.3): "flat abstract color-field painting made only of soft blocks of color: mostly [dominant] at [value in words: very dark / dark / middle / light / very light], one small area of [accent], [contrast] contrast between the light and dark blocks". Lay the swatches side by side in sequence order. This is the cheap equivalent of the Pixar pastel strip. If a swatch comes back with figures or lettering, regenerate it; do not add "no people" to the prompt.

**Optional thumbnail strip.** If storyboards are being made, a second strip can use one tiny, rough frame per sequence (the most important shot, painted loosely) instead of pure swatches. It is still judged only on color and value, never on drawing.

### 8.3 How to write one (steps)

1. List sequences and the story value change in each (from the scene breakdown).
2. Mark the story's intensity peaks. In *The Catch*: the fall and turn; the recording confession; the fire; the void.
3. Decide the film's **color logic**: which oppositions the story contains, which motifs the text already supplies (Section 5.1), and what each will mean.
4. Assign the peaks first (highest contrast or saturation), then fill in the valleys lower, so the curve has shape.
5. Check for monotony: if three sequences in a row share the same frame value, the same saturation and the same temperature, change one of them, unless the sameness is the point and the row says why.
6. Check each motif's appearances: does it appear only where its meaning applies?
7. Write each character's color arc in one line (Section 8.4).

### 8.4 Motifs and character arcs in *The Catch*

The script already supplies a coherent signal language. The design job is to define each motif so every appearance agrees.

| Motif | Appearances in the text | Proposed meaning | Rule |
|---|---|---|---|
| **Red** | Red tag "Goods only. No persons." (a load limit), which "whips against the upside-down gate" as the cage falls away; Jude's blood in "round red beads"; the red traffic light; the suit camera's red light; the shell light "turns RED" (too heavy); the figure's red outline ("Its own red"); "Her projected outline turns red" (the crossing that would end inside rock); the cabinet "glows red" | **A limit, and its cost**: what something weighs, what cannot be carried | Red appears only as small self-lit or printed accents until the fire, which is the one time red fills the frame. |
| **Green** | The backwards fire-exit sign; "Three green lights"; the shell turns "GREEN"; the green way home on the visor; outlines "turn green"; the mint | **Fits, allowed, go** | The mint is the single inversion: a living green that proves she no longer fits. |
| **Yellow** | "A band of yellow paint" in the shaft; the "yellow line painted across the floor" of the receiving room | **The line**: where the fall ends, and the threshold she chooses to cross | Painted only, never a light. Seen by torch in the shaft; seen in daylight at the receiving room. |
| **Flat black** | The puck; the engine collar "the same flat black as the puck"; the engine heads; the cells; the figure | **The engines and their makers**: power without a face | Matte, light-absorbing; shown by rim only (Rule 25). |
| **Blue (costume)** | "a strip of blue cloth. The sleeve of her shirt" | **What Iona gave**: the sleeve pressed into Jude's wound, later kept and labeled by the figure | Iona's shirt must be established as blue from the tunnel onward, or the collection-room reveal has nothing to recall. Keep other blues (police lights, the "OSTREL" stitching on the blanket) soft, small or desaturated so hers stays distinct. Check the shirt under every light it appears in: under a cool flashlight it stays blue; under orange sodium street light it would go near black (Section 4.7). |
| **Grey growth** | The dishes "furred with grey growth"; "The grey grows over the drop and closes"; "Behind the cloth, something cloudy moves"; "The cloudy growth behind the scrap of shirt fills half the container now" | **What has turned and cannot be undone**: the life that "nothing on earth will eat" | Render it as a soft, cloudy, pale grey, never a sickly green (the stock "toxic" color would break the film's green, which means "fits"). Keep the same grey in the monitor footage (9, 10) and in the container at the end (16, 23), so the final image quietly recalls the dish. |
| **Cold white (the leak)** | "A thin WHITE JET"; "a little white crust from the jet... turns to slush on the warm tile"; "A thread of water creeps out, so cold it whitens as it goes" | **The damage Iona did, and repairs**: the animal's life leaking from the crack her cylinder made | The jet in 11 and the whitening thread in 19 should look like the same substance lit the same way (caught by a hard edge light so it sparkles against black), so the audience connects the blow with the repair without being told. |

**A design decision the text forces.** The suit camera's red light will sit on screen through much of the ship section. Either make it a deliberate member of the red family (everything she does is being measured and recorded, and the cost is being counted), or keep it tiny and dim so it does not compete with the shell light and the outlines. Choose one and record it in the location plan.

**Character color arcs (one line each).**

- **Iona:** starts as the source (her torch lights everything we see; her beam even arrives before she does, when Jude reads the tag while she is still off-screen); in the middle she is lit by other people's devices (monitors, tablets, recordings), which is how the institution holds her; on the ship she is the source again (suit lamps); at the end she sits in low light and no longer needs to hold it.
- **Eli:** almost always behind glass and in institutional light; his secret is kept in shadow (the hidden hand); his confession is lit by the screen that shows what he did; at the end his "familiar little smile" appears "on the wrong side of his face", so keep his lighting identical to earlier close-ups and let the mirrored smile carry it.
- **The figure:** opaque flat black lit only at the edges; its pale strip is its only light; when the chest opens, light passes into it for the first time, and the animal inside is "almost clear". Its arc is from silhouette to translucency.
- **Saye:** neutral, even light throughout. She never carries a light of her own; the light she controls is the monitors she turns to face the glass, so she lights other people with information while staying flat and even herself. Her one moment of warmth, taking Nell's hand, happens in the receiving room's flat light, so the warmth is in the gesture, not in the lighting.

### 8.5 Sample color script for *The Catch*

Scales: value and saturation 1-5. "Out" is the transition out of the sequence. Location details are in Section 5.4.

| # | Sequence | Story value change | Val | Sat | Temp | Dominant | Accent / motif | Key source | Contrast | Out |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Loading tunnel | routine to danger (brakes gone) | 1 | 1 | cool | wet grey-black brick | red tag | handheld flashlight | extreme | torch into her teeth; tilt up the ladder |
| 2 | Shaft climb | control to near-fall, recovered | 1 | 1 | cool with warm slits | brick, steel | yellow stripe; warm lines under gates | flashlight in her mouth | extreme | out through mesh gate into white |
| 3 | Treatment floor, Eli's room, corridor | search to rescue | 4 | 1 | cool, green cast | white, pale green-grey | Eli's skin, the flask's steel | overhead fluorescents | low | hard cut into the cage |
| 4 | Cage descent, fall, turn, catch | escape to catastrophe to reversal | 2 | 2 | cool | brick and grid | red blood beads; yellow stripe "Coming" | passing floor light: "Light, brick, light, brick" | extreme, rhythmic | BLACK (one instant); after the turn, same light arriving from the other direction |
| 5 | Maintenance passage | survival to unease | 2 | 1 | cool grey | concrete | backwards green exit sign | dim service light | medium | exterior night |
| 6 | Street and car | escape to dread | 2 | 2 | cool white LED streetlight (see 5.4) | night city, backwards signs | red traffic light on Eli's eyes in the mirror (the scene's one saturated color, sat 3 for that moment only) | passing streetlight, dashboard | high | lamp in the kitchen |
| 7 | Saye's kitchen, before dawn | hope of help to proof of wrongness | 3 | 2 | warm lamp against blue window | bare neutral kitchen | green mint | lamp held by Iona | medium-high | CUT TO BLACK; title |
| 8 | Treatment floor, morning | shock to containment | 4 | 1 | cool daylight | white, frosted glass | soft blue pulses; blue "OSTREL" | frosted daylight, fluorescents | low | through glass to demo room |
| 9 | Demonstration room | ignorance to understanding | 4 | 1 | neutral | lab grey | the backwards F; grey growth on monitor | even lab light | low | to partition |
| 10 | Glass partition: the recording | trust to betrayal to unanswerable | 3 | 1 | cool, screen-lit | grey | none; the truth is in the flat grey footage | monitor as key | rises from low to high as the scene goes on | Jude switches it off: screen goes dark |
| 11 | Iona's room, night: Jude taken; the figure | watchfulness to terror | 2 | 1 | cool, dim, even night light; tablet on her face | dim grey room, every corner visible | the pale strip; the white jet | tablet on Iona; dim night panels on the room; strip on the figure | medium: nothing is hidden, and the figure is simply there | alarm; to dawn |
| 12 | Observation room, dawn | loss to purpose | 2 | 2 | cool dawn window; black star-field on the monitor | stars on screen | Nell's old file photograph (paper or screen; the script says only "Saye opens a file") | monitor, dawn window | medium | to receiving room day |
| 13 | Receiving room: suiting up | fear to decision | 5 | 2 | neutral daylight | white suit, grey room | yellow line; red suit-camera light | flat daylight | low | she steps onto the yellow line; cut to ship |
| 14 | Ship: service cavity | arrival to awe | 1 | 1 | cold | black | stars below her feet | her suit lamps | extreme | into the dim chamber |
| 15 | Ship: human rooms | fear to strange tenderness | 2 | 2 | cool chamber, warm pocket in Nell's room | blue-black | three green radio lights; the figure "comes into the light" at the chamber's end | suit lamps; Nell's fetched human lamp | medium | to collection room |
| 16 | Collection room: the archive (includes the short outer-recess courier scene) | horror to recognition | 2 | 1 | cool | archive grey, near colorless | blue sleeve and her copied name (the only color); the cloudy growth behind the cloth | suit lamps, container reflections | high | message into courier; the courier goes |
| 17 | Human rooms: the beds leave | helplessness to letting go | 2 | 2 | cool | blue-black | shell light RED to GREEN; burnt grey cells | chamber light; shell indicator | medium-high | wrist chime; to the fire |
| 18 | Collection room: the fire | duty to sacrifice | 3 | 5 | hot white and red | white glare, red glow | green way home on visor, then deleted | the fire | extreme; the film's peak in saturation and in hue contrast (red against green) | white glare stops; the room still burns, lower and redder; fire shutter slams; smoke cut off |
| 19 | Outer recess: the chest opens | enemy to patient | 1 | 2 | cool with pale translucency | black | red and green outlines; the clear animal; the lit loop of tube; the whitening thread of water (rhymes with the white jet in 11) | helmet lamp | high | onto the ledge |
| 20 | Ledge, beside the ship, the void | falling to faith | 1 | 2 | cold | black and stars | green and red visor graphics; numbers | helmet lamp | extreme; then black twice, lit only by her helmet lamp on gloves and vessel | "Nought." BLACK |
| 21 | Receiving room: return | isolation to reunion with a catch | 4 | 1 | neutral | white, paper suits | "RECEIVING"; Eli's smile on the wrong side | flat daylight | low | to quarantine day |
| 22 | Quarantine, day: bread and rings | distance to shared life | 4 | 2 | soft neutral-warm | pale | the two rings through glass | soft daylight through glass | low | to night |
| 23 | Quarantine, night: the pump | vigilance to uneasy peace | 2 | 2 | warm, low, with one cool pale pocket | warm dark | the animal and its container; the cloudy grey growth, kept readable | the over-bed reading light, low (see the quarantine plan in 5.4); a small cool monitoring light beside the vessel | medium | CUT TO BLACK; sound of the pump |

**Why this shape.** The film opens at maximum darkness and minimum color, so the institution's flat white (3, 8, 9) reads as exposure rather than relief. Warmth is rationed: it appears first as slits under the shaft gates (other people's lives), then as the kitchen lamp (care), then as a pocket in Nell's room (the ship's care), then as the fire (the cost), and finally as the low light of the last scene. Saturation stays at 1-2 for the entire film apart from small, brief accents (the traffic light, the signal lights) so that the single saturated peak, the fire in sequence 18, is the film's visual climax, exactly where Iona gives up her way home. Light-dark contrast is already extreme in the tunnel and shaft (1, 2), so it cannot rise at the climax; saturation and red-against-green hue contrast are the components saved for it (Section 4.4). The collection room is kept near colorless before the fire (16) so the jump to 5 is as large as possible. The black in sequence 4 ("A dark with nothing in it") is the only black inside the story with no source at all; the cuts to black at the ends of 7 and 23 are editing, and the black at the end of the camera recording in 12 is on a monitor. The two blacks in sequence 20 keep one thing lit, her helmet lamp on her gloves and the vessel ("Her own two gloves in her helmet light"), so even inside "Nothing" she carries her own light, which completes her arc from the torch in the first scene. The last scene is warm and low but not closed: the cloudy grey growth in the container stays visible in a cool, pale pocket of light (motivated by a small monitoring light beside the vessel, the kind quarantine would put there), because the script ends on something still growing and a pump still going, not on a resolution.

---

## 9. Per-shot light and color spec

Each shot in the breakdown gets these two fields. Record only what differs from the location plan; write "as plan" otherwise.

```
LIGHT:  source(s) in story | key direction as a visible result (which side of the face is lit,
        high or low) | hard/soft | contrast band | backlight/rim yes/no | practicals in frame |
        what stays dark | eye light yes/no | light cue during the shot (what changes, when, why)
COLOR:  dominant hue | accent and motif (with meaning) | saturation 1-5 | frame value 1-5 |
        temperature | costume/set colors that must survive this light
WHY:    one sentence linking the choice to the beat
PROMPT: one plain-language lighting sentence for the model (Section 13)
```

---

## 10. Worked examples

### Example 1. The first image: "Torchlight on wet brick." (*The Catch*, loading tunnel)

**Text.** "Torchlight on wet brick. Cold grease. Rain that got in years ago and never left." / "A red tag is wired to the gate." / "JUDE, forties, easy in the shoulders, turns the tag to the light and reads it." / "Then she gets down on her knees and puts the light under the floor frame."

**Choice.** Iona's flashlight is the only source that lights anything we need to read (the faint spill from the tunnel mouth only gives the cage a shape). Jude has to turn the tag into her beam to read it, and at that moment Iona is still off-screen ("IONA (O.S.)"), so her light arrives before she does and the film's first line of dialogue is read in it: she is the one who sees; he depends on her. The red tag is the only saturated color in the frame, which starts teaching the audience that red means a limit ("Goods only. No persons."). When she puts the light under the floor frame, the beam rakes (skims at a low angle) across the empty brackets and the "Four bright bolt holes" catch hard highlights: metal just exposed by removing the bolts has not had time to rust or blacken, so the brightness itself is the evidence that the brakes were taken off recently. On "She stays on her knees. One breath.", the beam stops moving. That stillness is the light cue for her realization; no music sting or light change is needed.

**Why.** Rule 2 (the carrier's light is the key), Rule 14 (accent against a low-saturation palette), Principle 7 (the unlit shaft above is the threat).

**Spec for the close-up of the bolt holes.**
```
LIGHT:  Iona's flashlight, handheld, low, entering from frame-right and raking across the bracket |
        hard | extreme | no rim | no practicals | everything beyond the bracket black |
        n/a (no face) | beam settles and holds still
COLOR:  steel grey, rust | none (tag out of frame) | sat 1 | value 1 | cool white
WHY:    the beat is discovery by touch; the light shows only what her hand finds
PROMPT: "Extreme close-up of an empty, rust-brown steel bracket under an old freight elevator
        floor. Four clean threaded bolt holes shine bright silver in a single hard flashlight
        beam skimming in low from the right side of the frame. A woman's fingertip rests in
        one hole. Beyond the bracket, deep black shadow and a glint of wet brick. Cold white
        light, realistic photographic film still."
```

### Example 2. The mirror across the table (*The Catch*, Saye's kitchen)

**Text.** "Jude on the table. Saye's medical case open. Iona holds the lamp." / "Hold up your right hand." / "They stand facing each other across the table like a woman and her reflection, each with the wrong hand in the air." / later: "Chew that." ... "Not mint." ... "Nothing has happened to the mint."

**Choice.** (A staging proposal; the script only says "Iona holds the lamp".) Before she raises her hand, Iona sets the lamp down on the table beside Jude, halfway between the two women. In the side-on two-shot (one frame holding both women, seen from the side), Iona is frame-left, Saye frame-right, the lamp and Jude's body between them. Each woman is lit on the side of her face that faces the lamp, so the lighting itself is a mirror image: the lit sides of the two faces turned toward each other, both raised hands catching the same warm light from below and in front. The window in the background of this two-shot adds a faint cool edge to both (or, if it is still full dark outside, stays a black pane; Section 5.4). For the mint beat, the light does **not** change. The script says "Nothing has happened to the mint", so the world stays exactly as lit; only Iona's face changes. The leaf's green reads when Saye holds it out into the lamplight; on the windowsill against the window it would be only a dark shape. It is the only saturated color in the kitchen, and it is the one "green" in the film that betrays her.

**Why.** Rule 8 (mirrored characters, symmetrical source), Rule 18 (a motif inverted once), Principle 10 (restraint: a light cue on "Not mint" would contradict the story's own logic).

### Example 3. The same question under two lights (*The Catch*, the car and the ship)

**Text, car.** "A red light. Iona finds his eyes in the mirror." / "Eli. Are we going to be all right?" / "He looks down at the flask in his hand for a long time." / "Drive."
**Text, ship.** "A light on the shell turns RED." ... "The light turns GREEN." ... "Io." ... "Are we going to be all right?" / "I don't know."

**Choice.** In the car, the red traffic light lays a faint red wash across the interior (a traffic light is weak at a distance; the wash is stronger if the windscreen is wet and scatters it). Frame Eli's eyes in the rear-view mirror, with the red on the side of his face toward the windscreen. (This needs Eli where the mirror can see him; see the seating note in Section 5.4.) When he looks down at the flask, his eyes leave the mirror, which is a small loss of eye light that matches his evasion. Keep the light red through "Drive." Do not sync the change to green with his word: that would be heavy-handed, and it would make the light answer for him. Let it hold red for a beat after he speaks, then change, and she drives. His non-answer happens entirely under the red of limit and cost, which he alone knows. On the ship the question returns with the roles reversed, and the script has already turned the shell light from red to green before Eli asks. Iona's honest "I don't know" is spoken after the shell light has turned green: permission to go exists, and there is still no promise.

**Why.** Rule 10 (one light cue at the turn), Rule 18 (the rhyme inverts the motif), Section 12 mistake "on-the-nose sync". The traffic light earns its meaning because it is ordinary and plausible; do not add a red glow in the ship scene to force the rhyme.

### Example 4. The fire and the deleted way home (*The Catch*, collection room)

**Text.** "Light fills the shelves. The cabinet's back glows red; insulation behind it curls and spits." / "On Iona's visor: her way home. Still green." / "She looks at the flask inside the outline. Leaves it there." / "She deletes the way home." / "She fires." / "The white glare stops." / "Bare bolts in the wall."

**Choice.** This is the only sequence where saturation reaches 5 (color script row 18). Two sources meet on Iona's face: the white-and-red fire from the cabinet side, and the small green glow of the way home on her visor display, lighting her face from inches away. A complementary pair on one face stages the choice (translation table: moral division). Keep the green faint, a display glow on the skin nearest the visor, not a green key light; a strong red-and-green face looks like a stage effect. When she deletes the way home, the green goes out of her face and only fire remains. When she fires, the light cue is the loss of the white glare, not a drop to darkness: the room is still burning (her visor route later leads back "across the burning room", and there is smoke until the shutter cuts it off), so what remains is lower, redder firelight from what still burns, the sparks from the parting cable, and her suit lamps on the bare bolts. On "The hum misses a beat. The deck drops beneath her", let the ship's own dim light dip once with it (Rule 26). Keep her eyes lit throughout: the audience must watch her look at the flask and leave it. Because she is in a helmet, that means light inside the helmet and a visor angled so it does not mirror the fire across her face (Rule 27).

**Why.** Block's principle: the film's greatest color contrast sits exactly on its largest story value change. Avoid the stock alternative (a slow-motion backlit silhouette against flames), which would hide the face at the moment we most need it.

### Example 5. Hidden in drama, revealed in flat light (*The Catch*, cage and recording)

**Text, live.** "Floors go by. Light, brick, light, brick." / "Eli gets one arm round Jude's chest. His other hand goes underneath. Behind Jude's back. Out of sight."
**Text, recording.** "a camera above the top gate, looking straight down the shaft. The cage is a small bright box with three small people in it." / "And in the long second of the fall, Eli's hand comes out from behind Jude's back. / Empty."

**Choice.** In the live descent, bars of landing light sweep through the open grid: the rhythm of "Light, brick, light, brick". Stage it so Eli's hidden hand always falls in the shadow of Jude's body. We see that he is hiding something (Rule 6) but not what. When Iona hits STOP, the rhythm freezes into one steady band of light on the bright sill ("A way out"); when the cage falls, the rhythm returns faster, then BLACK. After the turn, the bars pass in the opposite direction. The revelation, several sequences later, plays in the flattest image in the film: small, top-down, low-detail security footage with no modeling on anyone, "a small bright box with three small people in it" in a dark shaft. The truth appears in the least dramatic light available (Rule 11), and it lands harder because the live version was so dramatic.

### Example 6. The lamp and the unsooted ceiling (*The Long Places*, the finished room)

**Text.** "The room the lamp stood up was long and low and rounded at every corner, and it was finished." / "the ceiling was pale as the day of its cutting, and unsooted, and every ceiling Nilay had ever met in that hill wore black like a surname." / "at the hem of the light, where the polish gave back more than the flame had to give, a third shape sat, or the wall sat."

**Choice.** Prose gives no shot list, but it does give physics. The main source is small oil lamps (about 1,800-1,900 K; the descent record says "three oil lamps"), led by Melek's, which goes in first "so that the rooms would meet her before they met the light", then is set "in the empty niche at the basin's head". The text does not say how high she carries it in this room. (The keeper's rule, "The flame you carry cupped and low, near the body", is about carrying a flame to light a wick, not about carrying a lamp, so do not cite it as a lamp height.) There is also an electric source in the room: Yusuf's headlamp, which he later unclips and sets on the mat, where the elder cups his hand round "the burning lens" and names it "the little sun that doesn't burn". Treat it as a cool, hard beam kept off the far wall (a headlamp aimed at the third shape would "insist" on it) until he sets it down; the elder's cupped hand over the lens is a light cue the text itself supplies. In every earlier underground room, the soot-black ceilings absorb light, so the lamp makes a small hard pool with darkness pressing down from above. In this room, the pale ceiling and the polished walls bounce the same flame, so the room is softer and brighter from the same lamp. The lighting change shows "finished" without any added source. The third figure is placed exactly at the edge of the falloff, kept within about one stop of the wall's value, and given no rim and no eye light, so the audience, like Nilay, cannot "certify" it. Do not add a separate light on the third shape; the text calls it "the one the light would not insist on".

**Why.** Rule 4 (no unmotivated light, because this is a scene about what can be witnessed), Rule 23 (keep one readable element: the two seated figures are clear, the third is not), and the novella's recurring rule that the rooms "meet her before they met the light".

---

## 11. Checklist (run on every scene, then on every shot)

**Scene level**
- [ ] Every light and color word in the text is listed and used (Section 5.1).
- [ ] The location plan names every source, its temperature, direction and hardness.
- [ ] The scene's position in the color script is stated (frame value, saturation, temperature, contrast).
- [ ] There is at most one main light idea in the scene, and it links to the story value change.
- [ ] Any light cue happens at a turning point and has a story-world cause.
- [ ] Motif colors appear only where their defined meaning applies.
- [ ] Costume and set colors that carry meaning survive this location's light (surface times light).
- [ ] Real-world signals are locally correct (emergency lights, streetlights, signage).
- [ ] If this scene is not a peak, its contrast and saturation sit below the next peak.
- [ ] This scene and the two before it do not all share the same frame value, saturation and temperature (the monotony test in Section 8.3, step 5), unless sameness is the point and the color script says why.

**Shot level**
- [ ] The key's source is named, and its side is consistent with the wide shot.
- [ ] We can tell where to look in the first second.
- [ ] Faces we need to read have an eye light; faces we must not read have a reason.
- [ ] At least one element is readable even in the darkest shots.
- [ ] Hidden things are hidden by staging and light, and the hiding itself is readable.
- [ ] Matte black objects have rim or edge separation; clear or glass objects are lit from behind or the side (Rules 25, 25a).
- [ ] Faces inside helmets have their own motivated light, and the visor's reflections are a decision, not an accident (Rule 27).
- [ ] Any flicker or dip in light has a script cause at that exact moment (Rule 26).
- [ ] Dark skin is rendered richly (exposure and fill chosen for it).
- [ ] The COLOR field names one dominant hue and at most two accents.
- [ ] Nothing is lit that the story needs dark.
- [ ] The WHY line names a story reason, not "it looks cinematic".
- [ ] The PROMPT line uses plain visible-result language, with no negative phrasing, no contradictory lighting words, and no named cinematographer.

---

## 12. Common mistakes and how to spot them

| Mistake | How to spot it | Fix |
|---|---|---|
| **Sourceless glamour** | A face is lit brightly in a dark room and you cannot name the lamp. | Name a source, or move the character into its light. |
| **Everything evenly lit** | No shadows anywhere, every scene; the frame value is 4-5 throughout. | Decide what stays dark; drop fill. |
| **Too dark to follow** | You cannot tell who is speaking or what the hand holds. | Add a rim, an eye light, or a practical in frame; keep the dark around it. |
| **Teal-and-orange default** | Skin orange, shadows teal, in every location. | Name the story opposition or remove the split (Section 4.8). |
| **Color shouting the theme** | Red floods the frame at every threat; blue at every sadness. | Shrink color to accents; let the story teach the code. |
| **On-the-nose sync** | The light changes exactly on a line of dialogue that states the change (the light turns green on "Drive"). | Offset the cue by a beat, or let the world change it for its own reasons. |
| **Inconsistent motif** | Red means danger in one scene and love in the next, with no design reason. | Write the motif table (Section 8.4) and check every appearance. |
| **Motif wallpaper** | The motif color appears in most shots and stops being noticed. | Ration it: a few appearances, each at a meaningful beat. |
| **Stock clichés** | Lightning at a revelation; flickering hospital tubes; god rays in every church; lens flare on every hero; backlit silhouette walking away from an explosion; candles for romance; sickly green for anything contaminated; a cold blue shift when the monster appears; neon pink-and-blue for "the future". | Ask what source this place really has, and what this specific story needs. Then write the WHY line; if it could be pasted into any other film unchanged, the choice is stock. |
| **Generic "cinematic" look** | The prompt or spec says "cinematic lighting", "moody", "atmospheric", "dramatic lighting" without naming a source. | Replace each with a named source, its side, its hardness and what stays dark. |
| **Accidental key flip** | In the reverse shot, the key jumps to the other side of a face for no reason. | Fix key side relative to the set in the location plan. |
| **Time-of-day drift** | Dawn in one shot, noon in the next, dusk in the third, within one continuous scene. | Assign each shot a step in the time progression (Rule 22). |
| **Surface times light failure** | A key red object turns brown under green or orange light. | Change the light, or make the object self-lit. |
| **Wrong local color** | American red-and-blue police lights in a British setting. | Check the real signal colors (Rule 19). |
| **Heavy-handed direction** | The villain is always split-lit and under-lit; the saint always has a halo. | Let light respond to the beat, not to a character label. |
| **Contradictory prompt words** | "Soft diffused light, harsh dramatic shadows" in one prompt. | One dominant quality and one dominant temperature per prompt. |
| **The AI house look** | Frames you did not ask to be styled come back with visible light shafts in the air, a glowing rim on every figure, soft blurred discs of out-of-focus light (bokeh) in the background, wet reflective floors, and a teal-and-orange grade. | Name the real sources and describe the plain conditions in positive words: "clear air", "dry concrete floor", "background in focus", "flat even light from the ceiling panels". Keep haze, wet surfaces and rim only in the locations whose plan contains them (the wet tunnel, the smoke in the collection room). |

---

## 13. How to say this to an AI image or video model

Models change quickly, and vendors document only part of their behavior. The notes below combine vendor guides (listed in Sources, checked 2026-09-27) with widely shared practitioner experience. Treat them as starting points and test them (Section 13.5).

### 13.1 What models tend to follow

- **Named sources and conditions.** "Lit by a single candle", "a flashlight beam", "overhead fluorescent lights", "the glow of a computer monitor", "a red traffic light", "golden hour", "overcast", "blue hour", "rain at night with reflections on wet pavement". Google's Veo 3.1 guide gives examples in exactly this form, such as "The scene is lit by the harsh fluorescent overhead lights and the green glow of the monochrome monitor", and "lit by a single, dramatic spotlight from the front".
- **Quality words.** "Soft diffused light", "harsh shadows", "hard light", "dim", "bright". Kling's lighting guide recommends simple words like soft, harsh, warm, cool, bright, dim, plus direction words like side lighting, backlighting, overhead lighting and uplighting.
- **Silhouette, backlit, rim light, haze, light beams, lens flare** (the streaks and rings a bright light makes inside a camera lens). Generally recognized, sometimes over-applied: "rim light" often produces a glowing outline on every figure, and "lens flare" appears wherever a light is visible. Use each only in the shots that need it.
- **Color attached to objects.** "A small red tag on a grey steel gate" works better than "red accent".
- **Overall color treatment.** "Desaturated", "muted colors", "black and white", "monochrome blue".

### 13.2 What models follow only partly

- **Direction.** "From the left" is often ignored or mirrored. Reinforce it with the visible result: "light comes from the right side of the frame; the left half of her face is in deep shadow". Avoid "camera left" and "stage left" in prompts: in practitioner reports models read them unreliably, and even people confuse them (stage left is the actor's left, which is the audience's right). Write "the left side of the frame".
- **Low-key and high-key.** Often read simply as "dark" and "bright". Add the structure: "mostly dark frame, one pool of light on her hands".
- **Chiaroscuro and Rembrandt lighting.** Usually produce dramatic contrast but may pull the image toward an oil-painting look. Add "photographic, realistic film still" if you want a photograph.
- **Eye light.** "Catchlights in her eyes" sometimes works in image models; video models rarely hold it across a clip.
- **Light cues within a clip.** "The light turns from red to green halfway through" is hit-or-miss. Safer: generate two clips, one per state, and cut, or use first-frame and last-frame control where the tool offers it (Veo's "First and Last Frame" feature).
- **Moving sources.** A handheld flashlight or head lamp that moves through a clip often drifts: the lit patch stops following the beam, or the whole frame brightens. Keep beam movement slow and simple, one moving source per clip, and describe where the pool of light is at the start and where it ends.
- **Flicker.** Video models sometimes add unwanted brightness flicker from frame to frame, especially in dark scenes. Check every dark clip at full screen; if it flickers, regenerate it or smooth it in the grade (Section 13.4, step 7; DaVinci Resolve's paid Studio version also has a deflicker tool).

### 13.3 What models usually ignore or misread

- **Kelvin numbers, ratios, stops.** "3200K" or "8:1" rarely produce the precise effect; at most they nudge warm or cool. Say "warm orange lamplight" or "cold bluish-white light".
- **Rig words.** "Negative fill", "bounce", "motivated", "short lighting", "fill ratio". Describe the result instead.
- **"Practical" as a noun.** The crew meaning ("a working lamp visible in the frame") is rare in ordinary captions, so a model may read "practical" as the everyday adjective or ignore it. Write the object: "a table lamp, switched on, visible in the frame".
- **Negative phrasing.** "No blue" can add blue. Runway's guides state that negative phrasing is not supported and may produce the opposite; use positive phrasing: "only grey and black tones, one small red tag".
- **British "torch".** Can produce a flaming torch. Write "flashlight".
- **Named cinematographers.** "Lit like Roger Deakins" tends to produce a generic "cinematic" look, and some platforms restrict names. Describe the qualities you want.
- **Exact colors by code.** Hex codes are not reliably reproduced; use a reference image or a style reference instead.
- **Contradictions.** "Soft diffused light" with "razor-sharp shadows" confuses the model; Kling's guide warns against such contradictory pairs and advises sticking to a single dominant color temperature within a scene. Where the story needs two temperatures (the lamp and the dawn window), say which one dominates and where the other one appears ("warm lamplight on both faces; a thin strip of cold blue from the window behind them").

### 13.3a Verdicts on four phrases people often try

These verdicts come from vendor guides plus practitioner reports, not controlled tests; confirm them with the probe in 13.5.

| Phrase tried | Verdict | Write instead |
|---|---|---|
| "single hard light from camera left" | "Single" and "hard" usually work; "camera left" is unreliable and may be mirrored. | "One hard light from the left side of the frame; crisp shadows; the right half of his face in deep shadow." |
| "practical lamp" | Often ignored or read loosely; the model may add a lamp but not light the scene from it. | "A table lamp, switched on, visible in the frame; it is the only light in the room; warm light falls off into darkness a few feet from it." |
| "low-key" | Usually read as "dark" or "moody" overall, without a clear structure of lit and unlit areas. | "Mostly dark frame; one pool of light on her hands and the tag; the rest falls to near black." |
| "rim light" | Well recognized, often over-applied: a glowing outline appears on every figure, even where no source could make one. | "A thin line of light along his shoulder and hair from the window behind him," and use it only in shots whose location plan has a source behind the subject. |

### 13.4 Keeping light consistent across separately generated shots

1. **Write a location lighting block** (two or three sentences from the location plan) and paste it unchanged into every prompt for that location. Put shot-specific changes after it.
2. **Generate a key frame per location first** (a single approved still image that fixes the look of the place), approve it, then use it as the input image or reference for every shot there. Runway's Gen-4 video guide says the input image conveys subjects, composition, colors, lighting and style, so the text prompt can focus on motion. Veo offers reference images ("Ingredients to Video") to keep an aesthetic consistent across shots. In Midjourney, a style reference (`--sref`) carries color, texture and lighting from a reference image.
3. **Keep the camera on the same side of the source** within a scene, so the key side stays stable.
4. **Chain continuous shots.** When one shot continues straight into the next (the cage descent, the fall), use the last frame of the approved clip as the first frame of the next clip. The light carries across exactly.
5. **Use Blender for light control when it matters.** Block out the set with simple shapes, put in a Sun light (its Angle setting sets how large the sun looks, and so how soft its shadows are) or Area lights (their size controls softness), and set each light's color by typing its kelvin value into the light's Temperature field (Blender 4.5 and later have this on every light; older versions need a Blackbody node in the light's node setup, and light node setups work only in Cycles, Blender's slower, physically accurate renderer). Render rough frames per shot. A plain grey render is not a usable first frame for a video model, because the model will keep it grey. Instead, either (a) turn the render into a finished still with an image model that can follow the render's structure (an image-editing model given the render plus a text description, or a depth-guided workflow in a tool such as ComfyUI, a free program for running open-source image and video models, where a depth map is a greyscale image recording how far each point is from the camera), approve that still, and use it as the first frame; or (b) feed the rough animation to a video-to-video tool that restyles footage while keeping its layout and light. This fixes direction and falloff, which text alone does poorly.
6. **Relight instead of regenerating.** Relighting tools take an existing image or clip and change its light direction or color: for stills, the open-source IC-Light models (which run in tools such as ComfyUI) and the relight functions in some image editors; for video, some video-to-video editing models accept an instruction such as "make the light come from the left, warm lamplight". Use them to rescue a good shot whose light is wrong. Tools change fast; check the current list in C1 and C2.
7. **Grade afterwards.** Put all clips of a sequence into one grading timeline (DaVinci Resolve has a free version) and match them to the approved key frame. A common grade hides small differences between clips.
8. **Test before scaling.** See 13.5.

### 13.5 A four-shot lighting probe

Before generating a whole scene, generate four shots of one location: a wide (the whole space), a medium (a figure from about the waist up), a close-up (a face), and a reverse (the same moment seen from the opposite direction). Check: does the key stay on the same side; does the dark stay dark; do the motif colors survive; does the temperature match? Fix the lighting block, then generate the rest.

### 13.6 Phrasebook: breakdown term to model phrase

| Breakdown term | Plain phrase for the model |
|---|---|
| Low-key, single practical | "a mostly dark room lit only by one small lamp on the table" |
| High-key institutional | "evenly lit by bright overhead fluorescent lights, almost no shadows, white walls" |
| Hard side key, high contrast | "hard light from the right side of the frame; the left half of the face falls into deep shadow" |
| Backlight and rim on a dark figure | "a tall black figure seen against a slightly lighter wall, a thin line of light along its shoulders and head" |
| Motivated under light from a screen | "her face lit from below by the glow of the tablet she is holding" |
| Falloff pool | "a small pool of flashlight on the wet bricks, darkness all around" |
| Pre-dawn mixed temperature | "warm lamplight on the faces, cold blue dawn light in the window behind them" |
| Frosted-glass emergency lights (British) | "faint, soft flashes of blue light on the ceiling, coming through frosted windows" |
| Motif accent | "a small bright red tag, the only color in a grey scene" |
| Face in a helmet | "her face inside the helmet lit softly by the green glow of the display on her visor; the visor glass clear, with only a faint reflection" |
| Bright costume in a dark place | "a white pressure suit with visible seams and fabric texture, not glowing" |
| Screen light matching the picture | "her face lit from the front by the grey-green glow of the video on the monitor" |
| Night room with nothing hidden | "a dim hospital room at night, low even light, every corner of the room visible" |
| Almost-clear creature in dark water (Rule 25a) | "a small, almost transparent sea creature inside a glass jar of dark water, lit from behind and to the side so its edges and thin limbs glow faintly against the dark water" |
| True black | Do not generate it; cut to black in editing. Generated "black" frames usually contain noise, shapes or a glow. |

---

## 14. Sources

**Books**
- Bruce Block, *The Visual Story: Creating the Visual Structure of Film, TV and Digital Media* (Focal Press; first edition 2001, later revised editions). Contrast and affinity; hue, saturation, brightness; story and visual intensity.
- Patti Bellantoni, *If It's Purple, Someone's Gonna Die: The Power of Color in Visual Storytelling* (Focal Press, 2005).
- Vittorio Storaro, *Writing with Light* (three volumes: *The Light*, *The Colors*, *The Elements*; Aperture / Electa; first volume 2002).
- Josef Albers, *Interaction of Color* (Yale University Press, 1963).
- Johannes Itten, *The Art of Color* (1961).
- John Alton, *Painting with Light* (1949; University of California Press reprint).
- Blain Brown, *Motion Picture and Video Lighting*, 3rd edition (Routledge, 2018).
- Dennis Schaefer and Larry Salvato, *Masters of Light: Conversations with Contemporary Cinematographers* (University of California Press, 1984; later reissued). Includes interviews with Gordon Willis, Conrad Hall and Vittorio Storaro.
- Amid Amidi, *The Art of Pixar: The Complete Colorscripts and Select Art from 25 Years of Animation* (Chronicle Books, 2011).
- Robert McKee, *Story* (1997) and *Dialogue* (Grand Central, 2016), for the idea of a story value changing charge within a scene, used throughout this pipeline.

**Web (all checked 2026-09-27)**
- Roger Deakins, "Looking at Lighting: 3 Sequences, *The Assassination of Jesse James*": https://www.rogerdeakins.com/jesse-james-x-3/ (source of the two short Deakins quotations and the saloon and undertaker rig details; re-checked 2026-09-27).
- TCM, "The Last Emperor" (Storaro's color progression): https://www.tcm.com/articles/21409/the-last-emperor (re-checked 2026-09-27).
- Storaro on *Apocalypse Now* (artificial light over natural light): https://scrapsfromtheloft.com/movies/apocalypse-now-interview-vittorio-storaro/ (returned 403 on re-check; the claim is widely reported in Storaro interviews). ASC, "Apocalypse Now: A Clash of Cultures": https://theasc.com/article/flashback-apocalypse-now/ (read via search summaries: the concept of one culture superimposing itself on another; artificial colored smoke against the natural colors of the jungle).
- Wikipedia, "Gordon Willis" (nickname from Conrad Hall; Brando's make-up lit from above; the "light to dark" quotation): https://en.wikipedia.org/wiki/Gordon_Willis. The NYFA post "Remembering Cinematography's Prince of Darkness" (https://www.nyfa.edu/film-school-blog/remembering-cinematographys-prince-darkness/) confirms the nickname but does not name who gave it.
- Wikipedia, "Vittorio Storaro" (first volume of *Writing with Light*, 2002; Goethe as the basis of his color philosophy): https://en.wikipedia.org/wiki/Vittorio_Storaro
- American Society of Cinematographers, "Robby Müller and *Paris, Texas*": https://theasc.com/article/robby-muller-paris-texas/ (page returned no text on re-check).
- Criterion Collection, "Robby Müller, 'Master of Light,' Dies at Seventy-Eight" (Wenders on *The American Friend*: "We're going to keep them all"; the lab anecdote; "The things that other people took out as mistakes we used as a virtue"; from a video for the 2016 EYE Filmmuseum exhibition; checked 2026-09-27): https://www.criterion.com/current/posts/5781-robby-m-ller-master-of-light-dies-at-seventy-eight
- ASC, "Shot Craft: Eye Lights" (eye light as the specular reflection in the eye; Lucien Ballard, Merle Oberon, *The Lodger*, the "Obie"; checked 2026-09-27): https://theasc.com/article/shot-craft-eye-lights/
- Wikipedia, "The Matrix" (green bias inside the simulation, blue in the real world; Bill Pope and Owen Paterson; checked 2026-09-27): https://en.wikipedia.org/wiki/The_Matrix. Wikipedia, "Traffic (2000 film)" (a different look per storyline and Soderbergh's reason; checked 2026-09-27): https://en.wikipedia.org/wiki/Traffic_(2000_film)
- Wikipedia, "Bradford Young" also supports the "shooting into" light and available-light claims (checked 2026-09-27).
- Wikipedia, "Bradford Young" (first African American Oscar nominee for cinematography, for *Arrival*; available light; the *Pariah* bedroom lit by Christmas lights and a red-shaded lamp): https://en.wikipedia.org/wiki/Bradford_Young. Variety (2017) on the nomination: https://variety.com/2017/film/awards/bradford-young-arrival-oscar-han-solo-1201988626/ (paywalled on re-check).
- Frame.io Insider, "The Cinematography of *Dune: Part Two*" (infrared ALEXAs, the black sun, the Arrakis comparison quoted in Section 3; re-checked 2026-09-27): https://blog.frame.io/2024/04/15/the-cinematography-of-dune-2-part-two-greig-fraser/ and IndieWire on the infrared camera: https://www.indiewire.com/features/craft/dune-2-cinematography-infrared-denis-villeneuve-1234967060/ (read via search summaries).
- Wikipedia, "In Cold Blood (film)" (Hall noticed the rain-shadow "tears" in rehearsal and called it "purely a visual accident"): https://en.wikipedia.org/wiki/In_Cold_Blood_(film). Also PremiumBeat and ASC: https://www.premiumbeat.com/blog/iconic-cinematography-conrad-hall/ and https://theasc.com/article/wrap-shot-in-cold-blood-2/ (read via search summaries).
- Cartoon Brew obituary of Ralph Eggleston (color scripts at Pixar, *FernGully* pastels, "an efficient way to convey color, light, emotion, and mood", production design credits; re-checked 2026-09-27): https://www.cartoonbrew.com/rip/ralph-eggleston-a-cornerstone-of-pixars-visual-style-dies-at-56-220781.html
- Thunder Chunky interview with Lou Romano on color scripts ("part inspiration and part continuity"; re-checked 2026-09-27): https://www.thunderchunky.co.uk/articles/pixar-colour-and-tent-poles-with-lou-romano/
- MoMA audio guide, "Colorscript. *The Incredibles*, 2004": https://www.moma.org/audio/playlist/192/2575 (blocked on re-check). MoMA audio guide, "Colorscript (detail). *Toy Story*, 1995" (John Lasseter: "I could see how the colors got more intense when the emotions were more intense, and when things got somber, it got very muted"): https://www.moma.org/audio/playlist/192/2581 (page blocked on direct fetch; wording confirmed through search results quoting it, 2026-09-27). The gouache-then-digital versions of Romano's *Incredibles* color script are from search summaries of museum and blog captions.
- Routledge page for Bellantoni's book (basis of claims, author's study with Josef Albers, AFI teaching, table of contents; re-checked 2026-09-27): https://www.routledge.com/If-Its-Purple-Someones-Gonna-Die-The-Power-of-Color-in-Visual-Storytelling/Bellantoni/p/book/9780240806884
- Shyamalan on red in *The Sixth Sense*: DVD featurette "Rules and Clues" (Hollywood Pictures Home Video, 2000), as quoted in Wikipedia, "The Sixth Sense": https://en.wikipedia.org/wiki/The_Sixth_Sense. (The No Film School article "Seeing Red", https://nofilmschool.com/the-sixth-sense-red-symbolism, analyzes the red but does not quote Shyamalan.)
- Todd Miro, "Teal and Orange - Hollywood, Please Stop the Madness" (2010): http://theabyssgazes.blogspot.com/2010/03/teal-and-orange-hollywood-please-stop.html
- Google Cloud, "Ultimate prompting guide for Veo 3.1" (lighting example sentences, Ingredients to Video, First and Last Frame; re-checked 2026-09-27): https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1
- Runway, "Gen-4 Video Prompting Guide": https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide (direct fetch returned 403; content taken from search-result summaries of the page).
- Kling AI, "AI Video Lighting Prompts": https://kling.ai/blog/professional-ai-video-lighting-techniques-tips (re-checked 2026-09-27: simple quality and direction words; avoid contradictory pairs; a single dominant color temperature "within the same scene").
- Midjourney documentation, "Style Reference": https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference (read via search summaries).
- Blender Manual, "Light Objects" (per-light Temperature in kelvin; Sun Angle; Area light size and soft shadows; re-checked 2026-09-27 against the 5.2 LTS manual; the per-light Temperature control arrived in Blender 4.5): https://docs.blender.org/manual/en/latest/render/lights/light_object.html. (The older Blackbody Node page URL, https://docs.blender.org/manual/en/latest/render/shader_nodes/converter/blackbody.html, now returns 404.)
- IC-Light (open-source relighting models by lllyasviel): https://github.com/lllyasviel/IC-Light (not re-checked; cited as an example of the tool category).

**Films named** (director / cinematographer where relevant): *The Godfather* (1972, Willis); *All the President's Men* (1976, Willis); *Pariah* (2011, Young); *The Mandalorian* (2019, season 1, Fraser among others); *Apocalypse Now* (1979, Storaro); *The Last Emperor* (1987, Storaro); *In Cold Blood* (1967, Hall); *Road to Perdition* (2002, Hall); *The American Friend* (1977, Wim Wenders / Müller); *Paris, Texas* (1984, Müller); *The Lodger* (1944, Lucien Ballard); *The Matrix* (1999, the Wachowskis / Bill Pope); *Traffic* (2000, Steven Soderbergh, who shot it himself); *Arrival* (2016, Young); *Dune: Part Two* (2024, Fraser); *The Assassination of Jesse James by the Coward Robert Ford* (2007, Deakins); *Sicario* (2015, Deakins); *Skyfall* (2012, Deakins); *1917* (2019, Deakins); *Blade Runner 2049* (2017, Deakins); *O Brother, Where Art Thou?* (2000, Deakins); *Barry Lyndon* (1975, John Alcott); *Days of Heaven* (1978, Néstor Almendros); *The Sixth Sense* (1999, M. Night Shyamalan); *Toy Story* (1995); *The Incredibles* (2004).

**Test texts:** *The Catch* (workshop revision, 25 September 2026) and *The Long Places* (revised final), supplied by the user.

**Uncertain or unverified points, stated plainly:** exact kelvin values vary by lamp and are approximate; key-to-fill ratio bands differ between textbooks; the behavior of AI models described in Section 13 is based on vendor guides and common practitioner reports rather than controlled tests, and will change as models change. Confirmed in the second fact-check pass: the Wenders lab anecdote (Criterion, about *The American Friend*), the Lasseter quotation on the *Toy Story* pastels (MoMA audio guide, via search results), Runway's statement that negative phrasing is not supported and may produce the opposite (via search results of Runway's Gen-4 guides), and the idea behind Storaro's *Apocalypse Now* concept, one culture superimposing itself on another (ASC "A Clash of Cultures" article, via search results). Still not read at first hand: Storaro's exact words on *Apocalypse Now*; the verdicts in Section 13.3a, which are practitioner experience. The script says nothing about the over-bed reading light and the monitoring light proposed for sequences 22-23; they are this file's design choices. Removed as unverifiable: a claim that Bradford Young "has argued" that dark images by Black cinematographers are misjudged as underexposed. The staging proposals in Examples 2 and 3 (the lamp set on the table; Eli's seat) and the design proposals in Section 5.4 (flashlight type, streetlight type, Nell's fetched lamp, helmet light) are this file's choices, not the script's.
