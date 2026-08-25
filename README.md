# agent-studio

**Build AI agent personas. Assemble them into panels of genuinely different viewpoints. Combine what they say without averaging it into mush.**

agent-studio is a [Claude Code](https://claude.com/claude-code) skill for viewpoint diversity: it constructs opinionated agent personas (stances, expertise, positions, identities), runs them as isolated ensembles on a question, and synthesizes their outputs while keeping the disagreements visible. It can also analyze an existing workflow and tell you where agents would help, and where they would be a waste of money.

Every design rule in it comes from a research pass over the academic and practitioner literature on persona prompting, multi-agent ensembles, and perspective synthesis. The short version of that evidence:

- Personas change what a model concludes, not just its tone, and a single prompt style quietly homogenizes output.
- Ensembles collapse toward consensus on their own, and more capable models conform more, so anti-conformity has to be engineered in.
- Naive blending of diverse outputs flattens them back to the average; how you combine is a first-order design lever.
- Panels only pay for themselves on judgment work. On tasks with one right answer, debate loses to a single strong pass at higher cost.

## What it does

```mermaid
flowchart TD
    Q(["Your question or target"]) --> FRAME{"What kind of work?"}

    FRAME -->|"one lens needed"| CONSTRUCT
    FRAME -->|"judgment / creative work"| ENSEMBLE
    FRAME -->|"'where would agents help?'"| DIAGNOSE
    FRAME -->|"'audit my panel'"| HARDEN

    subgraph CONSTRUCT ["1 · CONSTRUCT a persona"]
        A1["Draft archetype criteria"] --> A2["Find contrasting real exemplars<br/>(Owens vs Chanel vs Miyake)"]
        A2 --> A3["Pull the chosen exemplar's corpus"]
        A3 --> A4["Write the persona:<br/>Role · Expertise · Process · Output<br/>Constraints · Positions · Identity"]
        A4 --> A5["Lint it"]
    end

    subgraph ENSEMBLE ["2 · ENSEMBLE a panel"]
        B1["Pick a panel recipe<br/>(members · size · combine mode)"] --> B2["Construct the member personas<br/>+ a devil's-advocate critic"]
        B2 --> B3["Run each lens ALONE<br/>in its own sealed context"]
        B3 --> B4["Critic sees all outputs:<br/>steelman, then challenge"]
        B4 --> B5["Synthesize in the recipe's mode:<br/>majority view + labeled dissents"]
        B5 --> B6["Measure diversity at output:<br/>did the dissent survive?"]
    end

    subgraph DIAGNOSE ["3 · DIAGNOSE a workflow"]
        C1["Map the target into stages"] --> C2{"One right answer,<br/>or a judgment call?"}
        C2 -->|"right answer"| C3["Single pass.<br/>A panel here is waste."]
        C2 -->|"judgment"| C4["Three-condition gate,<br/>then recommend a recipe"]
    end

    subgraph HARDEN ["4 · HARDEN a panel"]
        D1["Ingest the existing panel"] --> D2["Eleven-point audit:<br/>isolation? critic? dissent kept?<br/>evidence, not stated intent"]
        D2 --> D3["PASS / FAIL / N-A / UNKNOWN<br/>with severity + fix per gap"]
    end

    CONSTRUCT --> OUT1[/"personas/*.md<br/>(reusable lens files)"/]
    ENSEMBLE --> OUT2[/"panel.md · synthesis-prompt.md<br/>run-*/synthesis.md · diversity.md"/]
    DIAGNOSE --> OUT3[/"diagnosis-*.md (report only)"/]
    HARDEN --> OUT4[/"hardening-*.md (report only)"/]

    OUT3 -. "build the recommended panels" .-> ENSEMBLE
    OUT4 -. "fix the gaps" .-> ENSEMBLE
    OUT1 -. "members feed panels" .-> ENSEMBLE
```

The mental model: **construct makes the people, ensemble makes the meeting.** Personas are standalone files you can reuse solo or in any panel; a panel is just an arrangement of them. Diagnose and harden are read-only analysis modes that emit reports and never touch the target.

## How you use it

Talk to it. In Claude Code, with the skill installed:

```
/agent-studio build me a creative-direction panel for this brand concept
/agent-studio construct a persona: a fashion designer lens, ground it in a real person
/agent-studio get 5 perspectives on whether we should enter this market, and synthesize
/agent-studio diagnose ~/my-skills/deep-research: where would agents actually help?
/agent-studio harden this panel   (with a panel.md in your project)
```

A typical panel run, end to end:

1. **Frame.** It classifies your question against a recipe table (analytical judgment, creative ideation, creative direction, strategy, normative, forecasting, review) and proposes the panel shape. One confirm, then it goes.
2. **Construct.** It writes each member persona. For grounded personas it searches for deliberately contrasting real people who embody the archetype differently, and can pull their actual writing as a corpus. Named-person personas are always labeled as interpretations.
3. **Run.** Each lens answers **alone, in a sealed context**. No lens sees another before combining. That isolation is what buys real diversity; the critic runs after and is the one agent that sees everything.
4. **Synthesize.** The default output is a dissent-carrying synthesis: where the lenses agree, where they clash, what only one of them saw, and which dissent must survive into the decision. Vote, selection, and set-preserving modes exist for recipes that call for them. Nothing is ever averaged into consensus.
5. **Measure.** A diversity score runs at generation and at output. If the synthesis quietly dropped the outlier view, that shows up as a flag, not a vibe.

By default the skill **generates artifacts and stops** (personas + panel plan + a paste-ready synthesis prompt). Say "run it" and it executes the panel too.

### Two rulebooks, switched by mode

The guardrails change with the kind of work, on purpose:

| | Judgment work (facts, evaluation, decisions) | Creative work (ideation, direction, options) |
|---|---|---|
| Persona bias | Contamination. Strict rules, stereotype probe. | Pigment. Strong, exaggerated lenses encouraged. |
| Opinions | Grounded in real, citable stances. | Authored for flavor. |
| Failure check | Stereotype injection. | Cliche collapse (lazy archetypes flatten into one voice). |
| Who decides | The synthesis surfaces the answer space. | **The human picks.** The skill never selects the winner. |

## Artifacts

Everything lands in `agent-studio-out/` in your working directory:

```
agent-studio-out/
  personas/<name>.md        reusable persona files (Five-Element template)
  panel.md                  the panel plan: members, size, topology, combine mode
  synthesis-prompt.md       paste-ready combine prompt for the recipe's mode
  run-<timestamp>/          when you ask it to run:
    <lens>.md               each lens's isolated answer
    synthesis.md            the combined output, dissents labeled
    diversity.md            generation-stage and output-stage diversity
  diagnosis-<slug>.md       diagnose reports
  hardening-<slug>.md       harden reports
```

## Install

```bash
git clone https://github.com/nraford7/agent-studio.git
cp -R agent-studio ~/.claude/skills/agent-studio     # or your skills directory
```

Then invoke with `/agent-studio` or just ask to build a persona or a panel.

### Optional environment keys (it degrades gracefully without them)

- `EXA_API_KEY` enables exemplar search (finding real contrasting people). Without it, supply exemplars yourself.
- `OPENAI_API_KEY` enables semantic diversity scoring. Without it, a lexical fallback runs and labels itself degraded.

No network library is required: pages are fetched with `curl`. WebFetch is never used.

## Scripts

Two small Python helpers do the parts a model can't do reliably in-prompt:

- `scripts/exemplar_find.py find --archetype "fashion designer"` searches for exemplar leads (titles + URLs, de-duplicated) which the skill resolves into named people. `corpus` pulls a chosen person's pages as stripped text.
- `scripts/diversity.py FILE1 FILE2 [...]` computes mean pairwise semantic distance with per-pair detail, used to catch a synthesis that flattened its panel.

```bash
python3 -m pytest -q     # 12 tests
```

## Design rules the skill enforces (the short list)

1. **One isolated subagent per lens.** Never persona-swaps in one shared context; that is the maximally colluding anti-pattern.
2. **A critic beats an extra generator.** Every judgment panel gets a devil's-advocate that steelmans before it attacks.
3. **Never naive-mean-blend.** Combine in the recipe's mode; dissent-carrying is the default; de-duplicate before combining.
4. **Quality AND coverage, never one scalar.** A panel result that reports a single score is hiding its flattening.
5. **Personas are stances, not job titles.** Identity through a name, a short backstory, one contradiction. Demographics off by default. Cap ~1000 words.
6. **Reused personas drift.** Re-anchor by re-injecting the persona file; never reset the conversation.

## Provenance

The rules above are distilled from a four-part research program (persona ensembles, construction axes, creative/subjective work, perspective synthesis) plus a reconciled external-source pass (Anthropic's Persona Selection Model, persona-drift literature, practitioner frameworks), each run through retrieval, adversarial review, and a fix cycle. Design docs, specs, plans, and run ledgers live in `docs/superpowers/`.

Honest limits: the stance-diverse panel itself is an evidence-grounded design bet, not a directly measured result; persona QC is structural linting, not behavioral testing; and the diagnose/harden reports are judgment aids, not proofs. The first experiment worth running with this skill is the one the literature hasn't run: a head-to-head of construction axes on a real task, measuring output diversity and decision quality through the synthesizer.

## License

MIT
