# agent-studio — Design Spec

Date: 2026-08-25
Status: draft for review

## Problem statement

Building good AI agent personas, and assembling them into panels that produce
genuine viewpoint diversity, is currently ad hoc. The evidence base (four
research runs + four ingested external sources, distilled in
`~/Desktop/Persona-Construction-Playbook.md` v2) shows that naive approaches
fail in predictable ways: generic role labels collapse to one voice, same-context
"persona lens" panels maximally collude, and naive mean-blending of diverse
outputs flattens them back toward the mean. `agent-studio` is a Claude Code skill
that operationalizes the Playbook so a user can, on demand, construct a
well-formed persona or build (and optionally run) an evidence-grounded panel.

## Scope

IN scope (this cycle):
- **CONSTRUCT** — build one persona using the Five-Element template, with an
  optional archetype -> contrasting-named-exemplars -> corpus grounding flow.
- **ENSEMBLE** — build a panel from the use-case recipe table, and optionally
  RUN it (isolated lenses -> critic -> dissent-carrying synthesis -> evaluation).

OUT of scope (later cycle, explicitly deferred):
- DIAGNOSE (point the skill at another skill/workflow and recommend where agents help)
- HARDEN (audit an existing ensemble for consensus-collapse)
- Any fine-tuning / training-time consistency work (referenced, not built)

## Success criteria (measurable)

1. `SKILL.md` exists at repo root, is a valid Claude Code skill (YAML frontmatter
   with `name: agent-studio` and a trigger `description` that fires on "construct a
   persona / agent", "build a panel / council of agents", "run an ensemble / panel",
   and `/agent-studio`), and orchestrates the six-stage flow below.
2. A construct request writes a persona to `agent-studio-out/personas/<name>.md`
   that PASSES the grep lint: the five headings `## Role / ## Expertise / ## Process
   / ## Output / ## Constraints` are present, Constraints has >=3 "never" lines, an
   implicit-identity block is present, and the banned-phrase regex finds no matches;
   capped ~1000 words; no demographic labels unless the task justified them.
3. An ensemble request writes `agent-studio-out/panel.md` (members, size, topology,
   combine mode, recipe row used) and `agent-studio-out/synthesis-prompt.md`.
4. When asked to run, the skill produces `agent-studio-out/run-<timestamp>/`
   containing one output file per lens (each produced in an isolated subagent) plus
   a `synthesis.md` (dissent-carrying by default) and a `diversity.md` note that
   reports generation-stage AND output-stage diversity.
5. `scripts/exemplar_find.py` runs, takes an archetype string, and returns
   candidate contrasting named exemplars with source URLs, using curl (never
   WebFetch); exits non-zero with a clear message when no retrieval key is set.
6. `scripts/diversity.py` runs, takes >=2 text files, and prints a semantic
   diversity score plus a per-pair distance summary.
7. Every subagent prompt the skill emits contains the NO-WebFetch rule and the
   isolation rule.
8. A `README.md` documents install/deploy (copy or symlink into `~/.claude/skills/`),
   and the skill does NOT auto-deploy.

## Proposed approach (Approach A: staged pipeline, separable stages)

`SKILL.md` is the orchestrator. It defines six stages, each written so it can
later be factored into a standalone command without rework:

1. **Frame** — read the request; classify the task type; map to a panel recipe
   (or single persona). Present the proposed shape via `AskUserQuestion` for one
   confirm; skip the ask if the request already fully specifies it, or in a
   non-interactive run.
2. **Construct** — generate persona(s). Sub-flow:
   a. Draft archetype criteria (what defines this lens).
   b. (optional) Call `exemplar_find.py find` to surface ~3 deliberately
      CONTRASTING real named exemplars of the archetype, each with a one-line
      contrast and a source URL; user picks.
   c. Pull the chosen exemplar's corpus (`exemplar_find.py corpus`, curl raw
      pages) and distill characteristic moves / voice / references into the
      persona. Label the persona an interpretation, not the real person.
      **Corpus grounding is REQUIRED (not optional) when the archetype has no
      common human/fiction precedent** (specify-against-the-prior rule, Playbook
      §1): steering cannot find a latent region that does not exist, so such a
      persona must be given exemplar/archetype material. It stays optional when a
      strong precedent exists.
   d. Emit the persona in the Five-Element template + implicit identity cues.
