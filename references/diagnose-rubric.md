# Diagnose rubric

How to map a target workflow into stages and judge, stage by stage, where a
persona/panel earns its keep and where it is waste. Recommend-only: the output is
a report, never a modification of the target.

## Classify each stage

Classify every stage of the target as one of two types. Rule of thumb: **could a
test assert the output?** If yes, it is mechanical. Mechanical means the ANSWER
is recoverable, not merely that a rubric exists — fixed-rubric scoring whose
items themselves require judgment (like this skill's own harden audit) is
judgment-laden.

**MECHANICAL** (single recoverable right answer):
- retrieval / search / fetching
- parsing, extraction, deterministic transforms
- citation or format verification, link checking
- computation, counting, scoring where the ANSWER is mechanically recoverable
  (exact matching, counting)
- file operations, packaging, export

**JUDGMENT-LADEN** (interpretation, no single right answer):
- synthesis framing, prioritization, "what matters here"
- design and creative direction
- strategy, positioning, option generation
- evaluation / critique / taste calls
- question generation, scoping, framing
- normative or value-laden calls

## Map to a recipe

A judgment-laden stage is mapped through the Persona Evidence Gate
(`evidence-gate.md`), not by judgment-ladenness alone:

1. Classify the stage into ONE task family from evidence-gate.md; its
   deterministic conclusion decides the recommendation.
2. "Research supports trying this" families (creative divergence, value-laden
   deliberation): recommend the matching `recipes.md` row IF genuinely
   heterogeneous members are constructible and the combine step can preserve
   disagreement; else "single strong pass".
3. "Supported only for a narrower analogous use" / "Promising, but
   experimental" families: recommend "in-house now; a role is possible via a
   narrowed/blind work sample" — name the proof owed. Never recommend the
   panel as if proven.
4. "No research-backed reason" families (forecasting, factual/checkable/
   procedural): mark **"single pass — do NOT ensemble"** with the reason: on
   ground-truth tasks, debate is often a no-op or loses to simple
   voting/self-consistency at higher cost. For forecasting, ensembling
   EVIDENCE FRAMINGS in-house (recipes.md row) is fine; a persona hire is not
   inferred.
Cost sanity still applies: a panel costs N+1 subagent runs — is this stage's
decision worth that?

## Existing multi-agent use

If the target already dispatches agents, check and report:
- **Isolation**: separate contexts per agent, or persona-swaps in one shared
  context (flag the latter as the maximally-colluding anti-pattern)?
- **Critic**: is there a dedicated critic/adversary/refuter stage?
- **Family**: is any adversary the same model family as the generator (flag)?
- **Combine mode**: dissent-carrying, vote, selection, or a naive blend (flag)?

## Creative stages

When diagnosing creative stages, apply the flavor-forward guardrails
(hard-rules.md #Guardrails switch by mode): strongly opinionated lenses are the
design, not a bias defect; flag cliche/archetype-collapse instead.

## Report template

Write the report to `agent-studio-out/diagnosis-<slug>.md` in exactly this shape:

```markdown
# Diagnosis: <target>

| Stage | Task type | Task family | Evidence conclusion | Ensemble? | Recommended recipe | Rationale |
|---|---|---|---|---|---|---|
| <stage> | mechanical / judgment-laden | <family, or —> | <conclusion, or —> | yes / no | <recipes.md row, or "single pass"> | <one line> |

## Where agents help
<the judgment-laden stages worth a panel, each with its recipe row>

## Where they would be waste
<the mechanical stages, with the debate-loses-to-voting reason>

## Gaps
<missing critic, same-family adversary, no output-stage diversity check, etc.>

Next: /agent-studio — door 2 (existing workflow) runs the full staffing lifecycle from this diagnosis.
```

Recommend-only: no persona files are generated, nothing in the target is edited,
no subagents are dispatched. The report ends with the build pointer above.
