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
shutil.copy2(ROOT / 'index.html', OUT / 'index.html')
shutil.copytree(ROOT / 'site', OUT / 'site')
(OUT / 'viewer-l-house').mkdir()
for name in ['index.html', 'styles.css', 'main.js', 'model.json', 'batch_static.js']:
    shutil.copy2(ROOT / 'viewer-l-house' / name, OUT / 'viewer-l-house' / name)
shutil.copy2(ROOT / 'output/pdf/l-house-design-booklet.pdf', OUT / 'output/pdf/l-house-design-booklet.pdf')
print(f'Staged {len(list(OUT.rglob("*.*")))} files in {OUT}')
