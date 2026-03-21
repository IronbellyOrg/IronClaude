# Refactoring Plan: Wiring Verification Gate <- TurnLedger Integration (a Design-First)

**Date**: 2026-03-20
**Design authority**: `v3.2/design.md`
**Target spec**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`

---

## Sections Requiring Modification

### Section 4.5: Sprint Integration
- **Current**: Mode-switch pseudocode with bare `wiring_gate_mode` string comparisons (`"off"/"shadow"/"soft"/"full"`). No TurnLedger parameter, no budget tracking, no `resolve_gate_mode()` usage.
- **Change**: Design demands `run_post_task_wiring_hook()` accept a `ledger: TurnLedger | None` parameter, replace string switches with `resolve_gate_mode(scope, grace_period)`, and add debit/credit calls around wiring analysis.
- **Edits**:
  - Replace the `config.wiring_gate_mode` conditional block with the budget flow from design Section 3 (debit before analysis, credit on pass, `resolve_gate_mode()` for enforcement).
  - Replace `wiring_gate_mode: Literal[...]` reference with `wiring_gate_enabled: bool` + `wiring_gate_scope: GateScope` + `wiring_gate_grace_period: int`.
  - Add the `attempt_remediation()` call path for BLOCKING mode failures (design Section 4).
  - Add null-ledger guard contract (design Section 6.1): `if ledger is not None` wrappers around all debit/credit calls.
- **Cross-refs**: Section 5 (File Manifest -- `sprint/executor.py` LOC estimate increases from +25 to ~+60), Section 6.2 (Configuration Contract -- `wiring_gate_mode` field replaced), Section 12 (Tasklist -- T07 scope expands).
- **Risk**: Any downstream consumer that parses `wiring_gate_mode` from config YAML or CLI args breaks. Design Section 9 proposes a `__post_init__` migration with deprecation warning.

### Section 5: File Manifest (sprint/models.py row)
- **Current**: `sprint/models.py` MODIFY +5 lines -- adds `wiring_gate_mode` to `SprintConfig`.
- **Change**: Design demands 3 new fields on `SprintConfig` (`wiring_gate_enabled`, `wiring_gate_scope`, `wiring_gate_grace_period`) plus 3 new fields and 3 new methods on `TurnLedger` (`wiring_gate_cost`, `wiring_gate_credits`, `wiring_gate_scope`, `debit_wiring()`, `credit_wiring()`, `can_run_wiring_gate()`).
- **Edits**: Update row from "+5 lines" to "+35-40 lines". Add note that `TurnLedger` gains domain-specific wiring accounting alongside its generic `debit()`/`credit()` interface.
- **Cross-refs**: Section 4.1 (Data Models -- no change needed, wiring gate models are separate), Section 6.1 (Public API -- `run_wiring_analysis` signature unchanged).
- **Risk**: `debit_wiring`/`credit_wiring` are wiring-specific helpers on a generic class. Cross-release summary recommends making these generic (`debit_gate(gate_name, turns)`). Decide before implementation.

### Section 5: File Manifest (sprint/executor.py row)
- **Current**: `sprint/executor.py` MODIFY +25 lines -- post-task wiring analysis hook.
- **Change**: Design demands threading `ledger` from `execute_phase_tasks()` line 602 into the hook, `resolve_gate_mode()` integration, `attempt_remediation()` call path, and `DeferredRemediationLog` integration for trailing mode.
- **Edits**: Update row from "+25 lines" to "+60-80 lines". Add `SprintGatePolicy` instantiation, `_format_wiring_failure()` helper, `_recheck_wiring()` helper.
- **Cross-refs**: Section 4.5, Section 8 (Rollout -- Phase 3 remediation now has concrete code path).
- **Risk**: Tight coupling between wiring hook and trailing gate infrastructure. Mitigated: `resolve_gate_mode()` and `attempt_remediation()` are already imported at executor.py line 37.

### Section 5: File Manifest (NEW row: sprint/kpi.py)
- **Current**: No `sprint/kpi.py` modification listed.
- **Change**: Design Section 5.1 demands `GateKPIReport` extension with 6 new fields and `build_kpi_report()` gains a `wiring_ledger: TurnLedger | None` parameter.
- **Edits**: Add row: `sprint/kpi.py | MODIFY | +20 | Wiring-specific KPI fields, build_kpi_report() wiring_ledger param`.
- **Cross-refs**: Section 10 (Success Criteria -- needs new SC for KPI observability).
- **Risk**: Low. Additive fields with defaults.

### Section 6.2: Configuration Contract
- **Current**: Defines `WiringConfig` with analysis-time settings. `SprintConfig.wiring_gate_mode` referenced in Section 4.5.
- **Change**: Design demands replacing `wiring_gate_mode` with `wiring_gate_enabled` + `wiring_gate_scope` + `wiring_gate_grace_period`, plus a migration mapping table (design Section 2.3).
- **Edits**: Add the old-mode-to-new-config mapping table. Add `__post_init__` migration note for backward compatibility. Remove `enforcement_mode` from report frontmatter or map it from scope+grace.
- **Cross-refs**: Section 4.3 (Report Format -- `enforcement_mode` frontmatter field needs remapping), Section 8 (Rollout -- phase definitions change from mode labels to scope configurations).
- **Risk**: `enforcement_mode` in report frontmatter is consumed by `WIRING_GATE` required fields. Must either keep it as a derived display field or update `WIRING_GATE.required_frontmatter_fields`.

### Section 8: Rollout Plan
- **Current**: Three phases defined as mode labels (shadow/soft/full) with decision criteria tables. No budget semantics.
- **Change**: Design demands phases expressed as TurnLedger configuration profiles (design Section 5). Transitions require changing one config field (`wiring_gate_scope`), not executor code.
- **Edits**: Replace phase definitions with the GateScope-based configuration table from design Section 5.4. Add budget effect columns (debit on analysis, credit on pass via `reimbursement_rate`). Add the rollout transition checklist showing config-only changes.
- **Cross-refs**: Section 4.5 (Sprint Integration), Section 6.2 (Configuration Contract).
- **Risk**: Existing threshold decision criteria (FPR <15%, etc.) remain valid but now also require budget metrics (wiring_total_debit, wiring_total_credit) for phase advancement decisions.

### Section 9: Testing Strategy
- **Current**: 14 unit tests + 2 integration tests. No TurnLedger-aware test scenarios.
- **Change**: Design Section 7 demands 4 new scenarios in `test_full_flow.py` (Scenarios 5-8) covering wiring pass budget credit, wiring fail remediation, null ledger backward compat, and shadow deferred logging.
- **Edits**: Add Section 9.4 (or extend 9.2) with Scenarios 5-8 from design Section 7.1. Add `tests/sprint/test_models.py` tests for `debit_wiring`, `credit_wiring`, `can_run_wiring_gate`. Update file manifest with `tests/pipeline/test_full_flow.py | MODIFY | +80`.
- **Cross-refs**: Section 12 (Tasklist -- new task or expanded T06/T10).
- **Risk**: `int(1 * 0.8) = 0` makes the Scenario 5 credit assertion counterintuitive. Design acknowledges this (Section 3.2 note). Tests must assert `wiring_gate_credits == 0` not `== 1`.

### Section 10: Success Criteria
- **Current**: SC-001 through SC-011. No criteria for budget accountability or `reimbursement_rate` activation.
- **Change**: Design demands observable TurnLedger accounting and first production consumption of `reimbursement_rate`.
- **Edits**: Add SC-012: "Wiring gate debit/credit reflected in TurnLedger accounting after task completion." Add SC-013: "`reimbursement_rate` consumed in production via `credit_wiring()` -- first non-test consumer." Add SC-014: "KPI report includes wiring-specific budget metrics."
- **Cross-refs**: Section 9 (Testing -- new scenarios verify these criteria).
- **Risk**: None. Additive.

### Section 12: Tasklist Index
- **Current**: T01-T11 with critical path T01->T02/T03/T04->T05->T06->T07->T10->T11.
- **Change**: T07 (Sprint integration) scope expands significantly. New tasks needed for TurnLedger model extensions and KPI extensions.
- **Edits**: Split T07 into: T07a (TurnLedger model extensions: `debit_wiring`, `credit_wiring`, `can_run_wiring_gate`, SprintConfig field replacements), T07b (Sprint integration: ledger threading, `resolve_gate_mode()`, remediation path), T07c (KPI extensions). Add T12: `test_full_flow.py` Scenarios 5-8. Update dependency: T07b depends on T07a + T05; T12 depends on T07b.
- **Cross-refs**: Section 5 (File Manifest), Section 9 (Testing).
- **Risk**: Critical path lengthens. T07a can parallelize with T02-T04.

---

## New Sections Required

### Section 4.7: TurnLedger Budget Flow (NEW)
- **Content**: The complete budget flow diagram from design Section 3 (task complete -> debit -> analysis -> mode resolution -> credit/remediation). This is the central integration artifact and has no home in the current spec.
- **Placement**: After Section 4.6 (Deviation Count Reconciliation), or as a subsection of 4.5.

### Section 6.4: Backward Compatibility Contract (NEW)
- **Content**: The `ledger: TurnLedger | None` behavioral matrix from design Section 6. Defines null-ledger semantics (analysis runs, no budget tracking, direct FAIL on blocking failure with no retry). Critical for phase-level execution mode.
- **Placement**: After Section 6.3 (Gate Contract).

---

## Sections Unchanged

- **Section 1 (Problem Statement)**: Still valid. "Defined but not wired" pattern unaffected.
- **Section 2 (Goals/Non-Goals)**: No change. TurnLedger integration is an implementation approach, not a new goal.
- **Section 3.1-3.3 (Architecture/Data Flow)**: Mostly unchanged. The data flow diagram (Section 3.3) should add a `TurnLedger debit/credit` annotation alongside the existing gate evaluation, but the flow shape is identical.
- **Section 4.1-4.4 (Data Models, Analysis Functions, Report Format, Gate Definition)**: Core wiring analysis is untouched. The `WIRING_GATE` constant and analysis algorithms are orthogonal to TurnLedger.
- **Section 4.6 (Deviation Count Reconciliation)**: Independent companion feature. Zero TurnLedger interaction.
- **Section 7 (Risk Assessment)**: Existing risks unchanged. Design adds 4 new risks (Section 9) that should be appended.
- **Section 11 (Dependency Map)**: Needs one addition: `sprint/models.py (MODIFY)` gains `trailing_gate.py` import for `GateScope`. Otherwise the dependency graph shape is identical.
- **Appendix A, B**: Unchanged.

---

## Interaction Effects

1. **`reimbursement_rate` activation ripple**: Design makes `credit_wiring()` the first production consumer of `reimbursement_rate`. This validates the field's existence but also means changing the default rate (currently 0.8) now has production consequences. All three releases (v3.05, v3.1, v3.2) independently propose consuming this field -- v3.2's `credit_wiring()` should be designed to coexist with v3.1's gate-pass reimbursement (different callers, same field).

2. **`resolve_gate_mode()` replaces string switches**: The wiring gate becomes the first sprint-loop consumer of `resolve_gate_mode()` from `trailing_gate.py`. This creates a precedent: future gates should also use scope-based resolution rather than mode strings. If v3.1 lands first (as cross-release summary recommends), this pattern is already established.

3. **`attempt_remediation()` first production caller**: Design wires `attempt_remediation()` into the sprint loop for the first time. This promotes a tested-but-never-called function to production status. The callable-based interface (`can_remediate`, `debit`) avoids a direct TurnLedger import in `trailing_gate.py`.

4. **KPI report becomes budget-aware**: Adding `wiring_ledger` to `build_kpi_report()` creates a pattern where KPI reports need economic data, not just pass/fail counts. Future gates will want the same pattern.

5. **`SprintConfig` field rename**: Replacing `wiring_gate_mode` with three fields (`enabled`, `scope`, `grace_period`) is a breaking config change. The `__post_init__` migration handles runtime, but any YAML config files, CLI argument parsers, or documentation referencing `wiring_gate_mode` must be updated.

---

## Migration / Backward Compatibility Notes

1. **Config migration**: `SprintConfig.__post_init__` should detect old `wiring_gate_mode` field (if loaded from YAML/dict) and map it to the new triple using design Section 2.3 mapping table. Emit deprecation warning. Remove migration in v3.2+1.

2. **Null ledger safety**: All TurnLedger interactions in the wiring hook MUST be gated behind `if ledger is not None`. This preserves phase-level execution mode (pre-task-ledger sprints) where no ledger exists. The hook signature uses `ledger: TurnLedger | None = None` with backward-compatible default.

3. **Report frontmatter**: The `enforcement_mode` field in report frontmatter (currently expects `"shadow"/"soft"/"full"` string) should be derived from the resolved gate mode rather than the raw config. Options: (a) keep `enforcement_mode` as a display-only string derived from `GateScope` + `grace_period`, or (b) replace with `enforcement_scope` and `enforcement_blocking`. Option (a) is lower risk -- preserves the `WIRING_GATE.required_frontmatter_fields` list unchanged.

4. **Test compatibility**: Existing test_full_flow.py Scenarios 1-4 are unaffected. New Scenarios 5-8 are purely additive. Existing unit tests for `TurnLedger` in `test_models.py` remain valid -- the new fields have defaults and new methods are independent of existing ones.

5. **Cross-release ordering**: If v3.1 (gate-coupled reimbursement) lands first, it establishes the `TurnLedger` instantiation in `execute_sprint()` and the gate-pass reimbursement loop. v3.2 then inherits this and adds wiring-specific tracking on top. If v3.2 lands first (without v3.1), the `ledger` must be instantiated locally or threaded from existing `execute_phase_tasks()` scope where it already exists (line 510).
