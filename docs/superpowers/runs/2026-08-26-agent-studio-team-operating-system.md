# Run: agent-studio-team-operating-system
Instruction: Implement the approved spec at docs/superpowers/specs/2026-08-26-agent-studio-team-operating-system-design.md end-to-end: integrate Agent Designer's mechanisms (methodology kernel, staff-neutral overlays, team manifest/package, structural validator, progressive exposure, promotion lifecycle, three-layer persona compiler, Team Charter) into agent-studio, honoring the durability gate and the four gap fixes now in the spec. Create and modify all files listed in the spec's "Planned repository changes", add tests, preserve MIT attribution in THIRD_PARTY_NOTICES.md, and run the full test suite to completion.
Stage: committing
Rung: light → **medium** (escalated on a BLOCKER surfaced in post-build review; the one-way ratchet climbed one step)
Lens (carry into EVERY review pass): existing behavior preserved (four entry paths, eleven stages, existing dossiers, existing tests still pass) + MIT attribution preserved.
Spec: docs/superpowers/specs/2026-08-26-agent-studio-team-operating-system-design.md   Plan: docs/superpowers/plans/2026-08-26-agent-studio-team-operating-system.md
Agency project: —

## Scorecards
Spec review: satisfied by prior in-conversation human review + edits (commit 5898f64); light rung requires one pass — the spec is human-approved.
Pass 1 [plan]: 0B/4S/2C/0R · fixed -/- · velocity = (—→6) · judge: n/a-light — all 4 substantive folded into the plan pre-execution.
Pass 1 [code:all-chunks] (3 parallel independent reviewers): 1B/4S/5C/0R · fixed -/- · velocity = · judge: n/a-medium — BLOCKER (validator symlink-escape) + 4 SUBSTANTIVE (validator exit code; Windows/URL paths; active in-house-only team; jd/binding path conflation). Escalated light→medium.
Pass 2 [code:fix-delta]: 0B/0S/0C/0R · fixed 5/5 prior · velocity ↓ (10→0) · judge: n/a-medium — every finding fixed and test-encoded; full suite 50 passed. Fix-delta verified by 8 new targeted tests (symlink escape, exit codes, Windows/URL rejection, in-house-only active, no-false-positive dup, dir-not-file).

## Verification gate
`python3 -m pytest -q` → 50 passed (42 existing+new doc/structure, incl. 8 new validator fix-tests). Banned-word sweep clean. Validator smoke: bad manifest → exit 1, missing file → exit 2.

## Chunks
- [x] A — Methodology layer (kernel + 3 overlays)
- [x] B — Team package (charter, package ref, 2 templates)
- [x] C — Validator + tests
- [x] D — Persona/gate/hiring reference edits (7 files)
- [x] E — SKILL + README + attribution + doc tests

## Notes
- Spec was authored + reviewed + committed (5898f64) before /do-it invocation; treating it as the approved spec draft. Start-floor evaluator still ran on it → light.
- Plan review (light, 1 subagent pass): 0 blockers, 4 substantive catches — all folded into the plan pre-execution (LICENSE untouched + supplementary notice; guard persona-lint worked example; reworded broken overlay bullet; extend banned-word scan to methodologies+templates; scope note that routing/persona tests are structural doc assertions). Run stays light.
- DEVIATION (surfaced): Step-3 Agency execution replaced by direct chunked authoring + mandatory per-chunk Stage-1 independent review. Reason: the Agency instance is functional but `agency_status` returns 63KB+ payloads, making a 21-file prose-authoring task-loop impractical; direct authoring against the detailed spec yields higher fidelity and the review discipline (the actual value) is fully preserved. Not a silent skip — recorded here and in the end summary per the skill's surface-the-wall rule.
