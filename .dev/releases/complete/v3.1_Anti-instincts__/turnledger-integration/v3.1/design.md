---
title: "v3.1 TurnLedger + TrailingGateRunner Integration Design"
status: DRAFT
author: Agent 2C (Architect/Designer)
date: 2026-03-20
applies_to:
  - src/superclaude/cli/sprint/executor.py
  - src/superclaude/cli/sprint/models.py (TurnLedger)
  - src/superclaude/cli/pipeline/trailing_gate.py (TrailingGateRunner, DeferredRemediationLog)
  - src/superclaude/cli/sprint/kpi.py (GateKPIReport, build_kpi_report)
  - src/superclaude/cli/pipeline/gates.py (gate_passed)
---

# v3.1 TurnLedger + TrailingGateRunner Unified Pipeline Integration

## 1. Executive Summary

This document specifies exactly where and how `TurnLedger`, `TrailingGateRunner`, `DeferredRemediationLog`, and `GateKPIReport` are wired into the sprint executor pipeline. It addresses a key finding: **`TurnLedger.reimbursement_rate=0.8` is defined but never consumed by production code** -- only exercised in `tests/pipeline/test_full_flow.py` (lines 102-103). This design closes that gap and defines the shadow-to-full rollout path.

---

## 2. Where TurnLedger.debit() and .credit() Are Called

### 2.1 Current State (executor.py lines 538-606)

`execute_phase_tasks()` already calls `ledger.debit()` and `ledger.credit()` in a pre-allocation/reconciliation pattern:

| Call Site | Line | What It Does |
|-----------|------|-------------|
| Pre-launch debit | 558 | `ledger.debit(ledger.minimum_allocation)` -- reserves turns before subprocess |
| Over-consumption debit | 587 | `ledger.debit(actual - pre_allocated)` -- if task used more than reserved |
| Under-consumption credit | 589 | `ledger.credit(pre_allocated - actual)` -- refunds unused pre-allocation |

### 2.2 Missing: Reimbursement on Gate Pass

**The `reimbursement_rate=0.8` field is dead code.** No production path computes `int(turns * reimbursement_rate)` and calls `ledger.credit()`. The test at `test_full_flow.py:102` exercises this manually but the executor never does.

**Integration point -- insert after the wiring hook at executor.py line 602, inside the task loop:**

```python
# After line 602: result = run_post_task_wiring_hook(task, config, result)
# NEW: Gate-pass reimbursement (activates reimbursement_rate)
if ledger is not None and result.status == TaskStatus.PASS:
    gate_result = _evaluate_trailing_gate(task, config, result)
    if gate_result is not None and gate_result.passed:
        reimbursement = int(result.turns_consumed * ledger.reimbursement_rate)
        if reimbursement > 0:
            ledger.credit(reimbursement)
```

### 2.3 Remediation Debit Path

When `attempt_remediation()` is invoked (trailing_gate.py line 354), it already accepts `debit` and `can_remediate` callables. The integration wires these to the ledger:

```
debit=ledger.debit
can_remediate=ledger.can_remediate
```

This is already demonstrated in `test_full_flow.py` scenarios 2-4 but not yet called from `execute_phase_tasks()` or `execute_sprint()`.

### 2.4 Complete Debit/Credit Call Map (Post-Integration)

```
execute_phase_tasks() loop:
  for task in tasks:
    [1] ledger.debit(minimum_allocation)           # pre-reserve
    [2] run subprocess
    [3] ledger.debit(actual - pre) OR              # reconcile over
        ledger.credit(pre - actual)                # reconcile under
    [4] run_post_task_wiring_hook()
    [5] NEW: trailing gate evaluation
        [5a] gate passes -> ledger.credit(turns * reimbursement_rate)
        [5b] gate fails -> attempt_remediation()
             [5b.i]   ledger.debit(turns_per_attempt)    # attempt 1
             [5b.ii]  gate re-check
             [5b.iii] if fail + budget: ledger.debit()   # attempt 2
    [6] append result
```

---

## 3. TrailingGateRunner.submit() Integration with gate_passed()

### 3.1 Current Architecture

`TrailingGateRunner.submit()` (trailing_gate.py line 110) already accepts a `gate_check` parameter that defaults to `gate_passed` (imported from `pipeline/gates.py`). The evaluation runs on a daemon thread and enqueues a `TrailingGateResult` into `GateResultQueue`.

