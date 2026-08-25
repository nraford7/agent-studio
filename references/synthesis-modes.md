# Synthesis modes

How you combine lens outputs is a first-order lever. Naive mean-blending of
quality-mixed lenses reliably flattens them back toward the average and discards the
standout view. Two rules always apply:

1. **De-duplicate by embedding BEFORE combining.** Run near-duplicate lenses through
   `diversity.py` and collapse pairs that are nearly identical, so the combiner is
   not flooded with the same view stated four ways.
2. **Never naive-mean-blend.** Pick a mode below; the default is Reconcile.

## Reconcile / dissent-carrying synthesis — DEFAULT

Produce the majority view PLUS explicitly labeled minority and dissenting views and
unique findings. This is the judicial "majority opinion with published dissents"
template. Use it for analytical judgment, creative direction, strategy, and normative
work — anywhere the value is an emergent combined answer that no single lens held.

Exact synthesis prompt:

```
You are combining several independent lenses on one question. Do NOT average them
into a bland consensus. Produce:
1. Majority view — where most lenses converge, and why.
2. Minority / dissenting views — each labeled with which lens holds it and the
   strongest case for it. Do not drop a view just because it is outnumbered.
3. Unique findings — points only one lens raised that the others missed.
4. Unified recommendation — your best synthesis, explicitly noting which dissent
   must survive into the decision.
Answer the underlying questions: Where do they agree? Where do they conflict? What
is the unified recommendation, and what dissent must survive?
```

## Concatenate

Append each lens output under its own heading, no merging. Use ONLY for genuinely
independent items that should not be reconciled (e.g. a set of distinct options meant
to stay separate). Apparent independence is often false when lenses came from one
model — prefer Reconcile when unsure.

## Vote

Count agreement across lenses, surface the majority answer, and flag disagreements.
For recoverable-answer tasks where a single answer is expected.

Paste-ready prompt:

```
You are tallying N independent lens answers to one question. Count agreement per
distinct answer. Output: (1) the majority answer with its count, (2) every
minority answer with its count and which lens held it, (3) a flag if any lens's
reasoning suggests the majority may be wrong. Do not blend answers.
```

## Selection

A judge picks the single best lens output. Better-evidenced than blending for tasks
with a recoverable best answer AND a competent judge — but it **cannot exceed the
best single candidate**, so never use it when you want an emergent combined answer.
For open-ended lens synthesis, use Reconcile instead.

Paste-ready judge prompt (recoverable-answer tasks only):

```
You are selecting the single best of N candidate outputs against the stated
goal. Rank all N with one-line justifications, name the winner, and list what
the winner MISSES that losing candidates contained (so the caller can graft).
Do not merge candidates.
```

On creative rows the selector is the HUMAN per hard-rules.md #Guardrails switch
by mode — never this judge prompt.

## Diversity-preserving set / variance-aware aggregate

Diversity-preserving (creative option sets, scenarios): emit the full
de-duplicated SET — no winner, no merging; the human selects.
Variance-aware aggregate (forecasting): report the center AND the spread AND the
minority tail — never the mean alone.

---

After synthesizing, measure diversity at the OUTPUT stage, not only at
generation. Two cases:

- SET outputs (creative options, scenarios): run `diversity.py` across the set —
  a large drop from generation-stage diversity with no quality gain means the
  combiner flattened the panel.
- SINGLE synthesis file (dissent-carrying recipes ONLY — a Vote or Selection
  output legitimately has no minority section): run `diversity.py` over
  [lens1..lensN, synthesis.md] and read the synthesis-vs-lens per-pair distances.
  A dissent-CARRYING synthesis contains material from every lens, so it sits
  roughly equidistant from all of them; FLATTENING shows when the synthesis is
  markedly FARTHER from the outlier lens than from the majority cluster (the
  dissent was dropped). Also grep synthesis.md for the labeled minority/dissent
  sections — their absence is itself a FAIL.
