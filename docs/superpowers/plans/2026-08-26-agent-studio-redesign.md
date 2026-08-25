# Agent Studio Evidence-Gated Redesign — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the agent-studio skill around the approved evidence-gated staffing lifecycle: four front doors, an 11-stage lifecycle with two Do-It engagements, a persona evidence gate, blind work samples, and a global consent-gated roster.

**Architecture:** The skill is a prompt artifact: `SKILL.md` carries the routing and lifecycle; per-stage detail lives in `references/*.md` files the executor reads at each stage. Five new reference files (evidence gate, job description, work sample, roster, Do-It handoff) are added; the existing hard-rules, recipes, synthesis-modes, persona-template, diagnose-rubric, and harden-checklist files survive and are re-pointed. Python scripts and their tests are untouched.

**Tech Stack:** Markdown skill files; existing Python helpers (`scripts/diversity.py`, `scripts/exemplar_find.py`) with pytest.

**Spec:** `docs/superpowers/specs/2026-08-25-agent-studio-redesign.md`

## Global Constraints

- In-house is the default; a specialist role opens only via the evidence gate (spec "Guardrails").
- The four user-facing evidence conclusions are verbatim: "Research supports trying this." / "Supported only for a narrower analogous use." / "Promising, but experimental." / "No research-backed reason to create a role."
- Task-family → conclusion mapping is deterministic (spec Stage 4): creative divergence + value-laden deliberation → supports; grounded simulation + multi-stakeholder subjective evaluation → narrower analogous; sustained functional priority + general critique/analytical judgment → promising-but-experimental; forecasting + factual/checkable/procedural → no research-backed reason.
- Roster waiver predicate (verbatim standard): ≥2 real assignments in the same task family with contributions retained downstream, ≥1 verified by a localized counterfactual contribution check. The waiver never waives the evidence gate itself.
- Roster writes require user consent BEFORE any file is created or appended; track-record entries exclude confidential or project-identifying detail.
- Personification is mandatory for every specialist agent; never an unnamed specialist. Names/biographies are never evidence of capability.
- Ensemble constraints (isolation, heterogeneity, disagreement-preserving synthesis, one-round debate cap) bind only when ≥2 roles answer the same question in parallel; sequential roles get handoff contracts.
- NO WebFetch anywhere, including every subagent prompt emitted (user CLAUDE.md + existing hard rule).
- Artifacts go to `agent-studio-out/` in the user's cwd, never this repo. Roster lives at `~/.claude/agent-roster/`.
- Do-It is not modified; engagement 1's deliverable IS the Workflow Specification document.
- `scripts/` and the two existing test files are not modified by any task; Task 9 ADDS `tests/test_docs.py`. `pytest tests/` must pass at the end.
- Do-It is a declared dependency for lifecycle doors 1-3. When the do-it skill is unavailable, Agent Studio authors the Workflow Specification itself following the same Engagement 1 brief and exclusions, and says so.
- Roster filenames are kebab-case slugs (`[a-z0-9-]+` only); never accept path separators or `..`; deletion is confirmed with the user and only ever targets files inside `~/.claude/agent-roster/`.
- Do not use the word "ship" (or variants) in any file content or commit message; use "deliver"/"release".

## Artifact layout (locked here, per spec Open Questions)

Full-lifecycle runs write to `agent-studio-out/<slug>/` (slug = kebab-case of the assignment, 3-4 words):

```
agent-studio-out/<slug>/
  brief.md                 # Assignment Brief (Stage 1)
  workflow-spec.md         # from Do-It engagement 1 (Stage 2)
  work-review.md           # work + staffing review (Stage 3)
  evidence-cards.md        # all Persona Evidence Cards (Stage 4)
  jds/<role>.md            # Job Descriptions (Stage 5)
  prototypes/<role>.md     # functional role prototypes (Stage 6)
  work-samples/<role>/     # sample-A.md, sample-B.md, verdict.md, key.md (Stage 7;
                           # key.md written only AFTER verdict.md exists)
  candidates/<role>.md     # slates + interview notes (Stage 8)
  personas/<name>.md       # approved Persona Profiles (Stage 8)
  staffed-spec.md          # staffed workflow specification (Stage 9)
  contribution-review.md   # post-run review (Stage 11); links the paths of
                           # Do-It engagement 2's run manifest / plan /
                           # verification record, which live in the target
                           # project per Do-It's own conventions
```

One-off panel runs keep the current layout: `agent-studio-out/panel.md`, `agent-studio-out/personas/`, `agent-studio-out/run-<timestamp>/`, `agent-studio-out/synthesis-prompt.md`.

---

### Task 1: `references/evidence-gate.md`

**Files:**
- Create: `references/evidence-gate.md`

**Interfaces:**
- Consumes: nothing (first task).
- Produces: the file `references/evidence-gate.md` with headings `# Persona Evidence Gate`, `## Task families`, `## Deterministic routing`, `## Roster waiver`, `## Persona Evidence Card template`. SKILL.md (Task 6) points Stage 4 here.

- [ ] **Step 1: Write the file**

