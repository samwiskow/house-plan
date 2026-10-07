from pathlib import Path
import json,math,hashlib
R=Path(__file__).resolve().parents[2];O=R/'output/design/kitchen-selections'
source=(R/'studies/l-house-booklet/plans.json').read_bytes();base=json.loads(source)['default'];old={r['id']:r for r in base['rooms'] if r['floor']=='g'}
def area(p):return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1])))/2
def box(x,y,w,h):return [[x,y],[x+w,y],[x+w,y+h],[x,y+h]]
proposal={'G2':[[6.85,5.35],[11.35,5.35],[11.35,8],[13.3,8],[13.3,9.3],[6.7,9.3],[6.7,6.7],[6.85,6.7]],'G3':box(11.5,5.35,1.8,2.5),'G4':[[13.45,5.35],[15.85,5.35],[15.85,10.65],[14.3,10.65],[14.3,9.3],[13.45,9.3]],'G10':[[14.3,10.8],[15.85,10.8],[15.85,14.45],[12.7,14.45],[12.7,11.45],[14.3,11.45]]}
furniture=[('Kitchen cabinets','G2',[6.85,5.35,4.3,.65]),('Island','G2',[7.525,7.2,2.4,1]),('Stool allowance','G2',[7.875,8.35,.45,.45]),('Stool allowance','G2',[8.925,8.35,.45,.45]),('Pantry counter','G3',[11.5,5.35,1.8,.6]),('Pantry shelves','G3',[11.5,7.5,1.8,.35]),('Washer','G4',[13.5,5.35,.65,.65]),('Dryer','G4',[14.2,5.35,.65,.65]),('Sink','G4',[14.9,5.35,.75,.65]),('Folding counter','G4',[15.25,6.4,.6,2.1]),('Tall cupboard','G4',[13.45,8.1,.6,1]),('Coats / shoes','G10',[13,11.45,1.5,.6]),('Boot bench','G10',[13.6,13.6,1.8,.45])]
doors=[('Kitchen → pantry',11.425,6.4,'v',.9),('Utility → pantry',13.375,6.325,'v',1.05),('Kitchen → utility',13.375,8.2,'v',.9),('Boot → utility',14.7,10.725,'h',.9)]
route=[[15.5,12.45],[15.15,12.45],[15.15,10.45],[14.65,8.9],[14.65,6.85],[12.4,6.85],[10.85,6.85]]
def inside(x,y,p):
 c=False
 for a,b in zip(p,p[1:]+p[:1]):
  if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:c=not c
 return c
for name,room,(x,y,w,h) in furniture:
 for dx,dy in [(1e-5,1e-5),(w-1e-5,1e-5),(w-1e-5,h-1e-5),(1e-5,h-1e-5)]:assert inside(x+dx,y+dy,proposal[room]),(name,'outside room')
for i,(a,pa) in enumerate(proposal.items()):
 for b,pb in list(proposal.items())[i+1:]:
  for ix in range(134,318):
   for iy in range(107,289):
    x=ix*.05+.025;y=iy*.05+.025
    assert not(inside(x,y,pa) and inside(x,y,pb)),('room overlap',a,b)
passages=[box(x,y-.12,w,.24) if axis=='h' else box(x-.12,y,.24,w) for _,x,y,axis,w in doors]
# A nominal 600 mm passage check is a screening test, not an access assessment.
for a,b in zip(route,route[1:]):
 for i in range(math.ceil(math.dist(a,b)/.04)+1):
  t=min(1,i*.04/math.dist(a,b));cx=a[0]+t*(b[0]-a[0]);cy=a[1]+t*(b[1]-a[1])
  for angle in [j*math.tau/24 for j in range(24)]:
   x=cx+.3*math.cos(angle);y=cy+.3*math.sin(angle)
   assert any(inside(x,y,p) for p in list(proposal.values())+passages),('route boundary',x,y)
   assert not any(rx+1e-5<x<rx+w-1e-5 and ry+1e-5<y<ry+h-1e-5 for _,_,(rx,ry,w,h) in furniture),('route furniture',x,y)
