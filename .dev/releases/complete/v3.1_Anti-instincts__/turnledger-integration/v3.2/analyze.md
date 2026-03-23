# v3.2 Wiring Verification Gate -- TurnLedger Integration Analysis

**Agent**: 3A (Analyzer)
**Date**: 2026-03-20
**Spec**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`

---

## 1. TurnLedger Overview

The `TurnLedger` class (`src/superclaude/cli/sprint/models.py:488-525`) provides:

| Method/Field | Purpose |
|---|---|
| `initial_budget` | Total turn allocation for sprint |
| `consumed` / `reimbursed` | Running counters |
| `reimbursement_rate = 0.8` | Reimbursement multiplier -- **DEAD FIELD** |
| `minimum_allocation = 5` | Min turns to launch a subprocess |
| `minimum_remediation_budget = 3` | Min turns to attempt remediation |
| `available()` | `initial_budget - consumed + reimbursed` |
| `debit(n)` / `credit(n)` | Consume / reimburse turns |
| `can_launch()` | `available() >= minimum_allocation` |
| `can_remediate()` | `available() >= minimum_remediation_budget` |

### Dead Field: `reimbursement_rate`

`reimbursement_rate = 0.8` is defined at `models.py:499` but **never consumed by any production code** in `src/`. The only consumers are:

- `tests/pipeline/test_full_flow.py:102` -- `int(10 * ledger.reimbursement_rate)`
- `tests/pipeline/test_full_flow.py:318` -- same pattern

No production code calls `ledger.reimbursement_rate` to compute a credit amount. The `credit()` method takes an explicit `int`, but no caller derives that int from the rate. The rate is pure dead weight.

---

## 2. v3.2 Concepts That USE TurnLedger Infrastructure

### 2.1 Budget Guard in Task Loop (DIRECT USE)

`execute_phase_tasks()` (`executor.py:506-606`) uses `TurnLedger` directly:

- **Pre-launch check** (line 542): `ledger.can_launch()` gates each task subprocess
- **Pre-allocation debit** (line 558): `ledger.debit(ledger.minimum_allocation)`
- **Post-task reconciliation** (lines 582-589): Adjusts debit/credit for actual vs pre-allocated turns
- **Budget exhaustion** (line 544): Marks remaining tasks as SKIPPED

`check_budget_guard()` (`executor.py:337-350`) wraps `ledger.can_launch()` into a message-or-None pattern. This exists but is **not called** from `execute_phase_tasks()` -- the inline `can_launch()` check at line 542 serves the same purpose.

### 2.2 `attempt_remediation()` Budget Integration (INDIRECT USE via Callable)

`attempt_remediation()` (`trailing_gate.py:354-449`) does NOT import TurnLedger. Instead it accepts **callables**:

- `can_remediate: Callable[[], bool]` -- bound to `ledger.can_remediate`
- `debit: Callable[[int], None]` -- bound to `ledger.debit`

This is tested in `test_full_flow.py` scenarios 2-4, where `ledger.can_remediate` and `ledger.debit` are passed directly. The pattern is sound but the connection is **never wired in production** -- `attempt_remediation()` is never called from `execute_phase_tasks()` or `execute_sprint()`.

### 2.3 `build_resume_output()` (DISPLAY ONLY)

`build_resume_output()` (`models.py:528-582`) accepts `ledger: TurnLedger | None` and renders `consumed` and `available()` into the HALT message. This is display/reporting only, not enforcement.

---

## 3. v3.2 Concepts That BYPASS TurnLedger Infrastructure

### 3.1 Shadow/Soft/Full Mode Switch (INDEPENDENT OF TURNLEDGER)

The v3.2 spec's core enforcement mechanism is `config.wiring_gate_mode` (spec Section 4.5), a 4-valued enum (`off/shadow/soft/full`) on `SprintConfig`. The `run_post_task_wiring_hook()` function (`executor.py:418-503`) implements this:

| Mode | Behavior | TurnLedger involvement |
|---|---|---|
| `off` | Skip analysis | None |
| `shadow` | Log findings, no status change | None |
| `soft` | Warn on critical findings | None |
| `full` | Set `TaskStatus.FAIL` + `GateOutcome.FAIL` | None |

**The entire shadow/soft/full mode switch operates without any TurnLedger interaction.** It modifies `TaskResult.status` and `TaskResult.gate_outcome` directly. There is no budget check before analysis, no debit for analysis time, and no reimbursement on pass.

### 3.2 `run_wiring_safeguard_checks()` (INDEPENDENT OF TURNLEDGER)

Pre-activation safeguards (`executor.py:353-415`) produce warnings only. No budget interaction.

### 3.3 `TrailingGateRunner` (NEVER CALLED FROM SPRINT LOOP)

The spec's architecture diagram (Section 3.1) shows `TrailingGateRunner` consuming wiring gate results in shadow mode. In production code, `execute_sprint()` never instantiates or calls `TrailingGateRunner`. The `TrailingGateRunner` class exists at `trailing_gate.py:88-213` but is completely disconnected from the sprint execution loop.

### 3.4 `SprintGatePolicy` (EXISTS BUT `build_remediation_step` NEVER INVOKED)

`SprintGatePolicy` (`executor.py:54-97`) implements `TrailingGatePolicy` and has `build_remediation_step()`. However:

- `execute_phase_tasks()` never instantiates `SprintGatePolicy`
- The full-mode path in `run_post_task_wiring_hook()` (line 491-501) sets `FAIL` status but **does not invoke any remediation**
- The spec says Phase 3 full enforcement uses `SprintGatePolicy.build_remediation_step()` -- this path does not exist in code

### 3.5 `DeferredRemediationLog` (EXISTS, NOT USED BY WIRING GATE)

Phase 2 (spec Section 8) specifies: "Findings recorded in `DeferredRemediationLog`." The class exists at `trailing_gate.py:489-572`. However:

- `run_post_task_wiring_hook()` does not instantiate or write to `DeferredRemediationLog`
- The soft-mode path logs warnings via `_wiring_logger` but does not create remediation entries
- No code in executor.py instantiates `DeferredRemediationLog` for wiring findings

---

## 4. Phase 3 Gap: Where `TurnLedger.can_remediate()` Would Be Needed

The spec's Phase 3 (Section 8, "Full") states:
> "Remediation via `SprintGatePolicy.build_remediation_step()`"

For this to work, the full-mode path in `run_post_task_wiring_hook()` (or a new orchestration point) would need:

### 4.1 Required Integration Points

```
run_post_task_wiring_hook(full mode, blocking > 0)
  |
  +-- ledger.can_remediate()  .............. MISSING: no ledger param on hook
  |     |
  |     +-- False --> return FAIL (budget exhausted)
  |     +-- True  --> proceed to remediation
  |
  +-- SprintGatePolicy.build_remediation_step()  .. EXISTS but never called
  |
  +-- attempt_remediation(                         .. EXISTS but never wired
  |     can_remediate=ledger.can_remediate,
  |     debit=ledger.debit,
  |     ...)
  |
  +-- On persistent failure:
        DeferredRemediationLog.append()  ......... EXISTS but never wired
