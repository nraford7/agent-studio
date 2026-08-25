# Persona Construction Playbook (v2)

Seed spec for a persona-ensemble skill. Synthesized from four evidence runs (persona ensembles, creative/subjective work, construction axes, perspective synthesis) plus four ingested external sources (Anthropic Persona Selection Model, zylos + 4 arXiv papers, agenticthinking practitioner series). Confidence flags: **[solid]** multi-study, **[thin]** single-study, **[inference]** design judgment with no direct study, **[anthropic]** Anthropic alignment hypothesis, **[practitioner]** blog, unmeasured, **[via news]** press-sourced.

---

## 0. First decide whether you even need an ensemble

Use a multi-persona ensemble only when **all three** hold `[solid]`: the task is **defeasible/normative** (creative direction, strategy, opinion), not single-ground-truth; the personas are **genuinely heterogeneous**; and the combine step **resists agreement**. For checkable tasks, prefer self-consistency or voting. Personas *focus* attention, they do not *add* capability `[practitioner]`.

---

## 1. Build one persona

Use the **Five-Element template** `[practitioner, confirms our functional-stance finding]`:
- **Role** = a stance/perspective, not a job title ("senior security engineer who thinks like an attacker"). This is the best-evidenced diversity lever `[thin]` and stays demographic-free by construction.
- **Expertise** = bounded, with explicit exclusions ("not compliance, not networking").
- **Process** = numbered steps (drives consistency).
- **Output** = a literal template.
- **Constraints** = >=3 "never" statements + escalation triggers.
Cap ~1000 words. Then:
- **Identity via implicit narrative cues** (a name, a short first-person backstory, one internal contradiction), **not** explicit demographic labels, which trigger stereotypes `[solid]`.
- **Keep demographics OFF by default**; opt in only for demonstrably demographically-loaded tasks (they explain <10% of variance on most) `[solid]`.
- **Specify against the model's prior.** Some traits are near-impossible to hold because they fight pre-training; for traits with no human/fiction precedent you must supply archetype data, because steering cannot find a region that does not exist `[anthropic + practitioner]`.

**Mechanism (why this works)** `[anthropic]`: a persona is a **pre-existing region** in the base model that the prompt/history *conditions* the model toward (the "Assistant Axis" exists before fine-tuning). The same activation directions ("persona vectors") mediate both prompt-time and training-time shifts. So "front-load a vivid, specific stance" is steering a Bayesian posterior over personas, not installing text. There is **no proven ranking** of which construction axis is best `[solid on the absence]`.

---

## 2. Long-run consistency and drift (do not skip)

Personas **drift**: strong at first, softening as context accumulates, regressing to baseline as recent tokens outweigh the system prompt `[evidence]`. Mechanistically, the model wanders out of the selected region under conversational (especially emotional) pressure `[anthropic]`.

- **Measure drift on three axes:** prompt-to-line (matches spec?), line-to-line (self-contradiction?), Q&A (same answer to equivalent questions?), scored by an LLM-as-judge `[evidence]`.
- **Re-anchor, do not reset.** On a drift-score breach, inject a targeted **repair prompt** that re-states identity, rather than dumping the conversation `[practitioner]`.
- **Externalize identity into boot-loaded files**, kept on a *separate layer* from task context and per-user state, so task pressure cannot bleed into character `[practitioner]`.
- **Structure a stable core + bounded adaptation:** a fixed dominant/auxiliary identity, short-term context adaptation, long-term reflection = "stable without rigid" `[thin: 2601.10025]`. If you ever fine-tune for consistency, a multi-turn RL reward on the three drift metrics cut inconsistency >55% and held as dialogue lengthened `[evidence: 2511.00222]`.
- Do **not** train a persona to *deny* its own inner states or nature; that manufactures a "hiding/lying" character `[anthropic]`.

---

## 3. Build the ensemble (anti-conformity is first-class)

- **Vary members by stance and values**, not job titles `[inference]`. For high-stakes normative work use **different underlying models**; same-model swarms collude fast `[solid]`.
- **Generate lenses in strict isolation** (separate contexts, no cross-talk before combining) `[solid]`. ⚠️ **Warning:** the common "persona lens" pattern (swap personas within one shared context/model) is the *maximally colluding* configuration; use it only for cheap consults, never as a real diversity panel `[practitioner source has this blind spot; our evidence flags it]`.
- **Add a dedicated critic / devil's-advocate** (steelman, then challenge). A critic is worth more than an extra generator `[solid + practitioner]`.
- **Engineer explicit anti-conformity.** Ensembles collapse to consensus even with zero incentive to agree, and capable models conform *more* `[solid, key numbers via news]`.
- **Cap rounds; add a stopping rule** `[solid]`.

---

## 4. Synthesize without flattening