areas={k:area(v) for k,v in proposal.items()}
record={'status':'Option D enclosed pantry approved for render study','source_sha256':hashlib.sha256(source).hexdigest(),'room_polygons':proposal,'areas_m2':areas,'furniture':furniture,'doors':doors,'shopping_route':route,'screening':'Furniture containment; sampled room overlap; 600 mm nominal route envelope at 40 mm intervals, no door swing or occupied-use simulation.','hall_changed':False}
(O/'boot-room-option.json').write_text(json.dumps(record,indent=2))
def svg(proposed):
 parts=['<svg viewBox="6.1 4.7 10.5 10.5" role="img" aria-label="'+('Proposed' if proposed else 'Current')+' kitchen pantry utility and boot room plan"><rect x="6.1" y="4.7" width="10.5" height="10.5" fill="#fffdf7"/><path d="M6.1 5H16.2V14.8H6.1Z" fill="#526052"/>']
 def poly(p,fill):parts.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in p)+f'" fill="{fill}"/>')
 def rect(x,y,w,h,c,stroke='#6f7861'):
  parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" stroke="{stroke}" stroke-width=".025"/>')
 def line(x,y,X,Y,c,w=.05,extra=''):parts.append(f'<line x1="{x}" y1="{y}" x2="{X}" y2="{Y}" stroke="{c}" stroke-width="{w}" {extra}/>')
 def text(x,y,t,size=.23):parts.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="middle" fill="#293f32" font-family="system-ui">{t}</text>')
 colors={'G2':'#e9dfc5','G3':'#dfe8d1','G4':'#d0dfd7','G10':'#e2e7d9','G8':'#eeeae0'}
 rooms={k:v['p'] for k,v in old.items() if k!='L'}
 if proposed:rooms.update(proposal)
 for k,p in rooms.items():poly(p,colors.get(k,'#f5f2e9'))
 if not proposed:line(12.625,5.35,12.625,6.4,'#748266',.15)
 gaps=[(d['id'],d['x'],d['y'],d['axis'],d['w']) for d in base['doors'] if d['floor']=='g' and d['x']<16.2]
 if proposed:gaps=[d for d in gaps if d[0] not in ['Kitchen to pantry','Kitchen to laundry','Laundry to boot']]+doors
 for _,x,y,axis,w in gaps:line(x,y,x+(w if axis=='h' else 0),y+(w if axis=='v' else 0),'#fffdf7',.20)
 for f,x,y,axis,w in base['openings']:
  if f=='g' and x<16.2:line(x,y,x+(w if axis=='h' else 0),y+(w if axis=='v' else 0),'#fffdf7',.32)
 for x,y,X,Y in [(7.1,5.175,10.3,5.175),(16.025,6.3,16.025,8.3),(16.025,13.25,16.025,14.2)]:line(x,y,X,Y,'#b5dade',.12)
 fs=furniture if proposed else [(f['name'],f['roomId'],f['r']) for f in base['furniture'] if f['floor']=='g' and f['roomId'] in ['G2','G3','G10']]
 for name,room,r in fs:
  rect(*r,'#78563f' if name=='Island' else '#b5bda8')
  if name in ['Washer','Dryer','Sink','Laundry sink']:text(r[0]+r[2]/2,r[1]+r[3]/2+.06,{'Washer':'W','Dryer':'D','Sink':'S','Laundry sink':'S'}[name],.20)
 labels=[(8.7,6.75,'Kitchen'),(11.75 if not proposed else 12.4,6.30,'Pantry'),(14.35 if not proposed else 14.45,7.85,'Utility'),(14.5,13.20,'Boot room'),(13.4,10.4,'WC'),(9.3,12.85,'Stairs'),(11.75,13.8,'Entry'),(8.8,10.2,'Hall unchanged')]
 for x,y,t in labels:text(x,y,t)
 if proposed:
  line(14.3,9.375,15.85,9.375,'#b36b4b',.06,'stroke-dasharray=".1 .08"');text(15.03,10.04,'Reallocated',.18);text(15.03,10.30,'2.09 m²',.20)
  parts.append('<line class="pantry-door" x1="13.375" y1="6.325" x2="13.375" y2="7.375" stroke="#a47a48" stroke-width=".07"/>')
  pts=route
  text(12.4,7.24,'1.80 × 2.50',.21);text(14.5,14.30,'Main boot area: 3.15 × 3.00',.19)
  text(9.1,9.10,'Stool space still needs review',.18)
  text(8.9,4.93,'Kitchen core width: 4.50 m',.21)
 else:
  pts=[[15.55,12.45],[15.15,12.45],[15.15,8.9],[14.45,7.0],[11.9,6.95]]
  text(8.9,4.93,'Kitchen core width: 3.90 m',.21);text(11.7,7.23,'1.65 × 2.10 zone',.18)
 parts.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+'" fill="none" stroke="#38798c" stroke-width=".055" stroke-dasharray=".12 .07"/>')
 text(16.35,12.55,'Link',.19);line(6.7,14.98,8.7,14.98,'#344735',.04)
 for i in range(3):line(6.7+i,14.90,6.7+i,15.05,'#344735',.025)
 text(7.7,15.18,'2 metres',.17)
 parts.append('</svg>');return ''.join(parts)
