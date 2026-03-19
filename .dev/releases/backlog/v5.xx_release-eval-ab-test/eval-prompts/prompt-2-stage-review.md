---
title: "Prompt 2: Per-Stage Adversarial Review"
sequence: 2 of 6
depends_on: prompt-1 (eval-spec.md must exist)
produces: 12 stage debate files + stage-review-summary.md
next_prompt: prompt-3-impact-analysis.md
---

# Context (carry-forward from prior work)

## Critical Lessons
- **Rejected approach**: 168 pytest unit tests tested gate functions in isolation. No pipeline stages executed. Rejected for producing no real artifacts.
- **What "real eval" means**: Evals must invoke `superclaude roadmap run` and produce inspectable disk artifacts.

## Pipeline Architecture
- 12 discrete pipeline steps + deviation-analysis logical phase.
- Steps 1-8 (extract through test-strategy) are largely unchanged in v3.0.
- Steps 9-12 (spec-fidelity, wiring-verification, remediate, certify) are new in v3.0.
- deviation-analysis runs inside the convergence loop, not as a standalone Step.
- remediate/certify only fire if spec-fidelity FAIL with HIGH findings.

## From Prompt 1 (Spec Generation)

- **eval-spec.md location**: .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md
 ## From Prompt 1 (Spec Generation)                                                                                          
  - **eval-spec.md location**: .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md
  - **spec_type used**: new_feature                                                                                           
  - **EVAL-SEEDED-AMBIGUITY count**: 2 ambiguities placed targeting: (1) deviation sub-entry schema omission in FR-001.4 →    
  BLOCKING, (2) "significant findings" undefined threshold in FR-001.5 → WARNING                                              
  - **Spec-panel findings applied**: N-1 atomic write mechanism, W-1 JSON/JSONL resolution, F-1 main.py row removal, N-3      
  overwrite behavior, N-2 concurrency risk clarification                                                                      
  - **Spec-panel findings preserved**: FR-001.4 and FR-001.5 EVAL-SEEDED items flagged by panel but intentionally kept
  - **Dry-run result**: PASS (10 steps listed, no warnings)                                                                   
  - **Functional requirements count**: 6                                                                                      
  - **Real files referenced**: executor.py, commands.py, gates.py, main.py, convergence.py, wiring_gate.py       

---

# Prompt

