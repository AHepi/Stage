"""render_previs.py: render grey preview plans in Blender, check them, and lay them out on a contact sheet page.

What this file does, in plain words (blueprint 9, add-on B):
- for each plan file (the kit's plan format, C4 section 5.2), it runs the kit's previs_from_plan.py, unchanged,
  which writes the clay, normal and depth renders, the plan view, the camera track and shot.blend;
- it runs the kit's check_blocking.py, unchanged, on shot.blend and reads its CLASH, OVERLAP and CAMERA lines.
  A CLASH between a stand-in and the seat or bed it rests on is excused when the plan's clash_exclusions list
  names that pair (a seated stand-in on its chair, blueprint 9); every other line means the blocking is not OK
  (PREVIS-02);
- it reads each figure's facing in shot.blend at the plan's stills and compares it with the facing the records
  give (the plan's derived_facings); a difference over facing_tolerance_deg is PREVIS-03. A plan that could not
  be built in Blender is PREVIS-01;
- it writes one contact sheet page per scene: the plan view and the clay stills of each shot with its one-line
  description, for the user's one question at checkpoint D.

It needs Blender's Python module (bpy) only to run the kit scripts and to read facings, and it runs them in a
separate process: the Python running this file needs only the standard library. It finds Blender in this order:
this Python when it can import bpy (pip install bpy); else the Blender app on the PATH (blender -b -P ...).

Run it by hand on any plan files (for example the kit's own plans):
    python render_previs.py plans/plan_chest_opens.json --out out/chest
    python render_previs.py a.json b.json --out renders --sheet renders/contact sheet.html
stage.py previs --render calls render_plan and write_contact_sheet from here for a project.
Exit codes: 0 every plan rendered with BLOCKING OK and facings in tolerance; 1 problems printed; 2 could not run.
"""

import argparse
import html
import importlib.util
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import quote

KIT_FOLDER = Path(__file__).resolve().parent
PLAN_SCRIPT = KIT_FOLDER / "previs_from_plan.py"
CHECK_SCRIPT = KIT_FOLDER / "check_blocking.py"
THIS_SCRIPT = Path(__file__).resolve()

# What the kit writes into a shot's folder; old copies of these (and nothing else) are cleared before a new render.
KIT_OUTPUT = re.compile(r"^(clay|normal|depth)(_f\d{4})?\.(mp4|png)$|^plan_view\.png$|^camera_track\.json$"
                        r"|^shot\.(blend|blend1|fbx|usdc)$")
BLOCKING_LINE = re.compile(r"^(CLASH|OVERLAP|CAMERA) frame (\d+): (.+)$")
CLASH_PARTS = re.compile(r"^(.+?) passes through (.+)$")
# The facing tolerance when a plan does not carry one (constants.json facing_tolerance_deg, blueprint 9).
DEFAULT_FACING_TOLERANCE_DEG = 20
# How long one kit script may run before it is stopped (seconds); a long shot at full size takes minutes.
DEFAULT_TIMEOUT_S = 3600


# ---------------------------------------------------------------- finding Blender

class BlenderRunner:
    """How to run a script under Blender's Python: this Python (it has bpy) or the Blender app."""

    def __init__(self, kind, program):
        self.kind = kind          # "module" (a Python that imports bpy) or "app" (the blender program)
        self.program = program

    def command(self, script, arguments):
        if self.kind == "module":
            return [self.program, str(script)] + [str(argument) for argument in arguments]
        return [self.program, "-b", "--factory-startup", "-P", str(script), "--"] + [str(argument) for argument in arguments]

    def describe(self):
        return "Blender's Python module in this Python" if self.kind == "module" else f"the Blender app ({self.program})"


def find_blender():
    """A BlenderRunner, or None when neither bpy nor the Blender app can be found."""
    if importlib.util.find_spec("bpy") is not None:
        return BlenderRunner("module", sys.executable)
    program = shutil.which("blender")
    if program:
        return BlenderRunner("app", program)
    return None


