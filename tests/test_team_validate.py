"""Tests for scripts/team_validate.py — the structural team-package validator.

Covers the spec's "Validator tests" list: valid calibrating, valid active,
missing fields, path traversal, missing referenced files, incompatible overlay,
duplicate role ids, active specialist missing links, parallel ensemble missing
rules, and an incomplete calibrating package blocked from active.
"""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "team_validate", ROOT / "scripts" / "team_validate.py"
)
team_validate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(team_validate)
validate = team_validate.validate


def _touch(base: Path, rel: str):
    p = base / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("placeholder\n")
    return rel


def _base_manifest():
    return {
        "schema": "1.0.0",
        "name": "Test Team",
        "slug": "test-team",
        "purpose": "A test team.",
        "type": "standing-team",
        "durability": "standing",
        "status": "calibrating",
        "created": "2026-08-26",
        "updated": "2026-08-26",
        "methodology": {"kernel": "1.0.0", "overlays": ["scenario-planning"]},
        "topology": "sequential",
    }


def _write(tmp_path: Path, manifest: dict, raw: str | None = None) -> Path:
    tj = tmp_path / "team.json"
    tj.write_text(raw if raw is not None else json.dumps(manifest))
    return tj


def test_valid_calibrating_team(tmp_path):
    m = _base_manifest()
    m["brief"] = _touch(tmp_path, "brief.md")
    m["staffed_spec"] = _touch(tmp_path, "staffed-spec.md")
    ok, errors = validate(_write(tmp_path, m))
    assert ok, errors


def test_valid_active_team(tmp_path):
    m = _base_manifest()
    m["status"] = "active"
    m["charter"] = {"approved": True, "approved_on": "2026-08-26"}
    m["brief"] = _touch(tmp_path, "brief.md")
    m["staffed_spec"] = _touch(tmp_path, "staffed-spec.md")
    m["topology"] = "parallel"
    m["ensemble"] = {"exposure": "isolated then summaries", "combination": "reconcile"}
    m["specialists"] = {
        "critic": {
            "jd": _touch(tmp_path, "bindings/critic.md"),
            "binding": _touch(tmp_path, "bindings/critic.md"),
            "persona": _touch(tmp_path, "personas/vera-cole.md"),
            "evidence": _touch(tmp_path, "evidence-cards.md"),
            "proof": _touch(tmp_path, "work-samples/critic/verdict.md"),
        }
    }
    ok, errors = validate(_write(tmp_path, m))
    assert ok, errors


def test_missing_required_field(tmp_path):
    m = _base_manifest()
    del m["name"]
    ok, errors = validate(_write(tmp_path, m))
    assert not ok
    assert any("name" in e for e in errors)


def test_path_traversal_rejected(tmp_path):
    m = _base_manifest()
    m["brief"] = "../../etc/passwd"
    ok, errors = validate(_write(tmp_path, m))
    assert not ok
    assert any("unsafe" in e for e in errors)


def test_absolute_path_rejected(tmp_path):
    m = _base_manifest()
    m["staffed_spec"] = "/etc/hosts"
    ok, errors = validate(_write(tmp_path, m))
    assert not ok
    assert any("unsafe" in e for e in errors)


def test_missing_referenced_file(tmp_path):
    m = _base_manifest()
    m["brief"] = "brief.md"  # never created
    ok, errors = validate(_write(tmp_path, m))
    assert not ok
    assert any("referenced file missing" in e for e in errors)


def test_incompatible_overlay(tmp_path):
    m = _base_manifest()
    m["methodology"] = {"kernel": "1.0.0", "overlays": ["time-travel"]}
    ok, errors = validate(_write(tmp_path, m))
    assert not ok
    assert any("unknown overlay" in e for e in errors)


def test_unknown_kernel(tmp_path):
    m = _base_manifest()
    m["methodology"] = {"kernel": "9.9.9", "overlays": []}
    ok, errors = validate(_write(tmp_path, m))
    assert not ok
    assert any("unknown kernel" in e for e in errors)


def test_duplicate_role_identifier(tmp_path):
    # raw JSON with a duplicated key inside specialists
    raw = json.dumps(_base_manifest())[:-1] + (
        ', "specialists": {"critic": {}, "critic": {}}}'
    )
    ok, errors = validate(_write(tmp_path, {}, raw=raw))
    assert not ok
    assert any("duplicate" in e for e in errors)


