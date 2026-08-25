---
name: agent-studio
description: Construct AI agent personas, assemble or run panels (ensembles) of them for viewpoint-diverse analysis, and analyze existing workflows or panels. Use when the user wants to design an agent persona, build a persona/lens, create a panel or council of agents, run an ensemble of perspectives on a question, get multiple analytical or creative lenses on a topic and synthesize them, find out where agents would help in an existing skill or workflow, or audit an ensemble. Triggers on "/agent-studio", "construct/design a persona or agent", "build a panel/council of agents", "run an ensemble", "get N perspectives on X", "diagnose this skill/workflow", "where would agents help in X", "audit/harden this panel/ensemble".
---

# agent-studio

Turn a question into a well-formed persona, or into a panel of diverse lenses that
run in isolation and are synthesized without flattening. Four uses: **construct**
one persona, **ensemble** (build, and optionally run, a panel), **diagnose**
(analyze an existing skill/workflow for where agents help vs waste), and **harden**
(audit an existing panel for the known failure modes). Diagnose and harden are
recommend-only analysis modes. This skill operationalizes the evidence in
`references/` — read the referenced file at each stage; do not improvise around
the hard rules.

Diagnose and harden requests SKIP the six stages entirely: go directly to their
Mode sections below (no Frame confirm, no panel shape).

Artifacts are written to `agent-studio-out/` in the user's current directory (never
this repo). Stages hand off through files (`panel.md`, `personas/*.md`), so each
stage can be run on its own.

## Hard rules (always)

Read and obey `references/hard-rules.md`. The essentials:

- Generate lenses in **strict isolation** — one subagent per lens, fresh context, no
  cross-talk before combining. **Never** run a panel as persona-swaps in one shared
  context (the maximally-colluding anti-pattern).
- **Anti-conformity is first-class:** every lens prompt uses the SUBAGENT PROMPT
  PREAMBLE from `references/hard-rules.md`; cap any debate at one round with a
  stopping rule.
- **Never naive-mean-blend.** De-duplicate by embedding, then combine via the
  recipe's mode (default: dissent-carrying). See `references/synthesis-modes.md`.
- **NO WebFetch anywhere** — `curl` raw pages only; carry this into every subagent
  prompt you emit.
- Always co-report a **quality note AND a coverage/diversity note**, never one scalar.
- **Guardrails switch by mode:** strict rulebook for judgment work, flavor-forward
  for creative work (see `references/hard-rules.md#Guardrails switch by mode`).

## The six stages

### 1. Frame
Read the request and classify the task type. Map it to a row in
`references/recipes.md` (or a single persona if that is all that was asked). Present
the proposed shape (persona, or panel: members / size / topology / combine mode) with
one `AskUserQuestion` for confirmation. Skip the ask if the request already fully
specifies the shape, or if the run is non-interactive.

### 2. Construct
Build the persona(s), using `references/persona-template.md`:
1. Draft the archetype criteria — what defines this lens.
2. (optional) `python3 <skill-dir>/scripts/exemplar_find.py find --archetype "<archetype>"` to
   surface exemplar LEADS (page titles + URLs). Resolve the leads into ~3
   deliberately CONTRASTING real named people (a listicle title is a lead to
   mine, not a person). Present the named people; the user picks.
3. Ground from a chosen exemplar's corpus:
   `python3 <skill-dir>/scripts/exemplar_find.py corpus --name "<name>" --url <u> [--url <u>] --out <dir>`,
   then distill characteristic moves / voice / references into the persona. Corpus
   grounding is **required (not optional)** when the archetype has no common
   human/fiction precedent (steering cannot find a region that does not exist);
   optional when a strong precedent exists. Label a named-exemplar persona an
   interpretation, not the real person.
4. Emit the persona in the Five-Element template + implicit identity cues, then run
   the grep lint from `references/persona-template.md`. Fix any lint failure before
   saving to `agent-studio-out/personas/<name>.md`.