```markdown
# Persona Evidence Gate

Every job in the Workflow Specification starts in-house. A job being
judgment-laden is NOT sufficient to open a role. This gate decides, per
candidate role, whether persona-shaped specialization is worth testing at all —
and how much proof it owes before hiring.

## Task families

Classify the job's candidate role into exactly ONE family:

| Task family | Intended persona benefit | Evidence status |
|---|---|---|
| Creative divergence | Useful semantic breadth and distinct options | Best-supported use in the corpus |
| Value-laden deliberation | Representation of legitimate conflicting priorities | Relatively favorable, conditional evidence |
| Grounded human or stakeholder simulation | Fidelity to differently situated human responses | Narrow, substrate-dependent support; never a substitute for real research |
| Multi-stakeholder subjective evaluation | Coverage of stakeholder-specific criteria | Promising in limited tested domains; human decision-maker retained |
| Sustained functional priority | Persistent attention to a consequential trade-off | Thin, single-domain causal evidence |
| General critique or analytical judgment | Valid blind spots or alternative interpretations | Indirect evidence or inference |
| Forecasting | Independent private signal or evidence framing | Persona-specific benefit unproven |
| Factual, checkable, or procedural work | Accuracy or reliable execution | No research-backed persona reason |

## Deterministic routing

Each family maps to exactly one user-facing conclusion, which sets the proof
the role owes. There is no discretion in this mapping.

| Family | Conclusion (verbatim to user) | Proof required before hiring |
|---|---|---|
| Creative divergence; value-laden deliberation | **Research supports trying this.** | None — may hire directly. A work sample is optional, recommended only when stakes are high. |
| Grounded simulation; multi-stakeholder subjective evaluation | **Supported only for a narrower analogous use.** | FIRST narrow the Job Description, mandate, activation trigger, and role status to the supported framing; THEN a blind work sample on that narrow framing. Success opens only the narrowed role. Human decision-maker retained for subjective evaluation. |
| Sustained functional priority; general critique or analytical judgment | **Promising, but experimental.** | A blind work sample (see `work-sample.md`). |
| Forecasting; factual/checkable/procedural work | **No research-backed reason to create a role.** | No role. Keep in-house: methods, tools, verification, independent attempts, or voting as appropriate. For forecasting, ensemble the EVIDENCE FRAMINGS in-house (recipes.md row) — do not infer a persona hire. |

## Roster waiver

A roster persona (see `roster.md`) may waive the work-sample requirement for a
task family when its track record shows:

1. Two or more real assignments in that SAME family, with contributions
   retained downstream, AND
2. At least one of those verified by a localized counterfactual contribution
   check (Stage 11).

The waiver replaces the work sample only. It never replaces the gate: a job
whose family maps to "No research-backed reason" gets no role regardless of who
is on the roster. Familiarity never bypasses the gate.

## Persona Evidence Card template

Write one card per candidate role into `evidence-cards.md`:

```
## Evidence Card: <role working title>
- Job (from workflow-spec.md): <job name>
- Task family: <one of the eight>
- Conclusion: <one of the four, verbatim>
- Intended persona effect: <the specific behavioral change the persona should cause>
- Intervention shape: <solo role | ensemble seat | simulation panel | none>
- Evaluation signal: <2-3 observable criteria tied to the intended effect> + <1 harm check>
- Contraindications / likely harm: <how this persona could make the work worse>
- Proof required: <direct hire | narrowed blind sample | blind sample | none — role refused>
- Waiver: <none | roster: <persona name> — <N> same-family entries, counterfactual-verified: <yes/no>>
```

A role proceeds to a Job Description only when it is coherent AND its
conclusion is not "No research-backed reason to create a role."
```

- [ ] **Step 2: Verify structure**

Run: `for h in 'Task families' 'Deterministic routing' 'Roster waiver' 'Persona Evidence Card template'; do grep -q "^## $h" references/evidence-gate.md || echo "MISSING: $h"; done`
Expected: no output

Run: `grep -c 'Research supports trying this' references/evidence-gate.md`
Expected: `>= 2`

- [ ] **Step 3: Commit**

```bash
git add references/evidence-gate.md
git commit -m "feat: add persona evidence gate reference (task families, routing, waiver, card template)"
```

---

### Task 2: `references/job-description.md`

**Files:**
- Create: `references/job-description.md`

**Interfaces:**
- Consumes: conclusion names from Task 1 (verbatim strings).
- Produces: `references/job-description.md` with headings `# Job Description`, `## Template`, `## Role statuses`, `## Narrowing rule`. Stage 5 in SKILL.md (Task 6) points here; `work-sample.md` (Task 3) consumes the JD fields.

- [ ] **Step 1: Write the file**

```markdown
# Job Description

The Job Description defines the ENDURING job. The Persona Profile (see
`persona-template.md`) defines a particular candidate designed to perform it.
The job may remain while a persona is revised or replaced.

Capabilities are human-world skills the job needs. Experience is learned
pattern recognition, expressed behaviorally (situations recognized, mistakes
anticipated, distinctions made, methods applied, grounded cases) — never a
biography claim. Values are what the role protects when legitimate goals
conflict, translated into observable trade-off behavior. Delivery feasibility
(model, tools, information, access, authority) is separate from capabilities —
a JD can be sound and still undeliverable.

## Template

Write to `agent-studio-out/<slug>/jds/<role>.md`:

```
# JD: <role title>
- Status: <one of the role statuses below>
- Job to be done: <one sentence>
- Why in-house improvements are not enough: <the residual need after playbook/method/tool fixes>
- Evidence case: <conclusion from the Evidence Card, verbatim> — intended effect: <...>
- Use when / do NOT use when: <activation and exclusion conditions>
- Mandate: <what the role optimizes for, under what pressure>
- Capabilities: <bounded list, with explicit exclusions>
- Experience profile: <situations / mistakes / distinctions / methods / grounded cases>
- Values: <trade-off rules and red lines, as behavior>
- Working methods: <the repeatable way the job is performed>
- Boundaries and authority: <what it may decide alone, what it may not>
- Inputs / outputs / handoffs / escalation: <exact artifacts and conditions>
- Delivery feasibility: <model, tools, information, access available? any blocker>
- Proof of value: <what the work sample or waiver must show> — Possible harm: <...>
- Review condition: <what triggers the Stage 11 keep/narrow/revise/retire decision>
```

## Role statuses

- No specialist role needed
- Specialist role worth evaluating
- Open specialist role         (work sample passed or waived; hiring underway)
- Provisional specialist role  (hired; not yet reviewed after a real run)
- Established specialist role  (kept after contribution review)
- Narrowed role
- Retired role

## Narrowing rule

When the Evidence Card's conclusion is "Supported only for a narrower analogous
use": rewrite Job-to-be-done, Mandate, Use-when, and Status to the narrow
framing BEFORE the work sample. A passing narrow sample opens ONLY the narrowed
role — never the original broader one.
```

- [ ] **Step 2: Verify structure**

Run: `for h in 'Template' 'Role statuses' 'Narrowing rule'; do grep -q "^## $h" references/job-description.md || echo "MISSING: $h"; done`
Expected: no output

Run: `grep -c 'Narrowed role' references/job-description.md`
Expected: `>= 1`

- [ ] **Step 3: Commit**

```bash
git add references/job-description.md
git commit -m "feat: add job description reference (template, role statuses, narrowing rule)"
```

---

### Task 3: `references/work-sample.md`

**Files:**
- Create: `references/work-sample.md`

**Interfaces:**
- Consumes: JD fields from Task 2 (`Mandate`, `Capabilities`, `Experience profile`, `Values`, `Working methods`, `Boundaries`, outputs contract); Evidence Card `Evaluation signal` from Task 1.
- Produces: `references/work-sample.md` with headings `# Functional Role Prototype and Work Sample`, `## Prototype template`, `## Blind protocol`, `## Outcomes`. Stages 6-7 in SKILL.md point here.

