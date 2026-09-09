# U-shaped family home - concept 05

The current dimensioned study is `output/pdf/u-home-dimensioned-concept.pdf`.
Its four A3 sheets contain the 1:100 floor plan, room schedule and 1:60 family
wing, 1:60 orangery/service/gym detail, and 1:200 illustrative site plan.
Print at 100% to preserve scale. Concept 04 remains available in Git history.

## Separate two-storey option

`output/pdf/two-storey-linked-pavilion-option.pdf` records option C as two
low-fidelity A3 sheets: ground floor and upper floor. A two-storey main house
contains all bedrooms; a separate single-storey office/gym pavilion connects
through an enclosed garden passage. No bedroom sits above or beside the office.

This is an unmeasured alternative, not a replacement for concept 05. Room
groups, stairs, areas and structure still need fitting and verification.
Its independent renderer is `two_storey_option.py`; run it with the same
Python runtime as the rebuild command below. It does not regenerate concept 05.

## Agreed brief

- Predominantly single-storey U around a sheltered courtyard, with a larger
  main garden. The H alternative was set aside because its arrival court was
  not a priority.
- Parents' bedroom, walk-in wardrobe and ensuite; three children's bedrooms;
  guest bedroom and shower; separate family bathroom and visitor WC.
- Compact family grouping with bathroom and storage buffering the parents.
- Large open kitchen/dining/living area and an enclosed reading/play snug at
  the guest-wing transition, with circulation beside it.
- Dedicated office/gaming room for one person; no business visitors.
- Pantry beside the kitchen counter and fridge, also reached from the smaller
  entrance hall. Boot room connects to the hall, enlarged separate laundry
  and indoor gym. Hall retains its own kitchen route.
- Visitor WC in the upper portion of the former pantry, off the guest hall.
- Small orangery in the bottom-right courtyard corner, linking the guest-wing
  hall and open-plan space. Direct hall/living and living/courtyard routes
  remain. Sliding glazing opens the orangery towards the courtyard.
- Indoor gym for a combined rack/cable station, barbell, bench, dumbbells and
  possible treadmill. Equipment footprints are illustrative; actual machine
  dimensions, use clearances and ceiling heights remain to be coordinated.
- Two household cars in a solar carport and an independent guest bay.
- Selected pocket doors are welcome where they improve circulation.

## Measured outcome

- Internal area (GIA): 319.91 m², up 40.10 m² from concept 04's 279.81 m².
- External footprint: 360.26 m²; outer envelope 27.15 × 18.40 m.
- External walls assumed 350 mm; internal partitions generally 120 mm.
  The former external walls between the additions and house remain 350 mm.
- Orangery: 4.00 × 3.50 m nominal external allocation; 3.65 × 3.15 m clear,
  giving 11.50 m² inside. Its contribution to GIA is 14.00 m², including
  retained dividing walls and thresholds.
- Indoor gym: 4.00 × 6.00 m clear / 24.00 m². Its contribution to GIA is
  26.10 m² including the retained wall between gym and service wing.
- Shared kitchen/dining/living: 74.73 m², compared with 75.49 m² in concept 04.
- Pantry: 6.11 m²; entrance hall: 6.66 m²; laundry: 10.86 m².
  Moving the pantry 0.90 m towards the hall recovers 2.34 m² of kitchen
  compared with the preceding exploratory pantry option, not concept 04.
- Visitor WC: 3.12 m²; boot room: 8.58 m².
- Children: 12.79 m² each, with clear internal dimensions 3.03 × 4.22 m.
- Parents' sleeping room: 16.80 m²; guest room: 17.12 m² including wardrobe recess.
- Other circulation: 26.80 m². Family corridor is 8.56 m long; guest corridor
  is 11.16 m long. Both are 1.20 m wide; shower lobby is included in circulation.
- Open courtyard: 88.40 m² within the original 8.00 × 12.80 m recess;
  approximately 38 m² remains paved. A 4.00 m outdoor strip separates the
  orangery from the family bedroom wing.
- Illustrative plot: 35 × 45 m / 1,575 m². House offset remains 3.30 m from
  the left boundary and 12.50 m from the rear; gym leaves 4.55 m to the right.
- Carport clear allocation: 6.80 × 6.20 m. Provisional roof envelope:
  7.20 × 6.60 m, with columns outside the clear allocation. Guest bay:
  3.20 × 6.00 m. A 1.40 m strip separates house and parking allocations;
  the carport roof overhang reduces that separation locally to 1.20 m.
- Internal partitions and doorway thresholds: 17.35 m². These reconcile the
  clear room polygons to GIA; thicker final walls could change the balance.

## Verification and limits

`plan_model.py` is the editable geometry and drawing source. The generated
`output/pdf/area-check.json` records room areas and checks. Geometry is in metres;
room areas include fitted joinery footprints.

The model checks room overlaps and envelope containment, furniture containment
and overlaps, declared internal door connections, conflicts between pocket
reservations and other openings, hinged door sweeps against furniture, and a
sampled 0.70 m walking envelope on seven nominated routes. These include the
orangery connection and boot-to-gym access. The current run has no reported
conflicts. All four PDF pages were rendered and visually inspected.

These checks do not certify building-regulations compliance, accessibility,
acoustics, structural spans, fire escape, drainage, ventilation or vehicle
turning. The gym's 1.35 × 2.20 m treadmill rear zone is a provisional space
reservation, not confirmation of a chosen manufacturer's clearance requirements.
Barbell loading, cable use, equipment access and anchoring require further work.

Orangery and laundry rooflights are indicative. The laundry's former side window
is replaced by a proposed rooflight because the gym adjoins that wall. Orangery
heating, glazing, shading and ventilation are undecided; doors allow separation
from the house. Bedroom daylight, courtyard privacy and roof drainage need a
site-specific review. The test plot is not a minimum plot specification or
proof that any particular plot is buildable. Vehicle swept paths, pocket-door
kits, structural wall build-ups, cabinetry and plumbing require coordination.

The GIA convention follows the internal-face definition in England's
[nationally described space standard](https://www.gov.uk/government/publications/technical-housing-standards-nationally-described-space-standard).
It is an area convention here, not a compliance claim. GIA includes the gym and
orangery; carport and open courtyard are additional.

## Rebuild

The script uses ReportLab and the locally available Arial fonts. In the current
Codex runtime:

```sh
/Users/sam/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 plan_model.py
```

Temporary page renders are under `tmp/pdfs/`.
