---
title: "Adversarial Review: v3.0 Scoring Framework"
date: 2026-03-19
reviewer: adversarial-agent
subject: scoring-framework.md v1.0.0
verdict: CONDITIONAL_PASS
total_findings: 14
critical: 3
major: 6
minor: 5
---

# Adversarial Review: v3.0 Scoring Framework

## Debate Structure

Four questions were evaluated against the scoring framework (`scoring-framework.md`), the merged specification (`merged-spec.md`), the eval specification (`eval-spec.md`), and three implementation files (`executor.py`, `gates.py`, `convergence.py`).

---

## Q1: Does the framework measure v3.0 changes specifically, or generic pipeline health?

### FINDING SF-001
- **FINDING_ID**: SF-001
- **SEVERITY**: CRITICAL
- **Question**: Q1
- **Description**: The stage-specific scoring procedures in Section 5.1 (Steps 1-8) measure generic pipeline health, not v3.0 delta. Metrics like "artifact existence," "artifact size within 30%," "gate pass/fail," and "frontmatter completeness" would pass identically on a pre-v3.0 codebase. Steps 1-8 (extract through test-strategy) exist on both branches and use identical gates (`EXTRACT_GATE`, `GENERATE_A_GATE`, etc. in `gates.py`). A pre-v3.0 codebase that passes these gates would score identically on all Section 5.1 metrics, producing a zero delta that contributes nothing to the overall score but still occupies one-third of the denominator in the impact formula.
- **Evidence**: `gates.py` lines 647-804 define the same gate criteria for steps 1-8 regardless of branch. The scoring framework Section 5.1 checks "compare artifact existence," "compare artifact size," "compare gate pass/fail" -- all of which are branch-agnostic.
- **Impact**: The overall_delta formula (Section 4.3) averages three impact scores, but only Impacts 1-3 (W, C, R metrics) actually measure v3.0 changes. Steps 1-8 comparison dilutes the signal. If steps 1-8 produce identical results on both branches (expected), the pipeline-level metrics in Section 5.3 add noise without information.
- **Recommended Fix**: Reclassify Section 5.1 metrics as "regression detection" (binary pass/fail guard), not as a scored impact area. They should not contribute to the overall_delta numerator. The framework should explicitly state: "Steps 1-8 parity is a precondition, not a scored improvement."

### FINDING SF-002
- **FINDING_ID**: SF-002
- **SEVERITY**: MAJOR
- **Question**: Q1
- **Description**: 26 of 31 metrics (W-1..W-12, C-1..C-11, R-1..R-3) are asymmetric deltas where master baseline is zero or N/A. The framework acknowledges this in Sections 3.1-3.3 ("Delta interpretation: asymmetric") but then feeds these into the same `impact_score = passing / total` formula as comparative metrics. An asymmetric delta is not a delta at all -- it is a feature existence check. Calling `1 - 0 = 1` a "positive delta" is tautological for any new feature that works.
- **Evidence**: Section 2.3 states: "delta for that stage is computed as `local_value - 0`." Section 3.1 states: "These are asymmetric deltas. Master has 0 for all of them."
- **Impact**: The framework claims to measure improvement but actually measures feature completeness. A release could have a broken convergence engine (C-7 through C-10 all fail) and still pass the overall gate at 0.80 if W and R impacts are strong. The framework conflates "feature exists" with "feature improves the pipeline."
- **Recommended Fix**: Split the scoring into two layers: (1) Feature Completeness Gate (all asymmetric metrics must pass at >= 0.90) as a binary precondition, and (2) True Delta Score (only metrics where master has a nonzero baseline contribute to the delta). The overall release gate should require both to pass.

### FINDING SF-003
- **FINDING_ID**: SF-003
- **SEVERITY**: MINOR
- **Question**: Q1
- **Description**: Metrics R-7 ("GateMode.TRAILING wired in _build_steps()") and R-8 ("Pipeline output references trailing/shadow") are code inspection metrics, not runtime behavior metrics. They test that source code contains specific patterns, which is a static analysis concern already covered by the wiring-verification gate itself. Including them in the scoring framework creates circular validation: the scoring framework measures whether the feature being scored (wiring verification) is correctly wired.
- **Evidence**: `executor.py` line 537 shows `gate_mode=GateMode.TRAILING` is statically set. R-7 checks this same line. R-8 checks stdout, which is produced by the step that R-7 already validates.
- **Recommended Fix**: Keep R-7 and R-8 as informational diagnostics but exclude from the scored impact. The wiring gate's own self-consistency is better validated by W-3 through W-6.

---

## Q2: Are the thresholds defensible?

