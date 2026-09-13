# Courtyard house: 13 September design review

The five agreed next steps now have reviewable concept outputs. Start with the
current whole-house plan. Selected directions, provisional layouts and unresolved
technical design are recorded separately; a recommendation is not a selection.

| Document | What it resolves or exposes |
| --- | --- |
| [20: Current whole-house plan](output/pdf/concept-20-current-whole-house-plan.pdf) | Current furnished plan at 1:100, room schedule and decision register. |
| [17: Service-end comparison](output/pdf/concept-17-service-end-comparison.pdf) | Laundry compromise versus a gym-block extension; B preserves the full gym and laundry but adds 12.22 m2 footprint. |
| [18: Office and guests](output/pdf/concept-18-office-and-guests.pdf) | Day / night furniture, guest bedroom / shower and a five-visitor sleeping example. |
| [19: Everyday-use review](output/pdf/concept-19-everyday-use-review.pdf) | Twelve scenarios with open doors, drawers, baskets, a seated person and extra dining chairs. |
| [21: Building coordination](output/pdf/concept-21-building-coordination.pdf) | Candidate service routes, sections, cooling coverage and inputs for detailed design. |

## Decisions for review

1. **Plant location:** develop the gym-block extension or revisit the laundry
   compromise. The original family-wing plant placeholder stays until a complete
   relocation is accepted and designed. The larger linen shelves remain conditional.
2. **Office sofa bed:** accept the one-sided night exit or explore a different
   furniture arrangement / mechanism. The far-side sleeper crosses the mattress;
   daytime work stops while the bed is open.
3. **Dining:** the current plan has eight dining chairs. Two added end chairs
   obstruct the cross-routes. Decide whether ten must sit together or whether
   occasional island seating is acceptable; no ten-seat layout is adopted.
4. **Services crossing:** a visible edge band below the vault may be required.
   Its proposed dimensions illustrate the architectural effect, not a verified fit.

## What has been checked

The two service-end variants retain 40 sampled house routes, and option B checks
three internal plant approaches and maintenance reservations. Office / guest
proposals check 49 routes in each day / night state; the office far-side strip is
only a local clearance check and is not a connected exit route. Whole-house use
scenarios compare clear baseline routes with temporary obstacles; recorded
failures are deliberate findings. All 19 new A3 pages were rendered and visually
reviewed. Older PDFs were not regenerated.

These are spatial checks. They do not establish accessibility, occupied bathroom
comfort, actual furniture mechanisms, structure, heat loss, cooling, ventilation,
hot-water capacity, solar coverage or site compliance.

## Detailed design inputs still needed

The actual plot / survey, roof and envelope build-ups, incoming water / electrical
supply, chosen shower flow and duration, room temperatures, acoustic priorities
and solar / battery preferences remain inputs. Concept 21 assigns these to the
relevant design work and shows the required outputs. No equipment orders or
joinery dimensions should be based on the provisional plant bodies alone.

## Rebuilding and provenance

Use the bundled Python runtime documented in README. Build concept 17 with
`service_end_study.py`, and concept 18 with `office_guest_study.py`.
Then run `household_use_review.py`, `consolidated_plan.py` and
`building_coordination.py`. The latter three load the source-checked concept 18
snapshot through `development_model.py`; source changes require rebuilding it.
The JSON files beside the PDFs preserve geometry, checks and explicit limits.

Work was delivered sequentially in five local branches / commits. The final
`codex/building-coordination` branch contains the complete stack. This repository
has no remote configured, so there is no PR/MR or remote pipeline. Main is unchanged.