def run_script(runner, script, arguments, timeout):
    """Run one kit script; (exit code, the printed lines, the error lines, seconds)."""
    started = time.monotonic()
    environment = dict(os.environ)
    environment.setdefault("PYTHONUNBUFFERED", "1")
    try:
        finished = subprocess.run(runner.command(script, arguments), capture_output=True, text=True,
                                  timeout=timeout, env=environment)
    except subprocess.TimeoutExpired:
        return None, [], [f"stopped after {timeout} seconds"], time.monotonic() - started
    except OSError as error:
        return None, [], [str(error)], time.monotonic() - started
    return (finished.returncode, finished.stdout.splitlines(), finished.stderr.splitlines(),
            time.monotonic() - started)


# ---------------------------------------------------------------- one plan

def plan_name(plan, plan_path):
    return str(plan.get("shot") or Path(plan_path).stem)


def clear_old_renders(out_folder):
    """Remove the files an earlier render of the kit left in this folder (and only those), so no old still stays."""
    if not out_folder.is_dir():
        return
    for path in out_folder.iterdir():
        if path.is_file() and KIT_OUTPUT.match(path.name):
            path.unlink()


def excused(line, exclusions):
    """True when a CLASH line is a stand-in resting on a seat or bed the plan's clash_exclusions names for it."""
    match = BLOCKING_LINE.match(line)
    if not match or match.group(1) != "CLASH":
        return False
    parts = CLASH_PARTS.match(match.group(3))
    if not parts:
        return False
    part, set_piece = parts.group(1), parts.group(2)
    for exclusion in exclusions or []:
        if exclusion.get("set") != set_piece:
            continue
        for stand_in in exclusion.get("stand_ins", []):
            if part == stand_in or part.startswith(stand_in + "_"):
                return True
    return False


def angle_apart(first, second):
    """The smaller angle between two facings, in degrees (0 to 180)."""
    difference = abs((first - second) % 360)
    return min(difference, 360 - difference)


def read_facings(runner, blend_path, request, timeout):
    """{figure: [[frame, facing_deg], ...]} read from shot.blend (the direction its nose points), or None."""
    with tempfile.TemporaryDirectory() as folder:
        request_path = Path(folder) / "facings request.json"
        request_path.write_text(json.dumps(request), encoding="utf-8")
        code, lines, errors, _ = run_script(runner, THIS_SCRIPT, ["--read-facings", blend_path, request_path], timeout)
    for line in lines:
        if line.startswith("FACINGS "):
            return json.loads(line[len("FACINGS "):])
    return None


