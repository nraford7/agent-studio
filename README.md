# agent-studio

A Claude Code skill that constructs AI agent personas and assembles or runs panels
(ensembles) of them for viewpoint-diverse analysis, then synthesizes their outputs
without flattening the diversity. It operationalizes an evidence base on persona
construction and multi-agent synthesis (see Provenance).

## Two uses

- **Construct** — build one well-formed persona from the Five-Element template, with
  an optional archetype -> contrasting-named-exemplars -> corpus grounding flow.
- **Ensemble** — assemble a panel from the use-case recipe table and, on request,
  run it: isolated lenses -> critic -> dissent-carrying synthesis -> diversity check.

## The six-stage flow

1. **Frame** — classify the task, map it to a panel recipe, confirm the shape.
2. **Construct** — archetype criteria -> optional contrasting named exemplars -> optional corpus -> persona in the Five-Element template.
3. **Assemble** — set members / size / topology / combine mode; add a critic; write `panel.md` + `synthesis-prompt.md`.
4. **Run** (optional) — one isolated subagent per lens, then the critic.
5. **Synthesize** — de-duplicate, then dissent-carrying synthesis (never naive-mean-blend).
6. **Emit + evaluate** — diversity at generation AND output stage; co-report quality + coverage.

Runtime artifacts are written to `agent-studio-out/` in your current directory.

## Scripts

- `scripts/exemplar_find.py`
  - `find --archetype "fashion designer" [--n 3]` — surfaces contrasting named
    exemplars as JSON lines `{name, contrast, url}`. Needs `EXA_API_KEY` (exits 20
    with a clear message without it).
  - `corpus --name "Rick Owens" --url <u> [--url <u> ...] --out <dir>` — curls raw
    pages and writes stripped text per page (exit 21 if none fetched).
- `scripts/diversity.py FILE1 FILE2 [...]` — mean pairwise semantic distance across
  text files. Uses OpenAI embeddings if `OPENAI_API_KEY` is set, otherwise a lexical
  TF-IDF fallback (labeled "degraded (lexical)"). Never hard-fails.

## Environment (all optional; the skill degrades gracefully)

- `EXA_API_KEY` — enables exemplar search (`find`). Without it, supply exemplars manually.
- `OPENAI_API_KEY` — enables semantic diversity. Without it, diversity is lexical.

No network library is required: web access uses `curl`. **WebFetch is never used.**

## Install / deploy

This repo is NOT auto-deployed. To make the skill available in Claude Code, copy or
symlink it into your skills directory:

```bash
# copy
cp -R ~/Projects/agent-studio ~/.claude/skills/agent-studio

# or symlink (keeps it in sync with this repo)
ln -s ~/Projects/agent-studio ~/.claude/skills/agent-studio
```

Then invoke it with `/agent-studio` or by asking to construct a persona or build a panel.

## Tests

```bash
python3 -m pytest -q
```

## Provenance

- Spec: `docs/superpowers/specs/2026-08-25-agent-studio-design.md`
- Requirements source: the Persona Construction Playbook (v2) and its companion
  research bibles + external-sources digest.

## Scope

This version implements **construct** and **ensemble**. Two further uses —
**diagnose** (point the skill at another skill and recommend where agents help) and
**harden** (audit an existing ensemble for consensus-collapse) — are deferred.
