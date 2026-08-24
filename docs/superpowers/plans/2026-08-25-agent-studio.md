# agent-studio Implementation Plan

> **For agentic workers:** This plan is executed via Agency (per the /do-it pipeline). Steps use checkbox (`- [ ]`) syntax for tracking. Scripts are built test-first (pytest); markdown deliverables are verified by structural grep checks.

**Goal:** Build the `agent-studio` Claude Code skill that constructs AI personas and assembles/optionally-runs persona panels, per the approved spec.

**Architecture:** Approach A — one `SKILL.md` orchestrates a six-stage flow (Frame → Construct → Assemble → Run → Synthesize → Emit/Evaluate). Two Python scripts do the parts the model can't do reliably in-prompt (exemplar retrieval + corpus pull; semantic diversity). Reference markdown files hold the persona template, recipe table, synthesis modes, and hard rules that the SKILL.md injects into subagent prompts.

**Tech Stack:** Markdown (SKILL.md + references), Python 3 (stdlib + optional `requests`/OpenAI; TF-IDF fallback via stdlib), pytest for script tests, curl for all web fetches.

**Spec:** `docs/superpowers/specs/2026-08-25-agent-studio-design.md`

## Global Constraints

- Scope: CONSTRUCT + ENSEMBLE only. DIAGNOSE and HARDEN are out of scope.
- NO WebFetch anywhere (scripts curl raw pages; SKILL.md forbids WebFetch in every emitted subagent prompt).
- Exactly TWO scripts (`exemplar_find.py`, `diversity.py`); persona QC is a grep lint documented in references, not a third script.
- Scripts must not hard-fail on missing optional keys: `diversity.py` falls back to TF-IDF (labeled "degraded (lexical)"); `exemplar_find.py find` exits 20 with a clear message if `EXA_API_KEY` is unset.
- Runtime artifacts go to `agent-studio-out/` in the user's cwd (never the repo dir).
- Do NOT deploy into `~/.claude/skills/`; README documents the manual deploy.
- Persona rules: functional stance over job title; implicit identity cues; demographics off by default; cap ~1000 words; named-exemplar personas labeled as interpretations.
- Ensemble rules: lenses generated in strict isolation (one subagent each, never persona-swaps in one shared context); never naive-mean-blend; default combine mode = dissent-carrying; co-report quality AND coverage.

---

### Task 1: Repo scaffolding

**Files:**
- Create: `.gitignore`, `requirements.txt`, `tests/__init__.py`
- Do NOT create `agent-studio-out/` — it is a runtime dir in the user's cwd, gitignored.

- [ ] **Step 1:** Write `.gitignore` with: `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.venv/`, `agent-studio-out/`, `.env`, `*.egg-info/`.
- [ ] **Step 2:** Write `requirements.txt`: `pytest` (test only); comment that `requests` and `openai` are OPTIONAL (scripts degrade without them). Runtime web calls use curl, not requests, per the no-dependency-on-network-libs preference; `requests` listed only as an optional convenience.
- [ ] **Step 3:** Create empty `tests/__init__.py`.
- [ ] **Step 4:** Verify: `ls .gitignore requirements.txt tests/__init__.py` all exist.
- [ ] **Step 5:** Commit: `chore: scaffold agent-studio repo`.

**Acceptance:** the three files exist; `.gitignore` contains `agent-studio-out/`.

---

### Task 2: `references/hard-rules.md`

**Files:**
- Create: `references/hard-rules.md`

- [ ] **Step 1:** Write the file with one `## ` heading per rule, each rule a short imperative paragraph, copying the spec's "Hard rules" list verbatim in substance: isolation; **never persona-swap in one shared context (maximally-colluding anti-pattern)**; anti-conformity first-class (lens prompts instruct each lens to reason from its own stance and not accommodate others; debate rounds capped at 1 for Strategy with a stopping rule); never naive-mean-blend; NO WebFetch (curl only) carried into every subagent prompt; always co-report quality AND coverage; persona construction rules (functional stance, implicit cues, demographics off, ~1000-word cap, exemplar personas are interpretations, must pass the grep lint).
- [ ] **Step 2:** Include a fenced "SUBAGENT PROMPT PREAMBLE" block that the SKILL.md pastes into every lens/critic prompt: it states the lens must (a) reason only from its assigned stance, (b) not anticipate or accommodate other lenses, (c) never use WebFetch (curl only if it must fetch), (d) return its own view even if it suspects it is the minority.
- [ ] **Step 3:** Verify: `grep -c "WebFetch" references/hard-rules.md` >= 2; `grep -qi "persona-swap" references/hard-rules.md`; `grep -qi "anti-conformity" references/hard-rules.md`.
- [ ] **Step 4:** Commit: `docs: add hard-rules reference`.

