---
name: agent-studio
description: Use when the user asks for a panel, council or team of agents or personas, "N perspectives on X", a persona or specialist agent designed, whether a specialist would help with some work, a reliable way to get an outcome done, or an existing skill, workflow or panel reviewed or hardened. Triggers on "/agent-studio", "build a panel", "run an ensemble", "get N perspectives on X", "would a specialist help", "construct a persona", "design how this work gets done", "diagnose this skill", "audit this panel".
---

# agent-studio

Decides whether AI work needs a persona at all, and when it does, hires, runs
and checks one. The central rule:

> Keep work in-house by default. Use a persona or panel only where the task
> matches a plausible persona benefit and the value is shown: by a blind test,
> a trial against a single-model baseline, or evidence strong enough to waive
> it. Then let the user hire and shape the named persona who fills the role.

A successful run may create no persona. Read each referenced file; never improvise around the hard rules.

Artifacts go to `agent-studio-out/` in the user's cwd (one `<slug>/` per job;
door 4 runs in `<slug>/run-<timestamp>/`), never this repo. Field-evidence rows
go to `~/.agent-studio/field-evidence.md` (`field_gate.py where`). The
roster of kept personas lives at `~/.agent-roster/`
(`references/roster.md`). Scripts live in this skill's directory: resolve
`<skill-dir>` = the folder holding this SKILL.md and call
`python3 <skill-dir>/scripts/...`.

## Hard rules (always; full text in `references/hard-rules.md`)

- **Speak as a hiring advisor, not a system.** Lead with your recommendation, talk
  in people and roles, keep stages, scripts, file paths and scores backstage.
  Every user-facing line follows `references/voice.md`.
- **In-house is the default.** Job titles, famous names and biographies are never
  proof of capability. Familiarity never bypasses the evidence gate.
- **Isolation.** One fresh subagent per generating lens, SUBAGENT PROMPT
  PREAMBLE first. Never persona-swap inside one shared context.
- **Second model family.** The critic runs on Codex by default (CODEX SEAT
  COMMAND); high-stakes normative panels also move one lens there.
- **Never naive-mean-blend.** Combine per `references/synthesis-modes.md`; at most
  one debate round.
- **SOURCE CHECK.** Any output stating facts or figures from given sources,
  in-house or panel, is checked claim by claim against them before the user
  sees it.
