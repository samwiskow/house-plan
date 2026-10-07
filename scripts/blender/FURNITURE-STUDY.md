# Isolated furniture study

Prepared on 7 October 2026. This is a separate furniture review scene. It does not change the measured house plan, the living room scene or the website. All assets used cost zero.

## Review pieces

- Table: Floris Smit's free Wooden monastery table from BlenderKit, adapted to 2.44 × 1.09 m. The original turned-leg base is retained and widened. Six 80 mm thick oak planks, breadboard ends and small dowel details replace the original top. Pale oak uses the existing Poly Haven CC0 texture.
- Chair: a custom study based on the user's Cotswold Company Camille reference. It has an arched cane back with actual woven openings, curved legs, cream upholstery fixed into the seat frame and a plain crown. It is not an exact retail product model.
- Sofa: the existing custom L-shaped sofa shown separately. The free Frankof Lagos asset requires a GreatCatalog account and has not been downloaded. This is not a Frankof or Loaf product model. No loose scatter cushions are included.
- Footstool: a custom 1.25 × 1.25 m square oatmeal footstool, with a full top cushion, piping and short oak feet.
- Media cabinet: a custom oak cabinet with inset painted door panels and a central open shelf. This replaces the rejected catalogue reference. The user approved this design direction on 7 October 2026.

The furniture is shown with the same neutral studio lighting, using Cycles. Review the shape and material before inserting pieces into the room. The approved set is placed in a separate room scene by `regenerate_living.py`; its report records the clearances.

## Source and licence

Table by Floris Smit: https://www.blendkit.com/asset-gallery-detail/6f6bf86f-e227-42ba-a3eb-646081d93a0d/

The catalogue marks the table free, under the BlenderKit Royalty Free licence. Licence information: https://www.blendkit.com/docs/licenses/

The downloaded source and editable composite study stay local and are excluded from Git. They must not be published as standalone downloadable furniture assets. Browser redistribution has not been approved. Rendered review images are derivative output.

Paid table and chair models were visual references only. No paid asset was downloaded or purchased. `assets/furniture-study/sources.json` records the source file hash and references.

## Rebuild

Download the free BlenderKit table to `assets/furniture-study/vendor/monastery-free.blend`. The existing `output/blender/living-study/living-study.blend` supplies the sofa geometry and packed fabric materials.

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python scripts/blender/build_furniture_study.py -- --root . --samples 64
```

Output is in `output/blender/furniture-study/`. The five PNGs are actual Blender renders. `furniture-study.blend` is an editable scene with separate named collections and packed textures. `report.json` records rendered pieces, dimensions, cost and provenance. `--only chair` can render a single piece after an edit.