- [ ] **Step 1: Write the file**

```markdown
# Functional Role Prototype and Work Sample

Skip this file entirely for roles whose Evidence Card says "direct hire" or
carries a roster waiver — they go straight to hiring.

## Prototype template

The prototype is an EVALUATION INSTRUMENT, not an agent the user keeps. It is
the smallest anonymous functional version of the role: NO famous name, NO
character identity, NO decorative biography. Write to
`agent-studio-out/<slug>/prototypes/<role>.md`:

```
# Prototype: <role title>
## Mandate
<from the JD, verbatim>
## Capabilities
<from the JD, with exclusions>
## Recognitions
<experience profile as behavior: situations / mistakes anticipated / distinctions / methods>
## Values
<trade-off rules and red lines>
## Method
<numbered working procedure>
## Output contract
<the literal output format>
## Boundaries
<what it must not do; when it escalates>
```

## Blind protocol

Default: ONE bounded assignment — the smallest representative slice of the job
from workflow-spec.md.

1. The in-house assistant performs the slice with the best appropriate playbook.
2. A fresh subagent performs the same slice AS the prototype — same model, same
   information, same tools, same reasonable effort. Its prompt opens with the
   SUBAGENT PROMPT PREAMBLE from `hard-rules.md`.
3. The orchestrator saves both outputs under neutral labels in RANDOM order to
   `agent-studio-out/<slug>/work-samples/<role>/sample-A.md` and `sample-B.md`.
   The A/B assignment is held in the orchestrator's context only — NOT written
   anywhere the evaluator could read.
4. The user (or an evaluator subagent that has NOT seen either generation)
   judges A vs B on the Evidence Card's evaluation signal: 2-3 criteria tied to
   the intended persona effect, plus the one harm check. Write the judgment to
   `verdict.md`; only THEN write the mapping to `key.md` and unblind.

Scaling: low-stakes reversible roles = 1 sample. Frequently reused or
moderately consequential = 2-3 cases. High-stakes = hand to a dedicated
evaluation process — do not improvise one here. Never build a full parallel
non-persona workflow by default.

## Outcomes

Record in `work-samples/<role>/verdict.md` — exactly one of:

- **Open the role** — proceed to hiring (Stage 8).
- **Keep in-house** — no meaningful lift. Record what the playbook keeps.
- **Persona harm** — the prototype made the work worse. ALWAYS reported
  separately from no-lift; name the harm.
- **Narrower only** — useful for a narrower assignment; apply the narrowing
  rule (`job-description.md`) and re-sample if the narrow framing was not what
  was tested.
- **Unclear** — run ONE additional case or revise the prototype once; then
  decide. No infinite retries.

A work sample proves the ROLE beats in-house on its slice. It does not prove
the end-to-end workflow improved (that is Stage 11), and it does not select the
named persona (that is Stage 8).
```

- [ ] **Step 2: Verify structure**

Run: `for h in 'Prototype template' 'Blind protocol' 'Outcomes'; do grep -q "^## $h" references/work-sample.md || echo "MISSING: $h"; done`
Expected: no output

Run: `grep -ci 'blind\|random order\|unblind' references/work-sample.md`
Expected: `>= 3`

- [ ] **Step 3: Commit**

```bash
git add references/work-sample.md
git commit -m "feat: add work-sample reference (anonymous prototype, blind protocol, outcomes)"
```

---

### Task 4: `references/roster.md` + persona-template split

**Files:**
- Create: `references/roster.md`
- Modify: `references/persona-template.md` (append one section; existing template and lint unchanged)

**Interfaces:**
- Consumes: waiver predicate wording from Task 1; five-element template heading names from `persona-template.md` (Role, Expertise, Process, Output, Constraints, Positions, Identity).
- Produces: `references/roster.md` with headings `# Roster`, `## File format`, `## Consent and privacy`, `## Rehire and waiver reading`; a new `## Character core vs job binding` section at the end of `persona-template.md`. Stage 8 and Stage 11 in SKILL.md point here.

- [ ] **Step 1: Write `references/roster.md`**

```markdown
# Roster

`~/.claude/agent-roster/` — one file per retained persona, shared across ALL
projects and skills. The roster stores the reusable CHARACTER CORE plus a
track record. It never stores a job binding (mandate, output contract,
boundaries, triggers) — those are written fresh per hire against the JD.

## File format

`~/.claude/agent-roster/<name>.md`, where `<name>` is a kebab-case slug of the
persona's name matching `[a-z0-9-]+` — never a raw string, never containing
path separators or `..`. If the slug collides with an existing DIFFERENT
persona, disambiguate with a suffix (`-2`) and tell the user. Deletions are
confirmed with the user first and only ever target files inside
`~/.claude/agent-roster/`.

```
# <Name>
> Interpretation of <figure>'s public work, not the real person.   <- when applicable

## Character core
Role stance: <what this character optimizes for, as identity — not a job mandate>
Values: <trade-off rules and red lines this character defends anywhere>
Experience: <situations recognized / mistakes anticipated / distinctions / methods / grounded cases>
Voice and cues: <how they speak; 2-3 memorable cues>
Internal contradiction: <one genuine tension>
Re-anchoring: <the one-line reminder that snaps them back in character on drift>

## Track record
### <YYYY-MM-DD> — <job, one line> (<task family>)
- Contributions retained downstream: <what survived into the final work>
- Mistakes caught / made: <both, plainly>
- Counterfactual check: <verified — rerun without them changed the result | not run>
- Helped when / did not help when: <conditions>
```

## Consent and privacy

- CONSENT PRECEDES ANY WRITE. New hire: ask keep-or-let-go FIRST; create the
  file only on "keep". Existing roster persona: show the drafted track-record
  entry and append only after the user confirms; the user may edit or redact it.
- "Let it go" for a rostered persona = delete the file (say so before doing it).
- Entries are summary-level. Generalize or omit confidential or
  project-identifying detail — the roster crosses projects.
- Retiring a ROLE does not remove a roster PERSONA; the core may outlive any
  single role.

## Rehire and waiver reading

At any hiring stage, check the roster BEFORE generating new candidates. A
persona fits when its character core matches the JD's values and experience
profile — never force a fit by editing the core (that is a candidate-fit
question, settled by hiring someone else or adjusting openly with the user).

Present a fitting rehire FIRST, alongside fresh candidates, with its track
record summarized. The roster suggests; the evidence gate decides.

Waiver check (feeds `evidence-gate.md`): count track-record entries in the
JD's task family with non-empty "Contributions retained downstream". Waiver
requires >= 2 such entries AND >= 1 with "Counterfactual check: verified".
```

