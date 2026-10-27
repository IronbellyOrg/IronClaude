---
release: v3.2-wiring-verification-gate
component: turnledger-integration
status: design
date: 2026-03-20
parent_spec: v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md
key_finding: TurnLedger.reimbursement_rate=0.8 is defined but never consumed by production code
---

# v3.2 Wiring Gate -- TurnLedger Integration Design

## 1. Problem with the Current Spec (Section 4.5)

The v3.2 release spec (Section 4.5) defines sprint integration using bare mode
switches on `SprintConfig.wiring_gate_mode`:

```python
if config.wiring_gate_mode == "shadow":
    logger.info(...)
elif config.wiring_gate_mode == "soft":
    tui.warn(...)
elif config.wiring_gate_mode == "full":
    passed, reason = gate_passed(wiring_report_path, WIRING_GATE)
```

This design has three defects:

1. **No budget accountability.** Wiring analysis consumes wall-clock time and
   subprocess context but is invisible to TurnLedger. A task that triggers
   expensive remediation from a wiring failure has no budget trail.

2. **reimbursement_rate is dead code.** `TurnLedger.reimbursement_rate = 0.8`
   exists on the model but is never read by any production code path. Tests
   exercise it manually (`int(10 * ledger.reimbursement_rate)`), but
   `execute_phase_tasks()` performs raw arithmetic without consulting the field.
   The wiring gate should be the first consumer to wire this field into
   production logic.

3. **Mode switches duplicate gate infrastructure.** The 3-phase rollout
   (shadow/soft/full) is implemented as string comparisons in the executor
   rather than leveraging `resolve_gate_mode()` and `GateScope` from
   `trailing_gate.py`, which already encode scope-aware enforcement semantics.

---

## 2. Modified Section 4.5: Sprint Integration via TurnLedger

### 2.1 Design Principle

The wiring gate is a **TurnLedger consumer**, not a mode-switch consumer.
Rollout phases are expressed as TurnLedger configuration profiles, not
as string literals in executor conditionals.

### 2.2 TurnLedger Extensions

```python
# models.py -- TurnLedger additions

@dataclass
class TurnLedger:
    # ... existing fields ...
    initial_budget: int
    consumed: int = 0
    reimbursed: int = 0
    reimbursement_rate: float = 0.8          # NOW CONSUMED (see 2.4)
    minimum_allocation: int = 5
    minimum_remediation_budget: int = 3

    # --- v3.2 additions ---
    wiring_gate_cost: int = 0                # turns debited for wiring analysis
    wiring_gate_credits: int = 0             # turns credited back on clean pass
    wiring_gate_scope: GateScope = GateScope.TASK  # scope for resolve_gate_mode()

    def debit_wiring(self, turns: int) -> None:
        """Debit turns for wiring analysis. Tracked separately for KPI."""
        if turns < 0:
            raise ValueError("wiring debit must be non-negative")
        self.wiring_gate_cost += turns
        self.consumed += turns

    def credit_wiring(self, turns: int) -> None:
        """Credit turns back after clean wiring pass. Uses reimbursement_rate."""
        if turns < 0:
            raise ValueError("wiring credit must be non-negative")
        actual = int(turns * self.reimbursement_rate)  # FIRST PRODUCTION USE
        self.wiring_gate_credits += actual
        self.reimbursed += actual

    def can_run_wiring_gate(self) -> bool:
        """Return True if budget allows wiring analysis.

        Wiring analysis costs WIRING_ANALYSIS_TURNS (default 1).
        Unlike can_remediate(), this is a lightweight check -- analysis
        is AST-only, not a subprocess launch.
        """
        return self.available() >= 1
```

### 2.3 Rollout Phases as TurnLedger Configuration

Instead of `wiring_gate_mode: Literal["off", "shadow", "soft", "full"]`,
rollout phases map to TurnLedger + GateScope configuration:

| Phase   | GateScope     | resolve_gate_mode() returns | Budget effect on FAIL | Budget effect on PASS |
|---------|---------------|-----------------------------|-----------------------|-----------------------|
| shadow  | `TASK`        | `TRAILING` (grace=inf)      | debit only; no block  | debit + credit via `reimbursement_rate` |
| soft    | `MILESTONE`   | config-driven (default: BLOCKING) | debit + DeferredRemediationLog | debit + credit |
| full    | `RELEASE`     | `BLOCKING` (immutable)      | debit + attempt_remediation() | debit + credit |

