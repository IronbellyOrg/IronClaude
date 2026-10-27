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
<!-- PLACEHOLDER: To be filled after Prompt 1 completes -->
- **eval-spec.md location**: .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md
- **EVAL-SEEDED-AMBIGUITY count**: [pending P1 completion]
- **Dry-run result**: [pending P1 completion]

---

# Prompt

```
/sc:spawn "Review each of the 12 roadmap pipeline steps against the eval spec for testing effectiveness" --strategy parallel

Precondition: Verify .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md exists and is non-empty before spawning agents.

Spawn 12 agents. Each agent's individual prompt MUST begin with the literal text `/sc:adversarial --depth quick` followed by their assignment.

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
- Agent 9: `/sc:adversarial --depth quick` — spec-fidelity + deviation-analysis (gate: SPEC_FIDELITY_GATE + DEVIATION_ANALYSIS_GATE, file: spec-fidelity.md — NOTE: deviation-analysis runs as a logical phase within the convergence loop, not as a separate Step)
- Agent 10: `/sc:adversarial --depth quick` — wiring-verification (gate: WIRING_GATE, file: wiring-verification.md — NOTE: runs real static analysis via run_wiring_analysis(), NOT an LLM)
- Agent 11: `/sc:adversarial --depth quick` — remediate (gate: REMEDIATE_GATE — NOTE: only runs if spec-fidelity FAIL)
- Agent 12: `/sc:adversarial --depth quick` — certify (gate: CERTIFY_GATE — NOTE: only runs if remediate completes)

Each agent writes its debate to: .dev/releases/current/v3.0_unified-audit-gating/adversarial/stage-{N}-{stage-name}.md

After all 12 complete, synthesize a single summary: .dev/releases/current/v3.0_unified-audit-gating/adversarial/stage-review-summary.md
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