`gate_passed()` (gates.py line 20) is a pure-Python function: file exists, non-empty, min lines, frontmatter fields, semantic checks. It returns `(bool, str | None)`.

### 3.2 Integration Point in the Pipeline Step Loop

There are two modes of integration, controlled by the existing `shadow_gates` flag on `SprintConfig`:

**Mode A -- Shadow (shadow_gates=True, current default path):**
```
After subprocess completes for task[i]:
  1. runner.submit(step)                    # non-blocking daemon thread
  2. Continue to task[i+1] immediately
  3. At phase boundary: runner.wait_for_pending()
  4. shadow_metrics.record() for each result
  5. Results logged but do not affect TaskStatus
```

**Mode B -- Trailing (activated by wiring_gate_mode="full" + gate scope TASK):**
```
After subprocess completes for task[i]:
  1. runner.submit(step)
  2. Continue to task[i+1]
  3. Between tasks: drain() to check completed gates
  4. Any gate failure triggers attempt_remediation()
  5. Remediation outcome affects TaskResult and budget
```

**Mode C -- Blocking (GateScope.RELEASE or GateScope.MILESTONE):**
```
After subprocess completes for task[i]:
  1. Synchronous: passed, reason = gate_passed(output_file, criteria)
  2. If fail: immediate attempt_remediation() or HALT
  3. No daemon thread involved
```

### 3.3 Concrete Wiring in execute_phase_tasks()

The `TrailingGateRunner` instance should be created at the top of `execute_phase_tasks()` and shared across the task loop:

```python
def execute_phase_tasks(tasks, config, phase, ledger=None, *, _subprocess_factory=None):
    runner = TrailingGateRunner()
    remediation_log = DeferredRemediationLog(
        persist_path=config.results_dir / "remediation-log.json"
    )
    gate_results: list[TrailingGateResult] = []
    # ... existing task loop ...
```

The `runner.submit()` call replaces direct gate evaluation. The `drain()` call between tasks processes completed results and triggers remediation for failures.

---

## 4. DeferredRemediationLog Replaces Existing Failure Tracking

### 4.1 Current Failure Tracking

Today, failure tracking is spread across:

| Component | What It Tracks | Location |
|-----------|---------------|----------|
| `TaskResult.status` | Per-task pass/fail | executor.py line 591-599 |
| `TaskResult.gate_outcome` | Gate-specific outcome | executor.py line 500 (wiring hook sets FAIL) |
| `AggregatedPhaseReport` | Phase-level counts | executor.py line 295 |
| `DiagnosticCollector` | Post-halt diagnostics | executor.py line 938 |

There is no persistent, cross-phase record of gate failures that survived remediation or were deferred.

### 4.2 DeferredRemediationLog as the Single Source

`DeferredRemediationLog` (trailing_gate.py line 489) provides:

- **Append on gate failure:** `log.append(gate_result)` creates a `RemediationEntry` with status=PENDING
- **Mark resolved:** `log.mark_remediated(step_id)` after successful remediation
- **Disk persistence:** JSON serialization to `config.results_dir / "remediation-log.json"`
- **Resume recovery:** `DeferredRemediationLog.load_from_disk(path)` for `--resume` support
- **KPI feed:** `log.pending_remediations()` and `log.entry_count` feed into `build_kpi_report()`

### 4.3 Replacement Mapping

| Old Tracking | Replaced By | How |
|-------------|------------|-----|
| `TaskResult.gate_outcome = FAIL` (wiring hook) | `remediation_log.append(gate_result)` | Gate failure recorded with full context |
| `AggregatedPhaseReport.tasks_failed` counting | Still used, but supplemented by `remediation_log.pending_remediations()` | Pending count = failures not yet resolved |
| `DiagnosticCollector` post-halt | `run_diagnostic_chain()` triggered by `RemediationRetryStatus.PERSISTENT_FAILURE` | Diagnostic chain fires on persistent failure, not just phase halt |
| No cross-phase tracking | `remediation_log` persists to disk | `--resume` reloads pending remediations |

### 4.4 Integration Sequence

