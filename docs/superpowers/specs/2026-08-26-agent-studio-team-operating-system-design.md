# Agent Studio Team Operating System Integration

**Date:** 2026-08-26

**Status:** Ready for user review

**Decision:** Integrate Agent Designer's strongest operating mechanisms into Agent Studio while preserving Agent Studio as the single product, evidence authority, and human-like hiring experience.

## Purpose

Agent Studio should become a stronger team builder without becoming a second workflow runtime or losing the thing that makes it distinctive: it mirrors how people build real organizations.

The user defines a job, determines what kinds of people and ordinary automation it needs, writes job descriptions, tests the roles, interviews recognizable candidates, hires a team, and commissions the workflows that team will use. Agent Studio produces that staffed team and its operating package. It does not perform the underlying job itself; the resulting skills, agents, and workflows are used separately.

The integration therefore absorbs the best mechanisms from Agent Designer—methodology kernels, standing-team manifests, overlays, progressive exposure, validation, and promotion—without importing its product shell or turning its predefined panels into a parallel source of truth.

## Design principles

1. **One studio, one evidence authority.** Agent Studio owns routing, role necessity, evidence, job descriptions, qualification, hiring, staffing, and review.
2. **Theatre remains operational.** Named candidates, interviews, hiring decisions, team cards, probation, performance reviews, and rehiring make tradeoffs legible; they are not cosmetic decoration.
3. **Characters never outrank the job.** A vivid candidate cannot compensate for a weak role, missing evidence, or failed proof.
4. **Methods are staff-neutral until staffing is justified.** A methodology describes the work before it suggests who should do it.
5. **Reusable teams are explicit products.** Standing and reusable teams receive a versioned package, manifest, validation, run structure, and lifecycle.
6. **Durability is an output choice, not a new front door.** The existing four ways into Agent Studio remain intact.
7. **Structure can be validated; quality must be evaluated.** Deterministic tooling verifies contracts and references, while model and human judgment assess whether a team is actually good.

## Product model

### Four ways into Agent Studio

The existing public entry paths remain:

1. a vague goal,
2. an existing brief,
3. an existing workflow,
4. an existing agent or team.

Every path converges on the same eleven-stage lifecycle. Existing Agent Designer panels enter through **existing workflow** or **existing agent or team** and are evaluated like any other incumbent design; they do not bypass the evidence gate.

### Output durability

During routing, the user chooses or confirms how durable the result should be:

- an in-house playbook,
- a solo specialist,
- a temporary one-off panel,
- a reusable staffed workflow,
- a standing team or panel.

This choice controls packaging, review, and promotion requirements. It is not a fifth way to start.

### Ownership model

Agent Studio uses two levels of identity:

- **Global character cores** contain stable identity, values, recognizable positions, formative experience, contradictions, blind spots, communication style, re-anchoring cues, and track record.
- **Local job bindings** contain the role, mandate, authority, process, outputs, exclusions, handoffs, constraints, and job-specific retrieval material for one team.

A team package references global cores but owns its bindings, charter, methodology choices, proof, and operating records. This avoids duplicate rosters while allowing the same character to be hired differently for different jobs.

## Methodology layer

### Studio Methodology Kernel

Add a versioned `methodologies/kernel.md`, adapted with attribution from Agent Designer. It defines the universal operating rules for staffed work:

1. the facilitator orchestrates and does not silently become an analyst;
2. contributors work independently before convergence;
3. disagreement is preserved as signal;
4. exposure to other contributors is progressive and intentional;
5. human checkpoints occur at consequential decisions;
6. findings are triaged by minor versus major significance;
7. required artifacts are validated before dependent phases continue;
8. file discipline supports re-entry, audit, and resumption;
9. deterministic checks validate structure while model-mediated checks assess quality;
10. exploration is bounded by explicit time, context, and iteration budgets.

The following remain conditional recipe decisions, not universal requirements:

- whether a critic is present;
- whether work uses multiple rounds;
- whether a high-stakes normative task requires model-family diversity;
- whether a creative result is selected by a human;
- how task-specific outputs are combined.

### Staff-neutral overlays

Add three initial overlays:

- `methodologies/overlays/scenario-planning.md`
- `methodologies/overlays/terrain-mapping.md`
- `methodologies/overlays/root-cause.md`

Each overlay defines phases, artifacts, handoffs, checkpoints, budgets, and task-family annotations. No overlay pre-staffs a persona or guarantees that a specialist is required.

The overlays create different staffing implications:

- **Scenario planning** may justify creative or value-bearing perspectives when divergent authored worlds materially improve the result.
- **Terrain mapping** usually calls for analytical functions; any personified specialist still needs experimental or work-sample proof.
- **Root-cause analysis** defaults to regular agents and tools unless a distinct specialist contribution passes the evidence gate.

