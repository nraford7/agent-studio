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
