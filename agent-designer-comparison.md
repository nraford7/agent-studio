# agent-studio vs. agent-designer — Comparative Analysis

_Compared: [`nraford7/agent-studio`](https://github.com/nraford7/agent-studio) (this repo) vs. [`dbmcco/agent-designer`](https://github.com/dbmcco/agent-designer). Analysis date: 2026-08-26._

---

## 1. Bottom line

Same DNA, different generation. **agent-designer** (dbmcco) is a lean v0.2.0 skill that *casts expert panels*. **agent-studio** (nraford7) is a much larger evolution of the same idea that *reframes the whole thing as hiring* — and, critically, is **skeptical about personas by default**.

agent-studio looks like a descendant: both repos carry the byte-identical design spec `docs/specs/2026-08-24-agent-designer-skill-design.md` (plus the calibration addendum and implementation plan), and agent-studio's own specs start one day later (`docs/superpowers/specs/2026-08-25-agent-studio-*`). This is a reconception of agent-designer, not an independent build.

**One-line take:** agent-designer answers *"how do I build a great expert panel?"*; agent-studio answers *"should I build one at all, and can I prove it worked?"*

---

## 2. The core philosophical split

This is the real difference, not the file layout:

- **agent-designer** — personas are good. Its thesis: "a persona is a retrieval key into the training distribution"; craft it well and the model lands in expert territory. The whole skill is about *making good personas*.
- **agent-studio** — personas are guilty until proven useful. Its thesis: "personas reliably change what a model concludes, but expert labels do not reliably improve correctness and can make it worse." So it *gates* every persona behind an evidence test. **A successful run can produce zero personas** — "keep it in-house" is a first-class win.

---

## 3. Side-by-side

| | agent-designer (dbmcco) | agent-studio (nraford7) |
|---|---|---|
| **Platform** | Pi skill | Claude Code skill |
| **Version/maturity** | v0.2.0, tagged, tighter | Later, larger, more iteration |
| **Governing metaphor** | Casting a panel of experts | Running a hiring process (JD → candidates → interview → review) |
| **Default stance** | Build the ensemble | Keep work in-house; justify every specialist |
| **Entry points** | 2 protocols (standing Panel / live Runtime) | 4 "front doors" (design work / fix existing / consider a specialist / one-off panel) |
| **Lifecycle** | Calibrate → cast → draft → scaffold | 11 stages incl. evidence gate, blind work sample, Do-It handoff, performance review |
| **Evidence gate** | None — completeness gate on persona *quality* | Central — task-family mapping + blind work samples that can veto a role |
| **Persona reuse** | "Promotable cast" left on disk | Global roster at `~/.claude/agent-roster/` with track records; rehires still re-gated |
| **Build/execution** | Executes runtime ensembles itself via Pi subagents | Hands staffed workflows to a separate **Do-It** engine |
| **Scripts** | Bash validators (`validate-persona.sh`) | Python (`exemplar_find.py` for real-person leads via Exa, `diversity.py` for embedding-distance checks) |
| **Repo shape** | Skill *is* the bundle; panels written into the work repo | Skill + research bibles + simmer iterations; artifacts to `agent-studio-out/` |

### What each does better

- **agent-designer** is cleaner and more focused. The "persona-as-retrieval-key" theory is elegantly stated, the two-protocol split is simple, and the whole thing is smaller and easier to reason about. Better if you *know* you want expert panels.
- **agent-studio** is far more rigorous and self-doubting. It won't spin up a persona because a task "feels expert" — it demands a matched task family, a blind work sample, or a real track record. It also closes the loop with a post-run contribution review and counterfactual check. Better when you care whether the persona actually *helped* vs. just sounded good.

---

## 4. Deep dive — where they actually diverge

### Axis 1 — Persona template: opposite theories of what a persona *is*

The single sharpest disagreement in the whole comparison.

| | agent-designer — "8 elements" | agent-studio — "5 elements" |
|---|---|---|
| **Core theory** | Persona = *retrieval key* into the training distribution. Identity richness **is the mechanism** | Persona *focuses* attention but **"does not add capability."** Stance is the mechanism; identity is risk |
| **Lead with** | Human name + institutional signature | A functional **Role/stance** sentence ("NEVER a bare job title") |
| **Word budget** | **≥300-word floor** — must be rich enough | **~1000-word cap** — must stay tight |
| **Demographics** | **Varied deliberately** across cast (names, ethnicities, career stages) — part of the key-set | **OFF by default** — "they inject stereotypes and rarely predict the answer" |
| **Required texture** | Formative experience, blind spots, communication behavior, query vocabulary | ≥3 hard "never" constraints, a fill-in Output contract, banned generic filler |
| **Failure signature** | "Reads like a job posting" / "no vocabulary of its own" | Fails a grep lint (filler regex, heading count, "never" count) |

The tell: **the same feature is a virtue in one and a liability in the other.** agent-designer *wants* the model deep in expert-text space, so it maximizes human/institutional texture and even varies ethnicity across the cast as a retrieval strength. agent-studio treats that exact texture as stereotype contamination, leads with function, and caps the word count.

Two things agent-studio adds that agent-designer has no equivalent for:

1. **Character-core vs. job-binding split** — the reusable identity is stored; the role/process/output is rewritten per hire from the JD. Exists *because* of the global roster + rehire model.
2. **Drift management** — explicit re-anchoring instructions, because personas "soften toward the default assistant" over long runs. agent-designer's personas are one-shot per round, so it doesn't address drift.

### Axis 2 — Orchestration: a deep durable canon vs. a measured combine step

| | agent-designer — kernel + overlays | agent-studio — synthesis-modes |
|---|---|---|
| **Shape** | 10-rule **versioned canon (v1.0.0), inherited whole** + phase-table overlays (scenario-planning, terrain-mapping, root-cause) | A **menu of 6 combine modes** picked per recipe (Reconcile default, Vote, Selection, Concatenate, diversity-set, variance-aware) |
| **Depth** | Multi-phase, multi-round; discovery up to **4 rounds**, progressive exposure (summaries→full transcripts) | Debate capped at **one round**; frame → run → synthesize |
| **Standing seat** | Permanent **moderator** that orchestrates, never analyzes; runs over weeks | No standing moderator; a critic seat per run, then synthesis |
| **Verification** | Model-mediated: transcript word floors, re-invoke if thin | **Quantitative:** `diversity.py` embedding distance at the *output* stage; missing dissent section = hard FAIL |
| **Provenance** | Extracted from 8 hand-built panels in `ai-simulations` (canonized practice) | Extracted from research bibles in `docs/research/` (literature-derived) |
| **Built for** | A **standing panel you re-enter and refine** | A **fast one-off**, or a staffed workflow handed to Do-It |

Where they fully agree (the shared inheritance): **independence before convergence**, **disagreement is signal** (dissent-carrying synthesis, never force consensus), and **exactly one adversarial/audit seat**. These three are near-verbatim in both — the common ancestor's spine.

Where they split: agent-designer invests in the *process of running the panel over time*. agent-studio strips that to one round and invests instead in *proving the output stayed diverse* — verified with embedding math.

### The unifying pattern

- **agent-designer trusts the persona and the process** → maximize persona texture, run a deep multi-round canon, verify by reading transcripts back.
- **agent-studio distrusts both** → minimize persona texture (stance-first, demographics off), cap debate at one round, and verify diversity/lift with scripts and gates.

agent-designer is a *craftsman's* tool for building rich standing panels. agent-studio is a *skeptic's* tool that keeps asking "does this persona/round/synthesis actually earn its place?"

---

## 5. Where they can benefit each other

Short version: they're two halves of one pipeline. agent-studio decides *whether* to build a panel and proves it worked; agent-designer is best-in-class at *building* one.

### What agent-designer gives agent-studio

1. **The overlays fill studio's biggest gap.** Studio has a fast one-off panel and a staffed-workflow-to-Do-It path — but nothing for a *standing analytical panel you re-enter over weeks*. Designer's `scenario-planning` / `terrain-mapping` / `root-cause` overlays are ready-made phase machinery for exactly that.
2. **Progressive exposure for bigger panels.** Designer's "summaries before full transcripts" is a real context-budgeting technique; studio's isolation is binary (isolated → synthesize).
3. **The 8-element craft as studio's creative-mode engine.** Once studio's gate justifies a persona, leanness stops being protective and designer's texture makes it a better retrieval key.
4. **Checkpoint / significance triage.** Designer's minor-vs-major feedback split (fold in vs. offer a re-round) is a clean human-in-loop pattern studio never formalizes.

### What agent-studio gives agent-designer

1. **The evidence gate — the big one.** Designer has *no counterpart*; it can produce a gorgeous 8-person panel for a question that needed zero personas. Studio's "in-house by default + task-family gate + blind work sample" is the exact brake designer lacks.
2. **Quantitative diversity audit.** Designer verifies transcripts *exist* and hit word floors but never measures whether seats diverged or whether synthesis flattened them. Studio's `diversity.py` + "missing dissent section = FAIL" catches duplicated seats and mean-blended synthesis that designer's model-mediated gate passes silently.
3. **Post-run contribution review + counterfactual.** Designer builds and casts, then stops. Studio's Stage 11 is the only way designer would learn whether its panels earned their cost.
4. **Named-exemplar grounding.** Studio can hire a real recognizable figure via `exemplar_find` + corpus pull, with the honest "interpretation, not the real person" label — stronger and more truthful than designer's invented names.

### Where they should NOT converge

Persona word budget (300 floor vs. 1000 cap) and demographics (varied vs. off) are genuine bets, not bugs — tied to *mode*. Studio's leanness is right for judgment work (stereotype risk); designer's richness is right for creative panels (retrieval key). Adopt each other's default **conditionally by mode**, don't overwrite.

### Why this works

They sit on opposite ends of the same risk curve. Designer optimizes **panel quality, assuming you want a panel**. Studio optimizes **whether you should have one and whether it helped**. Cleanest concrete form: **studio calls designer as its Stage-8 persona-construction engine; designer adopts studio's gate as its Step-0 and studio's diversity check as its verify step.**

---

## 6. What studio's evidence base actually says about designer's approach

Read from `docs/research/Persona-Construction-Research-Bible.md` and `docs/research/Persona-Construction-Playbook.md`.

### Verdict

Designer's **orchestration** is well-supported by studio's evidence. Designer's **persona theory** — "a persona is a retrieval key; more expert texture lands the model in expert-text territory where it continues convincingly" — is the single claim the corpus most directly disputes. The catch: it's disputed *for correctness*, not *for diversity* — and diversity is what panels are for. Designer's machine does the thing panels need; it just mislabels the mechanism.

### Where the evidence contradicts designer

1. **"Expert texture → better expert output" is the claim with the most evidence against it.** PLOS One (~90M generations, 162 personas, 7 models): role/expert personas "reliably drive variability but NOT accuracy" — a 38.56-point accuracy spread *not organized around expertise*, and "expert personas may not be the best performer."
2. **Designer leads with the weakest-evidenced axis.** Its 8 elements are name → title → CV → vocabulary (occupation/identity). The one clean causal result (Cureus clinical 2×2) isolates **functional stance** as the lever that moves reasoning. Occupation-title "acts mainly as a multiplier." Studio leads with stance *because* of this.
3. **"Continues convincingly" is a failure signature, not success.** GPT-4 emulations of real people were "too factorially pure to be real" (internal consistency 0.97–0.99 vs. 0.79–0.89 in the actual humans). Convincing ≠ faithful ≠ correct. Designer has no guard against caricature; studio's anonymize-names + over-purity check is built for it.
4. **"Vary ethnicities across the cast" is contraindicated as a default.** Demographics explain <10% of answer variance on most tasks, and explicit demographic conditioning injects stereotypes. Partial reprieve: designer varies *names*, and name-based implicit priming is the one channel Lutz 2025 blesses — the name mechanism is fine; the demographic-variety *rationale* is what the evidence flags.
5. **The stated mechanism is "disputed," not "settled."** The closest support for the retrieval-key/attractor theory is a single-author, non-peer-reviewed preprint that "sits in direct tension" with the well-replicated finding that personas drift and decay with conversation length. Studio tags this exact idea `[via news; disputed]`.

### Where the evidence *backs* designer

- **The whole kernel is right.** Independence before convergence, one adversarial seat, preserve tension, bounded rounds — studio's ensemble bible independently reaches the same `[solid]` rules.
- **Formative experience + blind spots + internal edge** map to the corpus's "narrative coherence + one internal contradiction drives deep binding" (Anthology).
- **Domain-common names** = implicit name priming, the low-stereotype channel the evidence prefers over explicit labels.

### The honest bottom line

The corpus does **not** prove designer wrong — it proves designer **unvalidated on its own success claim**. That texture reliably buys *diversity* (which panels want) and does *not* reliably buy *accuracy* (which designer implies). Two corrections studio's evidence would make, neither touching orchestration:

1. **Re-order the template: stance first, occupation second.** Keep all 8 elements, but make "what this seat optimizes under what pressure" the head, not name/title/CV.
2. **Swap the success test.** Replace "reads convincingly like a real expert" (an over-coherence / caricature signal) with a diversity/dissent measure at the *output* stage.

The deep irony: designer built an excellent diversity engine and described it as a correctness engine. Studio read the same literature, concluded the same machine is a diversity engine, and gated it accordingly.

---

## Key sources cited

- Helpful assistant or fruitful facilitator? (PLOS One) — role drives variability not accuracy — https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0325664
- Decomposing Persona Prompts for Simulated Clinical Reasoning (Cureus 2026) — stance 2×2 — https://pmc.ncbi.nlm.nih.gov/articles/PMC13107492/
- The Prompt Makes the Person(a) (EMNLP Findings 2025) — implicit name priming beats explicit labels — https://aclanthology.org/2025.findings-emnlp.1261
- Binding LLMs to Virtual Personas / Anthology (EMNLP 2024) — narrative backstory binding — https://doi.org/10.18653/v1/2024.emnlp-main.1110
- Evaluating the ability of LLMs to emulate personality (Scientific Reports) — over-coherence / caricature — https://www.nature.com/articles/s41598-024-84109-5
- Stick to your role! (PLOS One) — persona drift decays with conversation length — https://doi.org/10.1371/journal.pone.0309114
