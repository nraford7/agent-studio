# Panel recipes by use case

Pick the panel shape from the task, not by habit. "Vary by" is the axis you make
members differ on. "Size" counts generator lenses, plus any critic. Isolation means
each lens is produced in its own subagent with no cross-talk before the combine step.

| Use case | Vary by | Size | Topology | Combine | Non-negotiable rule |
|---|---|---|---|---|---|
| Factual / has a right answer | do NOT ensemble | 1 | single pass | self-consistency or vote | debate wastes money here |
| Analytical judgment / decision review | functional stance | 3-5 + 1 critic | parallel, isolated | reconcile (dissent-carrying) | isolate, then add a devil's-advocate |
| Creative ideation / divergent generation | stance + method | 4-6 | parallel, strict isolation, no debate | human selector + diversity-preserving | never let lenses see each other; measure output diversity |
| Creative direction / taste judgment | stance | 3-5 + 1 critic | parallel, isolated | dissent-carrying + human final judge | human owns the taste call; do not max spread |
| Strategy / positioning / options | stance + values | 4-6 | parallel isolated (optional 1 debate round) | dissent-carrying, preserve minority | ground values in real positions, not invented |
| Normative / ethics / value-laden | values | 3-5 | parallel isolated | preserve disagreement, no forced consensus | use different model families |
| Forecasting / estimation | evidence framing | 5-9 | parallel isolated | variance-aware aggregate, not naive mean | keep the private/minority signal |

Two rules cut across every row: **generate in isolation**, and **never
naive-mean-blend** the results (see `synthesis-modes.md`). Panel size beyond ~6
generators mostly adds cost, not coverage, except forecasting where extra
independent samples help.

The Playbook's 8th row, "Artifact / skill review", is deliberately omitted here: it
maps to the DIAGNOSE use, which is out of scope for this version.
