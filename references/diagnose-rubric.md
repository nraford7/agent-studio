# Diagnose rubric

How to map a target workflow into stages and judge, stage by stage, where a
persona/panel earns its keep and where it is waste. Recommend-only: the output is
a report, never a modification of the target.

## Classify each stage

Classify every stage of the target as one of two types. Rule of thumb: **could a
test assert the output?** If yes, it is mechanical.

**MECHANICAL** (single recoverable right answer):
- retrieval / search / fetching
- parsing, extraction, deterministic transforms
- citation or format verification, link checking
- computation, counting, scoring against a fixed rubric
- file operations, packaging, export

**JUDGMENT-LADEN** (interpretation, no single right answer):
- synthesis framing, prioritization, "what matters here"
- design and creative direction
- strategy, positioning, option generation
- evaluation / critique / taste calls
- question generation, scoping, framing
- normative or value-laden calls

## Map to a recipe

- JUDGMENT-LADEN stages map to a row of `recipes.md` by use case (analytical
  judgment, creative ideation, creative direction, strategy, normative,
  forecasting, artifact/skill review). Name the row and the panel shape.
- MECHANICAL stages are marked **"single pass — do NOT ensemble"** with the
  reason: on ground-truth tasks, debate is often a no-op or loses to simple
  voting/self-consistency at higher cost. Adding agents here is waste.

## Existing multi-agent use

If the target already dispatches agents, check and report:
- **Isolation**: separate contexts per agent, or persona-swaps in one shared
  context (flag the latter as the maximally-colluding anti-pattern)?
- **Critic**: is there a dedicated critic/adversary/refuter stage?
- **Family**: is any adversary the same model family as the generator (flag)?
- **Combine mode**: dissent-carrying, vote, selection, or a naive blend (flag)?

## Report template

Write the report to `agent-studio-out/diagnosis-<slug>.md` in exactly this shape:

```markdown
# Diagnosis: <target>

| Stage | Task type | Ensemble? | Recommended recipe | Rationale |
|---|---|---|---|---|
| <stage> | mechanical / judgment-laden | yes / no | <recipes.md row, or "single pass"> | <one line> |

## Where agents help
<the judgment-laden stages worth a panel, each with its recipe row>

## Where they would be waste
<the mechanical stages, with the debate-loses-to-voting reason>

## Gaps
<missing critic, same-family adversary, no output-stage diversity check, etc.>

Next: build with /agent-studio construct|ensemble
```

Recommend-only: no persona files are generated, nothing in the target is edited,
no subagents are dispatched. The report ends with the build pointer above.
