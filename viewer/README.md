# Fresh courtyard-house model

This scene was built from scratch for Design book 01. It does not reuse the
previous viewer. Room geometry comes from the current measured proposal;
roof forms and ceilings carry the 06B / 07B study heights. Forms and finishes
are illustrative. The low roof envelopes do not encode construction falls.

## Open

From this worktree root:

```sh
python3 -m http.server 4186 --bind 127.0.0.1
```

Open <http://127.0.0.1:4186/viewer/>. Serve the worktree root so the design-book
link works. Three.js 0.180.0 and OrbitControls are vendored with their MIT
license; the scene makes no remote requests.

Choose a view, drag to orbit and scroll to zoom. Roof off reveals the furnished
layout. Office offers Professional, Personal and Night states. Daylight toggles
to Evening. Walk uses drag to look and WASD / arrows to move; Escape stops.
Click a nearby door to open / close it. Walking blocks walls and closed door
openings, but furniture is not a collision obstacle. Use the measured plan
checks, not walking alone, to assess clearances.

## Rebuild

Use a Python environment with reportlab and Pillow; the Codex bundled Python
also includes pdfplumber for verification. PDF fonts use macOS Arial / Georgia.
Run in this order from the worktree root, with the preview server running for
the capture step:

```sh
python3 house_design_model.py
python3 viewer/export_model.py
node scripts/capture_model.cjs
python3 build_design_book.py
python3 scripts/check_design_book.py
node scripts/check_viewer.cjs
```

`capture_model.cjs` requires Playwright resolvable through Node (for the bundled
runtime set NODE_PATH to its node_modules directory) and uses the installed
Google Chrome binary. Captures are stored in `output/design/book-views/`.

`model.json` is the common geometric input to this scene and the PDF. The book
manifest records the model and image hashes. Source scripts and generated
files are kept together so future editions can be regenerated consistently.

## Edition 02 and publishing

The office now has a continuous L-shaped worktop. Outdoor seats follow their
recorded facing directions. Three main-space and two family-hall rooflights
join the library opening, with matching roof openings, ceiling openings and
lightwells. These remain a concept proposal with shading and product selection
open.

`python3 scripts/build_pages.py` stages the current scene and PDF in `tmp/pages`.
GitHub Actions verifies geometry, the book manifest and browser behaviour before
publishing that folder on a push to `main`. Pull requests run the same checks.
The browser check supports `BASE_URL` for checking the deployed project path
and `CHROME_PATH` to override the local browser. On Linux it uses Playwright's
installed Chromium.
