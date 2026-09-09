# U-shaped family home - concept 04

The current dimensioned study is `output/pdf/u-home-dimensioned-concept.pdf`.
It has three A3 pages: a 1:100 floor plan and area schedule, 1:60 enlarged
details, and a 1:200 illustrative site plan. Print at 100% to preserve scale.

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
- Boot room connects to the entrance hall, pantry and separate laundry.
  Pantry also connects directly to the kitchen; entrance hall has its own
  kitchen route.
- Two household cars in a solar carport, an independent guest bay, and a
  possible detached exercise studio.
- Selected pocket doors are welcome where they improve circulation.

## Measured outcome

- Internal area: 279.81 m² against the 280 m² schedule.
- External footprint: 317.12 m²; outer dimensions 22.80 × 18.40 m.
- External walls assumed 350 mm; internal partitions assumed 120 mm.
- Shared kitchen/dining/living: 75.49 m².
- Children: 12.79 m² each, with clear internal dimensions 3.03 × 4.22 m.
- Parents' sleeping room: 16.80 m²; guest room: 17.12 m² including wardrobe recess.
- Entrance hall: 9.00 m². Other circulation: 26.80 m², above the 24 m² allowance.
  The family corridor is 8.56 m long; the guest corridor is 11.16 m long.
  Both are 1.20 m wide; an additional shower lobby is included in circulation.
- Courtyard recess: 8.00 × 12.80 m / 102.40 m², with approximately 52 m² paved.
- Illustrative plot: 35 × 45 m / 1,575 m². This is a test rectangle, not a
  minimum plot specification or a finding that any real plot is buildable.
- Carport clear allocation: 6.80 × 6.20 m. A provisional 7.20 × 6.60 m roof
  envelope keeps columns outside the clear allocation. Guest bay: 3.20 × 6.00 m.
- The initial 21 m² internal-partition allowance became 12.62 m² for partitions
  and doorway thresholds. That accounts for most of the extra room and
  circulation area while keeping the overall target. Thicker acoustic or
  structural walls could change this balance.

## Verification and limits

`plan_model.py` is the editable geometry and drawing source. The generated
`output/pdf/area-check.json` records room areas and checks. Geometry is in metres;
room areas include fitted joinery footprints. Net room polygons plus residual
internal partitions/thresholds reconcile to the internal area.

The model checks room overlaps, furniture containment and overlaps, declared
door connections, conflicts between pocket reservations and other openings,
hinged door sweeps against furniture, and a sampled 0.70 m walking envelope on
five nominated routes. The current run has no reported conflicts. The PDF was
rendered and all three pages visually inspected.

These checks do not certify building-regulations compliance, accessibility,
acoustics, structural spans, roof design, fire escape, drainage, ventilation,
or actual vehicle turning. The 6 m manoeuvring apron is a space reservation;
chosen vehicles still need a swept-path test. Pocket-door kit dimensions,
wall build-ups, cabinetry and plumbing require detailed coordination.

The GIA convention follows the internal-face definition in England's
[nationally described space standard](https://www.gov.uk/government/publications/technical-housing-standards-nationally-described-space-standard/technical-housing-standards-nationally-described-space-standard).
It is used here as an area convention, not as a compliance claim.

## Rebuild

The script uses ReportLab and the locally available Arial fonts. In the current
Codex runtime:

```sh
/Users/sam/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 plan_model.py
```

Temporary page renders are under `tmp/pdfs/`.
