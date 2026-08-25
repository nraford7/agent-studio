#!/usr/bin/env python3
"""diversity: mean pairwise semantic distance across text files.

Uses OpenAI embeddings when OPENAI_API_KEY is set and reachable, otherwise falls
back to a stdlib TF-IDF cosine (labeled "lexical (degraded)"). It never fails for
a missing API key (falls back to lexical); exit 2 only on unusable inputs (<2
readable, tokenizable files).

Run it at the generation stage (across lens outputs) and at the output stage. For
a SET output (creative options, scenarios) run it across the set. For a SINGLE
synthesis file, run it over [lens1..lensN, synthesis] and read the synthesis-vs-
lens per-pair distances: flattening shows when the synthesis is markedly FARTHER
from the outlier lens than from the majority cluster (the dissent was dropped).
"""
import json
import math
import os
import re
import sys
from collections import Counter


def _tokens(t: str):
    return re.findall(r"[a-z0-9]+", t.lower())


def tfidf_vectors(texts):
    docs = [_tokens(t) for t in texts]
    df = Counter()
    for d in docs:
        df.update(set(d))
    n = len(docs)
    vocab = sorted(df)
    idx = {w: i for i, w in enumerate(vocab)}
    vecs = []
    for d in docs:
        tf = Counter(d)
        v = [0.0] * len(vocab)
        for w, c in tf.items():
            v[idx[w]] = (c / max(len(d), 1)) * math.log((n + 1) / df[w])
        vecs.append(v)
    return vecs


def _cos(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def mean_pairwise_distance(vecs):
    pairs = [(i, j) for i in range(len(vecs)) for j in range(i + 1, len(vecs))]
    if not pairs:
        return 0.0, None, []
    dists = [(i, j, 1 - _cos(vecs[i], vecs[j])) for i, j in pairs]
    mean = sum(d for _, _, d in dists) / len(dists)
    most_redundant = min(dists, key=lambda t: t[2])
    return mean, most_redundant, dists


def _openai_vectors(texts):
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        return None
    try:
        import urllib.request

        body = json.dumps(
            {"model": "text-embedding-3-small", "input": texts}
        ).encode()
        req = urllib.request.Request(
            "https://api.openai.com/v1/embeddings",
            data=body,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read().decode())
        return [d["embedding"] for d in data["data"]]
    except Exception as e:  # noqa: BLE001 - fall back, never hard-fail
        print(f"openai embeddings failed, falling back to lexical: {e}", file=sys.stderr)
        return None


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) < 2:
        print("usage: diversity.py FILE1 FILE2 [...]", file=sys.stderr)
        return 2
    # Fail-open on unreadable inputs: skip them, keep the readable set.
    paths, texts = [], []
    for p in argv:
        try:
            texts.append(open(p, encoding="utf-8", errors="ignore").read())
            paths.append(p)
        except OSError as e:
            print(f"skip (unreadable): {p} ({e})", file=sys.stderr)
    if len(texts) < 2:
        print("need at least 2 readable files to measure diversity", file=sys.stderr)
        return 2
    argv = paths
    # Zero-vector guard: files with no tokens would read as maximal diversity.
    kept_p, kept_t = [], []
    for p, t in zip(argv, texts):
        if _tokens(t):
            kept_p.append(p)
            kept_t.append(t)
        else:
            print(f"skip (no tokens): {p}", file=sys.stderr)
    argv, texts = kept_p, kept_t
    if len(texts) < 2:
        print(
            "need at least 2 usable (tokenizable) files to measure diversity",
            file=sys.stderr,
        )
        return 2
    vecs = _openai_vectors(texts)
    backend = "openai"
    if vecs is None:
        vecs = tfidf_vectors(texts)
        backend = "lexical"
    mean, mr, dists = mean_pairwise_distance(vecs)
    out = {
        "score": round(mean, 4),
        "n": len(texts),
        "backend": backend,
        "most_redundant": [argv[mr[0]], argv[mr[1]], round(mr[2], 4)] if mr else None,
        "pairs": [
            {"a": argv[i], "b": argv[j], "distance": round(d, 4)} for i, j, d in dists
        ],
    }
    if backend == "lexical":
        out["note"] = "degraded (lexical) — set OPENAI_API_KEY for semantic diversity"
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
