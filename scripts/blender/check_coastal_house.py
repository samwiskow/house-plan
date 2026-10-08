"""Check the saved model against measured sources and sampled clear routes."""
import hashlib
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).parent/'coastal'))
from model import load, inside, rect, LEVELS, HEIGHTS
O=ROOT/'output/blender/coastal-house'
data=load();original=json.loads((ROOT/'studies/l-house-booklet/plans.json').read_text())['default']
bpy.ops.wm.open_mainfile(filepath=str(O/'coastal-house.blend'))
scene=bpy.context.scene;bpy.context.view_layer.update()
assert scene.unit_settings.scale_length==1
assert json.loads(scene['source_hashes'])==data['source_hashes']
rooms={r['id']:r for r in data['rooms']}
for r in original['rooms']:
    if r['id'] not in ['G2','G3','G10']:assert rooms[r['id']]['p']==r['p'],r['id']
assert abs(sum((3.5/18 for _ in range(18)))-3.5)<1e-8
assert all(s['r'][3]-(s['risers']//2-1)*s['going']>=1-1e-8 for s in data['stairs'])
assert all(s['going']>s['rise'] for s in data['stairs'])
assert all(im.packed_file for im in bpy.data.images if im.source=='FILE' and im.users)

verts=[];faces=[]
for obj in scene.objects:
    if obj.hide_render or obj.type!='MESH' or obj.get('part') not in ['walls','floors','ceilings','roof']:continue
    if 'linen ceiling shade' in obj.name:continue
    if any(m and 'glaz' in m.name.lower() for m in obj.data.materials):continue
    ev=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();offset=len(verts)
    verts.extend(ev.matrix_world@v.co for v in me.vertices)
    faces.extend(tuple(offset+i for i in p.vertices) for p in me.polygons)
    ev.to_mesh_clear()
bvh=BVHTree.FromPolygons(verts,faces)
roof_rays=0
for r in data['rooflights']:
    x,y,w,d=r['r']
    for u,v in [(.5,.5),(.25,.25),(.75,.25),(.25,.75),(.75,.75)]:
        hit=bvh.ray_cast(Vector((x+u*w,-y-v*d,6.15)),Vector((0,0,1)),5)
        assert hit[0] is None,(r['id'],'opaque rooflight',hit[0]);roof_rays+=1
ceiling_samples=0
for room in data['rooms']:
    base=LEVELS[room['floor']];height=HEIGHTS[room['floor']]
    xmin=min(p[0] for p in room['p']);xmax=max(p[0] for p in room['p'])
    ymin=min(p[1] for p in room['p']);ymax=max(p[1] for p in room['p'])
    for i in range(math.ceil((xmax-xmin)/.45)):
        for j in range(math.ceil((ymax-ymin)/.45)):
            x=xmin+.12+i*.45;y=ymin+.12+j*.45
            if not all(inside(x+dx,y+dy,room['p']) for dx,dy in [(-.04,0),(.04,0),(0,-.04),(0,.04)]):continue
            hit=bvh.ray_cast(Vector((x,-y,base+.065)),Vector((0,0,1)),height+.4)
            if hit[0] is not None:assert hit[0].z>=base+height-.005,(room['id'],'ceiling intrusion',tuple(hit[0]))
            ceiling_samples+=1
headroom=[]
for s in data['stairs']:
    x,y,w,d=s['r'];half=s['risers']//2;rise=s['rise'];run=(half-1)*s['going'];upper=LEVELS[s['upper']]
    for side in [0,1]:
        for i in range(half-1):
            z=.04+((i+1)*rise if side==0 else upper/2+(half-1-i)*rise)
            hit=bvh.ray_cast(Vector((x+.5+side*1.4,-y-(i+.5)*s['going'],z+.05)),Vector((0,0,1)),10)
            clear=hit[3]+.05 if hit[0] is not None else 10
            assert clear>=2,(s['id'],i,clear);headroom.append(clear)
for d in data['doors']:
    if d['floor']!='u':continue
    x=d['x']+(d['w']/2 if d['axis']=='h' else 0);y=d['y']+(d['w']/2 if d['axis']=='v' else 0)
    start=(x,-y-.25,4.5) if d['axis']=='h' else (x-.25,-y,4.5)
    direction=(0,1,0) if d['axis']=='h' else (1,0,0)
    assert bvh.ray_cast(Vector(start),Vector(direction),.5)[0] is None,('blocked opening',d['id'])
# Independent 700 mm suite paths, including real open door leaves.
obstacles=[]
for obj in scene.objects:
    if obj.hide_render or obj.type not in ['MESH','CURVE'] or obj.get('level')!='u' or obj.get('part') not in ['furniture','openings']:continue
    if any(t in obj.name.lower() for t in ['rug','skirting','tray','drain','ceiling','curtain','wall panel','panel flute','reading light']):continue
    points=[obj.matrix_world@Vector(c) for c in obj.bound_box]
    if not points:continue
    z0=min(p.z for p in points);z1=max(p.z for p in points)
    if z1<3.60 or z0>5.0:continue
    x0=min(p.x for p in points);x1=max(p.x for p in points);y0=-max(p.y for p in points);y1=-min(p.y for p in points)
    if x0>6.6 or y0>9.95:continue
    obstacles.append((obj.name,[x0,y0,x1-x0,y1-y0]))
routes={'bedroom':[(5.95,10.5),(5.95,3.05),(4.8,3.05)],'dressing':[(5.95,10.5),(5.95,5.175),(2.7,5.175)],'bathroom':[(5.95,10.5),(5.95,7.75),(2,7.75)],'shower':[(2,7.75),(1.85,9.05)],'WC':[(4.5,7.75),(4.5,8.65)]}
route_failures=[];route_samples=0
for name,route in routes.items():
    for a,b in zip(route,route[1:]):
        n=math.ceil(math.dist(a,b)/.05)
        for i in range(n+1):
            x=a[0]+(b[0]-a[0])*i/n;y=a[1]+(b[1]-a[1])*i/n;route_samples+=1
            for oname,(xx,yy,w,d) in obstacles:
                distance=math.hypot(max(xx-x,0,x-xx-w),max(yy-y,0,y-yy-d))
                if distance<.345:route_failures.append((name,oname,round(distance,3)));break
route_failures=list(dict.fromkeys(route_failures))
fit_failures=[];fit_objects=0
for obj in scene.objects:
    room_id=obj.get('room_id')
    if obj.hide_render or obj.type!='MESH' or not room_id:continue
    room=rooms[room_id];base=LEVELS[room['floor']];fit_objects+=1
    for corner in obj.bound_box:
        p=obj.matrix_world@Vector(corner)
        if not any(inside(p.x+dx,-p.y+dy,room['p']) for dx in [-.031,0,.031] for dy in [-.031,0,.031]):
            fit_failures.append((room_id,obj.name,'outside room'));break
        if p.z>base+HEIGHTS[room['floor']]+.01:
            fit_failures.append((room_id,obj.name,'above ceiling'));break
fit_failures=list(dict.fromkeys(fit_failures))
result={'scene_sha256':hashlib.sha256((O/'coastal-house.blend').read_bytes()).hexdigest(),'room_ceiling_rays':ceiling_samples,'furniture_meshes_checked':fit_objects,'furniture_fit_failures':fit_failures,'source_hashes':data['source_hashes'],'preserved_rooms':len(original['rooms'])-3,'rooflight_clear_rays':roof_rays,'stair_headroom_samples':len(headroom),'minimum_stair_headroom_m':round(min(headroom),3),'suite_route_samples':route_samples,'suite_route_failures':route_failures,'packed_textures':True,'units':'metres','scope':'Source equality, structural ceiling rays, furniture bounds within room outlines (31 mm tolerance), opaque opening rays, stair headroom and 700 mm nominal suite routes with modelled doors open. No construction or occupied-use certification.'}
(O/'geometry-checks.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
assert not route_failures,route_failures[:10]
assert not fit_failures,fit_failures[:20]