```

### 4.2 Specific Missing Wiring

| What | Where it should be | Current state |
|---|---|---|
| `TurnLedger` parameter on `run_post_task_wiring_hook()` | `executor.py:418` signature | Not present -- hook takes `(task, config, task_result)` only |
| `ledger.can_remediate()` check before remediation | Full-mode branch at `executor.py:491` | Not present -- sets FAIL immediately with no remediation attempt |
| `SprintGatePolicy` instantiation in task loop | `execute_phase_tasks()` | Not present |
| `attempt_remediation()` call from full-mode path | `run_post_task_wiring_hook()` or new function | Not present |
| `DeferredRemediationLog` instantiation for wiring failures | `execute_phase_tasks()` or `execute_sprint()` | Not present |

### 4.3 The `execute_phase_tasks` Call Site

At `executor.py:602`, the hook is called:
```python
result = run_post_task_wiring_hook(task, config, result)
```

The `ledger` variable is in scope (line 510 parameter), but is **not passed** to the hook. This is the primary missing connection.

---

## 5. Phase 2 `DeferredRemediationLog` Alignment

### Spec Expectation (Section 8, Phase 2)

> "Findings recorded in `DeferredRemediationLog`"
> "Block only at release scope (per `resolve_gate_mode()` which returns BLOCKING for release)"

### Existing `DeferredRemediationLog` Class

The class at `trailing_gate.py:489-572` was designed for **gate failures** from `TrailingGateResult` objects. Its `append()` method (line 501) takes a `TrailingGateResult`.

### Alignment Assessment

| Aspect | Spec expectation | Existing class | Aligned? |
|---|---|---|---|
| Input type | Wiring findings (WiringReport/WiringFinding) | TrailingGateResult | **NO** -- type mismatch |
| Entry structure | Wiring finding with file_path, symbol_name, line | step_id, gate_result dict, failure_reason | **PARTIAL** -- could encode wiring data in failure_reason but loses structure |
| Persistence | Disk-backed for release-scope blocking | Disk-backed via `_write_to_disk()` | **YES** |
| Resume support | Not specified | `load_from_disk()` / `deserialize()` | **YES** |
| Status tracking | pending/remediated | pending/remediated/waived | **YES** |

**Key mismatch**: `DeferredRemediationLog.append()` takes `TrailingGateResult` (a gate evaluation result with step_id/passed/evaluation_ms). Wiring findings are structured differently (finding_type/file_path/symbol_name/line_number/severity). Two options:

1. **Adapter**: Convert `WiringReport` into a synthetic `TrailingGateResult` before appending. Loses finding-level granularity.
2. **Extension**: Add a `WiringRemediationEntry` subclass or parallel method `append_wiring(report)`. Preserves structure but grows the class.

### `resolve_gate_mode()` Integration

`resolve_gate_mode()` (`trailing_gate.py:593-628`) returns `GateMode.BLOCKING` for `GateScope.RELEASE`. The spec says Phase 2 blocks at release scope only. This function exists and works correctly, but is **never called** from the wiring gate path. The wiring gate uses its own `wiring_gate_mode` field instead of the scope-based resolution system.

---

## 6. Summary: Integration Map

```
                        USES TurnLedger          BYPASSES TurnLedger
                        ==============           ===================
