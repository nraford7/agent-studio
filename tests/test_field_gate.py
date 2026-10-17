"""Tests for scripts/field_gate.py (field override from the field-evidence logs)."""
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "field_gate.py"
sys.path.insert(0, str(SCRIPT.parent))
import field_gate as fg  # noqa: E402


def _row(date, family, verdict, weaker="fidelity", fix="none", bound="no"):
    return (f"### {date}: some task\n- Family: {family}\n- Bound to sources: {bound}\n"
            f"- Verdict: {verdict}\n"
            f"- Weaker criterion: {weaker}\n- What fixed it: {fix}\n\n")


def _logs(tmp_path, seed_rows, user_rows=""):
    seed, user = tmp_path / "seed.md", tmp_path / "user.md"
    seed.write_text("# Field evidence\n\n## Rows\n\n" + seed_rows)
    if user_rows:
        user.write_text("## Rows\n\n" + user_rows)
    return fg.all_rows(seed=seed, user=user)


def test_most_recent_worse_drops_a_level(tmp_path):
    rows = _logs(tmp_path, _row("2026-08-01", "Creative divergence", "better")
                 + _row("2026-09-16", "Creative divergence (hooks), bound to a source",
                        "worse", fix="a source check", bound="yes"))
    out = fg.decide("Creative divergence", rows, sourced=True)
    assert out["effect"] == "drop-one-level"
    assert "a source check" in out["say"]


def test_source_bound_row_skipped_for_unsourced_job(tmp_path):
    # The 2026-09-16 hook row lost on fidelity to a source; a naming job has none.
    rows = _logs(tmp_path, _row("2026-08-01", "Creative divergence", "better")
                 + _row("2026-09-16", "Creative divergence (hooks)", "worse", bound="yes"))
    assert fg.decide("Creative divergence", rows)["effect"] == "none"
    assert fg.decide("Creative divergence", rows, sourced=True)["effect"] == "drop-one-level"


def test_newer_better_row_reverses_an_older_worse(tmp_path):
    rows = _logs(tmp_path, _row("2026-08-01", "Forecasting", "worse")
                 + _row("2026-09-01", "Forecasting", "better"))
    assert fg.decide("Forecasting", rows)["effect"] == "none"


def test_mixed_adds_required_signal(tmp_path):
    rows = _logs(tmp_path, _row("2026-08-26", "General critique or analytical judgment",
                                "mixed", weaker="breadth"))
    out = fg.decide("general critique or analytical judgment", rows)
    assert out["effect"] == "required-signal"
    assert out["signal"] == "breadth"


def test_user_log_rows_count_and_win_ties(tmp_path):
    rows = _logs(tmp_path, _row("2026-10-01", "Forecasting", "worse"),
                 user_rows=_row("2026-10-01", "Forecasting", "better"))
    out = fg.decide("Forecasting", rows)
    assert out["effect"] == "none" and "user log" in out["row"]


def test_no_rows_means_table_stands(tmp_path):
    rows = _logs(tmp_path, _row("2026-08-01", "Forecasting", "worse"))
    assert fg.decide("Creative divergence", rows)["effect"] == "none"


def test_unknown_family_and_missing_verdict_are_errors(tmp_path):
    rows = _logs(tmp_path, "### 2026-08-01: t\n- Family: Forecasting\n\n")
    with pytest.raises(ValueError):
        fg.decide("Vibes", rows)
    with pytest.raises(ValueError):
        fg.decide("Forecasting", rows)


def test_shipped_log_rows_all_parse_with_verdicts():
    rows = fg.all_rows(user=Path("/nonexistent/field-evidence.md"))
    assert len(rows) >= 3
    for r in rows:
        assert r.get("verdict", "").lower() in fg.VERDICTS, r["task"]
        assert any(r["family"].lower().startswith(f.lower()) for f in fg.FAMILIES), r["family"]


def test_cli_where_creates_user_log(tmp_path):
    env = {"AGENT_STUDIO_HOME": str(tmp_path / "home"), "PATH": "/usr/bin:/bin"}
    out = subprocess.run([sys.executable, str(SCRIPT), "where"], env=env,
                         capture_output=True, text=True)
    assert out.returncode == 0
    path = Path(out.stdout.strip())
    assert path.exists() and "## Rows" in path.read_text()
    chk = subprocess.run([sys.executable, str(SCRIPT), "check", "Creative divergence"],
                         env=env, capture_output=True, text=True)
    assert chk.returncode == 0 and chk.stdout.strip()


# --- Self-check due (R6) -------------------------------------------------------
def test_self_check_due_when_never_run(tmp_path):
    rows = _logs(tmp_path, _row("2026-08-01", "Forecasting", "worse"))
    assert fg.self_check_due(rows, today="2026-10-17")["due"]


def test_self_check_not_due_within_window(tmp_path):
    recent = _row("2026-10-01", "General critique or analytical judgment", "better")
    recent = recent.replace("some task", "self-check: pricing review")
    rows = _logs(tmp_path, "", user_rows=recent)
    out = fg.self_check_due(rows, today="2026-10-17")
    assert not out["due"] and out["last"] == "2026-10-01"
    assert fg.self_check_due(rows, today="2026-11-15")["due"]


def test_cli_due(tmp_path):
    env = {"AGENT_STUDIO_HOME": str(tmp_path / "home"), "PATH": "/usr/bin:/bin"}
    out = subprocess.run([sys.executable, str(SCRIPT), "due"], env=env,
                         capture_output=True, text=True)
    assert out.returncode == 0 and out.stdout.startswith("due")
