# agent-studio Fix Cycle Implementation Plan

> **For agentic workers:** Executed via Agency (per the /do-it pipeline). Steps use checkbox syntax. All verify commands run from repo root /Users/noahraford/Projects/agent-studio.

**Goal:** Apply the 10 reconciled review fixes (F1-F10) surgically.

**Architecture:** Three chunks ordered so references land before SKILL.md references them: C1 scripts+tests, C2 references, C3 SKILL.md+README.

**Tech Stack:** Markdown, Python 3, pytest.

**Spec:** `docs/superpowers/specs/2026-08-25-agent-studio-fixes-design.md`

## Global Constraints

- Surgical edits; no renames; keep existing 8 tests green; prior-cycle grep gates must still pass (frontmatter triggers, `synthesis-prompt.md` in SKILL.md, recipes row greps, persona lint on worked example).
- The Diagnose-mode reference to a TARGET's `scripts/` dir stays target-relative (exempt from F1).

---

### Task 1 (C1): diversity.py zero-vector fix + test

**Files:** Modify `scripts/diversity.py`; Test `tests/test_diversity.py`

- [ ] **Step 1: Failing test** — append to tests/test_diversity.py:

```python
def test_empty_files_not_maximal_diversity(tmp_path):
    a = tmp_path / "a.txt"; a.write_text("")
    b = tmp_path / "b.txt"; b.write_text("!!! ???")
    r = run([str(a), str(b)])
    assert r.returncode == 2
    assert "usable" in (r.stderr + r.stdout).lower()

def test_empty_file_skipped_but_rest_measured(tmp_path):
    a = tmp_path / "a.txt"; a.write_text("")
    b = tmp_path / "b.txt"; b.write_text("quarterly revenue and profit margins")
    c = tmp_path / "c.txt"; c.write_text("avant garde sculpture in leather")
    r = run([str(a), str(b), str(c)])
    assert r.returncode == 0
    out = json.loads(r.stdout)
    assert out["n"] == 2
```

- [ ] **Step 2:** Run `python3 -m pytest tests/test_diversity.py -v` → the two new tests FAIL (currently empty files score 1.0 and are counted).
- [ ] **Step 3: Implement** in `diversity.py` main(), inserted IMMEDIATELY AFTER the existing `argv = paths` line (so path labels stay aligned), add a tokenization filter:

```python
    # Zero-vector guard: files with no tokens would read as maximal diversity.
    kept_p, kept_t = [], []
    for p, t in zip(argv, texts):
        if _tokens(t):
            kept_p.append(p); kept_t.append(t)
        else:
            print(f"skip (no tokens): {p}", file=sys.stderr)
    argv, texts = kept_p, kept_t
    if len(texts) < 2:
        print("need at least 2 usable (tokenizable) files to measure diversity", file=sys.stderr)
        return 2
```

Also update the docstring: replace the "post-synthesis set" output-stage sentence with the F2 interpretation (single synthesis: measure synthesis-vs-each-lens; flattening = synthesis markedly farther from the outlier lens than from the majority); replace the never-hard-fails sentence (NOTE: it wraps across two lines in the file; match accordingly) with "It never fails for a missing API key (falls back to lexical); exit 2 only on unusable inputs."
- [ ] **Step 4:** `python3 -m pytest tests/test_diversity.py -v` → all pass (3 old + 2 new).
- [ ] **Step 5:** Commit `fix: diversity.py zero-vector guard + doc accuracy`.

**Acceptance:** 5 diversity tests green; docstring contains "outlier" and the reworded never-fails claim.

---

### Task 2 (C1): exemplar_find.py dedup, --n validation, --max-usd removal + tests

**Files:** Modify `scripts/exemplar_find.py`; Test `tests/test_exemplar_find.py`

- [ ] **Step 1: Failing tests** — append:

```python
def test_n_zero_rejected():
    r = run(["find", "--archetype", "x", "--n", "0"])
    assert r.returncode != 0 and r.returncode != 20

def test_dedupe_same_domain_and_title():
    m = _load()
    rows = [
        {"name": "Rick Owens Interview", "contrast": "", "url": "https://vogue.com/a"},
        {"name": "Rick Owens interview", "contrast": "", "url": "https://vogue.com/b"},
        {"name": "Chanel at 100", "contrast": "", "url": "https://ft.com/c"},
    ]
    out = m.dedupe_leads(rows)
    assert len(out) == 2
```