**Acceptance:** grep checks in Step 3 pass.

---

### Task 3: `references/persona-template.md`

**Files:**
- Create: `references/persona-template.md`

- [ ] **Step 1:** Write the Five-Element template with the exact headings `## Role`, `## Expertise`, `## Process`, `## Output`, `## Constraints`, plus an `## Identity` block. Under each, encode the spec's rules: Role = a functional-stance sentence (never a bare job title); Expertise = bounded list + a `Not:` exclusions line; Process = numbered steps; Output = a literal fenced template; Constraints = at least three `never ...` lines + one `Escalate when ...` line; Identity = a name, a 2-3 sentence first-person backstory, one `Internal contradiction:` line; demographics off by default.
- [ ] **Step 2:** Add a "## Lint" section documenting the grep checks the skill runs: (a) all five element headings present; (b) `grep -c "^- never\|never " ...` >= 3 in Constraints; (c) banned-phrase regex `be helpful|write clean code|ensure quality|be thorough|and so on|etc\.` returns NO matches; (d) word count <= ~1100.
- [ ] **Step 3:** Add one fully worked example persona ("Vera Cole, adversarial security reviewer") that itself passes the lint.
- [ ] **Step 4:** Verify: `grep -c "^## " references/persona-template.md` >= 6; run the banned-phrase regex against the example section and confirm no matches (the example must be lint-clean).
- [ ] **Step 5:** Commit: `docs: add persona five-element template`.

**Acceptance:** six headings present; the worked example passes the banned-phrase regex.

---

### Task 4: `references/recipes.md` and `references/synthesis-modes.md`

**Files:**
- Create: `references/recipes.md`, `references/synthesis-modes.md`

- [ ] **Step 1:** `recipes.md`: reproduce the 7-row use-case → panel table from the spec (columns: Use case, Vary by, Size, Topology, Combine, Hard rule), plus the two cross-cutting rules and the note that the 8th "Artifact/skill review" row is deferred (DIAGNOSE).
- [ ] **Step 2:** `synthesis-modes.md`: document the four combine modes (Concatenate, Reconcile/dissent-carrying [DEFAULT], Vote, Selection) with when-to-use and, for Reconcile, the exact dissent-carrying prompt ("Where do they agree? Where conflict? What is the unified recommendation, and what dissent must survive?"). State: always de-duplicate by embedding before combining; never naive-mean-blend; Selection cannot exceed the best single candidate.
- [ ] **Step 3:** Verify: `grep -c "|" references/recipes.md` >= 9 (table rows); `grep -qi "dissent" references/synthesis-modes.md`.
- [ ] **Step 4:** Commit: `docs: add recipes and synthesis-modes references`.

**Acceptance:** recipes table has >=7 data rows; synthesis-modes names all four modes and marks Reconcile default.

---

### Task 5: `exemplar_find.py` — arg dispatch + `find` subcommand (no-key + empty paths)

**Files:**
- Create: `scripts/exemplar_find.py`
- Test: `tests/test_exemplar_find.py`

**Interfaces:**
- Produces: CLI `exemplar_find.py find --archetype STR [--n INT] [--max-usd FLOAT]` printing JSON lines `{"name","contrast","url"}`; exit 20 if `EXA_API_KEY` unset. `exemplar_find.py corpus --name STR --url U [--url U...] --out DIR` (built in Task 6). Module funcs: `strip_html(html:str)->str`, `search_exemplars(archetype:str, n:int, api_key:str)->list[dict]`.

