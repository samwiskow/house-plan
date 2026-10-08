# Coastal whole-house model

The coordinated model uses the L01.1 measured plan, the selected Option D pantry,
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
continuous parquet, linen curtains and four folding divider leaves. New rooms
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
  family-bedroom library gym office combined-room terrace
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
performance or services design. The four rooflight rectangles are still the
approved plan zones. Their glazing and trimmers are modelling allowances.
The shared-room furniture retains the earlier tight route; chair, stool and
appliance operation needs further design. No surveyed coast or daylight analysis
is claimed.