def render_plan(plan_path, out_folder, runner=None, timeout=DEFAULT_TIMEOUT_S, check_facings=True):
    """Render one plan with the kit, run the blocking check, compare facings. Returns a plain dict:
    name, out_folder, rendered, render_seconds, check_seconds, blocking_ok, blocking_lines (the problems left),
    excused_lines, facing_checks [{figure, frame, rendered, derived, apart}], facing_problems (the same, over
    tolerance), tolerance, problems [(check ID, text)], error."""
    plan_path = Path(plan_path)
    out_folder = Path(out_folder)
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    name = plan_name(plan, plan_path)
    tolerance = plan.get("facing_tolerance_deg", DEFAULT_FACING_TOLERANCE_DEG)
    result = {"name": name, "plan": str(plan_path), "out_folder": str(out_folder), "rendered": False,
              "render_seconds": None, "check_seconds": None, "blocking_ok": False, "blocking_lines": [],
              "excused_lines": [], "facing_checks": [], "facing_problems": [], "tolerance": tolerance,
              "frames": plan.get("frames"), "problems": [], "error": None}
    runner = runner or find_blender()
    if runner is None:
        result["error"] = "Blender's Python module (bpy) and the Blender app were not found"
        result["problems"].append(("PREVIS-01", "could not be rendered: " + result["error"]))
        return result
    out_folder.mkdir(parents=True, exist_ok=True)
    clear_old_renders(out_folder)
    code, lines, errors, seconds = run_script(runner, PLAN_SCRIPT, [plan_path, out_folder], timeout)
    result["render_seconds"] = round(seconds, 1)
    blend = out_folder / "shot.blend"
    if code != 0 or not blend.is_file() or not any(line.startswith("DONE") for line in lines):
        detail = [line for line in errors + lines if line.strip() and "EGL" not in line][-3:]
        result["error"] = "Blender could not build the plan" + (": " + " / ".join(detail) if detail else "")
        result["problems"].append(("PREVIS-01", result["error"]))
        return result
    result["rendered"] = True
    code, lines, errors, seconds = run_script(runner, CHECK_SCRIPT, [blend], timeout)
    result["check_seconds"] = round(seconds, 1)
    finding = [line.strip() for line in lines if BLOCKING_LINE.match(line.strip())]
    printed_ok = any(line.strip() == "BLOCKING OK" for line in lines)
    if code != 0 or not (printed_ok or finding or any("blocking problem" in line for line in lines)):
        detail = [line for line in errors + lines if line.strip() and "EGL" not in line][-3:]
        result["error"] = "the blocking check could not run" + (": " + " / ".join(detail) if detail else "")
        result["problems"].append(("PREVIS-02", result["error"]))
        return result
    exclusions = plan.get("clash_exclusions") or []
    result["excused_lines"] = [line for line in finding if excused(line, exclusions)]
    result["blocking_lines"] = [line for line in finding if not excused(line, exclusions)]
    result["blocking_ok"] = not result["blocking_lines"]
    for line in result["blocking_lines"]:
        result["problems"].append(("PREVIS-02", "blocking not OK: " + line))
    derived = plan.get("derived_facings") or {}
    if check_facings and derived:
        request = {figure: [frame for frame, _ in entries] for figure, entries in derived.items()}
        rendered = read_facings(runner, blend, request, timeout)
        if rendered is None:
            result["problems"].append(("PREVIS-03", "the figures' facings could not be read from shot.blend"))
        else:
            for figure, entries in derived.items():
                measured = dict((frame, value) for frame, value in (rendered.get(figure) or []))
                for frame, wanted in entries:
                    found = measured.get(frame)
                    if found is None:
                        check = {"figure": figure, "frame": frame, "rendered": None, "derived": wanted, "apart": None}
                        result["facing_checks"].append(check)
                        result["facing_problems"].append(check)
                        result["problems"].append(("PREVIS-03", f"{figure} is missing from the render at frame {frame}"))
                        continue
                    apart = round(angle_apart(found, wanted), 1)
                    check = {"figure": figure, "frame": frame, "rendered": found, "derived": wanted, "apart": apart}
                    result["facing_checks"].append(check)
                    if apart > tolerance:
                        result["facing_problems"].append(check)
                        result["problems"].append((
                            "PREVIS-03", f"{figure} faces {found:g} degrees at frame {frame}, but the records give "
                                         f"{wanted:g} degrees ({apart:g} apart; at most {tolerance:g})"))
    return result


# ---------------------------------------------------------------- reading facings inside Blender

def read_facings_in_blender(blend_path, request_path):
    """Runs under Blender's Python: print FACINGS {figure: [[frame, facing_deg], ...]} for the request."""
    import bpy  # only here: this function runs in the Blender process
    from mathutils import Vector
    request = json.loads(Path(request_path).read_text(encoding="utf-8"))
    bpy.ops.wm.open_mainfile(filepath=str(blend_path))
    scene = bpy.context.scene
    found = {}
    for figure, frames in request.items():
        target = bpy.data.objects.get(figure)
        if target is None:
            found[figure] = []
            continue
        values = []
        for frame in frames:
            scene.frame_set(int(frame))
            nose = target.matrix_world.to_3x3() @ Vector((0.0, -1.0, 0.0))   # the kit's nose points along -Y
            heading = math.degrees(math.atan2(nose.y, nose.x))
            values.append([int(frame), round((heading + 90.0) % 360.0, 2)])
        found[figure] = values
    print("FACINGS " + json.dumps(found), flush=True)


# ---------------------------------------------------------------- the contact sheet

