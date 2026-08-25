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
