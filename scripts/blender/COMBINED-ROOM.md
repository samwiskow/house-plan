# Combined kitchen, dining and living study

The user approved combining the three rooms on 7 October 2026. This separate Blender scene starts from the kitchen study, which already contains the approved living furniture. Source files remain unchanged.

## Rebuild

Run from the repository root with Blender 5.2, Python 3 and a Metal-capable Mac.
The renderer currently selects Metal explicitly. Use the `blender` command from
your installation, or `/Applications/Blender.app/Contents/MacOS/Blender` on macOS.

First obtain the free table source described in [FURNITURE-STUDY.md](FURNITURE-STUDY.md).
The source path and SHA-256 are recorded in `assets/furniture-study/sources.json`.
The earlier living scene and fabric textures are already tracked. Build in this
order because each scene uses the preceding scene as its input:

```sh
python3 studies/l-house-zoning/build_study.py
python3 studies/l-house-zoning/build_boot_study.py
blender --background --disable-autoexec --python-exit-code 1 --python scripts/blender/build_furniture_study.py -- --root . --samples 64
blender --background --disable-autoexec --python-exit-code 1 --python scripts/blender/regenerate_living.py -- --root . --width 1800 --samples 128
blender --background --disable-autoexec --python-exit-code 1 --python scripts/blender/build_kitchen_study.py -- --root . --width 1600 --samples 96
blender --background --disable-autoexec --python-exit-code 1 --python scripts/blender/build_combined_room.py -- --root . --width 1600 --samples 96
python3 scripts/blender/check_combined_layout.py
python3 scripts/blender/build_kitchen_gallery.py
python3 scripts/blender/build_combined_gallery.py
```

Use `--views` followed by view names on the combined builder for selected renders.
The committed gallery can be viewed without Blender or the licensed source file.

The editable file is output/blender/combined-room/combined-kitchen-dining-living.blend. Frame 1 opens the internal divider; frame 60 closes it. Four hinged leaves form a parented chain. Textures are packed. The file stays local because it includes the existing licensed furniture asset.

Serve output/design/kitchen-selections on 127.0.0.1:4195 and open combined.html. The page shows rendered comparisons and a furniture plan, not live Blender rendering.

## Placement changes

- Dining furniture and chandelier move 600 mm towards the hall.
- Island, pendants and stools move 100 mm towards the sink and 75 mm towards the pantry.
- Kitchen herringbone meets the living floor at the same height.
- The partial screen clears the sofa, coastal picture and corner lamp.
- Four folding glass leaves replace the earlier sliding proposal. Parking on the north return would conflict with the burner or kitchen cabinets. The rear folded position leaves about 2.14 m clear.
- A glazed transom replaces the solid wall above the opening; support is not designed.
- Overlapping ceiling and wall patches and zero-thickness wall cells are hidden in the combined copy.

## Checks and limits

validation.json records object-bound measurements and source hash. route-check.json screens a nominal 600 mm route against furniture boxes with 400 mm dining-chair pull-out, sampled every 20 mm. It has only about 10 mm margin at its tightest point. This is an initial geometry check, not access or occupied-use validation.

The rear stool and dining-chair spaces are not through-routes. Pantry door swing, open appliances, high cupboard access, folding hardware, stove installation, structural support and first-floor coordination of the 3.2 m ceiling remain open.

## Finish revision

The combined copy now uses lighter natural oak on the dining table and chair frames, with lighter cane. The rug uses `assets/furniture-study/faded-persian-rug.png`, generated with the built-in image tool from the user reference. The table, chair and rug geometry, dining upholstery, furniture layout and lighting are unchanged.

Texture prompt: flat edge-to-edge rug albedo; traditional Persian floral and vine motifs with nested borders; distressed ivory and oatmeal ground, muted taupe, warm brown and slate blue-grey details; even diffuse lighting; no room, furniture, UI or perspective.

Sofa colour trial: earthy olive green (supersedes sage) on the existing cotton material, applied only to the corner sofa. The footstool stays cream.

Continuous flooring: extend the kitchen herringbone board size, orientation, material and grid origin across living/dining and the internal opening. Existing straight boards are hidden only in the combined copy. Add cream linen curtains on a full-width ceiling track at the garden bifolds, drawn back at both ends. Furniture positions remain unchanged.
