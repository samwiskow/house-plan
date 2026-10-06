# L-house Blender study 01

An editable Blender 5.2 scene built from the corrected L01 measured browser model. Room layouts, wall openings and furniture footprints are retained. This is a design study, not a construction model.

## Files

- `output/blender/l-house/l-house.blend`: native scene with packed textures, named objects, floor collections, alternate layouts, six cameras and Cycles lighting.
- `output/blender/l-house/l-house.glb`: static default layout for browser review.
- `output/blender/l-house/{arrival,garden,living,kitchen,parents,office}.png`: Cycles images.
- `output/blender/l-house/build-report.json`: measured-source hash and build settings.
- `viewer-blender/`: local GLB viewer with camera presets and floor cutaways.

## Build

From the repository root, run an HTTP server on port 4193. Install Playwright in your Node environment and set `CHROME_PATH` if Chrome is not at its standard macOS path.

```sh
python3 -m http.server 4193 --bind 127.0.0.1
node scripts/blender/export_scene.cjs
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python-exit-code 1 --python scripts/blender/build_scene.py -- --source tmp/blender-source/scene.json --output output/blender/l-house --render arrival garden living kitchen parents office --samples 64 --width 1500
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python-exit-code 1 --python scripts/blender/export_lighting.py -- .
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python-exit-code 1 --python scripts/blender/check_scene.py -- .
```

The exporter disables browser mesh batching only for its own request. It captures the default layout, enclosed-pantry alternative and guest-office alternative. Generated intermediate data stays under ignored `tmp/blender-source/`. `BASE_URL` can select another server.

Open `http://127.0.0.1:4193/viewer-blender/` to inspect the GLB. The preview batches static geometry by material and renders only when the view changes. It uses the existing Three.js r180 runtime. `GLTFLoader.js`, `HDRLoader.js` and `BufferGeometryUtils.js` come from the official r180 tag; their MIT license is in `viewer/vendor/LICENSE`.

Check the browser with `node scripts/blender/check_preview.cjs`. This checks all eight views, floor visibility, phone widths, load errors and idle rendering.

## Edit in Blender

Scene units are metres. Blender Z is vertical; plan Y runs along negative Blender Y.

- Floors are collections under **Structure**. Roof, ceilings and site have separate collections.
- For the enclosed pantry, hide **House - ground - open pantry** and enable **ALT - enclosed pantry ground floor** for both viewport and render.
- For the guest office, hide **Garage - office - work** and enable **ALT - office guest bed** for both viewport and render.
- Hinged-door parent objects have an **Open** property: 0 is closed, 1 is open. Other doors retain the source pose and separate editable parts.
- Choose Arrival, Garden, Living, Kitchen, Parents or Office as the render camera. Interior stills use +0.3 exposure; exterior stills use +0.4.

## Presentation changes and limits

The study adds small edge bevels, ivory room-facing wall surfaces, daylight and soft ceiling lights. Gable cladding meets the existing roof slopes without overlapping the wall cap. Paving layers have offsets under 3 mm to remove coplanar overlaps. The surrounding ground is extended to avoid a visible edge behind the plot. None of these changes moves a room or furniture footprint.

The default is the open pantry with a short divider and the work office. Both alternatives remain editable in the Blender file. The GLB contains only the default layout; the browser preview has no walking, door animation or layout switching. Use the existing L-house walkthrough for those controls.

The browser uses an HDR sky exported from this Blender scene, AgX colour processing, matching camera lenses and exposure, and shadow-casting warm room lights. Glass admits sunlight. Interior views reduce unoccluded sky fill and add warm fill to approximate reflected light. Floor cutaways hide room lights. Cycles indirect illumination is not baked into the GLB, so this real-time preview still differs from the path-traced stills. Furniture, planting, roof form and finishes remain schematic. Windows, roof construction and the 40 × 65 m plot are design assumptions.