### 3. Assemble
From the chosen recipe row: set the members axis, size, topology, and combine mode;
add a critic (devil's-advocate) unless the recipe says otherwise; for high-stakes
normative panels, offer different-model-family members (note in `panel.md` if
unavailable). Write `agent-studio-out/panel.md` (members, size, topology, combine
mode, recipe row) AND `agent-studio-out/synthesis-prompt.md` carrying the
paste-ready prompt FOR THE RECIPE'S COMBINE MODE from
`references/synthesis-modes.md` (dissent-carrying only when the recipe says so).
Verify members differ in POSITIONS/conclusions, not just tone; for
strategy/normative/value-laden recipes and opinionated creative lenses, each
persona carries a Positions block per the template. Generate-by-default stops
here and hands the user these artifacts.

### 4. Run (only when asked)
Dispatch one **isolated subagent per lens**, each prompt opening with the SUBAGENT
PROMPT PREAMBLE from `references/hard-rules.md`, then the persona and the question.
THEN dispatch the critic: the critic is NOT isolated from the outputs — the critic receives all lens outputs and uses the CRITIC PREAMBLE from
`references/hard-rules.md` (isolation applies to the generating lenses only).
Write each lens output and the critic's output to
`agent-studio-out/run-<timestamp>/<lens>.md`.

### 5. Synthesize
De-duplicate lens outputs by embedding first, then combine per the recipe's mode
(default: reconcile / dissent-carrying — majority view PLUS explicitly labeled
minority and unique findings). Never naive-mean-blend. Write
`agent-studio-out/run-<timestamp>/synthesis.md`.

### 6. Emit + evaluate
Run `python3 <skill-dir>/scripts/diversity.py` over the lens outputs (generation
stage). Then measure the OUTPUT stage, two cases:
- SET outputs (creative options, scenarios): run diversity.py across the set; a
  large drop from generation-stage diversity with no quality gain flags
  flattening.
- SINGLE synthesis.md from a DISSENT-CARRYING recipe: run diversity.py over
  [all lens outputs + synthesis.md] and read the synthesis-vs-lens per-pair
  distances (the `pairs` array; the outlier lens = the one farthest from the
  others in the generation-stage pairs). Flattening = the synthesis is markedly
  FARTHER from that outlier lens than from the majority cluster (the dissent was
  dropped); roughly equidistant = dissent carried. ALSO grep synthesis.md for
  the labeled "Minority" / dissent sections — absence = FAIL. These two checks
  apply ONLY to dissent-carrying recipes; a Vote or Selection output legitimately
  has no minority section and tracks its winning lens.
Write `agent-studio-out/run-<timestamp>/diversity.md` reporting both stages.
Report back a quality note AND the coverage/diversity note — never one scalar.

## Mode: Diagnose (recommend-only)

Point the skill at an existing workflow and report where a persona/panel would help
and where it would be waste. Follow `references/diagnose-rubric.md` exactly.

1. **Ingest.** Path with a SKILL.md: read it plus `scripts/` and `references/` to
   recover the pipeline. Path without one: read the entry document (README or main
   script). Nothing readable: ask the user for a prose description. Prose given:
   parse the described steps. Produce an ordered stage list.
2. **Classify** each stage mechanical vs judgment-laden per the rubric.
3. **Map** judgment stages to a `references/recipes.md` row; mark mechanical stages
   "single pass — do NOT ensemble" with the reason.
4. **Check existing multi-agent use** (isolation, critic, model family, combine mode).
5. **Emit** `agent-studio-out/diagnosis-<slug>.md` per the rubric's report template
   (slug = target dir name, or first 3-4 words of prose, kebab-case).

Recommend-only: generate no persona files, modify nothing in the target, dispatch
no subagents. End the report with the build pointer.

## Mode: Harden (recommend-only)

Audit an existing panel/ensemble against `references/harden-checklist.md`.

1. **Ingest.** Prefer `agent-studio-out/panel.md` if present; else grep the target's
   files for agent-dispatch patterns (Agent tool calls, subagent prompts,
   "dispatch", "panel", "ensemble") and audit those sites; else ask for a prose
   description of the panel.
2. **Run the eleven checks**, scoring each PASS / FAIL / N-A / UNKNOWN with the
   checklist's default severity, an Evidence citation per verdict, and a one-line
   fix per FAIL (declared intent is not evidence — see the checklist).
3. **Emit** `agent-studio-out/hardening-<slug>.md` per the checklist's report
   template, leading with the verdict line (count + names of HIGH gaps).

Recommend-only: report, never rewrite. End with the build pointer.

## Scripts

Locating the scripts: they live in THIS skill's directory, not the user's cwd.
Resolve `<skill-dir>` = the base directory containing this SKILL.md (reported
when the skill loads) and invoke `python3 <skill-dir>/scripts/...`.

- `exemplar_find.py find|corpus` — archetype -> exemplar LEADS (titles + URLs the
  model layer resolves into named people), and corpus pull (pages via curl).
  Needs `EXA_API_KEY` for `find` (exits 20 without it).
- `diversity.py FILE...` — mean pairwise semantic distance (OpenAI embeddings if
  `OPENAI_API_KEY`, else a lexical fallback). Never fails for a missing API key;
  exit 2 only on unusable inputs.
