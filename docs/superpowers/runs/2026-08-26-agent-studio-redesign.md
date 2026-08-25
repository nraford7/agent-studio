# Run: agent-studio-redesign
Instruction: Execute the already-approved implementation plan at docs/superpowers/plans/2026-08-26-agent-studio-redesign.md to completion. Spec and plan are already written, fresheyes-reviewed, and user-approved — do NOT re-derive; execute the 9 tasks in order.
Stage: committing
Rung: light (start-floor light: default — doc-only skill markdown, reversible, no data/money/security/prod)
Spec: docs/superpowers/specs/2026-08-25-agent-studio-redesign.md (approved, committed 67fe3f4)
Plan: docs/superpowers/plans/2026-08-26-agent-studio-redesign.md (approved, committed 58ae2a4)
Agency project: — (execution done directly: the plan pre-specifies verbatim file contents; Agency task ceremony would only copy plan text to disk. Recorded per anti-skip rule; flagged in summary.)
Branch: redesign-evidence-gated

## Scorecards
Pass 1 [code:redesign-diff]: 0B/1S/3C/0R · fixed -/- · velocity = (—→4, escalation no) · judge: n/a-light
  → 1 SUBSTANTIVE (SKILL Stage 9 ensemble-constraint trigger dropped "or evaluate the same artifact") + 3 COSMETIC (README dead link, door-4 layout header attribution, synthesis.md unnamed in SKILL step 6). ALL FIXED in-pass; nothing survived → no escalation, rung stays light.
Verification gate: 21 passed (9 doc + 12 helper). Artifacts: spec ✓ plan ✓ manifest ✓.

## Chunks
- [x] Task 1 — references/evidence-gate.md (verify clean; added 4-verdict list)
- [x] Task 2 — references/job-description.md (verify clean)
- [x] Task 3 — references/work-sample.md (verify clean)
- [x] Task 4 — references/roster.md + persona-template split (verify clean)
- [x] Task 5 — references/doit-handoff.md (verify clean)
- [x] Task 6 — rewrite SKILL.md (all 11 refs present, ship=0)
- [x] Task 7 — update legacy rubrics (gate-wired, stale pointers=0)
- [x] Task 8 — README rewrite (stale-architecture checks all 0)
- [x] Task 9 — tests/test_docs.py (21 passed)

## Notes
- Spec + plan review loops skipped: both artifacts already fresheyes-reviewed and user-approved this session (Codex passes on both; 10 plan findings fixed).
- Execution mechanism: direct authoring rather than Agency. The plan contains exact file contents for every task, so Agency would add ceremony without added correctness. Verification gate (pytest) + a post-build review still run on the combined result.
