from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
root=Path(__file__).resolve().parents[2]/'output/blender/furniture-study'
font='/System/Library/Fonts/Supplemental/Arial.ttf'
regular=ImageFont.truetype(font,22); small=ImageFont.truetype(font,18); title=ImageFont.truetype(font,40); label=ImageFont.truetype(font,26)
sheet=Image.new('RGB',(1500,2120),'#f4f1eb');draw=ImageDraw.Draw(sheet)
draw.text((50,35),'L-house | Furniture study',fill='#28362d',font=title)
draw.text((50,94),'Separate Blender previews • 7 October 2026 • No paid assets',fill='#596056',font=regular)
cards=[('table','01  Monastery table','Free model adapted • thick plank top'),('chair','02  Cane dining chair','Custom • fixed upholstery in the oak seat frame'),('sofa','03  Corner sofa','Existing custom model • not the Frankof asset'),('footstool','04  Square footstool','Custom • plain oatmeal • 1.25 m square'),('media-cabinet','05  Media cabinet','Custom • approved furniture direction')]
for i,(slug,name,caption) in enumerate(cards):
    x=50+(i%2)*725;y=155+(i//2)*620
    image=Image.open(root/(slug+'.png')).convert('RGB');image.thumbnail((675,507))
    sheet.paste(image,(x,y));draw.text((x,y+522),name,fill='#28362d',font=label);draw.text((x,y+563),caption,fill='#596056',font=small)
x,y=775,1450
for text in ['Review the shape and finish first.','','The house scene is unchanged.','Furniture direction approved.','','The table uses a free BlenderKit base.','The other pieces are custom studies.','','These are real Blender renders.','They are not exact retail product models.']:
    draw.text((x,y),text,fill='#596056',font=regular);y+=38
sheet.save(root/'review-sheet.jpg',quality=93)
links=''.join(f'<figure><a href="{slug}.png"><img src="{slug}.png" alt="{name}"></a><figcaption><b>{name}</b><br>{caption}</figcaption></figure>' for slug,name,caption in cards)
(root/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>L-house furniture study</title><style>body{max-width:1100px;margin:40px auto;padding:0 24px;background:#f4f1eb;color:#28362d;font:18px/1.5 system-ui}h1{font-size:32px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:36px}figure{margin:0}img{width:100%;display:block}figcaption{padding-top:12px}p{max-width:760px}a{color:inherit}</style><h1>L-house furniture study</h1><p>Separate Blender previews. No paid assets. Select any image to see the full size.</p><p>The table uses an adapted free model. The other pieces are custom studies. The sofa is the existing custom model, not a downloaded Frankof model. The furniture direction is approved. The house scene is unchanged.</p><main>'''+links+'''</main><p><a href="review-sheet.jpg">Comparison sheet</a> · <a href="report.json">Dimensions and source record</a></p></html>''')
report=json.loads((root/'report.json').read_text())
assert report['cost']==0 and len(report['renders'])==5
for slug,_,_ in cards:
    image=Image.open(root/(slug+'.png'));assert image.size==(1440,1080);image.verify()
assert 2.43<report['dimensions_m']['table'][0]<2.45
assert abs(report['dimensions_m']['footstool'][0]-report['dimensions_m']['footstool'][1])<.001
assert .9<report['dimensions_m']['chair'][2]<1.05
print('Five valid 1440×1080 PNGs; table dimensions, square footstool, chair height and zero cost checked.')
