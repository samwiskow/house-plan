# L-house living/dining realism benchmark

This study develops one interior for review. It uses the L01 measured model as its base. The current interior proposal widens the garden opening and changes the sofa footprint and coffee-table position; those changes have not been applied to the measured plan or browser model. It builds on the native Blender study in `output/blender/l-house/l-house.blend`.

## Styling from the house brief

`MATERIALS-BRIEF.md`, **Agreed shared-space palette**, specifies warm ivory, pale-to-honey oak, muted bronze, a deeper oatmeal sofa and a six-arm chandelier with ivory shades. The visible kitchen uses ivory framed perimeter cabinets and a forest-green island. The brief's courtyard-house dimensions, vaulted ceiling, roof choices and stove reservation are not applied to the L-house.

The next user direction adds warm ivory wall panelling, a muted rust rug, an oatmeal corner sofa, plantation shutters, an antique-style oak dining table and garden bifolds across most of the end wall. These choices replace the first study's neutral rug, straight sofa, linen curtains and plain dining table. Cream chairs and forest-green/tobacco cushions remain supporting proposals. The living and dining floor uses matte natural oak planks, as requested, with staggered joints and subtle board colour variation. The kitchen retains the warm buff limestone-effect option. No flooring product is selected. The detailed furniture is custom study geometry, not a selected retail product.

## Deliverables

- `output/blender/living-study/living-dining.png`: main room view towards the garden.
- `output/blender/living-study/seating-detail.png`: closer view of the seating and textiles.
- `output/blender/living-study/living-study.blend`: editable native scene with packed textures.
- `study-report.json` and `validation.json`: provenance and measured-source checks.

The detailed scene has separate upholstery cushions and piping, tapered furniture legs, curved chair backs, framed cabinet fronts, bronze handles, shutter louvres, framed wall panelling, window sills, skirting, a rust woven rug and the chandelier. The dining table has a darker aged-oak finish, breadboard ends and turned legs. Planting visible through the windows has individual leaves. The rest of the house and outdoor furniture remain schematic. The original G1 furniture and G2 cabinet/island objects are retained but hidden; the two island seats stay visible; the original pantry and office alternatives remain available without the new detailed furniture treatment.

The proposed garden opening is 5.80 m wide with a 2.40 m head, short wall returns and six glazed folding leaves shown open outwards. Its source wall sections and original slider are retained but hidden. This is a visual opening proposal; support and door-system details are not resolved. The corner return is at the garden end of the sofa. The coffee table moves 0.15 m across and 0.60 m towards dining, with at least 0.35 m clearance from each sofa base section. Eleven other furniture centres stay in place.

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
