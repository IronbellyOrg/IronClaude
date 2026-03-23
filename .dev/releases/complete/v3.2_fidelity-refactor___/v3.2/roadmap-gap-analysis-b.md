# v3.2 Roadmap Gap Analysis (Agent B)

**Date**: 2026-03-21
**Scope**: v3.2 Wiring Verification / Fidelity Refactor
**Method**: Phase-by-phase comparison of executed roadmap against codebase state, with focus on TurnLedger integration gaps

---

## Roadmap Phase-by-Phase Status

### Phase 1: Core Analysis Engine (Data Models + Analyzers)

| Milestone | Roadmap Status | Code Status | Disposition |
|-----------|---------------|-------------|-------------|
| M1.1 — WiringFinding dataclass | Specified | `wiring_gate.py:44-64` — 7 fields including `suppressed` (spec said 6) | PASS (superset) |
| M1.1 — WiringReport dataclass | Specified | `wiring_gate.py:67-135` — includes `files_skipped`, `rollout_mode`, `scan_duration_seconds`, `blocking_count()`, `unsuppressed_findings`, `clean` | PASS (superset) |
| M1.1 — WiringConfig dataclass | Specified | `wiring_config.py:47-71` — all fields present | PASS |
| M1.1 — Whitelist schema + loader | Specified | `wiring_config.py:74-151` — 3-type whitelist (all finding types), mode-aware validation | PASS |
| M1.2 — `analyze_unwired_callables()` | Specified | `wiring_gate.py:313-363` — AST-based, whitelist-aware | PASS |
| M1.2 — `analyze_orphan_modules()` | Specified | `wiring_gate.py:393-516` — includes dual evidence rule (beyond spec) | PASS (superset) |
| M1.2 — `analyze_registries()` | Specified | `wiring_gate.py:553-665` — name + string reference resolution | PASS |
| M1.3 — `emit_report()` | Specified | `wiring_gate.py:715-866` — 16-field frontmatter, `yaml.safe_dump()`, 7 Markdown sections | PASS |
| M1.3 — `WIRING_GATE` constant | Specified | `wiring_gate.py:973-1026` — 16 required fields, 5 semantic checks | **PARTIAL** — field names diverge from spec |
| M1.4 — Unit tests | Specified | `tests/audit/test_wiring_gate.py`, `tests/audit/test_wiring_analyzer.py`, `tests/audit/test_wiring_integration.py`, `tests/audit/fixtures/` | PASS |

**Phase 1 verdict**: PASS with deviations. Core analysis engine is fully implemented. Field naming in `WIRING_GATE` diverges from spec (e.g., `unwired_callable_count` vs spec's `unwired_count`; `rollout_mode` vs spec's `enforcement_scope`/`resolved_gate_mode`). The implementation chose a richer 16-field schema over the spec's 12-field schema. This is functional but breaks frontmatter contract compatibility with the spec.

### Phase 2: Sprint Integration (TurnLedger + Executor Hook)

| Milestone | Roadmap Status | Code Status | Disposition |
|-----------|---------------|-------------|-------------|
| M2.1 — TurnLedger: 3 wiring fields | Specified | `models.py:537-539` — `wiring_turns_used`, `wiring_turns_credited`, `wiring_budget_exhausted` | **PARTIAL** — field names differ from spec |
| M2.1 — `debit_wiring()` | Specified | `models.py:565-576` | PASS |
| M2.1 — `credit_wiring()` with floor | Specified | `models.py:578-593` — `int(turns * rate)` floor verified | PASS |
| M2.1 — `can_run_wiring_gate()` | Specified | `models.py:595+` | PASS |
| M2.1 — SprintConfig: 3 scope-based fields | Specified | `models.py:321-329` — `wiring_gate_mode`, `wiring_gate_scope`, `wiring_analysis_turns`, `remediation_cost` present | **PARTIAL** — see below |
| M2.1 — SprintConfig migration shim | Specified | `models.py:341-343` — alias mapping exists | PASS |
| M2.2 — `run_post_task_wiring_hook()` | Specified | `executor.py:449-582` — shadow/soft/full branches, budget debit/credit | PASS |
| M2.2 — `_resolve_wiring_mode()` | Specified | `executor.py:420-446` — uses `resolve_gate_mode()` | PASS |
| M2.2 — Null-ledger compat | Specified | `executor.py:479-484` — guarded with `ledger is not None` | PASS |
| M2.3 — TurnLedger unit tests | Specified | `tests/sprint/test_models.py` | PASS |

