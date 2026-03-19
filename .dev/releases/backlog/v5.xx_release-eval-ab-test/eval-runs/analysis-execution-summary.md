# Analysis: Execution Summary

**Source**: `eval-runs/execution-summary.md`
**Analyst**: Claude Opus 4.6
**Date**: 2026-03-19

---

## 1. Key Findings

### F1: 50% of runs terminated early, but all produced usable partial data
All 4 runs were marked PARTIAL. Local runs completed 9/10 steps; global runs completed 3/8 steps. Despite this, the eval extracted meaningful signal from every run -- partial runs are the norm, not the exception, in real pipeline evals.

### F2: Global runs fail deterministically at generate-opus due to prompt quality regression
Both global runs failed identically: opus-architect produced 9-11 lines instead of the required 100+ minimum. Haiku-architect succeeded on both branches. This is a genuine regression signal -- master's prompts produce summaries while v3.0's prompts produce full roadmaps (182-208 lines).

### F3: Spec-fidelity gate blocks reproducibly across paired runs
Both local runs failed at spec-fidelity with identical verdicts (high_severity_count_zero semantic check). The failure reason was fabricated requirement IDs and missing spec references in the LLM-generated roadmap -- a real quality defect, not a flaky gate.

### F4: Duration variance within pairs is 6-39%, with debate step as the outlier
Most steps show <15% variance between A/B pairs. The debate step (70s vs 97s = 28% variance in local, and generate-opus at 28% in global) are the highest-variance steps, both involving multi-turn LLM interaction.

### F5: Artifact size variance is substantial even when verdicts match
Local-A and Local-B produce identical gate verdicts but debate-transcript.md varies from 9,603 to 14,224 bytes (48% size difference). Haiku-architect varies from 18,352 to 13,565 bytes (35%). Verdict reproducibility does not imply content reproducibility.

---

## 2. Insights That Impact the Release-Eval Spec

### I1: The spec needs a "partial run scoring" strategy

**Observed**: All 4 runs were PARTIAL. Global runs produced only 3/8 stages. The eval still extracted useful signal from every run. The execution summary explicitly notes that partial data is scoreable ("W-10 through W-12 can be scored via direct analysis").

**Affected sections**: FR-EVAL.4 (Multi-Run Parallel Execution Engine), FR-EVAL.13 (Release Eval Executor), FR-EVAL.14 (Asymmetric Stage Handling)

**Spec change warranted**: FR-EVAL.4 assumes runs either complete or fail. Add an AC: "Partial runs (N of M steps completed) produce RunResult with `steps_completed` and `steps_total` fields. Partial runs are included in aggregation for completed steps, not discarded." FR-EVAL.13's fail-fast logic (Layer 1 failure halts Layer 2) should be distinguished from within-layer partial completion -- a run that completes 9/10 pipeline steps is not a "failed run" in the same sense as a structural test failure. FR-EVAL.14 already handles missing stages across branches but not missing stages within a single run due to internal gate failure.

### I2: The 4-layer failure model needs a "prompt quality" sub-layer

**Observed**: Global runs failed at generate-opus because master's prompt template produced 10-line summaries instead of full roadmaps. This is neither a structural failure (files exist), nor a functional failure (CLI exited cleanly with exit code 0), nor a quality failure (never reached judge scoring). It is a gate-enforced minimum-output-size failure that falls between functional and quality layers.

**Affected sections**: Section 2 (4-layer failure model), Section 5.2 (Gate Criteria), FR-EVAL.13 (Release Eval Executor)

**Spec change warranted**: The 4-layer model (structural/functional/quality/regression) should acknowledge that pipeline-internal gates (like min_lines) create a fifth failure mode: "gate rejection." When a CLI pipeline run passes functional checks (exit code 0, artifacts produced) but an internal quality gate rejects an intermediate artifact, this is distinct from both L2-functional and L3-quality failures. The spec should add a semantic check to L2: `_internal_gate_passed()` that checks whether the pipeline's own gates accepted all steps, or alternatively document that internal gate failures map to L2-functional failures with a specific `failure_reason` field in RunResult.

### I3: Variance tracking needs per-step granularity, not just per-run

