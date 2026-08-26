# Overlay: Root Cause Investigation

Overlay id: root-cause
Kernel compatibility: 1.0.0

Adapted with attribution from Agent Designer (see `THIRD_PARTY_NOTICES.md`),
rewritten to be **staff-neutral**: the phases describe work and artifacts, not
people. No phase pre-staffs a persona, and selecting this overlay does not
guarantee that a specialist is required. Personified roles are decided later
through `references/evidence-gate.md`.

Investigates why something happened: incidents, failures, regressions, recurring
problems, near misses. Evidence-governed — observed facts are separated from
belief, inference, missing evidence, and contested claims throughout.

## Phases

| # | Phase | Work produced | Required artifacts |
|---|---|---|---|
| 0 | Case framing | Event, impact, boundary, evidence inventory, uncertainty, and the decision the investigation must support | `intake.md` |
| 1 | Evidence ledger + sequence | Provenance recorded, timeline reconstructed, changes identified, observed facts separated from inference | `evidence-ledger.md`, `timeline.md` |
| 2 | Method stack | A revisable combination of methods chosen from the case shape (fishbone, 5 Whys, fault tree, barrier analysis, control-structure) — not one fixed method | `method-stack.md` |
| 3 | Evidence-led causal analysis | Method-driven hypothesis building and testing; structured method data; confidence limits per hypothesis | `causal-hypotheses.md`, `method-analyses/` |
| 4 | Disconfirmation + gap resolution | Leading explanations challenged, missing evidence requested, residual uncertainty marked | `disconfirmation.md`, `evidence-gaps.md` |
| 5 | Synthesis + corrective actions | Triggers, contributing conditions, failed controls, and systemic causes separated; actions mapped to supported mechanisms; what the investigation itself missed | `causal-synthesis.md`, `corrective-actions.md` |

## Overlay-specific rules

- Evidence-first intake: classify every input as observed fact, belief, inference,
  missing evidence, or contested claim before analysis begins.
- Evidence-gap loop: the investigation may pause, request specific missing inputs,
  and resume with amended artifacts (bounded per kernel rule 10).
- Anti-blame: "human error" never ends a branch — it starts one (what made the
  error likely?).
- Corrective actions map only to supported causal mechanisms, each with a
  verification signal. No action without a mechanism; no mechanism without its
  evidence class stated.
- A disconfirm function runs at phase 4 against all standing hypotheses, before
  synthesis; corrective actions may map only to mechanisms that survived it.

## Staffing implication (not a mandate)

Root-cause analysis **defaults to regular agents and tools** — its work is largely
factual, checkable, and procedural, which the evidence base maps to "No
research-backed reason to create a role." A personified role is opened only if a
distinct specialist contribution passes the evidence gate on its own.