- [ ] **Step 2:** Run → FAIL (`--n 0` currently accepted; `dedupe_leads` missing).
- [ ] **Step 3: Implement:** (a) argparse: `f.add_argument("--n", type=positive_int, default=3)` with

```python
def positive_int(v):
    i = int(v)
    if i < 1:
        raise argparse.ArgumentTypeError("--n must be >= 1")
    return i
```

(b) remove the `--max-usd` argument and its docstring mention entirely; (c) add and wire `dedupe_leads(rows)` — the title lives in the `name` key; normalize it (lowercase, strip non-alnum) + domain; drop a row when BOTH its domain matches a kept row's domain AND normalized-title similarity is high (first 40 chars equal after normalization); call it in `search_exemplars` before the `[:n]` slice; (d) docstring: state plainly that `find` returns LEADS (page titles + URLs) that the caller must resolve into named people, and scope the curl claim: "page fetching uses curl; API calls (Exa) use urllib over HTTPS — neither is WebFetch."
- [ ] **Step 4:** `python3 -m pytest tests/test_exemplar_find.py -v` → all pass (5 old + 2 new).
- [ ] **Step 5:** Commit `fix: exemplar_find lead dedup, --n validation, drop --max-usd`.

**Acceptance:** 7 exemplar tests green; `grep -c "max-usd" scripts/exemplar_find.py` = 0; docstring contains "LEADS" (or "leads") and the scoped curl claim.

---

### Task 3 (C2): synthesis-modes.md — per-mode prompts + corrected closing rule

**Files:** Modify `references/synthesis-modes.md`

- [ ] **Step 1:** Under `## Vote`, add a fenced paste-ready prompt: "You are tallying N independent lens answers to one question. Count agreement per distinct answer. Output: (1) the majority answer with its count, (2) every minority answer with its count and which lens held it, (3) flag whether any lens's reasoning suggests the majority may be wrong. Do not blend answers."
- [ ] **Step 2:** Under `## Selection`, add a fenced paste-ready judge prompt: "You are selecting the single best of N candidate outputs against the stated goal. Rank all N with one-line justifications, name the winner, and list what the winner MISSES that losers contained (so the caller can graft). Do not merge candidates." Plus the note: "On creative rows the selector is the HUMAN per hard-rules.md #Guardrails switch by mode — never this judge prompt." (That anchor is created in Task 4 — do NOT "correct" or drop the reference; if executing strictly in order, it is a forward reference that lands one task later.)
- [ ] **Step 3:** Add one-line instructions for diversity-preserving (emit the full de-duplicated SET, no winner) and variance-aware aggregate (report center AND spread AND the minority tail, never the mean alone).
- [ ] **Step 4:** Replace the closing paragraph's output-stage rule with the F2 interpretation: SET outputs → diversity.py across the set; single synthesis.md → diversity.py over [lenses + synthesis], flattening = synthesis markedly farther from the outlier lens than from the majority cluster; ALSO grep synthesis.md for the labeled minority/dissent sections — absence is a FAIL. IMPORTANT: the rewritten paragraph MUST retain the literal phrase "measure diversity at the OUTPUT stage" (harden-checklist item 8 cites it as an anchor).
- [ ] **Step 5:** Verify: `test $(grep -c '^```' references/synthesis-modes.md) -ge 6 && grep -qi "outlier" references/synthesis-modes.md && grep -qi "HUMAN" references/synthesis-modes.md`
- [ ] **Step 6:** Commit `fix: per-mode synthesis prompts + corrected output-stage rule`.

**Acceptance:** >=3 fenced prompts (6+ fence lines); outlier interpretation present; human-selector note present.

---

### Task 4 (C2): hard-rules.md — mode-switched guardrails + critic preamble + curl scope

**Files:** Modify `references/hard-rules.md`

