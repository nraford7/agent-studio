#!/usr/bin/env python3
"""Field override for the evidence gate, read from the field-evidence logs.

Two logs, read together:
  - the bundled seed log, `<skill-dir>/references/field-evidence.md` (read-only
    at runtime; grows by pull request);
  - the user's own log, `~/.agent-studio/field-evidence.md` (rows a run adds,
    with consent). `AGENT_STUDIO_HOME` overrides `~/.agent-studio`.

Each row is a `### YYYY-MM-DD: <task>` heading followed by `- Field: value`
lines. This script reads four of them: `Family` (must start with one of the
eight family names in evidence-gate.md), `Bound to sources` (yes | no),
`Verdict` (worse | better | mixed | same, on the deciding criterion against the
baseline) and `Weaker criterion`. A source-bound row counts only when the job
is source-bound too (`--sourced`); other rows count for every job.

Usage:
  field_gate.py check "<family>" [--sourced]
                                   most recent row for the family + its effect
  field_gate.py where              print the user log path (created with a header
                                   if missing); append new rows there
  field_gate.py due                "due" or "not due": is a self-check owed (no
                                   `self-check:` row in the last SELF_CHECK_DAYS)

The rule applied is evidence-gate.md "Field override": a most-recent row with
verdict `worse` drops the conclusion one level unless this run applies the
row's "What fixed it" step; `mixed` never moves the level but makes the weaker
criterion a required evaluation signal; `better` and `same` change nothing.
Whether the fix applies is a judgment the caller makes and states.

Exit 0 on an answer (including "no rows"); 2 on unusable input (unknown family,
or a row missing its Verdict).
"""
import datetime
import os
import re
import sys
from pathlib import Path

FAMILIES = [
    "Creative divergence",
    "Value-laden deliberation",
    "Grounded human or stakeholder simulation",
    "Multi-stakeholder subjective evaluation",
    "Sustained functional priority",
    "General critique or analytical judgment",
    "Forecasting",
    "Factual, checkable, or procedural work",
]
VERDICTS = {"worse", "better", "mixed", "same"}
SELF_CHECK_DAYS = 30
SEED = Path(__file__).resolve().parent.parent / "references" / "field-evidence.md"
ROW_RE = re.compile(r"^### (\d{4}-\d{2}-\d{2}): (.*)$", re.M)
FIELD_RE = re.compile(r"^- ([A-Za-z ]+?): (.*)$", re.M)
USER_HEADER = """# Field evidence (this machine)

Rows added by agent-studio runs here, with consent. Same row format as the
skill's `references/field-evidence.md`; the gate reads both. To share a row
publicly, generalize it (no client or confidential detail) and open a pull
request against the skill's log.

## Rows
"""


def user_log():
    home = os.environ.get("AGENT_STUDIO_HOME") or str(Path.home() / ".agent-studio")
    return Path(home) / "field-evidence.md"


def parse_rows(text, origin):
    heads = list(ROW_RE.finditer(text))
    rows = []
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        fields = {k.strip().lower(): v.strip()
                  for k, v in FIELD_RE.findall(text[h.end():end])}
        rows.append({"date": h.group(1), "task": h.group(2).strip(),
                     "origin": origin, **fields})
    return rows


def all_rows(seed=SEED, user=None):
    user = user or user_log()
    rows = []
    for path, origin in ((seed, "seed"), (user, "user")):
        if path.exists():
            rows += parse_rows(path.read_text(), origin)
    return rows


def canonical_family(name):
    for fam in FAMILIES:
        if name.strip().lower() == fam.lower():
            return fam
    raise ValueError(f"unknown family {name!r}; use one of: " + "; ".join(FAMILIES))


def decide(family, rows, sourced=False):
    fam = canonical_family(family)
    same = [r for r in rows if r.get("family", "").lower().startswith(fam.lower())
            and (sourced or r.get("bound to sources", "no").lower() != "yes")]
    if not same:
        scope = "" if sourced else " that apply to unsourced work"
        return {"family": fam, "row": None, "effect": "none",
                "say": f"No field rows for {fam}{scope}; the table conclusion stands."}
    # Most recent by date; on the same date a user row is newer than a seed row.
    row = max(same, key=lambda r: (r["date"], r["origin"] == "user"))
    verdict = row.get("verdict", "").lower()
    if verdict not in VERDICTS:
        raise ValueError(f"row {row['date']} {row['task']!r} has no valid Verdict "
                         f"(one of {sorted(VERDICTS)})")
    label = f"{row['date']}: {row['task']} ({row['origin']} log)"
    fix = row.get("what fixed it", "none recorded")
    if verdict == "worse":
        return {"family": fam, "row": label, "effect": "drop-one-level",
                "say": (f"Most recent row {label} has the panel worse on "
                        f"{row.get('weaker criterion', 'its main criterion')}. Drop "
                        f"the conclusion one level unless this run applies its fix: {fix}")}
    if verdict == "mixed":
        weaker = row.get("weaker criterion", "the weaker criterion")
        return {"family": fam, "row": label, "effect": "required-signal",
                "signal": weaker,
                "say": (f"Most recent row {label} is mixed. Level unchanged; add "
                        f"'{weaker}' as a required evaluation signal.")}
    return {"family": fam, "row": label, "effect": "none",
            "say": f"Most recent row {label} is {verdict}; the table conclusion stands."}


def self_check_due(rows, today=None):
    """A self-check row is any row whose task starts with 'self-check'."""
    today = datetime.date.fromisoformat(today) if today else datetime.date.today()
    dates = [r["date"] for r in rows if r["task"].lower().startswith("self-check")]
    last = max(dates) if dates else None
    due = last is None or (today - datetime.date.fromisoformat(last)).days > SELF_CHECK_DAYS
    return {"due": due, "last": last}


def ensure_user_log(path=None):
    path = path or user_log()
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(USER_HEADER)
    return path


def main(argv):
    if len(argv) == 2 and argv[1] == "where":
        print(ensure_user_log())
        return 0
    if len(argv) == 2 and argv[1] == "due":
        out = self_check_due(all_rows())
        print(("due" if out["due"] else "not due") + f" (last self-check: {out['last'] or 'never'})")
        return 0
    args = [a for a in argv[1:] if a != "--sourced"]
    if len(args) != 2 or args[0] != "check":
        print('usage: field_gate.py check "<family>" [--sourced] | where | due',
              file=sys.stderr)
        return 2
    try:
        result = decide(args[1], all_rows(), sourced="--sourced" in argv[1:])
    except (OSError, ValueError) as e:
        print(f"field_gate: {e}", file=sys.stderr)
        return 2
    print(result["say"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
