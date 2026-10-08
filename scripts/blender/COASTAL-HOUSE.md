# Coastal whole-house model

The coordinated model uses the L01.1 measured plan, a revised full kitchen-depth pantry based on Option D,
and the approved combined kitchen, dining and living scene. The earlier courtyard
house is not a geometry source. The measured source files and earlier Blender
scenes remain unchanged.

## Review

Serve this checkout on loopback only:

```sh
python3 -m http.server 4197 --bind 127.0.0.1
```

- `http://127.0.0.1:4197/viewer-coastal/gallery.html`: Cycles views.
- `http://127.0.0.1:4197/viewer-coastal/`: local orbit viewer with floor cutaways.
- `output/blender/coastal-house/coastal-house.blend`: editable scene in metres.
- `output/blender/coastal-house/coastal-house.glb`: local browser scene.
- `output/blender/coastal-house/geometry-checks.json`: geometric check results.

The native scene and GLB contain the licensed table from the approved room study.
Both files stay local and are ignored by Git. They must not be published as raw
assets. Renders, builders and reports can be reviewed in the branch.

## Coordinated section

| Part | Structural floor level | Ceiling underside above datum |
| --- | ---: | ---: |
| House ground | 0.00 m | 3.20 m |
| House first | 3.50 m | 2.70 m |
| Garage ground | 0.00 m | 2.70 m |
| Garage office | 3.00 m | 2.70 m |

The 300 mm difference between ceiling and upper-floor datums resolves the previous overlap between the 3.20 m
interior study and the old 3.00 m floor-to-floor model. This is a section proposal,
not an approved structural design. Finished floor surfaces are 40 mm above the
structural levels, so finished clear heights are 3.16 m downstairs and 2.66 m
upstairs and in the garage. This retains the exact ceiling elevation of the
approved room scene. Ceiling thickness grows upwards into the floor zone; it
does not reduce those clear heights. Timber and masonry relief extends up to 25 mm beyond the base
wall surface.

The main roof has a proposed 6.41 m eave and 8.46 m ridge datum. The office
roof retains its 7.75 m ridge. The link and plant high roof edges are 3.65 m
and 3.10 m, with clear space above the ceiling build-up.

The house stair has 18 risers at 194.44 mm and 287.5 mm goings. The garage stair
has 16 risers at 187.5 mm and 300 mm goings. Both fit the recorded stair envelopes.
The full stair voids are cut from the floor slabs. The upper suite keeps its
rectangular bedroom and separate gallery doors. Four rooflights have roof cuts,
ceiling cuts, light wells and provisional trimmers.

The burner stays in a separate hidden option collection, as selected by the user.
Its former vertical flue would obstruct the suite gallery. It has not been routed
through occupied space.

## Model detail

The approved room scene supplies the original furniture, kitchen joinery,
parquet material, linen curtains and four folding divider leaves. New rooms
include beds with bedding and supports, framed joinery, library books, bathroom
fittings, mirrors, towels, desks and monitors, gym equipment, workshop tools and
plant reservations. Separate collections and object tags identify levels, walls,
floors, ceilings, openings, furniture, roof, stairs and site.

The assumed 40 x 65 m plot includes the source forecourt and visitor bays, an
arrival gate and road, sheltered dining under an oak pergola, limestone terraces,
gravel routes, sea-view seating, raised growing beds, a tool store, an outdoor
rinse point, compost bins, windbreak planting, grasses, low dune banks and rocks.
The shoreline is illustrative. Planting is a visual proposal, not a planting
specification for a known site.

## Rebuild

The approved combined-room scene must be present locally. Pass its actual path;
the builder verifies that the source file remains unchanged.

```sh
blender --background --disable-autoexec --python-exit-code 1 \
  --python scripts/blender/build_coastal_house.py -- \
  --interior /path/to/combined-kitchen-dining-living.blend \
  --width 1600 --samples 64 --export \
  --views arrival garden coastal-plot ground-cutaway first-cutaway \
  parents-bedroom suite-gallery dressing bathroom bathroom-vanity \
  family-bedroom library gym office guest-room bathroom-shower rooflights combined-room terrace \
  entrance-hall under-stair pantry kitchen-storage utility bathroom-shower-closed \
  sea-sunset coffee-station
blender --background --disable-autoexec --python-exit-code 1 \
  --python scripts/blender/check_coastal_house.py
python3 scripts/blender/build_coastal_gallery.py
node scripts/blender/check_coastal_preview.cjs
```

Blender 5.2 and a local Cycles device are required. The builder uses Metal when
available, with a CPU fallback. The browser check uses Playwright and local Chrome.
The browser keeps the same geometry but uses simpler material colours where
Blender procedural shaders cannot be exported. Cycles stills are the finish and
lighting reference.

## Check scope and remaining design work

Checks compare unchanged rooms with the measured source, cast rays through all
four rooflight openings, sample structural ceiling clearance throughout the rooms and stair headroom,
check new furniture bounds with a 31 mm room-edge tolerance, and check nominal 700 mm suite
routes against the saved furniture and open door leaves. Browser checks cover
camera presets, cutaways, local-only requests and a 390 px phone viewport.