3. **Assemble** — from the recipe row: set members axis, size, topology, combine
   mode; add a critic (devil's-advocate) unless the recipe says otherwise; offer
   different-model-family members for high-stakes normative panels. Write `panel.md`.
4. **Run** (only when the user asks) — dispatch each lens as an ISOLATED subagent
   (fresh context, no cross-talk before combining), then the critic. Each lens
   prompt carries the persona, the question, and the hard rules.
5. **Synthesize** — de-duplicate lens outputs by embedding first, then combine via
   the recipe's mode (default: reconcile / dissent-carrying — majority view PLUS
   explicitly labeled minority and unique findings). Never naive-mean-blend.
6. **Emit + evaluate** — write artifacts; run `diversity.py` on the lens outputs
   (generation stage) AND on the post-synthesis result set (output stage), and
   report the before-vs-after diversity so a large drop without a quality gain
   flags flattening at the selector (Playbook §5: "diversity dies at the
   selector"). Co-report a quality note AND a coverage note, never one scalar.

Stage hand-off is FILE-BASED so stages can later be factored into standalone
commands without rework: Frame/Assemble write `panel.md`; Construct writes
`personas/<name>.md`; Synthesize reads those plus the run outputs. A later
standalone command reads the same files rather than relying on shared context.

### Panel recipe table (encoded in references/recipes.md, summarized here)

| Use case | Vary by | Size | Topology | Combine | Hard rule |
|---|---|---|---|---|---|
| Factual / right answer | do NOT ensemble | 1 | single pass | self-consistency/vote | debate wastes money |
| Analytical judgment | stance | 3-5 + critic | parallel isolated | reconcile | isolate + devil's-advocate |
| Creative ideation | stance + method | 4-6 | parallel strict isolation, no debate | human selector + diversity-preserving | never let lenses see each other |
| Creative direction / taste | stance | 3-5 + critic | parallel isolated | dissent-carrying + human judge | human owns taste; don't max spread |
| Strategy / positioning | stance + values | 4-6 | parallel isolated (opt 1 debate round) | dissent-carrying, preserve minority | ground values in real positions |
| Normative / ethics | values | 3-5 | parallel isolated | preserve disagreement | different model families |
| Forecasting / estimation | evidence framing | 5-9 | parallel isolated | variance-aware aggregate | keep minority signal |

(The Playbook's 8th row, "Artifact/skill review", is deliberately omitted: it
maps to the deferred DIAGNOSE use, out of scope this cycle.)

### Files

```
agent-studio/
  SKILL.md                 # orchestrator: the six stages + hard rules
  README.md                # what it is, install/deploy, usage
  scripts/
    exemplar_find.py       # archetype -> contrasting named exemplars (+ corpus pull); curl only
    diversity.py           # semantic diversity over lens outputs
  references/
    persona-template.md    # the Five-Element template + implicit-cue guidance + example
    recipes.md             # the full use-case -> panel recipe table
    synthesis-modes.md     # reconcile / concatenate / vote / select + the dissent-carrying prompt
    hard-rules.md          # isolation, no-naive-blend, no-WebFetch, quality+coverage
```

Runtime artifacts (written into the USER's cwd under `agent-studio-out/` — named
distinctly from the skill repo dir `agent-studio/` to avoid collision if the user
runs from inside the repo):
```
agent-studio-out/personas/<name>.md
agent-studio-out/panel.md
agent-studio-out/synthesis-prompt.md
agent-studio-out/run-<timestamp>/{<lens>.md, synthesis.md, diversity.md}
```

### Scripts (kept minimal — exactly two)

- `exemplar_find.py` has TWO explicit subcommands (one script, dispatched by
  first arg; they are mutually exclusive):
  - `exemplar_find.py find --archetype "fashion designer" [--n 3] [--max-usd 0.5]`
    — Exa search via `EXA_API_KEY` + curl; prints candidate exemplars as JSON
    lines `{name, contrast, url}`. Exit 20 if `EXA_API_KEY` unset (clear message);
    exit 0 with an empty list if search returns nothing.
  - `exemplar_find.py corpus --name "Rick Owens" --url <u> [--url <u> ...] --out <dir>`
    — curls each raw page, strips HTML to text, writes `<dir>/<slug>.txt`. Exit 0
    on any page fetched (per-page fail-open); exit 21 if zero pages fetched.
  NO WebFetch anywhere in either subcommand (curl only).
- `diversity.py <file1> <file2> ...`: embeds each text (OpenAI embeddings if
  `OPENAI_API_KEY`, else a local TF-IDF fallback so it NEVER hard-fails — the
  fallback path is labeled "degraded (lexical)" in output because it is not the
  semantic measure). Prints mean pairwise cosine distance (the diversity score) +
  the most-redundant pair. Run at BOTH the generation stage (lens outputs) and the
  output stage (post-synthesis set) to catch selector-stage flattening.

Persona QC is a grep-based lint the SKILL runs inline (NOT a third script): a
banned-phrase regex rejecting "be helpful / write clean code / ensure quality /
be thorough / and so on", plus a structural check that the five element headings
are present. Documented in `references/persona-template.md`; keeps the script
count at two per the build constraint.

### Hard rules the skill enforces (references/hard-rules.md, injected into prompts)

- Generate lenses in strict isolation (separate subagents, no cross-talk before combine).
- **Never run lenses as persona-swaps within one shared context/model** — that is
  the maximally-colluding anti-pattern (Playbook §3); one isolated subagent per lens.
- **Anti-conformity is first-class:** every lens prompt carries an explicit
  instruction to reason from its own stance and NOT anticipate or accommodate other
  views; any optional debate round is capped (max 1 round for the Strategy recipe)
  with a stopping rule (stop when a round adds no new labeled dissent).
- Never naive-mean-blend; use the recipe's combine mode (default dissent-carrying).
- NO WebFetch anywhere — curl raw pages only. Carried into every emitted subagent prompt.
- Always co-report a quality note AND a coverage/diversity note, never one scalar.
- Persona construction: functional stance over job title; implicit identity cues;
  demographics off by default; cap ~1000 words; named-exemplar personas are
  interpretations, labeled as such. Persona files must pass the grep lint
  (banned-phrase regex + five element headings present).

### references/persona-template.md must encode (so criterion 2 is verifiable)

- The five element headings verbatim: `## Role`, `## Expertise`, `## Process`,
  `## Output`, `## Constraints`.
- Role = a functional stance sentence, never a bare job title.
- Expertise = a bounded list WITH an explicit "Not:" exclusions line.
- Process = numbered steps.
- Output = a literal fenced template block.
- Constraints = at least three "never ..." lines + an escalation trigger line.
- An implicit-identity block: a name, a 2-3 sentence first-person backstory, one
  stated internal contradiction. No demographic labels by default.
- One fully worked example persona.

## Alternatives considered

- **B: library of primitives + thin orchestrator.** More flexible/composable and
  better for the later diagnose/harden uses, but heavier upfront and slower to a
  first working panel. Rejected for v1; A's stages are separable so B can be
  factored out later without rework.
- **C: prompt-only skill, no scripts.** Lightest, but grounding (exemplar
  retrieval, corpus) and diversity measurement are much weaker without scripts.
  Rejected: the two scripts are the parts the model cannot do reliably in-prompt.

## Blast radius / rollback

- Self-contained new repo at `~/Projects/agent-studio`. Touches nothing else.
- Does NOT deploy into `~/.claude/skills/` (user does that manually per README),
  so it cannot affect the live skill set until the user opts in.
- Rollback = delete the repo dir; nothing else references it.

## Open questions

- None blocking. Model/provider for lens subagents defaults to the Claude Code
  session's Agent tool; different-model-family members are offered but not
  required for v1 (a note in panel.md when unavailable).
