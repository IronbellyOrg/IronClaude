# v3.2 Roadmap Gap Analysis (Agent A)

**Release**: Wiring Verification Gate v1.0 (v3.2_fidelity-refactor)
**Analysis Date**: 2026-03-21
**Execution Log Status**: All 5 phases marked PASS (24m 31s total)
**Analyst**: Agent A (code-level verification against roadmap spec)

---

## Roadmap Phase-by-Phase Status

### Phase 1: Core Analysis Engine -- IMPLEMENTED

| Milestone | Status | Evidence |
|-----------|--------|----------|
| 1.1 Data Models (WiringFinding, WiringReport, WiringConfig) | PRESENT | `audit/wiring_gate.py:44-135`, `audit/wiring_config.py` |
| 1.2 analyze_unwired_callables() | PRESENT | `audit/wiring_gate.py:313-363` |
| 1.2 analyze_orphan_modules() | PRESENT | `audit/wiring_gate.py:393-516` |
| 1.2 analyze_unwired_registries() | PRESENT | `audit/wiring_gate.py:553-665` (named `analyze_registries`) |
| 1.3 emit_report() | PRESENT | `audit/wiring_gate.py:715-866` |
| 1.3 WIRING_GATE constant | PRESENT | `audit/wiring_gate.py:973-1026` |
| 1.3 5 semantic check functions | PRESENT (evolved) | 5 checks exist but names differ from spec (see deviations below) |
| 1.4 Unit tests | PRESENT (assumed) | Execution log shows Phase 1 PASS |

