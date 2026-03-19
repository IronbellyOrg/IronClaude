---
title: "Reflect: Prompt 2 — Per-Stage Adversarial Review"
date: 2026-03-19
model: claude-opus-4-6
---

# Prompt 2 Reflection: Per-Stage Adversarial Review

## Summary of Prompt 2

Prompt 2 spawns 12 parallel agents, each performing `/sc:adversarial --depth quick` on one of the 12 pipeline stages. Each agent debates 5 questions about their stage's interaction with the eval spec. Outputs go to individual stage debate files plus a synthesis summary.

---

## Proposed Improvements

### Improvement 1: Add explicit exit criteria and a grading rubric for the synthesis summary

**What**: The prompt tells agents to "synthesize a single summary" but provides no structure for what that summary must contain or how to grade each stage. Add a required output schema for `stage-review-summary.md` that mandates: (a) a per-stage verdict row (ADEQUATE / NEEDS-REVISION / BLOCKED), (b) a ranked list of coverage gaps, and (c) a prioritized action list for Prompt 3 to consume.

**Why**: Without a defined schema, the synthesis step is unconstrained. Different runs will produce wildly different summaries, making it impossible for Prompt 3 to reliably consume the output. The forward-context section at the bottom already expects structured fields like "Stages flagged as trivially passing" but the prompt never tells the synthesizer to produce those categories explicitly.

### Improvement 2: Add a convergence gate — require agents to cross-reference at least one adjacent stage

**What**: Currently each agent operates in isolation on its own stage. Add a requirement that each agent must identify at least one upstream or downstream dependency and state whether the eval spec exercises the interface between the two stages (e.g., Agent 4 (diff) must check whether the artifacts from Agents 2-3 (generate-A/B) are in the format diff expects).

**Why**: The pipeline is sequential — each stage consumes the prior stage's output. Reviewing stages in isolation misses the most common failure mode: format mismatches or missing fields at stage boundaries. This is especially critical for the v3.0 stages (9-12) which form a conditional chain (spec-fidelity -> remediate -> certify).

### Improvement 3: Replace the 12-agent parallel spawn with a 3-tier strategy (unchanged stages batch, new stages individual, conditional stages paired)

**What**: Instead of 12 identical agents, group stages 1-7 (largely unchanged per the prompt's own note) into a single batch review agent, keep stages 8-10 as individual agents, and pair stages 11-12 (remediate + certify) into one agent since they share a conditional trigger.

**Why**: The prompt itself acknowledges "Steps 1-7 are largely unchanged in v3.0." Giving 7 agents identical depth to unchanged stages wastes compute and dilutes attention from the 5 new v3.0 capabilities. Pairing remediate+certify acknowledges their tight coupling — you cannot meaningfully review certify without understanding remediate's output.

---

## Adversarial Debate

### Improvement 1: Exit criteria and grading rubric for synthesis

**Advocate**: This is the highest-leverage change because it directly fixes a structural gap. The prompt has a "Forward Context" section that expects specific structured fields (trivially-passing stages, likely-to-fail stages, coverage gaps, recommendations). But the actual prompt body never instructs anyone to produce those categories. This means the human operator has to manually extract and categorize findings before feeding Prompt 3 — exactly the kind of manual bridging that breaks eval reproducibility. Adding a schema takes 5-8 lines and guarantees the output is machine-parseable by the next prompt.

**Critic**: The synthesis step is done by the orchestrator, not the individual agents. The orchestrator has the full debate outputs and can structure the summary however the next prompt needs. Over-constraining the synthesis format might cause it to force-fit findings into categories that don't match what was actually found. Additionally, the forward-context section is a human checklist, not an automated pipeline — the operator can fill it in.

**Verdict**: **APPLY**. The critic's point about over-constraining is valid, but the current state is under-constrained to the point of non-reproducibility. The forward-context section lists 5 specific deliverables; the synthesis should be told to produce them. The risk of force-fitting is low because the categories are broad (trivially passing, likely to fail, coverage gaps).

---

### Improvement 2: Cross-reference adjacent stages

**Advocate**: Stage boundary failures are the number-one failure mode in sequential pipelines. Agent 9 (spec-fidelity) can't meaningfully assess whether the eval spec exercises its stage without knowing what merge (stage 7) actually produces. Agent 11 (remediate) can't assess its trigger condition without understanding spec-fidelity's output format. This cross-referencing is the single most valuable thing these agents could do beyond what the 5 debate questions already cover.

**Critic**: The 5 debate questions already partially cover this. Question 2 asks about upstream/downstream v3.0 changes. Question 4 asks about failure modes. An agent reviewing the diff stage will naturally consider whether generate-A/B outputs are compatible. Adding a formal cross-reference requirement risks turning a quick adversarial review into a deep integration analysis, which is Prompt 3's job. The prompt already says `--depth quick`. Adding cross-stage analysis contradicts that depth setting.

**Verdict**: **SKIP**. The critic is right that this overlaps with debate questions 2 and 4, and that deep integration analysis belongs in Prompt 3. The `--depth quick` flag signals intentional constraint. Forcing cross-referencing here would either be superficial (adding noise) or deep (scope creep).

---

### Improvement 3: Consolidate agents by tier

**Advocate**: 12 agents is expensive and the prompt itself says stages 1-7 are "largely unchanged." The real eval value is in stages 8-12. Consolidating unchanged stages into a batch lets the executor allocate more compute to the stages that matter. Pairing remediate+certify acknowledges their shared conditional trigger — reviewing certify without knowing remediate's output is meaningless.

**Critic**: This fundamentally changes the prompt's architecture. The 12-agent design has a 1:1 mapping between agents and pipeline steps, which is clean, debuggable, and produces 12 individually reviewable artifacts. Batching stages 1-7 means their debate output is merged into one file, losing granularity. If one unchanged stage IS affected by v3.0 changes (the prompt acknowledges this possibility in question 2), the batch agent might bury the finding. The compute savings are modest — these are `--depth quick` reviews, not deep analyses. And the pairing of 11+12 creates an asymmetry that complicates the synthesis step.

**Verdict**: **SKIP**. The 1:1 mapping is a deliberate design choice that prioritizes debuggability and artifact granularity over efficiency. The prompt already mitigates over-investment via `--depth quick`. Consolidation introduces structural complexity for marginal compute savings.

---

## Final Selection

**Winner: Improvement 1 — Exit criteria and grading rubric for the synthesis summary**

**Rationale**: Highest impact-to-risk ratio. The change is additive (does not modify existing agent instructions), directly fixes a reproducibility gap between Prompt 2's output and Prompt 3's input expectations, and requires only a small addition to the prompt. The other two improvements either overlap with existing coverage (Improvement 2) or introduce structural risk for marginal gains (Improvement 3).

**Specific edit**: Add a structured output schema for `stage-review-summary.md` that mandates the categories already expected by the forward-context section, ensuring the synthesis is consumable by Prompt 3 without manual intervention.
