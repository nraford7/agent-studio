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

## Selection

A judge picks the single best lens output. Better-evidenced than blending for tasks
with a recoverable best answer AND a competent judge — but it **cannot exceed the
best single candidate**, so never use it when you want an emergent combined answer.
For open-ended lens synthesis, use Reconcile instead.

---

After synthesizing, measure diversity at the OUTPUT stage (the post-synthesis set),
not only at generation. A large drop from generation-stage to output-stage diversity
with no quality gain means the combiner flattened the panel — fix the combine step.
