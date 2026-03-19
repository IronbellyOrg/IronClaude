---
title: "Prompt 5: Parallel Execution + Scoring Framework"
sequence: 5 of 6
depends_on: prompt-1 (eval-spec.md), prompt-4 (validation PASS)
produces: eval-runs/local-A/, local-B/, global-A/, global-B/, scoring-framework.md
next_prompt: prompt-6-scoring-report.md
---

# Context (carry-forward from prior work)

## Critical Lessons
- **Rejected approach**: 168 pytest unit tests. No pipeline execution. No artifacts. Rejected.
- **This prompt exists because of that rejection.** It RUNS the actual pipeline.
- **12 steps, not 13**: deviation-analysis is a logical phase, not a discrete step.
- **Master lacks 5 stages**: Global runs on master will NOT have spec-fidelity, wiring-verification, deviation-analysis, remediate, certify. Score these as "stage not available on master" not "stage failed."
- **Scoring framework is authoritative**: Prompt 6 MUST defer to whatever methodology this prompt's framework defines. Do not produce a generic pipeline health tool — produce a delta-demonstration tool.
- **Known escape hatches from adversarial debate**: Potemkin pipelines (real execution but trivial spec), copy-paste evals (run once, copy artifacts), checkpoint evals (real first stages, synthetic later stages), warm-cache evals (real execution but nothing to detect), timing-only deltas (measure duration, not quality).

## Pipeline Architecture
- 12 discrete steps. v3.0 adds 5 new capabilities.
- Each `superclaude roadmap run` invocation spawns ~10 Claude subprocess calls.
- 4 parallel runs = ~40 total Claude calls. Launched with 30s stagger intervals to stay within API rate limits.
- Artifact provenance matters: files on disk don't prove they were produced by the pipeline.

## From Prompt 3 (Impact Analysis + Eval Design)
- **eval-e2e-design.md location**: .dev/releases/current/v3.0_unified-audit-gating/eval-e2e-design.md
- **3 identified impacts**: (1) Deterministic wiring verification gate [executor.py:244-259, wiring_gate.py:313], (2) Convergence-controlled spec-fidelity with DeviationRegistry [convergence.py:50-226, executor.py:521], (3) Mode-aware rollout enforcement [wiring_gate.py:113-135, executor.py:248/537]
- **3 pre-v3.0 issues mitigated**: (1) Documents pass but code modules are unwired (32 symbols/14 files), (2) LLM severity noise indistinguishable from structural regressions, (3) New gates must deploy at full enforcement or not at all
- **Eval scripts**: scripts/eval_1.py, scripts/eval_2.py, scripts/eval_3.py (pseudocode in design doc, extracted to standalone files in Prompt 4)
- **Reflect findings**: D-1 convergence multi-run narrowing accepted with limitation noted; D-2 direct analyzer call accepted as improvement; G-1 missing multi-run regression phase (MEDIUM); G-2/G-3/G-4 minor clarification gaps (LOW)

## From Prompt 4 (Eval Validation)
- **Validation report**: .dev/releases/current/v3.0_unified-audit-gating/eval-validation-report.md
- **Overall status**: PASS
- **CRITICAL criteria results**: [1:PASS, 2:PASS, 3:PASS, 4:PASS, 5:PASS]
- **REQUIRED criteria results**: [6:PASS, 7:PASS]
- **Remediation applied**: Extracted eval_1.py, eval_2.py, eval_3.py from design doc to scripts/. Added verify_artifact_provenance() to all 3 scripts. Added content integrity assertions to eval_1. Updated eval_runner.py with E2E orchestration via run_e2e_script().
- **Re-validation count**: 2 (first pass failed due to unextracted scripts; second pass clean)
- **E2E scripts**: All 3 invoke `superclaude roadmap run` via subprocess, produce persistent timestamped artifacts, include mtime-based provenance checks, support `--branch local|global` for A/B comparison

---

# Prompt

```
/sc:spawn "Execute v3.0 eval suite: 4 parallel eval runners + scoring framework + adversarial review" --strategy adaptive

Precondition: Verify .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md exists and eval-validation-report.md shows no BLOCKED criteria.

## Phase 1: Spawn 4 eval runners (staggered launch)

Executable eval scripts exist at scripts/eval_1.py, eval_2.py, eval_3.py (extracted in Prompt 4, validated PASS on all 7 criteria). Use `uv run python scripts/eval_runner.py --mode full` to orchestrate all runs, OR run the agents below for manual control.

**Launch stagger**: Each agent spawns ~10 Claude subprocess calls. To avoid API rate-limit failures, launch agents with a minimum 30-second delay between starts:
- T+0s: Agent 1 (Local Run A)
- T+30s: Agent 2 (Local Run B)
- T+60s: Agent 3 (Global Run A)
- T+90s: Agent 4 (Global Run B)

**Rate-limit recovery**: If any subprocess returns HTTP 429 or a rate-limit error, the agent must retry with exponential backoff (initial 30s, max 5 retries). Log each retry with timestamp. If an agent exhausts retries, mark the run as FAILED and continue with remaining agents.

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

Partial-failure policy: Minimum 1 local + 1 global run must complete successfully to proceed. Report any failures including rate-limit exhaustion events.

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
