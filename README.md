# U-shaped family home - concept 05

The full floor-plan reference is `output/pdf/concept-07-open-garden-room.pdf`:
a full plan at 1:100 and a before/after corner detail at 1:50, both on A3.
It opens the year-round garden room and relocates the hall door beyond the snug.
Read it alongside concept 12, which adds the approved direct kitchen–utility
hinged door D19; that opening is not shown in the earlier full-plan export.
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

## Concept 19: everyday-use review

`output/pdf/concept-19-everyday-use-review.pdf` records 12 reproducible spatial
scenarios across laundry, shopping, cooking, school mornings, dining and bath
assistance. Open machine doors retain the sampled approach; a basket in the
laundry aisle blocks it. Open pantry drawers and dishwasher doors obstruct their
work routes; the existing direct kitchen and courtyard-side routes offer bypasses.
An occupied boot bench needs the gym-side bypass. A bath-assisting adult occupies
the bath approach. These are synthetic occupied-use reservations, not a simulation
of simultaneous household movement.

The current table has eight chairs. End-chair tests for ten obstruct both dining
cross-routes; no ten-at-one-table layout is adopted. Eight plus island seating
is separate seating. Concept 18's five-visitor sleeping example remains conditional
on child sharing and acceptance of the office sofa-bed exit compromise.

`household_use_review.py` and concept-19-study-check.json preserve both failures
and passing alternatives. Each scenario route passes without its temporary
obstacles; 0.70 m moving envelopes are checked against the obstacle additions.
`development_model.py` loads the concept 18 geometry / furniture snapshot and
rejects changed source files, avoiding regeneration of historical PDFs.

## Concept 18: office and overnight guests (proposal)

`output/pdf/concept-18-office-and-guests.pdf` develops the office day / night
layout and guest bedroom / shower on four A3 sheets. User confirmed an
occasional office sofa bed and that visiting children may share beds.
A five-visitor example is two in the guest double, two on the office sofa bed and one visiting child
sharing a child-room bed. This can include four adults and one child, subject
to sofa-bed comfort and its one-sided exit; it does not provide five adult beds.

The office retains a 2.60 x 0.75 m desk and adds a 2.00 x 0.90 m sofa reservation.
Its open envelope is 2.00 x 2.20 m, with a 1.40 x 2.00 m mattress allowance.
The desk cannot be used in night mode; the chair parks inside the room.
Only the entry side has a connected floor route out. A far-side sleeper must
cross the mattress. This compromise is explicitly awaiting review.
The guest double shifts to provide a 0.75 m narrower side and 0.90 m foot gap.
The guest shower proposal is 1.20 x 1.00 m with fixed glass, WC and 0.70 m vanity.

`office_guest_study.py` retains concept 15 and checks both furniture states;
concept-18-study-check.json records routes and limitations. Room boundaries,
doors and windows stay unchanged. Product mechanisms, occupied bathroom use,
window operation and accessibility are not validated.

## Concept 17: service-end comparison (proposal)

`output/pdf/concept-17-service-end-comparison.pdf` compares the laundry and a
northward extension of the existing gym block on four A3 sheets. Neither is
selected. A retains side-by-side machines and drying but reduces folding from
1.45 m to 0.65 m, removes sorting drawers and leaves the controls zone unresolved.
B preserves the laundry and full 4 x 6 m gym, testing a 4.70 x 2.60 m extension
(12.22 m2 added footprint) with a 4 x 2.25 m clear plant compartment and external
access. B is recommended for development, subject to site, roof and full package
coordination. Equipment and maintenance envelopes are planning allowances.

Both variants retain the 40 sampled house routes; B also checks three internal
plant approaches and clear maintenance reservations. These do not establish
occupied use, equipment replacement, performance or compliance. Keep the
concept 15 family-wing plant reservation and modest linen shelves meanwhile.
Rebuild with `service_end_study.py`; checks are in concept-17-study-check.json.

## Plant location: revised direction, 12 September 2026

The user declined the family-wing annexe in concept 16. Investigate the laundry
room and/or extending the existing gym block to accommodate plant at the service
end, away from bedrooms. Preserve the full usable gym; an extension is permitted
for investigation, not selected or dimensioned. Prefer continuing the existing
block and roof form to creating another separate annexe. A gym-block extension
still requires roof, structure and drainage coordination.