These checks do not establish construction compliance, occupied furniture use,
structural support, roof drainage, product fit, waterproofing, coastal exposure
performance or services design. Three rooflights retain the source plan zones. Gallery rooflight G1 moves 1.15 m
toward the bedroom so its glazing and a 100 mm surrounding allowance stay on one
roof plane. Glazing, trimmers and flashings remain modelling allowances.
The shared-room furniture retains the earlier layout. The new kitchen route is
checked at a nominal 700 mm width; occupied chair, stool and appliance use still
needs product-specific design. No surveyed coast or daylight analysis
is claimed.

## Interior review corrections

The parents bathroom window moves from the shower to the west wall above the
bath. Its opening is 1.30 m wide and 1.35 m high, with a 1.05 m sill above the
structural floor datum. The custom timber ofuro allowance is 1.10 x 0.85 x 0.74 m,
with 43 mm walls, a 610 mm deep well, an internal seat, waste, overflow and wall
spout. Its form follows [Bartok Design's square hinoki tub](https://www.bartokdesign.com/japan/7-custom_ofuro/square_tub_for_canada.php).
These are model dimensions, not a selected product specification.

Each fixed shower glass panel has an overhead head and hand shower behind it.
Each station has a wall-mounted 350 mm rain head on an extended arm and a hand shower. The two independent
mixer/diverter controls sit between the showers on the real rear wall, away from
the rain heads. There are no control pedestals. The enclosure front is all glass. A hinged glass door closes the central opening.
Both open and closed door views are available in the gallery and browser model.

Inset louvred shutters occupy all five windows in the office, library and guest
bedroom. The office bookcase moves along the east wall to clear the window.
The U5 bed turns onto the solid west wall. Headboard panels now follow bed
position and orientation, and the geometry check tests every bed headboard and
panel against window openings. It also checks shutter reveal depth and extent,
paired shower fittings, the bath window, tub depth and rooflight plane clearance.


## Warm interior and service-room revision

The finish scheme uses natural oak, warm ivory, pale limestone, woven rugs and
linen, with muted blue accents. Bedrooms have upholstered headboards, shaped
bedding, framed art and rugs. The parents bedroom includes a reading chair,
side table and full-height linen curtains. The bathroom combines an oak vanity
body and mirror frames with blue drawer fronts and pale stone.

The pantry extends through the full kitchen depth, from plan Y 5.35 to 9.30 m.
Its net area is 6.655 m², with an east worktop, drawers and open shelving. A small
recess on its west side accommodates two generic 600 mm fridge/freezer columns.
The hall-to-kitchen opening moves to X 9.85 m and opens into the hall. The old
fridge position becomes an oven and storage tower. The utility outline stays
unchanged. Kitchen and pantry share the same continuous herringbone layout and
threshold. The boot room and utility use honed stone floors. The boot-to-link door opens
into the link to keep the route past the coat cupboard clear.

Six doors retract into modelled wall pockets: the three suite doors, guest and
office shower rooms, and the utility-to-pantry door. The kitchen-to-pantry leaf
is concealed in the cabinet front, closed by default and open in the pantry view.
A matching full-height infill closes the narrow joint beside the fridge bank. The house stair's lower flight is now
on the east side and its upper flight on the west. Open guards face the entrance
hall. Five integrated storage modules fit below the lower flight and face the hall.
A bench remains below the upper flight. A 2.10 × 2.63 m stair window brings
daylight through the stair volume.
The garage stair remains in its original arrangement.

The metal roof uses 430 mm panels with 25 mm standing seams running down each
roof pitch, plus ridge and valley flashings. These visual dimensions follow
[VMZINC's standing-seam guidance](https://www.vmzinc.com/en-gb/standing-seam-vmzinc).
The roof is a model allowance, not a specified coastal roofing system.

Additional checks cover the pantry outline, matching floor materials, pocket
leaf fit inside wall cores, stair direction, under-stair cabinet clearance,
700 mm service routes, roof seam direction and the shower door's 0–90° swing
against adjacent fittings. The browser check verifies both shower door poses.


## Golden hour and everyday objects

The scene uses a single multiple-scattering sky with a visible 7° sun. A matching
HDR environment is generated for the browser, with its sun direction aligned to
the native scene. Interior lamps use lower output and warm light. Interior stills
use 0.6 stops more exposure than exteriors to retain detail in the rooms. The
setting is illustrative, with no surveyed site orientation or dated solar claim.
A sloping sand beach, low dunes and rippled water extend beyond the garden.

[Poly Haven's CC0 licence](https://polyhaven.com/license) covers the imported
[armchair](https://polyhaven.com/a/modern_arm_chair_01),
[wooden bowl](https://polyhaven.com/a/wooden_bowl_01) and
[kettle](https://polyhaven.com/a/vintage_electric_kettle).
The chairs retain the source mesh and surface detail, with neutral upholstery
for this scheme. Download URLs and checksums are in `assets/coastal-study/sources.json`.
The available vintage bed models did not fit the supplied bedroom references;
the measured upholstered beds remain custom geometry. The compact espresso
machine is also custom geometry, using the form of a domestic machine such as
[the Sage Bambino](https://www.sageappliances.com/en-gb/product/bes450) as a reference.
It is not an exact product model.

Stoneware plates and mugs, clear water glasses, cutlery, napkins, fruit, books and
post add signs of daily use. Fabric weave, subtle stone roughness, brushed metal
and the water surface respond differently to the same light. The kitchen and
pantry walking routes remain clear with the concealed pantry door open.