```
/sc:spawn "Review each of the 12 roadmap pipeline steps against the eval spec for testing effectiveness" --strategy parallel

Precondition: Verify .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md exists and is non-empty before spawning agents.

Spawn 12 agents. Each agent's individual prompt MUST begin with the literal text `/sc:adversarial --depth <LEVEL>` followed by their assignment, where LEVEL is:
- `quick` for Agents 1-8 (stages largely unchanged in v3.0 — review focuses on indirect effects)
- `standard` for Agents 9-12 (stages new in v3.0 — these are the primary eval targets and require deeper adversarial analysis)

Context for all agents:
- The eval spec is at: .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md
- The v3.0 release spec is at: .dev/releases/current/v3.0_unified-audit-gating/merged-spec.md
- The pipeline implementation is at: src/superclaude/cli/roadmap/executor.py (function _build_steps, lines 396-541)
- The gate definitions are at: src/superclaude/cli/roadmap/gates.py
- Master branch diff: run `git diff master -- src/superclaude/cli/roadmap/ src/superclaude/cli/audit/` and include relevant output

Each agent must:
1. Read their gate's SemanticCheck functions from gates.py before debating
2. Address ALL 5 debate questions below

Debate questions (all 5 required per agent):
1. Will the eval spec produce meaningful output at this stage, or will the gate trivially pass/fail?
2. What does v3.0 specifically change about this stage compared to master? (For stages 1-7 which are unchanged: "Do any upstream or downstream v3.0 changes indirectly affect this stage's behavior?")
3. What artifact does this stage produce and how can a third party verify its quality?
4. What is the single most likely failure mode at this stage with this eval spec?
5. How does v3.0's change to this stage alter what the eval spec must exercise, and does the eval spec account for this?

Agent assignments (12 agents for 12 pipeline steps):
- Agent 1: `/sc:adversarial --depth quick` — extract (gate: EXTRACT_GATE, file: extraction.md)
- Agent 2: `/sc:adversarial --depth quick` — generate-A (gate: GENERATE_A_GATE, file: roadmap-{agent-a}.md)
- Agent 3: `/sc:adversarial --depth quick` — generate-B (gate: GENERATE_B_GATE, file: roadmap-{agent-b}.md)
- Agent 4: `/sc:adversarial --depth quick` — diff (gate: DIFF_GATE, file: diff-analysis.md)
- Agent 5: `/sc:adversarial --depth quick` — debate (gate: DEBATE_GATE, file: debate-transcript.md)
- Agent 6: `/sc:adversarial --depth quick` — score (gate: SCORE_GATE, file: base-selection.md)
- Agent 7: `/sc:adversarial --depth quick` — merge (gate: MERGE_GATE, file: roadmap.md)
- Agent 8: `/sc:adversarial --depth quick` — test-strategy (gate: TEST_STRATEGY_GATE, file: test-strategy.md)
- Agent 9: `/sc:adversarial --depth standard` — spec-fidelity + deviation-analysis (gate: SPEC_FIDELITY_GATE + DEVIATION_ANALYSIS_GATE, file: spec-fidelity.md — NOTE: deviation-analysis runs as a logical phase within the convergence loop, not as a separate Step)
- Agent 10: `/sc:adversarial --depth standard` — wiring-verification (gate: WIRING_GATE, file: wiring-verification.md — NOTE: runs real static analysis via run_wiring_analysis(), NOT an LLM)
- Agent 11: `/sc:adversarial --depth standard` — remediate (gate: REMEDIATE_GATE — NOTE: only runs if spec-fidelity FAIL)
- Agent 12: `/sc:adversarial --depth standard` — certify (gate: CERTIFY_GATE — NOTE: only runs if remediate completes)

Each agent writes its debate to: .dev/releases/current/v3.0_unified-audit-gating/adversarial/stage-{N}-{stage-name}.md

After all 12 complete, synthesize a single summary: .dev/releases/current/v3.0_unified-audit-gating/adversarial/stage-review-summary.md

The summary MUST use this structure (these categories map directly to what Prompt 3 consumes):

## Per-Stage Verdicts
| Stage | Verdict | Rationale |
For each of the 12 stages, assign exactly one verdict:
- **ADEQUATE**: eval spec will produce meaningful, non-trivial output at this stage
- **NEEDS-REVISION**: eval spec has a gap that should be addressed before running evals
- **BLOCKED**: eval spec cannot exercise this stage as currently written

## Stages Flagged as "Trivially Passing"
List any stages where the agent concluded the gate will pass without exercising real behavior.

## Stages Flagged as "Likely to Fail"
List any stages with identified failure risks, with the failure mode from debate question 4.

## Coverage Gaps
Ranked list of pipeline behaviors the eval spec does not exercise, ordered by severity.

## Recommendations for Eval Design
Key findings that should inform the 3 E2E evals designed in Prompt 3. Each recommendation must cite the stage(s) and debate question(s) that produced it.
```

---

# Post-Run: Forward Context to Next Prompt

After this prompt completes, append the following to the **Context** section of `prompt-3-impact-analysis.md`:

```markdown
## From Prompt 2 (Stage Review)
- **Stage review summary**: .dev/releases/current/v3.0_unified-audit-gating/adversarial/stage-review-summary.md
- **Stages flagged as "trivially passing"**: [list any stages where agents said the eval spec won't produce meaningful output]
- **Stages flagged as "likely to fail"**: [list stages with identified failure risks]
- **Coverage gaps identified**: [any pipeline behaviors the eval spec doesn't exercise]
- **Recommendations for eval design**: [key findings that should inform the 3 E2E evals in Prompt 3]
```
