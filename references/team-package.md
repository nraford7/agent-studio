# Team Package

A **team package** is the durable, re-enterable form of a staffed team. It is
produced only for the two durable outputs — a reusable staffed workflow or a
standing team — per the durability gate (`SKILL.md`). Lightweight outputs leave a
flat dossier under `agent-studio-out/`, not a package.

Agent Studio decides **who and how**; Do-It **implements** the package (Stage 10).
Neither the handoff nor the package automatically runs the team's substantive
work — the compiled skill or team is used separately for that.

## Compiled layout

When the result is reusable or standing, Do-It compiles the locked staffed
specification into a target contract equivalent to:

```text
agent-teams/<slug>/
  team.json          the manifest (see templates/team.json.md)
  README.md          human-facing (see templates/team-readme.md)
  methodology/
    kernel.md        the inherited kernel (version pinned in team.json)
    overlays/        the selected overlays
  jds/
    <role>.md        the enduring Job Description per role (Stage 5)
  bindings/
    <role>.md        the local job binding per role (Stage 8)
  personas/
    <name>.md        the hired character (references a global core)
  templates/         starter artifacts the overlays require
  runs/              one directory per run
```

The exact physical layout may be adapted when the target is a reusable skill
rather than a team directory, but the same logical contracts and references must
survive: a manifest, a README, the pinned methodology, per-role bindings,
per-hire personas, and a runs area.

## Ownership (two levels of identity)

- **Global character cores** live on the roster (`references/roster.md`,
  `~/.claude/agent-roster/`): stable identity, values, positions, experience,
  contradiction, blind spots, voice, re-anchoring, and track record.
- **Local job bindings** live in the package: role, mandate, authority, process,
  outputs, exclusions, handoffs, constraints, and the job-specific retrieval kit
  for this team.

A package references global cores but owns its bindings, charter, methodology
choices, proof, and operating records. The same character can be hired differently
for different teams without duplicating the roster.

## Discovery

The local `team.json` plus `README.md` are the discovery mechanism —
workspace-wide discovery is `find . -name team.json`. There is **no central team
registry**. An `AGENTS.md` entry may be added to the target repo only when the
user authorizes it.

## Do-It boundary

Do-It compiles and validates the package; it may not touch staffing. It integrates
the approved personas exactly as written, and it never reopens hiring. A narrow
staffing question discovered during the build comes back to Agent Studio; the rest
of the build continues. If Do-It is unavailable, Agent Studio delivers the dossier
and the locked package contract but does not claim an active team exists.
