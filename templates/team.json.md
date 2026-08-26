# Team Manifest (team.json)

Every compiled team package carries `team.json` at its root. It is the machine
marker and the re-entry record: workspace-wide discovery is
`find . -name team.json`. `scripts/team_validate.py` checks its structure (not its
quality). Field reference:

| Field | Type | Notes |
|---|---|---|
| `schema` | string | Manifest schema version, e.g. `1.0.0` |
| `name` | string | Human-facing team name |
| `slug` | string | Kebab-case `[a-z0-9-]+`; matches the directory name |
| `purpose` | string | One paragraph: what this team is for |
| `type` | string | `staffed-workflow` \| `standing-team` |
| `durability` | string | `reusable` \| `standing` (pairs with `type`: `staffed-workflow`↔`reusable`, `standing-team`↔`standing`) |
| `status` | string | `calibrating` \| `active` \| `dormant` \| `retired` |
| `created` | string | `YYYY-MM-DD` |
| `updated` | string | `YYYY-MM-DD` |
| `brief` | string | Path to `brief.md`, relative to the team root |
| `staffed_spec` | string | Path to `staffed-spec.md`, relative to the team root |
| `charter.approved` | boolean | Whether the Team Charter was approved |
| `charter.approved_on` | string | `YYYY-MM-DD` of charter approval |
| `methodology.kernel` | string | Kernel version inherited, e.g. `1.0.0` |
| `methodology.overlays` | array | Overlay ids from `methodologies/overlays/` |
| `in_house` | array | In-house jobs / regular-agent + tool assignments, each with a playbook path |
| `specialists` | object | role-key → `{ jd, binding, persona, evidence, proof }` (paths relative to the team root) |
| `topology` | string | `parallel` \| `sequential` \| `mixed` |
| `handoffs` | array | For sequential/complementary roles: `{ from, to, artifact, acceptance }` |
| `ensemble.exposure` | string | Progressive-exposure rule; required when `topology` is `parallel` or `mixed` |
| `ensemble.combination` | string | Combine mode from `references/synthesis-modes.md`; required when `topology` is `parallel` or `mixed` |
| `exclusions` | array | Coverage axes the team deliberately does not cover |
| `budgets` | object | `{ rounds, context, time }` |
| `checkpoints` | array | Consequential decisions where the human is consulted |
| `runs_dir` | string | Run-directory convention, e.g. `runs/<slug>-YYYY-NNN` |
| `history` | array | `{ date, change }` review and status history |

`calibrating` means the package exists but its charter is not yet approved and its
roster is not yet confirmed; no persona is active in this state. A team enters
`active` only when the charter is approved and every active specialist has its
evidence, JD, binding, persona, and proof links resolved. `dormant` is an inactive
but retained team; `retired` is closed.

Example:

```json
{
  "schema": "1.0.0",
  "name": "Weekly Market Report Team",
  "slug": "weekly-market-report",
  "purpose": "Produces a reliable weekly market report: in-house data gathering and checks, with a value-laden deliberation seat for the outlook section.",
  "type": "standing-team",
  "durability": "standing",
  "status": "active",
  "created": "2026-08-26",
  "updated": "2026-08-26",
  "brief": "brief.md",
  "staffed_spec": "staffed-spec.md",
  "charter": { "approved": true, "approved_on": "2026-08-26" },
  "methodology": { "kernel": "1.0.0", "overlays": ["scenario-planning"] },
  "in_house": [
    { "job": "data-gathering", "playbook": "playbooks/data-gathering.md" },
    { "job": "numeric-checks", "playbook": "playbooks/numeric-checks.md" }
  ],
  "specialists": {
    "outlook-deliberator": {
      "jd": "jds/outlook-deliberator.md",
      "binding": "bindings/outlook-deliberator.md",
      "persona": "personas/mireille-basco.md",
      "evidence": "evidence-cards.md",
      "proof": "work-samples/outlook-deliberator/verdict.md"
    }
  },
  "topology": "parallel",
  "handoffs": [],
  "ensemble": {
    "exposure": "isolated full outputs, then summaries + dissent, then clustered reading",
    "combination": "reconcile (dissent-carrying)"
  },
  "exclusions": ["macro forecasting is kept in-house, not personified"],
  "budgets": { "rounds": 2, "context": "single-session", "time": "under 30 min" },
  "checkpoints": ["outlook direction before drafting"],
  "runs_dir": "runs/weekly-market-report-YYYY-NNN",
  "history": [
    { "date": "2026-08-26", "change": "team created and activated" }
  ]
}
```
