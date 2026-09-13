"""Stage the current public presentation for GitHub Pages."""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tmp/pages'
if OUT.exists():
    shutil.rmtree(OUT)
(OUT / 'viewer/vendor').mkdir(parents=True)
(OUT / 'output/pdf').mkdir(parents=True)
for name in ['index.html', 'styles.css', 'main.js', 'model.json']:
    shutil.copy2(ROOT / 'viewer' / name, OUT / 'viewer' / name)
for name in ['three.module.js', 'three.core.js', 'OrbitControls.js', 'LICENSE']:
    shutil.copy2(ROOT / 'viewer/vendor' / name, OUT / 'viewer/vendor' / name)
shutil.copy2(ROOT / 'output/pdf/house-design-book.pdf', OUT / 'output/pdf/house-design-book.pdf')
(OUT / 'index.html').write_text('''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The courtyard house</title><meta http-equiv="refresh" content="0;url=./viewer/"></head>
<body><p><a href="./viewer/">Explore the courtyard house</a></p>
<p><a href="./output/pdf/house-design-book.pdf">Read the house design book</a></p></body></html>
''')
print(f'Staged {len(list(OUT.rglob("*.*")))} files in {OUT}')
