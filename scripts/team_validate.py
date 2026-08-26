#!/usr/bin/env python3
"""Structural validator for a compiled team package's team.json.

Checks STRUCTURE ONLY: required fields, valid lifecycle states, safe
project-local paths, referenced files exist, kernel/overlay compatibility,
unique role identifiers, the evidence/JD/binding/persona/proof links an active
specialist owes, charter approval before `active`, and ensemble contracts for
parallel work.

It does NOT and CANNOT judge whether a persona is accurate, whether the
methodology is wise, or whether the team will perform well. Those are matters of
model and human judgment (kernel rule 9).

Usage:
    python3 scripts/team_validate.py <path-to-team.json>

Exit 0 = structurally valid. Exit 1 = one or more structural problems (printed).
Exit 2 = usage / unreadable input.
"""
import argparse
import json
import re
import sys
from pathlib import Path

KNOWN_KERNELS = {"1.0.0"}
KNOWN_OVERLAYS = {"scenario-planning", "terrain-mapping", "root-cause"}
LIFECYCLE_STATES = {"calibrating", "active", "dormant", "retired"}
VALID_TYPES = {"staffed-workflow", "standing-team"}
VALID_DURABILITY = {"reusable", "standing"}
PARALLEL_TOPOLOGIES = {"parallel", "mixed"}
SLUG_RE = re.compile(r"^[a-z0-9-]+$")
REQUIRED_TOP = [
    "schema", "name", "slug", "purpose", "type", "durability",
    "status", "created", "updated", "methodology",
]
SPECIALIST_LINKS = ["jd", "binding", "persona", "evidence", "proof"]


class _DuplicateKey(ValueError):
    pass