- [ ] **Step 1: Write failing tests** (`tests/test_exemplar_find.py`):

```python
import json, subprocess, sys, os
from pathlib import Path
SCRIPT = str(Path(__file__).resolve().parents[1] / "scripts" / "exemplar_find.py")

def run(args, env=None):
    e = dict(os.environ); e.pop("EXA_API_KEY", None)
    if env: e.update(env)
    return subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True, env=e)

def test_find_exits_20_without_key():
    r = run(["find", "--archetype", "fashion designer"])
    assert r.returncode == 20
    assert "EXA_API_KEY" in (r.stderr + r.stdout)

def test_no_subcommand_errors():
    r = run([])
    assert r.returncode != 0

def test_strip_html_removes_tags():
    import importlib.util
    spec = importlib.util.spec_from_file_location("ef", SCRIPT)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    assert m.strip_html("<p>Hello <b>world</b></p><script>x=1</script>") .split() == ["Hello", "world"]
```

- [ ] **Step 2: Run tests, verify they fail** — `pytest tests/test_exemplar_find.py -v` → FAIL (module/functions missing).
- [ ] **Step 3: Implement** dispatch + `find` + `strip_html`:

```python
#!/usr/bin/env python3
"""exemplar_find: archetype -> contrasting named exemplars (find) and corpus pull (corpus). curl only; NO WebFetch."""
import argparse, json, os, re, sys, subprocess, urllib.parse, html as _html

def strip_html(h: str) -> str:
    h = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<[^>]+>", " ", h)
    return re.sub(r"\s+", " ", _html.unescape(h)).strip()

def _curl(url: str, timeout: int = 40) -> str:
    p = subprocess.run(["curl", "-sL", "--max-time", str(timeout), url], capture_output=True, text=True)
    return p.stdout or ""

def search_exemplars(archetype: str, n: int, api_key: str) -> list:
    # Exa search for iconic contrasting instances of the archetype.
    import urllib.request
    q = f"iconic contrasting famous {archetype} with distinct style and public writing"
    body = json.dumps({"query": q, "numResults": max(n * 3, 9), "contents": {"text": False}}).encode()
    req = urllib.request.Request("https://api.exa.ai/search", data=body,
        headers={"x-api-key": api_key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            data = json.loads(r.read().decode())
    except Exception as e:
        print(f"exa search failed: {e}", file=sys.stderr); return []
    out = []
    for item in data.get("results", [])[: max(n * 3, 9)]:
        title = (item.get("title") or "").strip()
        url = item.get("url") or ""
        if title and url:
            out.append({"name": title[:80], "contrast": "", "url": url})
    return out[:n]

def cmd_find(a):
    key = os.environ.get("EXA_API_KEY")
    if not key:
        print("EXA_API_KEY not set — cannot search for exemplars. Set it or supply exemplars manually.", file=sys.stderr)
        return 20
    for row in search_exemplars(a.archetype, a.n, key):
        print(json.dumps(row))
    return 0

def main(argv=None):
    p = argparse.ArgumentParser(prog="exemplar_find")
    sub = p.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("find"); f.add_argument("--archetype", required=True); f.add_argument("--n", type=int, default=3); f.add_argument("--max-usd", type=float, default=0.5)
    c = sub.add_parser("corpus"); c.add_argument("--name", required=True); c.add_argument("--url", action="append", required=True); c.add_argument("--out", required=True)
    a = p.parse_args(argv)
    if a.cmd == "find": return cmd_find(a)
    if a.cmd == "corpus": return cmd_corpus(a)  # defined in Task 6
    return 2

if __name__ == "__main__":
    sys.exit(main())
```

Add a temporary `def cmd_corpus(a): return 0` stub so the module imports; Task 6 replaces it.

- [ ] **Step 4: Run tests, verify pass** — `pytest tests/test_exemplar_find.py -v` → 3 pass.
- [ ] **Step 5: Commit** — `feat: exemplar_find find subcommand + html strip`.

**Acceptance:** find exits 20 without key; strip_html strips tags and scripts; no-subcommand errors.

---

### Task 6: `exemplar_find.py` — `corpus` subcommand