[SERVICES-BRIEF.md](SERVICES-BRIEF.md) records the known requirements, missing
household inputs and the comparison to develop. Confirmed: two adults and three
children, with an upper planning allowance of five overnight guests (ten total). Design for two simultaneous
high-flow rain showers, mandatory active cooling powered by solar, and preferably
side-by-side washer / dryer. Cool all bedrooms, shared / garden room, office,
snug and gym. The PV / battery / grid energy balance remains open. The utility is already fitted
with separate washer / dryer bays, sink, sorting, folding and air-drying space;
plant there requires a tested rearrangement. A gym-block extension may preserve
both functions, but added footprint, access, acoustics and distribution routes
remain untested. Check the longer hot-water route to the family bathrooms.

`output/pdf/concept-16-plant-and-linen.pdf` is a historical, declined location
study. It illustrates a 6.89 m2 family-wing annexe and conditional 2.00 x 0.55 m
linen shelving; neither is adopted. Its original 40 house-route and two annexe
approach checks apply only to that old scenario. Existing house geometry and
full gym furniture were retained. The PDF is preserved as history; the study
JSON and builder status record the rejection. Continue using concept 15's plant
reservation until a service-end arrangement is designed and accepted. Do not
load concept 16's cleared ST furniture as the latest adopted layout.

## Concept 15: children's rooms, family bath and linen (proposal)

`output/pdf/concept-15-family-bedrooms-bath-linen.pdf` contains four A3 sheets:
a family-wing plan at 1:50, mirrored bedroom details at 1:30, a bathroom plan
at 1:20 and linen / plant plan with shelving elevation at 1:20.
The user confirmed **small double beds where they fit** and a family bathroom
with **a bath, separate generous shower and two basins**.

Each 3.03 x 4.22 m child room (12.79 m2) gets the same furniture allowances:
a 1.20 x 2.00 m mattress in a 1.35 x 2.10 m frame, a 1.80 m wardrobe at 0.66 m
depth, a 1.40 x 0.65 m desk and a 0.65 m-square chair reservation. Beds turn
across the far end with their heads at the external wall. C1 / C3 share the
layout and C2 mirrors it. Desk height, chair size, sill / window operation,
blackout, fixings and actual bed frames still require selection.

The 3.03 x 2.68 m family bathroom fits a 1.70 x 0.75 m bath, a separate
1.20 x 1.20 m shower zone, a 1.40 m double vanity and WC. Move D03 north from
y=4.80 to 5.05 m, retaining its width and swing, to clear the vanity. No room
polygons or windows change. The shower window needs privacy, waterproofing
and hardware coordination. Fixed glass is checked as an obstacle; the shower
floor is walkable. Bath assistance, occupied use, actual enclosures, plumbing,
electrical zones, drainage and construction compliance are not validated.

The linen / plant store retains its existing 0.85 x 0.85 m plant placeholder.
A 0.90 m-wide, 0.45 m-deep linen unit has five proposed shelf levels, keeping
the door swing clear. This is modest provision for five bedrooms. The plant
footprint is not a selected or sized equipment package: service / replacement
clearances, cylinder, ventilation unit and pipework may change usable storage.
No relocation of equipment into the utility is assumed.

`family_rooms_study.py` loads selected parents-suite A before the rejected B
alternative, retaining the snug and kitchen–utility D19. It replaces furniture
only in C1 / C2 / C3 / FB / ST and moves D03. All 40 sampled routes and room-door
sweeps pass at the existing 0.70 m envelope, with desk chair reservations present.
These are footprint / approach checks, not occupied-use or accessibility tests.
All four pages were rendered and visually reviewed. The proposal is recorded
in `output/pdf/concept-15-study-check.json`.

## Concept 14: parents' suite (proposal)

`output/pdf/concept-14-parents-suite.pdf` contains four A3 sheets: the suite
plan at 1:40, bedroom / wardrobe elevations at 1:25, an ensuite detail at 1:20
with elevation at 1:25, and an alternative suite plan at 1:40.
The user confirmed a **180 x 200 cm super king** and clarified that **two basins
and a generous separate shower matter more than an ensuite bath**. Both options
retain those priorities. The user selected Option A and declined the bath
alternative because of its dressing-room compromises. The four-page comparison
PDF is retained as the decision reference.

The bed turns onto the solid north wall, away from the south window. Its
1.95 x 2.15 m frame allowance leaves 0.80 m east, 1.45 m west and 1.75 m at the
foot before furniture / door use. Bedside units clear the room-door sweep.
The head wall backs onto the family bathroom: coordinate services and sound
isolation. Actual frame, blinds, finishes and lighting remain to specify.

