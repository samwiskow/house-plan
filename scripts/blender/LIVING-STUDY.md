# L-house living/dining realism benchmark

This study develops one interior for review. The room envelope, openings and furniture centres come from the L01 measured model. It builds on the native Blender study in `output/blender/l-house/l-house.blend`.

## Styling from the house brief

`MATERIALS-BRIEF.md`, **Agreed shared-space palette**, specifies warm ivory, pale-to-honey oak, muted bronze, a deeper oatmeal sofa and a six-arm chandelier with ivory shades. The visible kitchen uses ivory framed perimeter cabinets and a forest-green island. The brief's courtyard-house dimensions, vaulted ceiling, roof choices and stove reservation are not applied to the L-house.

Cream chairs, linen curtains, a textured oatmeal rug and small forest-green/tobacco cushions are supporting proposals in that brief. The living and dining floor uses matte natural oak planks, as requested, with staggered joints and subtle board colour variation. The kitchen retains the warm buff limestone-effect option. No flooring product is selected. The detailed furniture is custom study geometry, not a selected retail product.

## Deliverables

- `output/blender/living-study/living-dining.png`: main room view towards the garden.
- `output/blender/living-study/seating-detail.png`: closer view of the seating and textiles.
- `output/blender/living-study/living-study.blend`: editable native scene with packed textures.
- `study-report.json` and `validation.json`: provenance and measured-source checks.

The detailed scene has separate upholstery cushions and piping, tapered furniture legs, curved chair backs, framed cabinet fronts, bronze handles, curtain folds, window sills, skirting, a woven rug and the chandelier. Planting visible through the windows has individual leaves. The rest of the house and outdoor furniture remain schematic. The original G1 furniture and G2 cabinet/island objects are retained but hidden; the two island seats stay visible; the original pantry and office alternatives remain available without the new detailed furniture treatment.

Daylight is supplemented by invisible area fill lights near the windows, plus warm chandelier bulbs. These are presentation lighting choices rather than a daylight or electrical design. Images use Cycles and are intended for review of materials, furniture and atmosphere. The browser GLB is not changed by this study.

## Rebuild and check

Run from the repository root with Blender 5.2:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python-exit-code 1 --python scripts/blender/refine_living.py -- --root . --width 1800 --samples 160
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python-exit-code 1 --python scripts/blender/check_living.py -- .
```

## External assets

Oak and fabric maps are [Poly Haven](https://polyhaven.com/license) CC0 assets, packed into the Blender file and included under `assets/living-study/` for rebuilds:

- [Oak Veneer 02](https://polyhaven.com/a/oak_veneer_02): colour, normal and roughness maps.
- [Terlenka](https://polyhaven.com/a/terlenka): woven-fabric colour, normal and roughness maps, recoloured in the shader to the brief's palette.

`sources.json` records the original download URLs. No purchased or restricted assets are used.
