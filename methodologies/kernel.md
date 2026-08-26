# Studio Methodology Kernel — The Canon

Kernel version: 1.0.0

Adapted with attribution from Agent Designer's methodology kernel (see
`THIRD_PARTY_NOTICES.md`). This kernel defines the universal operating rules for
any staffed work Agent Studio designs. Overlays (`methodologies/overlays/`) add
phase-specific structure on top; they never amend the kernel. Kernel changes are
deliberate, reviewed acts with a version bump.

The kernel is a **methodology** — it describes how work is organized and checked.
It is **staff-neutral**: it says nothing about who does the work, and it never on
its own justifies hiring a persona. Staffing is decided later, and only through
the evidence gate (`references/evidence-gate.md`).

The kernel is part of the durable-output machinery. Per the durability gate
(`SKILL.md`), it is inherited whole by a **reusable staffed workflow** or a
**standing team**, and recorded by version in that team's `team.json`. Lightweight
outputs — an in-house playbook, a solo specialist, or a one-off panel — run the
lean lifecycle and do not carry the kernel.

## The ten rules

1. **The facilitator orchestrates.** Whenever two or more contributors work in
   parallel, the facilitator does not also analyze — a coordinator that both runs
   the panel and weighs in anchors every other voice to its own view. If analysis
   is missing there, add a contributor rather than widening the facilitator. On a
   solo or small run with no parallel panel to bias, the facilitator may analyze
   directly.
2. **Independence before convergence.** Contributors work in isolation before they
   are exposed to each other's work. Early exposure anchors every later voice to
   the first confident output. The default is parallel isolated work first;
   cross-reading happens only in explicit convergence steps.
3. **Disagreement is signal.** Where contributors diverge, that is information
   about what is genuinely uncertain. Never force consensus. Surface divergence
   explicitly; a synthesis preserves tension and marks what is robust versus
   contested, and never averages strong differences into a bland middle.
4. **Exposure is progressive and intentional.** Context is the scarce resource.
   Stage exposure: summaries before full transcripts, full cross-reading only in
   dedicated integration steps. This protects a single context from drowning and
   prevents anchoring at the same time (see the progressive-exposure section of
   `SKILL.md`).
5. **Human checkpoints at consequential decisions.** After each synthesis step the
   human gets a concise summary and targeted questions. The facilitator does the
   mechanics; the user is never asked to run scripts by hand.
6. **Findings are triaged by significance.** Minor feedback — corrections that do
   not change direction, clarifications — folds in without another round. Major
   feedback — new factors, contradictions of a contributor's assumptions — offers
   a re-round the human may decline.
7. **Required artifacts are validated before dependent phases continue.** Each step
   leaves its named artifact at an announced path; the facilitator confirms it
   exists and is substantive before the next phase depends on it. A missing or
   thin artifact triggers a retry with the path restated, never a silent skip.
8. **File discipline supports re-entry.** Exact paths, announced in advance,
   validated after. Run state lives in a manifest the facilitator updates as
   phases advance. Outputs lead with what a step discovered or changed; process
   notes follow as provenance. Every run is re-enterable from its files alone.
9. **Deterministic checks validate structure; model-mediated checks assess
   quality.** Scripts may verify that files exist, sections are present, and
   references resolve. Anything about quality, voice, fidelity, or significance
   stays a matter of model or human judgment — never a regex.
10. **Exploration is bounded.** Set an explicit budget up front — contributors,
    rounds per phase, context, time — and say what it is. Use the minimum that
    covers the question. Work that exceeds the budget splits into a new run rather
    than expanding silently.

## What the kernel does NOT fix (conditional recipe decisions)

These are chosen per task by the recipe (`references/recipes.md`) and the overlay,
not mandated by the kernel:

- whether a critic / devil's-advocate is present;
- whether the work uses more than one round;
- whether a high-stakes normative task requires different model families;
- whether a creative result is selected by a human (for creative work it is —
  `references/hard-rules.md`);
- how task-specific outputs are combined (`references/synthesis-modes.md`).

## Relationship to the evidence gate

The kernel organizes work; it never staffs it. A methodology describing a phase
does not imply a persona should perform that phase. Every personified role still
passes `references/evidence-gate.md` on its own evidence. A kernel or overlay
phase is satisfied in-house by default.
