<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Variants: analysis-eval-report.md (V1), analysis-execution-summary.md (V2), analysis-improvement-proposals.md (V3) -->
<!-- Merge date: 2026-03-19 -->

# Ranked Spec Change Proposals for release-eval-spec.md

## Methodology

13 proposals from 3 analysis artifacts were debated by 3 Advocate agents and 1 Skeptic agent (depth: deep). Proposals were scored on **Value** (1-10: impact on eval correctness, evidenced by actual v3.0 eval run data) and **Complexity** (1-10: effort to implement in spec + code). Duplicates merged (C+L). Final ranking by Value/Complexity ratio with a minimum absolute value threshold of 5.0 for "Recommended" status.

---

## Final Ranked Table

| Rank | ID | Proposal | Value | Complexity | Ratio | Verdict | Source |
|------|----|----------|-------|------------|-------|---------|--------|
| 1 | C+L | **Ternary verdict model** (PASS/CONDITIONAL_PASS/FAIL) | 8.7 | 2.3 | 3.78 | ACCEPT | V1+V3 |
| 2 | F | **Partial run scoring** (steps_completed/steps_total on RunResult) | 7.5 | 2.0 | 3.75 | ACCEPT | V2 |
| 3 | K | **Eval-mode execution** (--continue-on-fail flag) | 8.0 | 2.5 | 3.20 | ACCEPT | V3 |
| 4 | E | **Duration variance threshold** (NFR-EVAL.16, informational) | 3.0 | 1.5 | 2.00 | CONSIDER | V1 |
| 5 | M | **Auto-detect LLM fabrication** (structural test in FR-EVAL.9) | 6.0 | 3.5 | 1.71 | CONSIDER | V3 |
| 6 | B | **Correct failure classification** (expected_gate_failures in suite YAML) | 7.5 | 4.5 | 1.67 | ACCEPT | V1 |
| 7 | D | **Regression-guard scoring mode** (binary PASS/REGRESSION) | 5.5 | 4.0 | 1.38 | DEFER | V1 |
| 8 | A | **Code-level evidence tier** (evidence_source field on Score) | 5.0 | 4.0 | 1.25 | DEFER | V1 |
| 9 | I | **Minimum completeness thresholds** (min_steps_for_inclusion) | 3.5 | 3.0 | 1.17 | DEFER | V2 |
| 10 | G | **Gate rejection vs functional failure** (5th failure mode) | 5.0 | 5.5 | 0.91 | DEFER | V2 |
| 11 | H | **Per-step variance tracking** (StepResult dataclass) | 4.5 | 5.5 | 0.82 | DEFER | V2 |
| 12 | J | **Worktree reuse policy** (per-variant lifecycle) | 3.5 | 1.0 | 3.50 | DEFER* | V2 |

*J has high ratio but absolute value (3.5) is below the 5.0 threshold for spec changes — it is an implementation detail suitable for code comments.

---

## Recommended Spec Changes (ACCEPT tier)

### 1. C+L: Ternary Verdict Model
**What to change**: Replace `EvalReport.overall_passed: bool` with `EvalReport.verdict: str` (enum: PASS/CONDITIONAL_PASS/FAIL). Add `blocked_layers: list[str]` and `conditions: list[str]`.
**Where**: FR-EVAL.5 (compute_verdict), FR-EVAL.7 (report generation), Section 4.5 (EvalReport dataclass).
**Why strongest**: Two independent analysts (V1, V3) converged on identical solution. The v3.0 eval's headline verdict was CONDITIONAL_PASS — a concept the spec cannot represent. ABComparison already uses `verdict: str`, making EvalReport the inconsistent outlier.
**Effort**: ~18 lines across models.py, aggregator.py, reporter.py.

### 2. F: Partial Run Scoring
**What to change**: Add `steps_completed: int` and `steps_total: int` fields to `RunResult` dataclass. Add `completion_ratio` property. Aggregator includes partial runs for completed steps only.
**Where**: FR-EVAL.1 (RunResult), FR-EVAL.4 (execution engine), FR-EVAL.13 (fail-fast vs partial completion).
**Why**: All 4 eval runs were PARTIAL (9/10 and 3/8 steps). Current RunResult cannot distinguish 90% completion from 10% completion.
**Effort**: ~30 lines across models.py, aggregator.py.

### 3. K: Eval-Mode Execution
**What to change**: Add `eval_mode: bool = False` to EvalConfig. When true, gate failures are recorded but do not halt execution. Add "Deferrable in eval-mode" column to Section 5.2 Gate Criteria table.
**Where**: FR-EVAL.4 (AC bullet 7), FR-EVAL.13 (AC bullets 1-4), Section 5.2.
**Why**: Unconditional fail-fast prevented wiring-verification from executing, forcing 4 metrics to use weaker code-level evidence. This is the root cause of CONDITIONAL_PASS.
**Effort**: ~15 lines in EvalConfig + executor control flow.

### 4. B: Correct Failure Classification
**What to change**: Add `expected_gate_failures: list[str]` field to `EvalSuiteTest` in the eval suite YAML schema. Add `correct_failure: bool` to `TestVerdict`. Update fail-fast logic to consult expected failures.
**Where**: Section 5.3 (YAML schema), FR-EVAL.13 (executor), FR-EVAL.9 (suite generator).
**Why**: Spec-fidelity gate FAILED correctly (detected fabricated IDs) but is classified identically to a real defect. Eval consumers cannot distinguish intentional detection from malfunction.
**Effort**: ~50 lines across suite schema, executor, and verdict logic.

---

## Worth Considering (CONSIDER tier)

### 5. M: Auto-Detect LLM Fabrication
**What**: FR-EVAL.9 auto-generates structural test comparing requirement IDs in generated output against source spec IDs.
**Tradeoff**: Catches the dominant v3.0 failure mode automatically, but narrow applicability (only for spec-to-document pipelines). Reasonable addition to Section 7 Risk Assessment regardless.

### 6. E: Duration Variance Threshold
**What**: Add NFR-EVAL.16 with 25% variance threshold, informational only (not blocking).
**Tradeoff**: Near-zero implementation cost but weak signal from N=2. Harmless to include.

---

## Deferred (insufficient value or covered by existing spec)

| ID | Reason for Deferral |
|----|-------------------|
| D | Layer 4 regression tests with configurable thresholds already cover this |
| A | Proposal K eliminates most of the need; remaining cases are annotation-level |
| I | Proposal F + FR-EVAL.14 handle this through per-step aggregation |
| G | Pipeline-specific; L2 catches this when exit codes are correct |
| H | N=2 data insufficient to justify StepResult dataclass proliferation |
| J | Implementation detail; FR-EVAL.6 API is correctly abstract |

---

## Implementation Order (for ACCEPT proposals)

```
Phase 1 (independent, parallelizable):
  C+L: Ternary verdict model     [~18 lines, FR-EVAL.5/7, models.py]
  F:   Partial run scoring        [~30 lines, FR-EVAL.1/4, models.py]

Phase 2 (depends on C+L):
  K:   Eval-mode execution        [~15 lines, FR-EVAL.4/13, executor]

Phase 3 (depends on K):
  B:   Correct failure class.     [~50 lines, FR-EVAL.9/13, suite schema]
```

C+L and F are independent foundations. K builds on C+L (CONDITIONAL_PASS logic informs eval-mode behavior). B builds on K (expected failures interact with eval-mode gate deferral).
