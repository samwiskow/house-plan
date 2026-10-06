# L-house living/dining realism benchmark

This study develops one interior for review. It uses the L01 measured model as its base. The current interior proposal widens the garden opening and changes the furniture layout; those changes have not been applied to the measured plan or browser model. It builds on the native Blender study in `output/blender/l-house/l-house.blend`.

## Styling from the house brief

`MATERIALS-BRIEF.md`, **Agreed shared-space palette**, specifies warm ivory, pale-to-honey oak, muted bronze, a deeper oatmeal sofa and a six-arm chandelier with ivory shades. The visible kitchen uses ivory framed perimeter cabinets and a forest-green island. The brief's courtyard-house dimensions, vaulted ceiling, roof choices and stove reservation are not applied to the L-house.

The current user direction combines warm ivory panelling and plantation shutters with a deep green rug, a much larger oatmeal corner sofa, botanical upholstery, large framed art and layered lamps. The table and ladder-back chairs use rustic French country forms and aged oak. The shallow painted media cabinet has framed doors and an aged oak top, and sits about 45 mm from the wall at its deepest rear edge.

Original generated Arts and Crafts botanical and English cottage floral textures take their direction from William Morris and Laura Ashley. They are study patterns, not replicas or selected retail fabrics. The botanical print is used on the ottoman and cushions; the blue floral print is used on dining seats and cushions. The living and dining floor uses matte natural oak planks, as requested, with staggered joints and subtle board colour variation. The kitchen retains the warm buff limestone-effect option. No flooring product is selected. The detailed furniture is custom study geometry, not a selected retail product.

## Deliverables

- `output/blender/living-study/living-dining.png`: main room view towards the garden.
- `output/blender/living-study/seating-detail.png`: closer view of the seating and textiles.
- `output/blender/living-study/living-study.blend`: editable native scene with packed textures.
- `output/blender/living-study/hearth-dining.png`: reverse view of the dining set and proposed burner position.
- `study-report.json` and `validation.json`: provenance and measured-source checks.

The detailed scene has separate upholstery cushions and piping, tapered furniture legs, curved chair backs, framed cabinet fronts, bronze handles, shutter louvres, framed wall panelling, window sills, skirting, a deep green woven rug and the chandelier. The dining table has an aged-oak finish, thick worn planks, breadboard ends, shaped trestles and a low stretcher. The matching ladder-back chairs have curved legs and floral seats. Two large framed paintings, two picture lights, a bronze corner floor lamp and a ceramic console lamp add detail and light. Planting visible through the windows has individual leaves. The rest of the house and outdoor furniture remain schematic. The original G1 furniture and G2 cabinet/island objects are retained but hidden; the two island seats stay visible; the original pantry and office alternatives remain available without the new detailed furniture treatment.

The proposed garden opening is 5.80 m wide with a 2.40 m head, short wall returns and six glazed folding leaves shown open outwards. Its source wall sections and original slider are retained but hidden. This is a visual opening proposal; support and door-system details are not resolved. The sofa now reserves about 4.10 × 3.65 m, with its return along the garden end. The separate armchair is removed. A 1.65 × 1.10 m upholstered ottoman replaces the coffee table. Checks confirm at least 0.35 m from the ottoman to the two sofa base sections and at least 1.20 m between the sofa end and media cabinet. Nine original furniture centres remain unchanged.

The log burner is a location study on the short wall between the side terrace door and kitchen opening, with a stone-effect backing and hearth replacing the timber panelling in that zone. The interior flue stops at the ceiling; no route through the first floor or roof has been selected. Hearth construction, heat output, ventilation and the chosen appliance's clearance requirements need a site/design check. Dining circulation around this hearth is the tight part of the proposal and is not verified as an installation. [Stovax guidance](https://www.stovax.com/distance-combustibles/) makes clear that the required distances depend on the stove model.

Daylight is supplemented by invisible area fill lights near the windows, plus warm chandelier bulbs, floor/table lamps and picture lights. These are presentation lighting choices rather than a daylight or electrical design. Images use Cycles and are intended for review of materials, furniture and atmosphere. The browser GLB is not changed by this study.

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

## Generated art and textile assets

`assets/living-study/generated-assets.json` records the exact prompts, built-in image_gen method and source references for `botanical.png`, `floral.png`, `landscape.png` and `still-life.png`. These are original study assets packed into the native Blender file. The room images are Cycles renders of the actual model.