def test_active_specialist_missing_links(tmp_path):
    m = _base_manifest()
    m["status"] = "active"
    m["charter"] = {"approved": True, "approved_on": "2026-08-26"}
    m["specialists"] = {"critic": {"jd": "bindings/critic.md"}}  # missing 4 links
    _touch(tmp_path, "bindings/critic.md")
    ok, errors = validate(_write(tmp_path, m))
    assert not ok
    assert any("missing required link" in e for e in errors)


def test_parallel_ensemble_missing_rules(tmp_path):
    m = _base_manifest()
    m["topology"] = "parallel"  # no ensemble block
    ok, errors = validate(_write(tmp_path, m))
    assert not ok
    assert any("ensemble.exposure" in e for e in errors)
    assert any("ensemble.combination" in e for e in errors)


def test_calibrating_cannot_become_active_without_approval(tmp_path):
    m = _base_manifest()
    m["status"] = "active"  # but no charter approval and no specialists
    ok, errors = validate(_write(tmp_path, m))
    assert not ok
    assert any("charter.approved" in e for e in errors)


def test_invalid_status(tmp_path):
    m = _base_manifest()
    m["status"] = "running"
    ok, errors = validate(_write(tmp_path, m))
    assert not ok
    assert any("invalid status" in e for e in errors)


def test_symlink_escape_rejected(tmp_path):
    import os
    team_dir = tmp_path / "team"
    team_dir.mkdir()
    secret = tmp_path / "secret.md"  # outside the team root
    secret.write_text("x")
    os.symlink(secret, team_dir / "brief.md")
    m = _base_manifest()
    m["brief"] = "brief.md"  # string looks safe, but resolves outside
    (team_dir / "team.json").write_text(json.dumps(m))
    ok, errors = validate(team_dir / "team.json")
    assert not ok
    assert any("escapes team root" in e for e in errors)


def test_windows_absolute_rejected(tmp_path):
    m = _base_manifest()
    m["brief"] = "C:/Windows/system32/x.md"
    ok, errors = validate(_write(tmp_path, m))
    assert not ok
    assert any("unsafe" in e for e in errors)


def test_url_path_rejected(tmp_path):
    m = _base_manifest()
    m["staffed_spec"] = "https://evil.example/x.md"
    ok, errors = validate(_write(tmp_path, m))
    assert not ok
    assert any("unsafe" in e for e in errors)


def test_directory_path_is_not_a_file(tmp_path):
    (tmp_path / "brief.md").mkdir()  # a directory where a file is expected
    m = _base_manifest()
    m["brief"] = "brief.md"
    ok, errors = validate(_write(tmp_path, m))
    assert not ok
    assert any("referenced file missing" in e for e in errors)


def test_exit_code_unreadable_is_2(tmp_path):
    assert team_validate.main([str(tmp_path / "does-not-exist.json")]) == 2


def test_exit_code_structural_is_1(tmp_path):
    m = _base_manifest()
    del m["name"]
    assert team_validate.main([str(_write(tmp_path, m))]) == 1


def _full_specialist(tmp_path, role):
    return {
        link: _touch(tmp_path, f"{role}-{link}.md")
        for link in ("jd", "binding", "persona", "evidence", "proof")
    }


def test_distinct_specialists_not_flagged_duplicate(tmp_path):
    m = _base_manifest()
    m["status"] = "active"
    m["charter"] = {"approved": True, "approved_on": "2026-08-26"}
    m["specialists"] = {
        "alpha": _full_specialist(tmp_path, "alpha"),
        "beta": _full_specialist(tmp_path, "beta"),
    }
    ok, errors = validate(_write(tmp_path, m))
    assert ok, errors  # two distinct roles sharing inner key names is fine


def test_active_in_house_only_valid(tmp_path):
    m = _base_manifest()
    m["status"] = "active"
    m["charter"] = {"approved": True, "approved_on": "2026-08-26"}
    m["in_house"] = [
        {"job": "gather", "playbook": _touch(tmp_path, "playbooks/gather.md")}
    ]
    ok, errors = validate(_write(tmp_path, m))
    assert ok, errors  # a durable all-in-house team may be active
