# Adversarial Debate: Prompt 2 — Per-Stage Adversarial Review

**Depth**: standard
**Date**: 2026-03-19
**Subject**: Generated Prompt 2 vs. Original Objective for v3.0 Eval Suite

---

## 1. Fidelity: Does the Generated Prompt Faithfully Implement the Original Objective?

### Advocate (Pro-Fidelity)

The generated prompt captures both dimensions specified in the original objective:

- **"the specs effectiveness at being used to test the effectiveness of that step"** is covered by debate question 1 ("Will the eval spec produce meaningful output at this stage, or will the gate trivially pass/fail?") and question 4 ("What is the single most likely failure mode at this stage with this eval spec?").
- **"v3.0's impact on that step"** is covered by debate question 2 ("What does v3.0 specifically change about this stage compared to master?").

The generated prompt goes further by adding concrete file paths, gate names, and artifact references for each agent, which the original objective left implicit.

### Adversary (Against Fidelity)

The fidelity is superficially correct but structurally weak in two ways:

**A. The "engage in an adversarial debate" requirement is diluted.** The original says each agent should "review that step and then engage in an adversarial debate." The generated prompt instead gives 4 structured questions. Answering 4 questions is not the same as an adversarial debate. A debate requires tension, steelmanning, counter-arguments — not a question-answer checklist. The generated prompt converts a dialectical process into a survey.

**B. The two dimensions are unequally weighted.** The original treats "specs effectiveness at testing that step" and "v3.0's impact on that step" as co-equal dimensions joined by "AS WELL AS." In the generated prompt, 3 of 4 questions lean toward testing effectiveness (Q1, Q3, Q4) while only Q1 touches v3.0 impact. The v3.0 dimension is underserved. An agent could answer Q2 in one sentence ("v3.0 adds SPEC_FIDELITY_GATE to this step") and move on. There is no question forcing the agent to analyze *how* v3.0 changes affect the *testing* of that step — which is the intersection the original objective requires.

### Verdict

**Partial fidelity.** The two dimensions are present but not integrated. A missing question like "How does v3.0's change to this stage alter what the eval spec must test, and does the eval spec account for this?" would bridge the gap. The adversarial debate format is replaced with structured questions, which may produce shallower analysis.

---

## 2. Agent Prompt Structure: /sc:adversarial --depth quick Enforcement

### Advocate

The generated prompt explicitly states: "Each agent's prompt MUST start with /sc:adversarial --depth quick." The capitalized "MUST" makes this a clear directive to the spawn orchestrator.

### Adversary

**The enforcement is illusory.** The statement says "MUST start with" but the actual agent assignments (Agent 1 through Agent 13) do not include the `/sc:adversarial --depth quick` prefix in their descriptions. The `/sc:spawn` command receives the overall prompt, and each agent gets a sub-assignment — but the sub-assignment text per agent is:

> "Agent 1: extract (gate: EXTRACT_GATE, file: extraction.md)"

That is not a prompt starting with `/sc:adversarial`. The orchestrator would need to prepend the adversarial command to each agent's individual prompt. Whether `/sc:spawn` does this automatically when instructed at the top level is implementation-dependent. If spawn merely distributes the assignment lines as-is, the adversarial protocol is never invoked.

**Risk:** Without `/sc:adversarial` actually triggering the protocol SKILL, each agent is just a regular Claude session answering 4 questions — no structured steelmanning, no scoring rubric, no convergence threshold. The entire adversarial machinery is bypassed.

### Verdict

**Weak enforcement.** The prompt tells spawn to do it but does not structure the per-agent prompts to guarantee it. A more robust approach would embed the `/sc:adversarial --depth quick` command literally inside each agent's assignment block.

---

## 3. Scope Per Agent: Are the 4 Debate Questions Sufficient?

### Advocate

The 4 questions cover:
1. **Testing effectiveness** — Will the eval spec produce meaningful output or trivially pass/fail?
2. **v3.0 delta** — What does v3.0 specifically change?
3. **Verifiability** — What artifact does the stage produce and how to verify quality?
4. **Risk** — Single most likely failure mode with this eval spec?

This is a focused, actionable set. More questions would dilute agent attention within the `--depth quick` constraint. The questions are well-scoped for a quick pass.

### Adversary

**Three gaps:**

**A. No question about inter-stage dependencies.** Each agent is siloed to its own stage. No question asks: "If the previous stage produces degraded output, how does this stage behave?" This matters critically for the pipeline architecture where stages 9-13 (the v3.0 additions) depend heavily on the quality of stage 7 (merge) output. An eval spec that produces a weak merged roadmap might cause all downstream gates to behave differently than expected.

