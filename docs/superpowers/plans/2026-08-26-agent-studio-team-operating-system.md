# Plan: Agent Studio Team Operating System Integration

Spec: `docs/superpowers/specs/2026-08-26-agent-studio-team-operating-system-design.md`
Rung: light · Lens (every review pass): existing behavior preserved (four entry paths, eleven stages, existing dossiers, `pytest` still green) + MIT attribution preserved.

## Approach

Absorb Agent Designer's mechanisms into agent-studio as staff-neutral, evidence-gated machinery. Create 11 files, modify 10. All new prose matches the existing warm-but-precise repo voice and the `voice.md` layer. Adapted material from agent-designer (kernel + 3 overlays + manifest/template/validator shapes) is attributed in `THIRD_PARTY_NOTICES.md`. **No file may contain the banned word `ship*`** (enforced by `tests/test_docs.py::test_no_banned_word`, which scans SKILL.md + README.md + every `references/*.md`).

Five chunks, sequential (E depends on A–D). Light rung: one Stage-1 review subagent per chunk on that chunk's diff; a surviving BLOCKER/SUBSTANTIVE escalates the whole run to medium. Verification gate = `python3 -m pytest -q` on the combined result before commit.

Source for adapted material: agent-designer @ github.com/dbmcco/agent-designer v0.2.0 (MIT, © 2026 Braydon McCormick), reviewed commit recorded in THIRD_PARTY_NOTICES.md at build time.

---

## Chunk A — Methodology layer (4 new files)

**Deliverable:** a versioned kernel + three staff-neutral overlays that describe work before staffing.

- [ ] `methodologies/kernel.md` — 10 universal operating rules, adapted from designer's kernel v1.0.0 with attribution header. Rule 1 uses the spec's **middle path** verbatim intent: facilitator never analyzes when ≥2 contributors run in parallel; may analyze on solo/small runs. Rules 2–10 per spec §"Studio Methodology Kernel". Header: `Kernel version: 1.0.0`. Include the "conditional recipe decisions" list (critic presence, rounds, model-family diversity, human selection, combine mode) as NOT universal. Studio voice; no `ship*`.
- [ ] `methodologies/overlays/scenario-planning.md` — phases/artifacts/handoffs/checkpoints/budgets/task-family annotations. **Staff-neutral**: strip designer's named moderator/personas; no overlay pre-staffs a persona. Add the staffing-implication note (may justify creative/value-bearing perspectives). `Overlay id: scenario-planning`, `Kernel compatibility: 1.0.0`.
- [ ] `methodologies/overlays/terrain-mapping.md` — staff-neutral terrain overlay; staffing implication = usually analytical functions, any personified specialist still owes proof.
- [ ] `methodologies/overlays/root-cause.md` — staff-neutral RCA overlay; staffing implication = defaults to regular agents/tools unless a distinct specialist passes the gate.
- [ ] Each overlay states plainly that it does not pre-staff a persona and does not guarantee a specialist is required (staff-neutrality is checkable text).

**Verify:** files exist; `grep "Kernel version: 1.0.0" methodologies/kernel.md`; each overlay has `Overlay id:` + `Kernel compatibility: 1.0.0`; no `ship*` (`grep -rEi '\bship(ped|ping|s)?\b' methodologies/` empty).
**Acceptance:** kernel rule 1 encodes the middle path; no overlay names a persona/character; each overlay carries the "does not guarantee a specialist" sentence.

---

## Chunk B — Team package (4 new files)

**Deliverable:** the Team Charter reference, the team-package reference, and the manifest + README templates.

- [ ] `references/team-charter.md` — the Stage-8 charter for **durable outputs only** (reusable staffed workflow / standing team). Records the 13 fields from spec §"Team Charter". States: charter approval ≠ candidate approval; lightweight outputs skip it (durability gate). Warm voice.
- [ ] `references/team-package.md` — the compiled-output contract: the `agent-teams/<slug>/` layout from spec §"Compiled output", the discovery mechanism (local `team.json` + README; no central registry; AGENTS.md entry only on user authorization), and the Do-It boundary (Do-It compiles/implements; never executes the substantive job; never reopens staffing).
- [ ] `templates/team.json.md` — manifest field reference per spec §"Team manifest" (schema version, name, slug, purpose, type, durability; status `calibrating|active|dormant|retired`; dates; brief + staffed-spec paths; charter approval record; kernel + overlays; in-house playbooks + regular-agent jobs; specialist ids → JD/binding/persona/evidence/proof; topology + handoffs; exposure + combination rules; exclusions/budgets/checkpoints; run-dir convention; review/status history). Include a valid JSON example.
- [ ] `templates/team-readme.md` — starter README shape for a compiled team package (purpose/durability, kernel+overlays, cast by seat, charter record, how to run, declared exclusions, history).

