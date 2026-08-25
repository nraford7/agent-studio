# Agent Studio Evidence-Gated Redesign

Date: 2026-08-25  
Status: ready for user review

## Summary

Agent Studio helps a user determine how a job should be done, what can remain
in-house, and whether any part of the work would benefit from a persona-driven
specialist. If a specialist is justified, Agent Studio defines the job, helps the
user choose and shape a candidate persona, and gives the staffed workflow back to
Do-It for implementation and execution.

The skill is not primarily a team generator. A successful run may create no
persona at all. It is a workflow-design and staffing process expressed through
familiar workplace concepts: assignments, jobs, job descriptions, candidates,
in-house work, specialist roles, interviews, work samples, and performance reviews.

The central rule is:

> Understand the assignment, specify the work, keep it in-house by default, and
> create a specialist role only when the task matches a plausible persona benefit
> and a functional prototype demonstrates useful lift; then let the user hire and
> shape the named persona who will fill it.

## Problem

The current Agent Studio moves too quickly from goal framing to proposing minds,
personas, and panels. Its mechanical-versus-judgment distinction is too broad:
many tasks involve judgment without having evidence that persona conditioning
will improve them. The current design also makes panels and famous-character
personas feel like the default product, even though the research says personas
reliably change outputs but do not reliably improve accuracy.

The redesign must preserve the delightful hiring experience while making the
staffing decision evidence-gated, economical, and subordinate to the intended
outcome.

## Evidence base

The design is grounded in:

- `docs/research/Persona-Construction-Research-Bible.md`
- `docs/research/Persona-Ensembles-Research-Bible.md`
- `docs/research/Perspective-Synthesis-Research-Bible.md`
- `docs/research/Persona-Construction-Playbook.md`
- `docs/research/Persona-External-Sources-Digest.md`
- `/Users/noahraford/Desktop/goal_squad/goal-elicitation-bible.md`

The evidence implies the following constraints:

1. Personas reliably change substantive outputs, but expert labels do not
   reliably improve correctness and can make performance worse.
2. Persona use is best supported for creative divergence, value-laden
   deliberation, and certain forms of grounded human simulation.
3. Multi-stakeholder subjective evaluation has narrower, domain-specific positive
   evidence and should retain a human decision-maker.
4. Sustained functional priorities have suggestive but thin causal evidence from
   a single domain and require a work sample when generalized.
5. General critique, analytical judgment, forecasting, and artifact review are not
   broadly validated persona applications. They are experiments unless they
   decompose into a better-supported task family.
6. Factual, checkable, retrieval, procedural, and execution work should remain
   in-house; use methods, tools, verification, independent attempts, or voting as
   appropriate.
7. Persona ensembles are conditional. Genuine heterogeneity, isolated generation,
   and disagreement-preserving combination are necessary; ordinary multi-agent
   debate can cost more and perform worse.
8. The user's first stated goal is working material, not ground truth. Guided
   discovery should use the user's words, clarify purpose and success, test against
   obstacles, and avoid premature fixing.

## Terminology

### In-house

Work performed by the user and the ordinary assistant using appropriate briefs,
playbooks, tools, information, and verification. Keeping work in-house does not
mean using a weak or bare generic prompt, and it does not require creating a
generic agent.

### Capability

A human-world skill required by a job, such as graphic design, writing design
briefs, evaluating marketing research, facilitating a workshop, or developing a
financial model.

### Experience

Learned pattern recognition from analogous work, expressed behaviorally as:

1. Situations the specialist recognizes.
2. Mistakes it anticipates.
3. Distinctions it knows to make.
4. Methods it knows when to apply.
5. Cases or documented practice grounding those behaviors.

An agent never receives experience merely because its biography claims years in
a profession. Experience may be grounded in documented practice and later
strengthened by the persona's actual track record.

### Values

What a role protects or prioritizes when legitimate goals conflict. Values must
be translated into observable trade-off behavior, not left as decorative nouns.

### Working methods

The repeatable way the job is performed.

### Delivery feasibility

Whether the available model, tools, information, access, authority, and
environment can support the work. This is separate from the capabilities named in
a job description.

### Job Description and Persona Profile

The Job Description defines the enduring job. The Persona Profile defines a
particular candidate designed to perform it. The job may remain while a persona is
revised or replaced.

## Product boundary

Agent Studio owns:

- Goal elicitation sufficient to establish the assignment.
- Commissioning a job-level workflow specification.
- Reviewing the work before reviewing staffing.
- Determining what remains in-house.
- Applying the evidence-based persona opportunity gate.
- Writing Job Descriptions for justified specialist opportunities.
- Candidate search, interviews, adjustments, and work samples.
- Constructing approved Persona Profiles.
- Adding provisional roles to the workflow specification.
- Reviewing actual specialist contributions after execution.
- Presenting the final reusable skill or workflow to the user.

The first Do-It engagement owns:

- A job-level workflow specification describing what work must happen.
- No implementation plan, implementation, execution, or staffing decisions.

The second Do-It engagement owns:

- The detailed implementation plan.
- Technical design and orchestration.
- Implementation, tests, review, execution, verification, and packaging.
- Shipping or installation only when authorized.

Agent Studio does not become a universal workflow planner. Do-It does not invent
personas or teams.

## Three front doors

### Design how the work gets done

For requests such as, "I want a reliable way to accomplish X."

Begin with goal elicitation and an Assignment Brief.

### Improve an existing workflow

For requests such as, "Review this skill or workflow and make it better."

Recover and confirm the intended assignment, specify the current workflow, review
the work itself, establish a baseline, and then consider staffing changes. An
existing persona or panel is treated as an incumbent workforce and evaluated
against its stated job.

### Consider a specialist

For requests such as, "Would a specialist who does X help?"

Recover enough of the assignment and workflow to evaluate the proposed role
responsibly. Do not construct the persona from a role label alone.

All three entry paths converge on the same shared lifecycle.

## Shared lifecycle

### Stage 1: Understand the assignment

Agent Studio uses an adaptive dialogue rather than a compulsory questionnaire.
It establishes:

- What the user wants to accomplish.
- What that outcome should make possible.
- What success looks like.
- Important constraints and non-negotiables.
- Known obstacles and failure modes.
- What has already been tried and learned.
- Important assumptions and unresolved choices.

The result is an **Assignment Brief** confirmed by the user. If the user already
has a precise, committed brief, Agent Studio accepts it rather than forcing
unnecessary exploration.

### Stage 2: Commission the workflow specification

Agent Studio gives Do-It the Assignment Brief and explicitly authorizes a
specification-only engagement.

Do-It returns a **Workflow Specification** describing what work must happen. For
each major job it records:

- Purpose.
- Input and output.
- Decisions and judgments involved.
- Important trade-offs.
- Dependencies.
- Failure modes.
- Observable success and verification requirements.

The specification may describe sequence, but it does not include detailed
prompts, agent orchestration, model selection, tool implementation, retry logic,
file structure, or an implementation sequence. It does not recommend agents,
personas, job titles, or a team.

For an existing workflow, the specification distinguishes the as-is workflow
from recommended structural improvements.

### Stage 3: Review the work and staffing

Agent Studio first reviews whether the work itself is well designed:

- Is every job necessary?
- Is a job missing?
- Are unrelated responsibilities combined?
- Are sequence and handoffs sensible?
- Is a missing check being mistaken for a missing critic?
- Could clearer instructions or a stronger method solve the problem?

Only then does it conduct the Staffing Review. Every job starts with the
presumption that it remains in-house.

The Staffing Review distinguishes:

- A clearer-assignment need.
- A workflow or method need.
- An information, tool, access, or delivery-feasibility need.
- An evidence-matched persona opportunity.

The conclusion may be:

- Keep the job in-house.
- Keep it in-house and strengthen its playbook.
- Resolve a workflow, information, or delivery issue.
- Explore a specialist role.
- Do not attempt the job with the available delivery arrangement.

### Stage 4: Apply the Persona Evidence Gate

A job being judgment-laden is not sufficient. Each possible role receives a
**Persona Evidence Card** with:

- Task family.
- Intended persona effect.
- Evidence status.
- Appropriate intervention shape.
- Evaluation signal.
- Contraindications and likely harm.

#### Evidence-matched task families

| Task family | Intended benefit | Status |
|---|---|---|
| Creative divergence | Useful semantic breadth and distinct options | Best-supported use in the corpus |
| Value-laden deliberation | Representation of legitimate conflicting priorities | Relatively favorable, conditional evidence |
| Grounded human or stakeholder simulation | Fidelity to differently situated human responses | Narrow, substrate-dependent support; never a substitute for real research |
| Multi-stakeholder subjective evaluation | Coverage of stakeholder-specific criteria | Promising in limited tested domains; human decision-maker retained |
| Sustained functional priority | Persistent attention to a consequential trade-off | Thin, single-domain causal evidence; work sample required |
| General critique or analytical judgment | Valid blind spots or alternative interpretations | Indirect evidence or inference; experiment required |
| Forecasting | Independent private signal or evidence framing | Persona-specific benefit unproven; do not infer a hire |
| Factual, checkable, or procedural work | Accuracy or reliable execution | No research-backed persona reason; keep in-house |

