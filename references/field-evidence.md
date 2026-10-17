# Field evidence

What happened when panels or persona roles were tested on real work, against a
plain single-model baseline. The research corpus (`docs/research/`) says what
other people found; this file says what happened here. Read it at the evidence
gate (`evidence-gate.md`) and before proposing any panel.

## How to use it

- Before a gate decision, run
  `python3 <skill-dir>/scripts/field_gate.py check "<family>"` (add `--sourced`
  when the job's output is bound to given sources). It reads this file and the
  user's own log together and applies the rules below; quote its line.
- A family whose most recent row says the panel or role did WORSE than the
  baseline on the deciding criterion drops one confidence level until a newer
  row reverses it (see `evidence-gate.md`, "Field override").
- Mixed results (better on one criterion, worse on another) do not change the
  level, but the gate names the weaker criterion as a required evaluation
  signal for any new role in that family.
- A row marked `Bound to sources: yes` counts only for jobs whose output is
  bound to sources; a row without it counts for every job in the family.

## How to add a row

Add one row after every trial run, work sample, or Stage 11 review that
compared a panel or role against a baseline. One row per comparison. Ask the
user before writing (same consent rule as the roster). Rows go to the user's
own log, never this file: `python3 <skill-dir>/scripts/field_gate.py where`
prints its path (`~/.agent-studio/field-evidence.md`) and creates it if
missing. This file is the bundled seed log and grows only by pull request,
at summary level (this repo is public): no confidential or client-identifying
detail.

| Field | What to write |
|---|---|
| Date | YYYY-MM-DD |
| Task | one line, generalized |
| Family | starts with one of the eight families in `evidence-gate.md` |
| Bound to sources | yes / no: was the output bound to given sources |
| Verdict | worse / better / mixed / same, panel vs baseline on the deciding criterion |
| Weaker criterion | the criterion the panel lost on, or none |
| Compared | what ran against what (seats, models, baseline) |
| Judged by | blind judge / user / both; criteria |
| Result | per criterion: panel better / same / worse, with numbers if any |
| What fixed it | any non-persona step that changed the result |
| Source | path to the report |

## Rows

### 2026-08-26: literature-search coverage audit
- Family: General critique or analytical judgment
- Bound to sources: no
- Verdict: mixed
- Weaker criterion: breadth (scope checklist items caught)
- Compared: 4 isolated persona lenses + adversarial verifier (all Claude) vs the stock single-model coverage script, same corpus
- Judged by: author review of both gap lists
- Result: breadth (scope checklist items caught): panel WORSE. Depth (base rates, effect sizes, definitions): panel BETTER. False positives: panel better (verifier removed one). Cost: panel worse. One seat (policy lens) produced zero usable gaps on a non-policy topic.
- What fixed it: a cheap single-model checklist pass BEFORE the panel, its gaps exempt from the panel's cap (now the "Coverage review" recipe row).
- Source: deep-research-squad skill build notes (local, not in this repo)

### 2026-09-16: deck hook writing from a source document
- Family: Creative divergence (hook writing), output bound to a source
- Bound to sources: yes
- Verdict: worse
- Weaker criterion: fidelity to source
- Compared: 3-lens persona hook panel vs a ~300-word single-writer prompt vs the full Narrative Engine, 4 sources, blind judge (gpt-6-astra)
- Judged by: blind judge on hook, chain, fidelity to source, naturalness
- Result: fidelity: panel WORSE (3.3 vs 7.3 on 10). The judge's verdict: persona panels at the hook stage are refuted for this use.
- What fixed it: a separate evidence reviewer holding the source (fidelity 9.5 on re-test, 2026-09-23). Now the SOURCE CHECK in `hard-rules.md`.
- Source: Narrative Engine ablation report and 2026-09-23 re-test (local, not in this repo)

### 2026-10-17: weekly multi-sector briefing (sector blocks + cross-sector summary)
- Family: Factual, checkable, or procedural work (source-bound writing), run as a trial on the user's request
- Bound to sources: yes
- Verdict: mixed
- Weaker criterion: logic and unsupported causal claims (sector blocks)
- Compared: (a) per-sector block: retired-executive persona per sector vs a plain writer, same rules and evidence, 13 sectors; (b) cross-sector summary: 13 isolated persona takes then a house-persona synthesis vs one plain pass over all material. All authors on one model family; judge, source checks, coverage and critic on a second family
- Judged by: blind judge on logic, insight, clarity (plus stated disagreement for the summary); separate source check per output; claim coverage check
- Result: cross-sector summary: panel BETTER on insight and stated disagreement, fewer unsupported claims, slightly lower clarity. Sector blocks: MIXED (persona better in 7 of 13, plain in 6): persona better on insight, worse on logic, more unsupported causal claims; the only contradicted claim came from a persona's "what it means for operators" line
- What fixed it: one synthesis revision naming the silenced lenses plus the critic's notes (first draft dropped 4 of 13 lenses; after revision all present). Recommended: a separate check on any interpretive callout, since code checks on figures do not read it
- Source: user's local trial report (not in this repo)
