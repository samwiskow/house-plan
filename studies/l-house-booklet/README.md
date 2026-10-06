# L-house design booklet, L01

The user requested a proposed plot, a sensible arrival drive and a roomy rear
garden, followed by a floor-plan booklet for approval before a 3D model.

The PDF is `output/pdf/l-house-design-booklet.pdf`. It is an alternative study;
it does not replace Design book 02 or the published courtyard model.

## Inputs and choices

- `plans.json` contains two snapshots from the reviewed, dimensioned layout.
  Its provenance records the original inline study and its hash.
- The default uses the short pantry divider and 1.05 m open passage.
- The enclosed pantry is preserved as a separate option on page 06.
- The proposed plot is 40 x 65 m, with a 28 m-deep rear garden strip.
- North-side road access and a south-facing garden are assumptions.
- The booklet proposes two garden doors without changing room boundaries.
- The compact soaking tub, two suite pocket doors and house-facing garage
  vehicle door carry forward the reviewed direction.

## Rebuild and check

From this worktree root, with reportlab, pdfplumber and macOS Arial available:

```sh
python3 studies/l-house-booklet/validate_booklet.py
pdftoppm -r 90 -png output/pdf/l-house-design-booklet.pdf tmp/pdfs/l-house-booklet/page
```

Validation rebuilds the booklet, checks the assumed car envelope against
buildings, parked cars, gate edges and paved areas, then checks PDF page sizes,
text bounds and the retained pantry alternative. Rendered pages must also be
visually reviewed. The source uses metres and prints the declared drawing
scales on A3 at 100%.

The car check is a tangent rectangle on paths with assumed 7 m and 8 m radii.
It is not a manufacturer-specific steering model. Real site access, structure,
roof geometry, headroom, products and detailed services remain open.

`site.json` and `checks.json` are generated evidence. The full plans and enlarged
room details use the same snapshot geometry. The prior floor-plan checks are
recorded with the source study; the new checks concern the booklet and plot.

The user approved the booklet direction. Its browser model is in `viewer-l-house/`,
with an export from these measured snapshots and both pantry options.