**Option A is selected:** retain the existing rooms, with a compact 1.20 m
double vanity, WC and a 1.10 x 1.78 m shower zone. A 0.88 m fixed screen leaves
a 0.90 m entry. The dressing room has 3.00 m of hanging storage at 0.66 m overall
depth and a 2.10 m shallow drawer / folded-clothes run at 0.35 m depth, leaving
1.09 m between closed fronts. The wardrobe pocket cavity stays reserved.

**Option B adds a bath:** move the partition 0.70 m into the dressing room,
raising ensuite area from 5.66 to 7.89 m2. It fits a 1.70 x 0.75 m bath,
1.20 x 1.00 m separate shower and 1.20 m double vanity. The dressing room drops
from 6.68 to 4.45 m2, with 2.60 m hanging storage, no shallow drawer run and a
0.74 m aisle. Replace P01 with relocated hinged D20 opening into the bedroom.
These changes are an alternative only; the external walls and windows remain.
The shower approach is only about 0.75 m deep, leaving little tolerance.

`suite_study.py` loads concept 13 without regenerating older exports. It checks
25 routes for A and 26 for B using the existing sampled 0.70 m envelope, with
fixed shower screens as obstacles and shower floors walkable. Both route sets
and door / furniture sweep checks pass. These checks do not establish occupied
use, actual frame / fixture tolerances, drawer operation or construction and
accessibility compliance. Waterproofing, drainage, the wet-zone window,
ventilation and bathroom electrics require design. All four pages were rendered
and visually reviewed. `output/pdf/concept-14-study-check.json` records A and B;
its default furniture proposal is A, retaining D19 and the concept 13 snug.

## Concept 13: snug (proposal)

`output/pdf/concept-13-snug.pdf` contains a furnished plan and two full-wall
interior elevations at 1:25 on A3. The user confirmed **TV and films, with room
to read**; this supersedes the earlier reading / play emphasis for this room.
The clear room remains 4.58 x 2.60 m (11.91 m2), retaining its west-facing
window, room door and separation from the office / guest hall.

Propose a 2.30 x 0.90 m sofa opposite 2.70 m of shallow storage, a movable
0.50 m footstool and a small side table. A centred 55-inch screen is illustrated
as a dimensional allowance, with its centre around 1.00 m high and an estimated
2.0 m seated viewing distance; actual sofa posture, TV and mount need selection.
Storage is 0.30 m deep with a 0.55 m-high base and side shelves. Keep cabling
accessible and equipment ventilated. A recess blind controls window light;
selected window / blind hardware still needs checking.

Local lighting separates film, reading and general use: dimmable storage-wall
ambient light, two reading lights and a general ceiling light whose position
is open. Warm ivory, honey oak and bronze carry through; an olive / moss sofa
and fitted wool-rich carpet are proposals for review, not selected finishes.

`snug_study.py` loads concept 12 without regenerating its outputs, retains D19,
and replaces only snug furniture. All 19 sampled routes pass with a 0.70 m
envelope, including access to the sofa and window with the footstool present.
Room-door swings clear furniture; room / door / window geometry is unchanged.
The storage-to-sofa gap is 1.35 m; the parked footstool leaves a 0.80 m passage.
These are footprint checks, not checks of occupied seating, joinery hinges,
window swings, acoustic performance or lighting output. The two PDF pages
were rendered and visually reviewed. The proposal is recorded in
`output/pdf/concept-13-study-check.json`.

## Concept 12: arrival, storage and utility (proposal)

`output/pdf/concept-12-arrival-storage-utility.pdf` contains four A3 sheets: a
furnished plan at 1:50, boot-room / hall elevations, utility elevations and
pantry elevations. Elevations are 1:25 except the hall cupboard at 1:40. The
room polygons and shared-room furniture remain unchanged. D19 adds an approved
0.80 m opening allowance directly between kitchen and utility, hinged at its
north end to open back into the utility. Boot-room access is retained. Final
frame dimensions, clear passage and the head / ambient-light junction need design.
Investigate a solid-core doorset with perimeter and suitable bottom seals;
coordinate ventilation transfer. No acoustic performance rating is established.

- Boot room: 1.10 m closed coat / bag storage, a 1.85 m oak bench with three shoe
  bays and five staggered hooks for wet coats. Keep the laundry pocket cavity
  clear. The bench is outside the room-door sweep.
