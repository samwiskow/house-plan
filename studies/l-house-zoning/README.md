# Kitchen selections, circulation and daylight study

The user selected cabinet reference 1B, surface appearance 2A, milk-glass pendants 4B and a Belfast-style sink on 7 October 2026. The island is dark oak with framed panels, substantial corner posts and a shaped pale countertop edge. This supersedes the forest-green island and straight 20 mm edge proposals. The surface material and edge construction remain unresolved. The new stool reference has a curved timber back, solid shaped seat, splayed legs and foot rails; the pictured bridge tap is not selected. Explore a functional single-lever tap with a pull-out or pull-down rinse.

The user requested both circulation routes for comparison and clarified that hikari means the general treatment of natural light in Japanese architecture. Option D with an enclosed pantry and utility connecting door is now selected for the render study; the alternative hall routes remain comparisons.

## Scope

`build_study.py` reads the L-house measured source at `studies/l-house-booklet/plans.json`. It does not use the different courtyard-house geometry in `plan_model.py`. It writes a local interactive reference study at `output/design/kitchen-selections/zoning.html` and a source snapshot at `zoning-source.json`.

- A preserves the source plan and its 1.55 m cross-hall.
- B moves the 5.85 m kitchen/hall partition 0.35 m towards the stairs, leaving a 1.20 m hall in that section. Kitchen gain: 2.0475 m². The unchanged entrance remains 1.80 m wide.
- C removes that partition. It reallocates 9.0675 m² of hall plus 0.8775 m² of partition footprint to the kitchen/shared route. This is not all usable furniture area. The WC and stair transition needs redesign.
- The default pantry retains the 1.05 m utility passage and direct kitchen door. The preserved enclosed version has no utility-to-pantry door.
- The divider elevation tests three nominal 0.80 m glazed leaves across the existing 2.40 m opening, stacking over the 1.30 m return. A 2.40 m door height and upper glazing to 3.20 m are proposals. Track depth, structure, overlap, sealing and exact clear width are unverified.
- A 1.20 m slat screen at the left-hand wall is a visual zoning proposal, not a closable living-room enclosure.
- The plan overlays later 5.80 m garden bifolds and omits the superseded side garden door. The ceiling remains an interior test; the first-floor level is not coordinated.
- Daylight paths show conceptual connections, not sun angles, illuminance or a validated lighting simulation. North-side arrival and south-facing garden remain site assumptions. Furniture and route lines are schematic; no clearance or access certification is claimed.

The original geometry and Blender scenes remain unchanged. Source reference images are user-provided. No paid asset or product has been bought. The linked tap products are function references only.

## Rebuild

Run `python3 studies/l-house-zoning/build_study.py`. Serve the output on localhost only. The kitchen selection sheet is separately saved in `output/design/kitchen-selections/index.html` with its source and selection record in `sources.json`.

Validation: check all 18 plan/pantry/divider combinations, confirm no horizontal page overflow at 390 px, confirm the kitchen sheet selects 1B/2A/4B and sink-only 5A with no stool selected, inspect desktop and phone previews, and verify the measured source hash has not changed.

## Option D: boot-room reallocation

The user asked to test reclaiming boot-room space to improve the pantry and kitchen while retaining the utility and boot-room functions. `build_boot_study.py` generates the proposed alternative at `output/design/kitchen-selections/boot-room.html` and its geometry record. The user selected its enclosed pantry variant for the separate kitchen render study. The measured source plan remains unchanged.

The utility/boot boundary moves 1.35 m along the 1.55 m-wide upper boot-room section, transferring 2.0925 m². The pantry moves right and becomes 1.80 × 2.50 m (4.50 m²), with direct kitchen and utility connections. Unlike the previous enclosed option, a door can close the utility connection without deleting it. The kitchen is 20.70 m²; utility 11.5725 m²; boot room 10.4575 m². The hall, WC, stairs, exterior walls, windows and link openings remain in place.

The kitchen core widens by 600 mm and the side gap beside the source island grows from 825 mm to 1425 mm. The 500 mm gap behind source stool footprints remains unresolved. The main boot rectangle remains 3.15 × 3.00 m; the proposed coat cupboard depth is 600 mm rather than the source 450 mm. The utility fits side-by-side washer/dryer/sink, a 2.10 m folding counter and a tall cupboard. Pantry storage is a 600 mm counter and opposite 350 mm shelves, with 1.55 m between them.

Checks: furniture corners inside their room polygons, no room overlap on a 50 mm sample grid, and a nominal 600 mm shopping-route envelope sampled at 40 mm intervals around 24 angular positions. Door swings, appliance use, human movement, structure and detailed access are not validated. Browser checks cover open/closed pantry states, no script errors and no page overflow at 390 px.

## Kitchen render study

`../../scripts/blender/build_kitchen_study.py` creates separate furniture previews and room views from a copy of the approved living scene. Review `output/design/kitchen-selections/renders.html`. The island remains 2.4 × 1.0 m; the new image label of 3.2 × 1.4 m is not a selected dimension. Two custom timber stools replace the placeholders. The exact tap, hob and appliance layout are provisional. No asset purchase was made. The 3.2 m ceiling test still requires first-floor coordination.

The latest render removes the cupboards around the sink window. The tall fridge and pantry bank remain closed to the 3.2 m test ceiling. A plain blind-corner return replaces the narrow framed faces. The pantry entrance has paired cabinet-front panels on one door leaf, aligned rails, matching pulls and no projecting architrave. The pantry door moves forward into the 350 mm-deep cabinet frontage, with a short lined doorway behind it. Approximate island-to-front clearance is 1.05 m; occupied stools, open doors and access to high cupboards remain untested. This cabinetry is in the Blender study, not yet in the schematic plan furniture layer.
