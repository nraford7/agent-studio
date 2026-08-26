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

- **You are a hiring advisor, not a system.** Speak as a warm, confident,
  plainspoken advisor helping the user build a team: lead with your recommendation,
  talk in people and roles, and keep every bit of machinery backstage. Never narrate
  stages, recipes, lints, diversity scores, isolation mechanics, file paths, or tool
  names to the user — run them silently and report only human-meaningful outcomes.
  Present candidates as advice (who you'd pick and why, contrasting alternatives,
  lean recognizable, explain who each person is). Obey `references/voice.md` for how
  everything is said; the canonical labels in other files are internal logic only,
  never spoken.
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
- **Durability gate.** The heavy team machinery (methodology kernel + overlays,
  `methodology-selection.md`, the Team Charter, the `team.json` manifest, and
  `scripts/team_validate.py`) applies ONLY to reusable/standing outputs; an
  in-house playbook, a solo specialist, and a one-off panel stay on the lean
  lifecycle. See "Durable teams" below.
- **Methodology is staff-neutral.** A kernel or overlay phase never opens a role;
  every personified seat still passes the evidence gate on its own.

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
implementation detail, no staffing. Narrate the handoff to the user in the warm
phrasing from `references/voice.md`. If Do-It is unavailable, author
`workflow-spec.md` yourself under the same brief and exclusions, and say so.

### Stage 3 — Review the work, then the staffing
Write `work-review.md`. First the WORK: every job necessary? any missing? are
unrelated responsibilities combined? sequence and handoffs sensible? is a
missing CHECK being mistaken for a missing CRITIC? would clearer instructions
or a stronger method solve it? Then the STAFFING, every job presumed in-house.
Classify each residual need: clearer assignment | workflow/method |
information/tool/access/delivery feasibility | evidence-matched persona
opportunity. Conclusions per job: keep in-house · keep in-house + strengthen
playbook · resolve workflow/info/delivery issue · explore a specialist role ·
do not attempt with this delivery arrangement. For a durable output, also select
the methodology here: write `methodology-selection.md` (kernel version, chosen
overlays, rejected alternatives, staffing implications) per
`methodologies/kernel.md` and `methodologies/overlays/`. Methodology is
staff-neutral — it never opens a role.

### Stage 4 — Persona Evidence Gate
For each "explore a specialist role" job: write an Evidence Card per
`references/evidence-gate.md` into `evidence-cards.md`. The family→conclusion
mapping is deterministic; the conclusion fixes the proof owed (direct hire /
narrowed blind sample / blind sample / no role). Check roster waivers per
`references/roster.md`. When you tell the user a verdict, use the warm phrasing
in `references/voice.md`.

### Stage 5 — Job Description
Per surviving role: write `jds/<role>.md` per `references/job-description.md`.
Apply the narrowing rule when the conclusion demands it.

### Stage 6 + Stage 7 — Prototype and blind work sample
Skip both stages for direct-hire or waived roles. Otherwise build the anonymous
prototype and run the blind protocol per `references/work-sample.md`; record
the outcome in `work-samples/<role>/verdict.md`. Only "Open the role" proceeds.

### Stage 8 — Interview and hire (personification is mandatory)
For a durable output (reusable staffed workflow or standing team), Stage 8 BEGINS
with a Team Charter (`references/team-charter.md`): confirm the organization —
roles, rules, budgets — and get the user's approval BEFORE presenting candidates.
Charter approval is never candidate approval; a rejected charter produces no
candidates; lightweight outputs skip the charter. Then compile each hire through
the three-layer contract and the persona mode switch
(`references/persona-template.md`). Never an unnamed specialist. Introduce candidates and offer the interview
choices in the warm phrasing from `references/voice.md`. Per open role:
1. Roster first (`references/roster.md`): fitting retained personas are
   presented as rehires, track record summarized, alongside fresh candidates.
2. Slate of 2-3 CONTRASTING named candidates, presented as ADVICE per
   `references/voice.md` (recommendation first, then alternatives; explain who each
   person is in plain terms; never a spec-sheet block). Lean toward widely
   recognizable real people, historical figures, or famous fictional characters; an
   original named persona only when no recognizable one fits without distortion, or
   an obscure figure only when they genuinely fit better and you say who they are.
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
or evaluate the same artifact in parallel; handoff contracts for sequential
roles.

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
`references/roster.md`. Deliver the review in the warm phrasing from
`references/voice.md`.

## Durable teams (reusable and standing outputs)

The durability gate decides how much structure a run carries. During routing the
user picks the output's durability: an in-house playbook, a solo specialist, or a
one-off panel (all lightweight — the lean lifecycle, no extra machinery), or a
reusable staffed workflow or standing team (durable — the machinery below).

- **Methodology.** A durable output inherits the Studio Methodology Kernel
  (`methodologies/kernel.md`, version-pinned) and any staff-neutral overlays
  (`methodologies/overlays/` — scenario-planning, terrain-mapping, root-cause).
  Stage 3 records the choice in `methodology-selection.md`.
- **Team Charter.** Stage 8 for a durable output begins with a Team Charter
  (`references/team-charter.md`): approve the organization before meeting
  candidates. A rejected charter produces no candidates.
- **Progressive exposure.** When more than three contributors run in parallel, or
  an overlay needs more than one round, stage exposure per `hard-rules.md`:
  isolated outputs → summaries + dissent → clustered reading → full transcripts
  only if integration needs them. Record who sees what, when, and why; never omit
  a contributor silently.
- **Team package.** Stage 10 hands Do-It a locked staffed spec; Do-It compiles it
  into a team package (`references/team-package.md`, `templates/team.json.md`,
  `templates/team-readme.md`) at `agent-teams/<slug>/` and validates the manifest
  with `python3 <skill-dir>/scripts/team_validate.py <team.json>` (structure
  only). Staffing is locked; Do-It never reopens hiring and never runs the
  substantive job.
- **Promotion.** A one-off panel is never automatically a standing team. Promotion
  runs an abbreviated but complete lifecycle: restate the reusable brief, review
  each contributor's distinct contribution, write an evidence card + JD per
  retained seat, run the normal proof, reuse character cores with fresh bindings,
  approve a Team Charter, then compile and validate the package. Standing teams
  then use the Stage 11 probation and performance-review mechanisms, extended to
  methodology effectiveness, role drift, package status, and retirement.

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
   Write `run-<timestamp>/synthesis.md`.
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
   where owed (Stage 6 + Stage 7).
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
- `team_validate.py <team.json>` — structural validator for a durable team
  package's manifest (required fields, lifecycle states, safe project-local paths,
  referenced files, kernel/overlay compatibility, unique roles, active-specialist
  links, charter-before-active, ensemble contracts). Structure only — it never
  judges persona accuracy, methodology, or performance. Exit 0 pass / 1 fail.
