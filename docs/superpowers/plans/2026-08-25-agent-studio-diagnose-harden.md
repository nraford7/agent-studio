# agent-studio Diagnose + Harden Implementation Plan

> **For agentic workers:** Executed via Agency (per the /do-it pipeline). Steps use checkbox (`- [ ]`) syntax. All deliverables are markdown; verification is structural grep checks (no new Python, no new tests).

**Goal:** Add the recommend-only DIAGNOSE and HARDEN analysis modes to the delivered agent-studio skill.

**Architecture:** Additive markdown-only change. Two new reference rubrics, two additive edits to existing references, and two new mode sections + frontmatter triggers in SKILL.md. No scripts, no execution paths, no changes to construct/ensemble.

**Tech Stack:** Markdown; grep for verification.

**Spec:** `docs/superpowers/specs/2026-08-25-agent-studio-diagnose-harden-design.md`

## Global Constraints

- Recommend-only: neither mode generates persona files, modifies the target, or dispatches subagents. Reports only, to `agent-studio-out/`.
- Reuse the existing rubrics: every harden-checklist item cites `[source: hard-rules.md #...]` or `[source: recipes.md #...]`.
- Slug rule: target dir name, or first 3-4 words of prose, kebab-case.
- NO WebFetch (curl only, and only if a target references a URL).
- Construct/ensemble behavior untouched.

---

### Task 1: Additive edits to existing references

**Files:**
- Modify: `references/hard-rules.md` (append 3 rules)
- Modify: `references/recipes.md` (replace stale note + add 8th row)

- [ ] **Step 1:** Append to `references/hard-rules.md`, before the SUBAGENT PROMPT PREAMBLE section, three new `## ` rules:
  - `## Members must be genuinely heterogeneous` — vary stance/values, not surface variants of one voice; surface-variant members add cost without diversity.
  - `## Different model families for high-stakes normative panels` — same-model swarms are low-variance and collude; use different families when the work is normative/value-laden and the stakes are high.
  - `## Vet the population, not just each member` — individually well-aligned members can form a collectively misaligned group; evaluate the panel as a group (consensus concentration, conformity onset), not only per-persona.
- [ ] **Step 2:** In `references/recipes.md`: replace the final paragraph ("The Playbook's 8th row ... out of scope for this version.") with the 8th table row appended to the table: `| Artifact / skill review | review dimension | 3-6 + verifier | parallel isolated, then verify stage | dedup + severity-rank | verify each finding adversarially |` plus one line noting this row serves the DIAGNOSE mode's mapping.
- [ ] **Step 3:** Verify (from repo root /Users/noahraford/Projects/agent-studio): `grep -qi "heterogeneous" references/hard-rules.md && grep -qi "population" references/hard-rules.md && grep -qi "model famil" references/hard-rules.md && grep -qi "dedup + severity-rank" references/recipes.md && ! grep -qi "out of scope for this version" references/recipes.md` (the `dedup + severity-rank` string only exists in the new table ROW, so deleting the stale note alone cannot pass)
- [ ] **Step 4:** Commit: `docs: add heterogeneity/model-family/population rules + review recipe row`.

**Acceptance:** all five grep checks pass.

---

### Task 2: `references/diagnose-rubric.md`

**Files:**
- Create: `references/diagnose-rubric.md`

- [ ] **Step 1:** Write the rubric with sections:
  - `## Classify each stage`: MECHANICAL (single recoverable right answer: retrieval, parsing, citation/format verification, computation, file ops, deterministic transforms) vs JUDGMENT-LADEN (interpretation, synthesis framing, design, strategy, evaluation/critique, prioritization, question generation). Rule of thumb: "could a test assert the output?" → mechanical.
  - `## Map to a recipe`: judgment stages map to a `recipes.md` row by use-case; mechanical stages are marked "single pass — do NOT ensemble" with the reason (debate loses to voting on ground-truth tasks at higher cost).
  - `## Existing multi-agent use`: what to check when the target already dispatches agents — isolated vs shared context, critic/adversary present, same-model-family adversary (flag), combine mode.
  - `## Report template`: the exact diagnosis-report skeleton — stage table (Stage | Task type | Ensemble? | Recommended recipe | Rationale), then `## Where agents help`, `## Where they would be waste`, `## Gaps`, ending with the build pointer line `Next: build with /agent-studio construct|ensemble`.
- [ ] **Step 2:** Verify: `grep -qi "mechanical" references/diagnose-rubric.md && grep -qi "single pass" references/diagnose-rubric.md && grep -qi "Where agents help" references/diagnose-rubric.md && grep -qi "Next: build with /agent-studio" references/diagnose-rubric.md`
- [ ] **Step 3:** Commit: `docs: add diagnose rubric`.

