---
title: "v3.0 Scoring Framework — Delta Demonstration Methodology"
version: 1.1.0
date: 2026-03-19
adversarial_review: CONDITIONAL_PASS (3 CRITICAL applied, 6 MAJOR noted)
purpose: "Quantify the v3.0 vs master delta across 3 impact areas"
authoritative: true
prompt_sequence: 5 of 6
---

# v3.0 Scoring Framework

## 1. Purpose

This framework exists to **demonstrate the delta between v3.0 and master**. It is not a generic pipeline health tool. Every metric, threshold, and scoring rule is designed to answer one question: *Does v3.0 measurably improve the pipeline compared to the codebase before these changes?*

## 2. Delta Computation Methodology

### 2.1 Run Matrix

| Run ID | Branch | Purpose |
|--------|--------|---------|
| local-A | v3.0-AuditGates | Primary measurement |
| local-B | v3.0-AuditGates | Reproducibility check (must match local-A) |
| global-A | master | Baseline measurement |
| global-B | master | Baseline reproducibility check |

### 2.2 Delta Formula

For each metric M:

```
delta(M) = local_avg(M) - global_avg(M)
```

Where:
- `local_avg(M) = (local-A[M] + local-B[M]) / 2`
- `global_avg(M) = (global-A[M] + global-B[M]) / 2`
- If only one run completed per branch: use that single value (no averaging)

### 2.3 Handling Missing v3.0 Stages on Master

Master lacks 5 stages: spec-fidelity, wiring-verification, deviation-analysis, remediate, certify.

**Scoring rule**: When a stage does not exist on master:
- The stage's artifact metrics score as `N/A (stage not available on master)` — NOT as "stage failed"
- The delta for that stage is computed as `local_value - 0` (baseline is zero capability)
- This is noted as an **asymmetric delta** in the report: the improvement is definitional, not comparative

### 2.4 Reproducibility Thresholds (SF-004 fix: differentiated by metric type)

Two reproducibility tiers based on metric determinism:

**Tier 1 — DETERMINISTIC metrics** (W-1..W-12, C-7..C-10, R-1..R-6): require **100% reproducibility** between A/B runs. These metrics measure deterministic code behavior (AST analysis, hash functions, mode enforcement). Any disagreement between runs indicates a bug, not variance.

**Tier 2 — STOCHASTIC metrics** (C-1..C-6, C-11, and any metric derived from LLM-generated artifact content): require **70% metric agreement** between A/B runs. LLM output varies inherently; the threshold acknowledges this while still detecting gross inconsistency.

Computed as:
```
reproducibility = 1 - |run_A[M] - run_B[M]| / max(run_A[M], run_B[M], 1)
```

If a DETERMINISTIC metric disagrees between A/B runs, it is flagged as **UNSTABLE** and triggers investigation (not merely excluded). If a STOCHASTIC metric falls below 70% agreement, it is flagged as **UNSTABLE** and excluded from delta scoring with the instability reported.

**Duration variance**: ≤25% between A/B runs is acceptable (LLM inference time is inherently variable).

**UNSTABLE count hard limit** (SF-011 fix): If UNSTABLE metrics exceed 20% of total metrics for a run pair, the entire run pair is invalidated and must be re-executed.

---

## 3. Metrics by Impact Area

### 3.1 Impact 1: Deterministic Wiring Verification Gate

These metrics measure whether v3.0 adds a working, structurally valid wiring verification step.

| Metric ID | Metric | Source | Type | Positive Delta Means |
|-----------|--------|--------|------|---------------------|
| W-1 | wiring-verification.md exists | artifact check | binary | v3.0 produces the artifact; master does not |
| W-2 | 16 frontmatter fields present | frontmatter parse | count (0-16) | Structural completeness of gate output |
| W-3 | Category sum consistency | `uc + om + ur == total` | binary | Deterministic analysis produces consistent counts |
| W-4 | Severity sum consistency | `critical + major + info == total` | binary | Severity classification is complete |
| W-5 | analysis_complete = true | frontmatter | binary | Analysis ran to completion |
| W-6 | rollout_mode in {shadow, soft, full} | frontmatter | binary | Mode-aware enforcement is active |
| W-7 | Report has 7 required sections | content scan | count (0-7) | Report structure matches spec |
| W-8 | .roadmap-state.json has wiring-verification step | state file | binary | Pipeline state tracking includes new step |
| W-9 | Wiring step has timing data | state file | binary | Observability of new step |
| W-10 | Detection power (files_analyzed > 0) | direct analysis | count | Analyzer actually scans code |
| W-11 | Detection power (total_findings > 0) | direct analysis | count | Analyzer detects real unwired components |
| W-12 | Scan performance < 5s | direct analysis | seconds | Deterministic analysis is fast |