The user-facing evidence conclusions are:

- **Research supports trying this.**
- **Supported only for a narrower analogous use.**
- **Promising, but experimental.**
- **No research-backed reason to create a role.**

Only a job that is both coherent and evidence-matched proceeds to a Job
Description.

### Stage 5: Write the Job Description

The Job Description contains:

- Role title and status.
- Job to be done.
- Reason the role may be needed after in-house improvements.
- Evidence case and intended persona effect.
- When to use and when not to use the role.
- Mandate.
- Capabilities.
- Experience profile.
- Values.
- Working methods.
- Boundaries and authority.
- Inputs, outputs, handoffs, and escalation.
- Proof of value and possible harm.
- Review condition.

Formal role statuses are:

- No specialist role needed.
- Specialist role worth evaluating.
- Open specialist role.
- Provisional specialist role.
- Established specialist role.
- Narrowed role.
- Retired role.

### Stage 6: Prepare a functional role prototype

Agent Studio translates the Job Description into the smallest anonymous
functional prototype that can test the proposed role. It includes the mandate,
required capabilities, experience-based recognitions, values, working method,
boundaries, and output contract. It contains no famous name, character identity,
or decorative biography.

This prototype is an evaluation instrument, not an agent the user will retain. It
exists only to determine whether persona-shaped specialization shows enough value
to justify opening and personifying the role.

### Stage 7: Minimum viable work sample

The work sample evaluates whether the functional role prototype can perform its
proposed job better than the in-house approach. It does not yet prove that the job
improves the end-to-end outcome, and it does not select the final named persona.

The default work sample uses the smallest representative slice from the Workflow
Specification:

1. The in-house assistant performs the job with the best appropriate playbook.
2. The functional role prototype performs the same job with the same model,
   information, tools, and reasonable effort.
3. The user or evaluator compares two or three criteria tied to the intended
   persona effect, plus one important harm check.

Low-stakes reversible roles use one bounded work sample. Frequently reused or
moderately consequential roles may use two or three cases. High-stakes roles are
handed to a dedicated evaluation process. Agent Studio does not create a full
parallel non-persona workflow by default.

Work-sample outcomes are:

- Open the specialist role and proceed to hiring.
- Keep the job in-house.
- Persona harm: the functional role made the work worse.
- Useful only for narrower assignments.
- Unclear: run one additional case or revise the prototype.

No meaningful lift and worse performance remain separate outcomes.

### Stage 8: Interview, hire, and construct the Persona Profile

Every role that passes Stage 7 proceeds through this stage. Personification is
mandatory for every specialist agent. Agent Studio converts the successful
functional prototype into persona requirements, then presents two or three named,
contrasting candidates who embody them.

Prefer interpretations of recognizable real people, historical figures, or
famous fictional characters whose documented traits make the role immediately
understandable and memorable. Existing retained personas may also be considered.
If no recognizable candidate fits without distortion, offer an original named
persona that embodies the Job Description precisely. Never fall back to an
unnamed specialist agent.

For each candidate, explain briefly:

- Who the person or character is.
- What they are like.
- Why their capabilities, experience, values, and methods fit the job.
- What distinctive contribution they would make.
- What risk, excess, or blind spot comes with hiring them.

This is the **interview** phase. The user can:

- Hire a candidate.
- Ask a candidate job-relevant interview questions.
- Reject one candidate or the entire slate.
- Request new candidates with similar role fit.
- Adjust a candidate in natural language.
- Combine qualities from candidates.

For example: "Warren Buffett, but more interested in emerging technology and
therefore willing to take slightly more risk." Agent Studio rebuilds the candidate
around that direction, presents the revised interpretation, and seeks approval
again. The loop continues until the user hires a candidate or decides not to fill
the role.

After approval, Agent Studio constructs the retained Persona Profile in the
candidate's recognizable character while preserving the behavioral substance of
the Job Description:

- Functional stance: optimization target, operating pressure, and trap to avoid.
- Capabilities expressed as observable behavior with exclusions.
- Experience expressed through situations, mistakes, distinctions, methods, and
  grounded cases.
- Values expressed as trade-off rules and red lines.
- Working procedure.
- Output contract.
- Boundaries and escalation.
- Name, identity, voice, and memorable character cues.
- Re-anchoring instructions for long interactions.