**Phase 2 verdict**: PASS with naming deviations. The critical gap is the **SprintConfig field model**:
- Spec says: `wiring_gate_enabled: bool`, `wiring_gate_scope: GateScope`, `wiring_gate_grace_period: int`
- Code has: `wiring_gate_mode: Literal["off","shadow","soft","full"]`, `wiring_gate_scope: str`, plus `wiring_analysis_turns: int`, `remediation_cost: int`
- The spec's `wiring_gate_enabled` / `wiring_gate_grace_period` / `SHADOW_GRACE_INFINITE` pattern was **NOT implemented**. Instead, the old `wiring_gate_mode` string-switch persists as the primary control mechanism, with `_resolve_wiring_mode()` as a secondary resolver.

### Phase 3: KPI and Deviation Reconciliation

| Milestone | Roadmap Status | Code Status | Disposition |
|-----------|---------------|-------------|-------------|
| M3.1 — 6 wiring KPI fields | Specified | `kpi.py:47-52` — 6 fields present but names differ from spec | **PARTIAL** |
| M3.1 — `build_kpi_report()` signature | Specified | `kpi.py:137-144` — accepts `turn_ledger` and `wiring_report` | PASS |
| M3.2 — `_deviation_counts_reconciled()` | Specified | `roadmap/gates.py:702` + wired into `SPEC_FIDELITY_GATE` at line 1068 | PASS |

**Phase 3 verdict**: PASS. KPI fields use different names (`wiring_findings_total`, `wiring_turns_used`, `wiring_turns_credited`, `wiring_findings_by_type`, `whitelist_entries_applied`, `files_skipped`) vs spec's (`wiring_total_debits`, `wiring_total_credits`, `wiring_net_cost`, `wiring_analyses_run`, `wiring_findings_total`, `wiring_remediations_attempted`). Only 2 of 6 field names match. `wiring_net_cost` and `wiring_remediations_attempted` are **MISSING** from the implementation.

### Phase 4: Integration Testing and Retrospective Validation

| Milestone | Roadmap Status | Code Status | Disposition |
|-----------|---------------|-------------|-------------|
| M4.1 — cli-portify fixture | Specified | `tests/audit/fixtures/unwired_callable.py`, `tests/audit/fixtures/consumer.py` | PASS |
| M4.1 — Budget Scenarios 5-8 | Specified | Partial coverage in `tests/sprint/test_e2e_trailing.py`, `tests/integration/test_sprint_wiring.py` | **PARTIAL** |
| M4.2 — Retrospective validation | Specified | No explicit retrospective report found | **MISSING** |
| M4.3 — Performance benchmark | Specified | No performance benchmark test found | **MISSING** |

**Phase 4 verdict**: PARTIAL. Integration tests exist but specific budget scenarios 5-8 (credit floor, BLOCKING remediation, null-ledger compat, shadow deferred log) are not clearly mapped to dedicated test cases. Retrospective validation (T11) and performance benchmark (SC-009) are not present as standalone artifacts.

### Phase 5: Rollout Validation (Post-Merge)

| Milestone | Roadmap Status | Code Status | Disposition |
|-----------|---------------|-------------|-------------|
| M5.1 — Shadow mode baseline | Post-merge | Not applicable (operational, not code) | N/A |
| M5.2 — Soft mode readiness | Post-merge | Not applicable | N/A |
| M5.3 — Blocking mode authorization | Post-merge | Not applicable | N/A |

---

## Present in Code

### Fully Implemented (matching or exceeding spec)

