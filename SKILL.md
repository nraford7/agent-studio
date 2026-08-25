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

### 1. Frame (a dialogue, not a classifier)

This stage is a conversation about what help the user actually needs. Do NOT jump
to panel geometry. Two beats:

**Beat 1: Goal diagnosis.** Restate, in one short paragraph, what the user is
trying to achieve and what success would look like. Classify the KIND of help
needed: fact-finding, judgment/decision support, creative divergence, evaluation,
or strategy. If the goal is genuinely underspecified (no way to know what a good
answer looks like), ask 1-2 clarifying questions FIRST, via `AskUserQuestion`.
Do not ask about things the request already answers.

**Beat 2: Direction proposal.** Propose the kind of mind(s) that would help and
WHY, before any construction: for a single persona, a one-line sketch of the
suggested personality/stance/skills; for a panel, a one-line sketch PER MEMBER
(e.g. "a cost-obsessed operator; a brand-purist contrarian; a
customer-anthropologist; plus a critic") tied to the goal from Beat 1, along
with the recipe row and shape (members axis, size, topology, combine mode) from
`references/recipes.md`. Present it with one `AskUserQuestion`: approve, swap or
adjust members/stances, or change the shape. Iterate if the user pushes back;
this discussion IS the product of the stage.

Skip the asks only when the request already fully specifies both the goal and
the shape, or when the run is non-interactive. Only after the direction is
agreed does the flow move to Construct.

### 2. Construct (a hiring process)
Personas are HIRED, not configured. The user is the hiring manager; the skill
runs the search. For each seat in the agreed direction:

1. **Write the job description.** Role title, mandate (what the seat optimizes
   for and under what pressure), required skills, hard prohibitions. This is
   the archetype criteria; it is recorded in `panel.md` beside the hire.
2. **Check the retainer roster first.** `~/.claude/agent-roster/` holds
   characters the user has kept on retainer from past hires. If one fits the
   job description, present them first ("X is on retainer and fits — rehire,
   or see new candidates?").
3. **Present a slate of candidates.** 2-3 deliberately CONTRASTING candidates
   who each genuinely fulfill the job description, drawn from real famous
   people, historical figures, or well-known fictional characters (literature,
   film, TV, comics). The recognizable package IS the point: a known name
   carries values, style, and stances the user can identify with at a glance.
   Each candidate: name · why they fit the job description · what their package
   brings · one risk of hiring them.
   `python3 <skill-dir>/scripts/exemplar_find.py find --archetype "<archetype>"`
   surfaces LEADS when useful (a listicle title is a lead to mine, not a
   person). In judgment mode prefer candidates with documented, citable
   stances. Every hire is an INTERPRETATION of the public figure or character,
   never the real person; the persona file opens with that label.
4. **The interview.** One `AskUserQuestion` per seat: hire candidate A/B/C, or
   direct an adjustment ("Rick Owens but less intense", "more like Coco
   Chanel"). On an adjustment: rebuild the character with the change blended
   in, present them back, re-offer the hire. Iterate until the seat is filled;
   the user may also reject the whole slate and ask for fresh candidates.
5. **Onboard the hire.** Ground from the exemplar's corpus when public work
   exists and stakes are high:
   `python3 <skill-dir>/scripts/exemplar_find.py corpus --name "<name>" --url <u> [--url <u>] --out <dir>`.
   Corpus grounding is **required (not optional)** when the archetype has no
   common human/fiction precedent (steering cannot find a region that does not
   exist). Emit the persona in the Five-Element template, in the hire's name
   and voice, run the grep lint from `references/persona-template.md`, fix any
   failure, save to `agent-studio-out/personas/<name>.md`.
6. **Consultants and the retainer.** A specialist needed mid-run that no seat
   covers is a **temp hire / consultant**: same flow, compressed (one strong
   candidate + accept/adjust). After any hire the user likes, offer to keep
   them **on retainer**: copy the persona to `~/.claude/agent-roster/<name>.md`
   for reuse across projects and skills.

**Hires play their part.** Dispatched agents speak in their character's name
and voice and are referred to by name in every report. Theatre never loosens
rigor: the Output format, isolation rules, preambles, and lint stay binding
regardless of who was hired.

**Performance review (end of every run that dispatched hires).** When a run's
results are presented, include a short review per hire: what they contributed
(findings kept, findings refuted, the dissent they defended), and what they
missed. Zero kept findings is reported plainly — it may mean the seat, not the
character, is wrong for this kind of topic; say which. For each temp
hire/consultant, END the review with one question: keep them on the roster
(`~/.claude/agent-roster/<name>.md`) or let them go. A roster persona carries a
`## Track record` section appended after each run (topic, findings kept, one
line on performance); future hiring slates read it.

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
persona carries a Positions block per the template.

**Cast card (skippable).** After `panel.md` is written, show the user the team
they hired, one screen: one line per member — name · role · what they hunt or
argue for · one signature "never". Then ONE `AskUserQuestion`: "Want to meet
your team before they start?" with options: **Keep the team (Recommended)**;
**Meet them** (show each full persona file, then re-offer); **Renegotiate a
hire** (an adjustment in the user's words — "less intense", "more Coco
Chanel" — rebuild, re-lint, re-present); **Open a new seat** (job description +
candidate slate + hire per Construct; offer the retainer afterwards). Iterate
until approved. Skip silently when the run is non-interactive, the user gave a
skip signal, or this cast was already confirmed this session. Skills BUILT by
this skill should carry the same cast-card stage before their own dispatch.

Generate-by-default stops here and hands the user these artifacts.

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