- [ ] **Step 2: Update `references/persona-template.md`**

Three edits to the existing file, then append the split section:

a. In the `## Template` fenced block, extend the `## Identity` section to:

```markdown
## Identity
Name: <a name>
Backstory: <2-3 sentences, first person, what shaped this stance>
Voice and cues: <how they speak; 2-3 memorable cues>
Internal contradiction: <one genuine tension this persona holds>
Re-anchoring: <the one-line reminder that snaps this persona back in character on drift>
```

b. Replace the save-path line near the top
(`Save generated personas to \`agent-studio-out/personas/<name>.md\`.`) with:

```markdown
Save generated personas to `agent-studio-out/personas/<name>.md` (one-off
panel runs) or `agent-studio-out/<slug>/personas/<name>.md` (full-lifecycle
runs).
```

c. In the `## Worked example` block, add matching `Voice and cues:` and
`Re-anchoring:` lines to Vera Cole's Identity section, e.g.
`Voice and cues: clipped declaratives; "show me the path in"; zero praise until the end.`
and `Re-anchoring: you assume breach until proven otherwise — re-read your Constraints.`

Then append at end of file:

```markdown
---

## Character core vs job binding

Every Persona Profile divides into two parts; each element belongs to exactly
one side:

- **Character core** (reusable, roster-storable): Identity (name, backstory,
  internal contradiction), voice and memorable cues, Values/Positions,
  Experience expressed as recognitions, re-anchoring instructions, track
  record.
- **Job binding** (written fresh per hire from the JD): Role mandate as scoped
  to THIS job, Expertise boundaries for this job, Process, Output contract,
  Constraints, boundaries/authority, activation trigger, escalation.

In the five-element template above: `## Identity`, `## Positions`, and the
experience content inside `## Expertise` belong to the core; `## Role`,
`## Process`, `## Output`, `## Constraints` are binding. When retaining a
persona to the roster, copy the core per `roster.md`; when rehiring, rebuild
the binding sections from the new JD. Never silently edit a core to fit a job.
```

- [ ] **Step 3: Verify**

Run: `for h in 'File format' 'Consent and privacy' 'Rehire and waiver reading'; do grep -q "^## $h" references/roster.md || echo "MISSING: $h"; done`
Expected: no output

Run: `grep -c 'Character core vs job binding' references/persona-template.md`
Expected: `1`

Run: `grep -c 'Counterfactual check' references/roster.md`
Expected: `>= 2`

- [ ] **Step 4: Commit**

```bash
git add references/roster.md references/persona-template.md
git commit -m "feat: add roster reference and character-core/job-binding split"
```

---

### Task 5: `references/doit-handoff.md`

**Files:**
- Create: `references/doit-handoff.md`

**Interfaces:**
- Consumes: artifact layout from this plan's header; ensemble rules from `hard-rules.md` and `recipes.md` (existing files, referenced by name only).
- Produces: `references/doit-handoff.md` with headings `# Do-It Handoff`, `## Engagement 1 brief (specification only)`, `## Workflow Specification template`, `## Staffed Workflow Specification template`, `## Engagement 2 brief (build and run)`. Stages 2, 9, 10 in SKILL.md point here.

- [ ] **Step 1: Write the file**

```markdown
# Do-It Handoff

Do-It is invoked twice, unmodified, via its normal single-shot pipeline. The
engagement brief IS the instruction passed to Do-It; the deliverable named in
it is where Do-It's run naturally ends. Never ask Do-It to stop mid-run.
Narrate each handoff to the user ("I am asking Do-It to specify the jobs and
decisions involved. It will stop before implementation or staffing.").

## Engagement 1 brief (specification only)

Pass verbatim, filling <>:

```
Assignment: produce a Workflow Specification document at
agent-studio-out/<slug>/workflow-spec.md, from the Assignment Brief at
agent-studio-out/<slug>/brief.md (attached below).

The document describes WHAT work must happen to fulfill the brief. For each
major job record: purpose; input and output; decisions and judgments involved;
important trade-offs; dependencies; failure modes; observable success and
verification requirements. You may describe sequence.

Excluded from this deliverable: detailed prompts, agent orchestration, model
selection, tool implementation, retry logic, file structure, implementation
sequence — and any recommendation of agents, personas, job titles, or teams.
Staffing is a separate later decision that is not yours.

This is a light-to-medium engagement: a specification document, not a build.
Prefer the lightest rigor your own evaluation permits.

The deliverable is the document itself. The engagement ends when it exists and
passes your own review.

<paste brief.md>
```

If the do-it skill is unavailable, Agent Studio authors `workflow-spec.md`
itself, following this brief's contract and exclusions exactly, and tells the
user Do-It was skipped and why.

For an existing workflow, add: "Distinguish the as-is workflow from recommended
structural improvements; both live in the same document, clearly separated."

## Workflow Specification template

Expected shape of `workflow-spec.md` (engagement 1 output):

```
# Workflow Specification: <assignment>
## Job: <name>            <- repeat per major job
- Purpose:
- Input -> Output:
- Decisions and judgments:
- Trade-offs:
- Dependencies:
- Failure modes:
- Observable success / verification:
## Sequence (optional)
```

## Staffed Workflow Specification template

Agent Studio (not Do-It) writes `staffed-spec.md` at Stage 9:

```
# Staffed Workflow Specification: <assignment>
## In-house jobs
- <job>: playbook = <the strengthened playbook, inline or by path>
## Role: <title>           <- repeat per approved provisional role
- JD: jds/<role>.md   Persona: personas/<name>.md
- Status: Provisional specialist role
- Activation trigger: <exact condition>
- Inputs -> Outputs:
- Boundaries / authority / handoff / escalation:
- Proof: <work-sample result | waiver, with one-line summary> — remaining uncertainty: <...>
## Ensemble constraints (binding)      <- ONLY when >=2 roles answer the same
                                          question or evaluate the same artifact
                                          in parallel
- Isolated generation: one subagent per role, fresh context, no cross-talk
  before combining; every prompt opens with the SUBAGENT PROMPT PREAMBLE
  (hard-rules.md).
- Heterogeneity: roles differ in POSITIONS, verified, not just tone.
- Combine: <mode from recipes.md row> — never naive-mean-blend
  (synthesis-modes.md).