### FINDING SF-004
- **FINDING_ID**: SF-004
- **SEVERITY**: CRITICAL
- **Question**: Q2
- **Description**: The 85% reproducibility threshold (Section 2.4) is not calibrated against actual LLM variance data. The formula `1 - |run_A[M] - run_B[M]| / max(run_A[M], run_B[M], 1)` is a relative difference metric, but the 85% cutoff is stated without justification. For binary metrics (W-1 through W-9, most C and R metrics), reproducibility is either 100% (both agree) or 0% (they disagree). There is no granularity at which 85% is meaningful for binary metrics. For count metrics (W-2, W-7, W-10, W-11), the 85% threshold means a difference of 2 out of 16 fields (W-2) is acceptable, which could mask a real structural bug.
- **Evidence**: Section 2.4 formula applied to W-2: if run_A reports 16/16 frontmatter fields and run_B reports 14/16, reproducibility = `1 - 2/16 = 0.875 > 0.85`, so this passes. But 2 missing frontmatter fields could indicate a broken emitter.
- **Impact**: The threshold is simultaneously too tight for stochastic metrics (LLM-generated content varies substantially) and too loose for deterministic metrics (wiring analysis should be 100% reproducible). A single threshold for both classes creates false confidence.
- **Recommended Fix**: Define two reproducibility tiers: (1) DETERMINISTIC metrics (W-1..W-12, C-7..C-10, R-1..R-5) require 100% reproducibility; (2) STOCHASTIC metrics (LLM-generated artifact content) require 70% metric agreement with a variance report. Document the rationale for each threshold with reference to measured variance from shadow-mode data.

### FINDING SF-005
- **FINDING_ID**: SF-005
- **SEVERITY**: CRITICAL
- **Question**: Q2
- **Description**: The 0.80 overall_delta gate (Section 4.3) uses an unweighted average of three impact scores. This means a release with Impact 1 (Wiring) = 1.0, Impact 2 (Convergence) = 1.0, Impact 3 (Rollout) = 0.40 yields `overall_delta = 0.80`, which passes. But Impact 3 at 0.40 means "no meaningful delta" per Section 4.2's own classification. A release where rollout enforcement shows "no meaningful delta" should not pass the quality gate.
- **Evidence**: Section 4.2 classifies `impact_score < 0.50` as "No meaningful delta." Section 4.3 allows `overall_delta >= 0.80` to pass. The math permits one impact area to show no meaningful improvement while the overall gate passes.
- **Impact**: The convergence engine could be completely broken (C-7..C-10 all fail, bringing Impact 2 below 0.50) and the release could still ship if wiring and rollout are strong. This defeats the purpose of measuring three independent impact areas.
- **Recommended Fix**: Add a per-impact floor: each impact area must individually score >= 0.70 ("moderate positive delta") AND the overall average must be >= 0.80. This prevents any single area from being dead weight.

### FINDING SF-006
- **FINDING_ID**: SF-006
- **SEVERITY**: MAJOR
- **Question**: Q2
- **Description**: The 30% artifact size variance threshold (Section 5.1) is stated without empirical basis. For LLM-generated artifacts like `debate-transcript.md` or `roadmap.md`, size variance of 50-100% between runs is common due to prompt sensitivity and model temperature. For deterministic artifacts like `wiring-verification.md`, size variance should be < 5%. The single 30% threshold is neither calibrated nor differentiated by artifact type.
- **Evidence**: Section 5.1 item 2: "Compare artifact size: +/-30% is acceptable variance; >30% flags for review." No data source, no empirical measurement, no differentiation between deterministic and LLM-generated artifacts.
- **Recommended Fix**: Split artifact size checks: deterministic artifacts (wiring-verification.md) require < 5% size variance; LLM artifacts use 50% as the flagging threshold (informational, not scored). Document that these thresholds will be calibrated against shadow-mode data during Phase 1.

---

## Q3: Can this framework distinguish v3.0 improvement from LLM variance?

### FINDING SF-007
- **FINDING_ID**: SF-007
- **SEVERITY**: MAJOR
- **Question**: Q3
- **Description**: The A/B run design (Section 2.1) uses only 2 runs per branch (N=2). With N=2, you cannot compute standard deviation, confidence intervals, or statistical significance. The delta between branches could be entirely due to LLM variance. For metrics like C-2 (gate fields present) where the LLM generates the frontmatter, a single unlucky run could flip the score.
- **Evidence**: Section 2.1 defines 4 total runs (2 per branch). Section 2.2 computes averages: `local_avg = (local-A + local-B) / 2`. With N=2, the standard error of the mean is `sigma / sqrt(2)`, which is barely better than a single run.
- **Impact**: The framework cannot distinguish a 0.05 delta from noise. If the true improvement is 0.10 but LLM variance contributes +/- 0.15, the measured delta could be negative despite a real improvement.
- **Recommended Fix**: Either (a) increase to N=5 runs per branch (10 total), which allows t-test significance testing at p<0.05, or (b) explicitly acknowledge that N=2 provides "directional evidence only, not statistical proof" and drop claims of quantitative rigor. If cost prohibits N=5, state the power limitation in the report preamble.