**Delta interpretation for W-1 through W-9**: These are asymmetric deltas. Master has 0 for all of them (no wiring step exists). v3.0 should score 1/1 for binaries, 16/16 for W-2, 7/7 for W-7.

**Delta interpretation for W-10 through W-12**: These measure detection power against the project's own source. Master has no equivalent capability.

### 3.2 Impact 2: Convergence-Controlled Spec-Fidelity

These metrics measure whether v3.0's convergence engine produces stable, trackable deviation analysis.

| Metric ID | Metric | Source | Type | Positive Delta Means |
|-----------|--------|--------|------|---------------------|
| C-1 | spec-fidelity.md exists | artifact check | binary | Spec-fidelity gate produces output |
| C-2 | Gate fields present (6 required) | frontmatter parse | count (0-6) | Gate output is structurally complete |
| C-3 | DeviationRegistry created (convergence mode) | file check | binary | Persistent cross-run tracking works |
| C-4 | Registry schema valid | JSON parse | binary | Registry data structure is correct |
| C-5 | Registry has ≥1 run recorded | JSON parse | count | Run tracking is operational |
| C-6 | Findings have stable_id field | JSON parse | binary | Deterministic finding identification works |
| C-7 | compute_stable_id is pure | direct test | binary | Same inputs → same output (determinism) |
| C-8 | stable_id is 16-char hex | direct test | binary | Format matches sha256 truncation spec |
| C-9 | _check_regression detects structural increase | direct test | binary | Regression detection fires on structural HIGH increase |
| C-10 | _check_regression ignores semantic fluctuation | direct test | binary | Noise isolation works |
| C-11 | Structural/semantic HIGH split fields in runs | JSON parse | binary | BF-3 resolution is implemented |

**Delta interpretation**: C-1 through C-6, C-11 are asymmetric (master has no convergence engine). C-7 through C-10 test internal correctness of new code — master baseline is N/A.

### 3.3 Impact 3: Mode-Aware Rollout Enforcement

These metrics measure whether v3.0's graduated rollout (shadow/soft/full) works correctly.

| Metric ID | Metric | Source | Type | Positive Delta Means |
|-----------|--------|--------|------|---------------------|
| R-1 | Same total_findings across all 3 modes | direct analysis | binary | Detection is mode-independent |
| R-2 | Shadow blocking_findings = 0 | direct analysis | binary | Shadow mode never blocks |
| R-3 | Soft blocking = critical count | direct analysis | binary | Soft blocks on critical only |
| R-4 | Full blocking = critical + major | direct analysis | binary | Full blocks on critical + major |
| R-5 | Graduated enforcement (shadow ≤ soft ≤ full) | derived | binary | Blocking increases with enforcement level |
| R-6 | rollout_mode values correctly written | frontmatter | binary | Mode metadata is accurate |
| R-7 | GateMode.TRAILING wired in _build_steps() | code inspection | binary | Pipeline step is correctly configured |
| R-8a | wiring-verification.md contains rollout_mode field | artifact frontmatter | binary | Runtime artifact records mode metadata |
| R-8b | _build_steps() configures wiring step with GateMode.TRAILING | code inspection / dry-run | binary | Step scheduling uses correct gate mode |

**Delta interpretation**: All asymmetric. Master has no rollout modes — wiring-verification step doesn't exist.

---

## 4. Scoring Rules

### 4.1 Per-Metric Scoring

| Score | Meaning |
|-------|---------|
| 1 | Metric passes on v3.0 (positive delta over master) |
| 0 | Metric fails on v3.0 OR metric is identical to master (no delta) |
| N/A | Metric cannot be evaluated (run failed, data unavailable) |
| UNSTABLE | Metric varies between A/B runs beyond reproducibility threshold |

### 4.2 Per-Impact Scoring

