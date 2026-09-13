# Courtyard house: services brief

13 September 2026 · Current requirements and system recommendations

This brief defines performance and space requirements. It does not select
plant capacity, products or an installation layout.

## Concept 26: underfloor preference and coordinated systems

On 13 September the user confirmed **underfloor heating for everyday winter
comfort**. The recommended architecture is wet UFH plus a cylinder served by
an air-to-water heat pump, with independent air-to-air cooling for the wings.
This normally adds an air-to-water outdoor unit to the two starting cooling
units; shared-space capacity / connections may require further cooling equipment.
No final outdoor count, capacity, cylinder volume or product is selected.

Develop two balanced MVHR systems as the first routing study, compared against
one central system with a proven cross-house duct section. The two-system
approach would need an accessible acoustic cupboard on the family side, likely
using some of ST. This is a proposal with a linen-space and bedroom-noise trade-off,
not household approval to return plant to that wing. Central MVHR keeps its
main equipment at the service end but still needs supply and extract routes.

Start hot-water design with one correctly sized service-end store; compare
insulated direct distribution with a controlled return. A local family store
remains a fallback. Two 16 L/min showers for ten minutes use 320 L mixed water;
an illustrative 55 C store / 10 C cold / 40 C mixed calculation gives 213 L
ideal hot draw before unusable volume, losses or recovery. This does not select
a 213 L or 230 L cylinder. Supply pressure / flow and repeat guest use matter.
The temperatures are arithmetic assumptions, not specified control setpoints.

See `output/pdf/concept-26-heating-hot-water-and-ventilation.pdf` for the four-page
comparison, room duties, demand examples and primary sources. Its JSON records
transparent formula results and the unchanged concept 25 geometry reference.
The next spatial pass should compare ventilation cupboards and route sections,
then coordinate plant access, the rear roof, snug rooflight and outdoor units.

## Revised direction: garden-side plant and separate wing cooling

The arrival-side plant projection in concept 17 B is declined. Concept 22 tests
an extension behind the gym, toward the garden / south (up on the plan), with
internal access through the gym and a separate external service door. It adds
13.05 m2 net footprint and gives 4.00 x 2.65 m clear plant space. Existing room
polygons remain unchanged. The rack and dumbbells move; D18 shifts 0.60 m to
clear them. Treadmill / bench positions and all equipment body sizes are retained.
The provisional treadmill rear reservation remains clear. Exercise movement,
barbell handling and selected equipment clearances still need verification.

The extension covers the snug's west window. Concept 22 replaces it with a
1.10 x 1.10 m rooflight reservation. Concept 24 updates the snug furniture. Blackout, daylight,
solar gain, opening / controls, roof structure, drainage and noise need design.
This is a proposal, not a selected rooflight or a claim of equivalent daylight.
The new plant leading edge is 0.25 m beyond the office window's plan extent;
roof edges, daylight and shading at that window require coordination.

Cooling direction: separate multi-split systems for the family and guest / service
wings. Each closed room needs suitable delivery; the shared / garden space is a
separate load and control zone whose outdoor-system allocation remains open.
Two outdoor units are a starting idea, not a sized equipment count. The prior
cross-vault cooling duct band is no longer assumed. Refrigerant, power and
condensate routes remain to design. MVHR / fresh-air ventilation is separate and
its distribution is unresolved.

Ordinary air-to-air systems usually do not provide tap water; combined products
exist. Compare a service-end cylinder / separate heat pump with a combined
system against the two simultaneous rain-shower requirement. Local family-side
storage is a fallback with space and maintenance costs. Hot-water pipes may use
floor / service construction, subject to build-up and routing design. Wet underfloor heating is now the confirmed winter preference;
concept 26 develops the associated heating and hot-water architecture. No capacity or performance result is claimed.

See `output/pdf/concept-22-garden-plant-and-wing-services.pdf` (six A3 pages),
`garden_plant_study.py` and concept-22-study-check.json. All 54 sampled routes,
room-door sweeps and the new routes around the open internal plant door pass.
The existing family plant placeholder remains until relocation is accepted
and the complete package is sized. The old arrival-side study is historical.

## Established requirements

