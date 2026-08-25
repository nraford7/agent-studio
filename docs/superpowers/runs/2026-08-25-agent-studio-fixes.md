# Run: agent-studio-fixes
Instruction: /do-it fix cycle, start light cap medium — apply the reconciled findings from the two independent reviews (Claude + fresheyes): script paths, output-stage diversity, per-recipe synthesis, critic inputs, Positions block, mode-switched guardrails, drift/re-anchoring, harden evidence model, diagnose gate, script/doc fixes.
Stage: done
Rung: light (start-floor: user override "start light"; cap medium — do NOT go heavy)
Spec: docs/superpowers/specs/2026-08-25-agent-studio-fixes-design.md   Plan: docs/superpowers/plans/2026-08-25-agent-studio-fixes.md
Agency project: 01a035d6-6361-75b8-a5fa-668ee2d7b00e (reuse)

## Scorecards
Pass 1 [spec]: 1B/4S/5C/0R · fixed -/- · velocity = (—→10, escalation no) · judge: n/a-light  (B1 centroid-interpretation inversion corrected + S1-S4/C1-C5 all fixed inline)
Pass 1 [plan]: 0B/6S/6C/0R · fixed -/- · velocity ↓ (10→12, escalation no) · judge: n/a-light  (insertion point, same-line grep, anchor retention, forward-ref note, preamble-intro amendment, eleven-checks heading + cosmetics fixed inline)
Pass 1 [code:fixes]: 0B/3S/5C/0R · fixed -/- · velocity ↓ (12→8, escalation no) · judge: n/a-light  (LEADS wording in stage 2; single-file checks scoped to dissent-carrying; manifest finalized; heading/lint/README/outlier-pointer cosmetics)

## Chunks
- [x] C1 scripts + tests — 12/12 green (4 new tests)
- [x] C2 references — all six files edited, all verify greps pass
- [x] C3 SKILL.md + README — T9 verify pass, full gate green

## Notes
- Fix cycle from dual review (mine + fresheyes FAIL verdict, 18 major/3 minor, reconciled in-session).
- DEFERRED (out of scope, per instruction): behavioral golden-fixture QC; operationalized population metrics; corpus provenance headers; diagnose/harden report regression harness.
- Push to master pre-authorized this session.
- Spec review caught a genuine inversion (B1): the original F2 "centroid-hugging = flattening" reading was backwards; corrected to "synthesis far from the outlier lens = dissent dropped".
- Agency: 9 tasks (FX-T1..T9) assigned under project 01a035d6-...; executed per composed prompts; evaluator round-trips not run (same bounded light-run decision as cycles 1-2, recorded there).
