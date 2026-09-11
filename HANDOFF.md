# House design handoff

## Latest direction: concept 07B

The shallow extensively glazed garden-room roof and broad plain ivory opening
are now selected. Continue the same flooring; design insulating solar-control
glass, external shading provision, high-level ventilation and whole-space
winter/summer comfort together. `output/pdf/concept-07b-glazed-roof-transition.pdf`
contains the section and interior view. Its heights and framing remain provisional.

## Floor-plan direction: concept 07

Concept 06B's continuous shared-room vault and lower stone wings/gym are chosen;
detailed heights remain provisional. The garden room is now for year-round use,
open to the shared room and adjoining hall. Concept 07 removes those two internal
walls and relocates the hall door beyond the snug, separating office and guest
rooms while leaving the snug and WC on the shared side. See the current README,
MATERIALS-BRIEF.md and `output/pdf/concept-07-open-garden-room.pdf`. Earlier notes
about an enclosed or seasonal orangery are superseded. Structural supports and
the transition between the lower garden-room roof and higher vault remain open.


## Update: 11 September 2026

The user has chosen the single-storey courtyard house for further development.
[MATERIALS-BRIEF.md](MATERIALS-BRIEF.md) is the current record of architectural
character, materials, arrangement A and the log-burner proposal. Its agreed
directions supersede the older exploratory focus below. Exact products and
technical specifications remain open; the measured model is unchanged.

## Earlier handoff: 9 September 2026

Prepared 9 September 2026. Next focus: low-fidelity exploration of a house
with more than one floor, compared with the accepted single-storey scheme.
An upper floor has not been selected or approved for the dimensioned model.

## Read these first

- `README.md`: authoritative agreed brief, current dimensions, room areas,
  validation scope, unresolved technical work and rebuild instructions.
- `output/pdf/u-home-dimensioned-concept.pdf`: accepted concept 05, four A3
  sheets. Inspect it visually before proposing spatial changes.
- `plan_model.py`: editable geometry and PDF renderer. Importing or running
  this file regenerates the PDF and area-check JSON as a side effect.
- `output/pdf/area-check.json`: computed areas and latest geometry checks.
- Commit `d85da1c`: accepted concept 05; commit `d9f1871`: concept 04 baseline.
  Use Git history for exact changes rather than treating exploratory sketches
  in the conversation as a second source of measured geometry.

At handoff creation, the accepted design was committed on `main`, with no
outstanding design changes. This handoff is a newly written, uncommitted file.
Verify Git state when resuming; do not duplicate the already completed commit.

## What the conversation established

We first explored U and H arrangements, then developed the U into a measured,
furnished concept. Later discussion refined the kitchen/service corner, brought
the exercise room indoors and added a compact corner orangery. These accepted
decisions are incorporated in concept 05; details are in the artifacts above.

The current request is to preserve context and then imagine multiple floors at
low fidelity. It does not replace concept 05 or authorize an unchosen upper-floor
scheme to overwrite it. Keep the baseline available for comparison.

## Distilled preferences and the reasons behind them

- Warm, understated modern architecture. Architectural character, sheltered
  outdoor spaces and distinct wings appeal more than a square box or a grand,
  complicated composition. The more elaborate H reference felt excessive.
- The U won largely through spatial efficiency and the useful garden-facing
  courtyard. A formal front arrival courtyard is not itself desirable. Earlier
  comparisons needed realistic room for household and guest vehicles.
- The important privacy boundary is between entertaining/shared activity and
  family bedrooms/bathrooms. An earlier suggestion that entertaining or guests
  needed a completely separate living domain was corrected: guests share the
  main kitchen and living room and do not need an extra private sitting room.
- This is an ideal-home exercise before selecting a plot. Family growth and
  regular grandparents/overnight guests matter. Exact ages, mobility needs,
  location, orientation, budget and planning constraints are not established.
- Single-storey living is attractive, but multiple floors are explicitly open
  for exploration. Parents' proximity to the children is still a question,
  not a fixed preference. Modest separation was welcomed in the single-storey
  scheme; do not assume that separation by a whole floor is therefore desired.
- Prefer generous shared living space over an oversized parents' sleeping
  room. Smaller retreat spaces should earn their place through flexible uses:
  reading/play in the snug, gaming in the daily-use office.
- Practical daily routes drive the design: groceries to pantry/counter/fridge,
  coats and shoes in the boot room, separate laundry, and useful storage.
  The entrance hall can shrink to protect useful kitchen and service space.
- A larger usable garden matters. The orangery became a small room connecting
  the guest-wing hall and shared space, rather than an enclosure of the whole
  courtyard. Preserve direct circulation around it and external exposure for
  bedroom windows.
- Pocket doors are welcome where they solve conflicts. Their cavities still
  need space; do not treat them as a way to eliminate circulation allowances.
- Work iteratively: establish needs, show comparable options, validate, then
  make the preferred plan measurable. Higher fidelity helped with the initial
  U/H choice; low fidelity is now explicitly requested for the floor-count study.
