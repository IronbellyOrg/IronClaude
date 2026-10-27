# Refactoring Plan: Wiring Verification Gate <- TurnLedger Integration (gamma Interleaved)

---
date: 2026-03-20
spec: wiring-verification-gate-v1.0-release-spec.md
design: v3.2/design.md
analysis: v3.2/analyze.md
brainstorm: v3.2/brainstorm.md
strategy: Proposal A (Documentation-Only TurnLedger Overlay) per cross-release recommendation
---

## Sections Requiring Modification

### Section 4.1: Data Models
- **Current**: Defines `WiringFinding`, `WiringReport` only. No budget-aware fields.
- **Change**: design.md Section 2.2 adds `wiring_gate_cost`, `wiring_gate_credits`, `wiring_gate_scope` fields and `debit_wiring()`, `credit_wiring()`, `can_run_wiring_gate()` methods to `TurnLedger`. The `credit_wiring()` method becomes the **first production consumer** of `reimbursement_rate`.
- **Edits**: Add TurnLedger extension subsection after WiringReport definition. Include the 3 new fields and 3 new methods from design.md Section 2.2. Reference `models.py:488-525` as the base class.
- **Cross-refs**: Section 4.5 (sprint integration), Section 6.2 (config contract), Section 5 (file manifest -- `models.py` LOC estimate increases from +5 to +25).
- **Risk**: `int(1 * 0.8) = 0` makes single-turn reimbursement a no-op. design.md Section 3.2 documents this explicitly; spec must acknowledge the floor behavior.

### Section 4.5: Sprint Integration
- **Current**: Uses bare `wiring_gate_mode` string switches (`shadow`/`soft`/`full`) with no TurnLedger interaction. Mode logic is duplicated inline rather than using `resolve_gate_mode()`.
- **Change**: design.md Section 2.3 replaces `wiring_gate_mode` with `wiring_gate_enabled` + `wiring_gate_scope: GateScope` + `wiring_gate_grace_period`. The hook signature gains a `ledger: TurnLedger | None` parameter (design.md Section 3.1). Budget flow: debit before analysis, credit on pass via `reimbursement_rate`.
- **Edits**: Replace the entire pseudocode block (spec lines 546-569) with design.md Section 3's budget flow. Replace `config.wiring_gate_mode == "shadow"` etc. with `resolve_gate_mode(scope=config.wiring_gate_scope, grace_period=config.wiring_gate_grace_period)`. Thread `ledger` from `execute_phase_tasks()` line 602.
- **Cross-refs**: Section 6.2 (SprintConfig contract changes), Section 8 (rollout plan -- phases become config-only transitions), Section 12 (tasklist T07 scope increases).
- **Risk**: Breaking change to `SprintConfig`. design.md Section 9 recommends `__post_init__` migration from old `wiring_gate_mode` field with deprecation warning.

### Section 5: File Manifest
- **Current**: `sprint/models.py` MODIFY +5 LOC for `wiring_gate_mode` field only.
- **Change**: TurnLedger gains 3 fields + 3 methods (~20 LOC). SprintConfig gains 3 fields replacing 1 (~+5 LOC). `sprint/kpi.py` gains `GateKPIReport` wiring extensions (~+15 LOC).
- **Edits**: Update `models.py` estimate from +5 to +25. Add `sprint/kpi.py` MODIFY +15 row. Total production LOC estimate increases from 360-430 to 390-470.
- **Cross-refs**: Section 12 (tasklist -- add KPI task or fold into T07).
- **Risk**: None. Additive.

### Section 6.2: Configuration Contract (SprintConfig)
- **Current**: Adds `wiring_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"` to SprintConfig.
- **Change**: Replace with `wiring_gate_enabled: bool = True`, `wiring_gate_scope: GateScope = GateScope.TASK`, `wiring_gate_grace_period: int = 999999`. Add mapping table showing old-mode-to-new-config equivalences (design.md Section 2.3).
- **Edits**: Replace the `wiring_gate_mode` field definition. Add the 4-row old-to-new mapping table. Add `__post_init__` migration note.
- **Cross-refs**: Section 4.5 (pseudocode uses new fields), Section 8 (rollout transitions become single-field changes).
- **Risk**: Any downstream consumer of `wiring_gate_mode` breaks. analyze.md confirms only `run_post_task_wiring_hook()` and `run_wiring_safeguard_checks()` read it -- both are v3.2-new code, so no legacy breakage.

### Section 6.3: Gate Contract (Frontmatter)
- **Current**: Frontmatter has `enforcement_mode: shadow|soft|full`.
- **Change**: Replace with `enforcement_scope` and `gate_mode` (derived from `resolve_gate_mode()` output). This aligns report metadata with the actual runtime resolution mechanism.
- **Edits**: Replace `enforcement_mode` row in the frontmatter contract table with `enforcement_scope: GateScope` and `resolved_gate_mode: GateMode`. Update `WIRING_GATE.required_frontmatter_fields` list in Section 4.4.
- **Cross-refs**: Section 4.3 (report format example needs updated frontmatter), Section 4.4 (WIRING_GATE constant).
- **Risk**: Low. No existing consumers of wiring report frontmatter.

