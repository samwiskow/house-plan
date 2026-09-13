# The courtyard house - Design book 01

Start with [the house design book](output/pdf/house-design-book.pdf).
The accompanying [fresh 3D model](viewer/index.html) uses the same measured
proposal. Serve this folder locally before opening the model; instructions are
in [viewer/README.md](viewer/README.md).

## Current set

1. The house brief and household priorities.
2. A furnished whole-house plan and clear room / area schedule.
3. Arrival, courtyard and garden elevations, with a current roof plan.
4. Two sections explaining the continuous shared vault and glazed garden room.
5. Shared-space palette and library character.
6. Bedrooms, bathrooms, office / guests and practical-room details.
7. Courtyard day / evening views and the comfort brief.
8. A short register of the decisions still open.

The 16-page landscape A3 PDF is the current presentation. Its full floor plan is
1:100 when printed at 100%. Other drawings are explanatory; use the full plan
and room schedule for dimensions. Images are captured from the new scene, not
from the older atmosphere images or viewer.

## Decisions carried forward

- Single-storey courtyard house, lower stone wings and a taller timber shared
  block. One continuous shared-room vault; the garden room remains open and
  glazed, with the main floor continuing through.
- Two adults and three children; occasional visitors bring the peak planning
  allowance to ten. Visiting children may share beds. Eight at the dining table
  plus two at the island is the current working interpretation.
- Parents-suite A, super king, two ensuite basins and generous shower. Three
  equally sized child rooms with small doubles where they fit. Family bathroom
  with a bath, separate generous shower and two basins.
- Library snug with TV provision and dark, full-height timber bookcases.
- One person using two permanent office setups, with occasional sofa-bed use.
- Side-by-side laundry appliances, useful storage and the full 4 x 6 m gym.
- Garden-side plant behind the gym, with internal and external access, is the
  current direction. The dimensioned room, equipment and rooflight remain a
  drawn proposal. The former family annexe and arrival projection are declined.
- Wet underfloor heating is confirmed. Active cooling and solar contribution
  are requirements. Two local MVHR systems are recommended for development,
  not selected; hot-water sizing and distribution remain open.

## Matters still open

The roof and ceiling heights are carried-forward study dimensions. The low
roofs are envelopes, without designed falls or drainage. The snug rooflight
replaces the covered side window but does not establish equivalent daylight.
Exact exterior material placement, weathering, floor and worktop products,
joinery and furniture are not fixed. Equipment locations, maintenance space,
family linen capacity, PV / battery / grid balance, actual site and budget need
further work. The book is a concept design, not a construction package.

## Sources and archive

`house_design_model.py` loads the checked concept 24 snapshot underlying the
concept 25 full plan. It checks its recorded source hashes and retains all three
office states. `viewer/export_model.py` derives the new scene directly from the
room polygons, wall gaps and measured openings; it does not import or reuse the
old viewer. `build_design_book.py` reads the same generated model.

Roof direction comes from 06B / 07B; courtyard and lighting from 09 / 10; room
studies continue through 24; services decisions through 26 / 27. All historical
PDFs and their source scripts remain available in `output/pdf/` and the older
working folders. They are supporting records, not competing current sets.

`output/design/design-book-manifest.json` records the model and image hashes for
this edition. No remote is configured in this repository; delivery is local on
`codex/house-design-book`.