**Acceptance:** all four grep checks pass; report template includes the five named columns.

---

### Task 3: `references/harden-checklist.md`

**Files:**
- Create: `references/harden-checklist.md`

- [ ] **Step 1:** First READ references/hard-rules.md (as updated by Task 1) so citations use its exact section headings. Then write the checklist with these TEN items, EACH with `[source: hard-rules.md #<section>]` or `[source: recipes.md #<row/section>]`:
  1. Lenses generated in isolation (not persona-swaps in one shared context)?
  2. A dedicated critic / devil's-advocate present?
  3. Members genuinely heterogeneous (stance/values), not surface variants?
  4. Different model families for high-stakes normative panels?
  5. Combine mode is dissent-carrying (not naive-mean-blend / summarize-to-consensus)?
  6. De-duplication before combining?
  7. Round cap + stopping rule on any debate?
  8. Diversity measured at the OUTPUT stage, not just generation?
  9. Quality AND coverage co-reported (not one scalar)?
  10. Population-level check (individually-aligned can be collectively misaligned)?
  Each item also carries a default severity (HIGH: shared-context collusion, naive blend/no dissent-carrying combine, no critic; MED: surface-variant members, same-family adversary on normative work, no round cap, no de-duplication, no population-level check; LOW: diversity not measured at output stage, one-scalar reporting), and a one-line fix suggestion.
- [ ] **Step 2:** Add the `## Report template` section: hardening-report skeleton — top-line verdict (e.g. "3 HIGH gaps: ..."), the checklist with PASS/FAIL/N-A + severity + fix per item, ending with the build pointer line.
- [ ] **Step 3:** Verify: `test $(grep -c "source:" references/harden-checklist.md) -ge 10 && grep -q "HIGH" references/harden-checklist.md && grep -qi "Next: build with /agent-studio" references/harden-checklist.md`
- [ ] **Step 4:** Commit: `docs: add harden checklist`.

**Acceptance:** >=10 source citations; severities present; template included.

---

### Task 4: SKILL.md modes + README + integration verify

**Files:**
- Modify: `SKILL.md` (frontmatter description + two new mode sections)
- Modify: `README.md` (uses list + scope section)

- [ ] **Step 1:** Extend the SKILL.md frontmatter `description` to also trigger on: "diagnose this skill/workflow", "where would agents help in X", "audit/harden this panel/ensemble". Keep it one description string.
- [ ] **Step 2:** Update the SKILL.md intro sentence ("Two uses: construct ... and ensemble ...") to name all FOUR uses (construct, ensemble, diagnose, harden — the last two recommend-only analysis modes). Then add `## Mode: Diagnose` after the six stages: ingest (path with SKILL.md → read it + scripts/ + references/; path without → entry document; nothing readable → ask for prose; prose → parse steps), classify per `references/diagnose-rubric.md`, map to `references/recipes.md`, check existing multi-agent use, emit `agent-studio-out/diagnosis-<slug>.md` per the rubric's template. State recommend-only explicitly (no generation, no modification, no execution) and the slug rule.
- [ ] **Step 3:** Add `## Mode: Harden`: ingest (panel.md preferred; else grep for dispatch patterns; else ask for prose), run `references/harden-checklist.md`, score PASS/FAIL/N-A + severity, emit `agent-studio-out/hardening-<slug>.md` per the checklist's template. Recommend-only stated.
- [ ] **Step 4:** Update README.md: change "Two uses" to "Four uses" (construct, ensemble, diagnose, harden — the last two recommend-only analysis modes), and update the Scope section to say diagnose/harden are now included.
- [ ] **Step 5:** Smoke-run DIAGNOSE against this repo itself (the executor follows the new Mode: Diagnose section on /Users/noahraford/Projects/agent-studio): confirm `agent-studio-out/diagnosis-agent-studio.md` is produced with the 5-column stage table, the three prose sections, and the build-pointer line; confirm no file outside agent-studio-out/ changed (`git status --short` shows only intended edits). Delete the smoke-run output dir afterward (it is gitignored anyway).
- [ ] **Step 6:** Verify (from repo root):
  `grep -qi "diagnose" SKILL.md && grep -qi "harden" SKILL.md && grep -qi "recommend-only\|recommend only" SKILL.md && grep -qi "diagnosis-" SKILL.md && grep -qi "hardening-" SKILL.md && head -6 SKILL.md | grep -qi "diagnose" && grep -qi "diagnose" README.md && python3 -m pytest -q`
  (pytest confirms the existing suite still passes — no code touched.)
- [ ] **Step 7:** Commit: `feat: diagnose + harden analysis modes`.

**Acceptance:** all greps pass; frontmatter triggers include diagnose/harden; pytest 8/8 green (unchanged code).
