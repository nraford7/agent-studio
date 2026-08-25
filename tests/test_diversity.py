import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT = str(Path(__file__).resolve().parents[1] / "scripts" / "diversity.py")


def run(paths):
    e = dict(os.environ)
    e.pop("OPENAI_API_KEY", None)
    return subprocess.run(
        [sys.executable, SCRIPT, *paths], capture_output=True, text=True, env=e
    )


def test_identical_texts_low_diversity(tmp_path):
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("the cat sat on the mat")
    b.write_text("the cat sat on the mat")
    r = run([str(a), str(b)])
    assert r.returncode == 0
    out = json.loads(r.stdout)
    assert out["backend"] == "lexical"
    assert out["score"] < 0.05


def test_different_texts_higher_diversity(tmp_path):
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("quarterly revenue and profit margins for the fiscal report")
    b.write_text("avant garde sculpture using deconstructed leather and silk")
    r = run([str(a), str(b)])
    out = json.loads(r.stdout)
    assert out["score"] > 0.5


def test_never_fails_without_key(tmp_path):
    a = tmp_path / "a.txt"
    a.write_text("one")
    b = tmp_path / "b.txt"
    b.write_text("two")
    r = run([str(a), str(b)])
    assert r.returncode == 0


def test_empty_files_not_maximal_diversity(tmp_path):
    a = tmp_path / "a.txt"
    a.write_text("")
    b = tmp_path / "b.txt"
    b.write_text("!!! ???")
    r = run([str(a), str(b)])
    assert r.returncode == 2
    assert "usable" in (r.stderr + r.stdout).lower()


def test_empty_file_skipped_but_rest_measured(tmp_path):
    a = tmp_path / "a.txt"
    a.write_text("")
    b = tmp_path / "b.txt"
    b.write_text("quarterly revenue and profit margins")
    c = tmp_path / "c.txt"
    c.write_text("avant garde sculpture in leather")
    r = run([str(a), str(b), str(c)])
    assert r.returncode == 0
    out = json.loads(r.stdout)
    assert out["n"] == 2