Naive mean-blending of quality-mixed lenses reliably flattens; **how you combine is a first-order lever** `[solid]`. Pick the combine mode deliberately (Merge-strategy selector) `[practitioner]`:
- **Concatenate** only for truly independent items.
- **Reconcile / dissent-carrying synthesis (default for your use case):** output the majority view PLUS explicitly labeled minority/dissenting views and unique findings (the judicial "majority opinion with published dissents" template) `[solid by analogy]`. Prompt: "Where do they agree? Where conflict? What is the unified recommendation, and what dissent must survive?"
- **Vote** for recoverable-answer tasks (count agreement, flag disagreement).
- **Selection** (judge picks one) is better-evidenced for recoverable-answer tasks but **cannot exceed the best single candidate**, so it is wrong when you want an emergent combined answer `[single-preprint; use with care]`.
Always: **de-duplicate by embedding before aggregating**, and use a **diversity-preserving sampler** when the output should be a *set* (creative options, scenarios) `[solid]`.

---

## 4b. Panel recipes by use case

Pick the panel shape from the task, not by habit. "Members" = the axis you vary; "size" counts generators, plus any critic. Isolation means each lens is produced in its own context with no cross-talk before the combine step.

| Use case | Vary members by | Size | Topology | Combine mode | Non-negotiable rule |
|---|---|---|---|---|---|
| Factual / has a right answer | do NOT ensemble | 1 | single strong pass | self-consistency or vote | debate wastes money here |
| Analytical judgment / decision review | functional stance | 3-5 + 1 critic | parallel, isolated | reconcile (dissent-carrying) | isolate, then add a devil's-advocate |
| Creative ideation / divergent generation | stance + method | 4-6 | parallel, strict isolation, no debate | human selector + diversity-preserving sampler | never let lenses see each other; measure output diversity |
| Creative direction / taste judgment | stance | 3-5 + 1 critic | parallel, isolated | dissent-carrying + human final judge | human owns the taste call; do not max spread |
| Strategy / positioning / options | stance + values | 4-6 | parallel isolated (optional 1 debate round) | dissent-carrying, preserve minority | ground values in real positions, not invented |
| Normative / ethics / value-laden | values | 3-5 | parallel isolated | preserve disagreement, no forced consensus | use different model families |
| Forecasting / estimation | evidence framing | 5-9 | parallel isolated | variance-aware aggregate, not naive mean | keep the private/minority signal |
| Artifact or skill review (the diagnose use) | review dimension | 3-6 + verifier | parallel isolated, then verify stage | dedup + severity-rank | verify each finding adversarially |

Two rules cut across every row: generate in isolation, and never naive-mean-blend the results (Section 4). Panel size beyond ~6 generators mostly adds cost, not coverage, except forecasting where independent samples help `[solid for the isolation/blend rules; sizes are inference]`.

## 5. Evaluate (measure, do not assume)

- **Per persona (three-tier QC** `[practitioner]`**):** Structural (required sections present) → Content (regex linter rejecting "be helpful / write clean code / ensure quality") → Behavioral (golden `expected_contains` / `expected_not_contains` / `expected_behavior` fixtures). Plus a stereotype/bias probe and a pronoun/label-swap sensitivity test `[solid]`.
- **Fidelity honestly:** benchmarking on famous named characters inflates scores via name-memorization; **anonymize names** to correct it. A model's **self-generated trait profile ≈ human-annotated** `[evidence: 2603.03915]`.
- **Per ensemble:** semantic (not lexical) diversity, measured at the **output/selection stage, not just at generation** (diversity dies at the selector); consensus concentration before vs after; unique-solve contribution; cost-adjusted quality vs a self-consistency baseline `[solid]`.
- **Population level:** individually aligned personas can form a collectively misaligned group; vet the group `[solid, via news]`.

---

## 6. For creative direction / strategy / opinion

Widen the option space with diverse structured personas; add critique to sharpen not to agree; keep a **human as final taste/value judge**; do **not** maximize spread (there is an optimum); ground value lenses in **real distributions** `[solid]`.

---

## 7. Honesty flags and experiments worth running

- **Your stance-diverse debating/synthesis ensemble has zero direct evidence** `[inference]`. First experiment: a head-to-head of construction axes (stance vs role vs values vs exemplar) on the same task, measuring output diversity, decision quality, and coverage retention through the synthesizer.
- "Stance is the best lever" rests on **one small single-model study**; the "select > blend" law on **one 0-citation preprint** scoped to recoverable-answer tasks.
- Practitioner blog claims are unmeasured; two zylos claims ("~100 turns", "Big-Five maintainability") are misattributed to their cited papers. Weight `[evidence]` and `[anthropic]` over `[practitioner]`.

Companion files on Desktop: `Persona-External-Sources-Digest.md`, `Persona-Ensembles-Research-Bible.md`, `Persona-Construction-Research-Bible.md`, `Perspective-Synthesis-Research-Bible.md`.
