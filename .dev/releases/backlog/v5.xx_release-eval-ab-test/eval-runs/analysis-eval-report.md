# Analysis: v3.0 Eval Scoring Report

**Source file**: `eval-runs/eval-report.md`
**Analyzed against**: `release-eval-spec.md` (v1.0.0)
**Date**: 2026-03-19

---

## 1. Key Findings from the Eval Report

### Finding 1: Code-Level Evidence Substitution Was Necessary and Widespread

The wiring-verification step (W-1, W-8, W-9) never executed in the pipeline because spec-fidelity blocked it. The eval scored these metrics using direct code analysis (`run_wiring_analysis()`, `emit_report()`) rather than pipeline execution artifacts. This was permitted under the scoring framework's Section 5.2, but represents a fundamentally different evidence tier than what the spec assumes.

### Finding 2: Cascading Gate Failure Created an Unscored Pipeline Tail

Spec-fidelity's correct detection of fabricated requirement IDs (3 HIGH deviations in both local runs) blocked the final pipeline step. The eval handled this gracefully -- scoring it as "feature working as designed" -- but the release-eval-spec has no mechanism for distinguishing "gate failure that proves the gate works" from "gate failure that indicates a defect." The CONDITIONAL_PASS verdict was an ad-hoc invention not defined in any scoring schema.

### Finding 3: Asymmetric Deltas Dominated (31 of 31 Metrics)

Every single scored metric was an asymmetric delta -- master had no baseline for any v3.0 capability. The eval's delta formula (`local_avg(M) - global_avg(M)`) with "baseline is zero when stage does not exist on master" meant the comparison was effectively "does this feature exist and work?" rather than "did this feature improve?"

### Finding 4: Tiered Reproducibility Worked Well

The DETERMINISTIC/STOCHASTIC tier split (Tier 1 requiring 100% agreement, Tier 2 requiring 70%) produced clean results: all deterministic metrics were 100% reproducible via direct code execution, all stochastic metrics agreed between A/B pairs. Zero UNSTABLE metrics out of 31.

### Finding 5: Master Branch Failure Asymmetry

Master's pipeline failed at step 2 (generate-opus produced 9-11 lines vs 100-line minimum), completing only 3 of 8 steps. This made steps 4-8 incomparable. The eval correctly noted this is a positive delta for v3.0, not a regression, but the spec has no framework for handling "baseline branch is broken."

---

## 2. Insights That Impact the Release-Eval-Spec

### Insight A: The Spec Needs a "Code-Level Evidence" Tier in the Failure Model

**What was observed**: 3 of 12 wiring metrics (W-1, W-8, W-9) and the R-8 rollout metric could not be scored from pipeline execution because an upstream gate blocked the step. The eval fell back to code analysis (inspecting `_build_steps()`, calling `emit_report()` directly, verifying timing infrastructure exists). This produced valid evidence but at a weaker confidence level than pipeline execution artifacts.

**Affected sections**: Section 2 (Solution Overview -- 4-layer failure model), Section 5.2 (Gate Criteria), FR-EVAL.14 (Asymmetric Stage Handling).

**Specific change warranted**: The 4-layer failure model (structural/functional/quality/regression) should add an explicit "evidence tier" axis orthogonal to the layers. When a pipeline step is defined but unreachable due to upstream gate failure, the system should:
1. Distinguish "code-level evidence" (function exists, can be invoked in isolation) from "pipeline-level evidence" (step executed in context, artifacts produced).
2. Report both the metric score AND the evidence tier in `scores.jsonl`.
3. Allow a CONDITIONAL_PASS verdict when all metrics pass but some are scored at a lower evidence tier.

