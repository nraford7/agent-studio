# agent-studio Fix Cycle — Design Spec

Date: 2026-08-25
Status: draft for review
Builds on: cycle-1 (construct+ensemble, da87833) and cycle-2 (diagnose+harden, 9e376d4)

## Problem statement

Two independent reviews (a Claude start-to-finish review and a fresheyes/codex
review, which converged on six findings and together produced 18 major + 3 minor)
found that the skill's evidence rules translated faithfully but its runtime
mechanics did not: script paths break on install, the output-stage diversity step
is unexecutable on the main path, the dissent-carrying synthesis prompt overrides
recipe-specific combine modes, the critic never sees the outputs it must challenge,
and the guardrails are global where the user explicitly wants them mode-switched
(strict for judgment work, flavor-forward for creative work). This cycle applies
the reconciled fixes surgically.

## Scope

IN: the 10 fixes below. OUT (deferred, recorded in the manifest): behavioral
golden-fixture QC tier; operationalized population-level metrics; corpus
provenance headers; diagnose/harden report regression harness.

## The fixes and their success criteria (each measurable)

F1 SCRIPT PATHS. All script invocations in SKILL.md are skill-root-qualified: a
new "Locating the scripts" note tells the executor to resolve the skill's base
directory (the directory containing this SKILL.md, reported when the skill loads)
into `<skill-dir>` and every command reads `python3 <skill-dir>/scripts/...`.
Criterion: `grep -q "python3 scripts/" SKILL.md` returns NOTHING (no bare
invocation remains); the Diagnose-mode reference to the TARGET workflow's
`scripts/` directory is explicitly exempt (it must stay target-relative); README
Deploy section unchanged in meaning.

F2 OUTPUT-STAGE DIVERSITY. SKILL.md stage 6 and synthesis-modes.md closing rule
distinguish: (a) SET outputs (creative options, scenarios) — run diversity.py
across the set (as now); (b) SINGLE synthesis.md — run diversity.py over
[lens1..lensN, synthesis.md] and read the per-pair distances of the synthesis vs
each lens. Interpretation (correct direction): a dissent-CARRYING synthesis
contains material from every lens, so it sits roughly equidistant from all of
them; FLATTENING shows when the synthesis is markedly FARTHER from the outlier
lens than from the majority cluster (the dissent was dropped). Pair the distance
check with a mechanical grep of synthesis.md for the labeled minority/dissent
sections (their absence is itself a FAIL). Update diversity.py's docstring
output-stage wording to match (folded from F10c). Criterion: stage 6 names both
cases with this interpretation; no instruction requires diversity.py on a single
file; the dissent-section grep is stated.

F3 PER-RECIPE SYNTHESIS. Assemble writes synthesis-prompt.md carrying the prompt
for the RECIPE's combine mode. synthesis-modes.md gains short paste-ready prompts
for Vote and Selection (Reconcile already has one; Concatenate needs none beyond a
heading instruction; diversity-preserving/variance-aware get a one-line
instruction each; the Selection prompt carries a note that on creative rows the
selector is the HUMAN per the mode-switched guardrails, never the judge prompt). harden-checklist item 5 scores the combine mode AGAINST THE
RECIPE: mismatch = FAIL (HIGH only when the recipe called for dissent-carrying;
otherwise MED), match = PASS; when the audited panel declares NO recipe (prose or
grep ingest), the auditor infers the row from task type or scores item 5 UNKNOWN
(the F8 state). Criterion: synthesis-modes.md contains >=3 fenced prompts;
checklist item 5 references "the recipe's mode" and the no-recipe rule.

F4 CRITIC INPUTS. SKILL.md stage 4 + hard-rules.md state: the critic runs AFTER
the generating lenses and RECEIVES their outputs; isolation applies to generators
only. hard-rules.md gains a CRITIC PREAMBLE variant (the generator preamble's
rule 2 "you cannot see them" is false for the critic): the critic sees all lens
outputs, must steelman each before challenging, and must not manufacture
consensus. Criterion: `grep -i critic SKILL.md | grep -qi "receiv"` passes; the
critic preamble block exists in hard-rules.md.

F5 POSITIONS BLOCK. persona-template.md gains an optional `## Positions` block
(substantive stances/red lines the persona would defend): REQUIRED for
strategy/normative/value-laden recipes and opinionated creative lenses; off by
default for neutral analytical lenses. Judgment work: positions grounded in real,
citable stances; creative: may be authored for flavor. Lint note updated
(Positions present when the recipe requires it). SKILL.md Assemble verifies
members differ in positions/conclusions, not just tone. Criterion: template has
`## Positions` with the required/optional rule; Assemble mentions position
divergence.