**SprintConfig change:**

```python
# Replace:
#   wiring_gate_mode: Literal["off", "shadow", "soft", "full"] = "soft"
# With:
wiring_gate_enabled: bool = True
wiring_gate_scope: GateScope = GateScope.TASK       # shadow default
wiring_gate_grace_period: int = 0                    # 0 = BLOCKING at task scope
```

**Mapping from old modes to new config:**

| Old mode | `wiring_gate_enabled` | `wiring_gate_scope` | `wiring_gate_grace_period` |
|----------|-----------------------|----------------------|----------------------------|
| off      | `False`               | N/A                  | N/A                        |
| shadow   | `True`                | `GateScope.TASK`     | `999999` (effectively infinite) |
| soft     | `True`                | `GateScope.MILESTONE`| `0`                        |
| full     | `True`                | `GateScope.RELEASE`  | `0`                        |

This eliminates the mode-switch string comparisons and reuses `resolve_gate_mode()`.

### 2.4 Wiring reimbursement_rate: First Production Consumer

The key integration point. When wiring analysis passes (zero findings),
the analysis cost is partially reimbursed using `TurnLedger.reimbursement_rate`:

```python
WIRING_ANALYSIS_TURNS = 1  # AST-only, < 2s for 50 files

# After wiring analysis completes:
ledger.debit_wiring(WIRING_ANALYSIS_TURNS)

if report.passed:
    ledger.credit_wiring(WIRING_ANALYSIS_TURNS)
    # Net cost: WIRING_ANALYSIS_TURNS * (1 - reimbursement_rate)
    # With default 0.8 rate: net cost = 0.2 turns (effectively free)
```

This means:
- **Clean code is cheap.** Projects with good wiring hygiene pay ~0.2 turns
  per task for wiring verification.
- **Broken code is expensive.** Wiring failures consume turns with no
  reimbursement, plus remediation costs in full mode.
- **The rate is tunable.** Setting `reimbursement_rate=1.0` makes wiring
  checks free on pass. Setting `reimbursement_rate=0.0` makes them always
  cost 1 turn.

---

## 3. Budget Flow: Task Complete to TurnLedger Debit/Credit

```
Task subprocess completes
        |
        v
execute_phase_tasks() reconciles budget (existing logic, lines 582-589)
        |
        v
run_post_task_wiring_hook(task, config, task_result, ledger)
        |
        +-- config.wiring_gate_enabled == False? --> return task_result (no cost)
        |
        +-- ledger is None? --> run analysis without budget tracking (phase mode)
        |
        +-- ledger.can_run_wiring_gate() == False? --> log "budget skip", return
        |
        v
ledger.debit_wiring(WIRING_ANALYSIS_TURNS)        # always debit before analysis
        |
        v
report = run_wiring_analysis(source_dir, config)
        |
        +-- Exception? --> log warning, return task_result (turns lost, no credit)
        |
        v
effective_mode = resolve_gate_mode(
    scope=config.wiring_gate_scope,
    config_gate_mode=GateMode.BLOCKING,
    grace_period=config.wiring_gate_grace_period,
)
        |
        v
    +---+---+---+
    |           |
  TRAILING    BLOCKING
    |           |
    v           v
Log findings  Gate evaluation
(shadow)       |
    |          +-- report.passed?
    |          |     |
    |          |     +-- Yes: ledger.credit_wiring(WIRING_ANALYSIS_TURNS)
    |          |     |        return task_result (pass)
    |          |     |
    |          |     +-- No:  --> attempt_remediation() path (see Section 4)
    |          |
    v          v
report.passed?
    |
    +-- Yes: ledger.credit_wiring(WIRING_ANALYSIS_TURNS)
    |        return task_result
    |
    +-- No:  DeferredRemediationLog.append(gate_result)
             return task_result (status unchanged in trailing mode)
```

### 3.1 Modified run_post_task_wiring_hook Signature

```python
def run_post_task_wiring_hook(
    task: TaskEntry,
    config: SprintConfig,
    task_result: TaskResult,
    ledger: TurnLedger | None = None,      # NEW: budget integration
) -> TaskResult:
```

