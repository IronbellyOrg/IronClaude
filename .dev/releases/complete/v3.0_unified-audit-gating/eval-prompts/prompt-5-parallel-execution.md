---
title: "Prompt 5: Parallel Execution + Scoring Framework"
sequence: 5 of 6
depends_on: prompt-1 (eval-spec.md), prompt-4 (validation PASS)
produces: eval-runs/local-A/, local-B/, global-A/, global-B/, scoring-framework.md
next_prompt: prompt-6-scoring-report.md
---

# Context (carry-forward from prior work)

## Critical Lessons
- **Rejected approach**: Unit tests with no pipeline execution. This prompt RUNS the actual pipeline.
- **12 steps, not 13**: deviation-analysis is a logical phase, not a discrete step.
- **Master lacks 5 stages**: Global runs on master will NOT have spec-fidelity, wiring-verification, deviation-analysis, remediate, certify. Score these as "stage not available on master" not "stage failed."
- **Scoring framework is authoritative**: Prompt 6 MUST defer to whatever methodology this prompt's framework defines. Do not produce a generic pipeline health tool — produce a delta-demonstration tool.

## Pipeline Architecture
- 12 discrete steps. v3.0 adds 5 new capabilities.
- Each `superclaude roadmap run` invocation spawns ~10 Claude subprocess calls.
- 4 parallel runs = ~40 total Claude calls (staggered, not simultaneous).

## From Prompt 1 (Spec Generation)
<!-- PLACEHOLDER: To be filled after Prompt 1 -->
- **eval-spec.md location**: .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md

## From Prompt 4 (Eval Validation)
- **Validation report**: .dev/releases/current/v3.0_unified-audit-gating/eval-validation-report.md
- **Overall status**: PASS
- **CRITICAL criteria results**: [1:PASS, 2:PASS, 3:PASS, 4:PASS, 5:PASS]
- **REQUIRED criteria results**: [6:PASS, 7:PASS]
- **Remediation applied**: Extracted eval_1.py, eval_2.py, eval_3.py from design doc pseudocode to scripts/. Added verify_artifact_provenance() to all 3 scripts. Added content integrity assertions to eval_1. Updated eval_runner.py with E2E orchestration.
- **Re-validation count**: 2 (first pass failed due to unextracted scripts; second pass clean)
- **Extracted E2E scripts**: scripts/eval_1.py (wiring gate), scripts/eval_2.py (convergence), scripts/eval_3.py (rollout enforcement) — all syntax-verified, all invoke `superclaude roadmap run` via subprocess
- **eval_runner.py**: Updated with `run_e2e_script()` function and `E2E_SCRIPTS` list for A/B orchestration

---

# Prompt

```
/sc:spawn "Execute v3.0 eval suite: 4 parallel eval runners + scoring framework + adversarial review" --strategy adaptive

Precondition: Verify .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md exists and eval-validation-report.md shows no BLOCKED criteria.

## Phase 1: Spawn 4 parallel eval runners

If Prompt 3 produced executable eval scripts (scripts/eval_1.py, eval_2.py, eval_3.py), run those. Otherwise, run `superclaude roadmap run` directly against the eval-spec as the eval mechanism.

Agent 1 (Local Run A):
Run `superclaude roadmap run .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md --output .dev/releases/current/v3.0_unified-audit-gating/eval-runs/local-A/`
After completion, list all files produced and their sizes. Record wall-clock time.

Agent 2 (Local Run B):
Run `superclaude roadmap run .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md --output .dev/releases/current/v3.0_unified-audit-gating/eval-runs/local-B/`
After completion, list all files produced and their sizes. Record wall-clock time.

Agent 3 (Global Run A):
Create git worktree from master at `../IronClaude-eval-global-A`. Install superclaude with `uv pip install -e .`.
Run `superclaude roadmap run .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md --output .dev/releases/current/v3.0_unified-audit-gating/eval-runs/global-A/`
NOTE: Master lacks 5 v3.0 stages. Score as "not available" not "failed."
After completion, list all files produced and their sizes. Record wall-clock time. Clean up worktree.

Agent 4 (Global Run B):
Create git worktree from master at `../IronClaude-eval-global-B`. Install superclaude with `uv pip install -e .`.
Run `superclaude roadmap run .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md --output .dev/releases/current/v3.0_unified-audit-gating/eval-runs/global-B/`
Same notes as Agent 3.
After completion, list all files produced and their sizes. Record wall-clock time. Clean up worktree.

Partial-failure policy: Minimum 1 local + 1 global run must complete successfully to proceed. Report any failures.

## Phase 2: While runners execute, generate scoring framework

Produce scoring framework at: .dev/releases/current/v3.0_unified-audit-gating/scoring-framework.md

DESIGNED TO DEMONSTRATE THE DELTA before and after v3.0. Lead with delta-focused requirements:
1. Define how to compute v3.0-vs-master delta for each metric — this is the framework's primary purpose
2. Define scoring thresholds: what constitutes a positive delta, neutral, negative
3. Address the 5 new v3.0 stages and how to score stages that don't exist on master
4. Define per-stage metrics (gate pass/fail, artifact size, quality indicators) as supporting data
5. Include human evaluator instructions
6. Define reproducibility thresholds for run-to-run consistency
7. Include /sc:troubleshoot analysis instructions for negative/inconsistent deltas

## Phase 3: Adversarial review of scoring framework

Spawn agent with: /sc:adversarial --depth standard "Review the scoring framework"

Provide: scoring-framework.md, merged-spec.md, eval-spec.md, executor.py, gates.py, convergence.py

Debate: (1) measures v3.0 changes vs generic health? (2) thresholds defensible? (3) distinguishes v3.0 improvement from LLM variance? (4) troubleshoot path actionable?

Write to: .dev/releases/current/v3.0_unified-audit-gating/adversarial/scoring-framework-debate.md
Apply critical findings to scoring-framework.md.

## Phase 4: Collect results

Produce summary at: .dev/releases/current/v3.0_unified-audit-gating/eval-runs/execution-summary.md
Include: artifact inventory per run, timing, errors, file size comparison.
```

---

# Post-Run: Forward Context to Next Prompt

After this prompt completes, append the following to the **Context** section of `prompt-6-scoring-report.md`:

```markdown
## From Prompt 5 (Parallel Execution + Scoring)
- **Scoring framework**: .dev/releases/current/v3.0_unified-audit-gating/scoring-framework.md
- **Execution summary**: .dev/releases/current/v3.0_unified-audit-gating/eval-runs/execution-summary.md
- **Runs completed**: [local-A: PASS/FAIL, local-B: PASS/FAIL, global-A: PASS/FAIL, global-B: PASS/FAIL]
- **Artifacts per local run**: [count and list of files]
- **Artifacts per global run**: [count and list — expect fewer due to missing v3.0 stages]
- **Wall-clock timing**: [local-A: Xs, local-B: Xs, global-A: Xs, global-B: Xs]
- **Adversarial findings on scoring framework**: [list critical findings applied]
- **Scoring framework delta methodology**: [brief summary of how deltas are computed per the framework]
- **Scoring framework reproducibility threshold**: [the threshold value defined]
```
