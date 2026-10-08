# L-house browser model

A furnished Three.js model of the reviewed L01 design booklet. This alternative
uses `studies/l-house-booklet/plans.json` and `site.json`. It does not replace the
courtyard model in `viewer/`.

## Open locally

Run from the worktree root:

```sh
python3 -m http.server 4190 --bind 127.0.0.1
```

Open <http://127.0.0.1:4190/viewer-l-house/>. Keep the server running while using
the model. All assets are local, including the Three.js files in `viewer/vendor`.
The navigation bar links to the model index and the courtyard model.
The booklet link opens the approved plan study.

## Controls

- Drag to orbit; scroll or pinch to move closer.
- Select a named view, floor, pantry option, or daylight/evening lighting.
- Turn the roofs off to inspect the full building.
- Select Walk, then use WASD to move or the arrow keys to move and turn.
  Drag to look, or select Mouse look. Shift moves faster. Escape stops walking.
- Point at a nearby door and press Space, click it, or use the door button.
  Hinged doors, suite pocket doors, the kitchen divider, garden doors and garage
  door operate. Closed doors, walls and furniture block movement.
- Both stairs connect the floors. The model prevents walking off an upper floor.
- In the office view, switch between work and guest-bed use.
- Touch screens have movement buttons while walking.

The default pantry has a short divider and an open passage from the utility.
The enclosed option keeps its direct kitchen door and separate utility access.
The kitchen door is concealed in timber joinery. The main ensuite includes the
compact soaking tub and large shower from the plan.

L01.1 updates the suite to a rectangular bedroom and separate private gallery.
The gallery gives direct access to bedroom, U-shaped dressing room and bathroom.
The exported model includes the new bedroom and gallery garden windows.
Four rooflight zones are recorded in `model.json`; the current renderer does
not cut the roof or ceiling for them. The next Blender model must coordinate
roof openings and light wells. See `studies/l-house-booklet/ASTRA-HANDOFF.md`.

## Rebuild and verify

```sh
python3 scripts/export_l_house.py
node --check viewer-l-house/main.js
node scripts/check_l_house.cjs
node scripts/check_door_timing.cjs
```

The browser check requires Playwright and Chrome. Set `CHROME_PATH` if Chrome is
not at the default macOS path. Set `BASE_URL` if using a different local server.
In this workspace, the bundled Playwright is available with:

```sh
NODE_PATH=/Users/sam/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules node scripts/check_l_house.cjs
```

The check compares both room/furniture layouts and source doors with the booklet.
It checks pantry passage/wall states, door collision, both stairs up and down,
keyboard movement, upper-floor edges, guest-bed state, lighting, the PDF link,
narrow-screen overflow, and local-only asset loading. It saves view images and
results in `tmp/l-house/` for visual review. The timing check inserts 250 ms
frame delays to verify that doors finish on time without jumping after idle.

## Proposals and limits

- The 40 × 65 m plot is assumed, with a north-side road, a 28 m rear garden and
  flat ground. It is not a surveyed site.
- Roof forms, window positions, external finishes and planting are proposals.
- The model uses a 3 m floor-to-floor height. Detailed structure, roof drainage,
  stair headroom, services, product fit and building compliance need design work.
- Furniture and vehicles are simplified objects at the plan footprints. The
  walkthrough is a layout review tool, not a construction or steering model.
- Lighting is illustrative. It is not a daylight or energy analysis.
- Blender and photographic rendering remain a later step.

Static opaque surfaces are batched by material within floor groups. Both model
pages stop their animation loops when idle. See `site/PERFORMANCE.md` for the
measured change and its limits.