- Working location: Northumberland; courtyard faces south. Actual plot unknown.
- Single-storey courtyard house with parents' suite, three children's rooms
  and a guest bedroom. Regular household confirmed: two adults and three children.
  Visiting family may include grandparents, aunt, uncle and cousins. The user
  estimates four or five overnight guests: use five as the upper planning
  allowance, ten people total, rather than assuming ten permanent residents.
  On 13 September the user agreed to an occasional office sofa bed and visiting
  children sharing beds. The five-guest example is two people in the guest room,
  two in the office and one visiting child sharing a child-room bed.
  Do not interpret this as provision for five adult guests.
- Open, year-round garden room with extensive roof glazing; continuous shared
  room vault and lower wing roofs. Protect usable ceiling heights and roof form
  when developing ducts and pipe routes.
- Parents' ensuite: two basins and generous shower; ensuite bath declined.
  Family bathroom: bath, separate generous shower and two basins. Guest shower
  room remains in the plan. High-flow rain showers are preferred; two showers
  must run comfortably together. Actual flow rates, duration, bath overlap and
  supply performance remain to establish before sizing equipment.
- Laundry: separate washing machine and dryer, some useful air-drying space,
  direct hinged kitchen door D19 and retained boot-room access. Prefer side-by-side
  machines; stacking is a fallback the user would consider, not the default.
- Keep the full usable gym: currently 4.00 x 6.00 m clear, with existing equipment.
- Locate plant toward the laundry / gym end, away from bedrooms. The concept 16
  family-wing annexe is declined. The dedicated linen gain is not yet secured.
- Earlier comfort studies propose heat-pump heating, wet underfloor heating and
  whole-house MVHR, with external shading and summer ventilation. These remain
  systems to develop; capacities and products have not been selected.
- Active cooling is a firm requirement, with solar PV intended to power it.
  Cool all bedrooms, the shared / garden room, office, snug and gym. Assess
  daytime solar use and evening / overnight demand; battery provision, grid contribution and the
  extent of solar coverage are not selected or demonstrated.
- Solar carport appears in the existing brief; array size, battery and charging
  provision are not established. A local log burner remains a proposal.

## Remaining household inputs

| Input | What remains to establish | Why it changes the design |
| --- | --- | --- |
| Shower usage detail | Rain-shower flow rates once fittings are shortlisted, typical shower duration and whether bath filling must overlap. Two simultaneous showers are already required. | Incoming water, cylinder storage and recovery performance. |
| Laundry and comfort detail | Everyday air-drying volume, room temperature preferences and night-time use. Side-by-side appliances are the preferred starting point. | Useful laundry space and heating / cooling operation. |

The household, peak guest allowance, two-shower requirement and room coverage
are sufficient to start the comparison. Remaining usage details can follow as
fittings and layout options become visible; do not ask again whether cooling
is required or which of the listed rooms to include.

## Information useful when available

- Actual plot / address, survey, boundaries, levels, access, neighbouring windows
  and intended position of the service side of the house.
- Mains water or private supply; drainage connection or private treatment.
  Pressure / flow, electrical service capacity and connection details are for
  the relevant designer or utility to establish, not guesses for the household.
- Solar array opportunities, battery preference, acceptable grid contribution,
  number of EV charging points, any backup-power expectation and other substantial
  loads. Solar-powered cooling is required; the energy balance is still to model.
- Budget priority: lower initial cost, low running cost, quiet operation,
  resilience and low maintenance; note any firm budget ceiling when known.
- Any ventilation or controls preferences: filter access, local manual controls,
  app use, noise sensitivity and whether windows may be open overnight.

Unknown site and supply details do not prevent a preliminary comparison, but
must remain explicit assumptions rather than settled design inputs.

## Historical location comparison: concept 17

The measured comparison is now in
`output/pdf/concept-17-service-end-comparison.pdf`. A retains side-by-side
machines but loses sorting drawers and reduces folding to 0.65 m. B tests a
12.22 m2 extension of the gym block with 9 m2 clear plant space, preserving the
full gym and laundry. B was recommended at that stage and is now declined. Both use
provisional equipment / service allowances; neither is a sized installation.

`output/pdf/concept-21-building-coordination.pdf` adds candidate distribution
routes and a section of the unresolved crossing to the family wing. A visible
services band is a proposal for review. The example hot-water route is 35.25 m
in plan before verticals and fittings. No thermal or hydraulic result follows.

### Comparison criteria retained

