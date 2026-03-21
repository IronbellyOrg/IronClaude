---
title: "Tasklist: Top 3 Eval Spec Proposals"
source: adversarial/merged-ranked-proposals.md
target_spec: release-eval-spec.md
executor: sc:task-unified
total_tasks: 15
phases: 3
status: ready
---

# Tasklist: Implement Top 3 Adversarial Proposals into release-eval-spec.md

**Scope**: Refactor `release-eval-spec.md` to incorporate proposals C+L (ternary verdict), F (partial run scoring), and K (eval-mode execution). Spec-only changes — no code files modified.

**Target file**: `/config/workspace/IronClaude/.dev/releases/backlog/v5.xx_release-eval-ab-test/release-eval-spec.md`

**Evidence base**: `eval-runs/adversarial/merged-ranked-proposals.md`

---

## Phase 1: Ternary Verdict Model (C+L)

> Rationale: Highest priority (Value 8.7, Complexity 2.3, Ratio 3.78). Two independent analyses converged. The v3.0 eval invented CONDITIONAL_PASS outside the spec's vocabulary.

### T01: Update EvalReport dataclass in Section 4.5

**Tier**: simple
**File**: release-eval-spec.md, Section 4.5, lines 492-502
**Action**: Modify the `EvalReport` dataclass:
1. Replace `overall_passed: bool` with `verdict: str` and add comment `# "pass" | "conditional_pass" | "fail"`
2. Add field `blocked_layers: list[str]` with comment `# layers that could not execute (empty for pass/fail)`
3. Add field `conditions: list[str]` with comment `# upgrade requirements (empty for pass/fail)`
4. Update the docstring to reference the ternary model

**Before** (line 498):
```python
overall_passed: bool
```
**After**:
```python
verdict: str                # "pass" | "conditional_pass" | "fail"
blocked_layers: list[str] = field(default_factory=list)
                            # layers that could not execute (empty for pass/fail)
conditions: list[str] = field(default_factory=list)
                            # upgrade requirements for conditional_pass → pass
```

**Acceptance criteria**:
- [ ] `overall_passed: bool` no longer exists in EvalReport
- [ ] `verdict` field uses string enum with exactly 3 values
- [ ] `blocked_layers` and `conditions` have default empty lists
- [ ] Docstring updated

---

### T01b: Sync FR-EVAL.1 EvalReport AC with ternary verdict fields

**Tier**: simple
**File**: release-eval-spec.md, Section FR-EVAL.1, line 136
**Action**: Update the EvalReport field enumeration to reflect the new verdict model:

**Before**:
```
- [ ] EvalReport includes spec_hash (SHA-256), confidence_level, model_breakdown, recommendations
```
**After**:
```
- [ ] EvalReport includes spec_hash (SHA-256), verdict (pass|conditional_pass|fail), blocked_layers, conditions, confidence_level, model_breakdown, recommendations
```

**Acceptance criteria**:
- [ ] FR-EVAL.1 AC mentions `verdict`, `blocked_layers`, and `conditions`
- [ ] `overall_passed` no longer referenced in FR-EVAL.1

---

### T02: Update FR-EVAL.5 compute_verdict() AC

**Tier**: simple
**File**: release-eval-spec.md, Section FR-EVAL.5, line 192
**Action**: Replace the `compute_verdict()` AC with ternary logic:

**Before**:
```
- [ ] `compute_verdict()` produces overall PASS/FAIL based on configurable thresholds
```
**After**:
```
- [ ] `compute_verdict()` produces ternary verdict based on configurable thresholds:
  - PASS: all layers executed and passed thresholds
  - CONDITIONAL_PASS: all executed layers passed, but one or more layers were blocked from executing; `blocked_layers` and `conditions` populated
  - FAIL: one or more executed layers failed thresholds
```

**Acceptance criteria**:
- [ ] Three verdict states defined with precise trigger conditions
- [ ] CONDITIONAL_PASS explicitly requires blocked_layers to be non-empty

---

### T03: Update FR-EVAL.7 report generation ACs

**Tier**: simple
**File**: release-eval-spec.md, Section FR-EVAL.7, line 232
**Action**: Update the report frontmatter AC to reference `verdict` instead of a boolean pass/fail:

**Before**:
```
- [ ] `generate_report()` writes report.md with YAML frontmatter (release, timestamp, verdict, confidence_level) and markdown body
```
**After**:
```
- [ ] `generate_report()` writes report.md with YAML frontmatter (release, timestamp, verdict: pass|conditional_pass|fail, confidence_level, blocked_layers, conditions) and markdown body
- [ ] When verdict is conditional_pass, report body includes "Conditions for Full Pass" section listing each condition with actionable remediation
```

**Acceptance criteria**:
- [ ] Frontmatter includes verdict, blocked_layers, conditions
- [ ] Conditional pass has dedicated report section

---

### T04: Update FR-EVAL.13 overall verdict AC

**Tier**: simple
**File**: release-eval-spec.md, Section FR-EVAL.13, line 326
**Action**: Replace binary verdict with ternary:

**Before**:
```
- [ ] Overall verdict: PASS requires all structural/functional pass AND quality above thresholds
```
**After**:
```
- [ ] Overall verdict uses ternary model:
  - PASS: all structural/functional layers pass AND quality above thresholds AND all layers executed
  - CONDITIONAL_PASS: all executed structural/functional layers pass AND quality above thresholds AND one or more layers were blocked from executing
  - FAIL: any executed structural/functional layer fails OR quality below thresholds
```

**Acceptance criteria**:
- [ ] Three verdict states with precise conditions
- [ ] "all layers executed" is the distinguishing condition between PASS and CONDITIONAL_PASS

---

## Phase 2: Partial Run Scoring (F)

> Rationale: Second highest priority (Value 7.5, Complexity 2.0, Ratio 3.75). All 4 eval runs were PARTIAL. Independent of Phase 1.

### T05: Add step tracking fields to RunResult in Section 4.5

**Tier**: simple
**File**: release-eval-spec.md, Section 4.5, lines 452-477
**Action**: Add two fields to `RunResult` dataclass after `stderr_path`:

```python
steps_completed: int        # number of pipeline steps that completed
steps_total: int            # total pipeline steps defined
```

Also add a property:
```python
@property
def completion_ratio(self) -> float:
    """Fraction of pipeline steps completed (0.0-1.0)."""
    return self.steps_completed / self.steps_total if self.steps_total > 0 else 0.0
```

Update `to_dict()` to include both fields.

**Acceptance criteria**:
- [ ] `steps_completed` and `steps_total` are int fields on RunResult
- [ ] `completion_ratio` property computes fraction
- [ ] `to_dict()` serializes both fields
- [ ] Edge case: steps_total=0 returns 0.0 (no division by zero)

---

### T05b: Sync FR-EVAL.1 RunResult AC with step tracking fields

**Tier**: simple
**File**: release-eval-spec.md, Section FR-EVAL.1, line 134
**Action**: Update the RunResult field enumeration to include step tracking:

**Before**:
```
- [ ] RunResult captures test_id, run_number, model, scores, exit_code, tokens_used, wall_time_seconds, artifacts, stdout_path, stderr_path
```
**After**:
```
- [ ] RunResult captures test_id, run_number, model, scores, exit_code, tokens_used, wall_time_seconds, artifacts, stdout_path, stderr_path, steps_completed, steps_total
```

**Acceptance criteria**:
- [ ] FR-EVAL.1 AC lists `steps_completed` and `steps_total`
- [ ] Field list matches the dataclass definition in Section 4.5

---

### T06: Add partial run AC to FR-EVAL.4

**Tier**: simple
**File**: release-eval-spec.md, Section FR-EVAL.4, after line 181
**Action**: Add a new AC bullet:

```
- [ ] Partial runs (N of M steps completed) produce RunResult with `steps_completed` and `steps_total` fields populated. Partial runs are included in aggregation for their completed steps; uncompleted steps produce no scores for that run.
```

**Acceptance criteria**:
- [ ] AC explicitly states partial runs are not discarded
- [ ] AC specifies that uncompleted steps produce no scores (not zero scores)

---

### T07: Add partial run handling to FR-EVAL.5

**Tier**: simple
**File**: release-eval-spec.md, Section FR-EVAL.5, as new AC bullet at the end of the AC list (before the Dependencies line)
**Action**: Add a new AC bullet:

```
- [ ] `aggregate_scores()` includes partial runs for steps they completed. Per-step aggregation reports the number of contributing runs (which may be less than total runs when some runs did not reach that step).
```

**Acceptance criteria**:
- [ ] Aggregation handles variable run counts per step
- [ ] Reports contributing run count per step

---

### T08: Update FR-EVAL.13 to distinguish fail-fast from partial completion

**Tier**: simple
**File**: release-eval-spec.md, Section FR-EVAL.13, after the ternary verdict AC from T04
**Action**: Add a new AC bullet:

```
- [ ] A run that completes N of M pipeline steps due to an internal gate failure is classified as PARTIAL (not FAILED). PARTIAL runs contribute scores for completed steps. The fail-fast behavior (structural failure halts functional) applies across eval layers, not within pipeline-internal steps of a single layer.
```

**Acceptance criteria**:
- [ ] PARTIAL status distinguished from FAILED
- [ ] Fail-fast scope clarified: eval layers, not pipeline-internal gates

---

## Phase 3: Eval-Mode Execution (K)

> Rationale: Third highest priority (Value 8.0, Complexity 2.5, Ratio 3.20). Addresses root cause of CONDITIONAL_PASS. Depends on Phase 1 (ternary verdict informs eval-mode behavior).

### T09: Add eval_mode field to EvalConfig in Section 4.5

**Tier**: simple
**File**: release-eval-spec.md, Section 4.5, line 545 (after `parallel` field)
**Action**: Add new field to `EvalConfig`:

```python
eval_mode: bool = False     # when True, gate failures are recorded but do not halt execution
```

**Acceptance criteria**:
- [ ] `eval_mode` field exists with default False
- [ ] Comment explains the behavior precisely

---

### T10: Add --eval-mode flag to CLI surface in Section 5.1

