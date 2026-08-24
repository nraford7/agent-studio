# Hard rules (always enforced)

These are non-negotiable. The orchestrator (`SKILL.md`) obeys them and injects the
relevant ones into every subagent prompt it emits.

## Generate lenses in strict isolation

Each lens (persona) runs in its OWN subagent with a fresh context. Lenses must not
see each other's output before the combine step. Isolation is what buys genuine
viewpoint diversity and blocks anchoring.

## Never persona-swap in one shared context

Do NOT implement a "panel" by swapping personas within a single shared context or
model instance and reading them back sequentially. That is the maximally-colluding
anti-pattern: the outputs correlate hard because they share one running context.
One isolated subagent per lens, every time. A shared-context lens swap is only ever
acceptable for a throwaway single consult, never for a diversity panel.

## Anti-conformity is first-class

Ensembles collapse toward agreement even with zero incentive to agree, and more
capable models conform more. Counter it deliberately:

- Every lens prompt instructs the lens to reason ONLY from its own stance and to
  NOT anticipate, accommodate, or pre-agree with other views.
- If a recipe permits a debate round, cap it at ONE round (Strategy recipe only),
  with a stopping rule: stop as soon as a round adds no new labeled dissent.
- Prefer a dedicated critic / devil's-advocate lens over an extra generator.

## Never naive-mean-blend

Do not average, summarize-to-consensus, or "combine these into one" without
preserving dissent. Use the recipe's combine mode; the default is dissent-carrying
synthesis (majority view PLUS explicitly labeled minority and unique findings).
De-duplicate lenses by embedding BEFORE combining. See `synthesis-modes.md`.

## NO WebFetch — ever

Never use WebFetch anywhere, in the orchestrator or in any subagent. WebFetch
returns a summarizer's paraphrase and drops exact wording. Fetch raw pages with
`curl` instead. This prohibition is carried verbatim into every subagent prompt.

## Always co-report quality AND coverage

Never report a single scalar for a panel result. Always report a quality note AND a
coverage/diversity note (from `diversity.py`), so flattening is visible.

## Members must be genuinely heterogeneous

Vary panel members by stance and values, not by surface variants of one voice.
Surface-variant members (the same perspective in different costumes) add cost
without adding diversity; the differences must change what each lens attends to
and concludes, not just its tone.

## Different model families for high-stakes normative panels

Same-model swarms are low-variance and collude fast. When the work is
normative or value-laden and the stakes are high, run members (or at minimum
the critic/adversary) on different model families. Flag any same-family
adversary as a weakness.

## Vet the population, not just each member

Individually well-aligned members can form a collectively misaligned group.
Evaluate the panel as a group: consensus concentration before vs after the
combine step, conformity onset, and whether preserved disagreement actually
reaches the final output — not only per-persona quality.

## Persona construction rules

Functional stance over job title; identity via implicit narrative cues (name +
short first-person backstory + one internal contradiction); demographics OFF by
default; cap ~1000 words; named-exemplar personas are INTERPRETATIONS, labeled as
such, not the real person. Every generated persona must pass the grep lint in
`persona-template.md`.

---

## SUBAGENT PROMPT PREAMBLE

Paste this block verbatim at the top of every lens and critic subagent prompt:

```
You are a single, isolated lens on this question. Rules:
1. Reason ONLY from your assigned persona/stance below. Do not adopt a neutral
   "balanced" voice.
2. Do NOT anticipate, accommodate, or pre-agree with any other lens. You cannot see
   them and must not imagine a consensus.
3. Return your own genuine view even if you suspect it is the minority position —
   the minority view is exactly what this panel exists to capture.
4. NEVER use WebFetch. If you must read a page, use `curl -sL <url>` and read the
   raw text.
5. End with a one-line "Dissent I would defend:" stating the point you would hold
   even if outvoted.
```
