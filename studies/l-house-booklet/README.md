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
- L01.1, approved 8 October 2026, replaces the walk-through dressing route with
  a private gallery and three separate room doors. The bedroom stays rectangular
  at 6.20 x 3.30 m; dressing is 4.95 x 2.75 m; bathroom is 4.95 x 3.20 m.
- U-shaped wardrobes are 660 mm deep, with a 1.43 m aisle. The gallery is
  1.10 m clear. The bedroom retains a pocket door; dressing and bathroom doors
  open into their rooms as provisional hardware choices.
- The 2.00 m bedroom garden window, 0.90 m gallery garden window and four
  rooflight zones are shared by the full plan, detail and model export.
  Roof openings, light wells, sills and structure remain to design.
- The compact soaking tub, double vanity, screened WC, 3.00 x 1.50 m shower
  and house-facing garage vehicle door carry forward the reviewed direction.

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
room details use the same snapshot geometry. The prior floor-plan checks apply
to the original source. `suite-checks.json` records revised sampled 700 mm routes
in both pantry snapshots, with doors open. These are footprint checks, not
occupied-use or accessibility checks. Other checks concern the booklet and plot.

The user approved the booklet direction. Its browser model is in `viewer-l-house/`,
with an export from these measured snapshots and both pantry options.

`output/design/l-house-plans/family-wing.png` and `parents-suite.png` are page
exports of the revised diagrams. Regenerate them after the PDF:

```sh
mkdir -p tmp/pdfs/l-house-booklet output/design/l-house-plans
pdftoppm -r 100 -png output/pdf/l-house-design-booklet.pdf tmp/pdfs/l-house-booklet/page
cp tmp/pdfs/l-house-booklet/page-4.png output/design/l-house-plans/family-wing.png
cp tmp/pdfs/l-house-booklet/page-7.png output/design/l-house-plans/parents-suite.png
```

The courtyard design books and older L-house render studies remain historical
references. `ASTRA-HANDOFF.md` identifies the inputs for the next coordinated
whole-house model.
