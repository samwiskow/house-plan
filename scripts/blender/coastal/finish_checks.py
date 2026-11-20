"""Check the saved finish revision, working routes and moving shower door."""
from model import area

assert abs(area(rooms['G3']['p'])-6.655)<1e-6
assert min(p[1] for p in rooms['G3']['p'])==min(p[1] for p in rooms['G2']['p'])==5.35
assert max(p[1] for p in rooms['G3']['p'])==max(p[1] for p in rooms['G2']['p'])==9.3
option=json.loads((ROOT/'output/design/kitchen-selections/boot-room-option.json').read_text())
assert rooms['G4']['p']==option['room_polygons']['G4']
parquet_names=['G2 continuous herringbone','G3 continuous herringbone','Kitchen pantry continuous threshold']
assert {scene.objects[n].data.materials[0].name for n in parquet_names}=={'K01 pale oak herringbone'}
for room_id in ['G4','G10']:
    assert scene.objects.get(room_id+' stone floor')
    assert not any(o.name.startswith(room_id+' oak board') for o in scene.objects)
pocket_names=[]
for door in data['doors']:
    if door['style']!='pocket':continue
    root=scene.objects[door['id']+' hinge'];axis=door['axis'];wall=door['y'] if axis=='h' else door['x']
    start=(door['x'] if axis=='h' else door['y'])+(door['w'] if door['slide']>0 else -door['w']-.03)
    for obj in root.children:
        x0,x1,y0,y1,z0,z1=bounds(obj)
        lo,hi,c0,c1=(x0,x1,y0,y1) if axis=='h' else (y0,y1,x0,x1)
        assert lo>=start-1e-5 and hi<=start+door['w']+.03+1e-5,('pocket length',obj.name)
        assert c0>=wall-.05 and c1<=wall+.05,('pocket thickness',obj.name)
    pocket_names.append(door['id'])
assert len(pocket_names)==6
seam_count=0
for obj in scene.objects:
    if 'pitch_gradient' not in obj:continue
    x0,x1,y0,y1,_,_=bounds(obj);dx,dy=obj['pitch_gradient']
    assert (y1-y0<=.00901 if abs(dx)>abs(dy) else x1-x0<=.00901),('roof seam across pitch',obj.name)
    assert obj['seam_height']==.025 and obj['panel_spacing']==.43
    seam_count+=1
house_treads=[bounds(o) for o in scene.objects if o.name.startswith('House stair closed tread')]
assert min(house_treads,key=lambda b:b[5])[0]>9.5
assert max(house_treads,key=lambda b:b[5])[1]<9.3
stair_meshes=[o for o in scene.objects if o.type=='MESH' and o.name.startswith(('House stair closed tread','House stair oak stringer','House stair half landing'))]
stair_vertices=[];stair_faces=[]
for obj in stair_meshes:
    offset=len(stair_vertices);stair_vertices.extend(obj.matrix_world@v.co for v in obj.data.vertices)
    stair_faces.extend(tuple(offset+i for i in face.vertices) for face in obj.data.polygons)
stair_bvh=BVHTree.FromPolygons(stair_vertices,stair_faces)
storage=[o for o in scene.objects if o.name.startswith('Lower stair fitted storage body')]
assert len(storage)==5
for obj in storage:
    for vertex in obj.data.vertices:
        point=obj.matrix_world@vertex.co
        hit=stair_bvh.ray_cast(Vector((point.x,point.y,.045)),Vector((0,0,1)),3.5)
        assert hit[0] is not None and point.z<hit[0].z-.015,('fitted storage hits stairs',obj.name,tuple(point),hit[0])
for xx in [8.6,9.4,10.2]:
    for zz in [.9,2.7]:assert bvh.ray_cast(Vector((xx,-14.3,zz)),Vector((0,-1,0)),.7)[0] is None,('stair window blocked',xx,zz)
pantry_hinge=scene.objects['Kitchen → pantry hinge'];pantry_angle=pantry_hinge.rotation_euler.z
assert abs(pantry_angle+math.pi/2)<1e-6
pantry_leaf=bounds(scene.objects['Kitchen → pantry framed leaf'])
assert pantry_leaf[0]<11.02 and pantry_leaf[2]<6.45 and pantry_leaf[3]>7.25
for yy in [7.86,7.94,8.015]:
    for zz in [.5,1.5,2.6]:
        hit=scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((10.5,-yy,zz)),Vector((1,0,0)),distance=.55)
        assert hit[0],('kitchen cabinet gap',yy,zz)
pantry_hinge.rotation_euler.z=0;bpy.context.view_layer.update()

service_obstacles=[]
for obj in scene.objects:
    if obj.hide_render or obj.type not in ['MESH','CURVE'] or obj.get('level')!='g' or obj.get('part') not in ['furniture','openings','interior']:continue
    if any(t in obj.name.lower() for t in ['rug','skirting','drain','curtain']):continue
    x0,x1,y0,y1,z0,z1=bounds(obj)
    if z1<.065 or z0>2.0:continue
    service_obstacles.append((obj.name,(x0,x1,y0,y1)))