SHEET_STYLE = """
:root { --paper: #f7f6f2; --ink: #1d1d1b; --soft: #5d5d58; --line: #d9d7cf; --good: #2f6b3a; --bad: #9b2c2c;
        --card: #ffffff; }
@media (prefers-color-scheme: dark) {
  :root { --paper: #1b1b1a; --ink: #eceae4; --soft: #a9a79f; --line: #3a3a37; --good: #7fc28a; --bad: #e08a8a;
          --card: #242423; }
}
* { box-sizing: border-box; }
body { margin: 0; padding: 24px 16px 48px; background: var(--paper); color: var(--ink);
       font: 16px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }
main { max-width: 1100px; margin: 0 auto; }
h1 { font-size: 1.6rem; margin: 0 0 4px; }
.question { font-size: 1.1rem; margin: 12px 0 24px; padding: 12px 16px; border-left: 4px solid var(--ink);
            background: var(--card); }
section.shot { background: var(--card); border: 1px solid var(--line); border-radius: 8px; padding: 16px;
               margin: 0 0 24px; }
section.shot h2 { font-size: 1.25rem; margin: 0 0 4px; }
.what { margin: 0 0 12px; }
.result { margin: 4px 0; color: var(--soft); }
.result.good { color: var(--good); }
.result.bad { color: var(--bad); }
.strip { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 12px; margin-top: 12px; }
figure { margin: 0; }
figure img { width: 100%; height: auto; display: block; border: 1px solid var(--line); background: #888; }
figcaption { font-size: 0.85rem; color: var(--soft); margin-top: 4px; }
.note { color: var(--soft); font-size: 0.9rem; }
"""


def still_caption(frame, moments, fps, handle_frames=0, frames=None):
    """A plain caption for a still: the frame, its second in the shot, and the moment that starts there."""
    seconds = (frame - 1 - handle_frames) / fps if fps else 0
    if handle_frames and frame <= handle_frames:
        caption = f"frame {frame} (the handle before the shot starts)"
    elif handle_frames and frames and frame > frames - handle_frames:
        caption = f"frame {frame} (the handle after the shot ends)"
    else:
        caption = f"frame {frame} ({seconds:.1f} seconds into the shot)"
    for moment in moments or []:
        if moment and moment[0] == frame and len(moment) > 1:
            caption += ": " + str(moment[1])
    return caption


