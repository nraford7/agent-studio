import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT = str(Path(__file__).resolve().parents[1] / "scripts" / "exemplar_find.py")


def _load():
    spec = importlib.util.spec_from_file_location("ef", SCRIPT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def run(args, env=None):
    e = dict(os.environ)
    e.pop("EXA_API_KEY", None)
    if env:
        e.update(env)
    return subprocess.run(
        [sys.executable, SCRIPT, *args], capture_output=True, text=True, env=e
    )


def test_find_exits_20_without_key():
    r = run(["find", "--archetype", "fashion designer"])
    assert r.returncode == 20
    assert "EXA_API_KEY" in (r.stderr + r.stdout)


def test_no_subcommand_errors():
    r = run([])
    assert r.returncode != 0


def test_strip_html_removes_tags():
    m = _load()
    assert m.strip_html(
        "<p>Hello <b>world</b></p><script>x=1</script>"
    ).split() == ["Hello", "world"]


def test_corpus_writes_text(tmp_path):
    src = tmp_path / "page.html"
    src.write_text(
        "<h1>Bio</h1><p>Deconstructed <b>tailoring</b> and monastic "
        "silhouettes define the house across four decades of work.</p>"
    )
    out = tmp_path / "corpus"
    m = _load()
    m._curl = lambda url, timeout=40: src.read_text()  # stub fetch
    rc = m.cmd_corpus(
        type("A", (), {"name": "Rick Owens", "url": [str(src)], "out": str(out)})()
    )
    assert rc == 0
    files = list(out.glob("*.txt"))
    assert len(files) == 1
    assert "Deconstructed tailoring and monastic" in files[0].read_text()


def test_corpus_exit_21_when_nothing(tmp_path):
    m = _load()
    m._curl = lambda url, timeout=40: ""
    rc = m.cmd_corpus(
        type("A", (), {"name": "X", "url": ["http://x"], "out": str(tmp_path / "o")})()
    )
    assert rc == 21
