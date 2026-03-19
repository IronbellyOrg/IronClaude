# Reflection: Prompt 3 — Impact Analysis + Eval Design

**Date**: 2026-03-19
**Reviewer**: Claude Opus 4.6 (reflect skill)
**Subject**: prompt-3-impact-analysis.md

---

## 3 Proposed Improvements

### Improvement 1: Add an explicit "implementation completeness" gate between /sc:design and /sc:reflect

**What**: After `/sc:design` produces `eval-e2e-design.md`, add a verification step that checks whether the design doc contains all 6 required elements (Python pseudocode, CLI invocations, artifact schemas, assertion criteria, comparison report format, error handling) for each of the 3 evals — before the `/sc:reflect` invocation. If any element is missing, loop back to `/sc:design` with specific remediation instructions rather than proceeding to reflect on an incomplete design.

**Why**: The current prompt chains `/sc:design` directly into `/sc:reflect`, but the reflect step only checks for brainstorm-to-design drift. If the design is incomplete (e.g., pseudocode is vague, artifact schemas are missing), the reflect step will PASS it because it faithfully matches the brainstorm — but Prompt 4's validation will FAIL on criteria 1 (REAL EXECUTION traceability) or 6 (NO MOCKS), forcing a costly re-run of Prompt 3. An inline completeness gate catches this earlier and cheaper.

### Improvement 2: Require the /sc:analyze step to consume and cross-reference Prompt 2's stage review findings

**What**: Add an explicit instruction after the `/sc:analyze` invocation: "Cross-reference your 3 identified impacts against the stage review summary from Prompt 2. If any of the top 3 impacts target a stage that Prompt 2 flagged as 'trivially passing' with the eval spec, flag this conflict and adjust the impact ranking or note the eval spec limitation." Also require the analyze output to explicitly state which of the 12 pipeline stages each impact maps to.

**Why**: Prompt 2 produces per-stage adversarial findings that directly inform whether the eval spec will actually exercise the impacts Prompt 3 identifies. Currently, Prompt 3 references the stage review summary in its context placeholder but never instructs the agent to USE those findings during impact selection. This means the agent could identify 3 impacts that are real in production but untestable with this eval spec — producing eval designs that look correct but fail to demonstrate anything meaningful when Prompt 5 runs them.

### Improvement 3: Add a failure-mode injection requirement to each eval design

**What**: Add a 7th requirement to the eval design list: "7. Each eval must include a negative control: a specific, documented way to make the eval FAIL (e.g., remove a gate definition, corrupt an input file, use a spec with no ambiguities). The negative control must be runnable as a CLI flag (e.g., `--inject-failure`) and must produce a different result than the normal run. If the eval passes with and without the negative control, it is not testing anything."

**Why**: The critical lesson from the rejected approach is that evals can appear to work while testing nothing. Prompt 4 checks for mocks and real execution, but it cannot verify that the eval is sensitive to the thing it claims to measure. A negative control is the standard scientific method for proving sensitivity. Without it, an eval could invoke the real pipeline, produce real artifacts, and still prove nothing — because the same artifacts would be produced regardless of whether v3.0's new gates exist.

---

## Adversarial Debate

### Improvement 1: Design completeness gate between /sc:design and /sc:reflect

**Advocate**: This is a structural fix for a known failure mode in sequential prompt chains. Prompt 4 exists specifically because incomplete designs escape Prompt 3. But Prompt 4 is expensive — it re-reads the entire eval-e2e-design.md plus all eval scripts plus greps for mocks. An inline completeness check in Prompt 3 is a 50-token verification that prevents a full Prompt 3 + Prompt 4 re-run cycle. The ROI is massive: spend 50 tokens to save 5000+. This is exactly the confidence-check pattern this framework is built on.

**Critic**: The `/sc:reflect` invocation at the end of Prompt 3 already serves as a quality gate. Adding ANOTHER verification step between design and reflect adds token overhead to every run, not just the ones that fail. More importantly, this changes the prompt's structure from 4 clean skill invocations to a conditional loop, which is harder for the executing agent to follow correctly. The reflect step can be expanded to check completeness instead of adding a new intermediate step — that is simpler and achieves the same result. Finally, Prompt 4 is the designated validation gate for the entire chain. Duplicating its function inside Prompt 3 violates single-responsibility and creates a maintenance burden: if the completeness criteria change, you must update both Prompt 3 and Prompt 4.