- Debate: capped at one round with a stopping rule.
- Recipe-specific: <critic seat | human selection | different model families | none>.
## Handoff contracts                   <- for sequential/complementary roles
- <role A> -> <role B>: <artifact passed, acceptance condition>
```

## Engagement 2 brief (build and run)

Pass verbatim, filling <>:

```
Assignment: implement the staffed workflow specified at
agent-studio-out/<slug>/staffed-spec.md (attached below, with the persona
files it names).

Your scope: detailed implementation plan; technical orchestration and context
flow; implementation; integration of the approved Persona Profiles exactly as
written; tests; verification; running the workflow when execution is part of
the assignment; risk-appropriate review; packaging the reusable artifact.
Install, deploy, or publish only when the user authorizes it.

Hard limits: do NOT add, remove, merge, or substitute roles or personas. The
"Ensemble constraints (binding)" section, when present, is non-negotiable —
implement orchestration within it. If implementation reveals a new staffing
question or invalidates a role boundary, STOP work on that role and return the
narrow question to Agent Studio; continue the rest.

When you finish, report the paths of your run manifest, implementation plan,
and verification record — they are linked from contribution-review.md.

<paste staffed-spec.md and persona files>
```
```

- [ ] **Step 2: Verify**

Run: `for h in 'Engagement 1 brief' 'Workflow Specification template' 'Staffed Workflow Specification template' 'Engagement 2 brief'; do grep -q "^## $h" references/doit-handoff.md || echo "MISSING: $h"; done`
Expected: no output

Run: `grep -c 'Ensemble constraints (binding)' references/doit-handoff.md`
Expected: `2`

- [ ] **Step 3: Commit**

```bash
git add references/doit-handoff.md
git commit -m "feat: add do-it handoff reference (engagement briefs, spec templates, ensemble constraints)"
```

---

### Task 6: Rewrite `SKILL.md`

**Files:**
- Modify: `SKILL.md` (full rewrite; frontmatter `name: agent-studio` kept)

**Interfaces:**
- Consumes: every reference file from Tasks 1-5 by exact filename; existing `hard-rules.md`, `recipes.md`, `synthesis-modes.md`, `diagnose-rubric.md`, `harden-checklist.md`, `persona-template.md`; scripts section content from the current SKILL.md (unchanged).
- Produces: the complete new SKILL.md below. Task 7 verifies its cross-references.

- [ ] **Step 1: Replace the entire SKILL.md body with:**

````markdown
---
name: agent-studio
description: Evidence-gated workflow design and staffing for AI work. Determines how a job should be done, what stays in-house, and whether any part benefits from a persona specialist; if justified, runs a hiring process (job description, named candidate slate, interview, roster rehires) and hands a staffed workflow to Do-It. Also runs one-off persona panels for perspectives on a question, and re-engineers existing skills/workflows/panels. Use when the user wants a reliable way to accomplish an outcome, asks whether a specialist or agent would help, wants a persona designed, a panel/council built or run, N perspectives on X, or an existing skill/workflow/panel analyzed or improved. Triggers on "/agent-studio", "design how this work gets done", "construct/design a persona or agent", "build a panel/council of agents", "run an ensemble", "get N perspectives on X", "would a specialist help", "diagnose this skill/workflow", "where would agents help in X", "audit/harden this panel/ensemble".
---

# agent-studio

Workflow-design and staffing, expressed through workplace concepts: assignments,
jobs, candidates, interviews, work samples, performance reviews. The central
rule:

> Understand the assignment, specify the work, keep it in-house by default, and
> create a specialist role only when the task matches a plausible persona
> benefit and the role's value is demonstrated — by a blind work sample, or by
> evidence strong enough to waive it (a best-supported task family or a proven
> roster track record); then let the user hire and shape the named persona who
> will fill it.

A successful run may create no persona at all. This skill is not a team
generator. Read the referenced file at each stage; do not improvise around the
hard rules.

Artifacts go to `agent-studio-out/` in the user's cwd (full-lifecycle runs
under `agent-studio-out/<slug>/`, layout in `references/doit-handoff.md` and
the stage list below), never this repo. The roster lives at
`~/.claude/agent-roster/` (`references/roster.md`).

## Hard rules (always)

Read and obey `references/hard-rules.md`. The essentials:

- **In-house is the default.** No generic agent merely to do in-house work; no
  persona inferred from task complexity or the presence of judgment; job
  titles, famous names, and biographies are never proof of capability.
- **Familiarity never bypasses the evidence gate.** Roster rehires are
  suggested, not pre-approved.
- **Roster writes need consent first**, and entries exclude confidential or
  project-identifying detail (`references/roster.md`).
- Ensembles: **strict isolation** for generating lenses (one subagent each,
  fresh context, SUBAGENT PROMPT PREAMBLE from `references/hard-rules.md`);
  **never naive-mean-blend** (`references/synthesis-modes.md`); debate capped
  at one round; co-report a quality note AND a coverage/diversity note.
- **NO WebFetch anywhere** — `curl` raw pages only; carry this into every
  subagent prompt you emit.
- **Guardrails switch by mode:** strict rulebook for judgment work,
  flavor-forward for creative work (`references/hard-rules.md`).
- Persona harm is always named separately from "no meaningful lift".
- The user owns candidate selection, adjustments, and final taste/value calls.

## Four front doors

Route by what the user asked for; when unclear, ask.

| Request sounds like | Door |
|---|---|
| "I want a reliable way to accomplish X" | **1. Design the work** — full lifecycle from Stage 1 |
| "Review/improve this skill or workflow" · legacy "diagnose"/"harden" | **2. Existing workflow** — see Existing-workflow path |
| "Would a specialist who does X help?" · legacy "construct" | **3. Consider a specialist** — never judge from a role label alone: run Stage 1 in compressed form (recover and confirm the brief), then the shared lifecycle from Stage 2 on, with the proposed role evaluated at Stages 3-4 |
| "Get N perspectives on X" · "run an ensemble/panel" — today's answer, not a reusable workflow | **4. One-off panel** — compressed path below; no Do-It, no staffed artifact |

## Full lifecycle (doors 1-3)

### Stage 1 — Understand the assignment
Adaptive dialogue, not a questionnaire (AskUserQuestion for genuine gaps only).
Establish: what the user wants to accomplish; what that makes possible; what
success looks like; constraints and non-negotiables; known obstacles and
failure modes; what was already tried; open assumptions. The user's first
stated goal is working material, not ground truth — clarify purpose, test
against obstacles, avoid premature fixing. Write `brief.md`; confirm it. A
user with a precise committed brief is not forced to explore.

