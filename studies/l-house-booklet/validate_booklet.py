import runpy, json, math
from pathlib import Path
M=runpy.run_path('studies/l-house-booklet/build_booklet.py')
def inside(x,y,p):
 c=False
 for a,b in zip(p,p[1:]+p[:1]):
  if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:c=not c
 return c
pave=M['SITE']['forecourt']
garage=M['box'](25.05,45,6.5,3.85)
fail=[]
for phase in ['IN','REV','EXIT']:
 for j,pose in enumerate(M[phase]):
  body=M['car_polygon'](pose)
  for a,b in zip(body,body[1:]+body[:1]):
   for i in range(11):
    x=a[0]+(b[0]-a[0])*i/10;y=a[1]+(b[1]-a[1])*i/10
    if y>=65:continue
    if not inside(x,y,pave) and not inside(x,y,garage) and not (24.6<=x<=25.1 and 45.25<=y<=48.55):fail.append([phase,j,x,y])
assert not fail,fail[:8]
print('All vehicle body samples remain on the drive or within the garage.')
import pdfplumber
with pdfplumber.open('output/pdf/l-house-design-booklet.pdf') as pdf:
 assert len(pdf.pages)==9
 for i,p in enumerate(pdf.pages):
  assert abs(p.width-420*72/25.4)<.1 and abs(p.height-297*72/25.4)<.1
  bad=[ch for ch in p.chars if ch['x0']<10 or ch['x1']>p.width-10 or ch['top']<8 or ch['bottom']>p.height-8]
  assert not bad, (i+1,bad)
  print(i+1,'text bounds passed')
 assert 'ENCLOSED PANTRY' in pdf.pages[5].extract_text()
 assert '1.05 m' in pdf.pages[5].extract_text()
 assert '571.58' in pdf.pages[8].extract_text()

checks_path=Path('studies/l-house-booklet/checks.json')
checks=json.loads(checks_path.read_text())
checks['pdf_validation']={'pages':9,'page_size':'A3 landscape','text_bounds':'pass','required_option_labels':'pass','vehicle_paving_check':'pass'}
checks_path.write_text(json.dumps(checks,indent=2))