**B. No question about the gate implementation itself.** Q1 asks about "meaningful output" but not about the gate's semantic checks. For example, `SPEC_FIDELITY_GATE` has specific `SemanticCheck` functions (heading gaps, cross-references, duplicate headings). Does the eval spec's content exercise these checks? An agent reviewing spec-fidelity without reading the actual check functions in `gates.py` would produce surface-level analysis.

**C. No question about false positives/negatives.** Q4 asks about the "most likely failure mode" but only in one direction. What about the opposite — the most likely way this stage *incorrectly passes* when it should not? For an eval suite, false passes are as dangerous as false fails.

### Verdict

**Necessary but insufficient.** The 4 questions provide a reasonable skeleton but miss inter-stage coupling, gate implementation specifics, and false-pass analysis. For `--depth quick` this may be acceptable, but the omissions will produce blind spots in the final eval assessment.

---

## 4. Feasibility: Can 13 Parallel Agents Be Spawned?

### Advocate

The `/sc:spawn` command is designed for parallel agent orchestration. 13 agents is within the documented 2-10+ range. Each agent receives a focused scope (one stage), limiting context requirements. The `--depth quick` flag keeps each debate brief.

### Adversary

**A. The pipeline has 12 steps, not 13.** The `_get_all_step_ids()` function in `executor.py` (line 603) returns exactly 12 IDs: extract, generate-A, generate-B, diff, debate, score, merge, test-strategy, spec-fidelity, wiring-verification, remediate, certify. There is no step called "deviation-analysis" in `_build_steps()`. The deviation-analysis is part of the `execute_validate()` subsystem invoked *after* the main pipeline completes, not a pipeline Step with its own gate in `_build_steps()`. The generated prompt assigns Agent 11 to "deviation-analysis (gate: DEVIATION_ANALYSIS_GATE)" as if it were a pipeline step like the others, but it is architecturally different — it runs inside `validate_executor.py`, not through `roadmap_run_step()`.

This is a **factual error in the generated prompt** that could cause Agent 11 to produce misleading analysis based on a false assumption about how deviation-analysis is orchestrated.

Separately, `DEVIATION_ANALYSIS_GATE` *is* defined in `gates.py` (line 885), and it *is* listed in the gate registry (line 945). So the gate exists, but its relationship to the pipeline step architecture is different from stages 1-9.

**B. Context budget per agent.** Each agent needs: the eval spec, the merged spec, the relevant gate code from `gates.py`, the relevant prompt builder from `prompts.py`, and the executor logic for that stage. For stages like `wiring-verification` (which involves `audit/wiring_gate.py`, AST analysis, `ToolOrchestrator`), the context required is substantial. `--depth quick` helps but does not eliminate the risk of agents operating without sufficient context to debate meaningfully.

**C. Spawn's actual capability.** The `/sc:spawn` command's ability to run 13 truly parallel agents depends on Claude Code's session management. In practice, "parallel" may mean sequential-with-concurrency or truly parallel depending on infrastructure. If sequential, the total execution time for 13 agents at `--depth quick` could still be 30-60 minutes.

### Verdict

**The 13-stage claim is factually incorrect — there are 12 pipeline step IDs.** Deviation-analysis is architecturally distinct from the other steps. The generated prompt should either reduce to 12 agents or explicitly acknowledge that deviation-analysis operates differently (inside validate, not inside `execute_pipeline()`). Feasibility of parallel spawning is implementation-dependent but plausible.

---

## 5. Synthesis Step: Valuable or Scope Creep?

### Advocate

The synthesis step ("After all 13 complete, synthesize a single summary") is operationally necessary. Without it, a human reviewer must read 13 separate debate files to determine whether the eval spec is ready. The synthesis aggregates findings and identifies cross-cutting issues that no single agent would detect.

### Adversary

The original objective says nothing about synthesis. It specifies: "Each agent should review that step and then engage in an adversarial debate." Full stop. Adding a synthesis step means the prompt does more than what was asked, and:

1. It requires a 14th execution step (or a sequential dependency after the parallel batch).
2. It introduces an aggregation layer that could smooth over sharp disagreements from individual agents.
3. It is arguably Prompt 3's job (the next prompt in the 6-prompt suite) to synthesize findings across stages.

### Verdict

**Mild scope creep, but pragmatically valuable.** The synthesis should be clearly marked as an additive enhancement beyond the original objective. If Prompt 3 already handles cross-stage synthesis, this is redundant. If not, it fills a real gap. The generated prompt should note this as an addition.

