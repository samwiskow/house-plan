"""Measured fittings, CC0 objects and surface detail for the golden-hour review."""

def place_asset(asset_id,centre,z,max_width,max_depth,room_id,angle=0,soft=False):
    before=set(scene.objects)
    bpy.ops.import_scene.gltf(filepath=str(ROOT/'assets/coastal-study'/asset_id/(asset_id+'_1k.gltf')))
    bpy.context.view_layer.update();added=set(scene.objects)-before
    points=[obj.matrix_world@Vector(v) for obj in added if obj.type=='MESH' for v in obj.bound_box]
    lo=Vector(tuple(min(p[i] for p in points) for i in range(3)));hi=Vector(tuple(max(p[i] for p in points) for i in range(3)))
    scale=min(max_width/(hi.x-lo.x),max_depth/(hi.y-lo.y))
    transform=Matrix.Translation((centre[0],-centre[1],z))@Matrix.Rotation(angle,4,'Z')@Matrix.Scale(scale,4)@Matrix.Translation((-(lo.x+hi.x)/2,-(lo.y+hi.y)/2,-lo.z))
    for obj in added:
        if obj.parent is None:obj.matrix_world=transform@obj.matrix_world
        for oldcol in list(obj.users_collection):oldcol.objects.unlink(obj)
        col.objects.link(obj);obj['level']=col['level'];obj['part']='furniture';obj['room_id']=room_id;obj['asset_source']='https://polyhaven.com/a/'+asset_id
        if soft and obj.type=='MESH':
            for slot in obj.material_slots:
                if 'pillow' not in slot.material.name:continue
                material=slot.material.copy();slot.material=material;n=material.node_tree.nodes;links=material.node_tree.links;shader=n.get('Principled BSDF')
                for socket in ['Base Color','Roughness','Metallic']:
                    for link in list(shader.inputs[socket].links):links.remove(link)
                shader.inputs['Base Color'].default_value=(.67,.61,.50,1);shader.inputs['Roughness'].default_value=.82;shader.inputs['Metallic'].default_value=0;shader.inputs['Sheen Weight'].default_value=.25
    return added

col=cols['u','furniture']
place_asset('modern_arm_chair_01',(1.1,2.58),3.54,.84,.86,'U1',soft=True)
col=cols['g','furniture']
for obj in list(col.objects):
    if obj.name.startswith('Reading chair'):bpy.data.objects.remove(obj,do_unlink=True)
place_asset('modern_arm_chair_01',(7.45,11.9),.04,.78,.78,'G7',angle=math.pi,soft=True)
place_asset('wooden_bowl_01',(9.7,7.60),.955,.29,.29,'G2')
place_asset('vintage_electric_kettle',(12.45,5.64),.925,.28,.27,'G3')

# A concealed pantry leaf aligns with the neighbouring cabinet fronts.
paint=bpy.data.materials['K01 warm ivory cabinetry']
pb('Kitchen fridge cabinet infill',[10.958,7.849,.06,.177],.04,3.17,paint,.002)
pantry_door=bpy.data.objects['Kitchen → pantry hinge'];pantry_door.location.x=10.99
for obj in pantry_door.children:
    if obj.type=='MESH' and 'lever' not in obj.name:obj.data.materials[0]=paint
for yy in [6.4,7.272]:pb('Concealed pantry cabinet reveal',[10.99,yy,.44,.028],.04,2.35,paint,.002)
pb('Concealed pantry lintel',[10.96,6.4,.47,.9],2.22,2.35,paint,.003)