Demographic labels are off by default. Biography cannot manufacture capability
or experience. Real-person, historical, and fictional personas are explicitly
labeled as interpretations. For judgment work, the interpretation is grounded in
documented public positions or source material where feasible. The name and
character make the role legible and memorable; they are not evidence that the
role performs better.

When more than one role is justified, repeat the interview separately for each
open position. After all positions are filled, present a compact team card with
each name, job, defining qualities, and contribution. The user may reopen any
hire before approving the working arrangement.

### Stage 9: Produce the staffed workflow specification

Agent Studio adds approved provisional roles to the Workflow Specification. The
result records:

- What remains in-house.
- In-house playbooks.
- Each provisional specialist role and its Job Description.
- The Persona Profile filling it.
- Exact activation trigger.
- Inputs and outputs.
- Boundaries, authority, handoff, and escalation.
- Work-sample result and remaining uncertainty.

One role never implies a team. Additional roles require separate evidence cards,
job descriptions, and hiring cases.

### Stage 10: Return to Do-It for execution

Agent Studio authorizes the second Do-It engagement. Do-It now:

- Creates the detailed implementation plan.
- Designs technical orchestration and context flow.
- Implements the workflow or skill.
- Integrates the approved Persona Profiles.
- Tests and verifies the complete workflow.
- Runs it when execution is part of the assignment.
- Obtains risk-appropriate review.
- Packages the reusable artifact.
- Installs, deploys, or publishes only when authorized.

Do-It may not add personas or teams independently. If implementation reveals a
new staffing question or invalidates an approved role boundary, it returns that
narrow question to Agent Studio, which resolves it and sends the updated staffed
specification back.

### Stage 11: Contribution and performance review

Actual staffing performance is evaluated only after the staffed workflow has
run. Agent Studio uses observable evidence:

- What the persona produced.
- What downstream work retained, rejected, or changed.
- What the persona uniquely contributed.
- What it missed.
- Whether it introduced delay, noise, bias, or harm.

When cheap and informative, Agent Studio performs a localized contribution check
by rerunning the relevant downstream integration once without the specialist's
output. This is not a second full workflow. Without a counterfactual comparison,
Agent Studio may report traceable contribution but must not claim causal lift.

The resulting decision is:

- Keep the role provisional.
- Establish the role.
- Narrow the role.
- Revise or replace the persona.
- Convert useful behavior into an in-house playbook.
- Retire the role.

Reusable personas accumulate a concise track record of assignments,
contributions retained, mistakes caught, mistakes made, useful conditions, and
conditions where the role did not help.

## Existing-workflow path

For an existing skill or workflow:

1. Recover and confirm the Assignment Brief.
2. Specify the as-is jobs, stages, handoffs, existing personas, and expected
   outputs.
3. Review process problems before staffing problems.
4. Treat existing personas as incumbents with Job Descriptions reconstructed from
   their actual use.
5. Establish existing outputs as the baseline where adequate evidence already
   exists; do not rerun work unnecessarily.
6. Apply the Persona Evidence Gate to proposed additions and existing roles.
7. Use a functional role prototype and minimum viable work sample to decide
   whether a new or replacement role should be opened.
8. Present named candidates for every open role and let the user interview,
   adjust, reject, replace, or hire them.
9. Give the approved staffed specification to Do-It for re-engineering,
   execution, and verification.
10. Compare the completed result with the existing baseline at a level
   proportionate to cost and stakes.

An existing panel is simply an existing workflow with multiple incumbent roles.
Isolation, conformity, synthesis, and diversity-retention checks remain available
inside this path; they are not a separate conceptual product.

## User experience

Agent Studio remains the conversational host. It narrates transitions without
making the user manually transfer context:

> "I understand the assignment. I am asking Do-It to specify the jobs and
> decisions involved. It will stop before implementation or staffing."

Then:

> "Most jobs can remain in-house. One job matches a plausible persona use, so I
> have written a Job Description. I will test a minimal functional version of the
> role before asking you to hire anyone."

Then:

> "The role's work sample showed useful lift, so the position is open. Here are
> three people who embody the job differently. You can interview, modify, reject,
> or hire any of them."

Then:

> "You hired a Warren Buffett interpretation adjusted to be more interested in
> emerging technology and somewhat more tolerant of risk. I have translated that
> character into the complete Persona Profile and am returning the staffed
> specification to Do-It for implementation and execution."

Finally:

