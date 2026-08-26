# agent-studio

**Agent Studio is a [Claude Code](https://claude.com/claude-code) skill for designing AI workflows and building the teams that run them.**

It mirrors the way you would build a good human team. You begin by defining the assignment and the outcome you need. Agent Studio breaks that assignment into jobs, decides what your regular assistant can handle, identifies where a specialist might genuinely help, writes the job descriptions, auditions uncertain roles, introduces candidates, helps you interview them, and records the people you hire.

The result is a staffed workflow: the jobs, playbooks, specialist personas, handoffs, and operating rules needed to accomplish your goal. That workflow can be turned into a reusable skill or agent team and put to work separately. **Agent Studio builds the team and its way of working; it is not the team doing the underlying job.**

It is also not an automatic team generator. A successful run may create one specialist, several specialists, or none at all. If a regular assistant with a better brief, method, tool, or check can do the job well, Agent Studio keeps the work there.

## Why give agents personalities?

A generic assistant tries to be broadly helpful. That is useful most of the time, but it also pulls different answers toward the same safe, balanced center.

A well-built personality gives an agent a durable point of view: what it notices, what it protects, which trade-offs it makes, what it refuses to overlook, and how it approaches the work. A security reviewer who assumes the system is already compromised will inspect a design differently from a product leader protecting ease of use. A creative director obsessed with restraint will generate different options from one who values spectacle.

This is more than a change in tone. Across 162 personas, seven models, and roughly 90 million generations, the difference between the best- and worst-performing persona on the same task reached 38.56 percentage points. That makes personality a powerful steering mechanism—and a dangerous one when used carelessly.

Agent Studio therefore treats a persona like a human hire. A title, famous name, or convincing biography is not proof that someone can do the job. The role must fit the work, the evidence must support trying it, and uncertain roles must earn their place through a blind work sample.

## What personified agents do well—and badly

The research does not say that personified agents are generally better. It says they are useful for particular kinds of goals, under particular working conditions.

### Where they tend to help

| Goal | What the personality contributes | Confidence |
|---|---|---|
| **Creative divergence** | Distinct tastes, methods, and stances widen the option space and counter the generic-model tendency to make everything similar. | Best-supported use |
| **Value-laden deliberation** | Different agents can represent legitimate conflicts—growth vs safety, speed vs care, ambition vs restraint—without pretending there is one neutral answer. | Relatively favorable, conditional evidence |
| **Grounded stakeholder simulation** | A carefully grounded persona can help explore how differently situated people might respond. | Narrow support; never a substitute for speaking to real people |
| **Multi-stakeholder subjective evaluation** | A panel can cover criteria that one evaluator may miss, such as the different concerns of a customer, operator, parent, or regulator. | Promising in limited domains; a human keeps the final decision |
| **Sustained functional priorities** | A persona can keep attention on a consequential trade-off that a generic assistant tends to soften or forget. | Thin evidence; test before relying on it |
| **Creative direction, strategy, and critique** | Strong, contrasting positions can expose options, tensions, and blind spots that one balanced voice may suppress. | Useful when divergence is the goal; analytical correctness remains experimental |

Personified teams work best when their members are genuinely different, produce their views independently, and preserve meaningful disagreement in the final result. More characters alone do not create more insight.

### Where they tend to do badly

| Goal or condition | Why a persona is a poor default |
|---|---|
| **Factual, checkable, or procedural work** | A personality does not add knowledge, tool access, or reasoning capability. It can steer a correct model away from the correct answer. |
| **Forecasting** | Multiple independent evidence framings may help, but the research does not show that personifying the forecasters adds value. |
| **Generic analytical judgment** | A critic or expert persona may reveal a blind spot, but the effect is not reliable enough to assume. It should beat the regular assistant in a blind test first. |
| **Claims of professional or lived experience** | A biography can imitate the language of experience without creating the pattern recognition, credentials, accountability, or lived reality behind it. |
| **High-stakes decisions without human review** | Personas can introduce bias, stereotype groups, become overconfident, or make a subjective preference sound authoritative. |
| **Large panels and open debate** | Agents conform, repeat one another, and manufacture consensus—even when nobody asks them to agree. More capable models are not immune. |
| **Long, unanchored conversations** | Persona behavior drifts as recent context overwhelms the original character instructions. |

These failures follow from how personas work:

- **A persona steers capability; it does not create capability.** It selects a region of behavior the model already learned.
- **Labels activate associations.** “Expert,” demographic descriptions, and famous names can trigger stereotypes as easily as useful patterns.
- **Agents are correlated.** Several instances of the same model often make the same mistakes and converge on the same ideas.
- **Discussion creates conformity.** Letting agents see one another too early erodes the independent signal a panel was meant to produce.
- **Synthesis can erase the value.** A naive “combine these answers” step tends to average strong differences back into a bland consensus.
- **Characters drift.** Long-running specialists need their role, values, and boundaries re-anchored.

Agent Studio is built around those limits: evidence-gated roles, anonymous work samples, isolated generation, explicit dissent, human hiring decisions, and a performance review after real use.

The complete evidence base—three research bibles, a construction playbook, and an external-sources digest—is in [`docs/research/`](docs/research/).

## Which kind of AI worker should you use?

| Use | Best when | Typical goals |
|---|---|---|
| **A personified specialist or team** | The point of the work is a distinctive stance, taste, value, stakeholder perspective, or persistent priority—and that difference is supported by research or a work sample. | Creative directions, strategic options, value conflicts, grounded perspectives, narrowly tested critics |
| **A regular agent or workflow** | The work needs a defined role, tools, files, repeated steps, handoffs, or independent checks, but personality itself adds no demonstrated value. | Research pipelines, coding, operations, retrieval, verification, scheduled or multi-step work |
| **A generic LLM assistant** | The task is clear, bounded, low-overhead, and can be handled well in one conversation without durable roles or orchestration. | Explanation, summarization, drafting, transformation, straightforward analysis, factual or procedural help |

The simplest useful arrangement wins. Start with the generic assistant. Add a regular workflow when the work needs structure. Add personality only when a particular human-like difference is part of what makes the result better.

## Four Ways to Use Agent Studio

You do not need to choose a mode name. Describe what you want, and Agent Studio routes the request.

| What you want | How Agent Studio helps |
|---|---|
| **1. Build a workflow and team from a goal** | Start with an outcome such as “I need a reliable weekly market report.” Agent Studio defines the work, decides the staffing, and produces the staffed workflow. |
| **2. Improve an existing workflow or skill** | Bring an existing skill, process, or agent team. Agent Studio reconstructs the jobs, fixes the workflow before changing the staff, and treats existing personas as employees whose contribution must be demonstrated. |
| **3. Decide whether to hire a particular specialist** | Ask whether a devil’s advocate, creative director, stakeholder representative, or other specialist would help. Agent Studio evaluates the proposed role against the actual assignment rather than building a character from the title alone. |
| **4. Assemble a one-off panel** | Ask for several perspectives on a creative or value-laden question. Agent Studio can hire and run a small panel now, without turning it into a permanent workflow. |

The first three ways create or improve a reusable staffed workflow. The fourth is the exception: it can return a set of perspectives immediately when today’s answer—not a reusable system—is the goal.

### How durable a result you want

During routing you also choose how durable the result should be: an in-house playbook, a solo specialist, a one-off panel, a reusable staffed workflow, or a standing team. The three lighter choices run a lean process. The two durable choices add a methodology, a team charter, a manifest, and a validator, and are compiled into a reusable **team package** you can re-open later. This is a packaging choice, not a fifth way to start.

## How Agent Studio works

The process should feel familiar because it follows the same sequence as defining and filling jobs in a human organization.

### 1. Define the assignment

Agent Studio talks through what you want to accomplish, why it matters, what success looks like, what cannot change, what has already been tried, and what could make the effort fail. It turns that conversation into an Assignment Brief for you to confirm.

### 2. Map the work

The assignment is broken into the jobs, decisions, inputs, outputs, dependencies, trade-offs, failure modes, and checks required to reach the outcome. This becomes the Workflow Specification. It describes the work before making any assumptions about who—or what—should perform it.

### 3. Decide what kind of help each job needs

Every job starts with the regular assistant. Agent Studio first asks whether a clearer brief, better method, missing information, a tool, or a verification step would solve the problem. Only a remaining need for a distinctive point of view becomes a possible specialist position.

### 4. Check whether a personified specialist is justified

Each proposed position goes through the Persona Evidence Gate. Creative divergence and value-laden deliberation can proceed directly. Narrow simulations and subjective panels must be tightly scoped and tested. Experimental critics or sustained priorities must prove themselves. Factual, procedural, and forecasting jobs stay with regular agents and methods.

### 5. Write the job description

For each surviving position, Agent Studio writes a real Job Description: the job to be done, mandate, capabilities, experience expressed as observable behavior, values, working methods, authority, handoffs, limits, possible harm, and proof of value.

The Job Description belongs to the job. The Persona Profile belongs to the person hired for it. That separation means you can replace the character without losing the role, or rehire a good character into a new role without dragging the old instructions along.

### 6. Audition uncertain roles

When the research alone is not strong enough, Agent Studio builds the smallest anonymous prototype of the role and gives it the same bounded assignment as the regular assistant. The outputs are randomized and judged blind. The role opens only if it produces meaningful lift; “no improvement” and “made it worse” remain separate outcomes.

### 7. Interview and hire candidates

For every open position, Agent Studio introduces two or three contrasting named candidates. These may be interpretations of recognizable real people, historical figures, fictional characters, or an original character built precisely for the job.

For each candidate, you see what they are like to work with, why they fit, what they would contribute that the others would not, and where they may overdo it. You can interview them, reject them, request a new slate, combine qualities, or adjust someone in ordinary language—“Warren Buffett, but more interested in emerging technology and a little more tolerant of risk.” You make every hiring decision.

### 8. Assemble the team and its workflow

Agent Studio combines the in-house jobs, playbooks, approved Job Descriptions, hired Persona Profiles, activation triggers, inputs, outputs, handoffs, authority, escalation paths, and ensemble rules into a Staffed Workflow Specification.

If several specialists answer the same question, they work independently before combination and the final synthesis must preserve disagreement. If they perform sequential jobs, the workflow defines explicit handoff contracts instead.

### 9. Build and use the result separately

The staffed specification is passed to [Do-It](references/doit-handoff.md), which handles the technical implementation, tests, verification, packaging, and—when requested—the run itself. If Do-It is unavailable, Agent Studio can still produce the specification and tell you what remains to be built.

This boundary is important: **Agent Studio creates the team, the roles, and the way they work together. The resulting skill or workflow is what you use to perform the job.**

### 10. Review performance and retain the people who helped

After the workflow has run, Agent Studio reviews what each specialist contributed, what downstream work kept or rejected, what they missed, and whether they added delay, noise, bias, or harm. A role can be established, narrowed, revised, converted into a regular playbook, or retired.

With your permission, useful personas are retained for future work with an honest track record. Familiarity never bypasses the evidence gate.

## What Agent Studio produces

For a full workflow-and-team engagement, the outputs land under `agent-studio-out/<slug>/`:

```text
agent-studio-out/<slug>/
  brief.md                 assignment and success criteria
  workflow-spec.md         the jobs required to reach the goal
  work-review.md           workflow and staffing decisions
  evidence-cards.md        the evidence case for each possible specialist
  jds/<role>.md            enduring Job Descriptions
  prototypes/<role>.md     anonymous role auditions, when required
  work-samples/<role>/     blind comparisons and verdicts
  candidates/<role>.md     candidate slates and interview notes
  personas/<name>.md       the people you hired
  staffed-spec.md          the complete team workflow
  contribution-review.md   the post-run performance review
```

Together, these artifacts describe a reusable agent team and the workflow that lets it accomplish your goal. They are plans and operating assets, not the completed underlying work product.

One-off panels and analysis-only reviews use a smaller flat layout under `agent-studio-out/`.

For a durable result (a reusable staffed workflow or a standing team), Do-It compiles the staffed specification into a re-enterable **team package** at `agent-teams/<slug>/`—a manifest (`team.json`), a README, the pinned methodology, per-role bindings, and the hired personas. Building the package does not run the team; the compiled skill or team is used separately to do the underlying job.

## Roster and rehires

Personas you keep are retained at `~/.claude/agent-roster/`, one file per person. The roster stores a reusable character core—identity, values, voice, experience expressed as recognitions, and re-anchoring cues—plus a track record from real assignments.

On a future job, a fitting persona is presented first as a rehire alongside fresh candidates. A proven same-family track record can waive another audition, but it never overrides a “no specialist needed” evidence verdict. Roster writes always require your permission, and entries omit confidential or project-identifying details because the roster crosses projects.

## How to use it

With the skill installed in Claude Code, talk to it naturally:

```text
/agent-studio I want a reliable way to produce our weekly market report
/agent-studio review ~/my-skills/deep-research and rebuild the workflow
/agent-studio would a devil's-advocate reviewer help my deploy checklist?
/agent-studio get 5 perspectives on whether we should enter this market
/agent-studio audit this panel for groupthink
```

## Install

```bash
git clone https://github.com/nraford7/agent-studio.git
cp -R agent-studio ~/.claude/skills/agent-studio     # or your skills directory
```

Then invoke it with `/agent-studio`.

Agent Studio uses the Do-It skill for the two build engagements in its full lifecycle. Without Do-It, it writes the workflow specification itself and tells you which implementation step was skipped.

### Optional environment keys

Agent Studio degrades gracefully without either key:

- `EXA_API_KEY` enables exemplar search for contrasting real people. Without it, you can supply candidates or source material yourself.
- `OPENAI_API_KEY` enables semantic diversity scoring. Without it, the diversity helper uses a lexical fallback and labels the result as degraded.

No network library is required. Pages are fetched as raw text with `curl`; WebFetch is never used.

## Technical helpers

Two small Python helpers handle work that is unreliable inside a prompt:

- `scripts/exemplar_find.py find --archetype "fashion designer"` returns de-duplicated exemplar leads with titles and source URLs. Its `corpus` command pulls selected pages as stripped text.
- `scripts/diversity.py FILE1 FILE2 [...]` measures mean pairwise semantic distance and reports per-pair detail, helping detect a panel or synthesis that collapsed into one voice.

Run the repository checks with:

```bash
python3 -m pytest -q
```

## Research corpus and provenance

The full research corpus is in [`docs/research/`](docs/research/):

| Document | What it covers |
|---|---|
| [Persona-Ensembles-Research-Bible.md](docs/research/Persona-Ensembles-Research-Bible.md) | When persona ensembles produce meaningful diversity, when debate fails, and the creative and normative use cases. |
| [Persona-Construction-Research-Bible.md](docs/research/Persona-Construction-Research-Bible.md) | How personas steer behavior, which construction choices carry signal, drift, stereotype risk, and the fidelity gap. |
| [Perspective-Synthesis-Research-Bible.md](docs/research/Perspective-Synthesis-Research-Bible.md) | How aggregation flattens diverse perspectives and how to preserve minority findings. |
| [Persona-Construction-Playbook.md](docs/research/Persona-Construction-Playbook.md) | The compact, confidence-labeled rules implemented by the skill. |
| [Persona-External-Sources-Digest.md](docs/research/Persona-External-Sources-Digest.md) | Reconciled external sources on persona selection, construction, and long-run consistency. |

The research bibles were produced with a retrieval-first pipeline, citation verification, and independent adversarial review. Claims inside the corpus are labeled by evidence strength; press-sourced and unverified claims remain marked as such.

The product’s design history, implementation plans, and run ledgers live in [`docs/superpowers/`](docs/superpowers/).

Honest limits: persona quality checks verify structure, not behavior; personified stakeholder simulations do not replace real research; and diagnosis or hardening reports support human judgment rather than proving that a workflow improved.

## License

MIT
