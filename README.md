# agent-studio

**agent-studio is a [Claude Code](https://claude.com/claude-code) skill for evidence-gated workflow design and staffing.**

It figures out how a job should be done, what can stay in-house, and whether any part of the work would genuinely benefit from a persona specialist. When a specialist is justified — by a research-matched task family, a blind work sample, or a proven track record — it runs a hiring process: a job description, a slate of named candidates, an interview, and a retained persona. Staffed workflows are then implemented and executed by a separate Do-It build engagement. A successful run may create no persona at all; "this work should stay in-house" is a first-class outcome, not a failure.

**Why gate on evidence?** Because the research is blunt: personas reliably change what a model concludes, but expert labels do not reliably improve correctness and can make it worse. So the skill refuses to infer a specialist from task complexity or the mere presence of judgment. It opens a role only when the task family is one the evidence supports, or when a blind work sample or a real track record demonstrates lift.

## Four front doors

Route by what you asked for; the skill asks if it's unclear.

| Request sounds like | Door |
|---|---|
| "I want a reliable way to accomplish X" | **1. Design the work** — full lifecycle from Stage 1 |
| "Review/improve this skill or workflow" · legacy "diagnose"/"harden" | **2. Existing workflow** — recover the assignment, treat existing personas as incumbents, re-engineer |
| "Would a specialist who does X help?" · legacy "construct" | **3. Consider a specialist** — never from a role label alone: recover the brief, then evaluate the role through the gate |
| "Get N perspectives on X" · "run an ensemble/panel" — today's answer, not a reusable workflow | **4. One-off panel** — compressed path; no Do-It, no staffed artifact |

Doors 1-3 share an eleven-stage lifecycle: understand the assignment → commission a workflow specification (Do-It engagement 1) → review the work, then the staffing → apply the persona evidence gate → write job descriptions → prototype and blind work sample where owed → interview and hire named candidates → assemble the staffed specification → build and run (Do-It engagement 2) → review actual contribution. Door 4 is the fast path for perspectives you want now.

## How you use it

Talk to it. In Claude Code, with the skill installed:

```
/agent-studio I want a reliable way to produce our weekly market report
/agent-studio would a devil's-advocate reviewer help my deploy checklist?
/agent-studio get 5 perspectives on whether we should enter this market
/agent-studio review ~/my-skills/deep-research and make it better
/agent-studio harden this panel   (with a panel.md in your project)
```

### Roster

Personas you keep are retained on a global roster at `~/.claude/agent-roster/`, one file per persona: a reusable **character core** (identity, values, voice, experience) plus a **track record** appended after each real assignment. On future jobs, a fitting persona is suggested first as a rehire — but familiarity never bypasses the gate, and a persona with a proven same-family track record is the one thing that can waive a work sample. Roster writes require your consent, and entries leave out confidential detail because the roster crosses projects.

### Two rulebooks, switched by mode

The guardrails change with the kind of work:

| | Judgment work (facts, evaluation, decisions) | Creative work (ideation, direction, options) |
|---|---|---|
| Persona bias | Contamination. Strict rules, stereotype probe. | Pigment. Strong, exaggerated lenses encouraged. |
| Opinions | Grounded in real, citable stances. | Authored for flavor. |
| Failure check | Stereotype injection. | Cliche collapse (lazy archetypes flatten into one voice). |
| Who decides | The synthesis surfaces the answer space. | **The human picks.** The skill never selects the winner. |

## Artifacts

Full-lifecycle runs (doors 1-3) land under `agent-studio-out/<slug>/`:

```
agent-studio-out/<slug>/
  brief.md                 Assignment Brief (Stage 1)
  workflow-spec.md         from Do-It engagement 1 (Stage 2)
  work-review.md           work + staffing review (Stage 3)
  evidence-cards.md        Persona Evidence Cards (Stage 4)
  jds/<role>.md            Job Descriptions (Stage 5)
  prototypes/<role>.md     functional role prototypes (Stage 6)
  work-samples/<role>/     sample-A.md, sample-B.md, verdict.md, key.md (Stage 7)
  candidates/<role>.md     slates + interview notes (Stage 8)
  personas/<name>.md       approved Persona Profiles (Stage 8)
  staffed-spec.md          staffed workflow specification (Stage 9)
  contribution-review.md   post-run review (Stage 11)
```

One-off panel runs (door 4), and analysis-only door-2 requests, keep the flat layout:

```
agent-studio-out/
  personas/<name>.md        reusable persona files (Five-Element template)
  panel.md                  the panel plan: members, size, topology, combine mode
  synthesis-prompt.md       paste-ready combine prompt for the recipe's mode
  run-<timestamp>/          <lens>.md · synthesis.md · diversity.md
  diagnosis-<slug>.md       diagnose reports (analysis-only door-2 requests)
  hardening-<slug>.md       harden reports (analysis-only door-2 requests)
```

## Install

```bash
git clone https://github.com/nraford7/agent-studio.git
cp -R agent-studio ~/.claude/skills/agent-studio     # or your skills directory
```

Then invoke with `/agent-studio`. Doors 1-3 hand build work to the Do-It skill; if Do-It is not installed, Agent Studio writes the workflow specification itself and tells you.

### Optional environment keys (it degrades gracefully without them)

- `EXA_API_KEY` enables exemplar search (finding real contrasting people). Without it, supply exemplars yourself.
- `OPENAI_API_KEY` enables semantic diversity scoring. Without it, a lexical fallback runs and labels itself degraded.

No network library is required: pages are fetched with `curl`. WebFetch is never used.

## Scripts

Two small Python helpers do the parts a model can't do reliably in-prompt:

- `scripts/exemplar_find.py find --archetype "fashion designer"` searches for exemplar leads (titles + URLs, de-duplicated) which the skill resolves into named people. `corpus` pulls a chosen person's pages as stripped text.
- `scripts/diversity.py FILE1 FILE2 [...]` computes mean pairwise semantic distance with per-pair detail, used to catch a synthesis that flattened its panel.

```bash
python3 -m pytest -q
```

## Why give agents personalities? The research

This skill exists because of a specific, evidence-backed claim: **a persona is not decoration, it is targeting** — but targeting only pays off under conditions the skill enforces. The full research corpus (three fact-checked research bibles, a distilled playbook, and an external-sources digest, about 24,000 words with full bibliographies) is in [`docs/research/`](docs/research/). The argument in brief:

**1. A personality steers where the model thinks from.** During pretraining a language model learns to simulate an enormous repertoire of characters. A well-written persona conditions the model into a different region of that space. You are not asking the model to pretend; you are choosing which of its learned characters does the reasoning.

**2. Personas change conclusions, not just tone.** Across 162 personas, 7 models, and roughly 90 million generations, the gap between the best and worst persona on the same task reached 38.56 percentage points. Personality is a substantive lever on output — which is exactly why careless personas inject bias, and why the skill gates on evidence rather than vibes.

**3. The default assistant voice quietly makes everything the same.** Generative AI raises individual output quality while shrinking collective diversity, because everyone draws from the same default character. Distinct personas are the documented countermeasure for ideation, creative direction, and strategy — where that spread is the product.

**4. A panel of personas beats one model only under conditions, and those conditions are engineerable.** Ensembles drift into consensus even with no incentive to agree, and more capable models conform more. What recovers the value: genuinely heterogeneous members, strict isolation while generating, a devil's-advocate, and a combine step that preserves disagreement. Panels pay off on judgment and creative work; on tasks with one right answer they lose to a single strong pass at higher cost.

**5. The combine step is where diversity goes to die.** Naive blending drags a diverse set of views back to their average. The evidence-backed alternative is dissent-carrying synthesis, the judicial model: a majority opinion published together with its dissents.

**6. What actually makes a persona work.** A functional stance (what it optimizes for, under what pressure) beats a job title. Identity lands through implicit cues rather than demographic labels. And personas drift over long conversations, so reused ones need re-anchoring.

**Confidence, honestly labeled.** The corpus marks every claim by evidence strength. Solid: personas change substance; single-voice homogenization; consensus collapse; blending flattens; isolation and critics help. Thinner: which construction axis drives diversity best. The evidence-gated staffing decision at the center of this skill is an evidence-grounded design bet — which is why it demands a work sample rather than assuming.

### The research corpus

| Document | What it covers |
|---|---|
| [Persona-Ensembles-Research-Bible.md](docs/research/Persona-Ensembles-Research-Bible.md) | The main question: do persona ensembles produce real reasoning diversity and better judgment? Includes the creative/subjective/taste deep-dive. |
| [Persona-Construction-Research-Bible.md](docs/research/Persona-Construction-Research-Bible.md) | How to build an effective persona; which construction axes carry the signal; the fidelity gap; failure modes. |
| [Perspective-Synthesis-Research-Bible.md](docs/research/Perspective-Synthesis-Research-Bible.md) | How to combine diverse perspectives without flattening them; mixture-of-agents evidence; the selection bottleneck. |
| [Persona-Construction-Playbook.md](docs/research/Persona-Construction-Playbook.md) | The one-page distillation the skill implements, every rule tagged by confidence. |
| [Persona-External-Sources-Digest.md](docs/research/Persona-External-Sources-Digest.md) | Reconciled external sources: Anthropic's Persona Selection Model, the persona-drift literature, practitioner frameworks. |

Each bible was produced by a retrieval-first research pipeline (evidence gate, question-driven deepening, mechanical citation verification) and then attacked by an independent adversary model whose refutations were folded back in; press-sourced and unverified claims are flagged inline.

## Provenance

The build itself is documented: design specs, implementation plans, and run ledgers live in `docs/superpowers/`. The redesign was reviewed independently (fresheyes/codex on both spec and plan) and the reconciled findings applied before execution.

Honest limits: persona QC checks structure against the template, not behavior; and the diagnose/harden reports aid judgment, nothing stronger.

## License

MIT