This is not just about asymmetric stages (FR-EVAL.14 handles stages that don't exist on one branch). This is about stages that exist on the candidate but were never reached during execution. FR-EVAL.14 addresses structural absence; this addresses runtime unreachability.

### Insight B: The Spec Needs a "Correct Failure" Classification

**What was observed**: The spec-fidelity gate FAILED on both local runs -- and this was the desired outcome. The LLM fabricated requirement IDs, the gate detected them, the pipeline halted. The eval report explicitly states "This is a feature demonstrating its value. The spec-fidelity gate found real problems." But the release-eval-spec's 4-layer model treats all failures as negatives. There is no concept of a "correct failure" -- a gate failing because it successfully detected a problem it was designed to detect.

**Affected sections**: Section 5.2 (Gate Criteria -- enforcement tiers), FR-EVAL.13 (Release Eval Executor -- fail-fast behavior), FR-EVAL.14 (Asymmetric Stage Handling).

**Specific change warranted**: Add a `correct_failure` classification to the gate/layer system. When a gate fails and the failure matches a known-seeded or known-expected defect in the test input:
1. The failure should be scored as a PASS for the gate's detection capability.
2. The downstream steps blocked by the failure should be annotated as "blocked by correct gate enforcement" rather than "failed" or "skipped."
3. The eval suite YAML schema (Section 5.3) should support an `expected_gate_failures` field that declares which gates are expected to fail for a given test input, so the system can distinguish expected from unexpected failures.

This directly affects the `EvalSuiteTest` dataclass in Section 4.5 -- it needs an `expected_failures` field.

### Insight C: The CONDITIONAL_PASS Verdict Needs Formal Definition

**What was observed**: The eval report invented a `CONDITIONAL_PASS` verdict with three explicit conditions for upgrading to full PASS. The release-eval-spec defines only PASS/FAIL verdicts via `compute_verdict()` in FR-EVAL.5 and the gate criteria in Section 5.2. There is no intermediate verdict, no conditions-for-upgrade mechanism, and no way to express "passes with caveats."

**Affected sections**: FR-EVAL.5 (Statistical Aggregation -- `compute_verdict()`), FR-EVAL.7 (Report Generation), Section 4.5 (data models -- `EvalReport` and `ABComparison`).

**Specific change warranted**: Define a three-tier verdict system: `PASS`, `CONDITIONAL_PASS`, `FAIL`. The `EvalReport` dataclass should include:
- `verdict: str` expanded from `{PASS, FAIL}` to `{PASS, CONDITIONAL_PASS, FAIL}`
- `conditions: list[str]` -- empty for PASS/FAIL, populated for CONDITIONAL_PASS with specific upgrade requirements
- `compute_verdict()` logic: PASS when all metrics pass at pipeline-level evidence; CONDITIONAL_PASS when all metrics pass but some use code-level evidence or N/A exclusions; FAIL when any metric fails.

### Insight D: The Regression Guard Pattern Needs Codification

**What was observed**: The eval report (Section 1) treats steps 1-8 as "regression detection guards" that are explicitly excluded from the impact delta numerator. They exist solely to verify that pre-existing functionality didn't break. This is a fundamentally different scoring mode than the 5-dimension rubric scoring the spec defines. The eval handled this with a binary PASS/regression table per step -- no rubric scores, no judge agent, no multi-run aggregation.

**Affected sections**: FR-EVAL.14 (Asymmetric Stage Handling), FR-EVAL.5 (Statistical Aggregation), the 4-layer failure model (Section 2).

**Specific change warranted**: FR-EVAL.14 currently handles the "new capability" side of asymmetric comparison but does not address the "regression guard" side. When a stage exists on both branches, the system should support a binary regression-guard scoring mode (PASS/NO REGRESSION/REGRESSION) alongside the rubric-scored quality mode. This is distinct from the regression layer (Layer 4) in the 4-layer model, which uses p-values and effect sizes. Regression guards are simpler: did the step that passed before still pass? No statistical apparatus needed.

Add to `EvalSuiteTest` config:
```yaml
scoring_mode: "rubric" | "regression_guard"
```

When `scoring_mode: regression_guard`, the runner skips judge invocation and scores purely on step pass/fail consistency between baseline and candidate.

### Insight E: Duration Variance Thresholds Need Specification

**What was observed**: The eval report uses a 25% duration variance threshold (Section 1.3) to flag timing outliers between A/B runs. Global generate-opus hit 28% variance. The release-eval-spec mentions wall_time_seconds in RunResult (FR-EVAL.1) and per-run execution time limits (NFR-EVAL.14) but has no concept of within-pair duration variance as a reproducibility signal.

**Affected sections**: FR-EVAL.5 (Statistical Aggregation -- `check_consistency()`), NFR-EVAL.3 (Within-model variance targets CV < 0.15 for scores, but nothing for timing).

**Specific change warranted**: Add a duration variance check to `check_consistency()` alongside the score CV check. Suggested threshold: 25% wall-clock variance between A/B pair runs of the same step flags as "informational" (not blocking). This is lower priority than Insights A-D because timing variance is informational, but it provides useful reproducibility signal for eval consumers. Add to NFR table:

`NFR-EVAL.16 | Within-pair duration variance | < 25% per step | wall_time_seconds comparison between A/B pair runs`

---

## 3. Insights That Do NOT Warrant Spec Changes

### Observation 1: All Metrics Were Asymmetric (31/31)

While notable, this is a property of the v3.0 release being evaluated (it adds entirely new capabilities), not a gap in the release-eval-spec. The spec's FR-EVAL.14 already handles asymmetric stages correctly. A release with mixed symmetric and asymmetric stages would exercise both paths. No spec change needed -- the spec anticipated this; it just happened that v3.0 is a pure-additive release.

### Observation 2: LLM Prompt Quality Caused Spec-Fidelity Failures

The fabricated requirement IDs are a real problem but are a property of the roadmap CLI's prompt templates, not the eval framework. The eval correctly detected and reported this. The release-eval-spec does not need to account for "LLM generates bad content" -- that is the domain of the pipeline being evaluated, not the evaluator.

### Observation 3: Generate-Opus Master Failure (9-11 Lines)

Master's generate-opus step producing trivially small output is a pre-existing defect on master, not a gap in the eval spec. The spec's asymmetric handling (FR-EVAL.14) would classify this as "baseline failed, candidate passed = improvement." No spec change needed.

### Observation 4: Zero UNSTABLE Metrics

The 20% UNSTABLE threshold from the scoring framework (SF-011) was never tested because no metrics were unstable. This is good news for the framework but provides no signal about whether the threshold is correctly calibrated. The release-eval-spec's NFR-EVAL.3 (CV < 0.15) is a reasonable parallel. No spec change needed -- absence of instability is not a design flaw.

### Observation 5: Escape Hatch Detection Passed Cleanly

The 5 escape-hatch checks (Potemkin pipeline, copy-paste artifacts, checkpoint evals, warm-cache evals, timing-only deltas) all passed. These are useful sanity checks but are specific to the v3.0 scoring framework. The release-eval-spec's structural layer (L1) and NFR-EVAL.9 (artifact provenance) cover similar ground. Duplicating the escape-hatch checklist would add spec bloat without adding capability.

### Observation 6: Debate Step Had Borderline Duration Variance (28%)

Local debate step had 70s vs 97s (28% variance), just over the 25% threshold. This is informational noise for a single step in a single run pair. While Insight E above recommends adding duration variance tracking to the spec, this specific data point does not indicate a systemic problem.
