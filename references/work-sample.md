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

1. The in-house assistant performs the slice with the best appropriate playbook.
2. A fresh subagent performs the same slice AS the prototype — same model, same
   information, same tools, same reasonable effort. Its prompt opens with the
   SUBAGENT PROMPT PREAMBLE from `hard-rules.md`.
3. The orchestrator saves both outputs under neutral labels in RANDOM order to
   `agent-studio-out/<slug>/work-samples/<role>/sample-A.md` and `sample-B.md`.
   The A/B assignment is held in the orchestrator's context only — NOT written
   anywhere the evaluator could read.
4. The user (or an evaluator subagent that has NOT seen either generation)
   judges A vs B on the Evidence Card's evaluation signal: 2-3 criteria tied to
   the intended persona effect, plus the one harm check. Write the judgment to
   `verdict.md`; only THEN write the mapping to `key.md` and unblind.

Scaling: low-stakes reversible roles = 1 sample. Frequently reused or
moderately consequential = 2-3 cases. High-stakes = hand to a dedicated
evaluation process — do not improvise one here. Never build a full parallel
non-persona workflow by default.

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
