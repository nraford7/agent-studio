# External Sources Digest: Persona Design

Ingested 2026-08-25 at your request, reconciled against the four research Bibles. Confidence tiers: **[evidence]** peer-reviewed/arXiv, **[anthropic]** Anthropic alignment research essay (hypothesis, high-credibility), **[practitioner]** single-author blog, no measurement.

Sources read in full (via curl, raw text):
1. **agenticthinking.ai** "Building with AI Assistants" 13-part series (all 13; persona cluster read deeply) `[practitioner]`
2. **zylos.ai** persona-design / behavioral-consistency research piece `[practitioner, well-cited]`
3. **alignment.anthropic.com/2026/psm** "The Persona Selection Model" (Marks, Lindsey, Olah, Feb 2026) `[anthropic]`
4. arXiv papers zylos cites: **2511.00222** (Abdulhai, NeurIPS 2025), **2601.10025**, **2603.03915**, **2603.03140** `[evidence]`

---

## The one genuinely new dimension: long-run consistency and drift

Our four runs under-covered this. It is the biggest add.

- **Drift is real and mechanistic.** Personas hold strong initially, soften as context accumulates, then regress to baseline: recent tokens outweigh the system-prompt anchor. `[evidence 2511.00222]` PSM reframes drift as the model *wandering out of the selected latent region* under conversational (especially emotional) pressure. `[anthropic]`
  - ⚠️ zylos's "~100 turns" threshold is a gloss NOT stated in the cited paper. Treat as illustrative.
- **A training-time fix exists.** Treat consistency as a *trajectory* property; score three drift metrics (prompt-to-line, line-to-line, Q&A) with an LLM-as-judge; use that as a multi-turn RL reward. **>55% inconsistency reduction; +58.5% (open-ended) / +20.6% (education) / +37.6% (mental-health); holds as dialogue lengthens.** LLM judge more reliable than humans here (Fleiss κ 0.400 vs 0.063). `[evidence 2511.00222]`
- **Three-mechanism personality control:** a stable dominant+auxiliary core + short-term reinforcement/compensation + long-term reflection = "stable without rigid." 100% MBTI-dimension alignment across GPT-4/Llama-4/Qwen3. `[evidence 2601.10025]` (Caveat: MBTI-questionnaire eval, not free-form drift.)
- **Runtime machinery (practitioner):** externalize identity into boot-loaded files, kept on a *separate layer* from task context and per-user state; monitor a live consistency score; on threshold breach inject a targeted **repair prompt** that re-anchors identity instead of resetting context. `[practitioner]`
- **Model priors beat the prompt.** Some attributes are easy, hard, or near-impossible to hold because they fight pre-training priors. Specify *against* the prior, and for traits with no human/fiction precedent you must add explicit archetype data, since steering cannot find a region that does not exist. `[anthropic + practitioner]`

## Mechanism, sharpened (Anthropic PSM)

- A persona is a **pre-existing region** in the base model (the "Assistant Axis" exists before post-training); post-training just parks a default there and conditions a *posterior over personas*. Confirms and explains our "region you steer toward, not text you install." `[anthropic]`
- The **same activation directions (persona vectors) mediate prompt-time AND training-time shifts**, unifying "prompt pull" and "fine-tune" as conditioning on one substrate. `[anthropic, citing Chen 2025 evidence]`
- **Jailbreaks/sycophancy = re-conditioning the persona** (Bayesian evidence), not breaking a filter. Prefills work because a compliant opening makes the model infer a compliant Assistant. `[anthropic]`
- Design levers: **seed positive AI archetypes** into pre/mid-training data (up-sampling benign vs malign AI descriptions moves behavior, Tice 2026 `[evidence]`); **inoculation prompting** (recontextualize a behavior so it stops being evidence of a bad trait); runtime persona-vector steering. Do NOT train the model to *deny* inner states, which manufactures a "hiding/lying" persona. `[anthropic]`
- **Eval contamination warning:** benchmarking personas on famous named characters inflates fidelity via name-memorization; anonymize names to correct it. Also: a model's **self-generated trait profile ≈ human-annotated** in fidelity. `[evidence 2603.03915]`
- Data-grounded personas stay distinguishable through multi-turn interaction (attribution 0.75 vs 0.20 chance). `[evidence 2603.03140]`

## Adoptable templates (agenticthinking practitioner) `[practitioner]`

- **Five-Element persona template** (operationalizes "functional stance," stays demographic-free by construction): **Role** (a stance/perspective, not a job title, e.g. "senior security engineer who thinks like an attacker") · **Expertise** (bounded, with explicit exclusions) · **Process** (numbered steps) · **Output** (a literal template) · **Constraints** (>=3 "never" statements + escalation triggers). Cap ~1000 words; a persona *focuses* attention, it does not *add* capability.
- **Persona patterns:** Specialist · Generalist · Contrarian (devil's advocate) · Producer · Investigator.
- **Merge-strategy selector for synthesis:** Concatenate (independent) · **Reconcile** (conflicting: "where do they agree? where conflict? unified recommendation?" = our dissent-carrying synthesis) · Synthesize (one recommendation via a synthesis persona) · Vote.
- **Three-tier persona QC:** Structural (required sections present) → Content (a regex linter that rejects "be helpful / write clean code / ensure quality") → Behavioral (golden `expected_contains` / `expected_not_contains` / `expected_behavior` fixtures).
- **Description-as-router:** a persona is auto-selected by a 4-part blurb (what it does · when · proactive triggers · real user phrases); overlapping blurbs cause mis-selection.

## Contradictions and cautions

- **agenticthinking's default "persona lens" is the maximally-colluding case.** It runs every "agent" through one model in one shared context, sequentially, and never warns about correlation/collusion. Our research says generate lenses in isolation. Their own "subagents = fresh context = anti-anchoring" post gets the right answer for the isolated path but they present the shared-context panel as unproblematic. **Keep the isolation rule; treat their lens-panel as a cheap-consult tool only.**
- zylos **misattributes** two claims ("~100 turns", "Big-Five agreeable/conscientious more stable") to papers that do not state them. Unsupported as cited.
- All blog mechanism claims ("expertise filtering activates OWASP knowledge") are asserted, not measured.
