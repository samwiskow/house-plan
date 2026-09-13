# Courtyard house: revised design review

Start with concept 25. It combines the garden-side plant, two-workspace office
and library snug with the retained house layout. These are measured proposals
for review; product and construction design remain outstanding.

| Document | Purpose |
| --- | --- |
| [25: Revised whole-house plan](output/pdf/concept-25-revised-whole-house-plan.pdf) | Furnished A3 plan at 1:100, 26-room schedule and next decisions. |
| [24: Library snug](output/pdf/concept-24-library-snug.pdf) | Plan and full-height bookcase elevations with integrated TV provision. |
| [23: Two-workspace office](output/pdf/concept-23-two-workspace-office.pdf) | Two permanent desks for one person, both work modes and both overnight foot exits. |
| [22: Garden-side plant and wing services](output/pdf/concept-22-garden-plant-and-wing-services.pdf) | Rear plant and gym layouts, internal access, rooflight, wing cooling and hot-water options. |

## Latest measured ventilation comparison: concept 27

[Central and two-local-unit layouts](output/pdf/concept-27-measured-ventilation-layouts.pdf)
now show the cupboard plans, rear maintenance space, main duct routes and vault
section. B is recommended for further design: retain 1.25 m linen beside a
family-side unit, versus 2.05 m with central plant and a 13.05 m shared-room
edge enclosure. Both alternatives pass 56 daytime routes. The five A3 sheets
were rendered and inspected. Unit duty, outlet throw, acoustic performance and
complete duct / roof fit remain unverified; neither option is selected.

## Latest services decision: concept 26

Underfloor heating is confirmed as the winter comfort preference. The
[heating, hot-water and ventilation study](output/pdf/concept-26-heating-hot-water-and-ventilation.pdf)
recommends an air-to-water heat pump for wet floors and a service-end cylinder,
plus separate wing cooling. Two local MVHR systems are the first routing option
to test against central duct distribution, conditional on a family-side cupboard.
No geometry or equipment size changes. All four A3 pages were rendered and checked;
room-duty references and illustrative water arithmetic were verified.

## Current direction

- The plant projects behind the gym toward the garden, with an interior gym
  door and an external service door. The arrival-side concept 17 B is declined.
- Full gym area and equipment body sizes are retained; rack and dumbbells move.
- The snug becomes a library with TV provision; a rooflight replaces its window.
- One person switches between professional and personal office setups. Both
  remain in place for occasional sofa-bed use, with a connected foot-end route
  for each sleeper. Visiting children may share beds.
- Dining is accepted on the stated working interpretation of eight at the table
  plus two at the island. A ten-at-one-table arrangement is not drawn.
- Separate wing cooling is the starting concept; outdoor-unit count and shared
  zone allocation depend on loads and the selected systems. Fresh-air ventilation
  remains separate. Wet underfloor heating is confirmed; hot-water sizing remains to design.

## Next decisions, in order

1. Develop the confirmed wet-underfloor direction and prove the proposed local ventilation outlets and acoustic treatment.
   Size hot water for simultaneous shower use; assess water supply, recovery,
   pipe delays / losses and equipment maintenance space.
2. Draw the roof / exterior with the rear plant, snug rooflight, nearby office
   window, shading, outdoor units and continuous shared-room vault.
3. Check the actual site and budget before fixing joinery and finishes.

## Verification and limits

The final proposal checks 56 sampled routes with a 0.70 m envelope in each of
three office states: professional, personal and overnight. Library approaches,
both office foot exits, room containment and door sweeps pass. Concept 22 also
checks the new plant approaches against the fully open internal door. All 16
new A3 pages were rendered and inspected. These checks do not establish actual
furniture mechanisms, accessibility, structural design or equipment performance.

The plant adds 13.05 m2 net footprint and 10.60 m2 clear room area. The revised
model totals 332.96 m2 internal envelope, 373.31 m2 external footprint and
315.52 m2 clear room polygons. The original family plant placeholder remains
until relocation is fully designed; no extra installed package or released
linen storage is implied. Proposed rooflight and joinery heights are allowances.

## Provenance and delivery

Rebuild sequentially with `garden_plant_study.py`, `two_workspace_office.py`,
`library_snug.py` and `revised_house_plan.py`. Each verifies source hashes; the
original measured model is loaded through `development_model.py`. JSON snapshots
beside the PDFs preserve geometry, route checks and limits. Older PDFs remain
historical records rather than being silently regenerated.

Four sequential local commits isolate plant / services, office, library and
consolidation. `codex/revised-house-plan` contains the complete stack. Main is
unchanged. No remote is configured, so no PR/MR or remote pipeline is available.

Concept 26 is delivered on `codex/heating-ventilation-options`, based on the
complete concept 25 stack. The source script, four-page PDF and calculation
snapshot form one scoped change; no older drawings are regenerated.

Concept 27 is delivered on `codex/measured-ventilation-layouts`, based on the
concept 26 stack. The whole-house geometry is unchanged; two conditional
plant/linen furniture states are stored in the study snapshot. No remote is
configured, and main remains unchanged.