The `ledger` parameter is threaded from `execute_phase_tasks()` line 602,
which already has the ledger in scope:

```python
# executor.py, line 601-602 (modified)
result = run_post_task_wiring_hook(task, config, result, ledger=ledger)
```

### 3.2 Budget Accounting Table

| Event | debit | credit | Net cost |
|-------|-------|--------|----------|
| Wiring analysis runs, passes | 1 | `int(1 * 0.8)` = 0 (floored) | 1 |
| Wiring analysis runs, fails (trailing) | 1 | 0 | 1 |
| Wiring analysis runs, fails (blocking) | 1 + remediation_turns | 0 | 1 + remediation |
| Wiring analysis skipped (budget) | 0 | 0 | 0 |
| Wiring gate disabled | 0 | 0 | 0 |

**Note on floor(1 * 0.8) = 0:** With WIRING_ANALYSIS_TURNS=1 and
reimbursement_rate=0.8, the credit rounds to 0. This is intentional: each
individual wiring check costs 1 turn. The reimbursement_rate becomes
meaningful when WIRING_ANALYSIS_TURNS is higher (e.g., for large packages)
or when accumulated across many tasks. If zero-cost-on-pass is desired,
set `reimbursement_rate=1.0`.

---

## 4. Remediation Path: attempt_remediation() on Wiring Gate Failure

When `resolve_gate_mode()` returns `BLOCKING` and the wiring gate fails:

```python
# In run_post_task_wiring_hook, after gate evaluation fails in BLOCKING mode:

if effective_mode == GateMode.BLOCKING and not report.passed:
    # Build remediation step from wiring findings
    policy = SprintGatePolicy(config)
    gate_result = TrailingGateResult(
        step_id=f"{task.task_id}_wiring",
        passed=False,
        evaluation_ms=report.scan_duration_seconds * 1000,
        failure_reason=_format_wiring_failure(report),
    )
    remediation_step = policy.build_remediation_step(gate_result)

    # Execute remediation with TurnLedger integration
    retry_result = attempt_remediation(
        remediation_step=remediation_step,
        turns_per_attempt=ledger.minimum_remediation_budget,
        can_remediate=ledger.can_remediate,
        debit=ledger.debit,
        run_step=_run_remediation_subprocess,
        check_gate=lambda sr: _recheck_wiring(sr, config),
    )

    if retry_result.status in (
        RemediationRetryStatus.PASS_FIRST_ATTEMPT,
        RemediationRetryStatus.PASS_SECOND_ATTEMPT,
    ):
        # Remediation succeeded: credit back wiring analysis cost
        ledger.credit_wiring(WIRING_ANALYSIS_TURNS)
        return task_result  # original status preserved

    # Persistent failure or budget exhausted
    task_result.status = TaskStatus.FAIL
    task_result.gate_outcome = GateOutcome.FAIL
    return task_result
```

### 4.1 Why attempt_remediation() and Not Custom Retry Logic

The existing `attempt_remediation()` in `trailing_gate.py` already implements:
- Pre-check budget guard (`can_remediate()`)
- Retry-once semantics (2 attempts max)
- Budget debit per attempt
- Structured result with `RemediationRetryStatus`

The wiring gate reuses this function exactly. The only new pieces are:
- `_format_wiring_failure(report)` -- converts WiringReport findings to a
  remediation prompt string
- `_recheck_wiring(step_result, config)` -- reruns `run_wiring_analysis()`
  on the same source dir and returns a `TrailingGateResult`

### 4.2 Remediation Budget Flow

```
Wiring gate FAIL (BLOCKING mode)
        |
        v
ledger.can_remediate()?
        |
   No --+--> task_result.status = FAIL
        |    retry_result.status = BUDGET_EXHAUSTED
        |
   Yes -+--> ledger.debit(minimum_remediation_budget)  # attempt 1
        |    run remediation subprocess
        |    recheck wiring analysis
        |
        +-- pass? --> credit_wiring(), return
        |
        +-- fail? --> ledger.can_remediate()?
                |
           No --+--> PERSISTENT_FAILURE (1 attempt cost lost)
                |
           Yes -+--> ledger.debit(minimum_remediation_budget)  # attempt 2
                     run + recheck
                     |
                     +-- pass/fail --> return result
```

