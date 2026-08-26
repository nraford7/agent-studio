# Panel recipes by use case

Pick the panel shape from the task, not by habit. "Vary by" is the axis you make
members differ on. "Size" counts generator lenses, plus any critic. Isolation means
each lens is produced in its own subagent with no cross-talk before the combine step.

| Use case | Vary by | Size | Topology | Combine | Non-negotiable rule |
|---|---|---|---|---|---|
| Factual / has a right answer | do NOT ensemble | 1 | single pass | self-consistency or vote | debate wastes money here |
| Analytical judgment / decision review | functional stance | 3-5 + 1 critic | parallel, isolated | reconcile (dissent-carrying) | isolate, then add a devil's-advocate |
| Creative ideation / divergent generation | stance + method | 4-6 | parallel, strict isolation, no debate | human selector + diversity-preserving | never let lenses see each other; measure output diversity; flavor-forward guardrails apply (hard-rules.md) |
| Creative direction / taste judgment | stance | 3-5 + 1 critic | parallel, isolated | dissent-carrying + human final judge | human owns the taste call; do not max spread; flavor-forward guardrails apply (hard-rules.md) |
| Strategy / positioning / options | stance + values | 4-6 | parallel isolated (optional 1 debate round) | dissent-carrying, preserve minority | ground values in real positions, not invented |
| Normative / ethics / value-laden | values | 3-5 | parallel isolated | preserve disagreement, no forced consensus | use different model families |
| Forecasting / estimation | evidence framing | 5-9 | parallel isolated | variance-aware aggregate, not naive mean | keep the private/minority signal |
| Artifact / skill review | review dimension | 3-6 + verifier | parallel isolated, then verify stage | dedup + severity-rank | verify each finding adversarially |

Two rules cut across every row: **generate in isolation**, and **never
naive-mean-blend** the results (see `synthesis-modes.md`). Panel size beyond ~6
generators mostly adds cost, not coverage, except forecasting where extra
independent samples help.

The "Artifact / skill review" row serves the Existing-workflow path's review stage
(legacy "diagnose"): when a reviewed workflow contains a review/audit stage, this
is the recipe it lands on.

Creative rows run under the flavor-forward guardrails; judgment rows under the
strict rulebook. See hard-rules.md #Guardrails switch by mode.

## Overlays and progressive exposure

For a **durable** result (reusable staffed workflow or standing team), a recipe
may sit inside a methodology overlay (`methodologies/overlays/`) that adds phases,
artifacts, and checkpoints on top of the row above — scenario-planning,
terrain-mapping, or root-cause. The overlay is staff-neutral: it never pre-staffs
a persona. Lightweight panels use the row alone, no overlay.

When more than three generators run in parallel, or a row uses more than one
round, apply **progressive exposure** (`hard-rules.md`): isolated outputs →
summaries + dissent → clustered reading → full transcripts only if integration
needs them. Small panels (the common one-off) skip staging and generate in one
isolated round.
