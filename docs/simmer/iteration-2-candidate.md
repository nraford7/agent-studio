# Agent Studio — user-facing voice (seed)

Every string below is something a USER reads or hears when the skill runs. The
job is to make them warm, simple, and clear — a friendly, understanding helper —
without changing what they MEAN or weakening the model-facing rules around them.
Each item tags where it lives and how the user meets it.

---

## A. The four evidence verdicts  (evidence-gate.md — a HEADLINE the user reads about a role)

1. Green light — research backs this, so you can go ahead and try it now.
2. Not for this exact job — but it could help a smaller, similar one, once we've checked a bit more.
3. Worth a shot, but unproven — let's run a quick test before you rely on it.
4. No — you don't need a specialist here. Your regular assistant has this.

## B. Role statuses  (job-description.md — a LABEL on a role)

- No special hire needed — the regular assistant handles it
- Might be worth a specialist — let's look closer
- Specialist spot is open — ready for someone to fill
- On trial — hired, but not proven yet on a real run
- Proven — did well on a real run, so we're keeping them
- Trimmed down — now doing a smaller job than before
- Let go — no longer on the team

## C. Work-sample outcomes  (work-sample.md — a VERDICT headline after a test)

- Open the spot — the test went well, so this role is worth filling
- Skip the hire — the regular assistant already does this fine
- Made it worse — I know that's not what we hoped, but bringing in the specialist actually hurt the work, so we won't use them here
- Only for a smaller job — helpful, but just for a narrower task, not this whole one
- Not clear yet — let's give it exactly one more attempt, either a fresh run or a quick rework, and then we'll decide either way

## D. The four front doors  (SKILL.md — what the user picks / is routed to)

- Design the work — "I want a reliable way to accomplish X"
- Existing workflow — "Review/improve this skill or workflow"
- Consider a specialist — "Would a specialist who does X help?"
- One-off panel — "Get N perspectives on X" — today's answer, not a reusable workflow

## E. Stage-transition narration  (what the skill SAYS as it moves between stages)

E1 (handing work to Do-It to specify):
"I'm handing this over to Do-It — that's the builder that turns a plan into a
working thing. Right now it's just mapping out the jobs and decisions involved.
Nothing gets built or staffed yet — the plan comes back to you first."

E2 (most work stays in-house, one role looks worth testing):
"Good news — most of this your regular assistant can handle on its own. Just one
part looks like it might call for a specialist, so I've written up what that job
would involve. Before I ask you to hire anyone, I'll quietly run a small test
version of the role to see if it actually helps."

E3 (the test showed value, the role is open):
"The trial run helped — it made the work better — so this spot is worth filling.
Here are three people who'd take on the job in their own way. Have a look: you can
ask them questions, tweak them, turn any of them down, or hire the one you like."

E4 (a hire is made and adjusted):
"Nice pick. You went with a take on Warren Buffett, tuned to be keener on new
technology and a bit more open to risk. I'm writing that character up in full now,
then handing the plan back to the builder so it can be built and run for real.
Nothing's locked in — you can still adjust any of this if you change your mind."

E5 (final review after the workflow ran):
"All done — the workflow ran fine. Here's what this trial role added and what we
kept from it. Now it's your call on what happens to the role: keep it as is,
narrow it to a tighter job, swap in or rework the character doing it, or let it
go entirely."

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