**Files:**
- Modify: `scripts/exemplar_find.py` (replace `cmd_corpus` stub)
- Test: `tests/test_exemplar_find.py` (add cases)

**Interfaces:**
- Consumes: `strip_html`, `_curl` from Task 5.
- Produces: `corpus` writes `<out>/<slug>.txt` per url; exit 0 if >=1 page fetched, exit 21 if zero.

- [ ] **Step 1: Add failing tests** using a `file://` URL fixture so no network is needed:

```python
def test_corpus_writes_text(tmp_path):
    src = tmp_path / "page.html"; src.write_text("<h1>Bio</h1><p>Deconstructed <b>tailoring</b> and monastic silhouettes define the house across four decades of work.</p>")
    out = tmp_path / "corpus"
    # monkeypatch curl via PATH shim is heavy; instead call the module function directly:
    import importlib.util
    spec = importlib.util.spec_from_file_location("ef", SCRIPT)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    m._curl = lambda url, timeout=40: src.read_text()  # stub fetch
    rc = m.cmd_corpus(type("A", (), {"name": "Rick Owens", "url": [str(src)], "out": str(out)})())
    assert rc == 0
    files = list(out.glob("*.txt")); assert len(files) == 1
    assert "Deconstructed tailoring and monastic" in files[0].read_text()

def test_corpus_exit_21_when_nothing(tmp_path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("ef2", SCRIPT)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    m._curl = lambda url, timeout=40: ""
    rc = m.cmd_corpus(type("A", (), {"name": "X", "url": ["http://x"], "out": str(tmp_path/"o")})())
    assert rc == 21
```

- [ ] **Step 2: Run, verify fail** — the stub returns 0 always, so `test_corpus_exit_21` fails.
- [ ] **Step 3: Implement** `cmd_corpus`:

```python
def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60] or "src"

def cmd_corpus(a):
    os.makedirs(a.out, exist_ok=True)
    written = 0
    for i, url in enumerate(a.url):
        raw = _curl(url)
        text = strip_html(raw)
        if len(text) < 40:
            print(f"skip (empty): {url}", file=sys.stderr); continue
        fn = os.path.join(a.out, f"{_slug(a.name)}-{i:02d}.txt")
        with open(fn, "w") as fh: fh.write(text)
        written += 1
    if written == 0:
        print("no pages fetched", file=sys.stderr); return 21
    print(f"wrote {written} file(s) to {a.out}")
    return 0
```

- [ ] **Step 4: Run tests, verify pass** — `pytest tests/test_exemplar_find.py -v` → all pass.
- [ ] **Step 5: Commit** — `feat: exemplar_find corpus subcommand`.

**Acceptance:** corpus writes a stripped text file per fetched page; exit 21 when none fetched.

---

### Task 7: `diversity.py`

**Files:**
- Create: `scripts/diversity.py`
- Test: `tests/test_diversity.py`

**Interfaces:**
- Produces: CLI `diversity.py f1 f2 [...]` prints JSON `{"score": float, "n": int, "backend": "openai|lexical", "most_redundant": [a,b,dist]}`; never hard-fails without `OPENAI_API_KEY` (TF-IDF fallback labeled "lexical"). Func `tfidf_vectors(texts:list[str])->list[list[float]]`, `mean_pairwise_distance(vecs)->float`.

- [ ] **Step 1: Write failing tests:**

```python
import json, subprocess, sys, os
from pathlib import Path
SCRIPT = str(Path(__file__).resolve().parents[1] / "scripts" / "diversity.py")

def run(paths):
    e = dict(os.environ); e.pop("OPENAI_API_KEY", None)
    return subprocess.run([sys.executable, SCRIPT, *paths], capture_output=True, text=True, env=e)

def test_identical_texts_low_diversity(tmp_path):
    a = tmp_path/"a.txt"; b = tmp_path/"b.txt"
    a.write_text("the cat sat on the mat"); b.write_text("the cat sat on the mat")
    r = run([str(a), str(b)]); assert r.returncode == 0
    out = json.loads(r.stdout); assert out["backend"] == "lexical"; assert out["score"] < 0.05

def test_different_texts_higher_diversity(tmp_path):
    a = tmp_path/"a.txt"; b = tmp_path/"b.txt"
    a.write_text("quarterly revenue and profit margins for the fiscal report")
    b.write_text("avant garde sculpture using deconstructed leather and silk")
    r = run([str(a), str(b)]); out = json.loads(r.stdout)
    assert out["score"] > 0.5

def test_never_fails_without_key(tmp_path):
    a = tmp_path/"a.txt"; a.write_text("one"); b = tmp_path/"b.txt"; b.write_text("two")
    r = run([str(a), str(b)]); assert r.returncode == 0
```