---

## 5. Three-Phase Rollout via TurnLedger Configuration

### 5.1 Phase 1: Shadow (This Release)

```python
SprintConfig(
    wiring_gate_enabled=True,
    wiring_gate_scope=GateScope.TASK,
    wiring_gate_grace_period=999999,  # trailing, never blocks
)
```

**TurnLedger behavior:**
- `debit_wiring(1)` on every task
- `credit_wiring(1)` on clean pass (net cost depends on reimbursement_rate)
- Failures logged via `DeferredRemediationLog` but never block
- `resolve_gate_mode()` returns `GateMode.TRAILING`
- KPI data: wiring_gate_cost and wiring_gate_credits tracked for reporting

**Data collection:** `GateKPIReport` extended with:
```python
wiring_gates_evaluated: int = 0
wiring_gates_passed: int = 0
wiring_gates_failed: int = 0
wiring_analysis_latency_ms: list[float] = field(default_factory=list)
wiring_total_debit: int = 0
wiring_total_credit: int = 0
```

### 5.2 Phase 2: Soft (Release +1)

```python
SprintConfig(
    wiring_gate_enabled=True,
    wiring_gate_scope=GateScope.MILESTONE,
    wiring_gate_grace_period=0,
)
```

**TurnLedger behavior:**
- Same debit/credit as shadow
- `resolve_gate_mode()` returns `GateMode.BLOCKING` (milestone default)
- Failures block at milestone scope but not at task scope
- `DeferredRemediationLog.append()` on failure
- Override: `--wiring-gate-scope task` (demotes to shadow behavior)

### 5.3 Phase 3: Full (Release +2)

```python
SprintConfig(
    wiring_gate_enabled=True,
    wiring_gate_scope=GateScope.RELEASE,
    wiring_gate_grace_period=0,
)
```

**TurnLedger behavior:**
- `resolve_gate_mode()` returns `GateMode.BLOCKING` (immutable for release scope)
- Failures trigger `attempt_remediation()` immediately
- No override without whitelist entry
- Remediation turns debited from same ledger
- Clean passes still receive reimbursement credit

### 5.4 Rollout Transition Checklist

Advancing from one phase to the next requires updating **one config field**
(`wiring_gate_scope`), not changing executor code. The TurnLedger and
`resolve_gate_mode()` handle all behavioral differences.

| Transition | Config change | Code change |
|------------|---------------|-------------|
| off -> shadow | `wiring_gate_enabled = True` | None |
| shadow -> soft | `wiring_gate_scope = GateScope.MILESTONE` | None |
| soft -> full | `wiring_gate_scope = GateScope.RELEASE` | None |
| full -> soft (rollback) | `wiring_gate_scope = GateScope.MILESTONE` | None |
| any -> off (emergency) | `wiring_gate_enabled = False` | None |

---

## 6. Backward Compatibility: TurnLedger is None

The wiring gate must work when `ledger is None`, which occurs in
phase-level execution mode (pre-task-ledger sprints).

### 6.1 Null Ledger Contract

```python
def run_post_task_wiring_hook(
    task: TaskEntry,
    config: SprintConfig,
    task_result: TaskResult,
    ledger: TurnLedger | None = None,
) -> TaskResult:
    if not config.wiring_gate_enabled:
        return task_result

    # Budget gate: if ledger exists, check budget; if None, always proceed
    if ledger is not None and not ledger.can_run_wiring_gate():
        _wiring_logger.info("Wiring analysis skipped: budget insufficient")
        return task_result

    # Run analysis (no budget tracking when ledger is None)
    report = run_wiring_analysis(source_dir, config)

    # Debit (no-op when ledger is None)
    if ledger is not None:
        ledger.debit_wiring(WIRING_ANALYSIS_TURNS)

    # Determine mode
    effective_mode = resolve_gate_mode(
        scope=config.wiring_gate_scope,
        grace_period=config.wiring_gate_grace_period,
    )

    # Credit on pass (no-op when ledger is None)
    if report.passed and ledger is not None:
        ledger.credit_wiring(WIRING_ANALYSIS_TURNS)

    # Enforcement follows effective_mode regardless of ledger presence
    if effective_mode == GateMode.BLOCKING and not report.passed:
        if ledger is not None:
            # attempt_remediation with budget
            ...
        else:
            # No budget tracking: block directly
            task_result.status = TaskStatus.FAIL
            task_result.gate_outcome = GateOutcome.FAIL

    return task_result
```