- **Baseline.** Every panel also runs one plain single-model pass on the same brief
  (skip only on the user's word). Co-report a quality note and a coverage note.
- **Field evidence.** `field_gate.py check "<family>"` before any gate decision
  (`references/field-evidence.md`); add a row (consent first) after every comparison.
- **NO WebFetch anywhere**: `curl` raw pages only, carried into every subagent prompt.
- Guardrails switch by mode (strict for judgment, flavor-forward for creative).
  Persona harm is always reported apart from "no lift". The user owns hiring and
  final taste and value calls. Roster writes need consent first.

## Four front doors

Route by what the user asked for; when unclear, ask (non-interactive: pick the
door whose OBJECT matches, and note the alternative). If the object is a door
2 or 3 job but the user explicitly asks for a panel, do that door's in-house
work AND run the panel as a door 4 trial against it.

| Request sounds like | Door |
|---|---|
| "I want a reliable way to accomplish X" | **1. Design the work** — full lifecycle, `references/full-lifecycle.md` |
| "Review/improve this skill or workflow" · "diagnose" · "harden" | **2. Existing workflow** — `references/full-lifecycle.md`, Existing-workflow path |
| "Would a specialist who does X help?" · "construct a persona" | **3. Consider a specialist** — `references/full-lifecycle.md`, from Stage 1 in compressed form |
| "Get N perspectives on X" · "run a panel" — today's answer | **4. One-off panel** — below |

Doors 1-3 run the eleven-stage lifecycle (Stage 1 brief to Stage 11 review); durable outputs add the
Durable teams machinery (Durability gate, `methodologies/kernel.md`, `methodology-selection.md`, Team
Charter, `scripts/team_validate.py`). Load `references/full-lifecycle.md`; never run them from memory.

## One-off panel (door 4)

1. **Frame.** Restate the goal and help; pick the recipe row (`references/recipes.md`)
   and state the expected model runs (seats + critic + baseline + checks). One
   structured question approves minds and shape; skip if given or non-interactive.
2. **Gate.** Classify the task family, name the runner-up family and why it does
   not apply, then read the conclusion (`references/evidence-gate.md`, with its
   field override and the output-bound-to-sources rule). Then:
   - "Research supports trying this" (or a roster waiver in the same family):
     run the panel. Options to pick from on the "Creative ideation" row take the
     light path, N + 2 runs (`references/recipes.md` #Divergence delivery).
   - Anything else: answer in-house with a one-line reason, under the SOURCE
     CHECK when sourced, and offer the full lifecycle. **Trial:** if the user
     explicitly asked for a panel, team, experts or perspectives, also offer to
     run it as a trial: the panel and the in-house answer side by side, judged
     blind. Say plainly what research expects for this kind of task; run it if
     the user agrees or the run is non-interactive. A trial uses the "Analytical
     judgment" row ("Coverage review" when the job is finding gaps), replaces the
     anonymous prototype, and writes `trial-card.md`: 2-3 judging criteria, one
     harm check, source fidelity when sourced, and the user's format rules.
3. **Hire.** Compressed Stage 8 (`references/full-lifecycle.md`): one slate per
   seat (non-interactive: hire your pick), 2-3 contrasting candidates led by
   their focus, kept roster personas included and labelled (`references/voice.md`),
   persona files per `references/persona-template.md`, lint clean. Cast card
   before dispatch (name · role · what they hunt · one signature "never").
4. **Assemble.** `panel.md` + `synthesis-prompt.md` from the recipe row.
   Members must differ in POSITIONS, not tone. For the "Coverage review" row,
   the single-model checklist pass runs first.
5. **Run.** In `agent-studio-out/run-<timestamp>/`, write `run.md` first (goal,
   recipe, gate, expected runs, lenses, artifacts; shape in `scripts/run_check.py`):
   - one isolated subagent per lens (PREAMBLE first) → `<lens>.md`; for a
     writing job each lens writes a full draft in the user's format;
   - `run_check.py <run-dir>`: rerun a missing or thin lens once, BEFORE the
     critic sees the set; if it fails again, name the missing seat to the user;
   - the critic after them, on Codex by default (CRITIC PREAMBLE) → `critic.md`;
   - the BASELINE: one fresh single-model subagent, same brief, same inputs,
     the best plain instructions you can write, no persona, no panel material
     → `baseline.md`. In a trial this IS the in-house answer (one run).
6. **Synthesize** once `run_check.py <run-dir> --all` passes, in a fresh subagent per
   the recipe's combine mode (`references/synthesis-modes.md`) → `synthesis.md`,
   plus `deliverable.md` when the user's format is tight ("Tight formats" there).
7. **Check.**
   - SOURCE CHECK on what the user receives (`deliverable.md`, else
     `synthesis.md`) and on `baseline.md` when sourced; fix, re-check.
   - Claim coverage check → `coverage.json`, scored by
     `scripts/coverage_report.py`; one re-synthesis if a lens was silenced.
   - The user's format rules on deliverable and baseline, checked mechanically.
   - Compare against the baseline. Normal run: what the panel added, and what
     the single pass had that it lost; when the single pass wins on the deciding
     criterion, deliver it instead (`hard-rules.md` #The baseline can bind).
     Trial: blind A/B per `references/work-sample.md` in `run-<timestamp>/trial/`,
     judged on `trial-card.md` by a judge on the second model family, then unblind.
8. **Report.** The delivered answer (the panel's, or the baseline when it won —
   say which), the quality note, the coverage line ("kept 11 of 14 points;
   dropped ..."), the source-check line, what the panel added over one pass,
   and actual runs against expected (also into `run.md`). Then a review per
   hire, a field-evidence row (consent first), roster upkeep (`references/roster.md`).

## Reference map

| File | Read when |
|---|---|
| `references/hard-rules.md` | always; preambles, SOURCE CHECK PROMPT, CODEX SEAT COMMAND |
| `references/voice.md` | before any user-facing line |
| `references/evidence-gate.md`, `references/field-evidence.md` | every gate decision; field-evidence after every comparison |
| `references/recipes.md`, `references/synthesis-modes.md` | choosing a panel shape; combining lenses; claim coverage check |
| `references/persona-template.md` | writing any persona |
| `references/roster.md` | before hiring; after a run (consent) |
| `references/full-lifecycle.md` | doors 1-3; Stage 8 hiring detail |
| `references/job-description.md` | Stage 5 |
| `references/work-sample.md` | Stages 6-7; door 4 trials |
| `references/doit-handoff.md` | Stages 2, 9, 10 |
| `references/team-charter.md`, `references/team-package.md` | durable outputs, Stages 8 and 10 (`templates/team.json.md`, `templates/team-readme.md`) |
| `references/diagnose-rubric.md`, `references/harden-checklist.md` | door 2 analysis-only report; door 2 panel audit |

## Scripts

- `run_check.py <run-dir> [--all]`: run manifest + every lens present and substantive (`--all`: listed artifacts too); exit 1 if not.
- `field_gate.py check "<family>" [--sourced] | where`: field override from both logs; user log path.
- `coverage_report.py <coverage.json>`: kept / dropped points per lens; exit 1 if a lens was silenced.
- `exemplar_find.py find|corpus`: candidate leads (needs `EXA_API_KEY`) and corpus pull via curl.
- `diversity.py FILE...`: optional spread score (word overlap only without `OPENAI_API_KEY`); `team_validate.py <team.json>`: durable package structure.