# Drawer fronts follow the underside of the lower stair and face the hall.
for i in range(5):
    y0=11.68+i*.48;y1=y0+.466
    def underside(yy):
        if yy>=13.45:return 1.60
        step=math.floor((yy-11.15)/.2875+1e-6)
        return min(.04+step*3.5/18,.04+3.5/18+(yy-11.15)/2.3*(1.75-3.5/18)-.28)-.025
    ys=sorted({y0,y1,*[11.15+j*.2875+delta for j in range(9) for delta in [-.001,.001] if y0<11.15+j*.2875+delta<y1]})
    profile=[(y0,.055),(y1,.055)]+[(yy,underside(yy)) for yy in reversed(ys)]
    count=len(profile);vs=[(xx,-yy,zz) for xx in [9.68,10.59] for yy,zz in profile]
    faces=[tuple(reversed(range(count))),tuple(range(count,2*count))]+[(j,(j+1)%count,(j+1)%count+count,j+count) for j in range(count)]
    mesh('Lower stair fitted storage body',vs,faces,wood,.003)
    front=mesh('Lower stair fitted drawer front',[(10.61,-yy,zz) for yy,zz in profile],[tuple(range(count))],wood,.002)
    front.modifiers.new('Timber drawer thickness','SOLIDIFY').thickness=.018
    tube('Lower stair recessed pull',[(10.63,-(y0+y1)/2-.055,min(underside(y0)-.055,.85)),(10.63,-(y0+y1)/2+.055,min(underside(y0)-.055,.85))],.005,black)

ceramic=mat('Coastal | glazed oatmeal stoneware',(.73,.69,.60),.24,noise=.02,scale=150)
coffee=mat('Coastal | coffee',(.018,.008,.003),.19)
steel=mat('Coastal | brushed stainless steel',(.54,.56,.57),.30,.95)

def turned(name,x,y,z,profile,material):
    count=48;vs=[(x+r*math.cos(i*math.tau/count),-y+r*math.sin(i*math.tau/count),z+h) for r,h in profile for i in range(count)]
    fs=[]
    for j in range(len(profile)-1):
        for i in range(count):k=j*count+i;n=j*count+(i+1)%count;fs.append((k,n,n+count,k+count))
    obj=mesh(name,vs,fs,material)
    for face in obj.data.polygons:face.use_smooth=True
    return obj

def mug(x,y,z):
    turned('Everyday stoneware mug',x,y,z,[(0,0),(.035,0),(.043,.012),(.045,.092),(.041,.098),(.037,.09),(.034,.012),(0,.012)],ceramic)
    tube('Mug handle',[(x+.04+.028*math.sin(t),-y,z+.05+.031*math.cos(t)) for t in [i*math.pi/20 for i in range(21)]],.006,ceramic)
    cyl('Coffee in mug',(x,-y,z+.074),.037,.002,coffee)

plate_profile=[(0,0),(.065,0),(.12,.008),(.14,.022),(.14,.026),(.12,.015),(.06,.009),(0,.009)]
for x,y in [(2.25,6.94),(3.30,6.94),(2.25,7.46),(3.30,7.46)]:
    turned('Everyday dinner plate',x,y,.821,plate_profile,ceramic)
    turned('Water glass',x+.22,y,.821,[(0,0),(.034,0),(.035,.11),(.032,.114),(.029,.108),(.028,.009),(0,.009)],glass)
    pb('Folded linen napkin',[x-.32,y-.10,.14,.20],.821,.832,linen,.015)
    tube('Table spoon stem',[(x+.17,-y+.07,.837),(x+.17,-y-.055,.835)],.003,steel)
    ellipsoid('Table spoon bowl',(x+.17,-y-.073,.836),(.012,.023,.002),steel)
mug(4.12,7.36,.821)
for i in range(4):turned('Pantry stacked plate',12.92,8.53,.92+i*.017,plate_profile,ceramic)
mug(12.88,7.65,.92)
for i in range(3):
    ellipsoid('Bowl citrus fruit',(9.65+i*.045,-7.60,1.01),(.042,.042,.040),mat('Coastal | citrus '+str(i),(.48+i*.04,.23+i*.02,.035),.52,noise=.08,scale=95))

# A compact espresso station uses the proportions of a small domestic machine.
start_objects=set(col.objects)
box('Espresso machine body',(0,0,.185),(.24,.28,.34),steel,.018)
box('Espresso rear water tank',(0,.15,.185),(.21,.05,.33),black,.012)
box('Espresso blue front',(0,-.145,.21),(.215,.012,.25),bluepaint,.014)
box('Espresso drip tray',(0,-.185,.028),(.23,.17,.024),steel,.008)
for i in range(9):box('Espresso drip grille',(-.092+i*.023,-.19,.043),(.009,.135,.005),black,.002)
cyl('Espresso group head',(0,-.16,.205),.036,.035,steel)
tube('Espresso portafilter',[(0,-.16,.19),(0,-.25,.19),(0,-.31,.175)],.011,wood)
tube('Espresso steam wand',[(.09,-.16,.25),(.135,-.20,.20),(.135,-.23,.095)],.005,steel)
for xx in [-.07,-.023,.023,.07]:
    obj=cyl('Espresso control button',(0,0,0),.01,.006,steel);obj.rotation_euler.x=math.pi/2;obj.location=(xx,-.155,.295)
