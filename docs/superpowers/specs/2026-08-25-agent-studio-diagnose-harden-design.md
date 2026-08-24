# agent-studio — Diagnose + Harden Design Spec (cycle 2)

Date: 2026-08-25
Status: draft for review
Builds on: `2026-08-25-agent-studio-design.md` (construct + ensemble, delivered)

## Problem statement

The delivered agent-studio does two things: construct a persona, and build/run a
panel. Two further uses were deferred: **diagnose** (point the skill at an existing
workflow and find where agents/panels would actually help, and where they would be
waste) and **harden** (audit an existing ensemble for the known failure modes,
chiefly consensus-collapse). Both are pure ANALYSIS passes: they read a target,
judge it against the same evidence rules the skill already encodes, and emit a
report. They do not generate agent specs and do not modify the target. When the
report says "add a panel here," the user runs the existing construct/ensemble
features to build it.

The value is discipline: the evidence shows that adding agents everywhere backfires
(debate loses to voting on ground-truth tasks; ensembles collapse to consensus).
Diagnose is therefore mostly a tool for saying where NOT to add agents; harden is a
tool for catching the specific ways a panel silently flattens.

## Scope

IN scope:
- **DIAGNOSE** — accept a skill directory/path OR a prose workflow description; map
  it into stages; classify each stage; emit a stage-by-stage report of where a
  persona/panel helps, where it is waste, and what recipe fits.
- **HARDEN** — accept an existing panel (an agent-studio `panel.md`, a prose
  description, or a skill that already uses multiple agents); audit it against the
  anti-conformity / no-flatten checklist; emit a pass/fail report with fixes.

OUT of scope:
- Generating persona/panel specs (that is the existing CONSTRUCT/ENSEMBLE use; the
  report points the user there).
- Modifying the target in place (recommend-only; never silently rewrite).
- Executing anything (no subagent runs; these are read-and-judge passes).

## Success criteria (measurable)

1. `SKILL.md` gains two new triggerable modes, `diagnose` and `harden`, described in
   the frontmatter `description` so they fire on "diagnose this skill / workflow",
   "where would agents help in X", "audit / harden this panel / ensemble".
2. DIAGNOSE on a skill directory reads its files (SKILL.md + scripts + references),
   and writes `agent-studio-out/diagnosis-<slug>.md` containing a stage table with
   columns: Stage | Task type (mechanical vs judgment-laden) | Ensemble? (yes/no) |
   Recommended recipe (or "single pass") | Rationale — plus a "Where agents help",
   "Where they would be waste", and "Gaps" section.
3. DIAGNOSE on a prose description produces the same report shape from the text.
4. HARDEN on a panel writes `agent-studio-out/hardening-<slug>.md`: a checklist of
   the anti-conformity rules (below), each marked PASS / FAIL / N-A with a severity
   and a one-line fix, plus a top-line verdict.
5. Both reports are recommend-only: they contain NO generated persona files and make
   NO edits to the target. Each ends with a "Next: build with /agent-studio
   construct|ensemble" pointer for the flagged items.
6. Every item in `references/harden-checklist.md` cites its source section in
   `references/hard-rules.md` or `references/recipes.md` (grep-verifiable, e.g.
   `[source: hard-rules.md #isolation]`). Three checklist items have no existing
   source and are ADDED to `references/hard-rules.md` in this cycle (additive
   edit): member heterogeneity (stance/values, not surface variants),
   different-model-families for high-stakes normative panels, and the
   population-level check (individually-aligned members can form a collectively
   misaligned group).

## Proposed approach

Both are new analysis stages in the existing `SKILL.md`, sharing a small amount of
new rubric material. No new Python scripts are required: the work is reading local
files (Read/grep) or prose, and judging against the encoded rules. Web access is not
needed; if a target references a URL, `curl` only (never WebFetch).

### DIAGNOSE flow

1. **Ingest the target.** If a path: read `SKILL.md`, list `scripts/` and
   `references/`, and skim them to recover the pipeline. If the path has no
   SKILL.md (arbitrary tool dir or workflow), read the entry document (README or
   the main script) and map stages from that; if nothing readable is found, ask
   the user for a prose description instead. If prose: parse the described
   steps. Produce an ordered list of stages/steps.