- Entrance: a 0.90 m visitor-coat cupboard and a 0.60 m-long, 0.28 m-deep keys
  ledge with mirror above. Sliding cupboard fronts are proposed; actual usable
  hanging depth and hardware need checking.
- Utility: the user confirmed separate washer and dryer plus some air-drying
  space. Reserve two 0.65 m appliance bays, a sink and sorting drawers along the
  3.15 m wall. Use 0.75 m depth including connection space. The return has a
  0.70 m ventilated hanging-cupboard reservation and 1.45 m folding counter.
  Drying airflow and capacity are not established; this is modest provision.
- Pantry: 0.60 m-deep counter / drawers on one end wall and 0.40 m food shelving
  on the other, leaving a 1.60 m aisle. Keep both side walls clear for the pocket
  doors. Upper counter shelves are 0.30 m deep. No extra sink or fridge is assumed.

`arrival_study.py` reads the current shared-space model without regenerating
earlier exports, replaces furniture only in H / B / L / PA and adds D19 for this study.
It records 12 furniture reservations in `output/pdf/concept-12-study-check.json`.
All 17 sampled routes pass at a 0.70 m envelope, as do room-door sweep checks
against furniture. Repeating with both 0.55 m machine-door projection rectangles
and the fully open D19 leaf also passes; the leaf is excluded from testing against
its own swing. The narrow utility aisle is 1.48 m closed and 0.93 m behind those
open reservations; the folding return has 1.03 m and is treated as a one-person
work zone. Drawers and baskets occupy circulation during use.

These checks do not validate selected appliance hinges, joinery-door operation,
two-person use, accessibility compliance or manufacturing tolerances. Machine
models, connections, extraction, noise, drying airflow and cabinet fixings remain
to specify. A Bosch dimensional reference is linked in the PDF only to explain
why door-open depth matters; it is not an appliance selection. The four pages
were rendered and visually reviewed. Rebuild with the Python runtime below,
substituting `arrival_study.py`.

## Concept 11: year-round comfort (proposal)

Working site assumption: Northumberland, England, with the courtyard opening due
south. On the retained plan, south is up, north down, east left and west right.
The shared-room courtyard glazing and garden-room front face south; the garden
side window faces east and family-wing courtyard windows face west. This
supersedes earlier notes that no compass orientation had been assigned. The
exact plot, altitude, exposure, horizon and weather file are still unknown.

`output/pdf/concept-11-year-round-comfort.pdf` contains three A3 sheets: a comfort
plan at 1:100, a roof / shade / ventilation section at 1:50 and seasonal operating
diagrams. It retains the measured walls, openings, roof heights, furniture and
selected courtyard layout. The lighting direction is now supported by the user;
fixture specifications and technical performance remain open.

- Reserve retractable external shading over the glazed roof and screens for
  south-facing sliders and the east garden-room side window. Retain insulating
  solar-control glass, with whole-unit performance and appearance to specify.
- The roof shade stops at plan y = 11.85 m, before two high vent reservations at
  y = 12.10-12.60 m. The approximately 0.95 m upper strip remains unshaded in this
  option and must be included in solar modelling. Plan separation is verified;
  cassette, frame, opening sweep, weathering and low-pitch compatibility are not.
- Investigate south-to-north purge openings and high-level exhaust, with a
  designed secure inlet for night use. Door opening is an attended option.
  Air arrows illustrate a possible route, not a wind or airflow calculation.
- Develop wet underfloor heating for a heat-pump design, coordinating the garden
  and shared-room loops and excluding fixed joinery / hearth. Assess winter
  comfort near glass before deciding whether another emitter is needed.
- Study whole-house MVHR for background fresh air separately from summer purge.
  Plant, manifolds, duct sizes and terminal locations are not selected. Coordinate
  service / hall ceiling routes with the vault, roof head and ambient lighting.

`comfort_study.py` builds this independently. Its JSON records orientation,
non-overlapping roof reservations and the retained clear routes. The illustrative
solar-noon angles use 55.2 N as a representative latitude, not a plot coordinate:
58.2 degrees in summer, 34.8 at equinox and 11.4 in winter. No shade duration or
indoor temperature follows from those angles. All three pages were rendered
and visually reviewed.

Next technical work: site-specific year-round thermal modelling of the connected
interior and bedrooms, room-by-room heat loss, usable ventilation areas, and
supplier coordination of roof shading / vents. Use appropriate current and future
weather data and confirm applicable regulations. No heating or cooling capacity,
airflow, overheating or compliance result is claimed. Source links are in the PDF.
Rebuild with the Python runtime below, substituting `comfort_study.py`.