for yy in [-.065,.065]:tube('Espresso cup rail',[(-.10,yy,.37),(.10,yy,.37)],.004,steel)
bpy.context.view_layer.update()
transform=Matrix.Translation((13.035,-8.03,.92))@Matrix.Rotation(-math.pi/2,4,'Z')
for obj in set(col.objects)-start_objects:obj.matrix_world=transform@obj.matrix_world;obj['room_id']='G3'

col=cols['u','furniture']
mug(1.79,2.77,4.065)
for i in range(2):pb('Bedside reading book',[4.58,.78,.18,.115],4.092+i*.023,4.114+i*.023,[blue,ivory][i])
col=cols['g','furniture']
for i in range(3):pb('Hall daily post',[7.83,10.61,.21,.12],.821+i*.002,.823+i*.002,linen)

# Fabric weave and restrained roughness give surfaces different light responses.
for material in [fabric,linen,blue]:
    nodes=material.node_tree.nodes;links=material.node_tree.links;shader=nodes['Principled BSDF'];shader.inputs['Sheen Weight'].default_value=.28
    coord=nodes.new('ShaderNodeTexCoord');mapping=nodes.new('ShaderNodeVectorMath');mapping.operation='SCALE';mapping.inputs[3].default_value=2.5;links.new(coord.outputs['Object'],mapping.inputs[0])
    texture=nodes.new('ShaderNodeTexImage');texture.image=bpy.data.images.load(str(ROOT/'assets/living-study/terlenka_rough.jpg'),check_existing=True);texture.image.colorspace_settings.name='Non-Color';texture.projection='BOX';texture.projection_blend=.25;links.new(mapping.outputs[0],texture.inputs['Vector'])
    bump=nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.16;bump.inputs['Distance'].default_value=.0006;links.new(texture.outputs['Color'],bump.inputs['Height']);links.new(bump.outputs['Normal'],shader.inputs['Normal'])
for obj in scene.objects:
    if obj.type=='LIGHT' and any(s in obj.name for s in ['bulb','Pendant warm pool','picture light','Bedside glow']):obj.data.energy*=.45;obj.data.color=(1,.79,.57)
col=sitecol
sand=mat('Coastal | beach sand',(.49,.40,.27),.94,noise=.07,scale=110)
surface('Sloping beach beyond the dunes',rect(-200,-65,400,25),lambda x,y:-.28-.02*(-y-40),sand)
for i in range(4):
    y=-57.5-i*1.8
    tube('Soft shore wash',[(x,-y-.35*math.sin(x*.05+i),-.62) for x in range(-180,181,3)],.026,white)
for x,y in [(-8,-34),(22,-37),(33,-35)]:
    ellipsoid('Coastal dune beyond plot',(x,-y,-.42),(7,4.5,.90),sand)
    grass_patch('Dune marram grass',[(x+rng.uniform(-4,4),y+rng.uniform(-2,2)) for _ in range(65)],straw,.48)

sea_shader=sea.node_tree.nodes['Principled BSDF'];sea_shader.inputs['IOR'].default_value=1.333
sea_shader.inputs['Roughness'].default_value=.11
sea_nodes=sea.node_tree.nodes;sea_links=sea.node_tree.links
wave=sea_nodes.new('ShaderNodeTexWave');wave.wave_type='BANDS';wave.bands_direction='Y';wave.inputs['Scale'].default_value=.65;wave.inputs['Distortion'].default_value=5;wave.inputs['Detail Scale'].default_value=.4
coord=sea_nodes.new('ShaderNodeTexCoord');sea_links.new(coord.outputs['Object'],wave.inputs['Vector'])
bump=sea_nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.24;bump.inputs['Distance'].default_value=.085;sea_links.new(wave.outputs['Color'],bump.inputs['Height']);sea_links.new(bump.outputs['Normal'],sea_shader.inputs['Normal'])