```
task fails gate:
  1. remediation_log.append(gate_result)           # persist failure
  2. policy.build_remediation_step(gate_result)     # SprintGatePolicy builds Step
  3. attempt_remediation(...)                        # retry-once with ledger
  4. if PASS_*:
       remediation_log.mark_remediated(step_id)     # resolve entry
  5. if PERSISTENT_FAILURE:
       run_diagnostic_chain(...)                     # fire diagnostics
       # entry stays PENDING -> visible in KPI report
  6. if BUDGET_EXHAUSTED:
       # entry stays PENDING -> logged, no turns consumed
```

---

## 5. GateKPIReport Integration Point

### 5.1 When build_kpi_report() Is Called

`build_kpi_report()` (kpi.py line 115) is called **once, after sprint completion**, not during execution. It is a post-hoc aggregation function.

**Concrete call site -- at the end of `execute_sprint()`, after the phase loop completes (executor.py ~line 979), before `logger.write_summary()`:**

```python
# After line 979: sprint_result.finished_at = datetime.now(timezone.utc)
# NEW: Build KPI report from accumulated gate results
from superclaude.cli.sprint.kpi import build_kpi_report

kpi_report = build_kpi_report(
    gate_results=_all_gate_results,        # collected across all phases
    remediation_log=_remediation_log,       # shared DeferredRemediationLog
    conflict_reviews_total=_conflict_count,
    conflicts_detected=_conflicts_found,
)

# Write KPI report to results directory
kpi_path = config.results_dir / "gate-kpi-report.md"
kpi_path.write_text(kpi_report.format_report())

# Attach to sprint result for TUI display
sprint_result.kpi_report = kpi_report
```

### 5.2 Data Flow into build_kpi_report()

```
Phase loop:
  execute_phase_tasks() produces:
    - gate_results: list[TrailingGateResult]  (from runner.drain() + runner.wait_for_pending())
    - remediation_log: DeferredRemediationLog (shared instance, persisted)

Post-loop:
  build_kpi_report(gate_results, remediation_log, ...)
    -> GateKPIReport with:
       .gate_pass_rate, .gate_fail_rate
       .p50_latency_ms, .p95_latency_ms
       .remediation_frequency
       .conflict_review_rate
```

### 5.3 Accumulation Strategy

Gate results must be accumulated across phases. Two approaches:

**Option A (Selected): Phase-scoped runner, cross-phase accumulation list.**
Each phase creates a fresh `TrailingGateRunner`. After `wait_for_pending()` at phase end, results are appended to a sprint-level `_all_gate_results: list[TrailingGateResult]`. The `DeferredRemediationLog` is shared across phases (single instance, same persist path).

**Option B (Rejected): Single runner for entire sprint.**
Would require runner reset between phases; daemon thread lifecycle becomes complex.

---

## 6. Shadow -> Soft -> Full Rollout Using ShadowGateMetrics

### 6.1 Existing Infrastructure

`ShadowGateMetrics` (models.py line 586) provides:
- `record(passed, evaluation_ms)` -- collects per-gate metrics
- `pass_rate`, `p50_latency_ms`, `p95_latency_ms` -- computed properties
- Gated by `SprintConfig.shadow_gates: bool` (line 318)

`SprintConfig.wiring_gate_mode` (line 321) already implements `off/shadow/soft/full` for the wiring analysis hook. This is the proven rollout pattern.

### 6.2 Three-Phase Rollout Plan

#### Phase 1: Shadow (Default -- No Behavioral Change)

**Config:** `shadow_gates=True` (already exists), `gate_rollout_mode="shadow"` (new field)

**Behavior:**
1. `TrailingGateRunner.submit()` fires on every task completion
2. Gate results collected via `runner.drain()` / `runner.wait_for_pending()`
3. Results fed into `ShadowGateMetrics.record()`
4. `DeferredRemediationLog` records failures but no remediation is attempted
5. `TurnLedger.reimbursement_rate` is NOT applied (no credits)
6. KPI report generated at sprint end with shadow data
7. **Zero impact on TaskResult, PhaseResult, or SprintOutcome**

**Activation:**
```bash
superclaude sprint run --shadow-gates tasklist.md
```

**Graduation criteria (automated):**
- `shadow_metrics.pass_rate >= 0.90` over 5+ sprints
- `shadow_metrics.p95_latency_ms < 500` (gate eval does not meaningfully delay)
- Zero false positives confirmed via manual review of `remediation-log.json`

#### Phase 2: Soft (Warnings, Reimbursement Active, No Blocking)

**Config:** `gate_rollout_mode="soft"` (new field paralleling `wiring_gate_mode`)

