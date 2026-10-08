# Astra handoff: coordinated L-house 3D model

Prepared 8 October 2026. The user approved the revised parents suite and asked
for the diagrams and booklet to be updated before the next 3D modelling pass.
This file is a handoff, not a dispatch. No new Astra task has been started.

## Start here

- Worktree: `/Users/sam/Projects/house-plan/.worktrees/codex-parents-suite-gallery`.
- Branch: `codex/parents-suite-gallery`, based on `main` at `7184b55`.
- Use this branch until it is merged. The primary checkout is kept clean.
- Geometry authority: `studies/l-house-booklet/plans.json`, revision L01.1.
- Source SHA-256: `5b37e21d78329e21091b100ef5fc32c3cde7aefddc258dc9c6d3c711aae55010`.
- Plot: `studies/l-house-booklet/site.json`.
- Updated booklet: `output/pdf/l-house-design-booklet.pdf`, nine A3 pages.
- Diagrams: `output/design/l-house-plans/family-wing.png` and `parents-suite.png`.
- Schematic scene export: `viewer-l-house/model.json`; rebuild with
  `python3 scripts/export_l_house.py`.

This is the two-storey L-house with the linked garage, gym, workshop, plant and
upper office. `plan_model.py` and `viewer/` describe the earlier courtyard
house. Do not use them as L-house geometry sources.

An older editable whole-house scene already exists at
`output/blender/l-house/l-house.blend`. It has the former suite layout.
Use the revised measured export to update it; do not treat the old scene as
the latest measured source. Native modelling and new renders are not part
of the completed suite-plan update.

## Approved parents suite

Plan units are metres. Garden / assumed south is at the top of the plan;
arrival / assumed north is at the bottom. Plan coordinates increase right
and down. The browser maps plan Y to Three.js Z. The Blender exporter maps
plan Y to negative Blender Y, with Blender Z vertical.

The outer house remains the L-shaped polygon:
`[[0,0],[6.9,0],[6.9,5],[16.2,5],[16.2,14.8],[0,14.8]]`.
The suite fits inside the existing clear envelope X 0.35-6.55, Y 0.35-9.90.
External walls have a 350 mm allowance; partitions have a 150 mm allowance.
Other room boundaries and furniture are unchanged by this revision.

| Room | Plan origin X,Y | Clear width x depth | Area |
| --- | --- | --- | --- |
| U1 bedroom | 0.35, 0.35 | 6.20 x 3.30 m | 20.46 m² |
| U2 dressing | 0.35, 3.80 | 4.95 x 2.75 m | 13.6125 m² |
| U3 bathroom | 0.35, 6.70 | 4.95 x 3.20 m | 15.84 m² |
| UG gallery | 5.45, 3.80 | 1.10 x 6.10 m | 6.71 m² |

Access is landing -> gallery -> three separate room doors. No route to the
bedroom passes through wardrobes. The gallery stops at the rectangular
bedroom; do not reintroduce the rejected corner cutout.

- Landing entry: horizontal, X 5.50, Y 9.975, width 0.90 m.
- Bedroom entry: horizontal, X 5.50, Y 3.725, width 0.90 m. Provisional pocket
  extends 1.00 m to the left. Keep services and fixings out of this zone.
- Dressing entry: vertical, X 5.375, Y 4.725, width 0.90 m.
- Bathroom entry: vertical, X 5.375, Y 7.30, width 0.90 m.
- Dressing and bathroom leaves provisionally open into their rooms. Hardware,
  sound seals and occupied door operation remain to design.

The 1.95 x 2.15 m super king frame starts at X 2.45, Y 0.50. It retains 1.00 m
at the foot. The three wardrobe runs are 660 mm deep, with a 1.43 m closed
aisle. One 0.50 m drawer leaves 0.93 m; do not claim this as two open drawers
or an occupied-use result. Corner joinery and usable hanging lengths need detail.

Bathroom features must remain: 3.00 x 1.50 m shower, two fixed screens with a
1.00 m central entry, two basins in a 1.50 x 0.55 m vanity, compact soaking tub
allowance 0.85 x 1.10 m, and screened WC. Fitting coordinates and privacy
returns are in the shared furniture list. Product comfort, filled loads,
entry, waterproofing and drainage remain unresolved.

## Approved daylight direction

`plans.json` -> `suiteDaylight` is shared by the booklet and model export.

| Opening | Plan position / footprint | Current modelling allowance |
| --- | --- | --- |
| Large bedroom garden window | Vertical wall X 6.725, Y 1.20-3.20 | 2.00 m wide; sill 0.60 m, head 2.40 m |
| Small gallery garden window | Vertical wall X 6.725, Y 3.90-4.80 | 0.90 m wide; sill 0.85 m, head 2.40 m |
| R1 dressing rooflight | X 1.95, Y 4.67, 1.00 x 1.00 m | Plan zone |
| R2 bathroom rooflight | X 1.80, Y 7.40, 1.00 x 0.75 m | Plan zone |
| G1 gallery rooflight | X 5.60, Y 6.05, 0.70 x 0.70 m | Plan zone |
| G2 gallery rooflight | X 5.60, Y 8.75, 0.70 x 0.70 m | Plan zone |

The right-hand suite wall is external only as far as plan Y 5.00. The gallery
window fits in that exposed segment before Child 2 begins. Do not place another
garden window in the gallery wall shared with Child 2.

The bedroom's existing left window is shortened to 2.40 m. The old dressing /
bathroom window at X 0.175, Y 5.90 is removed because it conflicts with the new
partition and wardrobe layout. The small bathroom window at Y 8.65 remains.