**Deviations from spec**:
- Spec required 5 checks: `analysis_complete_true`, `zero_unwired_callables`, `zero_orphan_modules`, `zero_unwired_registries`, `total_findings_consistent`
- Implementation has 5 different checks: `analysis_complete_true`, `recognized_rollout_mode`, `finding_counts_consistent`, `severity_summary_consistent`, `zero_blocking_findings_for_mode`
- This is an intentional evolution: the implementation uses mode-aware blocking logic rather than zero-tolerance checks, which better supports the shadow/soft/full rollout model
- Frontmatter field names differ from spec: `unwired_callable_count` vs `unwired_count`, `orphan_module_count` vs `orphan_count`, `unwired_registry_count` vs `registry_count`; implementation adds `rollout_mode`, `critical_count`, `major_count`, `info_count`, `blocking_findings`, `audit_artifacts_used` (16 fields vs spec's 12)
- `files_skipped` field on WiringReport: PRESENT (OQ-3 gap resolved)

### Phase 2: Sprint Integration -- PARTIALLY IMPLEMENTED

| Milestone | Status | Evidence |
|-----------|--------|----------|
| 2.1 TurnLedger: 3 new fields | PRESENT (renamed) | `models.py:537-539` -- `wiring_turns_used`, `wiring_turns_credited`, `wiring_budget_exhausted` (spec named them `wiring_gate_cost`, `wiring_gate_credits`, `wiring_gate_scope`) |
| 2.1 debit_wiring() | PRESENT | `models.py:565-576` |
| 2.1 credit_wiring() with floor | PRESENT | `models.py:578-593` -- floor-to-zero arithmetic confirmed |
| 2.1 can_run_wiring_gate() | PRESENT | `models.py:595-599` |
| 2.1 SprintConfig: wiring fields | PARTIAL | `wiring_gate_mode` (string enum) present instead of spec's `wiring_gate_enabled` (bool). `wiring_gate_scope`, `wiring_analysis_turns`, `remediation_cost` present. Missing: `wiring_gate_grace_period`, `SHADOW_GRACE_INFINITE` constant |
| 2.1 Migration shim | PRESENT (different fields) | `models.py:340-355` -- migrates `wiring_budget_turns`, `wiring_remediation_cost`, `wiring_scope` (not `wiring_gate_mode` as spec requires) |
| 2.2 run_post_task_wiring_hook() | PRESENT | `executor.py:449-582` |
| 2.2 BLOCKING mode path | PRESENT | `executor.py:548-579` |
| 2.2 SHADOW mode path | PRESENT | `executor.py:519-530` |
| 2.2 SOFT mode path | PRESENT | `executor.py:532-546` |
| 2.2 Null-ledger compat | PRESENT | All ledger operations guarded with `if ledger is not None` |
| 2.2 resolve_gate_mode() usage | **DEAD CODE** | `_resolve_wiring_mode()` defined at line 420 but NEVER CALLED -- `run_post_task_wiring_hook` uses `config.wiring_gate_mode` string directly (line 473) |
| 2.3 TurnLedger unit tests | PRESENT (assumed) | Execution log shows Phase 2 PASS |

### Phase 3: KPI and Deviation Reconciliation -- IMPLEMENTED

| Milestone | Status | Evidence |
|-----------|--------|----------|
| 3.1 KPI Report: 6 wiring fields | PRESENT (different names) | `kpi.py:47-52` -- `wiring_findings_total`, `wiring_findings_by_type`, `wiring_turns_used`, `wiring_turns_credited`, `whitelist_entries_applied`, `files_skipped` (spec expected: `wiring_total_debits`, `wiring_total_credits`, `wiring_net_cost`, `wiring_analyses_run`, `wiring_findings_total`, `wiring_remediations_attempted`) |
| 3.1 build_kpi_report() signature | PRESENT | `kpi.py:137-143` -- accepts `turn_ledger` and `wiring_report` params |
| 3.2 _deviation_counts_reconciled() | PRESENT | `roadmap/gates.py:702` -- integrated into SPEC_FIDELITY_GATE semantic checks |

### Phase 4: Integration Testing and Validation -- PRESENT (via execution log)

| Milestone | Status | Evidence |
|-----------|--------|----------|
| 4.1 Integration tests | PRESENT (assumed) | Phase 4 PASS in execution log |
| 4.2 Retrospective validation | PRESENT (assumed) | Phase 4 PASS |
| 4.3 Performance benchmark | PRESENT (assumed) | Phase 4 PASS |

### Phase 5: Rollout Validation -- PRESENT (via execution log)

| Milestone | Status | Evidence |
|-----------|--------|----------|
| 5.1 Shadow mode baseline | PRESENT (assumed) | Phase 5 PASS |
| 5.2 Soft mode readiness | PRESENT (assumed) | Phase 5 PASS |
| 5.3 Blocking mode authorization | PRESENT (assumed) | Phase 5 PASS |

---

## Present in Code

1. **Core analysis engine** (wiring_gate.py, ~1048 LOC) -- all three analyzers working
2. **WiringConfig + whitelist** (wiring_config.py) -- configuration and whitelist loading
3. **WIRING_GATE constant** with 16-field frontmatter and 5 semantic checks
4. **emit_report()** with yaml.safe_dump() serialization
5. **TurnLedger extensions**: `debit_wiring()`, `credit_wiring()` (with floor-to-zero), `can_run_wiring_gate()`
6. **TurnLedger fields**: `wiring_turns_used`, `wiring_turns_credited`, `wiring_budget_exhausted`
7. **SprintConfig wiring fields**: `wiring_gate_mode`, `wiring_gate_scope`, `wiring_analysis_turns`, `remediation_cost`
8. **run_post_task_wiring_hook()** in executor.py -- hooked into `execute_phase_tasks()` at line 788
9. **Shadow/soft/full mode branches** in the wiring hook
10. **Null-ledger compatibility** -- all ledger ops guarded
11. **GateKPIReport wiring metrics** -- 6 fields in kpi.py
12. **build_kpi_report()** accepting TurnLedger and WiringReport
13. **_deviation_counts_reconciled()** in roadmap/gates.py, wired into SPEC_FIDELITY_GATE
14. **run_wiring_safeguard_checks()** -- pre-activation validation (SC-010, SC-011)
15. **SprintGatePolicy** class -- concrete implementation of TrailingGatePolicy

---

## Missing from Code

### CRITICAL GAPS

1. **`_resolve_wiring_mode()` is dead code** -- defined at executor.py:420-446 but never called. The `run_post_task_wiring_hook()` reads `config.wiring_gate_mode` directly (line 473) instead of calling `_resolve_wiring_mode()` which would use `resolve_gate_mode(scope, grace_period)` from trailing_gate.py. This means **Goal-5d (scope-based mode resolution) is specced but not active**.

2. **No `DeferredRemediationLog` usage in sprint executor** -- The spec (Section 4.5.3, Gamma IE-4) requires shadow mode to construct a synthetic `TrailingGateResult` and append it to `DeferredRemediationLog`. The implementation's shadow branch (executor.py:519-530) only logs findings -- it does not create a `TrailingGateResult` or touch `DeferredRemediationLog`. The executor does not even import `DeferredRemediationLog`.

3. **No `TrailingGateRunner` integration in `execute_sprint()`** -- The spec's dependency map (Section 11) shows `sprint/executor.py` consuming `TrailingGateRunner` from `pipeline/trailing_gate.py`. The `execute_sprint()` function (line 843) never instantiates or calls `TrailingGateRunner`. Gate evaluation runs synchronously in `run_post_task_wiring_hook()`, not via the trailing gate's daemon-thread evaluator.

4. **No `attempt_remediation()` call in wiring hook** -- The spec (Section 4.5.3) describes a full remediation flow: `_format_wiring_failure()` -> `SprintGatePolicy.build_remediation_step()` -> `attempt_remediation()` -> `_recheck_wiring()`. The implementation's BLOCKING branch (executor.py:548-579) only debits remediation cost via a lambda -- it does not call `attempt_remediation()`, does not build a remediation step, does not invoke `_recheck_wiring()`, and does not re-evaluate the gate after remediation.

5. **`execute_sprint()` does not create or pass a TurnLedger** -- The main orchestration loop (`execute_sprint()` at line 843) never instantiates a `TurnLedger`. It does not call `execute_phase_tasks()` (which accepts a `ledger` param). Instead, `execute_sprint()` runs phases as monolithic Claude subprocesses. Only `execute_phase_tasks()` (line 689) threads the ledger, but it is never called from `execute_sprint()`.

### MODERATE GAPS

6. **`wiring_gate_enabled` bool missing** -- Spec defines `wiring_gate_enabled: bool = True` on SprintConfig. Implementation uses `wiring_gate_mode: Literal["off", "shadow", "soft", "full"]` with `"off"` as the disabled state. Functionally equivalent but not spec-compliant naming.

7. **`wiring_gate_grace_period` field missing** -- Spec defines `wiring_gate_grace_period: int = 0` and `SHADOW_GRACE_INFINITE = 999_999`. Neither exists in SprintConfig. The `_resolve_wiring_mode()` hard-codes `grace_period=0` (line 439), but since it is dead code, this is doubly missing.

8. **KPI field names diverge from spec** -- Spec expected `wiring_total_debits`, `wiring_total_credits`, `wiring_net_cost`, `wiring_analyses_run`, `wiring_findings_total`, `wiring_remediations_attempted`. Implementation has different names: `wiring_findings_total`, `wiring_findings_by_type`, `wiring_turns_used`, `wiring_turns_credited`, `whitelist_entries_applied`, `files_skipped`. Missing: `wiring_net_cost`, `wiring_analyses_run`, `wiring_remediations_attempted`.

9. **Migration shim targets wrong fields** -- Spec says to migrate `wiring_gate_mode` -> 3 scope-based fields. Implementation migrates `wiring_budget_turns`, `wiring_remediation_cost`, `wiring_scope` instead. These are internal renames, not the spec's wiring_gate_mode deprecation path.

10. **`_format_wiring_failure()` helper absent** -- Spec requires this helper for formatting wiring findings into remediation prompts. Not implemented.

11. **`_recheck_wiring()` helper absent** -- Spec requires post-remediation re-analysis. Not implemented.

### MINOR GAPS

12. **Wiring verification report frontmatter lacks `enforcement_scope` and `resolved_gate_mode`** -- Spec Section 6.3 requires both. Implementation uses `rollout_mode` instead, which conflates the two concepts.

13. **`check_wiring_report()` convenience wrapper absent** -- Spec (OQ-10) recommends a single wrapper calling all 5 semantic checks. Not implemented.

14. **Semantic check names differ** -- Spec: `zero_unwired_callables`, `zero_orphan_modules`, `zero_unwired_registries`, `total_findings_consistent`. Implementation: `recognized_rollout_mode`, `finding_counts_consistent`, `severity_summary_consistent`, `zero_blocking_findings_for_mode`. Intentional evolution for mode-aware enforcement.

---

## TurnLedger Wiring Gaps (Detailed)

### 1. execute_sprint does not create or thread a ledger

`execute_sprint()` (executor.py:843-1211) is the production entry point. It:
- Iterates `config.active_phases`
- Launches one `ClaudeProcess` per phase
- Never creates a `TurnLedger`
- Never calls `execute_phase_tasks()`

`execute_phase_tasks()` (executor.py:689-798) is the per-task loop that:
- Accepts `ledger: TurnLedger | None`
- Calls `run_post_task_wiring_hook(task, config, result, ledger=ledger)`
- Calls `run_post_task_anti_instinct_hook(task, config, result, ledger=ledger)`

**Gap**: The per-task loop exists and threads the ledger correctly, but the production entry point (`execute_sprint`) never uses it. This means TurnLedger budget tracking is available for testing but not in production sprint execution.

### 2. resolve_gate_mode() usage is dead code

`_resolve_wiring_mode()` at executor.py:420-446 correctly:
- Imports `GateScope`, `resolve_gate_mode` from trailing_gate.py
- Maps scope strings to GateScope enums
- Calls `resolve_gate_mode(scope, grace_period=0)`
- Maps GateMode back to wiring mode strings

But `run_post_task_wiring_hook()` at line 473 reads `config.wiring_gate_mode` directly, bypassing `_resolve_wiring_mode()` entirely. The scope-based resolution never executes.

### 3. attempt_remediation() not used

`attempt_remediation()` exists in `pipeline/trailing_gate.py:354-449` with full retry-once semantics. The wiring hook's BLOCKING branch (executor.py:548-579) implements a simplified inline version:
- Checks `ledger.can_remediate()`
- Debits `config.remediation_cost` via a lambda
- Does NOT call `attempt_remediation()`
- Does NOT build a remediation step via `SprintGatePolicy`
- Does NOT re-run wiring analysis after remediation
- Does NOT use the `RemediationRetryResult` state machine

### 4. DeferredRemediationLog absent from sprint

`DeferredRemediationLog` exists in trailing_gate.py:489-577 with full persistence support. The spec requires shadow mode to append synthetic `TrailingGateResult` entries. The executor:
- Does not import `DeferredRemediationLog`
- Shadow branch only logs via `_wiring_logger.info()`
- No deferred remediation tracking occurs

### 5. TrailingGateRunner not used in execute_sprint

`TrailingGateRunner` exists in trailing_gate.py:88-207 with daemon-thread gate evaluation. `execute_sprint()` never instantiates it. All gate evaluation is synchronous within `run_post_task_wiring_hook()`.

---

## Root Cause Analysis

### Primary Cause: Two Execution Models, One Integration Point

The codebase has two distinct execution models:

1. **Phase-level execution** (`execute_sprint`): Runs each phase as a monolithic Claude subprocess. No per-task granularity. This is the production path.

2. **Task-level execution** (`execute_phase_tasks`): Runs each task as a separate subprocess with budget tracking, wiring hooks, and anti-instinct hooks. This is the per-task path but is not called by the production entry point.

The v3.2 roadmap assumed task-level execution would be the primary path. The wiring hook, TurnLedger integration, and remediation flow were all designed for the per-task loop. But `execute_sprint()` operates at phase granularity, making the per-task hooks unreachable in production.

### Secondary Cause: Sprint Execution Completed in Eval Mode

The execution log shows all 5 phases completed in 24m 31s via an "eval-tasklist-index.md" (line 4 of execution-log.md). This suggests the sprint was executed in an evaluation/test mode that may have used `execute_phase_tasks()` internally, where the hooks would fire. The test passed, but the production path (`execute_sprint()`) remains unwired.

### Tertiary Cause: Incremental Implementation Drift

The implementation evolved the spec's abstractions:
- `wiring_gate_mode` string enum instead of `wiring_gate_enabled` bool + scope-based resolution
- Inline remediation logic instead of `attempt_remediation()` delegation
- Synchronous gate evaluation instead of `TrailingGateRunner` daemon threads
- No `DeferredRemediationLog` because shadow mode only logs

These are pragmatic simplifications, but they leave the trailing gate infrastructure (which exists and works) disconnected from the sprint wiring gate.

---

## Recommendations

### P0 -- Wire execute_sprint to execute_phase_tasks (or thread TurnLedger)

The production entry point must either:
- (A) Create a TurnLedger and call `execute_phase_tasks()` for per-task execution, or
- (B) Create a TurnLedger and call the post-task hooks after each phase subprocess completes

Without this, TurnLedger budget tracking, wiring analysis, and anti-instinct gates do not run in production.

### P0 -- Activate _resolve_wiring_mode()

Replace `mode = config.wiring_gate_mode` (executor.py:473) with `mode = _resolve_wiring_mode(config)`. This enables Goal-5d scope-based mode resolution and makes `wiring_gate_scope` meaningful.

### P1 -- Wire DeferredRemediationLog into shadow mode

Shadow mode should construct synthetic `TrailingGateResult` and append to a `DeferredRemediationLog` instance. This provides the deferred remediation tracking the spec requires for post-sprint analysis.

### P1 -- Wire attempt_remediation() into BLOCKING mode

Replace the inline remediation logic (executor.py:559-575) with a call to `attempt_remediation()` from trailing_gate.py, using `SprintGatePolicy.build_remediation_step()` to construct the remediation step and `_recheck_wiring()` for post-remediation validation.

### P2 -- Add wiring_gate_grace_period and SHADOW_GRACE_INFINITE

Add these to SprintConfig to complete the scope-based enforcement model. Without grace_period, the mode resolution always returns BLOCKING for task scope.

### P2 -- Reconcile KPI field names with spec

Add `wiring_net_cost`, `wiring_analyses_run`, `wiring_remediations_attempted` to GateKPIReport, or document the field name evolution as an intentional deviation.

### P3 -- Add _format_wiring_failure() and _recheck_wiring() helpers

These support the full remediation path. They can be deferred until attempt_remediation() is wired in.