## Concept 10: lighting and evening scenes (direction supported)

`output/pdf/concept-10-lighting-scenes.pdf` contains three A3 sheets: a lighting
plan at 1:100, scene and control settings, and an evening view from dining toward
the garden room and courtyard. It retains the current furniture and house geometry.

- Six adjustable kitchen spots provide a separate task-light group. Four concealed
  linear runs soften the shared-room edges; their ledges and maintenance access
  need coordinating with the vault.
- Keep the single dining chandelier, two lounge lamps and a garden-room reading
  light on a solid pier. No lighting is fixed to the glazed roof.
- Add three concealed ambient wall runs along the pantry face and WC approach,
  on a separate group retained in every shared-room scene. Pantry shelf and WC
  mirror lights have independent local switches.
- Four bronze courtyard pillars replace the outdoor table lamps.
  The study reserves 0.18 m square bases and 0.75 m height, spaced beside
  the routes and seating with recessed downward light. Retain two low threshold
  lights and one manual indoor garden-room table lamp.
- Add seven broad downward wall lights around the courtyard, following the user's
  numbered markup: W1-W4 on solid family-wing wall sections and W5-W7 on the guest
  return. Propose 2.00 m mounting height and a separate ambient dimmer. These add
  light across paving and seating alongside the pillars; overlapping coverage
  remains a design target. Check bedroom-window spill and planting shadows with
  actual fittings. No dedicated planting uplights are proposed.
- Wall controls at the entrance hall, family-hall approach and dining slider recall
  Everyday, Entertaining and Quiet evening. Keep local reading controls, labelled
  lamp outlets and independent pillar / wall-light dimming at the dining slider;
  no app is required. The revised interior ambient direction is supported.

Scene percentages are starting dimmer settings for commissioning, not calculated
light output. Outdoor scenes apply after dark while the court is in use, with a
proposed 60-minute auto-off extendable at the slider control. Groups express the
control intent, not final wiring circuits. Proposed colour temperatures are 2700 K
inside and 2200-2700 K outside, subject to actual fittings and samples.

`lighting_study.py` reads the current shared-space geometry and concept 09 JSON
without regenerating earlier exports. It records 33 light locations, eight
scene groups plus local task lights and one indoor portable, and three controls in
`output/pdf/concept-10-study-check.json`. Scene coverage and value ranges pass;
the 13 existing indoor route checks also pass with the floor-lamp base reserved.
The four pillar bases stay inside the courtyard and clear of planting, furniture
in both chair positions, and the four retained routes with their 1.00 m envelopes.
Pillar spacing and output are proposals, not verified lighting coverage.
All seven wall-light positions avoid the measured window spans; their light
distribution, mounting details and courtyard uniformity are not validated.
All three PDF sheets were rendered and visually reviewed.