execute_phase_tasks()   can_launch()             wiring_gate_mode switch
  budget guard          debit()/credit()         run_wiring_safeguard_checks()
  pre-allocation        minimum_allocation       shadow mode logging
  reconciliation                                 soft mode warnings
                                                 full mode FAIL (no remediation)
build_resume_output()   consumed/available()
                        (display only)

attempt_remediation()   can_remediate() via       SprintGatePolicy.build_remediation_step()
  (tested, never          callable param            (exists, never called)
   called from prod)    debit() via callable      DeferredRemediationLog
                                                    (exists, not wired to wiring gate)
                                                  TrailingGateRunner
                                                    (exists, not called from sprint)
                                                  resolve_gate_mode()
                                                    (exists, not called by wiring gate)
```

### Dead/Orphan Summary

| Component | Status | Impact on v3.2 |
|---|---|---|
| `TurnLedger.reimbursement_rate = 0.8` | DEAD -- no production consumer | No impact (never read) |
| `check_budget_guard()` | ORPHAN -- exists but not called | Redundant with inline check |
| `SprintGatePolicy.build_remediation_step()` | ORPHAN -- defined but never invoked | Phase 3 blocker |
| `TrailingGateRunner` | ORPHAN -- never called from sprint loop | Phase 1 shadow data collection gap |
| `attempt_remediation()` | TESTED but never called from production | Phase 3 blocker |
| `resolve_gate_mode()` | FUNCTIONAL but wiring gate uses own mode field | Phase 2 scope-aware blocking gap |