**Tier**: simple
**File**: release-eval-spec.md, Section 5.1, in BOTH CLI options tables
**Action**: Add new row to both tables:

1. In the `superclaude ab-test` options table (after `--debug`, line 661), add:
```
| `--eval-mode` | FLAG | False | Record gate failures but continue execution past failed gates. Overall verdict still reflects failures. Use for comprehensive coverage measurement. |
```

2. In the `superclaude release-eval` options table (after `--debug`, line 682), add the same row:
```
| `--eval-mode` | FLAG | False | Record gate failures but continue execution past failed gates. Overall verdict still reflects failures. Use for comprehensive coverage measurement. |
```

**Acceptance criteria**:
- [ ] Flag listed in both `release-eval run` and `ab-test run` option tables
- [ ] Description clarifies that verdict still reports failures (not bypassed)

---

### T11: Update FR-EVAL.4 and FR-EVAL.13 fail-fast ACs for eval-mode

**Tier**: moderate
**File**: release-eval-spec.md, Sections FR-EVAL.4 and FR-EVAL.13
**Action**:

In FR-EVAL.4, update AC bullet 7:
**Before**:
```
- [ ] Fail-fast: structural/functional layer failures halt evaluation before quality layer
```
**After**:
```
- [ ] Fail-fast (default): structural/functional layer failures halt evaluation before quality layer
- [ ] Eval-mode (`--eval-mode`): all layers execute regardless of earlier failures. Each layer's pass/fail verdict is recorded independently. Layers that ran past a failed gate are annotated with `past_failed_gate: true` in their TestVerdict. Overall verdict reflects all failures (eval-mode does not suppress FAIL verdicts).
```

In FR-EVAL.13, update AC bullets 2-3:
**Before**:
```
- [ ] Structural failure halts before functional tests run (fail-fast)
- [ ] Functional failure halts before quality tests run (fail-fast)
```
**After**:
```
- [ ] Structural failure halts before functional tests run (fail-fast) — unless `--eval-mode` is active
- [ ] Functional failure halts before quality tests run (fail-fast) — unless `--eval-mode` is active
- [ ] In eval-mode: failures are recorded in TestVerdict but execution continues to the next layer. Downstream layers annotated with `past_failed_gate: true`.
```

**Acceptance criteria**:
- [ ] Default fail-fast behavior unchanged
- [ ] Eval-mode behavior precisely defined
- [ ] `past_failed_gate` annotation specified for downstream layers
- [ ] Overall verdict still reflects failures (no false PASSes)

---

### T12: Add past_failed_gate field to TestVerdict in Section 4.5

**Tier**: simple
**File**: release-eval-spec.md, Section 4.5, lines 480-488
**Action**: Add field to `TestVerdict`:

```python
past_failed_gate: bool = False  # True when this layer ran after a prior layer failed (eval-mode only)
```

**Acceptance criteria**:
- [ ] Field exists with default False
- [ ] Only set to True in eval-mode execution
- [ ] Consumers can filter/flag scores from layers that ran past failures

---

### T12b: Sync FR-EVAL.1 TestVerdict AC with past_failed_gate field

**Tier**: simple
**File**: release-eval-spec.md, Section FR-EVAL.1, line 135
**Action**: Update the TestVerdict description to include the new field:

**Before**:
```
- [ ] TestVerdict aggregates across runs with per-dimension mean/stddev/min/max
```
**After**:
```
- [ ] TestVerdict aggregates across runs with per-dimension mean/stddev/min/max and includes past_failed_gate annotation (False by default; True when layer ran after a prior layer failed in eval-mode)
```

**Acceptance criteria**:
- [ ] FR-EVAL.1 AC mentions `past_failed_gate`
- [ ] Description matches the field added in T12

---

## Dependency Graph

```
Phase 1 (C+L):          Phase 2 (F):
  T01  ─┐                 T05  ─┐
  T01b ─┤                 T05b ─┤
  T02  ─┤ (parallel)      T06  ─┤ (parallel)
  T03  ─┤                 T07  ─┤
  T04  ─┘                 T08  ─┘
       │                       │
       └──── Phase 3 (K): ────┘
               T09  ─┐
               T10  ─┤ (parallel)
               T11  ─┤
               T12  ─┤
               T12b ─┘
```

Phase 1 and Phase 2 are independent (parallelizable).
Phase 3 depends on Phase 1 (ternary verdict) and Phase 2 (partial run concept).
All tasks within each phase are parallelizable (no cross-task insertion dependencies).

## Execution Summary

| Phase | Tasks | Tier | Estimated Lines Changed | Parallelizable |
|-------|-------|------|------------------------|----------------|
| 1: Ternary Verdict (C+L) | T01, T01b, T02-T04 | 5x simple | ~45 lines in spec | Yes (within phase) |
| 2: Partial Run Scoring (F) | T05, T05b, T06-T08 | 5x simple | ~35 lines in spec | Yes (within phase) |
| 3: Eval-Mode (K) | T09-T12, T12b | 4x simple, 1x moderate | ~40 lines in spec | Yes (within phase) |
| **Total** | **15 tasks** | **14 simple, 1 moderate** | **~120 lines** | Phases 1+2 parallel |