**Verify:** files exist; `team.json.md` lists all four lifecycle states and has a fenced JSON example; no `ship*`.
**Acceptance:** charter is explicitly durable-outputs-only; manifest example validates as JSON.

---

## Chunk C — Structural validator + tests (2 new files)

**Deliverable:** a deterministic team validator that checks structure only, plus pytest coverage.

- [ ] `scripts/team_validate.py` — Python (matches repo's Python helper convention). Reads a `team.json`, checks: required fields present; valid lifecycle state; safe project-local paths (reject `..`/absolute/traversal); referenced files exist (relative to the team dir); kernel+overlay compatibility (kernel `1.0.0`, overlay ids known); unique role identifiers; each active specialist has evidence + JD + binding + persona + proof links; approval record required before `active`; ensemble contracts (combination + exposure rules) present when topology is parallel. Reports STRUCTURAL readiness only — prints explicit "structure only; does not judge quality/accuracy/performance". Exit 0 pass / non-zero fail with clear messages. CLI: `python3 scripts/team_validate.py <path-to-team.json>`. No network, stdlib only (`json`, `pathlib`, `sys`, `argparse`).
- [ ] `tests/test_team_validate.py` — pytest covering spec §"Validator tests": valid calibrating team; valid active team; missing required fields; path traversal/non-local reference; missing referenced file; incompatible overlay; duplicate role ids; active specialist missing evidence/JD/binding/persona/proof; parallel ensemble missing combination/exposure rules; incomplete calibrating package correctly blocked from `active`. Build fixtures in `tmp_path`.

**Verify:** `python3 -m pytest tests/test_team_validate.py -q` green; `python3 scripts/team_validate.py` on a hand-made good fixture exits 0, on a bad one exits non-zero.
**Acceptance:** validator never asserts quality; all listed negative cases fail validation.

---

## Chunk D — Persona / gate / hiring reference edits (7 modified files)

**Deliverable:** the three-layer persona contract, mode switch with the two gap fixes, and the gate/JD/roster/recipes/handoff wiring — all preserving existing structure the tests rely on.

- [ ] `references/persona-template.md` — add the **three-layer contract** (job binding / character core / **domain retrieval kit**) mapped onto the existing Five-Element headings (keep those headings — `test_docs` and downstream depend on them). Add the **persona mode switch** (judgment vs creative). Judgment mode: stance-first, grounded positions, demographics off, + **caricature probe** for named-real hires + **name-hidden fidelity scoring** (Gap 2). Add the **Gap-1 caveat**: the retrieval kit is operational scaffolding, not evidence — "vocabulary is not proof." Keep "no minimum length; ~1000-word ceiling". Preserve the existing grep lint block. **Guard the worked example** (Vera Cole or any replacement): it must still pass the file's own lint — ≥6 `## ` headings and ≥3 `never ` lines under `## Constraints` — since SKILL runs that lint at runtime.
- [ ] `references/evidence-gate.md` — add one line: retrieval-kit richness never counts toward the gate; vocabulary/fluent queries/named methods are not proof of capability (Gap 1). Keep the four verbatim conclusions (tested).
- [ ] `references/hard-rules.md` — add: (a) Gap-1 retrieval-kit caveat; (b) pointer to the methodology kernel + staff-neutral overlays; (c) progressive-exposure rule; (d) the **durability gate** one-liner (heavy machinery only for reusable/standing). Preserve existing rules + PREAMBLE blocks.
- [ ] `references/job-description.md` — add JD fields for methodology needs, overlay obligations, authority, and package interfaces (spec Stage-5 mapping). Keep role statuses + narrowing rule (structure).
- [ ] `references/roster.md` — add the ownership split: global character core vs local job binding vs local retrieval kit; note lazy migration of existing entries. Keep "CONSENT PRECEDES ANY WRITE" + "Counterfactual check" (tested strings).
- [ ] `references/recipes.md` — cross-reference the overlays and the progressive-exposure trigger for larger panels; keep the eight-row table.
- [ ] `references/doit-handoff.md` — add the durable-output team-package contract to Engagement 2 (compile the locked staffed spec into `agent-teams/<slug>/`; staffing locked; Do-It never reopens hiring, never runs the substantive job). Keep both engagement briefs.

**Verify:** `python3 -m pytest tests/test_docs.py -q` still green; no `ship*` in any `references/*.md`; tested strings intact ("CONSENT PRECEDES ANY WRITE", "Counterfactual check", four gate conclusions, four warm phrasings, role statuses).
**Acceptance:** three-layer contract + mode switch + both gap fixes present; no existing tested string removed.

---

## Chunk E — SKILL.md + README + attribution + doc tests (3 modified + 1 new)

**Deliverable:** wire the new machinery into the dispatcher and README, attribute the source, and lock the new structure with tests.

- [ ] `SKILL.md` — add: the **durability gate** (heavy machinery only for reusable/standing; playbook/solo/one-off stay lean); Stage 3 emits `methodology-selection.md` (kernel+overlays, staffing implications); Stage 8 begins with the **Team Charter for durable outputs** (lightweight skip); the **three-layer persona compiler** + mode switch; **progressive exposure**; the **promotion lifecycle** (one-off → standing needs the abbreviated full lifecycle); pointers to `methodologies/kernel.md`, the three overlays, `references/team-charter.md`, `references/team-package.md`, `templates/team.json.md`, `templates/team-readme.md`, `scripts/team_validate.py`. **Preserve** the four doors and all eleven `Stage N` headings (tested). No `ship*`.
- [ ] `README.md` — add the **Output durability** choices and a short **team package** mention; keep "Four Ways" + the eleven-step "How Agent Studio works" intact; keep MIT. No `ship*`.
- [ ] `THIRD_PARTY_NOTICES.md` (new) — attribute Agent Designer v0.2.0, upstream repo URL, the reviewed source commit SHA (capture at build time via the /tmp clone), MIT license text, © 2026 Braydon McCormick; list which files adapted material (kernel, overlays, team.json/README templates, validator shape); state new Studio policy is distinct from adapted concepts. **Do NOT modify `LICENSE`** (the repo's own MIT © 2026 Noah Raford stays as-is); `THIRD_PARTY_NOTICES.md` supplements it and reproduces the upstream MIT text + upstream copyright line verbatim.
- [ ] Scope note: this is a documentation/structure integration. The spec's "Persona compatibility tests" and "Routing scenarios" are covered as STRUCTURAL doc assertions in `tests/test_docs.py` (headings, layers, mode-switch text, gap-fix strings present) — behavioral/runtime execution of routing scenarios is out of scope for this plan and is exercised when the skill actually runs.
- [ ] `tests/test_docs.py` — ADD (do not remove existing) tests: kernel + three overlays exist; kernel pins `1.0.0`; overlays are staff-neutral (no `## Cast`/named moderator); SKILL mentions the durability gate + methodology-selection + Team Charter; SKILL still has four doors + eleven stages (existing tests already cover — keep); persona-template has the three layers + mode switch + "vocabulary is not proof" + caricature probe; new team files exist; `THIRD_PARTY_NOTICES.md` names Agent Designer + MIT. Extend `test_no_banned_word` scope to include `methodologies/*.md`, `methodologies/overlays/*.md`, and `templates/*.md` (the `references/*.md` glob already covers new references).

**Verify:** `python3 -m pytest -q` fully green (existing + new); `grep -rEi '\bship(ped|ping|s)?\b'` over SKILL.md, README.md, references/, methodologies/ empty; all three mandatory artifacts exist.
**Acceptance:** every spec "Planned repository changes" file created/modified; existing tests still pass; new structure locked.

---

## Blast radius / rollback

Self-contained skill repo; no production/DB/deploy surface. Rollback = `git revert` the build commit(s) on the `spec/team-operating-system` branch. Existing dossiers and tests are additive-only touched (new tests added, existing assertions preserved). If a chunk's review escalates the run to medium, remaining chunks get one fresheyes pass each.

## Open questions
None blocking — file names/manifest fields may be refined in-build per the spec's own "Open questions".
