"""Tests for scripts/run_check.py (door 4 run manifest + lens artifact check)."""
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "run_check.py"
sys.path.insert(0, str(SCRIPT.parent))
import run_check as rc  # noqa: E402

GOOD = ("# CFO lens\nRecommend: do not switch next quarter. Usage pricing makes "
        "revenue lumpy, and with fourteen months of runway forecastability matters "
        "more than upside. Run a hybrid pilot on new logos only, with a seat floor "
        "plus usage overage, and protect the two largest accounts.\n"
        "Dissent I would defend: the two largest accounts decide this, not the model.\n")

MANIFEST = """# Run
- Goal: decide whether to move to usage pricing
- Recipe: Analytical judgment / decision review
- Gate: Research supports trying this.
- Expected runs: 7
- Lenses: cfo, growth
- Artifacts: critic.md, baseline.md
"""


def _run(tmp_path, manifest=MANIFEST, files=None):
    if manifest is not None:
        (tmp_path / "run.md").write_text(manifest)
    default = {"cfo.md": GOOD, "growth.md": GOOD, "critic.md": GOOD, "baseline.md": GOOD}
    for name, text in (default if files is None else files).items():
        if text is not None:
            (tmp_path / name).write_text(text)
    return tmp_path


def test_complete_run_passes(tmp_path):
    report = rc.check(_run(tmp_path))
    assert report["problems"] == []


def test_missing_lens_is_reported(tmp_path):
    report = rc.check(_run(tmp_path, files={"cfo.md": GOOD, "critic.md": GOOD,
                                            "baseline.md": GOOD}))
    assert any("growth.md" in p and "missing" in p for p in report["problems"])


def test_empty_and_error_stub_lenses_are_thin(tmp_path):
    report = rc.check(_run(tmp_path, files={
        "cfo.md": "", "growth.md": "Error: request failed (529 overloaded).\n",
        "critic.md": GOOD, "baseline.md": GOOD}))
    joined = "\n".join(report["problems"])
    assert "cfo.md" in joined and "growth.md" in joined


def test_truncated_prose_lens_is_flagged(tmp_path):
    cut = GOOD.rstrip().rstrip(".") + " and then we will\n"
    report = rc.check(_run(tmp_path, files={"cfo.md": GOOD, "growth.md": cut,
                                            "critic.md": GOOD, "baseline.md": GOOD}))
    assert any("growth.md" in p and "truncated" in p for p in report["problems"])


def test_lens_without_dissent_line_is_flagged(tmp_path):
    bare = GOOD.split("Dissent I would defend")[0]
    report = rc.check(_run(tmp_path, files={"cfo.md": GOOD, "growth.md": bare,
                                            "critic.md": GOOD, "baseline.md": GOOD}))
    assert any("growth.md" in p and "Dissent" in p for p in report["problems"])


def test_list_ending_is_not_truncation(tmp_path):
    names = GOOD + "\n- Oatbound\n- Groundswell\n- Field Pour\n"
    report = rc.check(_run(tmp_path, files={"cfo.md": GOOD, "growth.md": names,
                                            "critic.md": GOOD, "baseline.md": GOOD}))
    assert report["problems"] == []


def test_missing_other_artifact_is_reported(tmp_path):
    report = rc.check(_run(tmp_path, files={"cfo.md": GOOD, "growth.md": GOOD,
                                            "critic.md": GOOD}))
    assert any("baseline.md" in p for p in report["problems"])


def test_artifacts_skipped_right_after_lenses(tmp_path):
    # The first check runs before the critic and baseline exist.
    run = _run(tmp_path, files={"cfo.md": GOOD, "growth.md": GOOD})
    assert rc.check(run, include_artifacts=False)["problems"] == []
    assert rc.check(run)["problems"]


def test_manifest_fields_required(tmp_path):
    report = rc.check(_run(tmp_path, manifest="# Run\n- Lenses: cfo, growth\n"))
    joined = "\n".join(report["problems"])
    for field in ("Goal", "Recipe", "Gate", "Expected runs"):
        assert field in joined


def test_cli_exit_codes(tmp_path):
    ok_dir = tmp_path / "a"
    ok_dir.mkdir()
    ok = subprocess.run([sys.executable, str(SCRIPT), str(_run(ok_dir)), "--all"],
                        capture_output=True, text=True)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    bad_dir = tmp_path / "b"
    bad_dir.mkdir()
    bad = subprocess.run([sys.executable, str(SCRIPT),
                          str(_run(bad_dir, files={"cfo.md": GOOD}))],
                         capture_output=True, text=True)
    assert bad.returncode == 1
    assert "growth.md" in bad.stdout
    none_dir = tmp_path / "c"
    none_dir.mkdir()
    unusable = subprocess.run([sys.executable, str(SCRIPT), str(none_dir)],
                              capture_output=True, text=True)
    assert unusable.returncode == 2