### Section 7: Risk Assessment
- **Current**: R1-R6 focus on analysis accuracy and naming conventions.
- **Change**: Add R7 for `int(turns * reimbursement_rate)` floor-to-zero behavior when WIRING_ANALYSIS_TURNS=1. Add R8 for SprintConfig field rename migration.
- **Edits**: Add two rows to risk table.
- **Cross-refs**: Section 9 (testing strategy should cover budget edge cases).
- **Risk**: None. Additive.

### Section 8: Rollout Plan
- **Current**: Three phases described as mode switches with independent threshold tables.
- **Change**: design.md Section 5 reframes phases as SprintConfig field transitions. Shadow->soft->full becomes `wiring_gate_scope` change only. The cross-release summary recommends adopting Unified Audit Gating rollout infrastructure (SS7.1/SS7.2 profiles). Existing rollout framework integration note (spec line 784) already points this direction.
- **Edits**: Replace phase descriptions with TurnLedger budget behavior tables from design.md Section 5.1-5.3. Replace "set `wiring_gate_mode`" instructions with "set `wiring_gate_scope`" + `wiring_gate_grace_period`. Add transition checklist from design.md Section 5.4. Keep existing rollout decision criteria table but note thresholds are initial values for Unified Audit Gating framework.
- **Cross-refs**: Section 4.5 (implementation matches), Section 6.2 (config contract matches).
- **Risk**: None. Simplifies operations (config-only transitions, no code changes per phase).

### Section 9: Testing Strategy
- **Current**: 14+ unit tests for analyzers + 2 integration tests. No budget/ledger test cases.
- **Change**: design.md Section 7 adds 4 new scenarios (5-8) to `test_full_flow.py`: wiring pass with budget credit, wiring fail with remediation, ledger=None backward compat, shadow mode deferred log. Also need unit tests for `debit_wiring()`, `credit_wiring()`, `can_run_wiring_gate()` on TurnLedger.
- **Edits**: Add Section 9.4 "Budget Integration Tests" with scenarios 5-8 from design.md Section 7.1. Add `test_models.py` extension for 3 new TurnLedger methods (design.md checklist item 8). Update test LOC estimate from 310-410 to 400-520.
- **Cross-refs**: Section 10 (new success criteria for budget accounting).
- **Risk**: Test count increase may affect sprint velocity estimates.

### Section 10: Success Criteria
- **Current**: SC-001 through SC-011.
- **Change**: Add SC-012 through SC-015 for TurnLedger integration.
- **Edits**: Add: SC-012 (`debit_wiring`/`credit_wiring` correctly track wiring-specific costs), SC-013 (`reimbursement_rate` consumed in production via `credit_wiring()`), SC-014 (ledger=None backward compatibility -- wiring gate runs without budget tracking), SC-015 (KPI report includes wiring-specific debit/credit totals).
- **Cross-refs**: Section 9 (test mapping for each SC).
- **Risk**: None. Additive.

### Section 11: Dependency Map
- **Current**: Shows `sprint/config.py` as modified. No TurnLedger dependency arrow.
- **Change**: Add `sprint/models.py (TurnLedger)` as a dependency of `audit/wiring_gate.py` (indirect, via executor threading). Add `sprint/kpi.py` as modified. Show `pipeline/trailing_gate.py` as consumed (not modified) for `resolve_gate_mode()`, `attempt_remediation()`, `GateScope`, `GateMode`.
- **Edits**: Add 3 nodes to dependency diagram: `sprint/models.py (MODIFY)`, `sprint/kpi.py (MODIFY)`, `pipeline/trailing_gate.py (CONSUME)`.
- **Cross-refs**: Section 5 (file manifest must match).
- **Risk**: None.

### Section 12: Tasklist Index
- **Current**: T01-T11, critical path T01->T02/03/04->T05->T06->T07->T10->T11.
- **Change**: T01 scope expands (TurnLedger extensions). T07 scope expands (ledger threading, resolve_gate_mode integration, attempt_remediation wiring). Add T12 for KPI extensions. Add T13 for budget integration tests (scenarios 5-8).
- **Edits**: Update T01 description to include TurnLedger field/method additions. Update T07 to reference ledger parameter, resolve_gate_mode, attempt_remediation paths. Add T12 (kpi.py extensions, depends on T01). Add T13 (budget integration tests, depends on T07). Critical path extends: ...->T07->T13->T10->T11.
- **Cross-refs**: Section 5 (file manifest alignment), Section 9 (test strategy alignment).
- **Risk**: Critical path lengthens by 1 task.

---

## New Sections Required

### Section 4.5.1: Backward Compatibility -- TurnLedger is None
- **Content**: design.md Section 6 defines the null-ledger contract. When `ledger is None` (phase-level execution mode), wiring analysis runs without budget tracking, remediation is direct FAIL with no retry. Behavioral matrix from design.md Section 6.2.
- **Placement**: After Section 4.5, before Section 4.6.