**Verdict: SKIP** — The concern is valid but the solution is wrong. The reflect step should be strengthened rather than adding a new intermediate gate. This avoids the structural complexity and maintenance duplication the critic identified.

---

### Improvement 2: Cross-reference Prompt 2 stage review findings during impact analysis

**Advocate**: This is the highest-leverage improvement because it addresses a semantic gap, not just a structural one. Prompt 3 is the pivotal prompt in the chain — it determines WHAT the evals test. If the 3 impacts are untestable with the eval spec (because Prompt 2 already identified that the relevant stages will trivially pass), then Prompts 4, 5, and 6 are all wasted effort. The stage review findings are the single most relevant input for impact selection, but the current prompt only lists them as passive context. Making the cross-reference explicit ensures the agent uses the information it already has. This costs zero additional tool calls — it is a prompt instruction change, not a new step.

**Critic**: The Prompt 2 context is already in the placeholder section. A competent agent will naturally consult it when selecting impacts. Adding explicit cross-reference instructions is hand-holding that inflates the prompt and makes it more fragile — if Prompt 2's output format changes, the cross-reference instruction becomes stale. Additionally, Prompt 2's findings might be wrong (adversarial debates produce false positives). Requiring Prompt 3 to defer to Prompt 2's findings could cause it to avoid the most important impacts in favor of "easier to test" ones, which defeats the purpose. The agent should use judgment, not follow a mechanical cross-reference.

**Advocate rebuttal**: The placeholder is currently empty — it says "[pending P2]". The instruction is not about deferring to Prompt 2's findings, it is about acknowledging and addressing conflicts. The instruction says "flag this conflict and adjust OR note the limitation" — it preserves agent judgment while requiring the conflict to be made explicit rather than silently ignored. This is the difference between "I checked and it is fine" and "I never checked."

**Verdict: APPLY** — The advocate's rebuttal is decisive. The cross-reference is low-cost (instruction change only), addresses a real semantic gap (impacts may be untestable), and preserves agent autonomy (flag + decide, not defer). The critic's concern about over-mechanization is mitigated by the "flag and note" framing.

---

### Improvement 3: Negative control / failure-mode injection

**Advocate**: This is scientifically sound and addresses the deepest failure mode: evals that run real code but prove nothing. Prompt 4 checks that execution is real, but cannot check that execution is meaningful. A negative control is the only way to prove an eval is sensitive to the thing it claims to measure. This is standard practice in any evaluation methodology. Without it, we could have 3 evals that all pass on both v3.0 and master — proving only that the pipeline runs, not that v3.0 improves it.

**Critic**: Adding a negative control requirement to each eval doubles the number of pipeline runs (3 normal + 3 negative = 6 runs in Prompt 5, vs the current 4). Each run involves ~10 Claude subprocess calls, so this adds ~20 Claude calls to the eval suite. The cost is enormous. More importantly, Prompt 5 already runs both v3.0 AND master. The master run IS the negative control — master lacks the 5 new stages, so if the eval measures those stages, master will naturally produce different results. Adding an artificial failure injection on top of the natural A/B comparison is redundant. Finally, designing good negative controls is itself a design problem that could absorb significant prompt budget and produce brittle injection mechanisms.

**Verdict: SKIP** — The critic's point about master-as-negative-control is correct for this specific eval suite. The A/B structure (v3.0 vs master) already provides the sensitivity check. Artificial failure injection would be valuable for a single-branch eval but is redundant here.

---

## Selection: Best Improvement

**Winner: Improvement 2** — Cross-reference Prompt 2 stage review findings during impact analysis.

**Rationale**: Highest impact-to-risk ratio. Zero additional cost (instruction-only change). Addresses a semantic gap that could silently waste all downstream prompts. Does not change the prompt's structure or skill invocation chain. Preserves agent judgment while requiring explicit acknowledgment of known testability constraints.

**Implementation**: Add a cross-reference instruction after the `/sc:analyze` output verification step (line 47 area) and before the `/sc:brainstorm` invocation.
