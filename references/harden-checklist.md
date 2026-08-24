# Harden checklist

Audit an existing panel/ensemble against the failure modes the evidence documents,
chiefly consensus-collapse and synthesis-flattening. Score every item PASS / FAIL /
N-A with the default severity given, and give each FAIL a one-line fix.
Recommend-only: the output is a report; the target is never modified.

## The ten checks

1. **Lenses generated in isolation** (not persona-swaps in one shared context)?
   [source: hard-rules.md #Generate lenses in strict isolation; #Never persona-swap in one shared context]
   Severity: HIGH. Fix: one isolated subagent per lens, fresh context each.
2. **A dedicated critic / devil's-advocate present?**
   [source: hard-rules.md #Anti-conformity is first-class]
   Severity: HIGH. Fix: add a critic lens (steelman, then challenge).
3. **Members genuinely heterogeneous** (stance/values), not surface variants?
   [source: hard-rules.md #Members must be genuinely heterogeneous]
   Severity: MED. Fix: re-author members to differ in stance/values, not tone.
4. **Different model families for high-stakes normative panels?**
   [source: hard-rules.md #Different model families for high-stakes normative panels; recipes.md #Normative / ethics row]
   Severity: MED. Fix: move at least the adversary to another model family.
5. **Combine mode is dissent-carrying** (not naive-mean-blend / summarize-to-consensus)?
   [source: hard-rules.md #Never naive-mean-blend; synthesis-modes.md #Reconcile]
   Severity: HIGH. Fix: switch the combine prompt to majority + labeled dissents.
6. **De-duplication before combining?**
   [source: hard-rules.md #Never naive-mean-blend; synthesis-modes.md #"De-duplicate by embedding BEFORE combining"]
   Severity: MED. Fix: embed + collapse near-duplicate lenses before the combiner.
7. **Round cap + stopping rule on any debate?**
   [source: hard-rules.md #Anti-conformity is first-class]
   Severity: MED. Fix: cap at one round; stop when a round adds no new labeled dissent.
8. **Diversity measured at the OUTPUT stage**, not just generation?
   [source: hard-rules.md #Always co-report quality AND coverage; synthesis-modes.md #"measure diversity at the OUTPUT stage"]
   Severity: LOW. Fix: run the diversity metric on the post-synthesis set too.
9. **Quality AND coverage co-reported** (not one scalar)?
   [source: hard-rules.md #Always co-report quality AND coverage]
   Severity: LOW. Fix: report a quality note and a coverage/diversity note together.
10. **Population-level check** (individually-aligned members can be collectively misaligned)?
    [source: hard-rules.md #Vet the population, not just each member]
    Severity: MED. Fix: check consensus concentration and whether dissent survives to the output.

## Report template

Write the report to `agent-studio-out/hardening-<slug>.md` in exactly this shape:

```markdown
# Hardening audit: <target>

Verdict: <e.g. "3 HIGH gaps: no critic, naive blend, shared-context lenses">

| # | Check | Result | Severity | Fix |
|---|---|---|---|---|
| 1 | Isolation | PASS / FAIL / N-A | HIGH | <one line, if FAIL> |
| ... | | | | |

Next: build with /agent-studio construct|ensemble
```

The verdict line leads with the count and names of HIGH gaps. N-A is for checks
that genuinely do not apply (e.g. no debate round exists, so no round cap needed).