def _no_duplicate_keys(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise _DuplicateKey(f"duplicate key {key!r} in team.json object")
        seen[key] = value
    return seen


def _is_safe_relative(path_str):
    """A safe project-local path string: relative, no traversal, no backslash,
    no drive letter, no URL scheme. (Real-path containment is checked separately
    against the team root, to also catch symlink escapes.)"""
    if not isinstance(path_str, str) or not path_str:
        return False
    if path_str.startswith("/") or "\\" in path_str:
        return False
    if "://" in path_str or re.match(r"^[A-Za-z]:", path_str):
        return False
    p = Path(path_str)
    if p.is_absolute():
        return False
    return ".." not in p.parts


def _collect_path_fields(data):
    """Yield (label, path) for every field that names a file/dir path."""
    for field in ("brief", "staffed_spec"):
        if isinstance(data.get(field), str):
            yield field, data[field]
    for job in data.get("in_house", []) or []:
        if isinstance(job, dict) and isinstance(job.get("playbook"), str):
            yield f"in_house[{job.get('job', '?')}].playbook", job["playbook"]
    specialists = data.get("specialists", {}) or {}
    for role, spec in specialists.items():
        if not isinstance(spec, dict):
            continue
        for link in SPECIALIST_LINKS:
            if isinstance(spec.get(link), str):
                yield f"specialists.{role}.{link}", spec[link]


def validate(team_json_path):
    """Return (ok: bool, errors: list[str]) for the team.json at the path."""
    errors = []
    path = Path(team_json_path)
    if not path.is_file():
        return False, [f"team.json not found: {team_json_path}"]
    base = path.parent

    try:
        raw = path.read_text()
        data = json.loads(raw, object_pairs_hook=_no_duplicate_keys)
    except _DuplicateKey as exc:
        return False, [f"duplicate role/field identifier: {exc}"]
    except json.JSONDecodeError as exc:
        return False, [f"invalid JSON: {exc}"]

    if not isinstance(data, dict):
        return False, ["team.json top level must be an object"]

    # 1. Required fields
    for field in REQUIRED_TOP:
        if field not in data or data[field] in (None, "", []):
            errors.append(f"missing required field: {field}")

    # 2. Enumerations
    status = data.get("status")
    if status is not None and status not in LIFECYCLE_STATES:
        errors.append(
            f"invalid status {status!r} (expected one of {sorted(LIFECYCLE_STATES)})"
        )
    if data.get("type") not in VALID_TYPES and "type" in data:
        errors.append(f"invalid type {data.get('type')!r}")
    if data.get("durability") not in VALID_DURABILITY and "durability" in data:
        errors.append(f"invalid durability {data.get('durability')!r}")

    # 3. Slug shape
    slug = data.get("slug")
    if isinstance(slug, str) and not SLUG_RE.match(slug):
        errors.append(f"slug {slug!r} must match [a-z0-9-]+")

    # 4. Kernel + overlay compatibility
    methodology = data.get("methodology") or {}
    if isinstance(methodology, dict):
        kernel = methodology.get("kernel")
        if kernel not in KNOWN_KERNELS:
            errors.append(
                f"unknown kernel version {kernel!r} (known: {sorted(KNOWN_KERNELS)})"
            )
        for overlay in methodology.get("overlays", []) or []:
            if overlay not in KNOWN_OVERLAYS:
                errors.append(
                    f"unknown overlay {overlay!r} (known: {sorted(KNOWN_OVERLAYS)})"
                )
    else:
        errors.append("methodology must be an object")

    # 5. Path safety (string) + real-path containment (catches symlink escape)
    #    + existence.
    base_resolved = base.resolve()
    for label, path_str in _collect_path_fields(data):
        if not _is_safe_relative(path_str):
            errors.append(f"unsafe or non-project-local path at {label}: {path_str!r}")
            continue
        target = (base / path_str).resolve()
        if not target.is_relative_to(base_resolved):
            errors.append(f"path escapes team root at {label}: {path_str!r}")
            continue
        if not target.is_file():
            errors.append(f"referenced file missing at {label}: {path_str}")

    # 6. Active-specialist link completeness + approval gate
    specialists = data.get("specialists", {}) or {}
    if status == "active":
        charter = data.get("charter") or {}
        if not (isinstance(charter, dict) and charter.get("approved") is True):
            errors.append("status 'active' requires charter.approved == true")
        if not specialists and not data.get("in_house"):
            errors.append(
                "status 'active' requires at least one specialist or a non-empty "
                "in-house job list"
            )
        for role, spec in specialists.items():
            if not isinstance(spec, dict):
                errors.append(f"specialist {role!r} must be an object")
                continue
            for link in SPECIALIST_LINKS:
                if not spec.get(link):
                    errors.append(
                        f"active specialist {role!r} missing required link: {link}"
                    )

    # 7. Ensemble contracts for parallel work
    topology = data.get("topology")
    if topology in PARALLEL_TOPOLOGIES:
        ensemble = data.get("ensemble") or {}
        if not (isinstance(ensemble, dict) and ensemble.get("exposure")):
            errors.append(f"topology {topology!r} requires ensemble.exposure")
        if not (isinstance(ensemble, dict) and ensemble.get("combination")):
            errors.append(f"topology {topology!r} requires ensemble.combination")

    return (not errors), errors


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Structural validator for a team package team.json "
        "(structure only — never judges quality)."
    )
    parser.add_argument("team_json", help="path to a team.json file")
    args = parser.parse_args(argv)

    ok, errors = validate(args.team_json)
    if ok:
        print(f"OK: {args.team_json} is structurally valid (structure only; "
              "does not judge persona accuracy, methodology, or performance)")
        return 0
    # Exit 2 for unreadable/unparseable input; exit 1 for structural problems.
    unreadable = len(errors) == 1 and (
        errors[0].startswith("team.json not found")
        or errors[0].startswith("invalid JSON")
        or errors[0].startswith("team.json top level must be an object")
    )
    print(f"FAIL: {args.team_json} has {len(errors)} structural problem(s):")
    for err in errors:
        print(f"  - {err}")
    return 2 if unreadable else 1


if __name__ == "__main__":
    sys.exit(main())