rows=[('Kitchen','18.86','20.70','+1.85'),('Pantry zone / enclosed room','3.47','4.50','+1.03'),('Utility, enclosed comparison','12.44','11.57','−0.87'),('Boot room','12.55','10.46','−2.09'),('Hall + entrance','18.84','18.84','No change')]
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>L-house · Boot room reallocation</title><style>*{box-sizing:border-box}body{margin:0;background:#f3f0e8;color:#293f32;font:16px/1.55 system-ui}header,main,footer{max-width:1320px;margin:auto;padding:30px}header{padding-top:44px}h1{font:normal clamp(34px,4.5vw,52px)/1.12 Georgia,serif;margin:12px 0 22px}h2{font:normal 29px Georgia,serif;margin:5px 0 16px}h3{font-size:18px;margin:6px 0 12px}p{max-width:920px}.eyebrow{font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#6a755d}a{color:inherit;text-underline-offset:3px}.summary{padding:22px;background:#284836;color:white}.grid{display:grid;grid-template-columns:1fr 1fr;gap:26px}.card{padding:22px;background:#fffdf7;border:1px solid #d2d5c7;min-width:0}svg{width:100%;height:auto;display:block}.note{font-size:13px;color:#62705d}.caption{font-size:13px;margin:10px 0}.controls{display:flex;align-items:center;flex-wrap:wrap;gap:12px;margin:18px 0}select{padding:10px;font:inherit;color:inherit;background:#fffdf7;border:1px solid #a8b29d}.section{margin-top:32px;padding-top:26px;border-top:1px solid #c8cebe}table{border-collapse:collapse;width:100%;font-size:14px}th,td{padding:12px 9px;text-align:left;border-bottom:1px solid #ccd1c2}.overflow{overflow-x:auto}.callout{padding:18px;background:#ede1c9;border-left:3px solid #a87943}li{margin:9px 0}.pantry-door{display:none}body.closed .pantry-door{display:block}@media(max-width:800px){.grid{grid-template-columns:1fr}header,main,footer{padding:20px}.card{padding:14px}table{font-size:12px}td,th{padding:8px 5px}}@media print{.controls{display:none}.grid{grid-template-columns:1fr 1fr}.section{break-inside:avoid}header,main,footer{padding:15px}}</style></head><body class="closed"><header><div class="eyebrow">L-house / Option D / 7 October 2026</div><h1>Borrow from the boot room.<br>Keep the useful parts.</h1><p>A measured layout test that enlarges both the kitchen and pantry, while retaining the utility, boot-room storage and separate hall route.</p><div class="summary"><strong>Test a 2.09 m² reallocation from the narrow upper boot-room section.</strong><p>The main 3.15 × 3.00 m boot-room area stays. Shift the pantry right, extend the utility down and give the kitchen a wider core.</p></div><p><a href="zoning.html">← Hall and daylight comparisons</a> · <a href="index.html">Kitchen selections</a> · <a href="renders.html">Kitchen renders</a></p></header><main><div class="controls"><label for="pantryState">Pantry connection:</label><select id="pantryState"><option value="open">Open utility passage</option><option value="closed" selected>Enclosed with connecting door</option></select></div><div class="grid"><div class="card"><div class="eyebrow">Current arrangement</div><h2>Longer boot-room approach</h2>CURRENT<p class="caption">Blue dashes show the shopping route. Current pantry zone has the short divider and open connection.</p></div><div class="card"><div class="eyebrow">Option D — selected for renders</div><h2>More space where it is used</h2>PROPOSED<p class="caption">Rust dashes mark the old utility/boot boundary. The cupboard-style kitchen pantry door and the utility connection both remain.</p></div></div><p class="note">Both drawings use the same scale. Garden side at top; link to garage at right. Kitchen dividers and the living-room boundary stay in place. These are layout tests, not construction drawings.</p><div class="section overflow"><h2>Where the space goes</h2><table><thead><tr><th>Space</th><th>Current m²</th><th>Option D m²</th><th>Change m²</th></tr></thead><tbody>ROWS</tbody></table><p class="note">Pantry and utility baseline areas use the preserved enclosed option for a like-for-like comparison. The current open shared room is 16.22 m², including the open connection. New partitions also change the net floor area slightly.</p></div><div class="grid section"><div class="card"><h3>Pantry: 1.80 × 2.50 m</h3><ul><li>1.80 m landing counter, 600 mm deep.</li><li>Opposite shelves, 350 mm deep.</li><li>1.55 m between these two storage runs.</li><li>900 mm kitchen opening and 1.05 m utility connection.</li></ul><p id="stateText">The enclosed pantry retains both the kitchen door and a connecting utility door.</p></div><div class="card"><h3>Utility: 11.57 m²</h3><ul><li>Side-by-side washer, dryer and sink along the garden-side wall.</li><li>2.10 m folding counter on the outer wall.</li><li>A tall cupboard for cleaning equipment.</li><li>Space above the counter for a wall-mounted drying rack; its open position needs testing.</li></ul><p>The principal utility rectangle is 2.40 × 3.95 m, with a 1.55 m-wide approach from the boot room.</p></div><div class="card"><h3>Boot room: 10.46 m²</h3><ul><li>Keep the 1.80 m bench and shoe space.</li><li>Allow a 1.50 m-long, 600 mm-deep coat cupboard.</li><li>Keep the direct route between garage link and hall.</li><li>Move the utility door into the shortened upper approach.</li></ul><p>The main rectangular area remains 3.15 × 3.00 m. The reduction comes from its narrow extension.</p></div><div class="card"><h3>Kitchen: 20.70 m²</h3><p>The main width increases from 3.90 m to 4.50 m. With the source island position, the side gap to the pantry wall increases from about 0.83 m to 1.43 m.</p><p class="callout">This does not fix the 0.50 m gap behind the current stool footprints. Repositioning the island or combining this with a hall adjustment is a separate test using the new curved timber stool reference.</p></div></div><div class="section"><h2>My recommendation</h2><p>Selected for the next kitchen render study. It gives a more useful pantry and a wider kitchen while retaining a separate hall. Check the boot-room storage against what you actually keep there before reducing it further.</p><p>The utility window stays. The pantry can borrow light through its open utility connection; a glazed upper panel could retain some of that light if you choose the enclosed version. The kitchen keeps its own garden-facing window.</p><p class="note">Furniture fits within the proposed room outlines. A sampled 600 mm-wide shopping route clears the drawn fixed furniture. This is an initial screening check; door swings, open appliances, occupied seats, structural walls and detailed access requirements still need review.</p></div></main><footer><p>The measured source and first-floor layout are unchanged. A separate Blender study uses this selected layout. <a href="boot-room-option.json">Dimensions and screening record</a>.</p></footer><script>document.querySelector('select').addEventListener('change',e=>{document.body.classList.toggle('closed',e.target.value==='closed');document.querySelector('#stateText').textContent=e.target.value==='closed'?'Add a closable door in the utility opening. Shopping still goes directly from boot room to utility to pantry; the kitchen door remains.':'The utility connection stays open. Use the dividing returns to define the pantry area.'});</script></body></html>'''.replace('CURRENT',svg(False)).replace('PROPOSED',svg(True)).replace('ROWS',''.join('<tr>'+''.join(f'<td>{v}</td>' for v in row)+'</tr>' for row in rows))
(O/'boot-room.html').write_text(page)
print('Areas:',areas);print('Fixture containment, sampled non-overlap and nominal 600 mm shopping route passed.')