def write_contact_sheet(path, title, entries, question):
    """One page: the question, then per shot its label, one-line description, results, plan view and stills.
    entries: [{"label", "description", "folder" (relative to the page), "stills", "moments", "fps",
    "result_lines" [(good, text)], "needs_answer", "notes"}]."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    parts = ["<!doctype html>", '<html lang="en">', "<head>", '<meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width, initial-scale=1">',
             f"<title>{html.escape(title)}</title>", f"<style>{SHEET_STYLE}</style>", "</head>", "<body>", "<main>",
             f"<h1>{html.escape(title)}</h1>", f'<p class="question">{html.escape(question)}</p>']
    for entry in entries:
        folder = entry.get("folder", "")
        parts.append('<section class="shot">')
        heading = entry["label"] + (" (needs your answer)" if entry.get("needs_answer") else "")
        parts.append(f"<h2>{html.escape(heading)}</h2>")
        if entry.get("description"):
            parts.append(f'<p class="what">{html.escape(entry["description"])}</p>')
        for good, text in entry.get("result_lines", []):
            parts.append(f'<p class="result {"good" if good else "bad"}">{html.escape(text)}</p>')
        for note in entry.get("notes", []):
            parts.append(f'<p class="note">{html.escape(note)}</p>')
        parts.append('<div class="strip">')
        plan_view = quote(f"{folder}/plan_view.png" if folder else "plan_view.png")
        parts.append(f'<figure><img src="{html.escape(plan_view)}" alt="The plan from above, the red cone is the camera">'
                     "<figcaption>the plan from above; the red cone is the camera</figcaption></figure>")
        for frame in entry.get("stills", []):
            image = quote(f"{folder}/clay_f{int(frame):04d}.png" if folder else f"clay_f{int(frame):04d}.png")
            caption = still_caption(int(frame), entry.get("moments"), entry.get("fps", 24),
                                    entry.get("handle_frames", 0), entry.get("frames"))
            parts.append(f'<figure><img src="{html.escape(image)}" alt="{html.escape(caption)}">'
                         f"<figcaption>{html.escape(caption)}</figcaption></figure>")
        parts.append("</div>")
        parts.append("</section>")
    parts += ["</main>", "</body>", "</html>", ""]
    temporary = path.with_suffix(".html.part")
    temporary.write_text("\n".join(parts), encoding="utf-8")
    temporary.replace(path)
    return path


def result_lines(result):
    """Plain lines for a render result: [(good, text)]."""
    lines = []
    if result.get("error"):
        return [(False, "Not rendered: " + result["error"] + ".")]
    frames = result.get("frames")
    seconds = (result.get("render_seconds") or 0) + (result.get("check_seconds") or 0)
    if result.get("blocking_ok"):
        text = "BLOCKING OK: no stand-in passes through the set or another stand-in, and the camera is in the open."
        if result.get("excused_lines"):
            text += f" ({len(result['excused_lines'])} contact with a seat or bed excused.)"
        lines.append((True, text))
    else:
        for line in result.get("blocking_lines", []):
            lines.append((False, "Blocking not OK: " + line))
    if result.get("facing_checks"):
        worst = max((check["apart"] or 0) for check in result["facing_checks"])
        if result.get("facing_problems"):
            count, total = len(result["facing_problems"]), len(result["facing_checks"])
            lines.append((False, f"Facings: {count} of {total} readings {'differs' if count == 1 else 'differ'} "
                                 f"from the records by more than {result['tolerance']:g} degrees."))
        else:
            lines.append((True, f"Facings: every figure within {result['tolerance']:g} degrees of the records "
                                f"(largest difference {worst:g})."))
    lines.append((True, f"{frames} frames, rendered and checked in {seconds:.0f} seconds."))
    return lines


# ---------------------------------------------------------------- by hand

def main(argv=None):
    parser = argparse.ArgumentParser(description="Render grey preview plans, check the blocking and the facings.")
    parser.add_argument("plans", nargs="*", help="plan files in the kit's format")
    parser.add_argument("--out", help="the folder for the renders (one subfolder per plan when there are several)")
    parser.add_argument("--sheet", help="also write a contact sheet page here")
    parser.add_argument("--title", default="Grey previews", help="the contact sheet's title")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_S, help="seconds one kit script may run")
    parser.add_argument("--read-facings", nargs=2, metavar=("BLEND", "REQUEST"), help=argparse.SUPPRESS)
    arguments = parser.parse_args(argv)
    if arguments.read_facings:
        read_facings_in_blender(*arguments.read_facings)
        return 0
    if not arguments.plans or not arguments.out:
        print("Give one or more plan files and --out <folder>.")
        return 2
    runner = find_blender()
    if runner is None:
        print("Rendering needs Blender's Python module (pip install bpy) or the Blender app on the PATH; "
              "neither was found.")
        return 2
    out = Path(arguments.out)
    entries = []
    failing = False
    for plan_path in arguments.plans:
        plan = json.loads(Path(plan_path).read_text(encoding="utf-8"))
        name = plan_name(plan, plan_path)
        folder = out / name if len(arguments.plans) > 1 else out
        result = render_plan(plan_path, folder, runner, arguments.timeout)
        if result["blocking_ok"] and not result["problems"]:
            print(f"{name}: BLOCKING OK" + (f", facings within {result['tolerance']:g} degrees"
                                             if result["facing_checks"] else "")
                  + f" ({result['render_seconds']} + {result['check_seconds']} seconds)")
        for check_id, text in result["problems"]:
            failing = True
            print(f"E {check_id} {name} {text}.")
        for line in result["excused_lines"]:
            print(f"{name}: excused (a stand-in resting on its seat or bed): {line}")
        if arguments.sheet:
            relative = os.path.relpath(folder, Path(arguments.sheet).parent)
            entries.append({"label": name, "description": plan.get("description", ""),
                            "folder": Path(relative).as_posix(), "stills": plan.get("stills", []),
                            "moments": plan.get("moments", []), "fps": plan.get("fps", 24),
                            "handle_frames": plan.get("handle_frames", 0), "frames": plan.get("frames"),
                            "result_lines": result_lines(result)})
    if arguments.sheet:
        write_contact_sheet(arguments.sheet, arguments.title, entries,
                            "Reply with the numbers of any that look wrong, or 'fine'.")
        print(f"Written: {arguments.sheet}")
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