Stage 3 produces `methodology-selection.md`, recording the kernel version, chosen overlays, rejected alternatives, compatibility decisions, and staffing implications.

## Team Charter

Stage 8 begins with a Team Charter after roles have passed the evidence gate and before candidates are presented. The charter confirms the organization—not the people—and records:

- purpose and durability;
- selected kernel and overlays;
- open specialist roles and their evidence;
- jobs assigned to regular agents, tools, or deterministic automation;
- topology, sequencing, and handoffs;
- exposure and convergence rules;
- critic and combination logic;
- model constraints where justified;
- time, context, and iteration budgets;
- human checkpoints;
- coverage and deliberate exclusions;
- required artifacts;
- promotion, review, and retirement policy.

If the user rejects the charter, Agent Studio revises the organization before starting candidate theatre. Charter approval must never be treated as candidate approval.

## Persona compiler and hiring

### Three-layer persona contract

Every hired specialist is compiled from three distinct layers:

1. **Job binding** — role, mandate, stance, capabilities, exclusions, trigger, process, output, authority, handoffs, and constraints.
2. **Character core** — name, backstory, values, recognizable positions, formative experience, contradiction, blind spots, communication style, re-anchor cues, and track record.
3. **Domain retrieval kit** — job-relevant vocabulary, methods, tools, recognitions, grounded cases, good and bad research queries, and information or tool requirements.

Stable biographical knowledge belongs in the core. Material that exists because of the current assignment belongs in the local retrieval kit. This separation prevents a character from being rewritten merely to fit a new job.

### Persona mode switch

The compiler explicitly chooses a mode:

**Judgment mode** is stance-first and compact. It uses grounded public positions when a real character is chosen, omits irrelevant demographics, and checks for stereotyping, motivated reasoning, and borrowed authority. Character richness never substitutes for a qualifying experiment or sample.

**Creative mode** permits richer texture, taste, authored positions, formative experience, stronger theatricality, and opinionated language. It adds a cliché check and requires human selection when subjective quality is central.

There is no minimum persona length. The existing approximate 1,000-word maximum remains a ceiling, not a target.

### Hiring theatre is mandatory

Once the charter is approved, each open specialist role follows the full Studio hiring experience:

1. consult the roster before inventing a duplicate character;
2. present two or three named, contrasting candidates;
3. prefer recognizable real, historical, or fictional figures when the fit is grounded and useful;
4. use an original named character when no recognizable figure is responsible or sufficiently grounded;
5. label the Studio's interpretation and distinguish it from sourced fact;
6. explain each candidate's fit, unique contribution, and principal risk;
7. let the user interview, reject, request a new slate, combine, or adjust candidates in natural language;
8. re-present materially altered candidates rather than silently changing them;
9. record the hiring decision, provenance, evidence, and binding;
10. issue a team card after the roster is complete.

The purpose of this theatre is to expose values, assumptions, tradeoffs, and working style in a form people can reason about. It is never cited as evidence that the role itself is necessary.

## Team package

### Dossier additions

The Studio dossier gains two artifacts:

- `methodology-selection.md`
- `team-charter.md`

All existing evidence cards, job descriptions, qualification records, candidate records, personas, team cards, staffed specifications, and review artifacts remain in force.

### Compiled output

When the result is reusable or standing, Stage 10 hands a locked staffed specification to Do-It. Do-It compiles the team into a target contract equivalent to:

```text
agent-teams/<slug>/
  team.json
  README.md
  methodology/
    kernel.md
    overlays/
  bindings/
    <role>.md
  personas/
    <name>.md
  templates/
  runs/
```

The exact physical layout may be adapted when the target is a reusable skill, but the same logical contracts and references must survive. Agent Studio decides who and how; Do-It implements the package. Neither Stage 10 nor the package automatically executes the team's substantive work.

### Team manifest

`team.json` records:

- schema version, team name, slug, purpose, type, and durability;
- status: `calibrating`, `active`, `dormant`, or `retired`;
- creation and update dates;
- brief and staffed-specification paths;
- charter approval record;
- methodology kernel and overlays;
- in-house playbooks and regular-agent jobs;
- specialist identifiers and their job descriptions, bindings, personas, evidence, and proof;
- topology and handoffs;
- exposure and combination rules;
- exclusions, budgets, and checkpoints;
- run-directory convention;
- review and status history.

Local `team.json` plus `README.md` are the discovery mechanism. An `AGENTS.md` entry may be added only when the user authorizes it. This design does not create a second central team registry.

### Structural validator

Add `scripts/team_validate.py`. It checks:

- required fields and valid lifecycle states;
- safe, project-local paths;
- referenced files exist;
- kernel and overlay compatibility;
- unique role identifiers;
- required evidence, job description, binding, persona, and proof links;
- approval requirements before a team can be `active`;
- ensemble contracts such as combination and exposure rules where applicable.

The validator reports structural readiness only. It must not claim that a persona is accurate, that the methodology is wise, or that the team will perform well.

## Progressive exposure and convergence

Progressive exposure becomes a first-class choice when any of these apply:

- more than three contributors generate in parallel;
- an overlay requires more than one convergence round;
- the projected context budget is material;
- a standing team must be resumable.

The default sequence is:

1. isolated full outputs;
2. contributor summaries and explicit dissent statements;
3. clustered reading of relevant full outputs;
4. full transcript exposure only when integration or audit genuinely requires it.

The staffed specification records who sees what, when, why, and how conclusions are combined. Context limits may trigger summarization, narrowing, or a fresh run, but never silent omission of a contributor.

## Promotion and lifecycle

A successful one-off panel is not automatically a standing team. Promotion requires an abbreviated but complete Studio lifecycle:

1. restate the reusable brief;
2. review each contributor's distinct contribution;
3. create an evidence card and job description for every retained specialist seat;
4. run the normal qualification proof;
5. reuse existing character cores where appropriate, with fresh local bindings;
6. approve a Team Charter;
7. compile and validate the package through Do-It.

Standing teams then use the existing probation and performance-review mechanisms, extended to cover methodology effectiveness, role drift, package status, and retirement. A contributor may be re-anchored, narrowed, replaced, moved back to a regular-agent job, or retired.

## Eleven-stage lifecycle mapping

1. **Intent Brief** — unchanged; captures the job, stakes, constraints, and starting path.
2. **Workflow Design** — remains staff-neutral; may use overlay phase requirements without naming personas.
3. **Staffing Review** — selects methodology and separates in-house work, regular agents, tools, and possible specialist roles.
4. **Evidence Gate** — remains the sole authority for whether a personified role may exist.
5. **Job Description** — adds methodology needs, overlay obligations, authority, and package interfaces.
6. **Role Prototype** — remains anonymous and tests the role rather than a character.
7. **Work-Sample Qualification** — remains anonymous and records pass, fail, or redesign evidence.
8. **Persona and Hiring** — begins with the Team Charter, then uses the full real-character candidate and interview process plus the three-layer compiler.
9. **Staffed Specification** — adds kernel, overlays, durability, progressive exposure, checkpoints, and the package contract.
10. **Do-It Handoff** — implements and validates the team or skill; it does not depend on a Pi-specific runtime and does not perform the user's substantive job.
11. **Performance Review** — evaluates contribution, drift, methodology effectiveness, promotion, lifecycle status, and manifest updates.

## Failure handling

- **No specialist passes the gate:** retain the method as a regular workflow or in-house playbook.
- **Charter rejected:** revise the organization and do not present candidates yet.
- **Character conflicts with the job:** the job description wins; rebind or recast the character.
- **Named figure lacks responsible grounding:** use an original character, request sources, or narrow the claimed interpretation.
- **Overlays conflict:** choose one, create a reviewed custom overlay, or document an intentional composition.
- **Context budget is exceeded:** summarize, narrow, or start a new run; never silently drop evidence or dissent.
- **A required artifact is missing:** retry once, then mark the run incomplete and stop dependent phases.
- **Do-It is unavailable:** deliver the dossier and locked package contract, but do not claim an active team exists.
- **Performance degrades:** re-anchor, narrow, replace, revise the method, return work to a regular playbook, or retire the package.

## Compatibility and migration

- The four ways into Agent Studio and the eleven stages remain stable.
- Existing dossiers remain valid; no bulk rewrite is required.
- Roster entries migrate lazily when next used.
- Historical one-off panels are not promoted automatically.
- Existing staffed specifications are treated as kernel-only until deliberately upgraded.
- The Five-Element persona headings remain recognizable while gaining explicit binding, core, and retrieval-kit sections.
- Existing Agent Designer panels enter through the normal incumbent-review paths and receive no special exemption.
- No Pi-specific execution dependency is introduced.

## Planned repository changes

### Create

- `methodologies/kernel.md`
- `methodologies/overlays/scenario-planning.md`
- `methodologies/overlays/terrain-mapping.md`
- `methodologies/overlays/root-cause.md`
- `references/team-charter.md`
- `references/team-package.md`
- `templates/team.json.md`
- `templates/team-readme.md`
- `scripts/team_validate.py`
- `tests/test_team_validate.py`
- `THIRD_PARTY_NOTICES.md`

### Modify

