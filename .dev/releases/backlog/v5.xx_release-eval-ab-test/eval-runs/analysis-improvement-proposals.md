---
title: "Analysis: Improvement Proposals Impact on Release-Eval Spec"
source: improvement-proposals.md
date: 2026-03-19
verdict: "2 of 3 proposals warrant spec changes; 1 does not"
---

# Analysis: Improvement Proposals Impact on Release-Eval Spec

## 1. Key Findings

1. **LLM requirement ID fabrication is a reproducible, systematic failure mode.** Both local eval runs (A and B) independently produced the same class of error: the LLM invented its own requirement numbering scheme instead of preserving the spec's IDs. This is not stochastic variance -- it is a deterministic prompt deficiency that triggers the spec-fidelity gate every time.

2. **Blocking gates create a chicken-and-egg problem for eval coverage.** The spec-fidelity gate's FAIL verdict prevented wiring-verification from executing, which meant several metrics could only be scored via static code analysis rather than actual pipeline execution evidence. The eval could not exercise the full pipeline it was designed to evaluate.

3. **Pipeline-level observability (stdout/stderr capture) is missing from the execution model.** The eval had no way to score metric R-8 because the pipeline does not emit its own execution log to a capturable stream. Artifact files (.md, .json) exist, but the pipeline's runtime output (step transitions, gate verdicts) is ephemeral.

4. **The improvement proposals form a dependency chain, not independent fixes.** IP-1 (prompt fix) eliminates the root cause, making IP-2 (eval-mode bypass) unnecessary for the specific v3.0 case. IP-3 (log capture) is orthogonal. The proposals correctly identify this prioritization.

5. **The CONDITIONAL_PASS verdict exposes a gap in the spec's failure taxonomy.** The v3.0 eval produced a result that is neither PASS nor FAIL -- it is "passed all gates that executed, but some gates were blocked from executing." The release-eval-spec's 4-layer failure model does not account for this intermediate state.

## 2. Insights That Impact the Release-Eval Spec

### Insight A: The spec needs an eval-mode execution concept for quality/coverage layers

**What was observed**: IP-2 proposes an `--eval-mode` flag that runs blocking gates but continues past failures, recording the verdict without halting. The v3.0 eval demonstrated that fail-fast behavior (correct for production) prevents the eval system from exercising all pipeline stages, defeating the purpose of comprehensive evaluation.

**Affected sections**: FR-EVAL.4 (Multi-Run Parallel Execution Engine, AC bullet 7: "Fail-fast: structural/functional layer failures halt evaluation before quality layer"), FR-EVAL.13 (Release Eval Executor, AC bullets 1-4 on layer ordering and fail-fast), Section 5.2 (Gate Criteria table, enforcement column).

**Warranted spec change**: FR-EVAL.4 and FR-EVAL.13 should add explicit support for a `--continue-on-fail` or `--eval-mode` flag that:
- Executes all layers regardless of earlier failures
- Records each layer's pass/fail verdict independently
- Marks the overall result as FAIL if any layer failed (preserving correctness)
- Annotates which downstream layers ran "past a failed gate" so their scores carry an appropriate caveat

This is distinct from removing fail-fast entirely. The spec currently treats fail-fast as unconditional. The eval run proved that for the eval tool's own use case (measuring coverage across all layers), unconditional fail-fast is counterproductive. The spec's Section 5.2 Gate Criteria table should add a "Deferrable in eval-mode" column.

### Insight B: The spec's 4-layer failure model needs a CONDITIONAL_PASS state

**What was observed**: The v3.0 eval produced a verdict of CONDITIONAL_PASS, meaning "all executed gates passed, but not all gates could execute." The release-eval-spec defines only PASS and FAIL outcomes (FR-EVAL.5 `compute_verdict()`, FR-EVAL.13 overall verdict). There is no representation for partial coverage.