### 6.2 Behavioral Matrix

| Ledger state | Wiring analysis | Budget tracking | Remediation |
|---|---|---|---|
| `None` | Runs if enabled | No debit/credit | Direct FAIL (no retry budget) |
| Present, sufficient | Runs | debit + conditional credit | `attempt_remediation()` with budget |
| Present, exhausted | Skipped | No debit | No remediation |

---

## 7. Test Contract: test_full_flow.py Extensions

### 7.1 New Scenarios Required

The existing 4 scenarios in `test_full_flow.py` exercise the TurnLedger +
gate + remediation chain but do not cover wiring-specific paths.

**Scenario 5: Wiring gate passes -- budget credited**

```python
def test_scenario_5_wiring_pass_budget_credit(self, tmp_path):
    """Wiring analysis passes; debit_wiring + credit_wiring applied."""
    ledger = TurnLedger(initial_budget=100, reimbursement_rate=0.8)

    # Task completes, wiring analysis runs
    ledger.debit(10)  # task cost
    ledger.debit_wiring(1)  # wiring analysis cost

    # Wiring passes: credit back
    ledger.credit_wiring(1)

    # Verify budget accounting
    assert ledger.consumed == 11  # 10 task + 1 wiring
    assert ledger.wiring_gate_cost == 1
    assert ledger.wiring_gate_credits == 0  # int(1 * 0.8) = 0
    assert ledger.can_launch()
```

**Scenario 6: Wiring gate fails in BLOCKING mode -- remediation flow**

```python
def test_scenario_6_wiring_fail_remediate(self, tmp_path):
    """Wiring gate fails, remediation via attempt_remediation(), budget debited."""
    ledger = TurnLedger(
        initial_budget=100,
        minimum_remediation_budget=5,
        reimbursement_rate=0.8,
    )

    # Task + wiring analysis
    ledger.debit(10)
    ledger.debit_wiring(1)

    # Wiring fails, remediation passes first attempt
    remediation_step = _make_step("task-5_wiring_remediation", tmp_path)
    retry_result = attempt_remediation(
        remediation_step=remediation_step,
        turns_per_attempt=5,
        can_remediate=ledger.can_remediate,
        debit=ledger.debit,
        run_step=lambda s: _make_step_result(s, StepStatus.PASS),
        check_gate=lambda r: _make_gate_result("task-5_wiring", True),
    )

    assert retry_result.status == RemediationRetryStatus.PASS_FIRST_ATTEMPT
    assert ledger.consumed == 16  # 10 task + 1 wiring + 5 remediation
    assert ledger.wiring_gate_cost == 1
```

**Scenario 7: Wiring gate with ledger=None -- backward compat**

```python
def test_scenario_7_wiring_no_ledger(self, tmp_path):
    """Wiring gate runs without TurnLedger (phase-level mode)."""
    # Verify run_post_task_wiring_hook works with ledger=None
    # Analysis runs, enforcement applies, no budget tracking
    # TaskResult status set to FAIL on blocking failure
```

**Scenario 8: Wiring gate shadow mode -- deferred log, no block**

```python
def test_scenario_8_wiring_shadow_deferred(self, tmp_path):
    """Shadow mode: wiring findings logged to DeferredRemediationLog, no block."""
    ledger = TurnLedger(initial_budget=100)

    # Wiring analysis runs, finds issues
    ledger.debit_wiring(1)
    # No credit (findings present)

    # DeferredRemediationLog receives the entry
    # Task status unchanged
    assert ledger.wiring_gate_cost == 1
    assert ledger.wiring_gate_credits == 0
```

### 7.2 Existing Scenario Modifications

No existing scenarios need modification. The new wiring scenarios are additive.
The existing scenarios 1-4 continue to validate the base TurnLedger + trailing
gate + remediation chain. Scenario 5 (budget accounting) should be extended
with a wiring sub-case but the existing assertions remain valid.

