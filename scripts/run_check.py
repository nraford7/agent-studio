#!/usr/bin/env python3
"""Structure check for a door 4 run folder, before the combine step.

Reads `<run-dir>/run.md` (the run manifest, SKILL.md door 4) and confirms that
every lens it names left a substantive `<lens>.md`. With `--all` (run before
synthesis) it also confirms every other artifact it names exists and is not
empty; without it (run right after the lenses) those are not written yet.
Kernel rule 7 in the run's own terms: a missing or thin artifact is retried,
never silently combined around.

Manifest shape (one `- Field: value` line each):
    - Goal: <one line>
    - Recipe: <recipe row>
    - Gate: <conclusion>
    - Expected runs: <N>
    - Lenses: <name>, <name>, ...
    - Artifacts: <file>, <file>, ...      (optional: critic.md, baseline.md)

"Substantive" is structural only: at least MIN_WORDS words, not an error stub,
carries the "Dissent I would defend:" line the SUBAGENT PROMPT PREAMBLE
requires (hard-rules.md), and not ending mid-sentence on a prose line. Whether a lens is any GOOD is a
model judgment (the claim coverage check), not this script's job.

Exit 0 all present; 1 a lens or artifact is missing or thin; 2 unusable input
(no manifest, or no Lenses line).
"""
import re
import sys
from pathlib import Path

MIN_WORDS = 30
REQUIRED_FIELDS = ["Goal", "Recipe", "Gate", "Expected runs", "Lenses"]
FIELD_RE = re.compile(r"^\s*-\s*([A-Za-z ]+?)\s*:\s*(.*?)\s*$", re.M)
STUB_RE = re.compile(r"^\s*(error|exception|traceback|failed|no output)\b", re.I)
# A last line that is a list item, heading, table row or rule is not prose.
NON_PROSE_RE = re.compile(r"^\s*([-*+>|#]|\d+[.)]|---|```)")
TERMINAL = ('.', '!', '?', ':', '"', "'", ')', ']', '*', '`', '_')


def _fields(text):
    return {k.strip().lower(): v for k, v in FIELD_RE.findall(text)}


def _names(value):
    return [n.strip() for n in value.split(",") if n.strip()]


def lens_problem(path):
    if not path.exists():
        return f"{path.name}: missing"
    text = path.read_text(errors="replace")
    if not text.strip():
        return f"{path.name}: empty"
    if STUB_RE.match(text):
        return f"{path.name}: error stub, not an answer"
    if len(text.split()) < MIN_WORDS:
        return f"{path.name}: thin ({len(text.split())} words)"
    if "dissent i would defend" not in text.lower():
        return f"{path.name}: no 'Dissent I would defend:' line (PREAMBLE item 5)"
    last = [ln for ln in text.splitlines() if ln.strip()][-1].rstrip()
    if not NON_PROSE_RE.match(last) and not last.endswith(TERMINAL):
        return f"{path.name}: looks truncated (ends mid-sentence)"
    return None


def check(run_dir, include_artifacts=True):
    run_dir = Path(run_dir)
    manifest = run_dir / "run.md"
    if not manifest.exists():
        raise ValueError(f"no run.md in {run_dir}")
    fields = _fields(manifest.read_text())
    problems = [f"run.md: missing field '{f}'" for f in REQUIRED_FIELDS
                if not fields.get(f.lower())]
    lenses = _names(fields.get("lenses", ""))
    if not lenses:
        raise ValueError("run.md names no lenses")
    for lens in lenses:
        name = lens if lens.endswith(".md") else f"{lens}.md"
        p = lens_problem(run_dir / name)
        if p:
            problems.append(p)
    for art in _names(fields.get("artifacts", "")) if include_artifacts else []:
        path = run_dir / art
        if not path.exists() or not path.read_text(errors="replace").strip():
            problems.append(f"{art}: missing or empty")
    return {"lenses": lenses, "problems": problems}


def main(argv):
    args = [a for a in argv[1:] if a != "--all"]
    if len(args) != 1:
        print("usage: run_check.py <run-dir> [--all]", file=sys.stderr)
        return 2
    try:
        report = check(args[0], include_artifacts="--all" in argv[1:])
    except (OSError, ValueError) as e:
        print(f"run_check: {e}", file=sys.stderr)
        return 2
    if not report["problems"]:
        tail = " with listed artifacts." if "--all" in argv[1:] else "."
        print(f"All {len(report['lenses'])} lenses present{tail}")
        return 0
    print("Not ready to combine:")
    print("\n".join(f"- {p}" for p in report["problems"]))
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