- [ ] **Step 1:** Add a new section `## Guardrails switch by mode` (before "Persona construction rules"): JUDGMENT mode (fact-finding, evaluation, decision review, forecasting, normative) = strict: demographics off, stereotype-probe QC, positions grounded in real citable stances. CREATIVE mode (ideation, creative direction, divergent options) = flavor-forward: strongly opinionated/exaggerated personas encouraged (bias is pigment, not contamination); the QC check is a CLICHE-check (lazy archetypes collapse into one generic voice — that flattening is the failure), not a stereotype-probe; HUMAN selection of creative options is mandatory (the skill presents the divergent spread, never picks the winner); do-not-max-spread still applies; demographics stay off-by-default here too (flavor comes from stance/method/taste).
- [ ] **Step 2:** Update `## Persona construction rules` to reference the mode switch ("QC check per mode: stereotype-probe in judgment mode, cliche-check in creative mode").
- [ ] **Step 3:** Amend the SUBAGENT PROMPT PREAMBLE's introduction line from "every lens and critic subagent prompt" to "every GENERATING-LENS subagent prompt; the critic uses the CRITIC PREAMBLE below" (removing the contradiction F4 exists to fix). Then, after the SUBAGENT PROMPT PREAMBLE block, add a `## CRITIC PREAMBLE` fenced block: "You are the critic for this panel. Unlike the generating lenses, you SEE all their outputs below. Rules: 1. Steelman each lens's strongest point before challenging it. 2. Attack the weakest reasoning wherever it sits, majority or minority. 3. Do not manufacture consensus; your job is to sharpen disagreement that matters and kill weak arguments. 4. Never use WebFetch (curl raw pages only if you must fetch). 5. End with: the single strongest objection to the majority view, and the minority point most worth preserving."
- [ ] **Step 4:** In `## NO WebFetch — ever`, scope the claim: "Fetch raw PAGES with curl. (Structured API calls — Exa search, embeddings — use HTTPS libraries and are fine; the prohibition is on summarizer-mediated page fetching.)" Also state in the isolation section: "Isolation applies to the GENERATING lenses. The critic is not a generator: it runs after them and receives their outputs (see CRITIC PREAMBLE)."
- [ ] **Step 5:** Verify: `grep -q "Guardrails switch by mode" references/hard-rules.md && grep -qi "cliche\|cliché" references/hard-rules.md && grep -q "CRITIC PREAMBLE" references/hard-rules.md && grep -qi "critic is not a generator" references/hard-rules.md`
- [ ] **Step 6:** Commit `feat: mode-switched guardrails + critic preamble`.

**Acceptance:** all four greps pass; SUBAGENT PROMPT PREAMBLE unchanged for generators.

---

### Task 5 (C2): persona-template.md — Positions block + drift subsection + mode line

**Files:** Modify `references/persona-template.md`

- [ ] **Step 1:** In the Template fenced block after `## Constraints`, add an optional block:

```markdown
## Positions (optional; required for strategy/normative/value-laden recipes and opinionated creative lenses)
- <substantive stance, opinion, or red line this persona would actively defend>
- <another>
```