F6 MODE-SWITCHED GUARDRAILS. hard-rules.md gains a "Guardrails switch by mode"
section: JUDGMENT mode (fact-finding, evaluation, decision review, forecasting,
normative) = strict (demographics off, stereotype-probe QC, grounded positions);
CREATIVE mode (ideation, creative direction, divergent options) = flavor-forward
(strong/exaggerated personas encouraged; cliche-check replaces stereotype-probe —
lazy archetypes flatten into one voice; HUMAN selection of options mandatory, the
skill never picks the winner; do-not-max-spread still applies; demographics stay
OFF-BY-DEFAULT in creative mode too — flavor comes from stance/method/taste, and a
demographic label needs the same explicit task justification as elsewhere).
persona-template.md carries a one-line pointer; recipes.md creative rows
reference the mode; diagnose-rubric.md and harden-checklist.md state that a
flavor-forward creative persona is NOT a bias failure but a cliche persona IS.
Criterion: the section exists; all four referencing files point at it.

F7 DRIFT / RE-ANCHORING. persona-template.md gains a short "Long-running use"
subsection (drift toward the default assistant over long conversations; re-inject
the persona file at intervals or on drift signs — re-anchor, do not reset; keep
identity text separate from task context). harden-checklist gains an 11th item
(drift management for reused personas; severity LOW; N-A for one-shot panel
lenses). Criterion: subsection exists; checklist has 11 items with >=11 source
citations (the new one cites the template subsection).

F8 HARDEN EVIDENCE MODEL. harden-checklist report template gains an Evidence
column (file/line/output supporting each verdict) and an UNKNOWN state; declared
intent in panel.md is NOT evidence of runtime behavior (mark UNKNOWN, not PASS).
Criterion: template row shows PASS/FAIL/N-A/UNKNOWN + Evidence column; the
intent-is-not-evidence rule is stated.

F9 DIAGNOSE GATE. diagnose-rubric.md: before recommending a panel for a
judgment-laden stage, apply the three-condition gate (defeasible/normative task?
genuinely heterogeneous members possible? disagreement-preserving combine
possible?) plus a one-line cost sanity check; failing the gate → "single strong
pass". Classifier fix: mechanical means the ANSWER is recoverable, not merely
that a rubric exists; fixed-rubric scoring whose items require judgment (like
harden itself) is judgment-laden. Criterion: gate section exists with the three
conditions; "scoring against a fixed rubric" no longer sits in the mechanical
list unqualified.

F10 SCRIPT FIXES + DOC ACCURACY. (a) diversity.py: files that tokenize to zero
tokens are skipped with a stderr warning; if <2 usable files remain, exit 2 with
a clear message; new test: two empty files do NOT yield score 1.0. (b)
exemplar_find.py find: de-duplicate results by domain+title similarity; output
documented (script docstring + README) as LEADS (titles+URLs) for the model layer
to resolve into named people; `--n` validated >= 1 (argparse type check); 
`--max-usd` REMOVED (unimplemented; strip from the script docstring/argparse —
README never documented it, so no README change needed). New test:
`--n 0` exits with argparse error. (c) Doc accuracy: diversity.py/README "never
hard-fails" reworded to "never fails for a missing API key; exit 2 only on
unusable inputs"; exemplar_find docstring + hard-rules "curl only" scoped to page
fetching (API calls to Exa/OpenAI use urllib over HTTPS — not WebFetch, not page
scraping). Criterion: new tests pass; old 8 tests pass; the reworded claims
appear.

## Approach

Three chunks, ordered so references land before SKILL.md references them:
C1 scripts + tests (F10a/b), C2 references (F3 prompts, F5, F6, F7, F8, F9, F10c
wording in hard-rules), C3 SKILL.md + README (F1, F2, F3 assemble-side, F4, F5
assemble-side, F10c wording; ALSO update the stale counts F7/F8 create:
SKILL.md "Run the ten checks" -> "eleven checks, PASS/FAIL/N-A/UNKNOWN", README
"ten-point checklist" -> "eleven-point"). Surgical edits only; no renames; no behavior
removals beyond `--max-usd`.

## Alternatives considered

- Full rebuild of the ensemble runtime as scripts: rejected — the skill is
  prompt-orchestrated by design; the reviews fault specific mechanics, not the
  architecture.
- Deferring mode-switched guardrails to a v3: rejected — explicit user decision,
  and it interlocks with F3/F5 (per-recipe behavior) landing now.

## Blast radius / rollback

Markdown + two scripts + tests, all in this repo. Construct/ensemble flows keep
their shape; only invocation paths, stage-6 measurement, and per-recipe prompt
selection change behavior. Rollback = git revert of the fix commit(s).

## Open questions

None. All decisions were taken in the reviewed instruction.
