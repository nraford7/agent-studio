# Persona Evidence Gate

Every job in the Workflow Specification starts in-house. A job being
judgment-laden is NOT sufficient to open a role. This gate decides, per
candidate role, whether persona-shaped specialization is worth testing at all —
and how much proof it owes before hiring.

## Task families

Classify the job's candidate role into exactly ONE family:

| Task family | Intended persona benefit | Evidence status |
|---|---|---|
| Creative divergence | Useful semantic breadth and distinct options | Best-supported use in the corpus |
| Value-laden deliberation | Representation of legitimate conflicting priorities | Relatively favorable, conditional evidence |
| Grounded human or stakeholder simulation | Fidelity to differently situated human responses | Narrow, substrate-dependent support; never a substitute for real research |
| Multi-stakeholder subjective evaluation | Coverage of stakeholder-specific criteria | Promising in limited tested domains; human decision-maker retained |
| Sustained functional priority | Persistent attention to a consequential trade-off | Thin, single-domain causal evidence |
| General critique or analytical judgment | Valid blind spots or alternative interpretations | Indirect evidence or inference |
| Forecasting | Independent private signal or evidence framing | Persona-specific benefit unproven |
| Factual, checkable, or procedural work | Accuracy or reliable execution | No research-backed persona reason |

## Deterministic routing

Each family maps to exactly one of four user-facing conclusions, verbatim:

- **Research supports trying this.**
- **Supported only for a narrower analogous use.**
- **Promising, but experimental.**
- **No research-backed reason to create a role.**

The conclusion sets the proof the role owes. There is no discretion in this
mapping. These four strings are internal keys — when you show one to the user,
say it in the warm phrasing from `voice.md`.

| Family | Conclusion (verbatim to user) | Proof required before hiring |
|---|---|---|
| Creative divergence; value-laden deliberation | **Research supports trying this.** | None — may hire directly. A work sample is optional, recommended only when stakes are high. |
| Grounded simulation; multi-stakeholder subjective evaluation | **Supported only for a narrower analogous use.** | FIRST narrow the Job Description, mandate, activation trigger, and role status to the supported framing; THEN a blind work sample on that narrow framing. Success opens only the narrowed role. Human decision-maker retained for subjective evaluation. |
| Sustained functional priority; general critique or analytical judgment | **Promising, but experimental.** | A blind work sample (see `work-sample.md`). |
| Forecasting; factual/checkable/procedural work | **No research-backed reason to create a role.** | No role. Keep in-house: methods, tools, verification, independent attempts, or voting as appropriate. For forecasting, ensemble the EVIDENCE FRAMINGS in-house (recipes.md row) — do not infer a persona hire. |

## Roster waiver

A roster persona (see `roster.md`) may waive the work-sample requirement for a
task family when its track record shows:

1. Two or more real assignments in that SAME family, with contributions
   retained downstream, AND
2. At least one of those verified by a localized counterfactual contribution
   check (Stage 11).

The waiver replaces the work sample only. It never replaces the gate: a job
whose family maps to "No research-backed reason" gets no role regardless of who
is on the roster. Familiarity never bypasses the gate.

## Persona Evidence Card template

Write one card per candidate role into `evidence-cards.md`:

```
## Evidence Card: <role working title>
- Job (from workflow-spec.md): <job name>
- Task family: <one of the eight>
- Conclusion: <one of the four, verbatim>
- Intended persona effect: <the specific behavioral change the persona should cause>
- Intervention shape: <solo role | ensemble seat | simulation panel | none>
- Evaluation signal: <2-3 observable criteria tied to the intended effect> + <1 harm check>
- Contraindications / likely harm: <how this persona could make the work worse>
- Proof required: <direct hire | narrowed blind sample | blind sample | none — role refused>
- Waiver: <none | roster: <persona name> — <N> same-family entries, counterfactual-verified: <yes/no>>
```

A role proceeds to a Job Description only when it is coherent AND its
conclusion is not "No research-backed reason to create a role."

## Retrieval material is not evidence

A persona's domain retrieval kit (its vocabulary, named methods, and fluent
research queries — see `persona-template.md`) never counts toward this gate.
Rich vocabulary makes an answer sound expert without making it more correct.
Only the mapped task family, a blind work sample, or a qualifying roster track
record can satisfy the proof a role owes. Vocabulary is not proof.
