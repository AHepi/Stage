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