**Behavior:**
1. All shadow behavior, plus:
2. `TurnLedger.reimbursement_rate` is activated -- `ledger.credit(turns * 0.8)` on gate pass
3. Gate failures logged as warnings (via `_wiring_logger.warning`)
4. `DeferredRemediationLog` records failures with status=PENDING
5. Remediation is **attempted** but failure does NOT set `TaskResult.status = FAIL`
6. KPI report includes remediation metrics
7. **TaskResult and SprintOutcome unchanged by gate failures**

**Activation:**
```bash
superclaude sprint run --gate-mode soft tasklist.md
```

**Graduation criteria:**
- `kpi_report.remediation_frequency < 0.15` (fewer than 15% of tasks need remediation)
- `kpi_report.remediations_resolved / total_remediations > 0.80` (remediation is effective)
- No budget exhaustion caused by remediation retries over 3+ sprints

#### Phase 3: Full (Blocking -- Gate Failures Halt)

**Config:** `gate_rollout_mode="full"`

**Behavior:**
1. All soft behavior, plus:
2. Gate failure after exhausted remediation retries sets `TaskResult.status = FAIL`
3. Phase halts on persistent gate failure (same as `wiring_gate_mode="full"` pattern)
4. `DeferredRemediationLog` entries that remain PENDING after retry trigger `run_diagnostic_chain()`
5. `build_resume_output()` includes remediation log path for `--resume` recovery

**Activation:**
```bash
superclaude sprint run --gate-mode full tasklist.md
```

### 6.3 Implementation via Existing Pattern

The `run_post_task_wiring_hook()` function at executor.py line 418 already implements the shadow/soft/full dispatch pattern. The gate rollout reuses this exact pattern:

```python
def run_post_task_gate_hook(
    task: TaskEntry,
    config: SprintConfig,
    task_result: TaskResult,
    runner: TrailingGateRunner,
    ledger: TurnLedger | None,
    remediation_log: DeferredRemediationLog,
    shadow_metrics: ShadowGateMetrics,
    policy: SprintGatePolicy,
) -> TaskResult:
    mode = config.gate_rollout_mode  # "shadow" | "soft" | "full"

    # Submit gate evaluation (all modes)
    step = _task_to_step(task, config)
    runner.submit(step)
    results = runner.wait_for_pending(timeout=30.0)

    for gate_result in results:
        shadow_metrics.record(gate_result.passed, gate_result.evaluation_ms)

        if gate_result.passed:
            # Reimbursement (soft + full only)
            if mode in ("soft", "full") and ledger is not None:
                reimbursement = int(task_result.turns_consumed * ledger.reimbursement_rate)
                if reimbursement > 0:
                    ledger.credit(reimbursement)
            continue

        # Gate failed
        remediation_log.append(gate_result)

        if mode == "shadow":
            continue  # log only

        # soft + full: attempt remediation
        remediation_step = policy.build_remediation_step(gate_result)
        retry = attempt_remediation(
            remediation_step=remediation_step,
            turns_per_attempt=ledger.minimum_remediation_budget if ledger else 3,
            can_remediate=ledger.can_remediate if ledger else lambda: True,
            debit=ledger.debit if ledger else lambda n: None,
            run_step=lambda s: _run_remediation_subprocess(s, config),
            check_gate=lambda r: _recheck_gate(r, step),
        )

        if retry.status in (
            RemediationRetryStatus.PASS_FIRST_ATTEMPT,
            RemediationRetryStatus.PASS_SECOND_ATTEMPT,
        ):
            remediation_log.mark_remediated(gate_result.step_id)
            continue

        # Persistent failure or budget exhausted
        if mode == "full":
            task_result.status = TaskStatus.FAIL
            task_result.gate_outcome = GateOutcome.FAIL

    return task_result
```

### 6.4 Config Field Addition to SprintConfig

```python
@dataclass
class SprintConfig(PipelineConfig):
    # ... existing fields ...
    shadow_gates: bool = False
    wiring_gate_mode: Literal["off", "shadow", "soft", "full"] = "soft"
    # NEW: gate evaluation rollout mode (parallels wiring_gate_mode)
    gate_rollout_mode: Literal["off", "shadow", "soft", "full"] = "off"
```

Default is `"off"` to preserve backward compatibility. When `shadow_gates=True` is passed without `gate_rollout_mode`, the system auto-promotes to `"shadow"`.

---