```
impact_score = passing_metrics / (total_metrics - N/A_metrics - UNSTABLE_metrics)
```

Impact classification:
- **Strong positive delta**: impact_score ≥ 0.90
- **Moderate positive delta**: 0.70 ≤ impact_score < 0.90
- **Weak positive delta**: 0.50 ≤ impact_score < 0.70
- **No meaningful delta**: impact_score < 0.50
- **Negative delta**: Any metric that passes on master but fails on v3.0

### 4.3 Overall v3.0 Delta Score (SF-005 fix: per-impact floor added)

```
overall_delta = (impact_1_score + impact_2_score + impact_3_score) / 3
```

**Release quality gate** (two conditions, both required):
1. `overall_delta ≥ 0.80` (strong or moderate positive delta on average)
2. **Per-impact floor**: each individual `impact_score ≥ 0.70` (no single area allowed below "moderate positive delta")

If any impact area scores below 0.70, the release gate FAILS regardless of the overall average. This prevents one broken area from hiding behind two strong areas.

### 4.4 Regression Detection

A **regression** is any metric that:
1. Passes on global (master) runs but fails on local (v3.0) runs, OR
2. Has a numerical value that is worse on v3.0 than master (e.g., longer scan time, fewer passing pre-existing gates)

Regressions in pre-existing pipeline steps (extract through test-strategy) are scored separately from v3.0-new-step metrics because they indicate that v3.0 changes broke existing functionality.

---

## 5. Stage-Specific Scoring Procedures

### 5.1 Stages Present on Both Branches — Regression Guard (SF-001 fix)

Steps 1-8 (extract through test-strategy) exist on both branches. Their metrics are **regression detection guards**, not scored improvement areas. They verify that v3.0 changes did not break pre-existing functionality.

**Regression guard checks** (binary pass/fail, not scored in overall_delta):
1. Compare artifact existence: both branches should produce the artifact
2. Compare gate pass/fail: both should pass; if v3.0 fails where master passes, it's a **regression**
3. Compare frontmatter completeness: v3.0 should have ≥ master's field count
4. Compare wall-clock time: informational only (LLM variance expected)
5. Artifact size variance: deterministic artifacts require <5% variance; LLM artifacts use 50% as flagging threshold (informational)

**If any regression is detected**: the release gate FAILS regardless of impact scores. Regressions in pre-existing stages indicate v3.0 changes broke existing functionality.

**These metrics do NOT contribute to the overall_delta numerator.** Steps 1-8 parity is a precondition, not a scored improvement.

### 5.2 Stages New to v3.0 (Steps 9-12)

For stages that only exist on v3.0 (spec-fidelity, wiring-verification, deviation-analysis, certify):

1. Artifact existence: score as 1 if produced, 0 if missing
2. Structural validity: score via impact-specific metrics above
3. **Do not compare to master** — master has no baseline for these stages
4. Score as "v3.0 adds N new pipeline capabilities" in the delta report

### 5.3 Pipeline-Level Metrics

| Metric | Computation | Threshold |
|--------|------------|-----------|
| Total stages completed | count of artifacts produced | v3.0 should complete ≥ 10 stages; master ≥ 8 |
| Total pipeline wall-clock | sum of step durations | Informational (no threshold; LLM variance dominates) |
| Gate pass rate | passing gates / total gates | v3.0 ≥ 0.90; master ≥ 0.90 for its stages |
| Artifact provenance | all artifact mtimes post-date eval start | Must be 100% for run validity |

---

## 6. Reproducibility Assessment

### 6.1 Run-to-Run Consistency

For each branch, compare A vs B runs:

| Check | Method | Threshold |
|-------|--------|-----------|
| Artifact set match | Same files produced in A and B | 100% (any missing file = FAIL) |
| Gate verdict match | Same pass/fail on each gate | 100% (any verdict flip = UNSTABLE) |
| Frontmatter value match | Numeric frontmatter values within 10% | 90% of fields must match |
| Duration variance | `abs(A - B) / max(A, B)` | ≤ 25% |

### 6.2 Stability Classification

| Classification | Criteria |
|---------------|----------|
| DETERMINISTIC | All checks pass, duration variance ≤ 10% |
| STABLE | All checks pass, duration variance ≤ 25% |
| VARIABLE | 1-2 metric disagreements between A/B |
| UNSTABLE | ≥3 metric disagreements or missing artifacts |

