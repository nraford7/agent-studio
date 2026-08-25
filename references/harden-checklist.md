# Harden checklist

Audit an existing panel/ensemble against the failure modes the evidence documents,
chiefly consensus-collapse and synthesis-flattening. Score every item PASS / FAIL /
N-A / UNKNOWN with the default severity given, and give each FAIL a one-line fix.
Evidence rule: every verdict cites its evidence (file/line/output). Declared
intent (panel.md) is NOT evidence of runtime behavior — if only intent exists
for a runtime check, score UNKNOWN, not PASS.
Mode note: a flavor-forward creative persona (strong opinions, exaggeration) is
NOT a bias failure — but a CLICHE persona is (archetype collapse flattens
diversity). See hard-rules.md #Guardrails switch by mode.
Recommend-only: the output is a report; the target is never modified.

## The eleven checks

1. **Lenses generated in isolation** (not persona-swaps in one shared context)?
   [source: hard-rules.md #Generate lenses in strict isolation; #Never persona-swap in one shared context]
   Severity: HIGH. Fix: one isolated subagent per lens, fresh context each.
2. **Critic / devil's-advocate present when the recipe row calls for one?**
   Score against the panel's `recipes.md` row (or infer the row from task
   type): rows listing a critic (analytical judgment, creative direction,
   artifact review) FAIL at HIGH without one; rows without a mandatory critic
   (creative ideation, normative, forecasting) score N-A. No inferable recipe:
   UNKNOWN.
   [source: recipes.md table; hard-rules.md #Anti-conformity is first-class]
   Severity: HIGH when the row requires it. Fix: add a critic lens (steelman,
   then challenge).
3. **Members genuinely heterogeneous** (stance/values), not surface variants?
   [source: hard-rules.md #Members must be genuinely heterogeneous]
   Severity: MED. Fix: re-author members to differ in stance/values, not tone.
4. **Different model families for high-stakes normative panels?**
   [source: hard-rules.md #Different model families for high-stakes normative panels; recipes.md #Normative / ethics row]
   Severity: MED. Fix: move at least the adversary to another model family.
5. **Combine mode matches THE RECIPE'S declared mode?** Score against the recipe
   row, not against dissent-carrying universally. Mismatch = FAIL (HIGH when the
   recipe called for dissent-carrying, MED otherwise); match = PASS. No declared
   recipe (prose/grep ingest): infer the row from task type, or score UNKNOWN.
   [source: recipes.md table; synthesis-modes.md; hard-rules.md #Never naive-mean-blend]
   Severity: HIGH/MED per above. Fix: switch the combine prompt to the recipe's mode.
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
11. **Drift management for REUSED personas** (re-anchoring plan; identity kept
    separate from task context)? N-A for one-shot panel lenses.
    [source: persona-template.md #Long-running use (drift)]
    Severity: LOW. Fix: re-inject the persona file at intervals; re-anchor, do not reset.

## Report template

Write the report to `agent-studio-out/hardening-<slug>.md` in exactly this shape:

```markdown
# Hardening audit: <target>

Verdict: <e.g. "3 HIGH gaps: no critic, naive blend, shared-context lenses">

| # | Check | Result | Severity | Evidence | Fix |
|---|---|---|---|---|---|
| 1 | Isolation | PASS / FAIL / N-A / UNKNOWN | HIGH | <file/line/output> | <one line, if FAIL> |
| ... | | | | | |

Next: /agent-studio — door 2 treats this panel as incumbents and runs the staffing lifecycle.
```

The verdict line leads with the count and names of HIGH gaps. N-A is for checks
that genuinely do not apply (e.g. no debate round exists, so no round cap
needed). UNKNOWN is for checks that cannot be verified from available artifacts
— stated intent alone earns UNKNOWN, never PASS.
