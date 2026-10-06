# Model performance, 6 October 2026

The site now loads a static model index. It loads Three.js and model data only
when a visitor opens a model page. Both pages share the same vendored Three.js
files. The two WebP previews total about 52 KB.

## Rendering changes

The L-house combines opaque static meshes that share a material and shadow
settings. Batches stay within each floor and ceiling group. Doors remain
separate and movable; transparent surfaces keep their original sorting.
Coordinates, normals, UVs, materials and triangle detail are retained. Source
room, furniture and door records still agree with both booklet plans.

Both viewers now schedule frames only when needed. Pointer and key input,
settings, camera damping and door animations wake the renderer. Stationary
walkthrough views also stop their animation loop.

## Local measurements

Chrome, Apple M1 Max / ANGLE Metal, 1200 × 800, device scale 1. Eight forced
renders per view, with `gl.finish()` included in each timing. These are local
render timings, not a promise of frame rate on other devices.

| L-house view | Draw calls before | Draw calls after | Median before | Median after |
| --- | ---: | ---: | ---: | ---: |
| Whole plot | 2,048 | 404 | 4.9 ms | 1.7 ms |
| Ground floor | 1,018 | 251 | 2.9 ms | 0.9 ms |
| Living room | 262 | 133 | 2.1 ms | 0.9 ms |

Allocated geometry objects fell from 2,052 to 408. Textures stayed at 36.
The living-room batch submits more triangles because whole batches share a
visibility bound; its measured render time still fell. Roof and floor controls,
collision and door picking are verified separately.

Whole-plot and ground-floor triangle counts are unchanged. Matching screenshot
comparisons had mean absolute RGB differences below 0.003 on the 0–255 scale.
The courtyard rendering is unchanged; its optimization concerns idle work.

In a 1.2-second idle sample, each page went from 72 animation callbacks to zero.
The page controls and walkthrough wake the loop again.

## Repeat

Serve the worktree root locally, or set `BASE_URL` to the staged site's root:

```sh
node scripts/measure_models.cjs current
node scripts/check_idle.cjs current
node scripts/check_viewer.cjs
node scripts/check_l_house.cjs
node scripts/check_site.cjs
```

The browser scripts require Playwright and Chrome/Chromium. `CHROME_PATH` can
override the browser. `tmp/performance/` contains measurements and images;
`tmp/site-review/` contains desktop and phone navigation captures.