2. **Classify each stage** against `references/diagnose-rubric.md` (new): is the
   stage's output a single recoverable-right-answer (mechanical: retrieval, parsing,
   verification, formatting, computation) or a judgment/creative/normative call
   (interpretation, design, strategy, evaluation, prioritization)?
3. **Map judgment stages to a recipe** from `references/recipes.md`; mark mechanical
   stages "single pass — do NOT ensemble" with the reason (debate wastes money /
   loses to voting on ground-truth).
4. **Check existing multi-agent use:** if the target already dispatches agents,
   note whether they are isolated, whether a critic/adversary exists, and whether it
   is same-model-family (flag same-family adversaries).
5. **Emit the report** to `agent-studio-out/diagnosis-<slug>.md` (slug = target
   directory name, or the first 3-4 words of a prose description, kebab-case).
   Recommend-only; end with the build pointer. The same slug rule applies to
   `hardening-<slug>.md`.

### HARDEN flow

1. **Ingest the panel.** From an agent-studio `panel.md`, a prose description, or a
   skill's agent-dispatch code. Detection when handed a directory: prefer
   `agent-studio-out/panel.md` if present; else grep the skill files for agent
   dispatch patterns (Agent tool calls, subagent prompts, "dispatch", "panel",
   "ensemble") and audit those sites; else ask for a prose description.
2. **Run the checklist** in `references/harden-checklist.md` (new), each item
   citing its source section in `hard-rules.md` or `recipes.md` (see criterion 6):
   - Lenses generated in isolation (not persona-swaps in one shared context)?
   - A dedicated critic / devil's-advocate present?
   - Members genuinely heterogeneous (stance/values), not surface variants?
   - Different model families for high-stakes normative panels?
   - Combine mode is dissent-carrying (not naive-mean-blend / summarize-to-consensus)?
   - De-duplication before combining?
   - Round cap + stopping rule on any debate?
   - Diversity measured at the OUTPUT stage, not just generation?
   - Quality AND coverage co-reported (not one scalar)?
   - Population-level check (individually-aligned can be collectively misaligned)?
3. **Score each** PASS / FAIL / N-A with a severity from a fixed scale
   HIGH / MED / LOW. Default severities: HIGH = shared-context collusion,
   no dissent-carrying combine (naive blend), no critic; MED = surface-variant
   members, same-family adversary on normative work, no round cap, no
   de-duplication, no population-level check; LOW = diversity not measured at
   output stage, quality/coverage reported as one scalar. Each FAIL carries a
   one-line fix.
4. **Emit the report** to `agent-studio-out/hardening-<slug>.md` with a top-line
   verdict (e.g. "3 HIGH gaps: no critic, naive blend, shared-context lenses").

### New files

```
references/diagnose-rubric.md    # mechanical-vs-judgment classification + stage-mapping guidance
references/harden-checklist.md   # the anti-conformity/no-flatten checklist (each item cites its source)
```
Plus additions to `SKILL.md` (two new mode sections + frontmatter triggers), and
two additive edits: append the three new rules to `references/hard-rules.md`, and
in `references/recipes.md` replace the stale "DIAGNOSE out of scope" note with the
8th row (Artifact / skill review | review dimension | 3-6 + verifier | parallel
isolated, then verify stage | dedup + severity-rank | verify each finding
adversarially) so diagnosed review-stages have a recipe row to land on.

## Alternatives considered

- **Generate specs / auto-fix.** Rejected per the decision and the evidence: silent
  rewriting of a working target is the failure mode the research warns against.
  Recommend-only keeps a human in the loop; building is the existing use.
- **Separate skill for diagnose/harden.** Rejected: they reuse the recipe table and
  hard rules and naturally live beside construct/ensemble; a separate skill would
  duplicate the rubric.
- **A script to auto-map a skill's stages.** Rejected: stage mapping is a judgment
  the model does well from the files; a parser would be brittle across skill shapes.

## Blast radius / rollback

- Additive: two new reference files + `SKILL.md` sections + two small additive
  edits (three new rules appended to `references/hard-rules.md`; the stale
  "DIAGNOSE out of scope" note in `references/recipes.md` replaced and the 8th
  "Artifact / skill review" row added). Existing construct/ensemble behavior is
  untouched. Reports are read-only outputs to `agent-studio-out/`.
- Rollback = revert the SKILL.md additions and delete the two reference files.

## Open questions

None. (Resolved at spec review: table-first report format confirmed; implicit
harden-input detection confirmed with the directory heuristic above.)