> "The workflow ran successfully. Here is what the provisional role contributed,
> what was retained, and whether I recommend keeping, narrowing, revising, or
> retiring it."

The hiring language provides warmth and affinity, but never substitutes for
evidence or creates unnecessary agents.

## Default output artifacts

The redesigned skill should maintain the following conceptual artifacts. The
implementation plan will determine their exact paths and file formats.

- Assignment Brief
- Workflow Specification
- Work Review
- Staffing Review
- Persona Evidence Cards
- Job Descriptions
- Functional role prototypes
- Work-sample notes
- Candidate slates and user adjustments
- Persona Profiles
- Staffed Workflow Specification
- Do-It implementation and verification record
- Contribution and Performance Review
- Final reusable skill or workflow
- Reusable persona track records, when retained

## Guardrails

- In-house is the default.
- Do not create a generic agent merely to perform in-house work.
- Do not infer persona usefulness from task complexity or the presence of
  judgment alone.
- Do not use job titles, expertise claims, famous names, or biographies as proof
  of capability.
- Do not equate experience with information or data.
- Do not substitute simulated stakeholders for actual research or participation.
- Do not create a panel when one role or no role is sufficient.
- Do not run open debate by default.
- Do not claim causal workflow improvement from a functional role work sample.
- Do not build a full parallel workflow unless cost, stakes, and user choice
  justify it.
- Name persona harm explicitly and separately from no meaningful lift.
- Preserve user control over candidate selection, adjustment, and final taste or
  value decisions.

## Alternatives considered

### Narrow persona assessor

Agent Studio would answer only whether a persona is needed and construct one if
so. Rejected because a responsible staffing decision requires understanding the
assignment and the major jobs in the workflow. The narrow version would judge
roles against an imaginary or prematurely accepted process.

### Universal workflow designer

Agent Studio would elicit goals, fully specify and plan the workflow, construct
agents, implement everything, and evaluate it alone. Rejected because this
dilutes its distinctive staffing competence and duplicates a more rigorous
dedicated workflow process.

### Full experimental evaluation by default

Every persona would receive multi-arm, multi-case testing and a parallel
non-persona workflow. Rejected because it is too expensive and slow for ordinary
use. The redesign uses minimum viable work samples, probation, real-work track
records, and optional escalation for consequential roles.

### Recommended: two Do-It engagements with Agent Studio staffing between them

The first Do-It engagement specifies the work and stops. Agent Studio evaluates
staffing, runs the human-centered hiring process, and adds provisional roles. The
second Do-It engagement plans, builds, executes, verifies, and packages the
staffed workflow. Agent Studio then reviews actual contribution.

## Success criteria

1. A user can begin with an outcome, an existing workflow, or a proposed
   specialist role.
2. The skill can conclude that all work should remain in-house and proceed
   without creating an agent or team.
3. The first Do-It engagement returns a workflow specification and does not
   prematurely implement or recommend agents.
4. Every proposed persona role maps to a confidence-labeled evidence task family
   and states the intended effect and contraindications.
5. General judgment, forecasting, review, and expertise labels do not
   automatically qualify for persona treatment.
6. Job Descriptions distinguish capabilities, experience, values, methods,
   mandate, and delivery feasibility.
7. Default work samples use one bounded assignment and compare the best in-house
   playbook with an anonymous functional prototype of the proposed role.
8. Every role that passes its work sample receives two or three named candidates,
   preferably recognizable real people, historical figures, or famous fictional
   characters who embody the Job Description.
9. The user can interview, hire, adjust, reject, or replace candidates until one
   is approved; a precisely matched original named persona is always available
   when no recognizable candidate fits.
10. No-lift and persona-harm outcomes remain distinct.
11. The second Do-It engagement creates the implementation plan, builds, runs,
    verifies, and packages the staffed workflow.
12. Actual staffing performance is assessed only after execution; causal claims
    require an appropriate counterfactual.
13. Existing skills and workflows can be re-engineered through the same lifecycle
    without treating agents as the default solution.

## Non-goals

- Proving that personas broadly improve factual accuracy.
- Treating every judgment task as a persona opportunity.
- Creating teams for their own sake.
- Replacing dedicated planning, implementation, or evaluation systems.
- Simulating professional credentials or lived experience.
- Replacing human stakeholders, customers, experts, or decision-makers.
- Requiring expensive evaluation for every reversible role.

## Open questions

None blocking. Exact artifact paths, command triggers, compatibility behavior,
and migration from the current Construct/Ensemble/Diagnose/Harden modes belong in
the implementation plan.
