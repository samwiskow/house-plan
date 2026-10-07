# Approved furniture in the living room

The user approved the furniture study on 7 October 2026 and asked for the dining seat to be upholstered into its frame. The new `Fixed upholstered seat` has a shallow crowned surface with its sides wrapped below the timber rails. It has no loose lower cushion or separate welt.

`regenerate_living.py` opens the previous living study, retains its shell and lighting, hides the superseded custom furniture and places the approved study pieces in a separate scene:

- 2.44 × 1.09 m monastery table with an 80 mm plank top and large turned legs.
- Eight cane chairs with fixed cream upholstery, using the previous chair centres and directions.
- Approved custom cream corner sofa.
- 1.25 m square oatmeal footstool, moved 100 mm away from the sofa return to retain clearance.
- Oak media cabinet with inset painted doors, close to the wall.

The existing linen runner is shortened for the table. The console lamp moves inward and down onto the shorter cabinet. Wood flooring, floral rug, panelling, curtains, inset shutters, coastal art, bifolds, log burner and 3.2 m ceiling proposal are retained.

The model uses the free table base credited in `assets/furniture-study/sources.json`. There are no paid assets. The custom sofa is not a downloaded Frankof or Loaf product model.

## Rebuild

First build the furniture study as described in `FURNITURE-STUDY.md`, then run:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python scripts/blender/regenerate_living.py -- --root . --width 1800 --samples 128
```

The build checks the original source object transforms and vertex counts, eight fixed upholstered seats, packed textures, retained alternatives, the 3.2 m ceiling property, the imported table dimensions, and the sofa clearances before rendering.

`output/blender/approved-room/` contains three Cycles PNGs, the editable `approved-room.blend`, and `validation.json`. The editable scene is kept local and excluded from Git because it includes the licensed table asset. This does not publish a browser model or coordinate the ceiling change with the first floor.
