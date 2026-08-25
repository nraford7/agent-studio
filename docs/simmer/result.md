# Agent Studio — user-facing voice (final)

Every string below is something a USER reads or hears when the skill runs. The
job is to make them warm, simple, and clear — a friendly, understanding helper —
without changing what they MEAN or weakening the model-facing rules around them.
Each item tags where it lives and how the user meets it.

Winner of the simmer loop: iteration 3 (Warmth 8 · Clarity 8 · Precision 9 ·
composite 8.33). Two micro-polish fixes applied here: E5's doubled "It's your
call" reduced to one; Section D's "N" left as-is (it is a routing trigger
example of user INPUT, not skill output).

---

## A. The four evidence verdicts  (evidence-gate.md — a HEADLINE the user reads about a role)

1. Green light — research backs this, so you can try it now.
2. Not this exact job — but a smaller, similar one could work, once we've checked a little more.
3. Worth a try, but unproven — let's run a quick test before you lean on it.
4. No specialist needed here — your regular assistant has this one.

## B. Role statuses  (job-description.md — a LABEL on a role)

- No special hire needed — the regular assistant handles it
- Might be worth a specialist — let's look closer
- Specialist spot is open — ready to fill
- On trial — hired, but not proven yet on a real run
- Proven — did well on a real run, so it stays
- Trimmed down — a smaller job than before
- Let go — off the team now

## C. Work-sample outcomes  (work-sample.md — a VERDICT headline after a test)

- Open the spot — the test went well, so this role is worth filling
- Skip the hire — the regular assistant already does this fine
- Made it worse — I know that's not what we hoped, but the specialist hurt the work, so we'll leave them out
- Only for a smaller job — helpful for a narrower task, but not this whole one
- Not clear yet — one more try (a fresh run or a quick rework, not both), then we decide

## D. The four front doors  (SKILL.md — what the user picks / is routed to)

- Design the work — "I want a reliable way to accomplish X"
- Existing workflow — "Review/improve this skill or workflow"
- Consider a specialist — "Would a specialist who does X help?"
- One-off panel — "Get N perspectives on X" — today's answer, not a reusable workflow

## E. Stage-transition narration  (what the skill SAYS as it moves between stages)

E1 (handing work to Do-It to specify):
"I'm passing this to Do-It, the builder that turns a plan into a working thing.
For now it's only mapping out the jobs and the decisions they involve. Nothing
gets built or staffed yet — the plan comes back to you first."

E2 (most work stays in-house, one role looks worth testing):
"Good news: most of this your regular assistant can handle on its own. One part
might call for a specialist, though, so I've written up what that job would
involve. Before you hire anyone, I'll run a small test version of the role to see
whether it helps."

E3 (the test showed value, the role is open):
"The trial run made the work better, so the spot is worth filling. Here are three
people who'd take on the job in their own way. Have a look: ask them questions,
adjust them, turn any of them down, or hire the one you like."

E4 (a hire is made and adjusted):
"Good choice. You went with a take on Warren Buffett, tuned to be keener on new
technology and a little more open to risk. I'm writing that character up in full
now, then handing the plan back to the builder so it can be built and run for
real. Nothing's locked in — you can still change your mind."

E5 (final review after the workflow ran):
"All done — the workflow ran fine. Here's what your specialist added, what got
used, and what I'd suggest. Now it's your call on what happens to the role: keep
it as is, narrow the job to something tighter (same person, smaller scope), keep
the job but rework or swap the person doing it, or let the role go entirely."

## F. Roster consent prompts  (roster.md — a QUESTION the user is asked)

F1 (new hire, end of run): keep-or-let-go — ask whether to keep the persona on
the roster or let them go.

F2 (existing roster persona): show the drafted track-record entry and append
only after the user confirms; they may edit or redact it.

F3 (letting a rostered persona go): say the file will be deleted before doing it.

## G. Candidate presentation  (SKILL.md Stage 8 — how each candidate is introduced)

For each candidate, the user is told, briefly:
- Who they are, and what they're like to work with
- Why they fit this job — what they're good at, what they've done, what they care about, how they work
- What they'd bring that the others wouldn't
- One honest caution — where they might overdo it or miss something

## H. The interview options  (SKILL.md Stage 8 — the choices offered per seat)

- Hire a candidate
- Ask a candidate job-relevant questions
- Reject one candidate or the whole slate
- Request new candidates
- Adjust a candidate in natural language
- Combine qualities from candidates
