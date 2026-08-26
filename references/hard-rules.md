# Hard rules (always enforced)

These are non-negotiable. The orchestrator (`SKILL.md`) obeys them and injects the
relevant ones into every subagent prompt it emits.

## Generate lenses in strict isolation

Each lens (persona) runs in its OWN subagent with a fresh context. Lenses must not
see each other's output before the combine step. Isolation is what buys genuine
viewpoint diversity and blocks anchoring. Isolation applies to the GENERATING
lenses; the critic is not a generator — it runs after them and receives their
outputs (see CRITIC PREAMBLE below).

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
returns a summarizer's paraphrase and drops exact wording. Fetch raw PAGES with
`curl` instead. (Structured API calls — Exa search, embeddings — use HTTPS
libraries and are fine; the prohibition is on summarizer-mediated page
fetching.) This prohibition is carried verbatim into every subagent prompt.

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

## Guardrails switch by mode

The persona guardrails are not global — they switch with the kind of work.

**JUDGMENT mode** (fact-finding, evaluation, decision review, forecasting,
normative): the strict rulebook. Demographics off; the persona QC probe is a
STEREOTYPE-probe; positions must be grounded in real, citable stances (never
invented). Here bias is contamination — a skewed lens produces wrong answers
with confidence.

**CREATIVE mode** (ideation, creative direction, divergent options): the
flavor-forward rulebook. Strongly opinionated, even exaggerated personas are
encouraged — bias is pigment, not contamination; an extreme lens is the value.
The QC probe becomes a CLICHE-check, not a stereotype-probe: lazy archetypes
(the tortured artist, the stern German engineer) collapse into one generic
voice, and that flattening is the failure. HUMAN selection of creative options
is mandatory — the skill presents the divergent spread and never picks the
winner. Do-not-max-spread still applies (extreme heterogeneity destabilizes).
Demographics stay off-by-default here too: flavor comes from stance, method,
and taste, and a demographic label needs the same explicit task justification
as everywhere else.

## Persona construction rules

Functional stance over job title; identity via implicit narrative cues (name +
short first-person backstory + one internal contradiction); demographics OFF by
default; cap ~1000 words; named-exemplar personas are INTERPRETATIONS, labeled as
such, not the real person. Every generated persona must pass the grep lint in
`persona-template.md`. The QC probe is mode-switched: stereotype-probe in
judgment mode, cliche-check in creative mode (see "Guardrails switch by mode").

## Retrieval material is not evidence

A persona's domain retrieval kit — vocabulary, named methods, good/bad research
queries — is operational scaffolding, not proof of capability. It never counts
toward the evidence gate and never substitutes for a work sample. Rich vocabulary
makes an answer sound expert without making it more correct. Vocabulary is not
proof (`evidence-gate.md`, `persona-template.md`).

## Methodology is staff-neutral

The methodology kernel (`methodologies/kernel.md`) and its overlays
(`methodologies/overlays/`) describe how work is organized; they never on their
own justify hiring a persona. Selecting an overlay does not pre-staff anyone.
Every personified role still passes `evidence-gate.md` on its own evidence, and
every kernel/overlay phase is satisfied in-house by default.

## Progressive exposure

When more than three contributors generate in parallel, or an overlay needs more
than one convergence round, or the context budget is material, or a standing team
must be resumable: stage exposure. Default sequence — isolated full outputs →
contributor summaries and explicit dissent → clustered reading of relevant full
outputs → full transcripts only when integration or audit genuinely requires it.
Record who sees what, when, and why. Context limits may trigger summarization,
narrowing, or a fresh run, but never the silent omission of a contributor.

## Durability gate

The heavy machinery — methodology kernel and overlays, `methodology-selection.md`,
the Team Charter, the `team.json` manifest, and `scripts/team_validate.py` —
applies only to the two durable outputs (reusable staffed workflow, standing
team). The lightweight outputs (in-house playbook, solo specialist, one-off panel)
run the lean lifecycle: no charter, no manifest, no team validator.

---

## SUBAGENT PROMPT PREAMBLE

Paste this block verbatim at the top of every GENERATING-LENS subagent prompt
(the critic uses the CRITIC PREAMBLE below instead):

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

## CRITIC PREAMBLE

Paste this block at the top of the critic's subagent prompt (the critic runs
AFTER the generating lenses and receives all their outputs):

```
You are the critic for this panel. Unlike the generating lenses, you SEE all
their outputs below. Rules:
1. Steelman each lens's strongest point before challenging it.
2. Attack the weakest reasoning wherever it sits, majority or minority.
3. Do not manufacture consensus; your job is to sharpen the disagreement that
   matters and kill weak arguments.
4. Never use WebFetch (curl raw pages only if you must fetch).
5. End with: the single strongest objection to the majority view, and the
   minority point most worth preserving.
```
