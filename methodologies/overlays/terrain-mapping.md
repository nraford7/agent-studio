# Overlay: Terrain Mapping

Overlay id: terrain-mapping
Kernel compatibility: 1.0.0

Adapted with attribution from Agent Designer (see `THIRD_PARTY_NOTICES.md`),
rewritten to be **staff-neutral**: the phases describe work and artifacts, not
people. No phase pre-staffs a persona, and selecting this overlay does not
guarantee that a specialist is required. Personified roles are decided later
through `references/evidence-gate.md`.

Maps the strategic terrain — which decisions are available, forced, or
time-sensitive — rather than producing answers or recommendations.

## Phases

| # | Phase | Work produced | Required artifacts |
|---|---|---|---|
| 0 | Worldview capture | Plain-language need anchor, observations, relevant domains, time horizon, beliefs, stakes — never in framework language | `worldview_capture.md` |
| 0b | Context builder | Local materials reviewed with the user; at least one broad research query; facts, inferences, and unresolved claims recorded separately | `context_packet.md`, `research/` |
| 1 | Domain selection (per slice) | Which domains the worldview touches; a coverage check; an under-coverage check | `slices/slice-1/coverage_decision.md` |
| 2 | Domain analysis | Step-major (all domains finish Round 1 before any cross-pollination): independent mapping → cross-pollination → disconfirm audit → refinement → per-domain synthesis | `slices/slice-1/domains/<domain>/…` |
| 3 | Intersection analysis | 3–7 structural collisions (reinforcing loops, contradictions, hidden dependencies, causal chains, scale mismatches); slice synthesis leads with the finding | `slices/slice-1/intersection_analysis.md` |
| 4 | Decision landscape | No-brainers / strategic bets / watch-and-wait / avoid; what must be true, dependencies, time-sensitivity, reversibility | `decision_landscape.md` |
| 5 | Tripwire plan | Observable signals per decision; wrongness signals; cadence and ownership | `tripwire_plan.md` |
| 6 | Output package | Report synthesis from the verified research record; each slice leads with what it discovered | `report_source/` |

## Overlay-specific rules

- Default domain budget 4–5 (kernel rule 10). Fewer only for a narrow follow-up
  slice with stated rationale; more only when excluding a domain creates a known
  blind spot. Additional domains split into another slice.
- Intersections happen only after every domain has finished its own analysis,
  including its disconfirm audit and synthesis (kernel rule 2, made structural).
- The coordinator facilitates, it does not analyze when domains run in parallel
  (kernel rule 1).
- Thin analyses are labeled thin, never padded (kernel rule 8).
- A disconfirm / audit function runs per-domain inside phase 2, after mapping and
  cross-pollination and before refinement.

## Staffing implication (not a mandate)

Terrain mapping usually calls for **analytical functions**, which are a poor fit
for the persona evidence base. Any personified specialist proposed here still owes
experimental or work-sample proof under the evidence gate, and the default is to
run the domains in-house.