- [ ] **Step 2: Run, verify fail** — `pytest tests/test_diversity.py -v` → FAIL.
- [ ] **Step 3: Implement** (stdlib TF-IDF cosine; OpenAI path only if key + lib present):

```python
#!/usr/bin/env python3
"""diversity: mean pairwise semantic distance across text files. OpenAI embeddings if available, else TF-IDF (lexical)."""
import json, math, os, re, sys
from collections import Counter

def _tokens(t): return re.findall(r"[a-z0-9]+", t.lower())

def tfidf_vectors(texts):
    docs = [_tokens(t) for t in texts]
    df = Counter(); [df.update(set(d)) for d in docs]
    n = len(docs); vocab = sorted(df)
    idx = {w: i for i, w in enumerate(vocab)}
    vecs = []
    for d in docs:
        tf = Counter(d); v = [0.0] * len(vocab)
        for w, c in tf.items():
            v[idx[w]] = (c / max(len(d), 1)) * math.log((n + 1) / (df[w])) 
        vecs.append(v)
    return vecs

def _cos(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a)); nb = math.sqrt(sum(y*y for y in b))
    if na == 0 or nb == 0: return 0.0
    return dot/(na*nb)

def mean_pairwise_distance(vecs):
    pairs = [(i, j) for i in range(len(vecs)) for j in range(i+1, len(vecs))]
    if not pairs: return 0.0, None
    dists = [(i, j, 1 - _cos(vecs[i], vecs[j])) for i, j in pairs]
    mean = sum(d for _, _, d in dists) / len(dists)
    most_redundant = min(dists, key=lambda t: t[2])
    return mean, most_redundant

def _openai_vectors(texts):
    key = os.environ.get("OPENAI_API_KEY")
    if not key: return None
    try:
        import urllib.request
        body = json.dumps({"model": "text-embedding-3-small", "input": texts}).encode()
        req = urllib.request.Request("https://api.openai.com/v1/embeddings", data=body,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read().decode())
        return [d["embedding"] for d in data["data"]]
    except Exception as e:
        print(f"openai embeddings failed, falling back to lexical: {e}", file=sys.stderr); return None

def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) < 2:
        print("usage: diversity.py FILE1 FILE2 [...]", file=sys.stderr); return 2
    texts = [open(p, encoding="utf-8", errors="ignore").read() for p in argv]
    vecs = _openai_vectors(texts); backend = "openai"
    if vecs is None:
        vecs = tfidf_vectors(texts); backend = "lexical"
    mean, mr = mean_pairwise_distance(vecs)
    out = {"score": round(mean, 4), "n": len(texts), "backend": backend,
           "most_redundant": [argv[mr[0]], argv[mr[1]], round(mr[2], 4)] if mr else None}
    if backend == "lexical": out["note"] = "degraded (lexical) — set OPENAI_API_KEY for semantic diversity"
    print(json.dumps(out, indent=2)); return 0

if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests, verify pass** — `pytest tests/test_diversity.py -v` → 3 pass.
- [ ] **Step 5: Commit** — `feat: diversity.py semantic/lexical diversity metric`.

**Acceptance:** identical texts → near-0; different texts → >0.5; never fails without OpenAI key; output labels lexical fallback.

---

### Task 8: `SKILL.md` orchestrator

**Files:**
- Create: `SKILL.md`

**Interfaces:**
- Consumes: `references/*.md`, `scripts/exemplar_find.py`, `scripts/diversity.py`.

- [ ] **Step 1:** Write YAML frontmatter: `name: agent-studio` and a trigger `description` firing on "construct a persona/agent", "build a panel/council of agents", "run an ensemble/panel", "design an agent persona", and `/agent-studio`. Keep description trigger-only (what/when), no house detail.
- [ ] **Step 2:** Write the six-stage flow as numbered sections, each a short procedure: Frame (classify task type; map to `references/recipes.md`; one `AskUserQuestion` confirm, skippable if fully specified or non-interactive), Construct (archetype criteria → `exemplar_find.py find` → `exemplar_find.py corpus` when grounding, REQUIRED when no precedent → emit persona via `references/persona-template.md` → run the grep lint), Assemble (fill the recipe row → add critic → write `agent-studio-out/panel.md`), Run (dispatch one ISOLATED subagent per lens using the SUBAGENT PROMPT PREAMBLE from `references/hard-rules.md`, then the critic), Synthesize (dedupe by embedding → combine per `references/synthesis-modes.md`, default dissent-carrying → write `synthesis.md`), Emit/Evaluate (run `diversity.py` on lens outputs AND post-synthesis set → write `diversity.md`; co-report quality + coverage).
- [ ] **Step 3:** Add a "Hard rules (always)" section that inlines the key rules and links `references/hard-rules.md`; state artifacts go to `agent-studio-out/` in cwd; state file-based stage hand-off. In the Assemble stage, state that the generate-by-default path emits BOTH `agent-studio-out/panel.md` AND `agent-studio-out/synthesis-prompt.md` (the paste-ready dissent-carrying prompt from `references/synthesis-modes.md`); the run path additionally writes `synthesis.md`. Note the persona grep lint is a RUNTIME SKILL step run against each generated persona — no automated test covers generated output (inherent to a prompt-driven skill).
- [ ] **Step 4:** Verify structure:
  Run: `head -6 SKILL.md | grep -q "name: agent-studio" && grep -qi "isolation\|isolated" SKILL.md && grep -qiE "never.*webfetch|no webfetch|webfetch.*(forbid|never)" SKILL.md && grep -qi "dissent-carrying" SKILL.md && grep -qi "agent-studio-out" SKILL.md && grep -qi "synthesis-prompt.md" SKILL.md`
  Expected: frontmatter name present; isolation, a WebFetch PROHIBITION (not usage), dissent-carrying, agent-studio-out, and synthesis-prompt.md all found.
- [ ] **Step 5:** Commit — `feat: SKILL.md orchestrator for agent-studio`.

**Acceptance:** valid frontmatter with `name: agent-studio` + trigger description; all six stages present; hard rules referenced; the WebFetch grep matches a PROHIBITION (never/no/forbid), not a usage instruction; `panel.md` and `synthesis-prompt.md` both named as generate-by-default deliverables.

---

### Task 9: `README.md` + final integration verification

**Files:**
- Create: `README.md`

- [ ] **Step 1:** Write README: what agent-studio is (1 paragraph), the two uses, the six-stage flow (bulleted), the two scripts + their subcommands, optional env keys (`EXA_API_KEY`, `OPENAI_API_KEY`) and graceful degradation, and a **Deploy** section: `cp -R ~/Projects/agent-studio ~/.claude/skills/agent-studio` OR symlink; note it is NOT auto-deployed. Link the spec + Playbook as provenance.
- [ ] **Step 2:** Run the whole test suite: `python3 -m pytest -q` → all pass.
- [ ] **Step 3:** Run the persona-template banned-phrase lint against the worked example to confirm lint-clean; run `env -u OPENAI_API_KEY python3 scripts/diversity.py references/persona-template.md references/recipes.md` to confirm the script runs end-to-end (exit 0; backend "lexical" with OPENAI_API_KEY unset).
- [ ] **Step 4:** Run `exemplar_find.py find --archetype "fashion designer"` without a key → confirm exit 20 with the clear message (proves the graceful path).
- [ ] **Step 5:** Commit — `docs: README + deploy guide`.

**Acceptance:** full pytest green; both scripts run end-to-end on the graceful/degraded paths; README documents manual deploy.