service_routes={
    'hall to pantry and utility':[(11.90,14.3),(11.90,13.4),(11.65,13.1),(11.65,10.65),(10.35,10.65),(10.325,9),(10.50,8.50),(10.50,6.85),(12.4,6.85),(14.65,6.85)],
    'utility to boot room':[(14.65,6.85),(14.65,8.9),(15.15,9.4),(15.15,12.7)]}
service_failures=[];service_samples=0
for name,route in service_routes.items():
    for pa,pb in zip(route,route[1:]):
        count=math.ceil(math.dist(pa,pb)/.05)
        for step in range(count+1):
            x=pa[0]+(pb[0]-pa[0])*step/count;y=pa[1]+(pb[1]-pa[1])*step/count;service_samples+=1
            for direction in range(8):
                angle=direction*math.pi/4
                assert bvh.ray_cast(Vector((x,-y,1.0)),Vector((math.cos(angle),math.sin(angle),0)),.345)[0] is None,('route wall',name,x,y)
            for oname,(x0,x1,y0,y1) in service_obstacles:
                distance=math.hypot(max(x0-x,0,x-x1),max(y0-y,0,y-y1))
                if distance<.345:service_failures.append((name,oname,round(distance,3)));break
service_failures=list(dict.fromkeys(service_failures))
assert not service_failures,service_failures[:20]

# Test the real door vertices at one-degree intervals against adjacent solid fittings.
def overlap(p,q):
    for poly in [p,q]:
        for a,b in zip(poly,poly[1:]+poly[:1]):
            nx,ny=-(b[1]-a[1]),b[0]-a[0]
            if nx*nx+ny*ny<1e-12:continue
            ap=[x*nx+y*ny for x,y in p];bp=[x*nx+y*ny for x,y in q]
            if min(max(ap),max(bp))<=max(min(ap),min(bp))+.00001:return False
    return True
hinge=scene.objects['Ensuite shower door hinge'];old_angle=hinge.rotation_euler.z
fixed=[o for o in scene.objects if o.type in ['MESH','CURVE'] and o.get('level')=='u' and any(t in o.name.lower() for t in ['wall control','ofuro','vanity'])]
door_checks=0
for degrees in range(91):
    hinge.rotation_euler.z=math.radians(degrees);bpy.context.view_layer.update()
    for obj in hinge.children:
        bb=bounds(obj)
        points=[obj.matrix_world@Vector(v) for v in obj.bound_box]
        # Four bottom corners in perimeter order.
        low=sorted({(round(p.x,7),round(-p.y,7)) for p in points})
        cx=sum(p[0] for p in low)/len(low);cy=sum(p[1] for p in low)/len(low)
        poly=sorted(low,key=lambda p:math.atan2(p[1]-cy,p[0]-cx))
        for solid in fixed:
            sb=bounds(solid)
            if min(bb[5],sb[5])<=max(bb[4],sb[4]):continue
            assert not overlap(poly,rect(sb[0],sb[2],sb[1]-sb[0],sb[3]-sb[2])),('shower swing collision',degrees,obj.name,solid.name)
        door_checks+=1
hinge.rotation_euler.z=old_angle;bpy.context.view_layer.update()
pantry_hinge.rotation_euler.z=pantry_angle;bpy.context.view_layer.update()
revision_checks.update(stair_window_clear_rays=6,integrated_lower_stair_storage_modules=5,concealed_pantry_leaf=True,kitchen_cabinet_gap_blocked_rays=9,pantry_area_m2=6.655,pocket_doors_inside_wall=pocket_names,stone_service_rooms=['G4','G10'],continuous_parquet=parquet_names,roof_pitch_seams=seam_count,swapped_stair_flights=True,under_stair_storage_clear=True,service_route_samples=service_samples,service_route_failures=service_failures,shower_door_sweep_component_checks=door_checks)

sky=next(node for node in scene.world.node_tree.nodes if node.type=='TEX_SKY')
assert sky.sun_disc and abs(math.degrees(sky.sun_elevation)-7)<1e-5
assert abs(math.degrees(sky.sun_rotation)-337)<1e-4
assert not any(obj.type=='LIGHT' and obj.data.type=='SUN' for obj in scene.objects)
if (O/'coastal-golden-hour.hdr').exists():
    from array import array
    hdr=bpy.data.images.load(str(O/'coastal-golden-hour.hdr'),check_existing=True)
    pixels=array('f',[0.0])*(hdr.size[0]*hdr.size[1]*4);hdr.pixels.foreach_get(pixels)
    peak=max(range(0,len(pixels),4),key=lambda i:pixels[i]+pixels[i+1]+pixels[i+2])//4
    sun_pixel=[peak%hdr.size[0],peak//hdr.size[0]]
    assert abs(sun_pixel[0]-190)<3 and abs(sun_pixel[1]-276)<3,('HDR sun direction',sun_pixel)
    revision_checks['golden_hour_environment_sha256']=hashlib.sha256((O/'coastal-golden-hour.hdr').read_bytes()).hexdigest()
    revision_checks['sun_pixel_1024x512']=sun_pixel
revision_checks['single_physical_sky_sun_elevation_degrees']=7
