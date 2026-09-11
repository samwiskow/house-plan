# U-shaped family home - concept 05

The current floor-plan revision is `output/pdf/concept-07-open-garden-room.pdf`:
a full plan at 1:100 and a before/after corner detail at 1:50, both on A3.
It opens the year-round garden room and relocates the hall door beyond the snug.
Print at 100% to preserve scale.

`output/pdf/u-home-dimensioned-concept.pdf` retains the original concept 05 plan,
room schedule, family/service details and illustrative site plan. Its enclosed
orangery and hall arrangement are superseded by concept 07. Concept 04 remains
available in Git history.

## Current design development

[MATERIALS-BRIEF.md](MATERIALS-BRIEF.md) records the 11 September direction for
the single-storey house: a continuous shared-room vault and lower
stone wings meeting a timber family area, arrangement A, the shared-space palette
and the proposed log burner.
It distinguishes agreed choices from proposals and open decisions, and includes
the exterior and interior atmosphere studies. Concept 07 changes internal walls
and the hall door within the same external footprint.

## Concept 07B: glazed-roof transition

`output/pdf/concept-07b-glazed-roof-transition.pdf` develops the agreed shallow
extensively glazed roof, broad ivory-headed opening and continuous floor finishes.
It contains a 1:50 section through the garden sitting area and kitchen plus an
interior perspective from a 1.60 m eye height. The shared hall appears to the
right when looking towards the courtyard.

Glass roof heights of +2.85/+3.45 m, a 3.10 m opening head and the resulting
0.40 m band below the main ceiling are study targets, not final specifications.
The garden roof's sloping outline supersedes its earlier +3.20 m placeholder.
The agreed comfort brief includes insulating solar-control glazing, external
roof-shading provision, investigation of high-level motorised vents and a
whole-space winter/summer performance assessment. Performance is not yet verified.

`glazed_roof_study.py` independently creates the section and perspective;
`output/pdf/concept-07b-study-check.json` records levels and camera position.
Both A3 pages were rendered and visually checked, including view orientation.
This study does not change the concept 07 floor plan or demonstrate a post-free
structural solution. Rebuild with the Python runtime below.

## Concept 07: open year-round garden room and hall separation

`open_orangery_study.py` loads concept 05 geometry and drawing helpers without
executing its exports. It expands the garden sitting zone across the two former
wall strips, removes the internal sliding doors, and relocates the hinged door
across the 1.20 m guest hall at the office/snug boundary (plan y = 9.40 m).
The snug and visitor WC remain on the shared side. The office and guest rooms
remain beyond the door, with the existing office door retained.

The new hall partition is 120 mm thick; the proposed door is 900 mm wide and
opens toward the office. The garden-room connections are 4.00 m toward shared
living and 3.50 m toward the shared hall. These are intended open-edge dimensions,
not confirmed structural clear spans. Beams, bearings and a possible corner post
remain unresolved. The lower garden-room ceiling meets the higher shared vault;
opening the plan does not extend that vault into the garden-room roof.

GIA and footprint are unchanged. The garden sitting zone is 14.00 m2 including
former wall/threshold strips; circulation is recorded separately. Furniture is
unchanged. `output/pdf/concept-07-area-check.json` records the revised room areas,
nine checked routes and zero reported geometry issues. The checks also verify
that former wall positions are open and unrelated room polygons are unchanged.
Both A3 pages were rendered and visually reviewed. Rebuild with the same Python
runtime below, substituting `open_orangery_study.py` for `plan_model.py`.

## Concept 06B: continuous vault and lower wings (chosen direction)

`output/pdf/concept-06b-continuous-vault-low-wings.pdf` contains a roof arrangement,
two elevations with the earlier garden roof lines overlaid, and two located
sections. All three sheets are A3 at 1:100 when printed at 100%. The garden view
puts the gym on the left; the arrival view puts it on the right.

The continuous shared-room vault with lower stone wings and gym is the chosen
direction. Detailed heights and construction remain provisional. One pitched roof covers the rear block, with flat ceilings over the
pantry and service rooms. The garden-room roof remains a low volume reservation; concept 07 now opens
its internal connections and establishes year-round use.

This study tests a +3.70 m main roof edge, +5.32 m ridge and +3.20 m lower roof
envelopes. The shared ceiling rises from 3.50 m at the side walls to 4.91 m at
the apex. Wing/service ceilings are 2.60 m; the gym tests 2.70 m. These are
massing assumptions, not verified structural or equipment clearances. Roof depth,
low-roof drainage, abutments and the final eave height remain to be developed.

`concept_06b_study.py` reads the baseline outline, shared-room polygon and windows
without executing the accepted plan renderer. Run it with the Python runtime
below. `output/pdf/concept-06b-study-check.json` records roof coverage, shared-vault
continuity and orientation checks. All three pages were rendered and visually
reviewed. The original concept 05 floor plan and validation files remain unchanged;
concept 07 records the subsequent internal opening and hall-door changes.

## Concept 06 roof study (earlier proposal)

`output/pdf/concept-06-roof-elevations-sections.pdf` contains three A3 sheets:
a roof plan, garden and arrival elevations, and two located sections, all at
1:100 when printed at 100%. This is the first roof proposal over concept 05;
it does not replace the accepted floor plan or approve new heights/materials.

The study tests 30-degree main roofs with a +2.80 m wall-edge roof datum.
Different spans produce ridge levels of +5.17 m (family), +4.71 m (guest),
+4.42 m (shared room) and +4.73 m (gym), measured above the floor. The gym
ridge runs across the wing. The orangery tests a lower mono-pitch roof.

This study exposed the ceiling transition between the lounge and dining
area, leading to the continuous-vault preference now explored in 06B. Seasonal
versus year-round orangery use remains open. The orangery abutment,
gym roof step and valley drainage remain unresolved. Roof overhangs, rooflights,
structure, roof build-ups and the stove/flue are not specified in this study.
Existing window widths are retained; opening heights are proposals.

`concept_06_study.py` reads the outline and windows from `plan_model.py`
without importing or executing it. Run it with the same Python runtime below.
`output/pdf/concept-06-study-check.json` records roof coverage and ridge checks.
All three pages were rendered and visually reviewed. These are geometry and
presentation checks, not structural, site-specific or compliance verification.

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
- Year-round garden sitting area in the bottom-right courtyard corner, open
  to the shared hall and main living space. External sliding glazing opens to
  the courtyard. A door beyond the snug separates the office and guest hall.
- Indoor gym for a combined rack/cable station, barbell, bench, dumbbells and
  possible treadmill. Equipment footprints are illustrative; actual machine
  dimensions, use clearances and ceiling heights remain to be coordinated.
- Two household cars in a solar carport and an independent guest bay.
- Selected pocket doors are welcome where they improve circulation.

## Concept 05 measured baseline (concept 07 changes noted above)

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
is replaced by a proposed rooflight because the gym adjoins that wall. Garden-room heating, glazing, shading and ventilation need design for the
chosen year-round use. Concept 07 removes the internal separating doors. Bedroom daylight, courtyard privacy and roof drainage need a
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
