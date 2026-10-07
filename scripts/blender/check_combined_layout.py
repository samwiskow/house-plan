from pathlib import Path
import json,math,hashlib
R=Path(__file__).resolve().parents[2];O=R/'output/blender/combined-room';report=json.loads((O/'validation.json').read_text());f=report['footprints'];obstacles=[]
for name,b in f.items():
 if name.startswith('Approved cane'):
  dx=dy=0
  if name[-2:] in ['07','08']:dx=.4 if sum(b[0])/2>3.1 else -.4
  else:dy=.4 if -sum(b[1])/2>7.2 else -.4
  obstacles.append((name,[b[0][0]+dx,b[0][1]+dx,-b[1][1]+dy,-b[1][0]+dy]))
for name in ['03 Corner sofa','04 Square footstool','05 Media cabinet proposal']:
 b=f[name];obstacles.append((name,[b[0][0],b[0][1],-b[1][1],-b[1][0]]))
obstacles += [('Table',[1.88,4.32,6.655,7.745]),('Hearth',[5.54,6.54,5.025,6.275])]
route=[(5.95,9.3),(5.95,7.6),(5.95,6.61),(4.8,6.61),(4.8,5.3),(5.2,5.3),(5.2,4.4)];minimum=100;nearest=None
for a,b in zip(route,route[1:]):
 steps=math.ceil(math.dist(a,b)/.02)
 for i in range(steps+1):
  x=a[0]+(b[0]-a[0])*i/steps;y=a[1]+(b[1]-a[1])*i/steps
  for name,(x0,x1,y0,y1) in obstacles:
   d=math.hypot(max(x0-x,0,x-x1),max(y0-y,0,y-y1))
   if d<minimum:minimum=d;nearest=name
assert minimum>=.3,(minimum,nearest)
assert hashlib.sha256((R/'output/blender/kitchen-study/kitchen-option-d.blend').read_bytes()).hexdigest()==report['source_sha256']
result={'route_plan_m':route,'radius_m':.3,'sample_interval_m':.02,'minimum_obstacle_gap_m':round(minimum,3),'closest':nearest,'scope':'400 mm chair pull-out boxes, sofa bounding box, table, ottoman, media cabinet and hearth. Doors closed; no person or appliance simulation. Ten millimetre margin at the tightest sampled point is not a generous route.'}
(O/'route-check.json').write_text(json.dumps(result,indent=2)+'\n');print('Source unchanged; nominal 600 mm route screened:',round(minimum,3),'m radial clearance. Detailed layout review still needed.')