Window sill and head values are provisional modelling choices, not approved
product specifications. The four rooflight rectangles are horizontal plan
zones, not final sizes measured along roof slopes. The browser stores them
but does not yet cut its roof or ceiling. Model trimmers, roof openings and
light wells together; do not add glazed boxes below an intact opaque roof.

## Carry forward the later interior studies

These remain separate from the whole-house measured baseline. Do not overwrite
them while adding the suite. Integrate their chosen geometry and finishes in
a new coordinated scene, with measured differences documented.

1. `output/design/kitchen-selections/boot-room-option.json` and
   `studies/l-house-zoning/README.md`: Option D selected for the render study,
   with enclosed pantry and both kitchen and utility connections. It reallocates
   2.0925 m² of the upper boot-room strip. Do not silently revert to the booklet's
   older short-divider or disconnected enclosed pantry alternatives.
2. `output/design/kitchen-selections/combined.html`, its `combined-renders/plan.svg`,
   and `scripts/blender/COMBINED-ROOM.md`: latest kitchen / dining / living
   arrangement, furniture shifts, four folding glass leaves, continuous kitchen
   parquet, earthy olive sofa, faded ivory rug, pale oak dining furniture,
   cane chairs with fixed upholstery, and full-height linen curtains.
3. `scripts/blender/APPROVED-ROOM.md`, `FURNITURE-STUDY.md`, and the source records
   in `assets/furniture-study/`: approved furniture forms and asset provenance.
4. `scripts/blender/LIVING-STUDY.md`: the 5.80 m garden bifold proposal and closed
   side garden door. Later combined-room finishes supersede older colour choices.
5. `scripts/blender/build_kitchen_study.py` and `build_combined_room.py`:
   reproducible joinery and room integration. Kitchen direction is ivory framed
   perimeter cabinets, dark oak island, pale shaped surface, milk-glass pendants,
   Belfast-style sink, curved timber stools and concealed pantry door.

Keep warm stone, timber and ivory as the house finish direction. Do not import
the courtyard house's roof, ceiling or dimensions into this two-storey model.

The shared-room ceiling study is 3.20 m high, but the schematic whole-house model
has a 3.00 m floor-to-floor height and 2.70 m clear ceiling. These conflict.
Resolve this with a coordinated section before placing the upper floor, stairs,
roof and flue. Do not hide intersecting slabs or silently raise floor levels.
Record a concrete height proposal for review if a choice is required.

The combined-room route check has only about 10 mm spare at its tightest point.
Occupied stools, chair pull-out, pantry swings and appliance use still need
layout work. The log burner is a location study; its flue route through the
first floor / roof has not been selected.

Some interior `.blend` files and the table source are intentionally local and
ignored by Git. Check existing study worktrees before rebuilding. If absent,
use the source records and builders; do not assume a cloned branch contains
those native files. Preserve the recorded asset distribution limits. Do not
purchase assets or publish raw licensed source/composite files.

Verified local inputs at handoff time:

- `/Users/sam/Projects/house-plan.codex-furniture-study/output/blender/combined-room/combined-kitchen-dining-living.blend`
- `/Users/sam/Projects/house-plan.codex-furniture-study/output/blender/approved-room/approved-room.blend`
- `/Users/sam/Projects/house-plan.codex-furniture-study/assets/furniture-study/vendor/monastery-free.blend`

Read or copy these into a new working scene; preserve the source files.

## Modelling sequence and acceptance

1. Start from revised measured geometry. Check full house, garage link, both
   stairs and all room openings. Preserve the approved suite and other boundaries.
2. Coordinate the vertical section and roof with the 3.20 m interior direction
   and four suite rooflights. Mark remaining structural and service assumptions.
3. Integrate the chosen kitchen / living studies, then fit the suite joinery
   and bathroom. Keep room, opening and furniture footprints traceable to sources.
4. Produce an editable Blender scene with named floor, roof, ceiling, opening,
   furniture and site collections. Use metres. Keep scene copies separate from
   the earlier references.
5. Render arrival, garden, full first-floor cutaway, parents bedroom, gallery,
   dressing and bathroom views. Show an unbroken landing-to-bedroom route and
   real light openings. Use Blender/Cycles for stills and the existing Three.js
   viewer for interactive review.
6. Check source hashes, room/door agreement, furniture fit, open doors, stairs,
   upper-floor edges and browser behaviour. Visually inspect final views. Report
   daylight as illustrative unless a daylight analysis has actually been done.

Useful existing pipeline: `scripts/blender/export_scene.cjs`, `build_scene.py`,
`check_scene.py`, `export_lighting.py` and `check_preview.cjs`.
See `scripts/blender/README.md` for commands and axis conventions.

## Checks for this handoff

- Nine A3 booklet pages rebuilt; page sizes and text bounds pass.
- Family-wing and suite diagrams exported from pages 04 and 07 and inspected.
- 533 sampled 700 mm route positions pass in each pantry snapshot, covering
  bedroom, dressing, bathroom, shower and WC with doors open.
- House/garage/plant/office shells, other room boundaries and other furniture
  match the baseline. The external floor-envelope total remains 571.58 m².
- `suite-checks.json` records the source hash and exact scope of those checks.
- Browser regression results are in `tmp/l-house/browser-checks.json` after
  running `node scripts/check_l_house.cjs`. The full check passed, including
  gallery routes in both pantry states, furniture facing, operating doors,
  both stairs, cutaways, walking, phone widths and local-only loading.

No surveyed plot, roof structure, services design, occupied-use approval,
product fit or construction compliance result is claimed.