### Section 4.5.2: Remediation Path on Wiring Gate Failure
- **Content**: design.md Section 4 defines the `attempt_remediation()` integration for BLOCKING mode failures. Includes `_format_wiring_failure()` and `_recheck_wiring()` helper specs. Budget flow diagram from design.md Section 4.2.
- **Placement**: After Section 4.5.1.

### Section 4.5.3: KPI Report Extensions
- **Content**: design.md Section 5.1 defines 6 new `GateKPIReport` fields for wiring-specific metrics. `build_kpi_report()` gains `wiring_ledger` parameter (design.md Section 7.3).
- **Placement**: After Section 4.5.2.

---

## Sections Unchanged

| Section | Reason |
|---------|--------|
| 1. Problem Statement | TurnLedger integration doesn't change the problem being solved |
| 2. Goals and Non-Goals | Wiring detection goals are orthogonal to budget integration |
| 3.1-3.3 Architecture / Data Flow | Core analysis architecture is unchanged; TurnLedger hooks into the sprint integration point only |
| 4.2 Analysis Functions (4.2.1-4.2.3) | Analyzer algorithms are pure functions with no budget interaction |
| 4.3 Report Format (body) | Report body structure is unchanged; only frontmatter gains scope/mode fields |
| 4.4 Gate Definition (WIRING_GATE) | SemanticCheck functions are content-based, budget-unaware (only frontmatter field list updates) |
| 4.6 Deviation Count Reconciliation | Independent companion; no TurnLedger interaction |
| Appendix A: Forensic Cross-Reference | Unchanged |
| Appendix B: Naming Conventions | Unchanged |

---

## Interaction Effects

### IE-1: `reimbursement_rate` activation sequence
The cross-release summary recommends v3.1 activates `reimbursement_rate` first via general gate-pass reimbursement, with v3.2 consuming it through domain-specific `credit_wiring()`. If v3.2 ships before v3.1, the spec must self-contain the `reimbursement_rate` activation (no dependency on v3.1 infrastructure). design.md is self-contained in this regard.

### IE-2: `resolve_gate_mode()` import path
analyze.md Section 3.3 confirms `resolve_gate_mode()` exists at `trailing_gate.py:593-628` and is already importable from `executor.py` (line 37). No new import coupling.

### IE-3: `attempt_remediation()` production activation
analyze.md confirms `attempt_remediation()` is tested but never called from production. This refactoring makes v3.2 its first production caller (via `run_post_task_wiring_hook` BLOCKING path). If v3.1 activates it first, v3.2 becomes the second caller -- no conflict.

### IE-4: `DeferredRemediationLog` type mismatch
analyze.md Section 5 identifies that `DeferredRemediationLog.append()` takes `TrailingGateResult`, not `WiringReport`. design.md Section 3 resolves this by constructing a synthetic `TrailingGateResult` from wiring findings (`step_id=f"{task.task_id}_wiring"`). The adapter approach (option 1 from analyze.md) is selected.

### IE-5: `SprintGatePolicy` first production instantiation
analyze.md confirms `SprintGatePolicy` exists but is never instantiated in production. design.md Section 4 instantiates it in the BLOCKING remediation path. This is additive -- no conflict with existing code.

### IE-6: `GateKPIReport` wiring extensions
design.md Section 5.1 adds 6 fields. brainstorm.md Proposal B suggests making these generic (`gate_family_counts: dict[str, int]`). For v3.2, the wiring-specific fields are acceptable; generalization deferred to v3.1 if it lands first.

---

## Migration / Backward Compatibility Notes

### BC-1: SprintConfig field rename
`wiring_gate_mode` -> `wiring_gate_enabled` + `wiring_gate_scope` + `wiring_gate_grace_period`. Since `wiring_gate_mode` is new in v3.2 (not yet shipped), there is **no legacy migration burden**. The `__post_init__` migration in design.md Section 9 is defensive only -- needed if any v3.2 development branches already use `wiring_gate_mode`.

### BC-2: TurnLedger is None safety
All new TurnLedger interactions guarded by `if ledger is not None` checks (design.md Section 6.1). Phase-level execution (pre-TurnLedger sprints) continues to work. Behavioral matrix in design.md Section 6.2 is normative.

### BC-3: Report frontmatter evolution
`enforcement_mode` field replaced by `enforcement_scope` + `resolved_gate_mode`. Since no wiring reports exist yet, no migration needed. Gate evaluation functions updated to match.

### BC-4: Test backward compatibility
Existing test scenarios 1-4 in `test_full_flow.py` are unchanged (design.md Section 7.2). New scenarios 5-8 are additive.

### BC-5: Cross-release execution order
If v3.1 (gate-coupled reimbursement) lands first, v3.2 inherits production `reimbursement_rate` activation and `TrailingGateRunner` sprint wiring. If v3.2 lands first, it self-contains these activations (design.md is self-sufficient). No ordering constraint, but v3.1-first is recommended by cross-release summary Section 4.