### FINDING SF-008
- **FINDING_ID**: SF-008
- **SEVERITY**: MAJOR
- **Question**: Q3
- **Description**: The framework does not separate deterministic and stochastic metrics in its scoring. Metrics W-1 through W-12 and R-1 through R-5 are deterministic (AST analysis, code inspection). Metrics C-1 through C-6 involve LLM-generated artifacts where stochastic variance is inherent. Mixing them in a single `impact_score` formula means a stochastic failure can mask deterministic success and vice versa.
- **Evidence**: `convergence.py` line 24-32 shows `compute_stable_id` is purely deterministic (SHA-256 hash). But C-1 and C-2 depend on LLM-generated `spec-fidelity.md` artifact existence and frontmatter, which is stochastic. These are averaged together in Impact 2's score.
- **Recommended Fix**: Within each impact area, report deterministic and stochastic sub-scores separately. The release gate should require deterministic sub-score >= 0.95 (near-perfect for things that should never vary) and stochastic sub-score >= 0.70 (acknowledging inherent variance).

### FINDING SF-009
- **FINDING_ID**: SF-009
- **SEVERITY**: MINOR
- **Question**: Q3
- **Description**: Metric C-10 ("_check_regression ignores semantic fluctuation") tests a code behavior, not a pipeline outcome. It verifies that `convergence.py:_check_regression()` returns False when semantic HIGH count changes. This is a unit test masquerading as an eval metric. Unit tests belong in `tests/roadmap/test_convergence.py`, not in the scoring framework.
- **Evidence**: `convergence.py` lines 240-272: `_check_regression()` only triggers on structural HIGH increases. C-10 tests this exact behavior. This is already tested (or should be) by unit tests.
- **Recommended Fix**: Move C-9 and C-10 to the test suite. Replace with pipeline-observable metrics: e.g., "deviation-registry.json shows structural HIGH count is monotonically non-increasing across consecutive pipeline runs."

---

## Q4: Is the troubleshooting path actionable?

### FINDING SF-010
- **FINDING_ID**: SF-010
- **SEVERITY**: MAJOR
- **Question**: Q4
- **Description**: Section 8.1 (Negative Delta) troubleshooting has 5 steps but no decision tree. Step 2 says "Check if the failure is in a new gate's semantic check (possible false positive)" but does not explain how to distinguish a false positive from a real regression. The guide assumes the evaluator already understands the gate architecture. For a third-party evaluator (which the eval-spec requires), these steps are insufficient.
- **Evidence**: Section 8.1 steps are linear (do step 1, then 2, then 3...) rather than branching (if X, do Y; if not X, do Z). Step 3 ("Verify the eval-spec.md wasn't modified between runs") has no method -- how does the evaluator verify this? File hash comparison is not mentioned.
- **Recommended Fix**: Convert Section 8.1 into a decision tree with explicit branch conditions. Add file hash verification commands (e.g., `sha256sum eval-spec.md` before and after runs). Add a "root cause categories" table mapping symptoms to likely causes.

### FINDING SF-011
- **FINDING_ID**: SF-011
- **SEVERITY**: MINOR
- **Question**: Q4
- **Description**: The escape hatch detection table (Section 7.3) is missing two significant escape hatches. (1) **Selective metric reporting**: the evaluator could omit UNSTABLE metrics to inflate the overall score, since Section 4.2 excludes N/A and UNSTABLE from the denominator. (2) **Pre-seeded worktree**: the global (master) worktree could be set up with cached Claude responses, making master runs artificially fast and potentially producing different artifacts than a clean run.
- **Evidence**: Section 4.2 formula: `impact_score = passing / (total - N/A - UNSTABLE)`. If an evaluator marks inconvenient metrics as UNSTABLE, the denominator shrinks and the score inflates. Section 7.3 has no detection method for denominator manipulation.
- **Recommended Fix**: Add: (1) "UNSTABLE count exceeding 20% of total metrics invalidates the eval run" as a hard constraint. (2) "Verify global worktree has no pre-existing artifacts: `ls eval-runs/global-A/` should be empty before run start." (3) "Report UNSTABLE metric IDs and justification in the scoring report."

