import argparse, bpy, hashlib, json, sys, time
from pathlib import Path
from mathutils import Vector

parser=argparse.ArgumentParser()
parser.add_argument('--source',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--preview',action='store_true')
parser.add_argument('--start',type=int,default=1)
parser.add_argument('--end',type=int,default=600)
parser.add_argument('--samples',type=int,default=16)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
args.output.mkdir(parents=True,exist_ok=True)
source_hash=hashlib.sha256(args.source.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(args.source.resolve()))
scene=bpy.context.scene;scene.frame_set(1)
for obj in scene.objects:
 if obj.name.startswith('Folding divider hinge'):obj.animation_data_clear()
scene.camera=scene.camera.copy();scene.camera.data=scene.camera.data.copy();scene.collection.objects.link(scene.camera)
scene.camera.name='Room tour camera';scene.camera.animation_data_clear();scene.camera.data.dof.use_dof=False;scene.camera.data.clip_start=.05
shots=[
 {'name':'Kitchen','first':1,'last':180,'from':(10.62,-8.85,1.65),'to':(10.50,-8.45,1.65),'look_from':(8.4,-5.9,1.3),'look_to':(5.5,-6.5,1.3),'lens':23},
 {'name':'Dining','first':181,'last':390,'from':(5.90,-8.8,1.65),'to':(5.90,-7.45,1.65),'look_from':(3.1,-7.0,1.1),'look_to':(3.45,-4.2,1.35),'lens':23},
 {'name':'Living','first':391,'last':600,'from':(2.0,-.80,1.65),'to':(2.8,-.80,1.65),'look_from':(4.3,-5.5,1.1),'look_to':(4.3,-6.2,1.25),'lens':23},
]
scene.frame_start=1;scene.frame_end=600;scene.render.fps=30;scene.render.fps_base=1
scene.render.engine='CYCLES';scene.cycles.samples=args.samples;scene.cycles.use_denoising=True;scene.cycles.use_animated_seed=False
scene.render.use_persistent_data=True
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
for device in prefs.devices:device.use=device.type=='METAL'
scene.cycles.device='GPU';scene.render.resolution_x=960 if args.preview else 1920;scene.render.resolution_y=540 if args.preview else 1080;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='JPEG';scene.render.image_settings.color_mode='RGB';scene.render.image_settings.quality=97
scene.render.use_file_extension=True
frames_dir=args.output/('preview' if args.preview else 'frames');frames_dir.mkdir(exist_ok=True)
for shot in shots:
 for frame in range(shot['first'],shot['last']+1):
  t=(frame-shot['first'])/(shot['last']-shot['first']);t=t*t*(3-2*t)
  location=Vector(shot['from']).lerp(Vector(shot['to']),t);target=Vector(shot['look_from']).lerp(Vector(shot['look_to']),t)
  scene.camera.location=location;scene.camera.rotation_euler=(target-location).to_track_quat('-Z','Y').to_euler();scene.camera.data.lens=shot['lens']
  scene.camera.keyframe_insert(data_path='location',frame=frame);scene.camera.keyframe_insert(data_path='rotation_euler',frame=frame);scene.camera.data.keyframe_insert(data_path='lens',frame=frame)
 scene.timeline_markers.new(shot['name'],frame=shot['first'])
report={'source_sha256':source_hash,'fps':30,'width':scene.render.resolution_x,'height':scene.render.resolution_y,'frames':600,'duration_seconds':20,'samples':args.samples,'engine':'Cycles / Metal','shots':shots,'audio':'None','rendered':[]}
frames=[f for f in [1,90,180,181,285,390,391,495,600] if args.start<=f<=args.end] if args.preview else range(args.start,args.end+1)
started=time.monotonic()
for frame in frames:
 filename=frames_dir/f'{frame:04}.jpg'
 if filename.exists() and not args.preview:continue
 scene.frame_set(frame);scene.render.filepath=str(filename)
 render_start=time.monotonic();bpy.ops.render.render(write_still=True)
 report['rendered'].append({'frame':frame,'seconds':round(time.monotonic()-render_start,2)})
 (args.output/('preview-report.json' if args.preview else 'render-report.json')).write_text(json.dumps(report,indent=2))
 print('TOUR_FRAME',frame,'SECONDS',round(time.monotonic()-render_start,2),'TOTAL',round(time.monotonic()-started,2),flush=True)
if not args.preview:
 bpy.context.preferences.filepaths.save_version=0;scene.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(args.output/'room-tour.blend'),compress=True)
assert hashlib.sha256(args.source.read_bytes()).hexdigest()==source_hash
print('TOUR_RENDER_COMPLETE',flush=True)
