# Agent Studio — user-facing voice (seed)

Every string below is something a USER reads or hears when the skill runs. The
job is to make them warm, simple, and clear — a friendly, understanding helper —
without changing what they MEAN or weakening the model-facing rules around them.
Each item tags where it lives and how the user meets it.

---

## A. The four evidence verdicts  (evidence-gate.md — a HEADLINE the user reads about a role)

1. Research supports trying this.
2. Supported only for a narrower analogous use.
3. Promising, but experimental.
4. No research-backed reason to create a role.

## B. Role statuses  (job-description.md — a LABEL on a role)

- No specialist role needed
- Specialist role worth evaluating
- Open specialist role
- Provisional specialist role
- Established specialist role
- Narrowed role
- Retired role

## C. Work-sample outcomes  (work-sample.md — a VERDICT headline after a test)

- Open the role
- Keep in-house
- Persona harm: the functional role made the work worse
- Narrower only: useful for a narrower assignment
- Unclear: run one more case or revise the prototype

## D. The four front doors  (SKILL.md — what the user picks / is routed to)

- Design the work — "I want a reliable way to accomplish X"
- Existing workflow — "Review/improve this skill or workflow"
- Consider a specialist — "Would a specialist who does X help?"
- One-off panel — "Get N perspectives on X" — today's answer, not a reusable workflow

## E. Stage-transition narration  (what the skill SAYS as it moves between stages)

E1 (handing work to Do-It to specify):
"I am asking Do-It to specify the jobs and decisions involved. It will stop
before implementation or staffing."

E2 (most work stays in-house, one role looks worth testing):
"Most jobs can remain in-house. One job matches a plausible persona use, so I
have written a Job Description. I will test a minimal functional version of the
role before asking you to hire anyone."

E3 (the test showed value, the role is open):
"The role's work sample showed useful lift, so the position is open. Here are
three people who embody the job differently. You can interview, modify, reject,
or hire any of them."

E4 (a hire is made and adjusted):
"You hired a Warren Buffett interpretation adjusted to be more interested in
emerging technology and somewhat more tolerant of risk. I have translated that
character into the complete Persona Profile and am returning the staffed
specification to Do-It for implementation and execution."

E5 (final review after the workflow ran):
"The workflow ran successfully. Here is what the provisional role contributed,
what was retained, and whether I recommend keeping, narrowing, revising, or
retiring it."

## F. Roster consent prompts  (roster.md — a QUESTION the user is asked)

F1 (new hire, end of run): keep-or-let-go — ask whether to keep the persona on
the roster or let them go.

F2 (existing roster persona): show the drafted track-record entry and append
only after the user confirms; they may edit or redact it.

F3 (letting a rostered persona go): say the file will be deleted before doing it.

## G. Candidate presentation  (SKILL.md Stage 8 — how each candidate is introduced)

For each candidate, the user is told, briefly:
- Who they are
- What they are like
- Why their capabilities, experience, values, and methods fit the job
- What distinctive contribution they would make
- What risk, excess, or blind spot comes with hiring them

## H. The interview options  (SKILL.md Stage 8 — the choices offered per seat)

- Hire a candidate
- Ask a candidate job-relevant questions
- Reject one candidate or the whole slate
- Request new candidates
- Adjust a candidate in natural language
- Combine qualities from candidates