## 7. Data Flow Diagram

```
                    execute_sprint()
                         |
                    for phase in phases:
                         |
                  execute_phase_tasks()
                         |
          +-------- for task in tasks --------+
          |                                    |
     [1] ledger.debit(min_alloc)              |
          |                                    |
     [2] _run_task_subprocess()               |
          |                                    |
     [3] ledger reconcile (debit/credit)      |
          |                                    |
     [4] run_post_task_wiring_hook()          |
          |                                    |
     [5] run_post_task_gate_hook() --------+  |
          |    |                            |  |
          |  runner.submit(step)            |  |
          |    |                            |  |
          |  runner.wait_for_pending()      |  |
          |    |                            |  |
          |  for gate_result:               |  |
          |    |                            |  |
          |  shadow_metrics.record()        |  |
          |    |                            |  |
          |  if passed:                     |  |
          |    ledger.credit(reimburse)     |  |
          |  if failed:                     |  |
          |    remediation_log.append()     |  |
          |    attempt_remediation()        |  |
          |      ledger.debit()             |  |
          |      mark_remediated() or       |  |
          |      run_diagnostic_chain()     |  |
          |                                 |  |
     [6] results.append(task_result) ------+  |
          +-----------------------------------+
                         |
          runner.wait_for_pending()  # drain stragglers
                         |
          gate_results += runner.drain()
                         |
          (end of phase loop)
                         |
          build_kpi_report(gate_results, remediation_log)
                         |
          logger.write_summary(sprint_result)
```

---

## 8. Key Invariants

1. **Monotonicity preserved:** `TurnLedger.debit()` only increases `consumed`; `credit()` only increases `reimbursed`. The `available()` calculation is always `initial - consumed + reimbursed`.

2. **Reimbursement is bounded:** `credit(int(turns * 0.8))` -- the `int()` truncation and the 0.8 rate ensure reimbursement never exceeds consumption. Combined with the pre-allocation reconciliation, a task that passes its gate recovers at most 80% of its actual turn cost.

3. **Shadow mode is side-effect free:** When `gate_rollout_mode="shadow"`, no `ledger.credit()` or `TaskResult` mutation occurs. Metrics are collected but behavior is identical to pre-integration.

4. **DeferredRemediationLog is the single failure journal:** All gate failures go through `log.append()`. The old `TaskResult.gate_outcome = FAIL` path in the wiring hook remains for wiring-specific failures; gate failures use the remediation log.

5. **Release gates are always blocking:** `resolve_gate_mode(GateScope.RELEASE, ...)` always returns `GateMode.BLOCKING` (trailing_gate.py line 614). The rollout mode only affects task-level gates.

---

## 9. Files Modified (Implementation Checklist)

| File | Change | Complexity |
|------|--------|-----------|
| `src/superclaude/cli/sprint/models.py` | Add `gate_rollout_mode` field to `SprintConfig` | Trivial |
| `src/superclaude/cli/sprint/executor.py` | Add `run_post_task_gate_hook()`, wire into task loop after line 602 | Medium |
| `src/superclaude/cli/sprint/executor.py` | Instantiate `TrailingGateRunner` + `DeferredRemediationLog` in `execute_phase_tasks()` | Medium |
| `src/superclaude/cli/sprint/executor.py` | Call `build_kpi_report()` after phase loop in `execute_sprint()` | Small |
| `src/superclaude/cli/sprint/executor.py` | Wire `ShadowGateMetrics` accumulation across phases | Small |
| `tests/sprint/test_shadow_mode.py` | Extend with gate_rollout_mode="shadow" integration test | Medium |
| `tests/pipeline/test_full_flow.py` | Add scenario 5: reimbursement_rate consumed in production path | Small |

---

## 10. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Gate eval latency blocks task loop | High | Shadow mode measures p95 before soft/full activation; `wait_for_pending(timeout=30)` caps blocking |
| Reimbursement inflates available budget | Medium | Rate is 0.8 (never > consumed); `can_launch()` checks `available() >= minimum_allocation` |
| Remediation retries consume entire budget | High | `attempt_remediation()` checks `can_remediate()` before each attempt; max 2 attempts |
| DeferredRemediationLog disk write fails | Low | `_write_to_disk()` is best-effort; in-memory state is authoritative |
| Backward compatibility break | High | `gate_rollout_mode` defaults to `"off"`; no behavior change without explicit opt-in |