- Keep a versioned local design record. Do not confuse a reassuring sketch
  with a dimensioned, checked plan or a construction-ready design.

## Corrections and unresolved choices to preserve

- Ignore the early transcription about ease of building; it was withdrawn.
- The detached gym is superseded by the indoor location in concept 05.
- The earlier larger orangery is superseded by the compact corner version.
- Seasonal versus fully heated year-round orangery use was asked about but
  never explicitly settled. Do not infer a heating/glazing specification.
- Materials, roof form, solar orientation, stair provision and acoustic build-ups
  remain proposals or future work, not approved technical specifications.
- The verification limits in `README.md` are material. Existing automated
  checks do not certify daylight, fire escape, stair design, accessibility,
  vehicle manoeuvres or equipment-specific operating clearances.

## Approach for the multiple-floor exploration

1. Start with room-group and massing diagrams, showing ground and upper floors
   together and aligning the stair position between them.
2. Compare a family sleeping floor with a smaller partial upper floor that
   retains more ground-floor living. Explicitly compare parents and children
   on the same floor versus different floors.
3. Retain a usable ground-floor guest bedroom and shower in the alternatives.
   Keep the accepted room programme visible; do not silently lose the office,
   snug, pantry, laundry, gym, family bath or orangery while stacking rooms.
4. Show which ground-floor area is removed or reassigned. An upper floor only
   reduces the footprint if the lower floor is deliberately recomposed.
5. Account for stairs, landings, structure and services before making area or
   cost claims. Existing single-storey checks do not validate a new stack.
6. Explore height on one wing first. Consider courtyard sunlight, overlooking,
   bedroom privacy and the relationship between the upper floor and orangery.
   These depend on a future plot and cannot be solved from the sketch alone.
7. Seek a preferred arrangement before revising the measured source/PDF.

## Suggested skills

- **visualize:visualize**: invoke/read the skill for the requested low-fidelity
  in-conversation spatial comparisons. Use deterministic labelled diagrams.
  Reload the full visualize skill after context compaction before authoring.
- **pdf:pdf**: invoke/read when inspecting or revising the dimensioned PDF;
  follow its authoring marker and render-and-inspect workflow.
- **imagegen**: only if a later request needs architectural atmosphere or
  material/appearance imagery. Do not use generated imagery as measured geometry.
- **handoff**: local guidance was found at `~/.codex/skills/handoff/SKILL-1.md`.
  This file is in the project because the user explicitly requested that
  location, overriding the skill's usual temporary-directory default.

## Low-fidelity study produced after this handoff

Two unselected alternatives are shown in
`~/.codex/visualizations/2026/09/09/01a08792-e0a1-7c40-85b5-5133c9bcdb4d/two-floor-family-home.html`:

- A: a family sleeping floor over one wing, with guests at ground level.
- B: a smaller children's upper floor, with parents and guests downstairs.

Both show the same stair location between floors. These are room-group diagrams,
not measured layouts: the drawn room blocks cannot be used to derive areas or
prove furniture, circulation, stair or structural fit. Neither changes the
accepted source model. A offers the stronger same-floor family grouping; B
retains more single-level daily living but separates parents and children by
stairs. Footprint savings require actual ground-floor recomposition, and are
not quantified in this study.

Latest steering: the user wants an alternative that deviates further from the
original plan, with particular emphasis on separating office and bedrooms.
The earlier A/B studies put work rooms under some family bedrooms; do not treat
that stacking as a preferred arrangement.

Option C explores a compact two-storey main house and an offset single-storey
office/gym pavilion joined by a short enclosed garden passage from the arrival
hall. All bedrooms, including ground-floor guests, remain in the main house;
none are above or beside the office. Office and gym have separate lobby access,
with a storage/circulation buffer. The small orangery becomes a room off shared
living rather than the original hall/living corner bridge. This alternative is
unselected, unmeasured and not incorporated into concept 05. Its diagram is
`~/.codex/visualizations/2026/09/09/01a08792-e0a1-7c40-85b5-5133c9bcdb4d/linked-work-pavilion.html`.

The user subsequently approved recording C as a separate two-storey option.
`output/pdf/two-storey-linked-pavilion-option.pdf` now contains its ground and
upper-floor diagrams on two A3 sheets. `two_storey_option.py` is the independent
renderer. Both sheets were rendered and visually inspected; the diagrams remain
unmeasured and do not replace concept 05. The PDF, renderer and documentation
updates have not yet been committed.

## Practical continuation notes

- Use `wt` for branch/worktree management when changing the accepted design.
  Prior work used an isolated worktree, verified the drawings, committed with
  a conventional message and integrated back to `main` locally.
- There is no requested remote publishing or external review workflow here.
- Use the bundled dependency runtime; the rebuild command is in `README.md`.
  `pypdfium2` successfully rendered review PNGs when Poppler produced noisy
  font-configuration warnings. Temporary renders belong in `tmp/pdfs/`.
- Keep contact details, commit-author email and other personal identifiers out
  of handoffs. No credentials or account configuration are needed to continue.