**Observed**: The execution summary reports per-step timing and per-step verdicts, not just per-run aggregates. The debate step shows 28% duration variance while extract shows only 10%. Artifact sizes vary 35-48% between paired runs even when verdicts match.

**Affected sections**: FR-EVAL.1 (RunResult dataclass), FR-EVAL.5 (Statistical Aggregation), NFR-EVAL.3 (Within-model variance CV < 0.15)

**Spec change warranted**: RunResult should include `step_results: list[StepResult]` capturing per-step timing, verdict, and artifact sizes -- not just overall exit_code and wall_time_seconds. NFR-EVAL.3's CV < 0.15 target should be specified as applying per-step, not just per-run, since some steps (debate, generation) are inherently higher-variance than others (extract, diff). The aggregator should report per-step CV alongside per-run CV so that high-variance steps can be identified and excluded from tight consistency requirements.

### I4: The spec underestimates the importance of "minimum run completeness" thresholds

**Observed**: The execution summary defines a "minimum threshold met" policy: "1 local + 1 global completed per policy." Global runs completing only 3/8 steps still counted as meeting the threshold. This is a pragmatic decision the spec does not anticipate.

**Affected sections**: FR-EVAL.4 (Multi-Run Parallel Execution Engine), FR-EVAL.5 (Statistical Aggregation), Section 6 NFR-EVAL.12

**Spec change warranted**: Add a configurable `min_steps_for_inclusion` parameter to EvalConfig. Runs completing fewer than this threshold are excluded from aggregation. NFR-EVAL.12 ("minimum 5 runs per variant") should be amended to "minimum 5 runs per variant that meet the minimum completeness threshold." The current spec assumes all runs either fully complete or fully fail, which does not match reality.

### I5: Worktree isolation for global baseline is sequential, not parallel

**Observed**: "Global runs used a shared worktree (IronClaude-eval-global-A) for both A and B runs (sequential, not parallel)." The worktree was reused across runs rather than one-per-run.

**Affected sections**: FR-EVAL.6 (Isolation Mechanism), FR-EVAL.4 (Multi-Run Parallel Execution Engine)

**Spec change warranted**: FR-EVAL.6 describes worktree setup/teardown per isolation configuration but does not specify whether worktrees are per-run or per-variant. The real execution reused one worktree sequentially for both global runs. Add an AC to FR-EVAL.6: "Worktrees are created per-variant (not per-run). Multiple runs of the same variant execute sequentially within the same worktree unless `--parallel` is specified, in which case separate worktrees are created per-run." This affects cost estimation (fewer worktrees = less disk) and correctness (sequential runs in shared worktree avoid git lock contention).

---

## 3. Insights That Do NOT Warrant Spec Changes

### N1: Both global runs failing at generate-opus is an interesting delta signal but not a spec deficiency
The fact that v3.0 prompts produce 182-208 line roadmaps while master produces 9-11 lines is a valuable A/B finding. However, the spec already handles this correctly via FR-EVAL.14 (Asymmetric Stage Handling) and the ab-test regression tier. The spec does not need to change to accommodate this finding -- it already anticipates branch-level differences. The finding validates the spec's design rather than exposing a gap.

### N2: The 28% duration variance on debate/generation steps is expected LLM behavior
Multi-turn LLM interactions are inherently variable in timing. The spec already accounts for this via NFR-EVAL.14 (per-run execution time < 15 minutes) and the CV < 0.15 target applies to scores, not wall-clock time. No spec change needed -- timing variance is informational, not gating.

### N3: No rate-limit errors or timeouts observed
The execution summary notes zero HTTP 429 errors and zero subprocess timeouts. This is good news but does not change the spec -- the risk mitigations for rate-limiting (Section 7) and timeout enforcement (FR-EVAL.4) remain necessary for production use at higher concurrency.

### N4: Artifact count consistency (same files produced within each pair)
Both local runs produced 10 .md + 1 .json; both global runs produced 4 .md + 1 .json. This validates the spec's structural layer approach (file presence checks) but does not reveal anything the spec missed.

### N5: The spec-fidelity failure detecting fabricated requirement IDs
This is a quality finding about the roadmap pipeline, not about the eval spec. The eval correctly surfaced the defect. No eval spec change needed -- the 4-layer model already positions quality checks downstream of functional checks.