| Option | What the current plan tells us | What the measured study must test |
| --- | --- | --- |
| Reconfigure laundry within current footprint | The utility already has washer / dryer bays, sink, sorting drawers, a 1.45 m folding counter and a 0.70 m hanging cupboard. It has no verified spare plant compartment. | Start with side-by-side appliances and useful drying / folding provision; compare stacking only as a fallback. Test actual equipment access, doors, routes and noise toward the snug. |
| Extend the gym block for a separate plant compartment | Utility and gym are adjacent at the service end. An enlarged block could retain the existing 24 m2 gym and fitted utility. No extension direction or dimension is selected. | Added footprint, continuous roof / drainage strategy, external and internal access, equipment replacement, gym windows / equipment, boundary and outdoor-unit siting. |
| Split equipment between the two | This is permitted by the user's laundry and/or gym direction, but no split is selected. | Whether it improves the two layouts enough to justify extra connections and maintenance locations. Do not force every manifold or ventilation component into one room. |

Moving the cylinder to this end increases separation from the family bathrooms.
The designer must compare actual pipe lengths, hot-water waiting time, insulation
and any circulation strategy, including its energy and control implications.
Plant next to the utility still needs acoustic coordination with the snug. A
continuous gym-block extension simplifies the architectural concept, but does
not remove roof, structure or drainage design work.

## Information and outputs for the design team

1. Confirm wall, floor, roof and glazing build-ups, airtightness target, shading
   and intended room temperatures; calculate room-by-room winter heat loss.
2. Establish hot-water demand, incoming supply performance, cylinder recovery
   and distribution requirements before selecting storage and heat-pump capacity.
   Test two simultaneous high-flow rain showers for the household of five plus
   up to five overnight guests (ten people total at peak). Do not retain the old
   300-litre reference as a selected size; account for shower pressure / flow and repeat-use recovery.
3. Calculate cooling loads for all bedrooms, shared / garden room, office, snug
   and gym, and design active cooling as a requirement. Retain shading to reduce loads. Compare suitable cooling emitters
   or dedicated air-conditioning; do not assume the earlier UFH / MVHR proposal
   provides the required cooling. Coordinate condensate, humidity, acoustic
   performance, distribution space and equipment access.
4. Model solar generation against cooling and other electrical loads, including
   evening / overnight use. Compare battery and grid contributions; agree the
   intended solar coverage before claiming cooling can run entirely on solar.
5. Develop ventilation supply / extract duties, duct routes, silencers, air
   terminals, condensate drainage and filter / replacement access. Test routes
   against the vault and lower wing roofs before assuming usable ceiling space.
6. Coordinate the complete indoor and outdoor package, maintenance clearances,
   floor loads, drainage, acoustics, electrical supply and local distribution
   points. Provide a dimensioned plan and section, not equipment body sizes alone.
7. Compare the utility and enlarged-gym layouts with the same household brief,
   identify functional compromises and show the effect on linen storage.

## Guidance informing this brief

Room-by-room heat loss is the basis for heating design, rather than a heat-pump
size inferred from the floor plan alone. See [Energy Saving Trust: heat-loss
calculations](https://greenheattoolkit.energysavingtrust.org.uk/t/heat-pump-installers-toolkit/heat-pump-system-design/heat-loss-calculations-detailed-guidance/).

Ventilation planning must include its distribution components as well as the
unit. See [Zehnder: ventilation FAQs](https://www.zehnder.co.uk/en/help/faq) and
[air distribution](https://www.zehnder.co.uk/en/indoor-ventilation/solutions/air-distribution?stay=true).

Solar storage can shift generated electricity into evening / overnight use;
its usable capacity and power must be tested against the proposed cooling load.
See [Energy Saving Trust: battery storage](https://energysavingtrust.org.uk/advice/battery-storage/).

Cooling needs compatible equipment and room delivery. See [Daikin: heating and
cooling](https://www.daikin.co.uk/en_gb/residential/products-and-advice/needs/heating-and-cooling.html)
for examples of heat-pump cooling emitters; this is not a product selection.

## Drawing status

The concept 16 PDF is preserved as a historical declined option. Its numerical
checks apply to that old scenario only. Concept 25 is the latest measured whole-house proposal, retaining
the selected parents-suite A, full gym and D19. Concept 26 changes system
direction only; it does not revise room geometry or select equipment.
