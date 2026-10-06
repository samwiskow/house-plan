# L-house living/dining realism benchmark

This study develops one interior for review. It uses the L01 measured model as its base. The current interior proposal tests a 3.2 m ceiling, widens the main garden opening, closes the side garden door and changes the furniture layout; those changes have not been applied to the measured plan or browser model. It builds on the native Blender study in `output/blender/l-house/l-house.blend`.

## Styling from the house brief

`MATERIALS-BRIEF.md`, **Agreed shared-space palette**, specifies warm ivory, pale-to-honey oak, muted bronze, a deeper oatmeal sofa and a six-arm chandelier with ivory shades. The visible kitchen uses ivory framed perimeter cabinets and a forest-green island. The brief's courtyard-house dimensions, vaulted ceiling, roof choices and stove reservation are not applied to the L-house.

The current user direction uses warm ivory panelling around the room, recessed plantation shutters with full-length linen curtains, a green floral woven rug, a large connected oatmeal corner sofa and a plain cream/oatmeal ottoman. Smaller coastal paintings and layered lamps add colour and light. The table and bare wooden ladder-back chairs use rustic French country forms and lighter oak, with Cotswold Co. as a style reference. A cream linen runner replaces the table vase. There are no loose sofa cushions or dining seat pads. The shallow painted media cabinet has framed doors and an oak top, and sits about 45 mm from the wall at its deepest rear edge.

Original generated botanical and floral textures take their direction from William Morris and Laura Ashley. These are original study patterns, not replicas or selected retail fabrics. The green floral print from the earlier ottoman is now used on the rug; the ottoman is plain woven linen. The living and dining floor uses matte natural oak planks, with staggered joints and subtle board colour variation. The kitchen retains the warm buff limestone-effect option. The detailed furniture is custom study geometry, not a selected retail product.

## Furniture reference update

The user's two room photographs guide the table's muted, weathered timber finish and the footstool's plain, tactile upholstery. They are visual references; their accessories, chairs and room layout are not copied into the study.

The user identified their sofa as the Loaf Big Easy Corner Sofa, Extra Large Right Hand, in Milky Way Clever Cotton. [Loaf's current product page](https://loaf.com/products/big-easy-corner-sofa) was checked on 6 October 2026. Its broad arms, low body, long seat cushions and loose back cushions inform this custom model. The room keeps its larger 4.10 × 3.65 m sofa reservation; this is not an exact Loaf product model or fit test. The material is a visual cotton approximation, not a manufacturer fabric scan. The user chose to retain cream/oatmeal for this room.

The table alone has a separate muted oak finish. The sofa uses fuller seat and back shapes with small cloth irregularities, broad arms and low feet. The plain footstool has a softly crowned top and fine piping. Existing room height, circulation, rug, curtains and panelling are retained.

## Deliverables

- `output/blender/living-study/living-dining.png`: main room view towards the garden.
- `output/blender/living-study/seating-detail.png`: closer view of the seating and textiles.
- `output/blender/living-study/living-study.blend`: editable native scene with packed textures.
- `output/blender/living-study/hearth-dining.png`: reverse view of the dining set and proposed burner position.
- `study-report.json` and `validation.json`: provenance and measured-source checks.

The detailed scene includes a single L-shaped sofa base with a joined corner seat and continuous back, upholstery seams, curved wooden chairs, a trestle table, a draped runner, framed panelling, recessed shutter louvres and curtain folds. Panelling is present on the rear wall for the reverse view, with mineral backing at the burner. Coastal paintings have picture lights. Floor lamps beside the dining area and behind the sofa near the bifolds supplement the ceramic console lamp and chandelier.

The ceiling underside is 3.20 m in this interior option. The walls, chandelier suspension and visible stove flue extend to suit it. Source ceiling, slab and upper-floor pieces which cross this test volume are retained but hidden. The first-floor level, stairs, roof and external elevations have **not** been coordinated with this option. This file must not be treated as a resolved whole-house design.

The original G1 furniture and G2 cabinet/island objects are retained but hidden; the two island seats stay visible. The original pantry and office alternatives remain available. The rest of the house and outdoor furniture remain schematic.

The proposed garden opening is 5.80 m wide with a 2.40 m head, short wall returns and six glazed folding leaves shown open outwards. Its source wall sections and original slider are retained but hidden. The separate side terrace door is retained but hidden behind a new wall infill in this option. This is a visual opening proposal; support and door-system details are not resolved. The sofa now reserves about 4.10 × 3.65 m, with its return along the garden end. The separate armchair is removed. A 1.65 × 1.10 m upholstered ottoman replaces the coffee table. Checks confirm at least 0.35 m from the ottoman to the continuous L-shaped sofa base and at least 1.20 m between the sofa end and media cabinet. Nine original furniture centres remain unchanged.

The log burner is a location study on the short wall beside the closed side terrace doorway and kitchen opening, with a stone-effect backing and hearth replacing the timber panelling in that zone. The interior flue stops at the ceiling; no route through the first floor or roof has been selected. Hearth construction, heat output, ventilation and the chosen appliance's clearance requirements need a site/design check. Dining circulation around this hearth is the tight part of the proposal and is not verified as an installation. [Stovax guidance](https://www.stovax.com/distance-combustibles/) makes clear that the required distances depend on the stove model.

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

`assets/living-study/generated-assets.json` records the exact prompts, built-in image_gen method and source references for the original botanical/floral textiles and coastal paintings. Earlier art assets remain in the asset history. The assets used in this scene are packed into the native Blender file. The room images are Cycles renders of the actual model.
