"""check_blocking.py - report stand-ins that pass through the set or through each other, and cameras inside solid objects.
Run after previs_from_plan.py, on the shot.blend it saved:
  python check_blocking.py out_dir/shot.blend        (bpy 5.2.2, Python 3.13)
  blender -b -P check_blocking.py -- out_dir/shot.blend
Prints one line per problem (frame, stand-in part, set piece) and "BLOCKING OK" if none. Tested with bpy 5.2.2."""
import sys
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
bpy.ops.wm.open_mainfile(filepath=args[0])
scn = bpy.context.scene
cam = bpy.data.objects["CAM"]

def root_of(o):
    while o.parent: o = o.parent
    return o
# Stand-in parts are meshes whose top parent is a figure root (an empty with the figure's name and no mesh);
# every other mesh (walls, floors, grids, sills, doors) counts as set.
fig_roots = {o.name for o in bpy.data.objects if o.type == "EMPTY" and any(c.name.startswith(o.name + "_") for c in o.children)}
parts = [o for o in bpy.data.objects if o.type == "MESH" and o.parent and o.parent.name in fig_roots]
setp = [o for o in bpy.data.objects if o.type == "MESH" and o not in parts and not o.name.startswith("blood")]

def world_tree(o, shrink=0.97):
    """BVH of the object in world space; stand-in parts shrunk 3% so standing on a floor is not a clash."""
    m = o.matrix_world; c = sum((Vector(v.co) for v in o.data.vertices), Vector()) / len(o.data.vertices)
    verts = [m @ (c + (Vector(v.co) - c) * shrink) for v in o.data.vertices]
    return BVHTree.FromPolygons(verts, [p.vertices[:] for p in o.data.polygons]), verts

def inside(o, p):
    """Is world point p inside o's local bounding box?"""
    q = o.matrix_world.inverted() @ p; bb = [Vector(c) for c in o.bound_box]
    return all(min(b[i] for b in bb) <= q[i] <= max(b[i] for b in bb) for i in range(3))

problems, seen = 0, set()
for f in range(scn.frame_start, scn.frame_end + 1):
    scn.frame_set(f)
    set_trees = {s.name: world_tree(s, 1.0)[0] for s in setp}
    for p in parts:
        tp, pv = world_tree(p)
        centre = sum(pv, Vector()) / len(pv)
        for s in setp:
            if tp.overlap(set_trees[s.name]) or inside(s, centre):
                key = (p.name, s.name)
                if key not in seen:            # report the first frame of each clash only
                    seen.add(key); problems += 1
                    print(f"CLASH frame {f}: {p.name} passes through {s.name}")
    trees = {p.name: world_tree(p)[0] for p in parts}
    for i, a in enumerate(parts):              # two different stand-ins occupying the same space
        for b in parts[i + 1:]:
            key = (a.parent.name, b.parent.name)
            if a.parent != b.parent and key not in seen and trees[a.name].overlap(trees[b.name]):
                seen.add(key); problems += 1
                print(f"OVERLAP frame {f}: {a.name} passes through {b.name}")
    for s in setp:
        if inside(s, cam.matrix_world.translation) and ("cam", s.name) not in seen:
            seen.add(("cam", s.name)); problems += 1
            print(f"CAMERA frame {f}: camera is inside {s.name}")
print("BLOCKING OK" if problems == 0 else f"{problems} blocking problem(s): fix the plan file and re-render")