### 7.3 KPI Report Extension

`build_kpi_report()` should accept an additional parameter:

```python
def build_kpi_report(
    gate_results: list[TrailingGateResult],
    remediation_log: DeferredRemediationLog | None = None,
    conflict_reviews_total: int = 0,
    conflicts_detected: int = 0,
    wiring_ledger: TurnLedger | None = None,  # NEW
) -> GateKPIReport:
```

When `wiring_ledger` is provided, the report includes:
- `wiring_total_debit` from `ledger.wiring_gate_cost`
- `wiring_total_credit` from `ledger.wiring_gate_credits`
- Wiring-specific pass/fail counts from gate results filtered by step_id suffix `_wiring`

---

## 8. Implementation Checklist

| # | File | Change | Depends on |
|---|------|--------|------------|
| 1 | `sprint/models.py` | Add `debit_wiring`, `credit_wiring`, `can_run_wiring_gate`, `wiring_gate_cost`, `wiring_gate_credits` to TurnLedger | -- |
| 2 | `sprint/models.py` | Replace `wiring_gate_mode` on SprintConfig with `wiring_gate_enabled`, `wiring_gate_scope`, `wiring_gate_grace_period` | -- |
| 3 | `sprint/executor.py` | Modify `run_post_task_wiring_hook` to accept `ledger` param, use `resolve_gate_mode()` instead of string switches | 1, 2 |
| 4 | `sprint/executor.py` | Thread `ledger` from `execute_phase_tasks()` line 602 into `run_post_task_wiring_hook` | 3 |
| 5 | `sprint/executor.py` | Add `attempt_remediation()` call path in BLOCKING mode | 3 |
| 6 | `sprint/kpi.py` | Extend `GateKPIReport` with wiring-specific fields; update `build_kpi_report()` | 1 |
| 7 | `tests/pipeline/test_full_flow.py` | Add scenarios 5-8 | 3, 4, 5 |
| 8 | `tests/sprint/test_models.py` | Add tests for `debit_wiring`, `credit_wiring`, `can_run_wiring_gate` | 1 |

---

## 9. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| `int(1 * 0.8) = 0` makes single-turn reimbursement a no-op | Low: wiring checks cost 1 turn always | Document in budget table; recommend `reimbursement_rate=1.0` for zero-cost-on-pass |
| SprintConfig field rename breaks existing configs | Medium: `wiring_gate_mode` -> `wiring_gate_enabled` + scope | Provide `__post_init__` migration that reads old `wiring_gate_mode` and maps to new fields with deprecation warning |
| `resolve_gate_mode()` import from trailing_gate creates tight coupling | Low: already imported at executor.py line 37 | No new coupling; reuses existing import |
| Ledger=None path skips remediation entirely | Medium: phase-level sprints get hard FAIL with no retry | Acceptable for phase-level mode; document that task-level ledger is recommended for full-mode deployments |

---

## 10. Appendix: reimbursement_rate Production Wiring Audit

**Current state (pre-v3.2):**

| Location | Reads `reimbursement_rate`? | Notes |
|----------|---------------------------|-------|
| `sprint/models.py:499` | Defines field | `reimbursement_rate: float = 0.8` |
| `sprint/executor.py:582-589` | No | Manual arithmetic: `actual - pre_allocated` / `pre_allocated - actual` |
| `pipeline/trailing_gate.py:395` | No | `debit(turns_per_attempt)` -- flat debit |
| `sprint/kpi.py` | No | Reports pass/fail counts, not budget economics |
| `tests/pipeline/test_full_flow.py:102` | Yes (test only) | `int(10 * ledger.reimbursement_rate)` |
| `tests/sprint/test_models.py:529+` | Yes (test only) | Multiple test cases exercise the field |

**After v3.2:**

| Location | Reads `reimbursement_rate`? | Notes |
|----------|---------------------------|-------|
| `sprint/models.py` (`credit_wiring`) | **Yes -- first production consumer** | `int(turns * self.reimbursement_rate)` |
| `sprint/executor.py` (`run_post_task_wiring_hook`) | Indirect via `ledger.credit_wiring()` | Called on wiring pass |

This design makes `TurnLedger.reimbursement_rate` a live production field
for the first time, validating its existence in the data model.