**Affected sections**: FR-EVAL.5 (Statistical Aggregation, AC bullet 4: `compute_verdict()` produces PASS/FAIL), FR-EVAL.7 (Report Generation), FR-EVAL.13 (overall verdict), Section 4.5 (EvalReport dataclass, `overall_passed: bool`).

**Warranted spec change**: The verdict model should be extended from binary (PASS/FAIL) to ternary (PASS/CONDITIONAL_PASS/FAIL):
- PASS: All layers executed and passed thresholds
- CONDITIONAL_PASS: All executed layers passed, but one or more layers were blocked from executing (with annotation of what was blocked and why)
- FAIL: One or more executed layers failed thresholds

The `EvalReport.overall_passed: bool` field should become `EvalReport.verdict: str` (enum: pass/conditional_pass/fail) with an accompanying `blocked_layers: list[str]` field. This maps directly to the v3.0 experience where spec-fidelity blocked wiring-verification.

### Insight C: The spec should account for LLM prompt deficiency as a structural failure mode

**What was observed**: IP-1 reveals that the LLM systematically fabricated requirement IDs in generated roadmaps. This is not a quality variance issue (covered by the spec's quality layer and multi-run aggregation). It is a deterministic prompt deficiency -- the generate prompt does not instruct ID preservation, so the LLM consistently invents new IDs.

**Affected sections**: Section 7 (Risk Assessment), FR-EVAL.9 (Suite Generator -- fixture generation should anticipate prompt-induced failures), Appendix C (Scoring Rubric -- accuracy dimension anchor at score 1 mentions "references non-existent files/functions" but not "fabricates identifiers").

**Warranted spec change**: The Risk Assessment table (Section 7) should add a new risk row:

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Pipeline prompts cause systematic LLM fabrication (IDs, paths, names) | High | High | Eval suite generator should include a "prompt fidelity" structural check that verifies generated outputs preserve spec-defined identifiers verbatim. This is a structural layer test, not a quality layer test, because it is deterministic and binary. |

Additionally, the eval suite generator (FR-EVAL.9) should auto-generate a structural test that compares requirement IDs in generated output against the source spec's IDs. This catches the class of failure IP-1 describes without requiring manual prompt fixes.

## 3. Insights That Do NOT Warrant Spec Changes

### IP-3: Pipeline stdout/stderr log capture

**What was observed**: Metric R-8 could not be scored because the pipeline does not capture its own stdout/stderr to a file. IP-3 proposes a `--log-file` option.

**Why no spec change is warranted**: This is a feature gap in the pipeline being evaluated (the roadmap CLI), not in the eval tool spec. The release-eval-spec already defines `RunResult.stdout_path` and `RunResult.stderr_path` fields (Section 4.5) and expects the runner to capture subprocess output (FR-EVAL.4, AC bullet 5: "Per-run output captured to isolated directories"). The spec correctly anticipates capturing output; the problem is that the pipeline under test does not produce capturable output for its own internal operations. Fixing the pipeline's logging is an improvement to `superclaude roadmap run`, not to the eval spec.

### IP-1's specific prompt fix (the literal text change)

**What was observed**: IP-1 proposes adding "CRITICAL: You MUST use the exact requirement identifiers from the spec" to the generate prompt.

**Why no spec change is warranted**: The specific prompt wording is an implementation detail of the roadmap CLI, not the eval tool. The eval spec should detect this class of failure (covered by Insight C above), but should not prescribe how individual pipeline prompts are written. The eval tool's job is to surface the problem; the fix lives in the pipeline being evaluated.

### The dependency chain between IP-1 and IP-2

**What was observed**: If IP-1 works, IP-2 becomes unnecessary for v3.0. The proposals correctly note this.

**Why no spec change is warranted**: This dependency observation is operational context for the v3.0 eval, not a gap in the eval spec's design. The spec change warranted by IP-2 (Insight A above) stands on its own merits -- eval-mode execution is valuable regardless of whether any specific prompt fix works, because future evals will encounter other blocking gates.
