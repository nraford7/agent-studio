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
| Coverage review (find what is missing against a scope) | review dimension | single-model checklist pass + 3-5 lenses + verifier | checklist pass FIRST (walk every scope item and named technique, mark absent/thin), then parallel isolated lenses for depth | union: checklist gaps first and outside the cap, then lens gaps severity-ranked under the cap | panels skip the obvious; the checklist catches it (field-evidence.md, 2026-08-26) |

Two rules cut across every row: **generate in isolation**, and **never
naive-mean-blend** the results (see `synthesis-modes.md`). Panel size beyond ~6
generators mostly adds cost, not coverage, except forecasting where extra
independent samples help.

The "Artifact / skill review" and "Coverage review" rows describe panels INSIDE a
workflow being designed or reviewed. They do not license dispatching a panel
for this skill's own diagnosis: an analysis-only diagnosis (door 2) stays a
single in-house pass unless the user asks for a panel, in which case it runs as
a trial (SKILL.md, door 4 "Trial").

Choosing between them: finding what is missing (gaps, coverage) uses
"Coverage review"; judging the quality of an artifact uses "Artifact / skill
review". The single-model checklist pass belongs to the panel side; a
baseline must never see it.

Every row except the creative ones runs its critic on a second model family by
default (hard-rules.md). Every row whose output states facts from given sources
gets the SOURCE CHECK (hard-rules.md).

Creative rows run under the flavor-forward guardrails; judgment rows under the
strict rulebook. See hard-rules.md #Guardrails switch by mode.

## Divergence delivery (door 4 light path)

Use it when BOTH hold: the recipe row is "Creative ideation / divergent
generation", and the user wants options to react to or pick from, not a pick
or a recommendation ("a spread of ideas", "brainstorm, I'll choose"). If the
user asks which option is best, or the output is bound to sources, run the
full door 4 protocol instead.

The run, in this order, N + 2 model runs:

1. N isolated lenses (4-6), PREAMBLE first → `<lens>.md`.
2. The BASELINE: one plain single-model pass on the same brief → `baseline.md`.
   It stays: it is one run, and it is the only comparison this path has.
3. `scripts/run_check.py <run-dir>`, as in the full protocol (no model run).
4. One fresh subagent assembles the SET (`synthesis-modes.md`,
   "Diversity-preserving set"): de-duplicated, no winner, no merging, every
   item tagged with its source lens or `[plain]` for baseline items, so the
   user sees what the panel added over one pass → `synthesis.md`.

Dropped on this path, because the human selector replaces them: the critic,
the claim coverage check and its script (the tags show every lens survived:
check that each lens name appears in `synthesis.md`), the trial, and the
blind judge. State the run count in the Frame step (`N + 2`), and report
actual runs at the end like any other run.

Field evidence: when the user picks, note whether the picks came from lens
items or `[plain]` items. That is the comparison; record it as a row with
consent, like any other.

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