### FINDING SF-012
- **FINDING_ID**: SF-012
- **SEVERITY**: MAJOR
- **Question**: Q4
- **Description**: Section 8.2 (Inconsistent Deltas) item 2 states: "For deterministic artifacts (wiring-verification): content MUST match. If not, check for race conditions or stale imports." But the framework provides no diagnostic tooling for this. The evaluator is told to "check for race conditions" without being given a method. In `executor.py` lines 244-259, the wiring verification runs `run_wiring_analysis()` which depends on `WiringConfig(rollout_mode="soft")` and `config.output_dir.parent` -- both of which could differ between A/B runs if the output directories are misconfigured.
- **Evidence**: `executor.py` line 248: `wiring_config = WiringConfig(rollout_mode="soft")` is hardcoded. Line 249: `source_dir = config.output_dir.parent if hasattr(config, 'output_dir') else Path(".")`. The fallback to `Path(".")` could cause different scan targets between runs.
- **Recommended Fix**: Add diagnostic commands to Section 8.2: (1) `diff eval-runs/local-A/wiring-verification.md eval-runs/local-B/wiring-verification.md` to pinpoint differences. (2) Verify `source_dir` resolution by logging it in the wiring step output. (3) Add `source_dir` to the wiring-verification frontmatter so evaluators can confirm both runs scanned the same directory.

### FINDING SF-013
- **FINDING_ID**: SF-013
- **SEVERITY**: MINOR
- **Question**: Q4
- **Description**: The warm-cache escape hatch (Section 7.3) uses ">60s for LLM stages" as the detection threshold, but this is not justified. Claude API response times can vary from 10s to 300s depending on prompt length and server load. A 45s response is not necessarily a cache hit, and a 90s response is not necessarily cold. The threshold is arbitrary and could produce false positives (flagging legitimate fast runs) or false negatives (missing sophisticated caching).
- **Recommended Fix**: Replace the absolute 60s threshold with a relative check: "LLM stage durations should be within 3x of each other across runs. If any stage is more than 3x faster than the same stage on the other branch, flag for cache investigation." This is relative to the run's own performance baseline, not an arbitrary absolute.

### FINDING SF-014
- **FINDING_ID**: SF-014
- **SEVERITY**: MINOR
- **Question**: Q1/Q4
- **Description**: The scoring framework references "Prompt 6" for the scoring script (Sections 1, 9) but Prompt 6 does not exist yet. The framework is therefore incomplete -- it defines what to measure but not how to automate the measurement. Without the scoring script, all 31 metrics must be manually evaluated, which is error-prone and defeats the reproducibility goal.
- **Recommended Fix**: Either (a) ship the scoring script alongside the framework, or (b) add explicit manual evaluation procedures for each metric with exact commands/queries the evaluator should run. The current state leaves the framework as a design document rather than an operational tool.

---

## Summary Table

| ID | Severity | Question | Title |
|----|----------|----------|-------|
| SF-001 | CRITICAL | Q1 | Steps 1-8 metrics measure generic health, not v3.0 delta |
| SF-002 | MAJOR | Q1 | Asymmetric deltas conflate feature existence with improvement |
| SF-003 | MINOR | Q1 | R-7/R-8 create circular validation with wiring gate |
| SF-004 | CRITICAL | Q2 | 85% reproducibility threshold is uncalibrated and undifferentiated |
| SF-005 | CRITICAL | Q2 | 0.80 overall gate allows one impact area to show no meaningful delta |
| SF-006 | MAJOR | Q2 | 30% artifact size variance is empirically unjustified |
| SF-007 | MAJOR | Q3 | N=2 runs per branch insufficient for statistical significance |
| SF-008 | MAJOR | Q3 | Deterministic and stochastic metrics mixed in single score |
| SF-009 | MINOR | Q3 | C-9/C-10 are unit tests, not eval metrics |
| SF-010 | MAJOR | Q4 | Troubleshooting guide lacks decision tree and diagnostic commands |
| SF-011 | MINOR | Q4 | Missing escape hatches: denominator manipulation, pre-seeded worktree |
| SF-012 | MAJOR | Q4 | Deterministic artifact mismatch has no diagnostic tooling |
| SF-013 | MINOR | Q4 | Warm-cache 60s threshold is arbitrary |
| SF-014 | MINOR | Q1/Q4 | Scoring script (Prompt 6) does not exist; framework is design-only |

## Verdict

**CONDITIONAL_PASS**: The framework's structure is sound and the metric selection covers the three v3.0 impact areas comprehensively. However, three critical findings must be addressed before the framework can be used for a real release gate:

1. **SF-001/SF-002**: The scoring formula must separate feature-existence checks from true comparative deltas. Currently, a tautological "new feature exists" score inflates the delta.
2. **SF-004**: Reproducibility thresholds must be differentiated by metric type (deterministic vs. stochastic).
3. **SF-005**: A per-impact floor must be added to prevent one broken area from hiding behind two strong areas.

The six MAJOR findings should be addressed but are not blocking -- they reduce confidence in the scoring results but do not invalidate the framework's core approach.