- `SKILL.md`
- `README.md`
- `references/hard-rules.md`
- `references/evidence-gate.md`
- `references/job-description.md`
- `references/persona-template.md`
- `references/recipes.md`
- `references/roster.md`
- `references/doit-handoff.md`
- `tests/test_docs.py`

## Provenance

The implementation must identify Agent Designer v0.2.0, its upstream repository, and the reviewed source commit in `THIRD_PARTY_NOTICES.md`; preserve its MIT attribution for adapted material; and clearly distinguish imported or adapted concepts from new Agent Studio policy.

`agent-designer-comparison.md` is design input, not a runtime dependency and not a file that the integration modifies by default.

## Verification strategy

### Documentation and contract checks

Verify that:

- kernel and overlay documents contain their required contracts;
- overlays are staff-neutral and do not pre-assign characters;
- the README still describes four ways into Studio and eleven stages;
- the distinction between building a team and using that team remains explicit;
- Stage 8 separates charter approval from candidate approval.

### Validator tests

Cover:

- a valid calibrating team;
- a valid active team;
- missing required fields;
- path traversal or non-project-local references;
- missing referenced files;
- incompatible overlay declarations;
- duplicate role identifiers;
- an active specialist missing evidence, job description, binding, persona, or proof;
- a parallel ensemble missing combination or exposure rules;
- an incomplete calibrating package that is correctly prevented from becoming active.

### Persona compatibility tests

Cover:

- old and new persona records;
- rejection of an ungrounded judgment-mode real character;
- acceptance of deliberately authored creative-mode texture;
- correct ownership between global core, local binding, and retrieval kit;
- retention of the Five-Element interface.

### Routing scenarios

Exercise at least these end-to-end cases:

1. a factual workflow where no persona is justified;
2. a creative brief where a richly characterized candidate is justified and selected by a human;
3. terrain mapping where a proposed specialist still owes qualification proof;
4. root-cause analysis that stays with regular agents;
5. promotion of a one-off panel requiring contribution review, evidence, job descriptions, proof, charter, and compilation;
6. a standing team that resumes from stored artifacts using progressive exposure;
7. a rejected charter that produces no candidates;
8. a Do-It handoff where staffing is locked and implementation cannot reopen hiring.

### Regression

Run the existing documentation, schema, routing, persona, evidence-gate, and handoff tests in addition to the new suite.

## Success criteria

The integration is complete when:

1. Agent Studio remains the sole user-facing product and evidence authority.
2. The four entry paths and eleven stages remain understandable and intact.
3. Users still experience job definition, job descriptions, candidate slates, interviews, hiring, team cards, probation, performance review, and rehiring.
4. Recognizable real, historical, and fictional characters remain supported with responsible interpretation labels.
5. Every personified seat still passes evidence, job-description, prototype, and work-sample gates.
6. Staff-neutral methodology selection happens before hiring.
7. The Team Charter is approved separately from candidate selection.
8. Persona records cleanly separate binding, core, and retrieval kit.
9. Judgment and creative persona modes have different safeguards.
10. Standing and reusable teams have manifests, local discovery, run structure, validation, and lifecycle status.
11. Progressive exposure and combination rules are explicit for larger ensembles.
12. One-off panels cannot silently become standing teams.
13. Agent Designer mechanisms are attributed and do not create a permanent runtime dependency.
14. Existing Agent Studio dossiers remain usable without bulk migration.
15. Do-It implements the locked staffed design without reopening staffing.
16. The resulting team or skill is used separately to perform the substantive job.
17. Automated tests distinguish structural validity from actual team quality.

## Non-goals

This integration does not:

- claim deterministic proof that a persona has authentic expert judgment;
- assign predefined characters merely because an overlay exists;
- replace the evidence gate with methodology preference;
- remove or flatten the Studio's real-character theatre;
- add a fifth public entry path;
- create a second roster or central team registry;
- move implementation responsibility out of Do-It;
- bulk-rewrite historical dossiers;
- require Pi as an execution environment;
- maximize persona length, panel size, or number of rounds as goals in themselves.

## Rejected alternatives

### Wholesale merge

Rejected because it would import a parallel product shell, predefined staffing assumptions, and runtime-specific structure that conflict with Studio's evidence-first lifecycle.

### Permanent Stage 8 dependency

Rejected because Studio would become dependent on another skill at the most important authorship boundary, splitting ownership of evidence, character construction, and hiring records.

### Keep both systems separate

Rejected because it would preserve duplicated concepts and prevent Studio from gaining durable team manifests, methodology overlays, progressive exposure, and a clear promotion path.

## Open questions

None block implementation planning. File names and manifest fields may be refined during the plan, but the ownership boundaries, hiring experience, evidence gate, methodology layer, package lifecycle, and Do-It boundary are design commitments.