### Stage 2 — Commission the Workflow Specification
Send Do-It the Engagement 1 brief from `references/doit-handoff.md` (verbatim
template). Deliverable: `workflow-spec.md` — what work must happen, no
implementation detail, no staffing. Narrate the handoff to the user. If Do-It
is unavailable, author `workflow-spec.md` yourself under the same brief and
exclusions, and say so.

### Stage 3 — Review the work, then the staffing
Write `work-review.md`. First the WORK: every job necessary? any missing? are
unrelated responsibilities combined? sequence and handoffs sensible? is a
missing CHECK being mistaken for a missing CRITIC? would clearer instructions
or a stronger method solve it? Then the STAFFING, every job presumed in-house.
Classify each residual need: clearer assignment | workflow/method |
information/tool/access/delivery feasibility | evidence-matched persona
opportunity. Conclusions per job: keep in-house · keep in-house + strengthen
playbook · resolve workflow/info/delivery issue · explore a specialist role ·
do not attempt with this delivery arrangement.

### Stage 4 — Persona Evidence Gate
For each "explore a specialist role" job: write an Evidence Card per
`references/evidence-gate.md` into `evidence-cards.md`. The family→conclusion
mapping is deterministic; the conclusion fixes the proof owed (direct hire /
narrowed blind sample / blind sample / no role). Check roster waivers per
`references/roster.md`.

### Stage 5 — Job Description
Per surviving role: write `jds/<role>.md` per `references/job-description.md`.
Apply the narrowing rule when the conclusion demands it.

### Stage 6 + Stage 7 — Prototype and blind work sample
Skip both stages for direct-hire or waived roles. Otherwise build the anonymous
prototype and run the blind protocol per `references/work-sample.md`; record
the outcome in `work-samples/<role>/verdict.md`. Only "Open the role" proceeds.

### Stage 8 — Interview and hire (personification is mandatory)
Never an unnamed specialist. Per open role:
1. Roster first (`references/roster.md`): fitting retained personas are
   presented as rehires, track record summarized, alongside fresh candidates.
2. Slate of 2-3 CONTRASTING named candidates — recognizable real people,
   historical figures, or famous fictional characters preferred; an original
   named persona when no recognizable one fits without distortion.
   `python3 <skill-dir>/scripts/exemplar_find.py find --archetype "<a>"`
   surfaces leads. Each candidate: who they are · what they are like · why
   their capabilities/experience/values/methods fit the JD · distinctive
   contribution · one risk of hiring them. Every real-person/character hire is
   an INTERPRETATION, labeled as such; for judgment work, ground in documented
   public positions (corpus pull:
   `python3 <skill-dir>/scripts/exemplar_find.py corpus --name "<n>" --url <u> --out <dir>`;
   required when the archetype has no common precedent).
3. Interview loop (one AskUserQuestion per seat): hire · ask a candidate
   job-relevant questions · reject candidate or slate · request new candidates ·
   adjust in natural language ("Warren Buffett, but more interested in emerging
   technology") · combine qualities. Rebuild and re-present until hired or the
   role is left unfilled. Record the slate, adjustments, and outcome in
   `candidates/<role>.md`.
4. Construct the Persona Profile in the hire's voice per
   `references/persona-template.md` (character core + job binding split; run
   the grep lint; fix failures). Save to `personas/<name>.md`. Demographics off
   by default. Biography never manufactures capability.
Multiple roles: separate interviews per seat, then one compact team card
(name · job · defining qualities · contribution); the user may reopen any hire.
One role never implies a team — each extra role needs its own card, JD, and
case.

### Stage 9 — Staffed Workflow Specification
Write `staffed-spec.md` per the template in `references/doit-handoff.md`:
in-house jobs + playbooks; each provisional role with JD, persona, exact
activation trigger, I/O, boundaries, proof and remaining uncertainty; the
BINDING "Ensemble constraints" section when ≥2 roles answer the same question
in parallel; handoff contracts for sequential roles.

### Stage 10 — Return to Do-It
Send the Engagement 2 brief from `references/doit-handoff.md` (verbatim
template). Do-It plans, builds, integrates personas unchanged, tests, runs when
asked, packages. It may not touch staffing; narrow staffing questions come back
here.

### Stage 11 — Contribution and performance review
Only after the staffed workflow has run. Write `contribution-review.md` from
observable evidence: what each persona produced; what downstream work retained,
rejected, changed; unique contribution; misses; delay/noise/bias/harm. When
cheap and informative, run the localized counterfactual check: rerun the
relevant downstream integration ONCE without the specialist's output (never a
second full workflow). Without a counterfactual, report traceable contribution
but never claim causal lift. Decide per role: keep provisional · establish ·
narrow · revise/replace persona · convert behavior into an in-house playbook ·
retire. Then roster maintenance with consent-first writes per
`references/roster.md`.

## One-off panel door (door 4)

1. **Frame** — short dialogue: restate the goal and the kind of help; propose
   the minds and the recipe row (`references/recipes.md`) with one-line
   sketches per member; one AskUserQuestion to approve/adjust. Skip the ask
   when the request fully specifies both, or the run is non-interactive.
2. **Eligibility** — only families whose conclusion is "Research supports
   trying this" (creative divergence, value-laden deliberation) — or roster
   personas holding a same-family waiver — may hire through this door. Anything
   that owes a work sample is answered in-house with that explanation, or
   offered the full lifecycle.
3. **Hire** — compressed Stage 8: roster first, slate, interview, persona files
   linted. Cast card before dispatch (one line per member: name · role · what
   they hunt · one signature "never"; one AskUserQuestion: keep team / meet
   them / renegotiate a hire / open a new seat; skip when non-interactive or
   already confirmed).
