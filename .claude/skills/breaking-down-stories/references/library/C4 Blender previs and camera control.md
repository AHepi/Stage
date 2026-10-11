# C4 — Controlling camera and movement: Blender previs, pose tools, motion capture, and feeding them to video models (as of 27 September 2026)

> **What this file is for**
> 1. It shows how to fix exactly where the camera is, what lens it has, how it moves, and where bodies are, before any AI video is made.
> 2. It explains Blender previs that an LLM builds and renders for you from a text floor plan, with a script I ran and tested today.
> 3. It lists current previs, posing and motion-capture tools with cost, difficulty, and whether an LLM can drive them.
> 4. It maps every route from a previs render into AI video: keyframe images, control videos, reference videos, camera data.
> 5. It applies all of this to three hard moments in *The Catch*. Tool facts change monthly: re-check before spending money.

---

## 0. How to read this file

- **[V] Verified**: found on a primary source (maker's page, release notes, model card, store page) or confirmed by running it myself on 2026-09-27. Source numbers like [P7] point to Section 14.
- **[U] Unverified**: only a secondary source, conflicting sources, or nothing found.
- **[J] Judgment**: my reasoning or recommendation.

**Companion kit.** The folder `C4_previs_kit/` next to this file holds the tested script `previs_from_plan.py`, the checker `check_blocking.py` (§5.3), five plan files for *The Catch* (`plan_cage_fall.json`, `plan_grid_pov.json`, `plan_inversion_reveal.json`, `plan_push_sill.json`, `plan_chest_opens.json`) and sample renders (`example_*.png`). All five plans render without errors on bpy 5.2.2 and pass `check_blocking.py` (no stand-in passing through a wall, floor or another stand-in; no camera inside a solid object), re-tested 2026-09-27 [V, P58]. **Correction history:** the first version of this kit rendered cleanly but failed the blocking check in three of four plans (Iona's floating body passed through the shaft wall; Eli and Jude stayed put while the rising cage passed through them; 17 clashes in the push). Those plans were rebuilt and re-rendered on 2026-09-27, and the depth pass was changed to a linear encoding (§4.6). A render that "runs without errors" can still be physically wrong, which is why Recipe 3 now makes the check a required step.

**Related files.** C1 chooses the video model; C2 covers image models, storyboards and character consistency; B1 covers lens and movement language and sets the film's lens family; A3 covers floor plans and the breakdown. This file follows B1: every focal length is a **full-frame equivalent** (a 36 mm-wide sensor), which is also Blender's default camera [V, P58].

**Search limits.** The first draft was checked mostly by opening primary pages directly, because the web-search budget ran out. A second, adversarial fact-check on 2026-09-27 re-verified the tool facts with web search plus direct page fetches (Blender, PyPI, GitHub, Hugging Face, Steam, Epic, Anthropic, fal, maker pricing pages) and folded the corrections in (for example Cine Tracer 2's status, Comfy Cloud prices, Unreal MCP set-up, Cascadeur's MCP server, and missing tools such as the official Claude connector for Blender, MetaHuman's free markerless capture, Marey, Wan-Animate-2, Lightcraft Spark Story and Intangible). Where a maker's page blocked access or only a secondary source was found, the fact is marked [U].

---

## 1. Plain-English terms used in this file

One word per concept. Where makers use other names, the maker's name is given once.

| Term | Meaning in one plain sentence |
|---|---|
| **Previs** | A rough 3D version of a shot, made before the real thing, to fix camera, lens, timing and positions. |
| **Grey-box set** | A set built only from plain boxes and slabs at real-world size, with no textures. |
| **Stand-in** | A simple figure that takes a character's place in previs (boxes, a mannequin, or a generic 3D human). |
| **Blocking** | Where each person stands and moves, and when. |
| **Plan file** | A text floor plan written in JSON (a strict text format programs can read) that lists the set, stand-ins, moves and camera for one shot. |
| **Key** | A value Blender stores at one frame (a position, a rotation, a lens); Blender fills the frames between keys. |
| **Keyframe image** | As in C1: a still picture pinned to a moment of a clip, usually the start frame or end frame. |
| **Focal length** | The lens number in millimetres (mm): small numbers see wide, large numbers see narrow. |
| **Sensor width** | The width of the camera's imaging chip in mm; with the focal length it sets the field of view. |
| **Field of view** | How wide an angle the camera sees, in degrees. |
| **Depth of field** | How much of the picture, front to back, is sharp. |
| **F-stop** | The lens opening number: lower means shallower depth of field. |
| **Camera rig** | The camera plus invisible handles that move and aim it (in this file: a moving handle and an aim point). |
| **Camera path** | How the camera's position, aim and lens change over the shot. |
| **Roll** | Rotating the camera around its own lens axis (a tilted "Dutch" angle, or a full 180° turn). |
| **Parent** | Attaching one object to another so it moves with it (a camera parented to the cage falls with the cage). |
| **Skeleton** | The hidden bones inside a 3D character that make it posable (Blender calls it an armature). |
| **Pass** | One kind of render of the same shot: clay, depth, normal, outline or pose. |
| **Clay render** | A grey, untextured render of the previs that shows shapes, positions and light direction. |
| **Depth pass** | A greyscale render where brightness means distance from the lens (here: near is white). |
| **Normal pass** | A colour render where colour means which way each surface faces. |
| **Pose pass** | A stick-figure skeleton drawn over each body, the format many video models follow for body position. |
| **Control video** | A pass (depth, normal, edges, pose or clay) given to a video model so the new video keeps its structure and motion. |
| **Video-to-video** | A model makes a new video that keeps the structure or motion of a video you give it. |
| **Motion transfer** | A model copies a body's movement from a reference video onto a character in a still image. |
| **Restyle** | Turning a clay still into a finished-looking image while keeping its layout. |
| **Motion capture (mocap)** | Recording a real person's movement as data a 3D skeleton can play back. |
| **Retarget** | Moving recorded motion from one skeleton onto a different skeleton. |
| **FBX / USD / BVH / Alembic** | Standard 3D file formats; FBX and USD carry scenes and cameras, BVH carries skeleton motion only, Alembic carries baked motion. |
| **bpy** | Blender's Python programming interface; also a package that runs Blender inside Python with no window. |
| **Headless** | Running Blender with no window, from a command, so an LLM can run it. |
| **MCP connector** | A small program using the Model Context Protocol that lets an LLM operate another program directly (C1 uses the same word). |
| **ComfyUI** | A free desktop app where you wire open AI models together as boxes ("nodes") into a workflow. |
| **LoRA / ControlNet** | Small add-on model files that teach a big model a new skill (a LoRA) or make it follow a structure image (a ControlNet). |
| **Reference video** | A video given to a hosted model as an example to copy (camera move, body motion, blocking), followed less strictly than a control video. |
| **Control strength** | How strictly a model follows the control video: high keeps the structure exactly, low lets the prompt change more. |
| **Master set** | The one grey-box set for a location that every shot there reuses. |
| **Plan view** | A flat drawing-like render of the set from straight above (floor plan) or from the side (elevation), with no perspective. |
| **Blocking check** | An automatic test (`check_blocking.py`) that reports any frame where a stand-in passes through the set or another stand-in, or the camera sits inside a solid object. |
| **Edge detector / pose detector** | Automatic filters that turn a video into line drawings (canny, HED, MLSD) or stick-figure skeletons (OpenPose, DWPose). |
| **Matcap** | A ready-made shading image Blender wraps onto surfaces; the normal matcap colours each surface by its direction. |
| **Insert** | A close shot of a detail (a palm on a sill, a limb in a socket). |
| **Over-the-shoulder** | A shot from just behind one person's shoulder, looking at what they face. |
| **Eyeline** | The direction a character is looking; it must meet what they look at across cuts. |
| **Coverage** | The set of camera angles filmed for one scene so it can be edited. |
| **LTS** | Long-term support: a Blender version that gets bug fixes for two years. |
| **Aggregator** | As in C1: a platform that sells many makers' AI models behind one account. |

---

## 2. The situation in one page (27 September 2026)

**Verified [V]:**

1. **Blender 5.2.2 LTS** is current (15 Sep 2026); 5.2 LTS came out 14 Jul 2026 with two years of long-term support [P1][P2]. The **bpy** package is 5.2.2 on PyPI and needs Python 3.13 [P7]. I installed it and rendered all five *Catch* plans headless on a 4-core machine with no graphics card, about 15–40 seconds per 640×360 shot of 29–96 frames for three passes plus a plan view and exports [P58].
2. **Blender 5.0 broke many older scripts.** The compositor moved to `scene.compositing_node_group`, EEVEE's engine name changed back to `BLENDER_EEVEE`, `action.fcurves` was removed, the old annotation data type (previously also called Grease Pencil) was renamed Annotation, and the File Output node changed [P5]. LLMs trained on older examples often write the old forms, so every script must be run once and fixed before you trust it.
3. **Blender 5.2 added VR location scouting**: in a VR headset you can place cameras and judge lens, focus and aperture from inside the 3D set [P3].
4. **Official and community MCP connectors for Blender exist.** Blender Lab's own MCP server (version 1.0.3, needs Blender 5.1 or newer) is marked "Released" [P10][P11]; it warns that it "will execute LLM generated code in Blender without any guards" [P10]. The community project by Siddharth Ahuja, renamed from `blender-mcp` to `mcp-for-blender`, reached 2.1.1 on 27 Sep 2026 and has about 29,500 GitHub stars [P12][P13]. The Blender Foundation states that "No generative AI functionality is currently available or planned to be integrated in Blender" [P9]; the MCP connectors are separate add-ons that drive Blender through its normal Python commands (the community one can also fetch AI-generated 3D models from outside services [P12]). **Claude has an official Blender connector**: on 28 Apr 2026 Anthropic released nine creative-tool connectors, including one for Blender built by the Blender developers on MCP, usable by other LLMs too [P59]. The community repository moved from `ahujasid/blender-mcp` to `ahujasid/mcp-for-blender` in September 2026; old `uvx blender-mcp` set-ups keep working through a compatibility package [P12][P13].
5. **Unreal Engine 5.8** (released 17 Jun 2026 [P60]) added an experimental MCP plugin for the editor [P17][P18] and the free, experimental **MetaHuman Animator Markerless Motion Capture** plugin: body, face and fingers of one actor from one ordinary camera (webcam or phone), processed on your own computer, free including commercial use, Windows only [P17][P61]. Reports say 5.8 is the last major UE5 release and Unreal Engine 6 early access is aimed at late 2027 [U: secondary, P60].
6. **Hosted video models now accept previs directly.** Seedance 2.5 (31 Jul 2026) takes "textureless 3D models" (clay renders) to set "spatial structure, character poses, motion paths, and camera angles" [P32]. MiniMax H3 can "reference the … camera movement from Video 1" [P33]. Kling 3.0 Motion Control copies body movement from a reference video onto a character image, up to 15 s [P34][P35]. Luma Ray3.2 allows up to 16 keyframe images per clip and Modify Video V2 up to 20 s at 1080p [P37][P38]. Runway Aleph 2.0 edits existing video and is callable through Runway's MCP connector since 14 Jul 2026 [P36]. Moonvalley's **Marey** (on fal) offers camera control from a single image, motion transfer and pose transfer, trained only on licensed footage (C1) [P62]. The open **Wan-Animate-2** (weights 7 Aug 2026, Apache 2.0) copies a driving video's motion onto a character image, non-human characters included, but its default 720p set-up uses eight data-centre GPUs [P63].
7. **Open control models are cheap to rent.** fal runs Wan VACE with depth control at $0.04–0.08 per second [P39] and Wan 2.2 VACE Fun depth at $0.05–0.10 per second [P40]. New on 22 Sep 2026: an open ControlNet for MiniMax H3 with eight control types, including depth, pose, edges and bounding-box layout [P43]; its two ~62 GB parts need an 80 GB data-centre graphics card with offloading, so for this user it is a rented-cloud option, not a home one [P43].
8. **Camera-trajectory control is still mostly research.** CameraCtrl (2024), MotionCtrl (2023), Uni3C (2025), ReCamMaster (2025) and 2026 papers such as CameraAnything and CoaG take exact camera paths, but only as research code, some of it wrapped for ComfyUI [P47]–[P53]. Productized camera control is **presets or references, not numbers**: Higgsfield's 50+ named moves (dolly, crane, bullet time, FPV drone and so on), Marey's camera moves re-framed from a single still (plus drawn paths for objects), Kling 3.0's per-shot camera in multi-shot, Luma Ray3.2's 16 keyframes, and move-copying from a reference video in Seedance 2.5 and H3 (C1) [P62][P64]. I found no hosted product that accepts a numeric camera track such as `camera_track.json` [U: absence of evidence]. Even the open Wan 2.2 Fun Control-Camera model takes preset pans and zooms, not an arbitrary path [P42]. An Autodesk Research study at CHI 2026 (PrevizWhiz) tested this file's core workflow (rough 3D → restyled frames → pose/depth → Wan Fun Control/VACE) with ten participants (eight filmmakers and creative professionals, two 3D/animation experts), using the small 1.3B Wan models for speed. They found it lowered technical barriers and sped up iteration, but rated how well results matched what they imagined only middling (median 3) and still wanted more control ("it's not very controllable… still takes time to refine") [P54].
9. **Motion capture from a phone video is cheap.** Rokoko Vision: 30 s a month free, 600 s for $10–12 a month, one performer per video [P27]. DeepMotion: 60 s a month free for non-commercial use; handles several people [P28]. QuickMagic: free tier (30 s videos, FBX only, non-commercial), Basic $14.90 a month [P29]. MetaHuman's markerless plugin is free, but only inside Unreal on Windows [P61]. Meshcapade's MoCapade web service closed on 18 Apr 2026 after the company joined Epic [U: secondary, P65].

**Judgment [J]:** For a non-technical user, the most reliable path today is: the LLM writes a plan file from the breakdown → runs Blender headless → runs `check_blocking.py` and fixes any clash → you look at the clay stills and plan view and ask for changes → the chosen still is restyled into a keyframe image → image-to-video with start and end frames, or the depth pass goes to a control model. Live MCP control of Blender is optional and convenient, but a plan file is easier to check, repeat and store in the breakdown.

---

## 3. Landscape tables

Difficulty is for a non-technical user with an LLM helping: **Easy** (click-through), **Medium** (install plus one or two settings), **Hard** (many parts, error messages likely).

### 3A. Blender and its add-ons

| Item | Current version, date | Cost | What it gives previs | Can an LLM drive it? | What you do by hand | Difficulty |
|---|---|---|---|---|---|---|
| **Blender** | 5.2.2 LTS, 15 Sep 2026 [P1] | Free | Everything: sets, stand-ins, cameras, renders, exports | Yes: Python scripts, or an MCP connector | Install; open files; look at results | Medium |
| **bpy package** | 5.2.2, 15 Sep 2026; Python 3.13 only [P7] | Free | Headless rendering from a script | Yes, fully, if the LLM has a terminal (Claude Code, Codex) | Nothing after setup | Easy with a terminal LLM |
| **MPFB** (MakeHuman for Blender) | 2.0.17, 22 Jul 2026; Blender 4.2+; GPL [P15] | Free | Human stand-ins with adjustable body shape, automatic skeleton, Rigify support | Partly: scripts can call its buttons [U] | Install extension; choose bodies | Medium |
| **Rigify** | Ships with Blender (confirmed present in bpy 5.2.2) [P58] | Free | Control skeleton for posing humans | Yes, to build; posing well is a skill | Posing | Medium–Hard |
| **Mixamo** (Adobe) | Still in use Aug–Sep 2026 [P16]; status monitors showed it operational in 2026, with outages and doubts about Adobe's support in 2025 [U: secondary; Adobe FAQ blocked] | Free with an Adobe ID, no Creative Cloud subscription [U: secondary] | Rigged characters and a motion library, FBX | No public API [U]; terms bar redistributing characters [P16] | Download each character and motion | Easy |
| **BVH importer** | Ships with Blender [P58] | Free | Loads motion-capture files | Yes | None | Easy |
| **Grease Pencil** | Built in; 5.2 added a new fill algorithm and brushes [P2] | Free | Drawn 2D storyboards inside the 3D scene | Partly (strokes by script) [P6] | Drawing | Medium |
| **VR location scouting** | New in 5.2 [P3] | Free (headset extra) | Place and judge cameras from inside the set | No | Wear the headset | Medium |

### 3B. Connectors that let an LLM operate 3D and control software

| Connector | Version / date | Cost | What it can do | Notes | Difficulty |
|---|---|---|---|---|---|
| **Blender Lab MCP server** (official) | 1.0.3; needs Blender 5.1+ [P10]; listed by Anthropic as an official Claude connector since 28 Apr 2026 [P59] | Free | Inspect scenes, rename, explain nodes, batch-apply changes, run LLM-written Python, add tools to Blender's interface [P10][P59] | "Without any guards": use a spare computer or virtual machine [P10] | Medium |
| **mcp-for-blender** (ahujasid; formerly `blender-mcp`) | 2.1.1, 27 Sep 2026; about 29,500 GitHub stars; Blender 3.0+ [P12][P13] | Free | Scene info, create/modify objects, materials, run any Python, viewport screenshot, GLB/FBX export, Poly Haven/Sketchfab/Poly Pizza assets, Hyper3D Rodin and Hunyuan3D model generation [P12] | Install: `uvx mcp-for-blender install-addon`, enable add-on, press **Start MCP Server**; optional safe mode `BLENDER_MCP_SAFE_MODE=1` (checks scripts before running them); telemetry off with `DISABLE_TELEMETRY=true` [P12] | Medium |
| Other Blender connectors | 2026 [P14] | Free | **blend-ai** (≈150 stars, AGPL): 186 tools, blocks dangerous imports, needs Blender open. **bpy-dev/blender-mcp** (≈95 stars, GPL): a modified Blender Lab server whose `_for_cli` tools edit saved `.blend` files with no window, using the Blender app or the bpy package [P14] | Small projects; check activity before relying | Medium–Hard |
| **Unreal MCP** (Epic, experimental) | Unreal Engine 5.8 [P17][P18] | Engine free for film ("linear content") for individuals and companies under $1M a year revenue; above that $1,850 per seat per year [U: secondary; Epic licence page not fetched] | Lets an agent operate the Unreal Editor | Enable the **Unreal MCP** and **AllToolsets** plugins (Edit → Plugins; the tools live in AllToolsets); the server runs at `http://127.0.0.1:8000/mcp` (auto-start in Editor Preferences → General → Model Context Protocol, or console `ModelContextProtocol.StartServer 8123` for another port); local connections only, no password [P18] | Hard |
| **Cascadeur MCP server** | Cascadeur 2026.2 (6 Aug 2026), with an expanded Python API [P26] | Needs a Cascadeur plan for FBX export (§3C) | Lets an agent drive Cascadeur's physics-aware posing | New; not tested here | Hard |
| **Intangible MCP** | "MCP Beta" in an open-beta product [P66] | Plans from $0 (150 one-time credits) to $65/month [P66] | Lets an agent build a 3D scene and camera in Intangible's browser studio, then render images/video with hosted models | New; not tested here | Medium |
| **comfy-mcp** (Comfy-Org, official) | 0.10.0, 10 Aug 2026 [P57] | Free | Run ComfyUI workflows, watch and cancel jobs, search templates, search/download models, fetch outputs (installing custom nodes not confirmed [U]) | Local only; a separate Comfy Cloud MCP is at `https://cloud.comfy.org/mcp` [P57] | Medium–Hard |
| Video aggregators (fal, Replicate, Runway, Higgsfield) | See C1 §7 | Pay per use | Run video models, including control and reference modes | fal's connector exposes Wan VACE, Kling Motion Control, Seedance 2.5 | Medium |

### 3C. Dedicated previs and posing apps

| Tool | Status found | Price | Strength | LLM-drivable? | Verdict [J] |
|---|---|---|---|---|---|
| **Unreal Engine** (Sequencer, virtual camera, MetaHuman) | 5.8, 17 Jun 2026; MCP experimental [P17][P60] | Free for film under $1M a year revenue [U: secondary] | Photoreal real-time previs; virtual camera on a phone or tablet; free markerless body capture (§3D) | Partly (MCP, Python) | Only if you already use it; too big for this user |
| **Cine Tracer** | Early Access since 28 Sep 2018; no update "in over 3 years"; Unreal Engine 4 [P19] | $89.99 (includes Cine Tracer 2) [P19] | Real cameras, lenses and film lights as a game | No | Abandoned; avoid |
| **Cine Tracer 2** | **Still Early Access** since 1 Aug 2023; last update "over 2 years ago"; Steam reviews "Mostly Negative" (31% of 97) [P20] | $89.99 [P20] | Same idea on Unreal Engine 5 with MetaHumans; one dolly, a small light library, two locations | No | Stalled; do not buy for this pipeline [J] |
| **FrameForge 4** | Core and Professional editions; "optically accurate" cameras; 14-day trial [P21] | Not shown on maker's pages; third-party listings give Core $498.95 or $12.99/month, Professional $799 or $24.99/month [U: secondary] | Lens-accurate storyboards; Professional plans dolly and crane moves to the inch | No | Only for people already trained in it |
| **ShotPro** | Desktop (macOS, Windows) plus iOS via the App Store; standalone 4.14.4 [P22] | ShotPro S subscription $9.99/month, $44.99/6 months, $79.99/year (includes the photoreal "HQ" version); standalone 4.x licence $35 once [P22] | Lens, aperture, focus, ISO, shutter, camera shake; posed and animated characters; text-to-speech dialogue; FBX import | No | Good hand tool for boards |
| **Previs Pro** | Version 3 imports screenplays (Final Draft, Fountain) [P23] | Free (one animatic per project); $39.99/month; $119.99/year; $359.99 lifetime; up to 5 Apple devices [P23] | Mac/iPad/iPhone; AR camera; LiDAR scans; FaceCap/PoseCap; export to 2D, 3D, MP4 and editors [P23] | No | Best hand-operated app for a beginner [J] |
| **Lightcraft Jetset** / **Spark Story** | Jetset: iPhone virtual production and previs; Spark Story: browser previs, public beta at SIGGRAPH 2026, commercial release planned for autumn 2026 [P67] | Jetset Standard free, Pro $20/month, Cine $80/month (April 2025 prices, not re-checked for 2026 [U]); Spark Story target ≈$29.95 per seat per month [P67] | Spark Story loads Final Draft scripts, ties every shot to a scene, simulates real camera bodies and lenses, stores everything as USD, accepts Gaussian splats and AI-made 3D [P67] | No (browser/iPhone) | Worth watching: the closest commercial match to this file's workflow, but no AI video output [J] |
| **Intangible** | Browser 3D studio that renders its scenes through hosted image and video models; open beta [P66] | Free 150 one-time credits; Explorer $35/month (250 credits); Business $65/month (1,000 credits) [P66] | Place 3D stand-ins and a camera, then generate consistent images or video; glTF export | Partly ("MCP Beta") | The quickest no-install way to try "3D layout → AI shot"; less exact than Blender passes [J] |
| **set.a.light 3D** | Version 3 (V3.1.13 June 2026 per a download site [U]); Mac and Windows [P68] | BASIC, STUDIO, CINEMA editions, lifetime licences with a year of updates; prices not shown on the pricing page [P68][U] | Photographic lighting simulation; CINEMA adds an animation tool, MP4 video export and 3D import [P68] | No | Only for lighting studies |
| **PoseMy.Art** | Web app [P24] | Free tier (basic models, inverse kinematics, OpenPose-format export); Pro $15/month, $150/year, or a "limited time" $99.99 lifetime deal [P24] | Fast posing of several figures in the browser; pose passes for image models; Pro exports the scene as .obj | No | Best quick pose-pass source [J] |
| **Magic Poser** | Apps [P25] | Free (1 model per scene); Pro $9.99 once (unlimited models); Master $14.99/month (3D model export). Free and Pro export 2D images only [P25] | Posing on a phone or tablet | No | Reference photos for poses |
| **Cascadeur** | 2026.2, 6 Aug 2026 (2026.2.2 on 9 Sep 2026): animation layers, easing controls, BVH import, an **MCP server**, Python API [P26] | Free (non-commercial; 300 frames and 120 joints per scene; saves only its own .casc format); Indie $19/month or $96/year (under $100k revenue); Pro $49/month or $396/year; paid plans become perpetual after a year [P26] | AI-assisted posing (AutoPosing, also fingers and quadrupeds), physics checking, AI in-betweens; Video MoCap (alpha) takes poses from video [P26]; exports FBX/USD/GLTF on paid plans | Partly (new MCP server and Python API; untested) | Best for falls and stunts once you want real physics [J] |

### 3D. AI motion capture from video

| Tool | What it does | Price found | Exports | Verdict [J] |
|---|---|---|---|---|
| **Rokoko Vision 3.0** | Upload one video, get 3D motion; rebuilt solver; dual-camera mode removed; one performer per video [P27] | Free 30 s/month; Basic $10/month (yearly) or $12 (monthly), 600 s [P27] | FBX; BVH on Basic; works with Blender, Unreal, Mixamo skeletons [P27] | Cheapest good start |
| **DeepMotion Animate 3D** | Video to 3D motion; face and hands extra; several people per video [P28] | Free 60 s/month, non-commercial (commercial use needs a paid plan); 1 credit = 1 s, face/hands +0.5 each; Studio plan "unlimited" (price not shown) [P28] | FBX, BVH, MP4; GLB for custom characters [P28] | Best cheap option when two or more people interact [J] |
| **QuickMagic** | Body, hands, face; single or multiple people; moving camera accepted [P29] | Free 50 credits (30 s videos, FBX only, no commercial use); Basic $14.90/month ($11.90 yearly, 200 credits); Pro $49.90 (1,000); credits per second vary by feature [P29] | Paid: FBX, BVH, Mixamo, Unreal, Unity, C4D, iClone and more [P29] | Strong on hands [U] |
| **Move.ai** | Genesis (multi-camera, enterprise) and Move One (single camera) [P30] | Move One: 30 free credits once; Starter $18/month (60 credits), Standard $48 (180); 1 credit = 1 person-second (Gen 1) or 2 credits (Gen 2) [P30; page dated Jan 2025, U for 2026] | GLB and others [U] | Pricier per second than Rokoko |
| **Autodesk Flow Studio** (formerly Wonder Studio) | AI mocap, camera track, clean plate, character replacement from live footage; "Wonder Animation" turns filmed shots into animated 3D scenes (paid plans only) [P31] | Free tier (AI MoCap and Live Action); Lite $10/month (Aug 2025 price cut) [P31]; Standard ≈$45 and Pro ≈$95/month [U: secondary] | Blender, Maya, Unreal scenes, USD [P31] | Useful if you shoot yourself acting |
| **MetaHuman Animator Markerless Motion Capture** (Unreal 5.8 plugin) | Body, face and fingers of one actor from one webcam or phone video; runs locally; experimental; a user test ran about one second of 1080p video per minute of processing; weaker with a moving camera [P61] | Free, including commercial use [P61] | Unreal (Windows only) | Only if Unreal is already installed |
| **Cascadeur Video MoCap** (alpha) | Poses from an .mp4 video onto a Cascadeur character; one actor only [P26] | Included in Cascadeur plans | Cascadeur, then FBX on paid plans | Good when the next step is physics clean-up in Cascadeur |
| **Meshcapade MoCapade** | Web service closed 18 Apr 2026 after Meshcapade joined Epic; its technology feeds MetaHuman's capture [U: secondary, P65] | — | — | Gone; ignore older tutorials |
| **Open pipeline** (GVHMR estimator → Mixamo skeleton → Blender) | Agent-operated script set, Aug 2026; needs ~8 GB graphics card; SMPL-X body model needs research registration [P16] | Free | Blender action | Hard; licence limits commercial use [U] |

### 3E. Bridges from previs into AI video

| Bridge | Takes from previs | Access | Price found | Maturity |
|---|---|---|---|---|
| **Image-to-video from a restyled keyframe image** (any model in C1) | Clay still → restyled start (and end) frame | Every platform | See C1 | Mature |
| **Seedance 2.5 reference-to-video** | Clay render as reference video (up to 10 videos, 30 images) [P32] | fal, Replicate, Runway, BytePlus (C1) | ≈$0.23–0.47/s at 720p (C1) | New, strong on blocking; weaker on multi-person interaction [P32] |
| **MiniMax H3** | Clay render as camera-move reference; video-to-video motion transfer [P33] | MiniMax API, fal, Runway | ≈$0.13/s (C1) | New |
| **Kling 3.0 Motion Control** | A body-motion video (mocap stand-in render or you acting) + character image; up to 15 s [P34] | Kling, fal ($0.168/s v3 Pro) [P35] | Atlas Cloud $0.071–0.095/s [P34] | Mature; hands crossing the body cause "spaghetti limbs"; face drift is the commonest failure (fix: several character images) [P34] |
| **Runway Aleph 2.0** | Restyles/edits an existing video, e.g. a clay render [P36] | Runway app, API, MCP | Runway credits | Mature; C1 notes it does not invent new angles [U] |
| **Luma Ray3.2 / Modify Video V2** | Up to 16 keyframe images; modifies clips up to 20 s [P37][P38] | Luma app, API | Credits (C1) | Mature |
| **Wan VACE (depth, pose, other controls)** | Depth/pose control video + reference image, optional first and last frame; 81–241 frames per request [P39] | fal: `wan-vace-14b/depth` $0.04–0.08/s; `wan-22-vace-fun-a14b/depth` $0.05–0.10/s, both billed per 16 frames [P39][P40]; or ComfyUI | Cheap | Mature, 16 fps base |
| **Wan 2.2 Fun Control / Fun Control-Camera** | Canny, depth, pose, MLSD (straight-line) control and trajectory control; the Control-Camera weights take **preset** moves (pan up/down/left/right, zoom, and combinations), not an arbitrary camera path; trained at 81 frames, 16 fps; 64 GB download for the 14B versions; smaller 5B versions exist (Aug 2025) [P42][P41] | ComfyUI, VideoX-Fun | Free weights, Apache 2.0 | Mature open |
| **LTX-2.3 IC-LoRA Union Control** | Canny + depth + pose [P45]; camera LoRAs (dolly, jib) exist for LTX-2 [P46] | ComfyUI (official LTX templates) [P44] | Free under $10M revenue (C1) | Open; union control for LTX-2.5 not found [U] |
| **MiniMax-H3-Fun-Controlnet-Union-2.0** | 8 controls: canny, depth, HED, MLSD, pose (DWPose skeletons), scribble, layout, grey; inpainting; up to 15 s at 24 fps; `control_context_scale` 0–1 sets strength [P43] | VideoX-Fun code | Free weights under the MiniMax H3 Community Licence (regional conditions); ~62 GB transformer + ~62 GB text encoder, 80 GB GPU with offloading [P43] | Brand new (22 Sep 2026) |
| **Uni3C / ReCamMaster** (camera paths) | Uni3C: camera path + human motion; its camera is set by 7 numbers (distance, elevation, azimuth, three offsets, focal length) or presets such as orbit and swing; ReCamMaster: re-films a video along 10 preset moves only [P48][P49] | ComfyUI via Kijai's WanVideoWrapper, which lists both [P47] | Free | Research-grade; Uni3C used ~46–51 GB GPUs in tests [P49] |
| **Marey** (Moonvalley) camera control, motion transfer, pose transfer | A still (camera control: the still becomes a 3D scene you direct the camera through; drawn paths move objects) or a reference video (motion or pose transfer) [P62] | Moonvalley app, fal | ≈$0.30/s; 5 or 10 s; 1080p; no audio (C1) | Hosted and mature; the only hosted product found that re-frames a single still in 3D for a camera move [J] |
| **Wan-Animate-2** (open) | A driving video (your own performance, or a stand-in render) + a character image, non-human characters included; no skeleton step [P63] | ModelScope demo; ComfyUI integration still "to do" on the model card [P63] | Free weights, Apache 2.0; 720p default set-up uses 8 data-centre GPUs [P63] | New (7 Aug 2026); cloud-only for this user |
| **Runway Act-Two** | Your webcam or phone performance (head, face, body, hands) onto a character [P36] | Runway app, API | Runway credits (C1) | Mature; for performances, not camera paths |

---

## 4. Blender basics that matter for previs

You do not need to learn Blender to use this file; the LLM does the technical work. You need to know what to ask for and what to check.

### 4.1 The camera

- **Focal length** is set in mm (default 50 mm) against a **sensor width** (default 36 mm) [V, P58]. Keep the sensor at 36 mm so every number matches B1's full-frame lens family. The field of view follows from both: horizontal field of view = 2 × arctan(sensor width ÷ (2 × focal length)).

| Focal length (36 mm sensor) | 18 mm | 24 mm | 35 mm | 50 mm | 85 mm | 135 mm |
|---|---|---|---|---|---|---|
| Horizontal field of view | 90.0° | 73.7° | 54.4° | 39.6° | 23.9° | 15.2° |

- **Depth of field**: switch it on, choose a **focus object** (the camera then stays focused on that stand-in however either moves) and an **f-stop** [V, P58]. The kit leaves depth of field off in its Workbench passes so control videos stay sharp [J]; the numbers still matter because they are written into `camera_track.json` and the breakdown, and they tell the video prompt "shallow focus, background soft" or not.
- **Move versus zoom.** Moving the camera changes perspective (near things grow faster than far things); changing the focal length only crops. A dolly zoom (Hitchcock's "Vertigo" effect) is both at once in opposite directions (B1). AI video models blur this distinction when given words; a control video removes the ambiguity [J].
- **Clip start/end** (default 0.1 m and 1,000 m) [V, P58]: objects closer than clip start vanish. Inside a 2 m freight cage, set clip start to 0.01–0.05 m or walls will disappear [J].

### 4.2 Camera rigs and camera paths

- **Aim with a target.** The tested script uses a **camera rig**: an invisible handle that carries the camera and a "Track To" constraint that always aims it at an invisible target. You key the handle's position and the target's position; Blender fills the move. The camera itself sits on the handle so it can **roll** (tilt around the lens axis) without breaking the aim [V, P58].
- **Ride along.** Parent the rig to a moving object and the camera moves with it: parented to the cage, it falls, stops and turns with the cage, so the shaft streams past (B1: "bolt the camera to the cage").
- **Smooth tracks.** For a long, even move, draw a curve and give the rig a "Follow Path" constraint; ask the LLM for it by name [J].
- **Handheld feel.** A "Noise" modifier on the rig's position and rotation curves adds small random shake; keep it under about 1 cm and 0.5° for a nervous handheld [J].
- **Timing.** Blender eases in and out of every key by default (new keys are "Bezier") [V, P58]. That is right for a camera move and wrong for a free fall, which should speed up the whole way: ask the LLM to key positions from the formula distance = 4.9 × seconds² (metres) **on every frame** of the fall, as `plan_cage_fall.json` now does [V, P58]. Keys every 8 frames are not enough: I measured the first kit version (keys at frames 20, 28, 36, 40) and the cage's speed stalled at about 5.6 m/s mid-fall, overshot to 13.4 m/s, then slowed to 3.7 m/s in the last frame before the impact, which reads as floating [V, P58].

### 4.3 Grey-box sets from simple shapes

Build to real size in metres: the story's geometry is the point. For *The Catch*: a shaft about 2.6 m square, a cage 2.0 × 2.0 × 2.3 m, a maintenance opening "broad enough to pass a machine through" (2.0 m wide, 2.2 m tall), a sill 9 m up, a yellow band at head height near the bottom (the numbers are my choices [J]). Two script details to respect: the band "circles the whole shaft at head height" (model it on all four walls whenever the camera can see more than one; `plan_grid_pov.json` does), and the opening is "Halfway up" the climb, so either end the shaft at about 18 m or accept that the kit's walls (to 25 m) put the sill a third of the way up; only what the camera sees matters [J]. Give each object a flat colour that means something (brick brown, steel grey, sill white, yellow band yellow) so clay renders read at a glance and image models can be told "the white strip is the bright steel sill" [J].

**Build one master set per location** and reuse it for every shot there. That is how geography stays consistent across shots: the opening is always on the same wall and the stripe always at the same height, whatever the camera does [J].

### 4.4 Stand-in characters: a ladder

| Level | Stand-in | Good for | Not good for |
|---|---|---|---|
| 1 | Box mannequin from the script (torso, legs, head, a "nose" showing which way it faces) [V, P58] | Positions, heights, eyelines, depth control, camera paths | Pose control (a pose detector will not find a skeleton in boxes) |
| 2 | **MPFB** human: set height, build, sex in sliders; automatic skeleton [P15] | Silhouette, body type, depth and outline passes | Performance |
| 3 | **Mixamo** character plus one of its motions (walk, fall, crouch) | Pose passes, motion transfer references | Specific acting |
| 4 | Your own mocap (Rokoko, DeepMotion, QuickMagic) retargeted onto level 2 or 3 | Exact acting, stunts you can safely mime | Zero gravity (see §8) |
| 5 | **Rigify** control skeleton posed by hand, or Cascadeur for physics-checked falls | Creatures, precise stunts | Non-animators |

The tall figure in *The Catch* is not human-shaped enough for human pose detectors: its head "sits low between its shoulders". Build it from boxes at 2.4 m and drive video models with depth, not pose [J].

### 4.5 Grease Pencil storyboards inside Blender

Grease Pencil draws 2D strokes in the 3D scene, so you can sketch over a clay render from the actual camera and keep the drawing tied to that camera. It is optional here: C2 makes storyboard frames with image models, and the clay stills from this file are already usable as storyboard frames. Use Grease Pencil only if someone wants to draw [J].

### 4.6 Rendering: engines and passes

- **Workbench** is Blender's fast preview renderer. It needs no graphics card, gives flat clay with outlines, and rendered 40–96 frames per pass in seconds in my test [V, P58]. Use it for all previs passes.
- **EEVEE** (real-time) and **Cycles** (physically accurate) give real light and shadow. Use them only if the previs frame itself will be the keyframe image's lighting guide; they are slower and EEVEE needs a graphics card [J].
- **Passes the script makes** [V, P58]: *clay* (Workbench, outlines and cavity shading), *normal* (Workbench with the built-in `check_normal+y.exr` matcap), *depth* (the depth value mapped so a chosen near distance is white and far distance is black, rendered with the "Raw" view transform so the grey level is linear in distance). Each pass is written as an MP4 (for video models) plus PNG stills at chosen frames (for image models).
- **Why "Raw" for depth:** the "Standard" view transform still applies the sRGB display curve. In a test on the same depth frame, one pixel read 0.455 under Raw and 0.706 under Standard (0.455 pushed through the sRGB curve), so a Standard depth pass is washed out and has the least contrast close to the lens, where the actors are [V, P58]. The first kit version made this mistake; the current script switches to Raw for the depth pass only. Depth estimators such as Depth Anything produce *inverse* depth (more contrast close to the lens) [J]; if a control model reads the kit's linear depth as too flat, ask the LLM for an inverse-depth mapping, or send `clay.mp4` and let the service estimate depth itself (§6, Route 2).
- **Outline pass**: most control models make their own edge pass from the clay video with a "canny" edge detector, so a separate outline render is rarely needed [J].
- **Pose pass**: render a human-shaped stand-in (level 2–3) and let the control tool extract the skeleton (DWPose, used by the H3 ControlNet [P43] and by ComfyUI preprocessors). PoseMy.Art exports OpenPose-format poses directly for stills [P24].

### 4.7 Exporting the camera

The script writes three kinds of camera record [V, P58]:
- `camera_track.json`: for every frame, position in metres, rotation, the full 4×4 matrix, focal length, sensor width and horizontal field of view. This is the most useful record for LLMs and research camera-control models.
- `shot.fbx` with baked animation, and `shot.usdc`: open in Unreal, Maya, Cascadeur or back in Blender.
- `shot.blend`: the whole previs, to reopen and adjust.

Blender 5.2 also imports animated cameras from Alembic files [P4].

### 4.8 Blender 5.x traps for LLM-written scripts [V, P5 unless marked P58]

| Old code an LLM may write | Correct for Blender 5.x |
|---|---|
| `scene.use_nodes = True; scene.node_tree` | `tree = bpy.data.node_groups.new(name, "CompositorNodeTree"); scene.compositing_node_group = tree`, and output through a Group Output node [V, P58] |
| `"BLENDER_EEVEE_NEXT"` | `"BLENDER_EEVEE"` |
| `action.fcurves` | Channelbags via `bpy_extras.anim_utils`; or just use `keyframe_insert()` as the kit does |
| `bpy.data.grease_pencils` for annotations | `bpy.data.annotations`; drawing objects remain `bpy.data.grease_pencils` [V, P58] |
| `bpy.data.grease_pencils_v3` (Blender 4.3–4.5) | Gone in 5.2: the new Grease Pencil data is `bpy.data.grease_pencils` [V, P58] |
| `scene.use_nodes = True` to switch the compositor on | Deprecated: always True, setting it does nothing, removal planned for 6.0 [P5] |
| File Output node `base_path`, `file_slots`, `layer_slots` | Removed; use `directory`, `file_name`, `file_output_items` [P5] |
| `CompositorNodeMapRange`, `CompositorNodeMath` | Do not exist in 5.2; use `ShaderNodeMapRange`, `ShaderNodeMath` inside compositor trees [V, P58] |
| `file_format = "FFMPEG"` alone | Set `image_settings.media_type = "VIDEO"` first [V, P58] |
| Default colour management | AgX/Filmic tone curves distort clay greys and depth; use `view_settings.view_transform = "Standard"` for clay and normal passes, and `"Raw"` for depth and other data passes, because Standard still applies the sRGB display curve [V, P58] |
| `obj.scale = size` on a box that has children | Children inherit the stretch; bake size into the mesh instead [V, P58] |

---

## 5. LLM-driven Blender

### 5.1 Three ways to work

| Mode | How it works | You need | Best for | Risk |
|---|---|---|---|---|
| **A. Script you run** | The LLM writes a `.py` file; you open Blender → Scripting tab → Open → Run, or run `blender -b -P script.py -- plan.json out` | Blender installed | Chat-only LLMs | You copy files by hand |
| **B. Headless, LLM runs it** | The LLM installs `bpy` in a Python 3.13 environment and runs the script itself | An LLM with a terminal (Claude Code, Codex); ~1 GB disk | Batch previs of many shots; repeatable | Lowest: it only writes files in the output folder |
| **C. Live MCP control** | The LLM operates an open Blender window through an MCP connector | Blender + connector add-on + LLM app settings | Interactive adjustment ("move the camera 30 cm left and show me") | Runs arbitrary code in your Blender; save first [P10][P12] |

**Recommendation [J]:** Mode B for the pipeline (every shot's plan file is stored in the breakdown and can be re-rendered later), Mode C for fiddling with one shot, Mode A only if the LLM cannot run programs.

### 5.2 The plan file (text floor plan as JSON)

Coordinates are metres; **Z is up**. A figure with `facing_deg` 0 faces −Y ("towards the audience" in Blender's front view); 90 faces +X; 180 faces +Y; 270 faces −X. A `loc` is relative to the parent if a `parent` is given.

| Field | Meaning |
|---|---|
| `shot`, `fps`, `frames`, `resolution` | Shot ID from the breakdown; 24 fps; length in frames; pixels |
| `pivots` | Invisible handles: hinges, groups, a whole cage (`name`, `loc`, optional `parent`) |
| `boxes` | Grey-box pieces: `name`, `loc` (centre), `size` (x, y, z metres), `rgb`, optional `parent` |
| `figures` | Stand-ins: `name`, `loc` (feet), `height`, `facing_deg`, `rgb`, optional `parent` |
| `animate` | Keys for any object: `[frame, [x,y,z], [rx,ry,rz] degrees]` |
| `camera` | `lens_mm`, `sensor_mm`, optional `fstop` and `focus_on`, optional `parent`; `keys` as `[frame, camera position, aim point, optional lens mm]`; optional `roll_keys` as `[frame, degrees]` |
| `depth_range_m` | Near and far distances for the depth pass |
| `stills` | Frames to save as PNG keyframe-image candidates |
| `plan_view` | `direction` "top" (floor plan) or "side" (elevation, for shafts and falls), `center`, `size_m`, `hide` (walls to leave out) |
| `beats` (optional) | `[frame, "what happens", "script line"]` entries for people to read; the script ignores this field, as it ignores any unknown field |

**Prompt to turn a breakdown shot into a plan file (paste into the LLM):**
> "Here is shot [ID] from the breakdown and the master set plan for this location. Write a plan file for `previs_from_plan.py` (schema in C4 §5.2). Use real sizes in metres, 24 fps, the lens from the breakdown with a 36 mm sensor, and keys at every story beat named in the shot. Put the beats first, in a `beats` list inside the plan file: frame number, what happens, script line. Then render it, show me the plan view and the stills, and list anything you had to guess."

### 5.3 The tested script

This is the complete script from the kit (169 lines). It ran without errors on bpy 5.2.2 LTS on 2026-09-27 for all five plan files (re-run after the depth-pass fix); it should also run inside the Blender 5.2 app [V, P58; app run not tested].

```python
"""previs_from_plan.py - build a grey-box shot from a JSON plan and render clay, depth, and camera data.
Run:  blender -b -P previs_from_plan.py -- plan.json out_dir      (Blender app)
 or:  python previs_from_plan.py plan.json out_dir                 (pip install bpy==5.2.2, Python 3.13)
Tested with bpy 5.2.2 LTS on 2026-09-27."""
import sys, json, math, os
import bpy
from mathutils import Matrix

args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
plan = json.load(open(args[0])); out = os.path.abspath(args[1]); os.makedirs(out, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
scn = bpy.context.scene
scn.render.fps = plan.get("fps", 24)
scn.frame_start, scn.frame_end = 1, plan["frames"]
scn.render.resolution_x, scn.render.resolution_y = plan.get("resolution", [1280, 720])

def grey(name, rgb):
    m = bpy.data.materials.new(name); m.diffuse_color = (*rgb, 1); return m

def box(name, loc, size, rgb=(0.6, 0.6, 0.6), parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object; o.name = name
    o.data.transform(Matrix.Diagonal((*size, 1)))   # bake size into the mesh so children are not stretched
    o.data.materials.append(grey(name, rgb))
    if parent: o.parent = parent
    return o

def figure(name, loc, height=1.75, facing_deg=0, rgb=(0.8, 0.5, 0.3)):
    """Stand-in mannequin: an empty 'root' at the feet with body parts parented to it."""
    root = bpy.data.objects.new(name, None); scn.collection.objects.link(root)
    root.location = loc; root.rotation_euler[2] = math.radians(facing_deg)
    h = height; mat = grey(name, rgb)
    parts = [("torso", (0, 0, 0.62*h), (0.34*h/1.75, 0.2*h/1.75, 0.34*h)),
             ("legs",  (0, 0, 0.24*h), (0.30*h/1.75, 0.18*h/1.75, 0.48*h)),
             ("nose",  (0, -0.12, 0.93*h), (0.04, 0.06, 0.04))]   # nose shows which way the face points (-Y)
    for pname, ploc, psize in parts:
        bpy.ops.mesh.primitive_cube_add(size=1, location=ploc)
        p = bpy.context.object; p.name = f"{name}_{pname}"; p.data.transform(Matrix.Diagonal((*psize, 1)))
        p.location = ploc; p.parent = root
        p.data.materials.append(mat)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.11*h/1.75, location=(0, 0, 0.93*h))
    head = bpy.context.object; head.name = f"{name}_head"; head.parent = root; head.data.materials.append(mat)
    return root

objs = {}
for pv_ in plan.get("pivots", []):     # empty "handles": hinges, rigs, groups. loc is relative to parent if given.
    e = bpy.data.objects.new(pv_["name"], None); scn.collection.objects.link(e)
    e.location = pv_["loc"]; e.parent = objs.get(pv_.get("parent")); objs[pv_["name"]] = e
for b in plan.get("boxes", []):
    objs[b["name"]] = box(b["name"], b["loc"], b["size"], tuple(b.get("rgb", (0.6, 0.6, 0.6))),
                          objs.get(b.get("parent")))
for f in plan.get("figures", []):
    r = figure(f["name"], f["loc"], f.get("height", 1.75), f.get("facing_deg", 0), tuple(f.get("rgb", (0.8, 0.5, 0.3))))
    if f.get("parent"): r.parent = objs[f["parent"]]
    objs[f["name"]] = r

# Keyframed motion for any object: {"object": name, "keys": [[frame, [x,y,z], [rx,ry,rz] degrees], ...]}
for anim in plan.get("animate", []):
    o = objs[anim["object"]]
    for frame, loc, rot in anim["keys"]:
        o.location = loc; o.rotation_euler = [math.radians(a) for a in rot]
        o.keyframe_insert("location", frame=frame); o.keyframe_insert("rotation_euler", frame=frame)

# Camera: lens in mm, sensor width in mm, depth of field, aimed with a Track To constraint.
c = plan["camera"]
cam_data = bpy.data.cameras.new("CAM"); cam = bpy.data.objects.new("CAM", cam_data); scn.collection.objects.link(cam)
scn.camera = cam
cam_data.lens = c["lens_mm"]; cam_data.sensor_fit = "HORIZONTAL"; cam_data.sensor_width = c.get("sensor_mm", 36.0)
if c.get("fstop"):
    cam_data.dof.use_dof = True; cam_data.dof.aperture_fstop = c["fstop"]
    if c.get("focus_on"): cam_data.dof.focus_object = objs[c["focus_on"]]
# Camera rig: RIG (moves, aims at TARGET) -> CAM (child; rolls around the lens axis).
rig = bpy.data.objects.new("CAM_RIG", None); target = bpy.data.objects.new("CAM_TARGET", None)
for o in (rig, target): scn.collection.objects.link(o)
if c.get("parent"): rig.parent = objs[c["parent"]]; target.parent = objs[c["parent"]]
cam.parent = rig
trk = rig.constraints.new("TRACK_TO"); trk.target = target; trk.track_axis = "TRACK_NEGATIVE_Z"; trk.up_axis = "UP_Y"
for frame, pos, aim, *lens in c["keys"]:          # [frame, camera position, aim point, optional lens mm]
    rig.location = pos; target.location = aim
    rig.keyframe_insert("location", frame=frame); target.keyframe_insert("location", frame=frame)
    if lens: cam_data.lens = lens[0]; cam_data.keyframe_insert("lens", frame=frame)
for frame, deg in c.get("roll_keys", []):          # roll in degrees: Dutch angle, or 180 for a world inversion
    cam.rotation_euler = (0, 0, math.radians(deg)); cam.keyframe_insert("rotation_euler", frame=frame)

light = bpy.data.objects.new("KEY", bpy.data.lights.new("KEY", "SUN")); scn.collection.objects.link(light)
light.rotation_euler = (math.radians(50), 0, math.radians(30))

def render_pass(name):
    """Render one pass as an MP4 (for video models) plus PNG stills at the key frames (for image models)."""
    im = scn.render.image_settings
    im.media_type = "VIDEO"; im.file_format = "FFMPEG"
    scn.render.ffmpeg.format = "MPEG4"; scn.render.ffmpeg.codec = "H264"
    scn.render.filepath = os.path.join(out, f"{name}.mp4")
    bpy.ops.render.render(animation=True)
    im.media_type = "IMAGE"; im.file_format = "PNG"
    stills = plan.get("stills", [scn.frame_start, (scn.frame_start + scn.frame_end) // 2, scn.frame_end])
    for f in stills:
        scn.frame_set(f); scn.render.filepath = os.path.join(out, f"{name}_f{f:04d}.png")
        bpy.ops.render.render(write_still=True)

# 1) CLAY pass: Workbench engine, flat grey studio look with outlines and cavity (fast, no GPU needed).
scn.render.engine = "BLENDER_WORKBENCH"
sh = scn.display.shading
sh.light = "STUDIO"; sh.color_type = "MATERIAL"; sh.show_object_outline = True; sh.show_cavity = True
scn.view_settings.view_transform = "Standard"   # no filmic/AgX tone curve: greys stay true
render_pass("clay")

# 2) NORMAL pass: surface direction as colour, using Blender's built-in "check_normal+y" matcap.
sh.light = "MATCAP"; sh.studio_light = "check_normal+y.exr"; sh.color_type = "SINGLE"; sh.single_color = (1, 1, 1)
sh.show_object_outline = False; sh.show_cavity = False
render_pass("normal")

# 3) DEPTH pass: distance from the lens mapped to grey (near = white, far = black) with the 5.x compositor API.
scn.view_layers[0].use_pass_z = True
scn.view_settings.view_transform = "Raw"        # data pass: no display curve, so grey level is linear in distance
tree = bpy.data.node_groups.new("depth_comp", "CompositorNodeTree"); scn.compositing_node_group = tree
rl = tree.nodes.new("CompositorNodeRLayers")
rng = tree.nodes.new("ShaderNodeMapRange")          # metres from lens -> brightness: near = white, far = black
near, far = plan.get("depth_range_m", [0.3, 15.0])
rng.inputs["From Min"].default_value, rng.inputs["From Max"].default_value = near, far
rng.inputs["To Min"].default_value, rng.inputs["To Max"].default_value = 1.0, 0.0
rng.clamp = True
outn = tree.nodes.new("NodeGroupOutput")
tree.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
tree.links.new(rl.outputs["Depth"], rng.inputs["Value"])
tree.links.new(rng.outputs["Result"], outn.inputs[0])
render_pass("depth")
scn.compositing_node_group = None; scn.view_settings.view_transform = "Standard"

# 4) PLAN VIEW: one orthographic still at frame 1 (floor plan or side elevation), red cone = shot camera.
sh.light = "STUDIO"; sh.color_type = "MATERIAL"; sh.show_object_outline = True
scn.frame_set(1)
bpy.ops.mesh.primitive_cone_add(radius1=0.25, depth=0.5, location=cam.matrix_world.translation)
marker = bpy.context.object; marker.data.materials.append(grey("cam_marker", (1, 0, 0)))
marker.rotation_euler = cam.matrix_world.to_euler(); marker.rotation_euler.x += math.pi
top = bpy.data.objects.new("TOP", bpy.data.cameras.new("TOP")); scn.collection.objects.link(top)
pv = plan.get("plan_view", {}); cx, cy, cz = pv.get("center", [0, 0, 0])
top.data.type = "ORTHO"; top.data.ortho_scale = pv.get("size_m", 8); top.data.clip_end = 500
if pv.get("direction", "top") == "top":       # looking straight down: a floor plan
    top.location = (cx, cy, cz + 50); top.rotation_euler = (0, 0, 0)
else:                                         # "side": looking along +Y: an elevation (for shafts, falls)
    top.location = (cx, cy - 50, cz); top.rotation_euler = (math.radians(90), 0, 0)
hidden = [objs[n] for n in pv.get("hide", [])]
for o in hidden: o.hide_render = True
scn.render.image_settings.media_type = "IMAGE"; scn.render.image_settings.file_format = "PNG"
scn.camera = top; scn.render.filepath = os.path.join(out, "plan_view.png")
bpy.ops.render.render(write_still=True)
bpy.data.objects.remove(marker); scn.camera = cam
for o in hidden: o.hide_render = False

# 5) CAMERA DATA: per-frame position, rotation, lens, sensor -> JSON (for video models and other tools).
frames = []
for f in range(scn.frame_start, scn.frame_end + 1):
    scn.frame_set(f); mw = cam.matrix_world
    frames.append({"frame": f, "position_m": [round(v, 4) for v in mw.translation],
                   "rotation_euler_deg": [round(math.degrees(a), 3) for a in mw.to_euler()],
                   "matrix_world": [[round(v, 5) for v in row] for row in mw],
                   "lens_mm": round(cam_data.lens, 3), "sensor_width_mm": cam_data.sensor_width,
                   "hfov_deg": round(math.degrees(2 * math.atan(cam_data.sensor_width / (2 * cam_data.lens))), 2)})
json.dump({"shot": plan.get("shot"), "fps": scn.render.fps, "resolution": plan.get("resolution"),
           "axes": "Blender world, Z up, metres; the camera looks along its own -Z axis", "frames": frames},
          open(os.path.join(out, "camera_track.json"), "w"), indent=1)

# 6) Interchange files: whole scene as USD and FBX (camera animation included), plus the .blend.
bpy.ops.wm.usd_export(filepath=os.path.join(out, "shot.usdc"))
bpy.ops.export_scene.fbx(filepath=os.path.join(out, "shot.fbx"), bake_anim=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, "shot.blend"))
print("DONE", out)
```

**What comes out** (per shot folder): `clay.mp4`, `normal.mp4`, `depth.mp4`; PNG stills of each pass at the `stills` frames; `plan_view.png`; `camera_track.json`; `shot.fbx`; `shot.usdc`; `shot.blend` [V, P58]. Harmless "EGL Error" lines appear on machines without a graphics card; rendering still succeeds [V, P58].

**The blocking check (`check_blocking.py`, 60 lines, in the kit).** "Rendered without errors" only means Python did not crash; it says nothing about a body inside a wall. The checker opens the saved `shot.blend` and, frame by frame, reports (a) any stand-in part that passes through a set piece (walls, floors, grids, sills, doors), (b) any two stand-ins passing through each other, and (c) the camera sitting inside a solid object. It prints the first frame of each problem, e.g. `CLASH frame 26: IONA_head passes through wall_S`, or `BLOCKING OK` [V, P58]. Stand-in parts are shrunk 3% so standing on a floor or touching is not reported. Run it after every render:
> `python check_blocking.py out/cage_fall/shot.blend` (bpy package) or `blender -b -P check_blocking.py -- out/cage_fall/shot.blend`

It found 3, 4 and 17 problems in the first versions of the fall, reveal and push plans, and 0 in the current five [V, P58]. It does not judge whether a pose is plausible or a hand reaches the right spot: that is still your eye on the stills.

**Extending it [J]:** ask the LLM to add cylinders or imported models (an MPFB human, a Mixamo FBX with its motion) as extra plan fields, a Follow Path option, or an EEVEE lighting pass. Always re-run all kit plans and `check_blocking.py` after a change.

### 5.4 Setting up live MCP control (optional)

1. Save your work; use a computer with nothing private on it, as the Blender Lab page advises [P10].
2. Community connector: install `uv`, add `{"command": "uvx", "args": ["mcp-for-blender"]}` to your LLM app's MCP settings, run `uvx mcp-for-blender install-addon`, enable "Interface: MCP for Blender" in Blender's add-ons, press N in the 3D view → MCP tab → **Start MCP Server** [P12].
3. Or the official connector from Blender Lab (Blender 5.1+): install its add-on in Blender (drag the downloaded file onto Blender twice, once to add the repository, once to install the extension) plus the MCP server package from its release page [P10]. In Claude it is listed as an official connector since 28 Apr 2026 [P59]; the exact switch-on steps inside Claude apps were not checked [U].
4. Test: "List the objects in the scene and take a viewport screenshot."
5. Work by asking for **plan-file edits and re-renders**, not free-form modelling, so every change is stored [J].

---

## 6. Bridging previs into AI video

Five routes, from easiest to hardest. Most shots use Route 1; hard shots combine routes.

**Route 1: restyled keyframe images → image-to-video.** Take the clay still at the shot's first frame (and last frame), restyle it with an image model that accepts a layout or structure image (C2 lists current ones; open options include the Fun ControlNet Union models for Qwen-Image 2.1 and FLUX.2 [P41]), approve the images, then run image-to-video with start-and-end frames (C1 Recipe 5). The previs fixes composition, lens and positions at both ends; the model invents the motion between. Cheap and available everywhere. Weak when the motion itself is the point.

**Route 2: control video → video-to-video.** Send `depth.mp4` (or clay, normal or a pose video) plus a reference image of the look to a control model: Wan VACE depth on fal [P39][P40], Wan 2.2 Fun Control in ComfyUI [P42], LTX-2.3 union control [P45], or the new H3 ControlNet [P43]. The camera path and blocking come through almost exactly; the model paints surfaces, faces and light. Choose **depth** for camera moves and sets, **pose** for human bodies (needs human-shaped stand-ins), **edges** for hard architecture, and combine where the tool allows [J]. The Wan family works at 16 fps [P39][P42]: generate, then have the editor retime to 24 fps. Practical limits on fal's Wan VACE depth endpoint [V, P39]: a request makes **81 to 241 frames** (default 81), so a 36- or 40-frame previs must be padded (hold its last frame) or the switch `match_input_num_frames` used; `match_input_frames_per_second` keeps your frame rate; `first_frame_url` and `last_frame_url` take the approved keyframe images; and a `preprocess` switch decides whether the service processes the input video itself (whether that means estimating depth from `clay.mp4` is not documented [U]; test both `depth.mp4` with it off and `clay.mp4` with it on).

**Route 3: clay render as a reference video to a hosted model.** Seedance 2.5 takes clay renders for "spatial structure, character poses, motion paths, and camera angles" and even derives light direction from them [P32]; MiniMax H3 copies a camera move from a reference video [P33]; Kling Motion Control copies body movement onto a character image [P34]; Marey's motion and pose transfer do the same on fal [P62]; Runway Act-Two transfers a filmed performance [P36]; Runway Aleph 2.0 and Luma Modify Video V2 restyle an existing clip [P36][P38]; the open Wan-Animate-2 transfers motion even onto non-human characters, but only on rented data-centre GPUs [P63]. Looser than Route 2 but higher image quality and, for Seedance and H3, native audio (Marey and Luma have none; audio from Kling Motion Control was not verified; C1). Best route for the non-technical user when the camera move matters [J].

**Route 4: camera numbers → camera-trajectory models.** `camera_track.json` holds the exact path. Research models (Uni3C, CameraCtrl, MotionCtrl, CameraAnything) accept camera paths, some through Kijai's ComfyUI-WanVideoWrapper [P47]–[P52]; but check what each really takes. ReCamMaster offers only ten preset moves (pan, tilt, zoom, translate, arc) [P48]; Wan 2.2 Fun Control-Camera takes preset pans and zooms [P42]; Uni3C takes seven numbers (distance, elevation, azimuth, three offsets, focal length) or presets, so the LLM must convert your track into its format [P49]; CameraAnything (27 Jul 2026) and CoaG (21 Sep 2026; cylinders on a floor grid for coarse blocking plus dolly-in, orbit, pan and crane paths, with dolly-out followed weakly) did not state released code or weights on their paper pages [P52][P53][U]. The productized alternatives are presets or directed moves from a still, not numbers (Higgsfield presets, Marey camera control) [P62][P64]. In practice Route 2 with a depth pass carries the same camera information more reliably and needs no conversion between camera formats [J]. Use Route 4 only for re-filming an already generated clip from a new angle.

**Route 5: composite what AI gets wrong.** For elements that must be geometrically exact (mirror-reversed text, screens, the diagrams on Iona's visor, floating blood beads), render them in Blender as separate layers from the same camera and lay them over the AI clip in the editor. The shared `camera_track.json` keeps them aligned [J]. Screens and visor graphics are the clearest case: the script specifies exact words ("HULL CLEARANCE", "UPWARD SPEED … Twelve. Six. Three.") that video models misspell [J; C1 §9 for text failures].

### 6.1 ComfyUI: what it is and how hard

ComfyUI is a free app in which each step (load model, load control video, extract depth, generate, save) is a box and you wire boxes into a workflow saved as a JSON file. It is the hub for open video models and all their control add-ons [P47][P55].

- **Install:** Comfy Desktop for Windows, macOS (Apple Silicon) and Linux; recommended Python 3.13; NVIDIA, AMD, Intel and Apple GPUs supported [P55].
- **Hardware:** Wan 2.2 14B control weights are a 64 GB download [P42] and want a 24 GB+ graphics card in practice [J]; smaller Wan 2.2 Fun **5B** Control and Control-Camera models exist for smaller cards [P41][U: memory needs not checked]; Uni3C tests used ~46–51 GB cards [P49]; the H3 ControlNet needs an 80 GB card [P43].
- **Cloud instead:** Comfy Cloud runs on 96 GB RTX 6000 Pro (Blackwell) cards: Standard $20/month, Creator $35, Pro $100, or $16, $28 and $80 a month when billed yearly; 5 free runs to try, no card needed. Standard cannot import your own model files (LoRAs, new checkpoints) and stops any workflow after 30 minutes (Creator also 30; Pro 1 hour) [P56].
- **LLM control:** the official `comfy-mcp` (0.10.0, 10 Aug 2026; `pip install comfy-mcp "comfy-cli>=1.14.0"`; about 40 tools) runs workflows, watches jobs, checks graphics memory, searches templates and downloads models on your machine, with a local ComfyUI running; a Comfy Cloud MCP exists at `https://cloud.comfy.org/mcp` [P57].
- **Difficulty: Hard** [J]. Missing custom nodes, model files in the wrong folder, and out-of-memory errors are routine. For a non-technical user, use fal's hosted Wan VACE endpoints first (Route 2 with no install), and move to ComfyUI only for controls that no hosted service offers.

---

## 7. Which tool for which aim

| Aim | No-3D option | Previs option (recommended [J]) | Video route | Why |
|---|---|---|---|---|
| **Exact camera move** (a push-in, a crane, a roll) | Text plus camera presets (Higgsfield's named moves; Marey's camera control from a still; C1) [P62][P64] | Plan file with camera keys; depth pass | Route 3 (Seedance 2.5 or H3 with clay reference) or Route 2 (Wan VACE depth) | Words are ambiguous about speed, height and lens; a depth video is not |
| **Exact blocking of several people** | Start and end keyframe images | Master set + box or MPFB stand-ins; plan view for sign-off | Route 1 for simple moves; Route 2 depth + reference images for complex ones | Models drift people's positions; Seedance itself flags multi-person interaction as weak [P32] |
| **Stunt or fall choreography** | Rarely works | Cascadeur (physics-checked poses) or mocap of a safe mime, on MPFB/Mixamo stand-ins | Route 2 pose + depth; or Kling Motion Control from the stand-in render | Physics is where video models fail most (C1 §9) |
| **Zero gravity** | Poor: models add gravity back | Key floating bodies and objects by hand in the cage frame; camera parented to the cage | Route 2 depth (keeps floating positions); Route 5 for blood beads | Mocap cannot record weightlessness; hand keys can |
| **A creature's body language** | Reference images + text | Box figure at true height; hinge pivots for moving parts; hand-keyed timing | Route 2 depth (pose detectors do not fit non-human shapes) + Route 3 for surface detail; or act the creature's movement yourself and transfer it with a skeleton-free model (Wan-Animate-2, cloud only) [P63][J] | Proportions and slowness are the performance |
| **Lip-synced dialogue** | Yes: image-to-video with audio (C1 Recipe 4) | Only for the coverage plan: camera positions, eyelines, the 180° line | Route 1: previs still → restyled keyframe image → talking model | Control videos fight lip sync; keep faces free [J] |
| **Matching geography across shots** | Hard to guarantee | One master set per location; every shot's camera placed in it; plan views filed in the breakdown | Any route; reuse the same set renders | The set, not the prompt, remembers where the door is |
| **Mirror-reversed world** | Generate normal, flip in edit (C1 Recipe 8) | Same set rendered normally; mark "flip" in the breakdown | Route 5 for exact backwards text | Flipping a whole clip is exact and free; whatever turned with Iona (the three characters, the cage) must be pre-reversed before the flip so it comes back the right way round (B1 §10.2) |
| **Screens, tablets, visor displays** | Unreliable text | Render the screen content as its own layer from the camera | Route 5 | Exact words, exact timing |

---

## 8. Decision rules

1. **If** a shot's meaning depends on where the camera is or how it moves (the cage fall, the reveal), **then** make previs **because** words leave speed, height and lens to chance.
2. **If** a shot is a static or simple dialogue set-up, **then** skip 3D and use keyframe images **because** previs costs more time than it saves there.
3. **If** a location appears in three or more shots, **then** build one master grey-box set before any shot **because** it guarantees the same geography in every angle.
4. **If** the LLM can run programs, **then** use headless bpy (Mode B) **because** every render is repeatable from a stored plan file; **if** it cannot, **then** have it write the script and run it yourself in Blender (Mode A).
5. **If** you want an LLM to change an open Blender scene, **then** use an MCP connector only on a machine with nothing private, after saving, **because** both connectors run arbitrary code [P10][P12].
6. **If** the control model will follow **pose**, **then** use human-shaped stand-ins (MPFB or Mixamo) **because** pose detectors cannot find a skeleton in boxes; **if** it follows **depth**, box stand-ins are enough.
7. **If** the body is not human-shaped (the figure), **then** control it with depth, not pose, **because** human pose detectors will force human proportions onto it.
8. **If** the camera move is the point of the shot, **then** prefer Route 3 (Seedance 2.5 or H3 with the clay render) or Route 2 (depth) over text **because** they take the move from the video, not from words.
9. **If** the shot has on-screen words, **then** render them in Blender and composite (Route 5) **because** models misspell and cannot mirror text reliably.
10. **If** motion must obey physics (a fall, a stop "dead", a swing), **then** key it from real numbers on every frame (free fall covers 4.9 m in the first second) or use Cascadeur **because** default easing, even between formula keys a few frames apart, slows the motion before the impact and looks like floating (§4.2).
11. **If** the scene is weightless, **then** key bodies and objects by hand relative to the cage and parent the camera to the cage **because** mocap and physics defaults assume gravity.
12. **If** a performance matters (a hand reaching, a flinch), **then** act it yourself on a phone and use motion transfer or mocap **because** you can direct your own body; hand-keying acting is an animator's skill.
13. **If** the shot has lip-synced dialogue, **then** do not feed a control video over the face **because** structure control fights mouth movement [J]; use previs only to place the camera.
14. **If** a control model runs at 16 fps (Wan family), **then** render the previs at 16 fps for that shot or retime afterwards **because** mismatched frame rates stretch the motion [J].
15. **If** you need a depth pass, **then** set the depth range to the nearest and farthest things that matter in that shot **because** a range set to the whole 30 m shaft turns the actors into a flat grey.
16. **If** a script from an LLM uses `scene.node_tree`, `BLENDER_EEVEE_NEXT` or `action.fcurves`, **then** tell it "Blender 5.2" and have it fix them **because** those were removed in 5.0 [P5].
17. **If** ComfyUI would be needed only for depth control, **then** use fal's hosted Wan VACE depth endpoint instead **because** it needs no install and costs cents per second [P39].
18. **If** a tool cannot be driven by an LLM (Previs Pro, ShotPro, FrameForge, Spark Story), **then** use it only when a person on the project enjoys operating it **because** the pipeline cannot automate it. Cascadeur (MCP server since 2026.2) and Intangible (MCP beta) are new, untested exceptions [P26][P66].
19. **If** a research camera model looks perfect in a paper, **then** do not plan around it until it is on a hosted service or in a maintained ComfyUI node **because** research code often lacks weights, licences or support [P52][P53].
20. **If** the previs still and the generated clip disagree at a key moment, **then** fix the plan file or the control strength, not the prompt wording, **because** the structure comes from the control input.
21. **If** `check_blocking.py` prints any CLASH, OVERLAP or CAMERA line, **then** fix the plan and re-render before any pass goes to a video model **because** a body inside a wall in the depth video becomes a body inside a wall in the AI clip; "rendered without errors" does not mean "physically possible" (three of the first four kit plans rendered cleanly and still failed this check).
22. **If** stand-ins travel inside a moving object (a rising cage, a car), **then** either parent them to it or key them on exactly the same frames as it, **because** two different curves drift apart between keys and the object's floor passes through their legs (the first reveal and push plans did this).
23. **If** a control clip is shorter than the video service's minimum (81 frames on fal's Wan VACE), **then** pad the previs by holding its last frame, or turn on `match_input_num_frames`, and trim afterwards **because** otherwise the service stretches or extends the motion to fit its own length [P39].
24. **If** a hosted product offers "camera control", **then** check whether it takes presets, a move directed by hand, a reference video or numbers before planning around it **because** in September 2026 none of the hosted products found accepts an exact numeric camera track; exact moves still go in as a video (Routes 2 and 3).
25. **If** a depth pass comes out pale and low in contrast, **then** check that it was rendered with the "Raw" view transform and that `depth_range_m` spans only the nearest and farthest things that matter **because** the "Standard" transform adds a display curve and a too-wide range turns actors into one grey (§4.6).
26. **If** you only want to try "3D layout → AI shot" before installing anything, **then** try a browser tool such as Intangible for an afternoon, and move to the Blender kit for the real shots **because** the browser tool is quick to learn but gives you no depth pass or camera numbers to reuse [J].

---

## 9. Difficulty ladder and minimum viable setup

| Level | What you do | Tools | Cost | When it pays off [J] |
|---|---|---|---|---|
| **0. No 3D** | Keyframe images from C2, text camera directions, image-to-video | Image and video models | Model fees only | Dialogue, inserts, simple coverage (most of *The Catch*) |
| **1. Posed stills** | Pose figures in a browser, export pose images, restyle | PoseMy.Art (free/$15), Magic Poser | $0–15/month | Exact body poses for keyframe images |
| **1b. Browser 3D layout (try-out)** | Place stand-ins and a camera in a web 3D studio that renders through hosted image and video models | Intangible (open beta) | $0 (150 one-time credits) to $35–65/month [P66] | A first feel for layout-driven shots; no passes or camera numbers to reuse [J] |
| **2. Headless clay previs (minimum viable setup)** | LLM writes plan files, renders clay/depth/plan views with the kit | bpy 5.2.2 + an LLM with a terminal | Free | Any shot with an exact camera move, blocking or geography |
| **3. Previs into control** | Depth or clay videos sent to Wan VACE (fal), Seedance 2.5, H3 | fal / Runway / Replicate MCP connectors | Cents to ~$0.50 per generated second | The hard shots: falls, zero gravity, the creature |
| **4. Performance** | Phone video → mocap → stand-in; or motion transfer | Rokoko Vision, DeepMotion, QuickMagic, Kling Motion Control, Runway Act-Two; MetaHuman's free plugin if you already use Unreal | $0–15/month + model fees | Physical acting, stunts |
| **5. Open-model control** | ComfyUI with Wan Fun Control, Uni3C, H3 ControlNet | ComfyUI Desktop + 24 GB GPU, or Comfy Cloud (80 GB+ cloud GPUs for H3 ControlNet and Wan-Animate-2) | $20–100/month on Comfy Cloud ($16–80 billed yearly), or your own GPU | Only when hosted services lack the control you need |

**Minimum viable setup (Level 2) [J]:** an LLM app that can run programs (Claude Code or similar), Python 3.13, `pip install bpy==5.2.2` (the LLM does this), the kit script and `check_blocking.py`, and a folder per shot. No Blender window, no graphics card, no 3D skill. Install the Blender app too, so you can open `shot.blend` and look around when a still confuses you.

---

## 10. Recipes (step by step, with an LLM doing the technical work)

### Recipe 1: First previs in 30 minutes (Mode B, one time)

1. Open an LLM app that can run programs (for example Claude Code) in an empty project folder.
2. Say: "Create a Python 3.13 virtual environment, install `bpy==5.2.2`, copy `C4_previs_kit/previs_from_plan.py` and `plan_cage_fall.json` here, and run it into `out/cage_fall`." (A 210–400 MB download, about 1 GB installed; bpy 5.2.2 is built for Windows, Apple-silicon Macs and Linux, not Intel Macs [P7].)
3. Ask it to show you `out/cage_fall/plan_view.png` and the clay stills, and to run `check_blocking.py out/cage_fall/shot.blend`. If you see the shaft, the cage and three coloured figures, and the checker prints `BLOCKING OK`, the setup works.
4. Also install the Blender app from blender.org (free) so you can open `shot.blend` when you want to look around yourself: middle mouse drag to orbit, Numpad 0 to look through the camera.

### Recipe 2: Build a master set for a location (per location, 20–40 minutes)

1. Give the LLM every scene description for the location plus A3's floor-plan notes.
2. Ask for a **set-only plan file**: walls, doors, openings, furniture, fixed marks (the yellow band, the sill), sizes in metres, one colour per material, and a list of the guesses it made.
3. Render a top plan view and a side elevation. Check against the script: is everything the script mentions present, in a place that makes every scripted action possible?
4. Save it as `SET_<location>.json`. Every shot plan in this location starts by copying it.

### Recipe 3: Previs one shot from the breakdown (per shot, 15–30 minutes)

1. Paste the shot's breakdown entry and the master set; use the prompt in §5.2.
2. Check the **beat list** first (frame, event, script line). Timing mistakes are cheaper to fix in words.
3. Render, then have the LLM run `check_blocking.py` on the shot and fix the plan until it prints `BLOCKING OK` (rule 21). Then look at the plan view (is the camera where the breakdown says?), then the clay stills at each beat (is the framing what the shot is for?).
4. Ask for changes in plain words ("lower the camera to knee height", "Jude clears the gate on frame 56, not 60", "roll the camera 15° by the end"). Re-render. Two or three rounds are normal.
5. Lock it: store in the breakdown the plan file path and the fields below.

**Breakdown fields for a previs shot [J]:** `previs_level` (0–5), `plan_file`, `lens_mm` and `sensor_mm`, `camera_path` (one sentence), `beats` (frame: event), `passes` (clay/depth/normal/pose), `route` (1–5 from §6), `control_strength`, `flip` (yes/no, C1 Recipe 8), `composite_layers` (screens, text, beads).

### Recipe 4: Keyframe images from clay stills (Route 1)

1. Choose the clay still for the first frame (and last frame) of the shot.
2. Send it with the character reference pack (C2) to an image model that accepts a layout image; prompt the look, not the layout ("the white strip is the worn bright steel sill; wet brick; light from the landing gates striping past; Iona in a blue work shirt…").
3. Reject images where anyone moved, changed size or lost the eyeline; the previs is the contract.
4. Use the approved images as start and end frames (C1 Recipe 5).

### Recipe 5: Depth-controlled clip via fal (Route 2, no install)

1. Connect fal's MCP connector (C1 Recipe 1).
2. Ask: "Upload `depth.mp4` and the approved first keyframe image. Using `fal-ai/wan-vace-14b/depth` (or `wan-22-vace-fun-a14b/depth`), make a 720p clip with this prompt. Pass the keyframe image as `first_frame_url`, set `match_input_num_frames` and `match_input_frames_per_second` to true and `preprocess` to false. If the clip is under 81 frames, first pad `depth.mp4` by repeating its last frame up to 81. Tell me the price first." (720p: $0.08 or $0.10 per 16 frames of output, so an 81-frame clip costs about $0.40–0.51 [P39][P40].)
3. Compare the result with the clay video at each beat. If the look is too literal (boxes with texture), make the prompt more descriptive or restyle the keyframe image more; if the camera drifts, shorten the clip; if the structure is ignored, try again with `clay.mp4` and `preprocess` on (§6, Route 2).
4. If the output came back at 16 fps, have the editor play it at 24 fps (keep every frame, change only the speed; not frame interpolation), then trim the padding.

### Recipe 6: Clay reference to a hosted model (Route 3)

1. Send `clay.mp4` as a reference video plus the character images to Seedance 2.5 reference-to-video (or H3).
2. Prompt in the model's reference style (Seedance 2.5 addresses uploads as "[Video1]", "[Image1]"; C1): "Follow [Video1] exactly for camera movement, positions and timing; it is a grey 3D layout, not the look. Characters: [Image1] is Iona (the blue figure), [Image2] is Eli (orange), [Image3] is Jude (red). Make it a photographic scene: …". Map the stand-in colours to characters explicitly [J].
3. Generate two takes; keep the one whose blocking matches the plan view. **If** people swap or merge in both takes, **then** split the shot by person (Route 2 depth per body, composite) **because** ByteDance names multi-subject interaction as a weak point [P32].

### Recipe 7: Your own performance onto a stand-in (Level 4)

1. Film yourself miming the action on a phone: locked-off camera, whole body in frame, plain background, good light (the open GVHMR pipeline also expects a locked camera [P16]).
2. Upload to Rokoko Vision (one performer) or DeepMotion (several people); download FBX (or BVH). If two of you act together in one take, use DeepMotion or QuickMagic, because Rokoko Vision captures one performer per video [P27][P28][P29].
3. Ask the LLM to import it onto an MPFB or Mixamo stand-in in the master set and re-render the passes.
4. Either send the stand-in render to Kling Motion Control with the character image [P34], or use the pose pass in Route 2.

---

## 11. Known failure modes and workarounds

| Failure | Cause | Workaround |
|---|---|---|
| Script stops with `AttributeError` on `node_tree`, `use_nodes`, `fcurves` | LLM wrote pre-5.0 Blender code [P5] | Say "Blender 5.2"; paste the error back; §4.8 table |
| Stand-ins or doors squashed or stretched | Parent object was scaled; children inherit it | Bake sizes into meshes (the kit does) [V, P58] |
| Camera sees only wall | Camera inside a wall, or clip start too large | Check plan view (red cone); set clip start 0.01–0.05 m in tight sets |
| Depth pass is one flat grey, or pale | Depth range too wide; tone or display curve applied | Set `depth_range_m` to the shot; "Raw" view transform for the depth pass (the kit does) [V, P58] |
| A stand-in passes through a wall, floor, grid or another stand-in | Plan keyed a body outside the set, or bodies not moving with the object they ride in | Run `check_blocking.py`; parent riders to the moving object or key them on the same frames (rules 21–22) [V, P58] |
| Service rejects or stretches a short control clip | Clip below the service's minimum length (81 frames on fal Wan VACE) | Pad by holding the last frame, or `match_input_num_frames`; trim after (rule 23) [P39] |
| A figure faces the wrong way | Facing convention misunderstood | Look at the nose marker; `facing_deg` 0 = −Y [V, P58] |
| Fall looks like floating | Default ease-in and ease-out, even between sparse formula keys | Key from 4.9 × t² metres on every frame; or Cascadeur physics [V, P58] |
| Output ignores the camera move | Reference route is loose | Switch to depth control (Route 2); shorten the clip |
| Output looks like painted boxes | Control too strong, prompt too thin | Lower strength (e.g. H3 ControlNet `control_context_scale` below 1.0 [P43]); richer prompt; restyled keyframe image |
| Pose control produces a mess | Box figures or the non-human figure | Human-shaped stand-ins, or depth only |
| People swap identities or merge | Several similar figures; model weakness [P32] | Distinct stand-in colours mapped to named references; split into single-subject shots; composite |
| Motion transfer breaks at the hands | Hands crossing the body in the reference [P34] | Re-perform with hands kept clear of the torso |
| Clip too slow or fast | 16 fps model output treated as 24 fps | Render control at 16 fps or retime |
| Weightless bodies sink | Mocap and physics assume gravity | Hand-key relative to the cage; parent camera to cage |
| Blood, gunshot or injury requests refused | Hosted content filters (C1 §4) | Composite the beads (Route 5); neutral wording ("small dark red droplets") |
| Glass vessel or water warps the scene | Depth of transparent things is ambiguous | Treat the vessel as a separate insert; keep it out of depth control |
| MCP session deleted or changed things | Arbitrary code execution | Save and version files; prefer plan-file edits (Mode B) |

---

## 12. Worked examples from *The Catch*

Stand-in colours used in every plan: Iona blue, Eli orange, Jude red, the figure near-black (it renders dark grey under the clay pass's studio light), sill white, band yellow. All plan files are in the kit, render without errors and pass `check_blocking.py` [V, P58]. Frame numbers are at 24 fps. The camera choices follow B1 §10 (the cage camera is level and never shakes; Iona's POV through the floor grid is top-down; the framing repeats across the black).

### Example A: the cage stops, falls, and turns (plans `plan_cage_fall.json`, `plan_grid_pov.json`, `plan_inversion_reveal.json`)

> "The opening reaches them. Iona hits STOP with her elbow. / The cage STOPS DEAD." … "Above them, something that has held for forty years gives one long METAL SHRIEK and lets go of the wall. / The cage falls. / Her boots leave the floor. She gets her fingers into the grid. Her body floats out behind her like washing. / Jude's blood lifts off the steel in round red beads and hangs in the air between them, turning." … "Through the grid, the yellow stripe. Coming." … "A hard metal CLACK. / BLACK." … "The floor grid is above her and she is holding it from underneath. The yellow stripe is under her boots, getting smaller. The brick slides past the wrong way. / The cage is going UP."

**Text floor plan (side elevation looking north, metres, Z up):**
```
 z 25 ┬ wall_W                               wall_E (upper)
      │                                      │
 11.2 │                                      ├─ top of maintenance opening
  9.2 │   ▭▭ CAGE FLOOR (grid), frames 1–12  │  OPENING → passage (east, +X)
 9.05 │                                      ├═ sill, bright white
      │         cage falls ↓ (free fall)     │ wall_E (lower)
 2.53 │   ▭▭ cage floor at frame 40 (CLACK)  │
  2.0 │ ═══ yellow band (circles the shaft) ═│
    0 ┴──────── tunnel floor ────────────────┴
     x = −1.3                            x = +1.3
 Cage 2.0 × 2.0 × 2.3 m; roof grid 2.3 m above floor; control box NW corner,
 Eli and Jude beside it; Iona flat on the grid, head west, feet east.
 The fall plan models the band on the north wall only (the one its camera sees);
 plan_grid_pov.json models it on all four walls.
```

**Camera path, shot "fall" (40 frames):**

| Frame | Beat | Camera (parented to cage; cage-relative) | Aim | Lens / roll |
|---|---|---|---|---|
| 1–12 | Stopped at sill; Iona thrown flat on the grid (lying across the frame, in profile); Eli and Jude by the control box; shriek on the soundtrack | (0.8, −0.8, 0.3): low SE corner, on the grid | Iona's middle (0.05, 0.1, 0.35) | 24 mm, f/2.8, focus Iona; level |
| 12 | Cage drops; boots leave floor | same | — | — |
| 12–40 | Free fall 9.2 → 2.53 m, keyed on **every frame** from 4.9 t²; Iona's hands (and head) stay at the grid while her legs float up and back, tilting her body to 60° by frame 40 ("like washing"); three beads rise and turn | (0.75, −0.75, 0.35) | (−0.15, 0.1, 0.95) | level throughout: no roll, no shake (B1 §10.1) |
| 40 | Cut on the CLACK | — | — | — |

**Insert, Iona's POV through the grid (`plan_grid_pov.json`, 29 frames = frames 12–40 of the fall):** the same free-fall keys; the cage floor is modelled as an open lattice of 2.5 cm bars every 25 cm so the shaft shows through; the camera is parented to the cage at (0.3, 0.25, 0.35) looking straight down, 24 mm, level. The yellow band, modelled on all four walls, starts as a thin ring far below and grows to fill the frame by frame 22 ("Through the grid, the yellow stripe. Coming."): B1's "the stripe grows shot by shot and becomes the fall's clock" [V, P58]. The other POV, "Through the grid, the opening flicks past. Going up.", is a level sideways look through the gate (B1 §10.1) and is not built in the kit: copy this plan and aim the camera at the east wall (+X).

**The inversion (shot "reveal", 36 frames, after one black frame):** the cage is built inverted (floor grid on top, roof below) and rises 5.0 → 6.4 m, slowing, so the band (2.0 m) is just below at the start and the push shot can pick up the rise at 9.0 m after the intervening beats ("Jude lies across Eli's arms. The gate has sprung open."). All three stand-ins are keyed on the same frames as the cage so they ride with it (Jude horizontal across Eli's arms). The camera is **not** parented: it stays world-upright at (0.7, −0.9, 3.2 → 4.6), aimed just above Iona's head at (−0.1, −0.4, 3.9 → 5.4), 24 mm, so the grid now sits at the **top** of frame [V, P58]. For "The yellow stripe is under her boots, getting smaller", copy `plan_grid_pov.json`, make the cage rise instead of fall and keep the camera world-upright looking down past her boots [J; not built]. This is the directing choice [J]: across the fall the camera belonged to the cage; after the black it belongs to the world, so the audience feels "Everything is in the wrong place." as a 180° swap in the frame, without a camera move. The low SE corner, 24 mm, looking up at Iona is used on both sides of the black, as B1's "Across a turn, repeat the framing." asks. If the breakdown adopts C1 Recipe 8 for the turned world (flip shots of the world horizontally in the edit, with Iona, Eli, Jude and the cage pre-reversed so they come back the right way round; B1 §10.2), the reveal is the first flipped shot; the same master set serves both sides of the turn [J].

**Kit correction [V, P58]:** the first version of the fall let Iona's floating body pass through the south shaft wall from frame 26, and the first reveal left Eli and Jude standing still while the rising cage's lower grid passed through them; `check_blocking.py` caught both. The first reveal also ran at 9.0 → 10.4 m, the same heights as the push shot that follows, which broke continuity.

**Route to video [J]:** Fall: Route 2 (`depth.mp4`, depth range 0.3–4 m) with the approved restyled first frame, because the floating positions and the level, cage-bolted camera must survive; the clip is 40 frames, so pad it to 81 for fal (rule 23); or Route 3 with Seedance 2.5 if Route 2's image quality disappoints. Grid POV: Route 2 depth, or simply Route 1, because the frame is architecture and one growing yellow ring. Blood beads: render them alone from the same camera and composite (Route 5), which also avoids injury filters. Reveal: Route 1 is enough (start frame from the clay still at frame 1, end frame at 36).

### Example B: the push through the maintenance opening (plan `plan_push_sill.json`)

> "Iona sees them together: the open side of the rising cage and, coming down to meet it, the tall maintenance opening. Slower now." … "She plants her heels on the frame. Lets go of the grid. / IONA: Push. / They go sideways together. Jude across the opening, Eli behind him, Iona holding on to both. / The sill comes down into reach. / Her arm knows it before she does. / She catches it. Her palm drags across the bright steel." … "The cage checks. Starts down. / Jude's boot clears the gate frame. / Iona's knees hit concrete."

**Text floor plan (side elevation looking north):**
```
 z 11.2 ─ top of opening ┐
                         │ OPENING in east wall, 2.2 tall (sill 2.0 wide; the kit
                         │ simplifies by leaving the whole wall width open)
  9.05 ═══ sill ═════════┼═══════ passage floor (top 9.0) ═══════ CAM ▶ (4.2, −0.8, 9.3)
                         │                                  30 cm above floor, 2.9 m from sill
   CAGE (inverted: floor grid on top at CAGE z, roof grid 2.3 m below)
   rises 9.0 → 11.6 (apex, frame 50) → 11.2 (frame 72, starting down)
   Bodies leave by the open gate side facing +X.
```

**Camera path and beats (72 frames):**

| Frame | Beat | Camera | Aim | Lens |
|---|---|---|---|---|
| 1 | Inverted cage rising into view below the sill (its top grid level with the sill; bodies inside, below) | (4.2, −0.8, 9.3), low in the passage | (1.3, 0, 9.4): the opening | 24 mm, f/4, focus Iona |
| 1–50 | Bodies ride up with the cage: their heights are keyed every 2 frames from the cage's own curve (lower grid = cage height − 2.27 m) | static | — | — |
| 37–48 | Bodies move sideways through the gate, above the sill (Jude horizontal, head first, held 0.3 m up; Eli leaning; Iona upright) | static | — | — |
| 48 | Iona's hand meets the sill (cut here to an insert of the palm, 50 mm, Level 0) | static | (1.3, 0, 9.3) | — |
| 50 | Cage apex | — | — | — |
| 50–62 | Bodies leave the cage's support and land on the passage floor (Jude's boot past the wall at 56; Iona's knees on concrete at 60) | small drift (4.4, −0.7, 9.3) by 72 | (2.0, 0, 9.2) | — |
| 72 | Cage starts down behind their feet | — | — | — |

The tested clay still at frame 48 shows the geometry the scene needs: bright sill across the lower frame, Jude's body coming head-first toward the lens, Iona and Eli behind, the inverted cage's lower grid under their feet just above the sill [V, P58]. The first kit version keyed the bodies independently of the cage, so the rising grid passed through their legs, Jude started with his body through the east wall, and legs dragged through the sill and passage floor (17 problems in `check_blocking.py`); the current plan derives the body heights from the cage's curve and passes (rule 22) [V, P58]. The upward motion is eased to a stop at frame 50 rather than using true ballistic numbers, because a real rise that stops in 2 s starts at ~20 m/s; the script asks for "Slower now.", which is a cinematic, not physical, speed [J].

**Route to video [J]:** Route 3 (Seedance 2.5 with `clay.mp4` and three character references) is the first try, because it handles image quality and multiple people together; if people swap or merge (a limitation ByteDance names [P32]), split into Route 2 depth for the bodies and Route 1 for the palm insert. Motion for the three bodies is hand-keyed (zero gravity) or, for Iona's reach and pull, mimed and captured (Recipe 7). The cage's red tag "whips against the upside-down gate" in the next shot. B1 §10.2 counts the cage among the things that turned with Iona (so it is not mirrored) and asks for no readable text in the shaft after the turn ("turn the red tag away"). **If** the tag's writing would be readable, **then** turn it away in the plan, or render it as its own layer (Route 5) so it stays the right way round when the rest of the shot is flipped **because** a flipped world-plate would otherwise mirror it too [J].

### Example C: the figure's chest opens (plan `plan_chest_opens.json`)

> "It puts its hand flat against its own chest. / Iona steps back. / Latches let go, one after another, down the front of it. / The chest swings open. / No flesh. No hollow in the shape of a person. Tubes, and a small mount, and hanging in the mount a glass VESSEL of dark water about as long as her forearm." … "One fine limb draws itself out of a socket in the wall of the vessel. Far above, the enormous black hand goes dead and hangs."

**Text floor plan (top view, outer recess, metres):**
```
 y +0.9  ═════════ back wall (dark) ═════════
 y  0.0            [ FIGURE 2.4 m tall, faces −Y ]
                   hinges at x = ±0.32, y = −0.26, z = 1.55
                   head low between shoulders; pale strip at z 2.28
 y −1.25              IONA (1.68 m) faces +Y ──► steps back to y −1.45 by frame 60
 y −1.95 … −2.4          ▲ CAM: over Iona's right shoulder
 x −1.9: fire shutter (west)
```
Figure built from boxes: legs, back plate, shoulders 0.95 m wide, a low head with a thin pale strip, arms, two chest doors on hinge pivots, and the vessel (0.14 × 0.14 × 0.45 m, "about as long as her forearm") on a mount [V, P58].

**Camera path and beats (96 frames):**

| Frame | Beat | Camera | Aim | Lens |
|---|---|---|---|---|
| 1 | Hand flat on chest (not keyed in the kit plan: add a shoulder pivot if the gesture must be exact); pale strip visible at top of frame | (0.25, −2.4, 1.7) | (0, 0, 1.9) | 35 mm, f/2.8, focus on vessel |
| 8–26 | Latches release one by one (sound effects, not keyed) | slow push begins | — | — |
| 30–70 | Left door swings 105°, right door follows 4 frames later | (0.2, −2.2, 1.65) at 60 | (0, 0, 1.6) | 35 mm |
| 40–60 | Iona steps back 20 cm | — | — | — |
| 96 | Vessel centred between the open doors | (0.12, −1.95, 1.6) | (0, −0.1, 1.55) | 50 mm |

The tested stills show frame 1 as a clean over-the-shoulder on the figure (Iona's blue head in the lower left, the pale strip at the top) and frame 96 with the vessel framed between the doors [V, P58]. Lens note: B1 allows 24 mm on the ship only for wides of its spaces and, for this beat (B1 §9.2 and its Example 5), asks for the figure at Iona's eye height, tilted up at its head, 35 mm, "the last time the camera looks up at it"; then a motivated **tilt** down with her eyes as the latches go; then the animal on a macro lens from above and level; then "A suit." on Iona's face, static, 50 mm. The kit plan matches the start (35 mm from 1.7 m, looking up at the head) and the tilt down, but adds a slow push that ends on 50 mm framing the vessel. **If** the breakdown follows B1 strictly, **then** keep the camera at (0.25, −2.4, 1.7) on 35 mm for all 96 frames and move only the aim point from (0, 0, 1.9) to (0, −0.1, 1.55) (two edits to the plan's camera keys), and cover the vessel with the macro insert below [J].

**Route to video [J]:** Doors and framing: Route 2 depth (the figure is non-human, so no pose control) with reference images of the black exosuit and pale strip from C2's pack, or Route 3 with Seedance 2.5. The transparent animal and the limb leaving its socket: separate macro inserts by image-to-video (Level 0), shot from high as B1 asks, because glass and water confuse depth control. The clip is 96 frames, above fal's 81-frame minimum. "The enormous black hand goes dead and hangs": a second small plan with a shoulder pivot keyed to drop the arm, cut in low and wide.

---

## 13. What I could not verify

- Mixamo's current official status and terms page (blocked); evidence it is in use comes from an August 2026 project [P16] and third-party status monitors.
- Prices not shown by the maker (secondary figures only, or none): FrameForge, set.a.light 3D, Autodesk Flow Studio Standard and Pro, Lightcraft Jetset and Spark Story, DeepMotion's paid plans; Unreal Engine licence terms (Epic's licence page not fetched). Move One prices come from a help page dated January 2025.
- Whether MPFB's operators can be driven reliably from headless scripts (I did not test MPFB).
- Whether LTX-2.5 has its own union-control or camera LoRAs: none on Lightricks' Hugging Face account as of 27 Sep 2026 (latest LTX-2.5 add-ons: slow-motion control, Ingredients, cinemagraph, colourisation and others) [P46].
- Whether Unreal Engine 5.9 will appear (reports say only as a maintenance release, if at all) and the Unreal Engine 6 date [P60, U].
- The exact switch-on steps for the Blender connector inside Claude's apps [P59].
- What fal's `preprocess` switch does on the Wan VACE depth endpoint (whether it estimates depth from an ordinary video) [P39].
- Cascadeur's and Intangible's MCP servers (both new; neither tested) [P26][P66].
- Meshcapade's closure (secondary sources only) [P65].
- Runway Aleph 2.0's exact limits beyond Runway's changelog (C1 [S27] is secondary).
- Any end-to-end video generation from the kit's passes: I did not run paid generations, so how well Seedance 2.5, H3, Wan VACE or Kling follow these particular clay and depth videos is untested; the routes in §6 rest on the makers' descriptions and the PrevizWhiz study [P32][P33][P39][P54].
- That `previs_from_plan.py` runs inside the Blender app GUI (tested only as the bpy package; the code uses no window features, so it should [J]).

---

## 14. Sources (all checked 2026-09-27)

- [P1] Blender download page (5.2.2 LTS, 15 Sep 2026): https://www.blender.org/download/
- [P2] Blender 5.2 LTS release (14 Jul 2026): https://www.blender.org/press/blender-5-2-lts-release/
- [P3] Blender 5.2 release notes, Virtual Reality: https://developer.blender.org/docs/release_notes/5.2/virtual_reality/
- [P4] Blender 5.2 release notes, Pipeline and I/O: https://developer.blender.org/docs/release_notes/5.2/pipeline_io/
- [P5] Blender 5.0 release notes, Python API: https://developer.blender.org/docs/release_notes/5.0/python_api/
- [P6] Blender 5.2 release notes, Python API: https://developer.blender.org/docs/release_notes/5.2/python_api/
- [P7] PyPI, bpy 5.2.2: https://pypi.org/project/bpy/
- [P8] Blender news index: https://www.blender.org/news/
- [P9] Blender, "Upcoming Blender Development Fund and AI Policies" (1 May 2026): https://www.blender.org/news/upcoming-blender-development-fund-and-ai-policies/
- [P10] Blender Lab, MCP Server: https://www.blender.org/lab/mcp-server/
- [P11] Blender Lab projects: https://www.blender.org/lab/
- [P12] mcp-for-blender (formerly blender-mcp), GitHub (the old `ahujasid/blender-mcp` address redirects here): https://github.com/ahujasid/mcp-for-blender ; rename notice: https://github.com/ahujasid/mcp-for-blender/issues/366
- [P13] PyPI, mcp-for-blender 2.1.1 and blender-mcp 2.0.0 rename notice: https://pypi.org/project/mcp-for-blender/ ; https://pypi.org/project/blender-mcp/
- [P14] Other Blender MCP projects: https://github.com/HoldMyBeer-gg/blend-ai ; https://github.com/bpy-dev/blender-mcp
- [P15] MPFB version history: https://extensions.blender.org/add-ons/mpfb/versions/
- [P16] mixamo-llm-mocap (GVHMR → Mixamo skeleton → Blender): https://github.com/squall01337/mixamo-llm-mocap
- [P17] Unreal Engine 5.8 release notes: https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-8-release-notes
- [P18] Epic, "Unreal MCP in Unreal Editor" (UE 5.8 documentation: plugins, default port 8000, console command, no authentication): https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor (replaces a community guide cited in the first draft)
- [P19] Steam, Cine Tracer: https://store.steampowered.com/app/904960/Cine_Tracer/
- [P20] Steam, Cine Tracer 2: https://store.steampowered.com/app/1774380/Cine_Tracer_2/
- [P21] FrameForge (frameforge.com redirects here): http://www.storyboardsmarter.com/
- [P22] ShotPro and its products/prices page: https://www.shotprofessional.com/ ; https://www.shotprofessional.com/products
- [P23] Previs Pro and pricing: https://www.previspro.com/ ; https://www.previspro.com/pricing
- [P24] PoseMy.Art pricing: https://posemy.art/pricing/
- [P25] Magic Poser pricing: https://magicposer.com/pricing-2.html
- [P26] Cascadeur plans, home, Mocap (Alpha) help, and CG Channel on 2026.2 (6 Aug 2026): https://cascadeur.com/plans ; https://cascadeur.com/ ; https://cascadeur.com/help/category/203 ; https://www.cgchannel.com/2026/08/nekki-releases-cascadeur-2026-2-with-animation-layers/
- [P27] Rokoko Vision: https://www.rokoko.com/products/vision
- [P28] DeepMotion Animate 3D pricing: https://www.deepmotion.com/pricing-animate3d
- [P29] QuickMagic and its pricing page: https://quickmagic.ai/ ; https://www.quickmagic.ai/Pricing
- [P30] Move.ai products, docs and Move One pricing: https://www.move.ai/products ; https://docs.move.ai/ ; https://docs.move.ai/knowledge/move-one-pricing
- [P31] Flow Studio help (wonderdynamics.com redirects to Autodesk Flow Studio), and Autodesk's freemium/pricing announcement (12 Aug 2025): https://help.wonderdynamics.com/ ; https://adsknews.autodesk.com/en/pressrelease/autodesk-launches-freemium-access-to-autodesk-flow-studio-with-new-pricing-tiers-making-world-class-vfx-ai-more-affordable-to-all-creators/
- [P32] ByteDance Seed, "Introducing Seedance 2.5" (31 Jul 2026): https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5
- [P33] MiniMax H3 blog (31 Jul 2026): https://www.minimax.io/blog/minimax-h3
- [P34] Atlas Cloud, Kling Motion Control guide (14 Jul 2026): https://www.atlascloud.ai/blog/guides/kling-ai-motion-control
- [P35] fal, Kling v3 Pro Motion Control: https://fal.ai/models/fal-ai/kling-video/v3/pro/motion-control
- [P36] Runway changelog (Aleph 2.0 13 May 2026; Aleph 2.0 in MCP 14 Jul 2026): https://runway.com/changelog
- [P37] Luma, "Introducing Ray3.2" (9 Jun 2026): https://lumalabs.ai/news/introducing-ray-3-2
- [P38] Luma, information for AI assistants (Modify Video V2): https://lumalabs.ai/llm-info
- [P39] fal, Wan VACE 14B depth, and its API schema (81–241 frames, match-input switches, `preprocess`, first/last frame): https://fal.ai/models/fal-ai/wan-vace-14b/depth ; https://fal.ai/models/fal-ai/wan-vace-14b/depth/api
- [P40] fal, Wan 2.2 VACE Fun A14B depth: https://fal.ai/models/fal-ai/wan-22-vace-fun-a14b/depth
- [P41] Hugging Face, alibaba-pai model list: https://huggingface.co/api/models?author=alibaba-pai
- [P42] Hugging Face, Wan2.2-Fun-A14B-Control-Camera model card: https://huggingface.co/alibaba-pai/Wan2.2-Fun-A14B-Control-Camera
- [P43] Hugging Face, MiniMax-H3-Fun-Controlnet-Union-2.0: https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union-2.0
- [P44] Hugging Face, Lightricks LTX-2.5: https://huggingface.co/Lightricks/LTX-2.5
- [P45] Hugging Face, LTX-2.3 IC-LoRA Union Control: https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Union-Control
- [P46] Hugging Face, Lightricks model list: https://huggingface.co/api/models?author=Lightricks
- [P47] Kijai, ComfyUI-WanVideoWrapper: https://github.com/kijai/ComfyUI-WanVideoWrapper
- [P48] ReCamMaster: https://github.com/KwaiVGI/ReCamMaster
- [P49] Uni3C: https://github.com/ewrfcas/Uni3C ; https://arxiv.org/abs/2504.14899
- [P50] CameraCtrl: https://arxiv.org/abs/2404.02101
- [P51] MotionCtrl: https://arxiv.org/abs/2312.03641
- [P52] CameraAnything (27 Jul 2026): https://arxiv.org/abs/2607.24591
- [P53] CoaG, cylinders on a grid (21 Sep 2026): https://arxiv.org/abs/2609.24208
- [P54] PrevizWhiz (Autodesk Research, CHI 2026): https://arxiv.org/abs/2602.03838
- [P55] ComfyUI system requirements: https://docs.comfy.org/installation/system_requirements
- [P56] Comfy Cloud pricing: https://www.comfy.org/cloud/pricing
- [P57] Comfy-Org comfy-mcp: https://github.com/Comfy-Org/comfy-mcp ; https://pypi.org/project/comfy-mcp/
- [P58] My own test: `pip install bpy==5.2.2` (Python 3.13, Linux, 4 CPU cores, no GPU); `previs_from_plan.py` run on all kit plans, outputs inspected (clay, normal, depth, plan view, MP4 frame counts, camera JSON), 2026-09-27. Re-test during the fact-check the same day: `check_blocking.py` on every plan (first versions: 3, 4 and 17 problems; current five: none), the free-fall curve sampled frame by frame, depth pixel values compared under "Standard" and "Raw", Blender's default key interpolation read from preferences ("BEZIER"), `bpy.data.grease_pencils_v3` confirmed absent in 5.2.2, and all five plans re-rendered with the corrected script. Files in `C4_previs_kit/`.
- [P59] Anthropic, "Claude for Creative Work" (28 Apr 2026; nine connectors incl. Blender, built by the Blender developers; updated 1 May 2026 on the donation): https://www.anthropic.com/news/claude-for-creative-work
- [P60] Unreal Engine 5.8 release (17 Jun 2026) and UE6 plans (secondary): https://www.unrealengine.com/news/unreal-engine-5-8-is-now-available (403 when fetched) ; https://wnhub.io/news/engines/item-51157 ; https://80.lv/articles/unreal-engine-5-8-is-out-today-with-big-optimization-improvements-and-mesh-terrain
- [P61] CG Channel, "Get the free MetaHuman Animator Markerless Motion Capture plugin" (18 Jun 2026): https://www.cgchannel.com/2026/06/get-the-free-metahuman-animator-markerless-mocap-plugin/
- [P62] Moonvalley, Marey features page; fal Marey endpoints: https://www.moonvalley.com/marey ; https://fal.ai/models/moonvalley/marey/motion-transfer ; https://fal.ai/models/moonvalley/marey/pose-transfer
- [P63] Hugging Face, Wan2.2-Animate-2-14B model card (weights 7 Aug 2026, Apache 2.0): https://huggingface.co/Wan-AI/Wan2.2-Animate-2-14B
- [P64] Higgsfield camera controls ("50+ Cinematic AI-Motion Presets"): https://higgsfield.ai/camera-controls
- [P65] Meshcapade closure (secondary): https://www.therundown.ai/tools/meshcapade
- [P66] Intangible FAQ and pricing (open beta; MCP beta): https://www.intangible.ai/faq ; https://www.intangible.ai/pricing
- [P67] VP Land, "Lightcraft Spark Story puts browser-based previs into every filmmaker's hands" (5 May 2026); Jetset prices (secondary): https://www.vp-land.com/p/lightcraft-spark-story-puts-browser-based-previs-into-every-filmmaker-s-hands ; https://creativecow.net/lightcraft-jetset-expands-iphone-virtual-production-tool-with-a-dozen-new-features/
- [P68] elixxier, set.a.light 3D pricing (editions and licence terms): https://www.elixxier.com/en/pricing/
- Sibling file C1 (video models, prices, aggregators) for figures marked "(C1)".