1. **Three analyzers**: `analyze_unwired_callables()`, `analyze_orphan_modules()`, `analyze_registries()` -- all AST-based, all with whitelist support
2. **Data models**: `WiringFinding`, `WiringReport`, `WiringConfig`, `WhitelistEntry` -- all present with additional fields beyond spec
3. **Report emission**: `emit_report()` with `yaml.safe_dump()` serialization, 16-field frontmatter, 7 Markdown sections
4. **Gate definition**: `WIRING_GATE` with 5 semantic checks -- different from spec's 5 but functionally equivalent
5. **Sprint hook**: `run_post_task_wiring_hook()` with shadow/soft/full branching, debit-before-analysis, credit-on-pass
6. **TurnLedger extensions**: `debit_wiring()`, `credit_wiring()` with floor-to-zero, `can_run_wiring_gate()`
7. **KPI reporting**: `GateKPIReport` with wiring fields, `build_kpi_report()` accepting wiring data
8. **Deviation reconciliation**: `_deviation_counts_reconciled()` wired into `SPEC_FIDELITY_GATE`
9. **Safeguard checks**: `run_wiring_safeguard_checks()` with zero-match warning, whitelist validation, provider dir check
10. **Three-type whitelist**: All finding types suppressed (roadmap OQ-9 resolution adopted)
11. **Dual evidence rule**: `analyze_orphan_modules()` accepts `file_references` parameter (beyond spec)
12. **Test fixtures**: `tests/audit/fixtures/` with unwired_callable, consumer, broken_registry, orphan handler, syntax_error fixtures
13. **Test suite**: `test_wiring_gate.py`, `test_wiring_analyzer.py`, `test_wiring_integration.py`, `test_eval_wiring_multifile.py`

### Beyond Spec (Excess Implementation)

1. **`suppressed` field on WiringFinding** -- spec does not define suppression as a finding-level attribute
2. **`blocking_count(mode)` method** -- mode-aware blocking logic not in spec
3. **`scan_duration_seconds` on WiringReport** -- operational metric not specified
4. **`rollout_mode` on WiringReport** -- carries enforcement context with report
5. **`audit_artifacts_used` frontmatter field** -- not in spec
6. **7-section Markdown body** -- spec shows 3 sections (Unwired, Orphans, Summary)
7. **Dual evidence rule in orphan analysis** -- `file_references` parameter for AST plugin integration

---

## Missing from Code

### Critical Gaps

1. **SprintConfig scope-based fields NOT adopted**: The spec mandates replacing `wiring_gate_mode` with `wiring_gate_enabled: bool`, `wiring_gate_scope: GateScope`, `wiring_gate_grace_period: int`, and `SHADOW_GRACE_INFINITE = 999_999`. None of these exist. The code retains the old `wiring_gate_mode` string literal as primary control.

2. **DeferredRemediationLog not used in shadow mode**: The spec (Section 4.5, shadow path) requires constructing a synthetic `TrailingGateResult` and appending to `DeferredRemediationLog` when shadow mode encounters failures. The `run_post_task_wiring_hook()` shadow branch (executor.py:519-530) only logs findings -- it does NOT call `DeferredRemediationLog.append()`.

3. **SprintGatePolicy remediation path incomplete**: The spec (Section 4.5.3) requires `SprintGatePolicy.build_remediation_step()` integration in the BLOCKING failure path with callable-based `can_remediate`/`debit` interface. The code (executor.py:559-575) uses `ledger.can_remediate()` and `ledger.debit()` directly but does NOT call `SprintGatePolicy.build_remediation_step()` or create a remediation Step. It only debits remediation cost -- no actual remediation subprocess is spawned.

4. **`_format_wiring_failure()` helper missing**: Spec Section 4.5.3 defines this helper for formatting wiring findings into a remediation prompt. Not implemented.

5. **`_recheck_wiring()` helper missing**: Spec Section 4.5.3 defines this for re-running analysis after remediation. Not implemented.

### Medium Gaps

6. **KPI field naming mismatch**: Spec defines `wiring_total_debits`, `wiring_total_credits`, `wiring_net_cost`, `wiring_analyses_run`, `wiring_findings_total`, `wiring_remediations_attempted`. Code has `wiring_turns_used`, `wiring_turns_credited`, `wiring_findings_total`, `wiring_findings_by_type`, `whitelist_entries_applied`, `files_skipped`. Missing: `wiring_net_cost` (computed), `wiring_analyses_run` (counter), `wiring_remediations_attempted` (counter).