---

## 6. Risks: What Could Go Wrong?

### Risk 1: Agents Debate Without Reading Gate Code

**Severity: HIGH.** The generated prompt tells agents the gate name (e.g., `EXTRACT_GATE`) but does not instruct them to read the gate definition in `gates.py` or the semantic check functions. An agent could write an entire "debate" about whether the eval spec exercises the extract stage without ever seeing what `EXTRACT_GATE` actually checks (min_length, required_sections, semantic_checks). This produces theater, not analysis.

**Mitigation:** Each agent assignment should explicitly say "Read the gate definition at `src/superclaude/cli/roadmap/gates.py` for your assigned gate and reference specific SemanticCheck functions in your debate."

### Risk 2: Agents Have No Access to the Eval Spec

**Severity: HIGH.** The generated prompt references the eval spec at `.dev/releases/current/v3.0_unified-audit-gating/eval-spec.md`. At the time of this debate, this file may not yet exist (it is the output of Prompt 1). If Prompt 2 runs before Prompt 1 completes, all 13 agents debate an eval spec that does not exist.

**Mitigation:** Prompt 2 should have an explicit precondition: "Verify eval-spec.md exists and is non-empty before spawning agents."

### Risk 3: v3.0 Delta Analysis Requires Master Branch Access

**Severity: MEDIUM.** Question 2 asks "What does v3.0 specifically change about this stage compared to master?" Agents on the `v3.0-AuditGates` branch may not have easy access to the master branch version of `executor.py` and `gates.py` for comparison. They would need to `git diff master...HEAD` or similar, which is not mentioned in the prompt.

**Mitigation:** Provide the diff output as context to agents, or instruct them to run `git diff master -- <relevant-files>`.

### Risk 4: Trivial Debates for Unchanged Stages

**Severity: MEDIUM.** Stages 1-7 (extract through merge) may have zero or minimal changes in v3.0. Agents assigned to these stages have little to debate regarding v3.0 impact. They may produce padding ("v3.0 does not change this stage materially") which is accurate but not useful for eval validation.

**Mitigation:** The prompt could identify which stages are v3.0-changed (spec-fidelity, wiring-verification, deviation-analysis, remediate, certify) vs. unchanged (extract through test-strategy) and adjust expectations accordingly. Unchanged stages should focus Q2 on "Do any upstream or downstream v3.0 changes indirectly affect this stage's behavior?"

### Risk 5: The 13-Stage Error Propagates

**Severity: MEDIUM.** As established in Section 4, the prompt incorrectly lists 13 stages when there are 12 step IDs. Deviation-analysis is not a pipeline Step in `_build_steps()`. If Agent 11 is given this assignment, it may attempt to find a `deviation-analysis` Step in the code, fail, and either hallucinate its analysis or produce a confused output that undermines the review.

---

## Summary of Findings

| Dimension | Rating | Key Issue |
|-----------|--------|-----------|
| Fidelity | PARTIAL | Two dimensions present but not integrated; debate format replaced with Q&A |
| Agent Prompt Structure | WEAK | `/sc:adversarial --depth quick` stated but not embedded per-agent |
| Scope Per Agent | NECESSARY BUT INSUFFICIENT | Missing inter-stage deps, gate impl specifics, false-pass analysis |
| Feasibility | FACTUAL ERROR | 12 steps, not 13; deviation-analysis is architecturally distinct |
| Synthesis | MILD SCOPE CREEP | Pragmatically useful but not in original objective |
| Risks | 2 HIGH, 3 MEDIUM | Gate code not read; eval spec may not exist; master diff not available |

## Recommended Fixes Before Execution

1. **Fix step count**: 12 agents, not 13. Either fold deviation-analysis into the validate subsystem review or explicitly note its distinct architecture.
2. **Embed adversarial command**: Include `/sc:adversarial --depth quick` literally in each agent's prompt block, not just as a top-level instruction.
3. **Add gate-reading instruction**: Require each agent to read their gate's `SemanticCheck` functions from `gates.py` before debating.
4. **Add bridging question**: "How does v3.0's change to this stage alter what the eval spec must exercise?" to integrate the two original dimensions.
5. **Add precondition**: "Verify eval-spec.md exists" before spawning.
6. **Provide master diff context**: Include or instruct agents to generate `git diff master -- src/superclaude/cli/roadmap/` output.
7. **Differentiate v3.0-changed vs. unchanged stages**: Set distinct expectations for stages 1-7 (indirect impact) vs. stages 8-12 (direct v3.0 changes).