4. **Assemble** — `panel.md` + `synthesis-prompt.md` from the recipe row
   (members axis, size, topology, combine mode; critic unless the recipe says
   otherwise; different model families offered for high-stakes normative
   panels). Verify members differ in POSITIONS. A one-off request ("get N
   perspectives on X") already asks for today's answer: RUN by default. Stop
   here only when the user asked for the panel artifacts, not answers ("build
   me a panel").
5. **Run** — one isolated subagent per lens (PREAMBLE first), then the critic
   (critic sees all outputs; CRITIC PREAMBLE). Outputs to
   `agent-studio-out/run-<timestamp>/<lens>.md`.
6. **Synthesize** — de-dup by embedding, combine per the recipe's mode (default
   dissent-carrying), `references/synthesis-modes.md`. Never naive-mean-blend.
7. **Evaluate + review** — `python3 <skill-dir>/scripts/diversity.py` over lens
   outputs, then the output stage (set diversity, or synthesis-vs-outlier
   distance for dissent-carrying; grep for the labeled Minority section —
   absence = FAIL). Write `run-<timestamp>/diversity.md`; report quality note
   AND coverage/diversity note. End with a performance review per hire
   (contributions kept, dissent defended, misses; zero kept findings reported
   plainly — seat vs character) and roster maintenance per
   `references/roster.md` (consent first).

## Existing-workflow path (door 2)

1. Recover and confirm the Assignment Brief (`brief.md`).
2. Specify the as-is workflow: for a SKILL.md target read it plus scripts and
   references; classify stages with `references/diagnose-rubric.md`; existing
   personas/panels are INCUMBENTS — reconstruct their JDs from actual use;
   audit incumbent panels with `references/harden-checklist.md`.
3. Review process problems before staffing problems (Stage 3 checklist).
4. Commission the spec (Engagement 1, as-is vs recommended-improvements form).
5. Use existing outputs as the baseline where adequate; do not rerun work
   unnecessarily.
6. Gate proposed additions AND incumbents (Stage 4); prototype + blind sample
   where owed (Stages 6-7).
7. Named candidates for every open role; interview, adjust, hire (Stage 8).
8. Staffed spec → Engagement 2 → contribution review vs the baseline,
   proportionate to cost and stakes (Stages 9-11).

When the user asked only for analysis (legacy diagnose/harden), stop after
step 3 with the report — steps 2-3 emit
`agent-studio-out/diagnosis-<slug>.md` / `hardening-<slug>.md` per the rubric
and checklist templates — and offer the full path as the build pointer.

## Scripts

Locating the scripts: they live in THIS skill's directory, not the user's cwd.
Resolve `<skill-dir>` = the base directory containing this SKILL.md (reported
when the skill loads) and invoke `python3 <skill-dir>/scripts/...`.

- `exemplar_find.py find|corpus` — archetype -> exemplar LEADS (titles + URLs the
  model layer resolves into named people), and corpus pull (pages via curl).
  Needs `EXA_API_KEY` for `find` (exits 20 without it).
- `diversity.py FILE...` — mean pairwise semantic distance (OpenAI embeddings if
  `OPENAI_API_KEY`, else a lexical fallback). Never fails for a missing API key;
  exit 2 only on unusable inputs.
````

- [ ] **Step 2: Verify cross-references and structure**

Run: `for f in evidence-gate job-description work-sample roster doit-handoff hard-rules recipes synthesis-modes diagnose-rubric harden-checklist persona-template; do grep -q "references/$f.md" SKILL.md || echo "MISSING: $f"; done`
Expected: no output

Run: `grep -c 'Stage 1\|Stage 11' SKILL.md`
Expected: `>= 2`

Run: `grep -ciE '\bship(ped|ping|s)?\b' SKILL.md`
Expected: `0` (word-bounded so "relationship" cannot false-positive)

- [ ] **Step 3: Commit**

```bash
git add SKILL.md
git commit -m "feat: rewrite SKILL.md as evidence-gated staffing lifecycle (four doors, 11 stages)"
```

---

### Task 7: Update legacy rubrics for the evidence gate

**Files:**
- Modify: `references/diagnose-rubric.md`
- Modify: `references/harden-checklist.md`

**Interfaces:**
- Consumes: task families and conclusions from Task 1 (`references/evidence-gate.md`); door names from Task 6.
- Produces: rubric and checklist consistent with deterministic evidence routing; both build pointers updated.

- [ ] **Step 1: Wire the evidence gate into `references/diagnose-rubric.md`**

In the `## Map to a recipe` section, replace the three-condition gate paragraph
and the two bullets that follow it with:

```markdown
A judgment-laden stage is mapped through the Persona Evidence Gate
(`evidence-gate.md`), not by judgment-ladenness alone:

1. Classify the stage into ONE task family from evidence-gate.md; its
   deterministic conclusion decides the recommendation.
2. "Research supports trying this" families (creative divergence, value-laden
   deliberation): recommend the matching `recipes.md` row IF genuinely
   heterogeneous members are constructible and the combine step can preserve
   disagreement; else "single strong pass".
3. "Supported only for a narrower analogous use" / "Promising, but
   experimental" families: recommend "in-house now; a role is possible via a
   narrowed/blind work sample" — name the proof owed. Never recommend the
   panel as if proven.
4. "No research-backed reason" families (forecasting, factual/checkable/
   procedural): mark **"single pass — do NOT ensemble"** with the reason: on
   ground-truth tasks, debate is often a no-op or loses to simple
   voting/self-consistency at higher cost. For forecasting, ensembling
   EVIDENCE FRAMINGS in-house (recipes.md row) is fine; a persona hire is not
   inferred.
Cost sanity still applies: a panel costs N+1 subagent runs — is this stage's
decision worth that?
```

In the `## Report template`, add a `Task family` and `Evidence conclusion`
column to the table header row (after `Task type`), and replace the build
pointer line `Next: build with /agent-studio construct|ensemble` with
`Next: /agent-studio — door 2 (existing workflow) runs the full staffing lifecycle from this diagnosis.`

- [ ] **Step 2: Recipe-condition the critic check in `references/harden-checklist.md`**

Replace check 2 with:

```markdown
2. **Critic / devil's-advocate present when the recipe row calls for one?**
   Score against the panel's `recipes.md` row (or infer the row from task
   type): rows listing a critic (analytical judgment, creative direction,
   artifact review) FAIL at HIGH without one; rows without a mandatory critic
   (creative ideation, normative, forecasting) score N-A. No inferable recipe:
   UNKNOWN.
   [source: recipes.md table; hard-rules.md #Anti-conformity is first-class]
   Severity: HIGH when the row requires it. Fix: add a critic lens (steelman,
   then challenge).
```

Replace the build pointer in its report template with
`Next: /agent-studio — door 2 treats this panel as incumbents and runs the staffing lifecycle.`

- [ ] **Step 3: Verify**

Run: `grep -c 'evidence-gate.md' references/diagnose-rubric.md`
Expected: `>= 1`

Run: `grep -rn 'construct|ensemble' references/diagnose-rubric.md references/harden-checklist.md`
Expected: no output

- [ ] **Step 4: Commit**

```bash
git add references/diagnose-rubric.md references/harden-checklist.md
git commit -m "feat: route diagnose recommendations through the evidence gate; recipe-condition harden critic check"
```

---

### Task 8: README rewrite

**Files:**
- Modify: `README.md` (full rewrite of user-facing description; keep installation, requirements, and license sections as-is)

**Interfaces:**
- Consumes: door names and stage names exactly as written in Task 6; artifact layout from this plan's header.

- [ ] **Step 1: Rewrite README.md**

Read `README.md`. Keep installation, requirements (`EXA_API_KEY`,
`OPENAI_API_KEY`), and license content. Replace EVERYTHING else that describes
behavior — overview paragraphs, any mode list
(construct/ensemble/diagnose/harden), workflow diagram, usage examples,
typical-run sequence, artifact layout, and any "construct makes the people,
ensemble makes the meeting" style explanation — so no retired architecture
remains. Open with:

```markdown
Agent Studio is an evidence-gated workflow-design and staffing skill. It
determines how a job should be done, what stays in-house, and whether any part
would benefit from a persona specialist. When a specialist is justified — by
research-matched task family, a blind work sample, or a proven roster track
record — it runs a hiring process: job description, named candidate slate,
interview, and a retained Persona Profile. Staffed workflows are implemented
and executed by a separate Do-It engagement.

Four front doors: design how work gets done · improve an existing workflow
(subsumes the old diagnose/harden modes) · consider a specialist (the old
construct) · run a one-off panel (the old ensemble). Retained personas live on
a global roster (`~/.claude/agent-roster/`) with per-assignment track records.
```

Then include: the four-door table copied verbatim from the new SKILL.md, and
the full-lifecycle artifact layout from this plan's header. Keep installation,
scripts, requirements, and license sections unchanged.

- [ ] **Step 2: Repo-wide consistency checks**

Run: `grep -rn 'six stages' SKILL.md README.md references/`
Expected: no output (the six-stage framing is gone from live docs)

Run: `grep -rln 'Mode: Diagnose\|Mode: Harden' SKILL.md`
Expected: no output (modes folded into door 2)

Run: `grep -c 'agent-roster' SKILL.md references/roster.md`
Expected: both files match at least once

Run: `grep -rniE '\bship(ped|ping|s)?\b' SKILL.md README.md references/ --include='*.md'`
Expected: no output

- [ ] **Step 3: Run the untouched test suite**

Run: `python3 -m pytest tests/ -v`
Expected: all tests PASS (scripts were not modified)

- [ ] **Step 4: Routing dry-run (skill smoke test)**

Dispatch one fresh subagent with ONLY the new SKILL.md content and this prompt:
"For each request, answer with the door number and first artifact you would
produce: (a) 'give me 5 perspectives on our pricing page' (b) 'I want a
reliable way to produce our weekly market report' (c) 'would a devil's-advocate
reviewer help my deploy checklist?' (d) 'audit this panel for groupthink'."
Expected: (a) door 4 → framing then panel.md; (b) door 1 → brief.md; (c) door
3 → recovered assignment then work-review.md/evidence card; (d) door 2 →
hardening report. Any wrong routing = fix SKILL.md's door table wording, not
the subagent.

- [ ] **Step 5: Commit**

```bash
git add README.md
git commit -m "docs: update README for the evidence-gated redesign; verify consistency and tests"
```

---

### Task 9: Durable documentation tests

**Files:**
- Create: `tests/test_docs.py`
- Test: `tests/test_docs.py` (self-testing)

**Interfaces:**
- Consumes: final file set from Tasks 1-8 (exact filenames and heading strings as written above).
- Produces: a pytest module that locks the redesign's structure against regressions.

- [ ] **Step 1: Write the failing test file**

```python
"""Structural regression tests for the evidence-gated redesign docs."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = (ROOT / "SKILL.md").read_text()
REFS = ROOT / "references"

NEW_REFS = [
    "evidence-gate.md", "job-description.md", "work-sample.md",
    "roster.md", "doit-handoff.md",
]
ALL_REFS = NEW_REFS + [
    "hard-rules.md", "recipes.md", "synthesis-modes.md",
    "diagnose-rubric.md", "harden-checklist.md", "persona-template.md",
]


def test_all_reference_files_exist():
    for name in ALL_REFS:
        assert (REFS / name).is_file(), f"references/{name} missing"


def test_skill_points_at_every_reference():
    for name in ALL_REFS:
        assert f"references/{name}" in SKILL, f"SKILL.md never references {name}"


def test_four_doors_present():
    for door in ["Design the work", "Existing workflow",
                 "Consider a specialist", "One-off panel"]:
        assert door in SKILL, f"door missing from SKILL.md: {door}"


def test_eleven_stages_present():
    for n in range(1, 12):
        assert re.search(rf"Stage {n}\b", SKILL), f"Stage {n} missing"


def test_evidence_conclusions_verbatim():
    gate = (REFS / "evidence-gate.md").read_text()
    for c in ["Research supports trying this",
              "Supported only for a narrower analogous use",
              "Promising, but experimental",
              "No research-backed reason to create a role"]:
        assert c in gate, f"conclusion missing: {c}"


def test_roster_consent_and_waiver():
    roster = (REFS / "roster.md").read_text()
    assert "CONSENT PRECEDES ANY WRITE" in roster
    assert "Counterfactual check" in roster
    assert "agent-roster" in SKILL


def test_blind_protocol_present():
    ws = (REFS / "work-sample.md").read_text()
    assert "sample-A.md" in ws and "sample-B.md" in ws
    assert "verdict.md" in ws


def test_no_retired_architecture():
    assert "six stages" not in SKILL
    assert "Mode: Diagnose" not in SKILL and "Mode: Harden" not in SKILL


def test_no_banned_word():
    for path in [ROOT / "SKILL.md", ROOT / "README.md", *REFS.glob("*.md")]:
        text = path.read_text()
        assert not re.search(r"\bship(ped|ping|s)?\b", text, re.I), \
            f"banned word in {path.name}"
```

- [ ] **Step 2: Run the suite**

Run: `python3 -m pytest tests/ -v`
Expected: all tests PASS, including the two existing helper-script modules. Any
FAIL here is a real regression in Tasks 1-8 — fix the doc, not the test,
unless the test string genuinely mismatches what an earlier task wrote (then
align the test with the task's exact wording).

- [ ] **Step 3: Commit**

```bash
git add tests/test_docs.py
git commit -m "test: lock evidence-gated redesign structure (doors, stages, conclusions, consent, blind protocol)"
```