Below the template, add the rule: judgment-mode positions must be grounded in real, citable stances (never invented); creative-mode positions may be authored for flavor (see hard-rules.md #Guardrails switch by mode). Neutral analytical lenses omit the block.
- [ ] **Step 2:** Add subsection `## Long-running use (drift)` after the Lint section: personas drift over long conversations — they soften toward the default assistant as context accumulates. For reused/solo personas: re-inject the persona file at intervals or at the first drift sign (out-of-character hedging, generic voice); RE-ANCHOR, do not reset the conversation; keep the identity text on a separate layer from task context so task pressure does not bleed into character.
- [ ] **Step 3:** Update the Lint section: add check 5 — "Positions block present when the recipe requires it (strategy/normative/value-laden, opinionated creative)". Add the mode line: the QC probe is mode-switched per hard-rules.md.
- [ ] **Step 4:** Verify: `grep -q "## Positions" references/persona-template.md && grep -qi "Long-running use" references/persona-template.md && grep -qi "re-anchor\|RE-ANCHOR" references/persona-template.md && grep -qi "Guardrails switch by mode" references/persona-template.md` and re-run the worked-example banned-phrase lint (must stay clean).
- [ ] **Step 5:** Commit `feat: Positions block + drift guidance in persona template`.

**Acceptance:** greps pass; worked example still lint-clean.

---

### Task 6 (C2): harden-checklist.md — recipe-aware item 5, 11th item, evidence model, mode note

**Files:** Modify `references/harden-checklist.md`

- [ ] **Step 1:** Rewrite item 5: "Combine mode matches THE RECIPE'S declared mode? Score against the recipe row, not against dissent-carrying universally. Mismatch = FAIL (HIGH when the recipe called for dissent-carrying, MED otherwise); match = PASS; no declared recipe (prose/grep ingest) = infer the row from task type or score UNKNOWN. [source: recipes.md table; synthesis-modes.md]"
- [ ] **Step 2:** Rename the heading "## The ten checks" to "## The eleven checks". Add item 11: "Drift management for REUSED personas (re-anchoring plan, identity separate from task context)? [source: persona-template.md #Long-running use (drift)] Severity: LOW. N-A for one-shot panel lenses."
- [ ] **Step 3:** Update the intro and report template: results are PASS / FAIL / N-A / UNKNOWN; add an Evidence column (file/line/output that supports the verdict); state: "Declared intent (panel.md) is NOT evidence of runtime behavior — if only intent exists for a runtime check, score UNKNOWN, not PASS."
- [ ] **Step 4:** Add the mode note near the top: "Mode matters: a flavor-forward creative persona (strong opinions, exaggeration) is NOT a bias failure — but a CLICHE persona is (archetype collapse flattens diversity). See hard-rules.md #Guardrails switch by mode."
- [ ] **Step 5:** Verify: `test $(grep -c "source:" references/harden-checklist.md) -ge 11 && grep -q "UNKNOWN" references/harden-checklist.md && grep -qi "Evidence" references/harden-checklist.md && grep -qi "NOT evidence" references/harden-checklist.md && grep -qi "cliche\|cliché" references/harden-checklist.md`
- [ ] **Step 6:** Commit `feat: harden evidence model + recipe-aware combine check + drift item`.

**Acceptance:** all five greps pass; 11 numbered items.

---

### Task 7 (C2): diagnose-rubric.md — three-condition gate + classifier fix + mode note

**Files:** Modify `references/diagnose-rubric.md`

- [ ] **Step 1:** In `## Classify each stage`, remove "scoring against a fixed rubric" from the MECHANICAL list; replace with "scoring where the ANSWER is mechanically recoverable (counting, exact matching)". Add to the rule of thumb: "mechanical means the ANSWER is recoverable, not merely that a rubric exists — fixed-rubric scoring whose items require judgment is judgment-laden."
- [ ] **Step 2:** In `## Map to a recipe`, insert the gate BEFORE recommending a panel: "A judgment-laden stage earns a panel ONLY if all three hold: (1) the task is defeasible/normative (no single recoverable answer); (2) genuinely heterogeneous members are constructible (different stances/values, not surface variants); (3) the combine step can preserve disagreement. Plus a cost sanity line: a panel costs N+1 subagent runs — is the stage's decision worth that? Failing any condition → 'single strong pass' even though judgment-laden."
- [ ] **Step 3:** Add the mode note: "When diagnosing creative stages, apply the flavor-forward guardrails (hard-rules.md #Guardrails switch by mode): strong opinionated lenses are the design, not a bias defect; flag cliche/archetype-collapse instead."
- [ ] **Step 4:** Verify: `grep -qi "ONLY if all three" references/diagnose-rubric.md && grep -qi "single strong pass" references/diagnose-rubric.md && ! grep -qi "scoring against a fixed rubric" references/diagnose-rubric.md && grep -qi "Guardrails switch by mode" references/diagnose-rubric.md`
- [ ] **Step 5:** Commit `fix: diagnose three-condition gate + classifier correction`.

**Acceptance:** all greps pass.

---

### Task 8 (C2): recipes.md — creative rows reference the mode switch

**Files:** Modify `references/recipes.md`

- [ ] **Step 1:** In the Creative ideation row's hard-rule cell, append "; flavor-forward guardrails apply (hard-rules.md)". Same for the Creative direction row. Below the table add one line: "Creative rows run under the flavor-forward guardrails; judgment rows under the strict rulebook. See hard-rules.md #Guardrails switch by mode."
- [ ] **Step 2:** Verify: `grep -qi "flavor-forward" references/recipes.md && grep -qi "dedup + severity-rank" references/recipes.md`
- [ ] **Step 3:** Commit `docs: recipes creative rows reference mode-switched guardrails`.

**Acceptance:** both greps pass (prior-cycle row gate intact).

---

### Task 9 (C3): SKILL.md — paths, stage 6, per-recipe prompt, critic, positions, counts + README

**Files:** Modify `SKILL.md`, `README.md`

- [ ] **Step 1 (F1):** Add under "## Scripts" (or a new "Locating the scripts" note above it): "The scripts live in THIS skill's directory, not the user's cwd. Resolve `<skill-dir>` = the base directory containing this SKILL.md (reported when the skill loads) and invoke `python3 <skill-dir>/scripts/...`." Replace both bare invocations in stage 2 (`scripts/exemplar_find.py find|corpus`) and stage 6 (`scripts/diversity.py`) with `<skill-dir>/scripts/...` forms. Do NOT touch the Diagnose-mode reference to the target's `scripts/` directory.
- [ ] **Step 2 (F2):** Rewrite stage 6: SET outputs → run diversity.py across the set; single synthesis.md → run diversity.py over [all lens outputs + synthesis.md] and read the synthesis-vs-lens per-pair distances — flattening = synthesis markedly FARTHER from the outlier lens than from the majority cluster (dissent dropped); roughly equidistant = dissent carried. ALSO grep synthesis.md for the labeled "Minority" / "dissent" sections; absence = FAIL. Keep the quality+coverage co-report.
- [ ] **Step 3 (F3):** In Assemble: "write `agent-studio-out/synthesis-prompt.md` carrying the paste-ready prompt FOR THE RECIPE'S COMBINE MODE from `references/synthesis-modes.md` (dissent-carrying only when the recipe says so)."
- [ ] **Step 4 (F4):** Rewrite stage 4: lenses first (isolated, generator preamble); THEN the critic, which is NOT isolated from the outputs — it receives all lens outputs and uses the CRITIC PREAMBLE from hard-rules.md. Keep the words "critic" and "receives" on the SAME line (the verify grep is line-based), and use a straight apostrophe in "recipe's combine mode".
- [ ] **Step 5 (F5):** In Assemble add: "verify members differ in POSITIONS/conclusions, not just tone; for strategy/normative/value-laden recipes and opinionated creative lenses, each persona carries a Positions block per the template."
- [ ] **Step 6 (S3):** Mode: Harden — "Run the eleven checks, scoring each PASS / FAIL / N-A / UNKNOWN". Hard rules bullet list: add one line pointing at "Guardrails switch by mode". README: "ten-point" → "eleven-point"; "never hard-fails" → "never fails for a missing API key (exit 2 only on unusable inputs)"; note that `find` returns leads (titles+URLs) the skill resolves into named people.
- [ ] **Step 7:** Verify: `! grep -q "python3 scripts/" SKILL.md && grep -q "skill-dir" SKILL.md && grep -qi "outlier" SKILL.md && grep -qi "RECIPE'S COMBINE MODE\|recipe's combine mode" SKILL.md && grep -i critic SKILL.md | grep -qi "receiv" && grep -qi "eleven" SKILL.md && grep -qi "eleven-point" README.md && grep -qi "leads" README.md && head -6 SKILL.md | grep -q "name: agent-studio" && grep -qi "synthesis-prompt.md" SKILL.md`
- [ ] **Step 8:** Full gate: `python3 -m pytest -q` (12 tests green) + worked-example lint + prior-cycle reference greps.
- [ ] **Step 9:** Commit `fix: skill-dir paths, executable stage-6 diversity, per-recipe synthesis, critic inputs`.

**Acceptance:** all Step-7 greps pass; 12/12 tests green.