7. **TurnLedger field naming mismatch**: Spec defines `wiring_gate_cost`, `wiring_gate_credits`, `wiring_gate_scope`. Code has `wiring_turns_used`, `wiring_turns_credited`, `wiring_budget_exhausted`. The `wiring_gate_scope` field on TurnLedger is missing entirely (it's on SprintConfig instead, as a string).

8. **WIRING_GATE frontmatter contract divergence**: Spec requires 12 fields: `gate`, `target_dir`, `files_analyzed`, `files_skipped`, `unwired_count`, `orphan_count`, `registry_count`, `total_findings`, `analysis_complete`, `enforcement_scope`, `resolved_gate_mode`, `whitelist_entries_applied`. Code defines 16 fields with different names: `unwired_callable_count` (not `unwired_count`), `rollout_mode` (not `enforcement_scope` + `resolved_gate_mode`), plus `critical_count`, `major_count`, `info_count`, `blocking_findings`, `audit_artifacts_used`.

9. **Budget Scenarios 5-8 test coverage**: The spec requires 4 explicit budget integration tests in `tests/pipeline/test_full_flow.py`. These specific scenarios (credit floor, BLOCKING remediation, null-ledger, shadow deferred log) are not present as labeled test methods.

10. **Retrospective validation artifact (T11)**: No validation report confirming the wiring gate detects the original cli-portify no-op bug on the actual `cli_portify/` directory.

11. **Performance benchmark (SC-009)**: No p95 < 5s benchmark test for 50-file packages.

### Low Gaps

12. **`check_wiring_report()` convenience wrapper**: Spec Section 6.1 defines this as a public API entry point. Not implemented -- callers must use `WIRING_GATE` directly via `gate_passed()`.

13. **`--skip-wiring-gate` CLI flag**: Deferred per roadmap OQ-5, but still specified in Phase 2 rollout plan.

---

## TurnLedger Wiring Gaps

### Gap TL-1: No scope-based gate mode resolution in production path

The spec's architectural intent was to replace `wiring_gate_mode` string switches with `resolve_gate_mode(scope, grace_period)` from `trailing_gate.py`. While `_resolve_wiring_mode()` exists at executor.py:420-446, it is **never called** from the production path. The actual `run_post_task_wiring_hook()` reads `config.wiring_gate_mode` directly at line 473:

```python
mode = config.wiring_gate_mode  # reads string literal, ignores _resolve_wiring_mode()
```

The `_resolve_wiring_mode()` function exists but is dead code in the current executor.

### Gap TL-2: Shadow mode does not log to DeferredRemediationLog

Spec Section 4.5 requires:
```python
deferred_result = TrailingGateResult(
    step_id=f"{task.task_id}_wiring",
    gate_name="wiring-verification",
    passed=False,
    findings=report.total_findings,
)
DeferredRemediationLog.append(deferred_result)
```

The shadow branch (executor.py:519-530) only logs via `_wiring_logger.info()` and credits turns. It does not construct a `TrailingGateResult` or append to `DeferredRemediationLog`. This means shadow-mode findings are lost to the KPI/remediation pipeline.

### Gap TL-3: BLOCKING remediation is debit-only (no subprocess, no recheck)

The BLOCKING failure path (executor.py:548-580) debits `remediation_cost` turns via `ledger.debit()` but:
- Does NOT call `SprintGatePolicy.build_remediation_step()` to create a remediation Step
- Does NOT spawn a remediation subprocess
- Does NOT call `_recheck_wiring()` to verify remediation success
- Does NOT credit turns back on successful recheck

The entire remediation lifecycle specified in Section 4.5.3 is unimplemented. The code debits budget as if remediation happened, but no remediation actually occurs.

### Gap TL-4: `wiring_gate_cost` / `wiring_gate_credits` naming mismatch

The spec defines:
- `TurnLedger.wiring_gate_cost` -- Code has `wiring_turns_used`
- `TurnLedger.wiring_gate_credits` -- Code has `wiring_turns_credited`
- `TurnLedger.wiring_gate_scope` -- Code has `wiring_budget_exhausted` (different semantics)

While functionally similar, consumers expecting the spec's field names will not find them.

### Gap TL-5: `GateKPIReport` missing 3 of 6 spec fields

Spec requires: `wiring_total_debits`, `wiring_total_credits`, `wiring_net_cost`, `wiring_analyses_run`, `wiring_findings_total`, `wiring_remediations_attempted`

Code has: `wiring_findings_total`, `wiring_turns_used`, `wiring_turns_credited`, `wiring_findings_by_type`, `whitelist_entries_applied`, `files_skipped`

Missing:
- `wiring_net_cost` (= debits - credits, trivially computable but not surfaced)
- `wiring_analyses_run` (count of analyses, not tracked anywhere)
- `wiring_remediations_attempted` (count of remediation attempts, not tracked since remediation is unimplemented)

---

## Root Cause Analysis

### RCA-1: Spec evolution was not propagated to implementation

The roadmap correctly identified the scope-based field replacement (Section 6.2 of spec) but the implementation retained the older `wiring_gate_mode` string pattern. The `_resolve_wiring_mode()` function was written as a bridge but never wired into the production call path. This suggests the implementer built the resolver but forgot to substitute it into `run_post_task_wiring_hook()`.

### RCA-2: Remediation path was stubbed, not implemented

The BLOCKING mode path debits budget for remediation but performs no actual remediation. This is a classic "debit without delivery" pattern -- the economic model was implemented but the behavioral model was not. The spec's `_format_wiring_failure()`, `_recheck_wiring()`, and `SprintGatePolicy.build_remediation_step()` integration are all absent. Given the sprint execution log shows all 5 phases passed in 24 minutes, the implementation likely prioritized the analysis engine and shadow integration over the full remediation lifecycle.

### RCA-3: Naming divergence from adversarial spec-fidelity findings

The spec-fidelity document (DEV-001) flagged `files_skipped` as an unspecified field addition. The implementation adopted the roadmap's decision (add `files_skipped`) but also renamed multiple other fields without spec amendment. This cascaded into frontmatter contract, KPI, and TurnLedger naming mismatches. The root cause is that the roadmap made several OQ decisions (extended whitelist, removed heuristic, added `files_skipped`) that were implemented but not reconciled back to the spec's formal contracts.

### RCA-4: DeferredRemediationLog integration was overlooked

The shadow mode path logs findings but does not feed them into the trailing gate pipeline via `DeferredRemediationLog`. This means the rollout validation infrastructure (Phase 5) has no shadow-mode data to analyze when deciding on soft/blocking promotion. The spec explicitly designed the shadow-to-DeferredRemediationLog adapter (Gamma IE-4) for this purpose, and its absence breaks the evidence-driven rollout chain.

---

## Recommendations

### P0 — Must Fix for TurnLedger Integration

1. **Wire `_resolve_wiring_mode()` into production path** (TL-1): Replace `mode = config.wiring_gate_mode` at executor.py:473 with a call to `_resolve_wiring_mode(config)`. This enables scope-based gate mode resolution and is a prerequisite for the Unified Audit Gating rollout framework.

2. **Add DeferredRemediationLog integration in shadow mode** (TL-2): In the shadow branch of `run_post_task_wiring_hook()`, construct a `TrailingGateResult` from wiring findings and append to `DeferredRemediationLog`. Without this, shadow-mode data is invisible to the trailing gate pipeline and rollout validation is impossible.

3. **Implement remediation lifecycle or remove debit** (TL-3): Either:
   - (a) Implement `_format_wiring_failure()`, `_recheck_wiring()`, and `SprintGatePolicy.build_remediation_step()` integration in the BLOCKING path, OR
   - (b) Remove the `ledger.debit(config.remediation_cost)` call from the BLOCKING path to stop debiting for non-existent remediation. Option (b) is safer for v3.2; option (a) can be deferred to v3.3.

### P1 — Should Fix

4. **Add SprintConfig scope-based fields**: Introduce `wiring_gate_enabled: bool`, `wiring_gate_grace_period: int`, and `SHADOW_GRACE_INFINITE = 999_999` alongside the existing `wiring_gate_mode`. Add a `__post_init__` that derives `wiring_gate_mode` from the scope-based fields for backward compatibility.

5. **Add missing KPI fields**: Implement `wiring_net_cost` (computed property), `wiring_analyses_run` (counter on TurnLedger), `wiring_remediations_attempted` (counter on TurnLedger).

6. **Align frontmatter field names**: Either update spec to match implementation's 16-field schema, or rename code fields to match spec. The implementation's schema is richer; recommend updating the spec.

### P2 — Nice to Have

7. **Add `check_wiring_report()` convenience wrapper**: Simple function calling all 5 semantic checks, matching spec Section 6.1 public API.

8. **Add retrospective validation artifact (T11)**: Run wiring analysis against actual `cli_portify/` directory and document results.

9. **Add performance benchmark test (SC-009)**: Assert p95 < 5s for 50-file package analysis.

10. **Add labeled budget scenario tests 5-8**: Create explicit test methods in `tests/pipeline/test_full_flow.py` mapping to spec Scenarios 5-8.
