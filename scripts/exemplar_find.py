#!/usr/bin/env python3
"""exemplar_find: archetype -> contrasting named exemplars (find) and corpus pull (corpus).

Two subcommands (mutually exclusive):
  find    --archetype STR [--n INT] [--max-usd FLOAT]   -> JSON lines {name, contrast, url}
  corpus  --name STR --url U [--url U ...] --out DIR     -> writes <out>/<slug>-NN.txt

All web access is via `curl` (raw pages). NO WebFetch, ever — a summarizer layer
would drop the exact wording a persona corpus needs.
"""
import argparse
import html as _html
import json
import os
import re
import subprocess
import sys


def strip_html(h: str) -> str:
    """Strip tags + script/style blocks, unescape entities, collapse whitespace."""
    h = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<[^>]+>", " ", h)
    return re.sub(r"\s+", " ", _html.unescape(h)).strip()


def _curl(url: str, timeout: int = 40) -> str:
    """Fetch a raw page with curl. Returns stdout ('' on failure)."""
    p = subprocess.run(
        ["curl", "-sfL", "--max-time", str(timeout), url],
        capture_output=True,
        text=True,
    )
    # -f makes curl fail (nonzero) on HTTP errors so a 404 body is not saved as corpus.
    return p.stdout if p.returncode == 0 else ""


def search_exemplars(archetype: str, n: int, api_key: str) -> list:
    """Exa search for iconic, contrasting instances of the archetype."""
    import urllib.request

    q = f"iconic contrasting famous {archetype} with distinct style and public writing"
    body = json.dumps(
        {
            "query": q,
            "numResults": max(n * 3, 9),
            "contents": {"text": False, "highlights": {"numSentences": 1, "highlightsPerUrl": 1}},
        }
    ).encode()
    req = urllib.request.Request(
        "https://api.exa.ai/search",
        data=body,
        headers={"x-api-key": api_key, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            data = json.loads(r.read().decode())
    except Exception as e:  # noqa: BLE001 - fail-open, print reason
        print(f"exa search failed: {e}", file=sys.stderr)
        return []
    out = []
    for item in data.get("results", [])[: max(n * 3, 9)]:
        title = (item.get("title") or "").strip()
        url = item.get("url") or ""
        hl = item.get("highlights") or []
        contrast = (hl[0].strip() if hl else "")[:160]
        if title and url:
            out.append({"name": title[:80], "contrast": contrast, "url": url})
    return out[:n]


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60] or "src"


def cmd_find(a) -> int:
    key = os.environ.get("EXA_API_KEY")
    if not key:
        print(
            "EXA_API_KEY not set — cannot search for exemplars. "
            "Set it or supply exemplars manually.",
            file=sys.stderr,
        )
        return 20
    for row in search_exemplars(a.archetype, a.n, key):
        print(json.dumps(row))
    return 0


def cmd_corpus(a) -> int:
    os.makedirs(a.out, exist_ok=True)
    written = 0
    for i, url in enumerate(a.url):
        raw = _curl(url)
        text = strip_html(raw)
        if len(text) < 40:
            print(f"skip (empty): {url}", file=sys.stderr)
            continue
        fn = os.path.join(a.out, f"{_slug(a.name)}-{i:02d}.txt")
        with open(fn, "w") as fh:
            fh.write(text)
        written += 1
    if written == 0:
        print("no pages fetched", file=sys.stderr)
        return 21
    print(f"wrote {written} file(s) to {a.out}")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="exemplar_find")
    sub = p.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("find")
    f.add_argument("--archetype", required=True)
    f.add_argument("--n", type=int, default=3)
    f.add_argument("--max-usd", type=float, default=0.5)
    c = sub.add_parser("corpus")
    c.add_argument("--name", required=True)
    c.add_argument("--url", action="append", required=True)
    c.add_argument("--out", required=True)
    a = p.parse_args(argv)
    if a.cmd == "find":
        return cmd_find(a)
    if a.cmd == "corpus":
        return cmd_corpus(a)
    return 2


if __name__ == "__main__":
    sys.exit(main())