---

## 7. Human Evaluator Instructions

### 7.1 Pre-Scoring Checklist

1. Verify all run directories exist: `eval-runs/{local-A, local-B, global-A, global-B}`
2. Verify artifact provenance: file mtimes must post-date the eval start timestamp
3. Verify no file copying: compare file hashes between local-A and local-B (must differ for LLM-generated content; must match for deterministic content like wiring-verification)
4. Read pipeline-stdout.log and pipeline-stderr.log for error indicators

### 7.2 Scoring Process

1. **Automated scoring first**: Run the scoring script (to be generated in Prompt 6) against all 4 run directories
2. **Manual review of flagged items**: Any metric scored UNSTABLE or any regression requires human review
3. **Spot-check 3 random metrics**: Pick 3 metrics at random, verify the automated score against the actual artifact content
4. **Sign-off**: Human evaluator confirms overall delta score and any regressions noted

### 7.3 Escape Hatch Detection

The following patterns indicate invalid eval data:

| Escape Hatch | Detection Method |
|-------------|-----------------|
| Potemkin pipeline | Verify eval-spec.md has real functional requirements (>10), not trivial placeholders |
| Copy-paste artifacts | Compare file hashes: local-A vs local-B must differ for LLM artifacts, match for deterministic ones |
| Checkpoint evals | Verify all 10+ stages ran; check pipeline-stdout.log for "step skipped" or "resume" indicators |
| Warm-cache evals | Verify run durations are >60s for LLM stages (cache hits would be nearly instant) |
| Timing-only deltas | This framework measures structural presence, not just timing — timing is informational only |

---

## 8. Troubleshooting Guide

### 8.1 Negative Delta

If v3.0 scores lower than master on any pre-existing stage:

1. Read the pipeline-stderr.log for the failing stage
2. Check if the failure is in a new gate's semantic check (possible false positive)
3. Verify the eval-spec.md wasn't modified between runs
4. Check for import errors from new v3.0 modules that could affect existing stages
5. Run `uv run superclaude roadmap run <spec> --dry-run` on both branches — compare step definitions

### 8.2 Inconsistent Deltas (A/B Disagreement)

If local-A and local-B produce different results:

1. For LLM-generated artifacts: this is expected — check if the *gate verdicts* match, not the content
2. For deterministic artifacts (wiring-verification): content MUST match. If not, check for race conditions or stale imports
3. For frontmatter values: check if LLM-generated frontmatter has numeric variance (common for complexity_score, convergence_score)

### 8.3 Global Run Failures

If global runs fail entirely:

1. Verify the worktree was created correctly: `git worktree list`
2. Verify `superclaude` is installed in the worktree: `uv pip install -e .` in worktree dir
3. Verify the eval-spec.md is accessible from the worktree
4. If master's pipeline has fewer stages, verify the failure is in a step that master should support

### 8.4 Partial Run Recovery

If a run fails partway through:

1. Record which stages completed (from .roadmap-state.json or artifact existence)
2. Score only the completed stages; mark incomplete stages as N/A
3. If ≥8 stages completed (all pre-existing stages), the run is usable for master-equivalent comparison
4. If <8 stages completed, the run should be discarded and re-attempted

---

## 9. Output Format

The scoring report (Prompt 6) must produce:

```yaml
overall_delta_score: <float 0.0-1.0>
release_quality_gate: PASS|FAIL
impact_scores:
  wiring_verification: <float>
  convergence_spec_fidelity: <float>
  rollout_enforcement: <float>
regressions: <list of metric IDs that regressed>
unstable_metrics: <list of metric IDs flagged UNSTABLE>
reproducibility:
  local: <DETERMINISTIC|STABLE|VARIABLE|UNSTABLE>
  global: <DETERMINISTIC|STABLE|VARIABLE|UNSTABLE>
asymmetric_deltas: <count of metrics where master has no baseline>
run_summary:
  local_A: {status, stages_completed, duration_s, artifact_count}
  local_B: {status, stages_completed, duration_s, artifact_count}
  global_A: {status, stages_completed, duration_s, artifact_count}
  global_B: {status, stages_completed, duration_s, artifact_count}
```
