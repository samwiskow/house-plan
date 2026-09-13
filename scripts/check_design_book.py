"""Check the delivered book and scene against the retained measured proposal."""
import hashlib
import json
import sys
from pathlib import Path

import pdfplumber

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from house_design_model import load_current_model

model=json.loads((ROOT/'viewer/model.json').read_text())
source,snapshot=load_current_model()
assert len(model['rooms'])==26
assert {r['id']:r['polygon'] for r in model['rooms']}=={r.id:r.poly for r in source.rooms}
assert model['outline']==source.OUTLINE
assert model['metadata']['giaM2']==round(source.polygon_area(source.INNER),2)==332.96
assert model['metadata']['externalFootprintM2']==373.31
for mode in ('Professional','Personal','Night'):
    current,_=load_current_model(mode)
    assert not current.verify(),mode
    assert [f['rect'] for f in model['officeStates'][mode]]==[f['rect'] for f in current.furniture if f['room']=='O']

for d in source.doors:
    x=d.x if d.vertical else d.x+d.width/2
    y=d.y+d.width/2 if d.vertical else d.y
    blockers=[wall for wall in model['walls'] if wall['bottom']<1.5<wall['top'] and wall['rect'][0]<x<wall['rect'][0]+wall['rect'][2] and wall['rect'][1]<y<wall['rect'][1]+wall['rect'][3]]
    assert not blockers,('door blocked in scene',d.id)

for ix in range(272):
    for iy in range(184):
        point=((ix+.37)/10,(iy+.41)/10)
        inside=source.inside(point,source.OUTLINE)
        surfaces=[r for r in model['roofSurfaces'] if source.inside(point,[[v[0],v[1]] for v in r['vertices']])]
        assert bool(surfaces)==inside,('roof coverage',point)
        assert len(surfaces)<=1,('overlapping roofs',point)

manifest=json.loads((ROOT/'output/design/design-book-manifest.json').read_text())
assert hashlib.sha256((ROOT/'viewer/model.json').read_bytes()).hexdigest()==manifest['model_sha256']
for name,digest in manifest['views'].items():
    assert hashlib.sha256((ROOT/'output/design/book-views'/name).read_bytes()).hexdigest()==digest
with pdfplumber.open(ROOT/'output/pdf/house-design-book.pdf') as pdf:
    assert len(pdf.pages)==16
    content='\n'.join(page.extract_text() or '' for page in pdf.pages)
    for phrase in ['332.96','373.31','315.52','underfloor heating is confirmed','two basins','1:100','not selected']:
        assert phrase.lower() in content.lower(),phrase
    for index,page in enumerate(pdf.pages):
        assert abs(page.width-420*72/25.4)<.01 and abs(page.height-297*72/25.4)<.01
        words=page.extract_words()
        assert words
        for word in words:
            assert 0<=word['x0']<word['x1']<=page.width+.2,(index,word)
            assert 0<=word['top']<word['bottom']<=page.height+.2,(index,word)
print('Verified: 16 A3 pages; source geometry and areas; 168 current route checks; all door centres clear; roof coverage; model and image hashes; PDF text bounds')
