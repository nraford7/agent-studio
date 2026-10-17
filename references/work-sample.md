# Functional Role Prototype and Work Sample

Skip this file entirely for roles whose Evidence Card says "direct hire" or
carries a roster waiver — they go straight to hiring.

## Prototype template

The prototype is an EVALUATION INSTRUMENT, not an agent the user keeps. It is
the smallest anonymous functional version of the role: NO famous name, NO
character identity, NO decorative biography. Write to
`agent-studio-out/<slug>/prototypes/<role>.md`:

```
# Prototype: <role title>
## Mandate
<from the JD, verbatim>
## Capabilities
<from the JD, with exclusions>
## Recognitions
<experience profile as behavior: situations / mistakes anticipated / distinctions / methods>
## Values
<trade-off rules and red lines>
## Method
<numbered working procedure>
## Output contract
<the literal output format>
## Boundaries
<what it must not do; when it escalates>
```

## Blind protocol

Default: ONE bounded assignment — the smallest representative slice of the job
from workflow-spec.md.

0. Inputs: use the user's real material for the slice; ask for it. Non-interactive
   with none supplied: write a synthetic fixture, and label the verdict as
   tested on synthetic material.
1. A fresh subagent performs the slice as the in-house assistant, with the best
   appropriate playbook (not the orchestrator, which knows the A/B plan).
2. A fresh subagent performs the same slice AS the prototype — same model, same
   information, same tools, same reasonable effort. Its prompt opens with the
   SUBAGENT PROMPT PREAMBLE from `hard-rules.md`.
3. The orchestrator saves both outputs under neutral labels in RANDOM order to
   `agent-studio-out/<slug>/work-samples/<role>/sample-A.md` and `sample-B.md`.
   The A/B assignment is held in the orchestrator's context only — NOT written
   anywhere the evaluator could read.
4. Both samples pass the SOURCE CHECK first when the slice is sourced
   (`hard-rules.md`).
5. The user (or an evaluator that has NOT seen either generation, on the second
   model family by default)
   judges A vs B on the Evidence Card's evaluation signal: 2-3 criteria tied to
   the intended persona effect, plus the one harm check. Write the judgment to
   `verdict.md`; only THEN write the mapping to `key.md` and unblind.

Scaling: low-stakes reversible roles = 1 sample. Frequently reused or
moderately consequential = 2-3 cases. High-stakes = hand to a dedicated
evaluation process — do not improvise one here. Never build a full parallel
non-persona workflow by default.

## Door 4 trials

When a one-off panel runs as a trial (SKILL.md, door 4), the same blind
protocol applies with two changes: sample A/B are the in-house answer and the
panel's synthesis (personas allowed, since the user asked for them), and both
pass the SOURCE CHECK first when sourced, so the judge compares checked
outputs. Record the verdict as a row in the user's field-evidence log (consent first;
`scripts/field_gate.py where` prints its path).

## Self-check (is agent-studio beating a plain answer?)

A normal door 4 run compares its answer with the baseline, but the
orchestrator judges that comparison itself: not blind, same model, and the
author of the panel. The self-check makes it blind, for one model run, because
every panel run already holds both answers.

Run it when either holds:
- at door 4 step 7, `python3 <skill-dir>/scripts/field_gate.py due` prints
  `due` (no self-check row in the last 30 days), the session is interactive,
  and the run is not already a trial: offer it, one sentence, with its cost
  (one run);
- the user asks whether agent-studio is worth it, or beats asking directly.

How: the blind protocol above, with sample A/B = the panel's answer
(`deliverable.md`, else `synthesis.md`) and `baseline.md`, labels randomized,
judged by a `judge` seat on the second model family (CODEX SEAT COMMAND),
on the run's deciding criterion, one harm check, and source fidelity when
sourced. Unblind. If the baseline wins, "The baseline can bind" applies
(`hard-rules.md`) before anything is delivered.

Record it as a row in the user's log (consent first) with a task heading that
starts `self-check:`, e.g. `### 2026-11-02: self-check: pricing decision
review`, and `Judged by: blind second-family judge`. When the user asks how
the skill has done, answer from the `self-check:` rows in both logs (wins,
losses, mixed, and over what period); if there are none, say so and offer one
on the current run.

## Outcomes

Record in `work-samples/<role>/verdict.md` — exactly one of (tell the user the
result in the warm phrasing from `voice.md`):

- **Open the role** — proceed to hiring (Stage 8).
- **Keep in-house** — no meaningful lift. Record what the playbook keeps.
- **Persona harm** — the prototype made the work worse. ALWAYS reported
  separately from no-lift; name the harm.
- **Narrower only** — useful for a narrower assignment; apply the narrowing
  rule (`job-description.md`) and re-sample if the narrow framing was not what
  was tested.
- **Unclear** — run ONE additional case or revise the prototype once; then
  decide. No infinite retries.

A work sample proves the ROLE beats in-house on its slice. It does not prove
the end-to-end workflow improved (that is Stage 11), and it does not select the
named persona (that is Stage 8).