The evening view illustrates colour and mood using approximate falloff. It does
not establish lux levels, glare, reflected glass, shadows, ecological performance
or electrical compliance. Beam selection, output, dimming compatibility, mounting,
outdoor ratings and spill require testing with actual fittings. Outdoor intent
follows the [DarkSky / IES principles](https://darksky.org/resources/guides-and-how-tos/lighting-principles/).
Rebuild with the Python runtime below, substituting `lighting_study.py`.

## Concept 09: courtyard layout selected; elevations in development

`output/pdf/concept-09-courtyard-elevations.pdf` contains a furnished courtyard
plan at 1:75 and coordinated garden / courtyard return elevations at 1:100,
on two A3 sheets. This develops the exterior around the current shared-space
study without changing any house walls, room polygons or opening widths.
The courtyard layout was selected on 12 September; technical details and exact
materials, planting and facade treatments remain open.

- Keep the 4.00 m strip beside the garden room clear as the route from shared
  living. A connected landing serves the existing dining and garden-room sliders.
- Put a 3.00 x 1.00 m outdoor table in the wider court, with four chairs per
  long side. Circulation passes on the guest-wing side, outside the seating.
- Add a separate pad toward the garden, beside the guest wing's solid return,
  with a 2.20 m sofa, one chair and a low table.
- Test a 0.75 m family-side planting band beyond a 0.35 m wall-side strip.
  Proposed maintained heights are 0.90-1.20 m beside dining, lower near the
  garden mouth. Planting filters views; species, mature dimensions, window
  privacy and daylight performance have not been established.

Paving totals 50.78 m2 of the 88.40 m2 open court. The remaining 37.62 m2 covers
soft landscape and wall-side strips. This increases paving from the earlier
rough 38 m2 allowance to accommodate the two seating areas and connecting paths;
no site-wide landscape scheme is implied.

The garden elevation correctly mirrors the plan: gym left, family wing right.
Three return elevations show the family windows, largely solid guest return
and the garden room's shallow glazed roof. Main eave/ridge, low-wing roof and
glass roof heights follow concepts 06B/07B. Existing opening widths stay fixed;
window heights, bronze frames, timber/stone distribution and edge details are
proposals. Two-panel sliders are illustrated with a target of at least 1.20 m
clear after framing, subject to system selection. Door passage is not validated.

`courtyard_study.py` reads the current shared-space model without running its
exports. It checks outdoor furniture containment, overlap and planting conflicts,
paving containment and area, and four routes with a sampled 1.00 m envelope.
All four routes pass with outdoor dining chairs in their normal positions and
pulled out 0.40 m. These routes stop outside the door faces and do not validate
threshold levels, accessibility or actual sliding-door clear widths. The JSON
`output/pdf/concept-09-study-check.json` records dimensions, route checks and
orientation assertions. Both sheets were rendered and visually reviewed.

Concept 11 now assumes a south-facing courtyard in Northumberland. Sunlight,
wind shelter, planting selection, privacy, drainage,
roof junctions and surface / threshold specifications remain unresolved.
Rebuild with the Python runtime below, substituting `courtyard_study.py`.

## Concept 08: coordinated shared-space study (proposal)

`output/pdf/concept-08-shared-space.pdf` contains an enlarged furnished plan at
1:50 and two interior perspectives on three A3 sheets. This is a new proposal
for review, retaining the concept 07 room polygons, openings and footprint.
It does not replace the agreed room arrangement or approve new products.

- The 2.80 m sofa retains its position. The dining table turns 90 degrees and
  grows to 3.00 x 1.00 m, with four chairs along each long side and none at the
  ends. Its centre and the chandelier position are retained. The media
  unit shortens to 2.20 m, the north armchair moves, and a 1.35 x 1.50 m hearth
  zone reserves the family-wing end for a stove. These are spatial allowances,
  not validated hearth dimensions, combustible clearances or TV heat protection.
- The 2.80 x 1.05 m island shifts 0.45 m toward the rear counter, with three
  stools on its garden side. The cooking aisle is 1.45 m. An island hob is
  proposed; extraction, ventilation and its proximity to seating need design.
- A 2.80 m rear base run allocates 1.00 m drawers, 0.80 m sink base, 0.60 m
  dishwasher and 0.40 m bins. Two 0.60 m towers reserve ovens and fridge/freezer.
  Cabinet fillers, chosen appliance dimensions and full operating envelopes
  are not resolved. The kitchen window retains its width and tests a 1.12 m sill.
- The garden sitting area tests a 1.80 x 0.85 m sofa, one 0.85 m chair and a
  0.60 m table. It retains the open hall connection and a central approach to
  the existing sliding-door opening. The actual sliding system's clear opening
  has not been validated.

`shared_space_study.py` loads the concept 07 model without running its exports.
The same furniture coordinates produce the plan and both depth-rendered views.
All 13 nominated routes pass the existing sampled 0.70 m envelope check,
including the added route around the rear table end. All 13 also pass with
all eight dining chairs pulled out 0.35 m. The 0.75 m seat pitch gives four
places per long side. Gaps from chairs to island and sofa are 1.55/1.70 m
normally and 1.20/1.35 m with chairs pulled out. The clear table-end gaps are
1.05 m toward the courtyard and 0.85 m toward the rear wall. These measured
allowances remain subject to the chosen table, leg positions and chair sizes.
A provisional 0.60 m appliance-door projection leaves 0.85 m of kitchen aisle;
this is not proof of comfortable simultaneous use or accessibility.

`output/pdf/concept-08-study-check.json` records furniture, camera positions,
clearances, checks and limits. All three A3 pages were rendered and visually
reviewed, including camera orientation. Stove installation, roof structure and comfort
remain unverified. Views show study proportions and colours, not photorealistic
materials or lighting performance. Rebuild using the Python runtime below,
substituting `shared_space_study.py`; this renderer also uses NumPy and Pillow.

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
- Large open kitchen/dining/living area and an enclosed TV / reading snug at
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
