# v3.2 TurnLedger Integration -- Spec Refactoring Tasklist

**Generated**: 2026-03-20
**Source**: `adversarial/merged-output.md` (3-plan adversarial merge)
**Target**: `wiring-verification-gate-v1.0-release-spec.md`
**Executor**: `/sc:task-unified`

---

## Summary

| Metric | Value |
|--------|-------|
| Total tasks | 30 |
| Total waves | 7 |
| Edit tasks | 18 |
| Add-section tasks | 4 |
| Verify tasks | 5 |
| Test tasks | 3 |
| Critical path | Wave 1 -> Wave 2 -> Wave 3 -> Wave 4 -> Wave 5 -> Wave 6 -> Wave 7 |
| Estimated parallel speedup | ~2.8x (Waves 1-2 contain 4-6 parallel tasks; bottleneck waves eliminated) |

## Execution Order

```
Wave 1: T01, T02, T03, T04              (4 independent edits -- data models, config, risk, success criteria)
Wave 2: V01, T05, T06, T07, T08, T10   (verify + 5 edits -- V01 merged in; T10 moved up; intra-wave order: T05->T06, T07->T08)
Wave 3: T09, T11                        (2 edits -- remediation path, sprint integration rewrite)
Wave 4: V02, T20                        (verify + Section 6.1 emit_report() signature fix)
Wave 5: T12, T13, T14, T15, T16, T21   (5 edits + frontmatter scope update; intra-wave order: T12->T15)
Wave 6: V03                             (full spec coherence verification)
Wave 7: V04, T17, T18, T19, V05        (section numbering + 3 test tasks + final sign-off; V04 merged in)
```

**Intra-wave ordering constraints** (tasks within a wave that must execute sequentially):
- Wave 2: T05 must complete before T06 (T06 depends on T05's frontmatter field names). T07 must complete before T08 (T08 references budget flow from T07).
- Wave 5: T12 must complete before T15 (T15's dependency map must match T12's file manifest).

---

## Wave 1: Foundation Edits (no dependencies)

### Task T01: Add TurnLedger Extensions subsection to Section 4.1
- **Type**: add-section
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: 4.1 Data Models
- **Description**: Add subsection "4.1.1 TurnLedger Extensions" after the `WiringReport` dataclass definition (after line 224). Document 3 new fields (`wiring_gate_cost: int = 0`, `wiring_gate_credits: int = 0`, `wiring_gate_scope: GateScope = GateScope.TASK`) and 3 new methods (`debit_wiring(turns: int)`, `credit_wiring(turns: int, rate: float)`, `can_run_wiring_gate(cost: int) -> bool`) on TurnLedger. Reference `models.py:488-525` as base class location. Include explicit note: "`credit_wiring()` uses `int(turns * reimbursement_rate)` which floors to 0 when `turns=1` and `rate=0.8`. Tests must assert `wiring_gate_credits == 0` for single-turn debits." Note that generic `debit_gate()`/`credit_gate()` generalization is deferred to v3.3.
- **Depends on**: none
- **Acceptance criteria**: Section 4.1 contains a subsection documenting all 3 fields and 3 methods with type signatures. Floor-to-zero behavior is explicitly called out. `WiringFinding` and `WiringReport` definitions remain unchanged.
- **Risk**: `credit_wiring()` floor behavior must be documented explicitly to prevent future misunderstanding. Decision on generic vs wiring-specific methods deferred to v3.3.
- **Wave**: 1

### Task T02: Replace `wiring_gate_mode` with scope-based fields in Section 6.2
- **Type**: edit
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: 6.2 Configuration Contract
- **Description**: Replace `wiring_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"` in the `SprintConfig` reference (currently at line 575-576 in Section 4.5 and implied in 6.2) with three fields: `wiring_gate_enabled: bool = True`, `wiring_gate_scope: GateScope = GateScope.TASK`, `wiring_gate_grace_period: int = 0`. Add an old-to-new mapping table showing how each `wiring_gate_mode` value maps to the new fields (e.g., `"off"` -> `enabled=False`; `"shadow"` -> `enabled=True, scope=TASK, grace_period=SHADOW_GRACE_INFINITE`; `"soft"` -> `enabled=True, scope=TASK, grace_period=0`; `"full"` -> `enabled=True, scope=TASK, grace_period=0`). Add `__post_init__` migration note: "Defensive only -- `wiring_gate_mode` is v3.2-new code, not yet shipped. Emit deprecation warning. Remove after 1 release." Define `SHADOW_GRACE_INFINITE = 999_999` as a named constant (per Beta recommendation).
- **Depends on**: none
- **Acceptance criteria**: `wiring_gate_mode` field definition is replaced with 3 new fields. Mapping table present. `SHADOW_GRACE_INFINITE` constant defined with value `999_999` in Section 6.2. Migration note present with deprecation warning detail. Negative criterion: no remaining references to the old `wiring_gate_mode` field in Section 6.2 outside of the mapping table and migration note.
- **Risk**: Only v3.2 development branches affected. No production legacy per Beta's analysis confirming only `run_post_task_wiring_hook()` and `run_wiring_safeguard_checks()` read this field.
- **Wave**: 1

### Task T03: Add R7 and R8 to Section 7 Risk Assessment
- **Type**: edit
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: 7 Risk Assessment
- **Description**: Add two rows to the risk table after R6. R7: Risk="`int(turns * reimbursement_rate)` floors to zero at `WIRING_ANALYSIS_TURNS=1`", Likelihood=High, Impact=Medium, Mitigation="Tests explicitly assert `wiring_gate_credits == 0`; document floor behavior in Section 4.1.1; `reimbursement_rate` effectively inert for single-turn debits unless set to 1.0". R8: Risk="SprintConfig field rename (`wiring_gate_mode` -> 3 fields) breaks development branch configs", Likelihood=Medium, Impact=Low, Mitigation="`__post_init__` migration shim with deprecation warning; v3.2-new code only (no production consumers)".
- **Depends on**: none
- **Acceptance criteria**: Risk table contains R1-R8 (previously R1-R6, now +2). New rows follow existing format.
- **Risk**: None. Additive change.
- **Wave**: 1

### Task T04: Add SC-012 through SC-015 to Section 10
- **Type**: edit
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: 10 Success Criteria
- **Description**: Add 4 rows to success criteria table after SC-011. SC-012: Description="`debit_wiring`/`credit_wiring` correctly track wiring-specific costs", Verification="Unit test: `test_debit_credit_wiring_tracking`". SC-013: Description="`reimbursement_rate` consumed in production via `credit_wiring()`", Verification="Integration test: verify `credit_wiring()` calls `int(turns * reimbursement_rate)`". SC-014: Description="Wiring gate operates correctly when `ledger is None`", Verification="Integration test: `test_wiring_gate_null_ledger`". SC-015: Description="KPI report includes wiring-specific debit/credit totals", Verification="Unit test: `test_kpi_wiring_fields`".
- **Depends on**: none
- **Acceptance criteria**: Success criteria table has SC-001 through SC-015. New entries follow existing format with testable verification methods.
- **Risk**: None. Additive change.
- **Wave**: 1

---

## Wave 2: Cross-Reference Verification, Gate Definition, Frontmatter, Budget Flow, and KPI Sections

### Task V01: Verify Wave 1 internal consistency
- **Type**: verify (lightweight inline check)
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: 4.1, 6.2, 7, 10 (all Wave 1 targets)
- **Description**: Verify cross-references between Wave 1 edits. Check: (1) Section 4.1.1 TurnLedger fields match the field names used in Section 6.2 mapping table. (2) R7 in Section 7 references Section 4.1.1 floor behavior documentation. (3) SC-012 through SC-015 in Section 10 reference test names that correspond to the new TurnLedger methods from Section 4.1.1. (4) `SHADOW_GRACE_INFINITE` constant in Section 6.2 is referenced consistently. (5) No orphaned references to `wiring_gate_mode` remain in Sections 4.1 or 6.2 (Section 4.5 will be updated in Wave 3-4).
- **Depends on**: T01, T02, T03, T04
- **Acceptance criteria**: All 5 specific cross-reference checks pass: (a) field name match between 4.1.1 and 6.2, (b) R7 -> 4.1.1 back-reference, (c) SC-012-SC-015 test names match 4.1.1 methods, (d) `SHADOW_GRACE_INFINITE` referenced consistently, (e) zero orphaned `wiring_gate_mode` references in 4.1/6.2. No contradictions between Wave 1 sections.
- **Risk**: None.
- **Wave**: 2

### Task T05: Update WIRING_GATE.required_frontmatter_fields in Section 4.4
- **Type**: edit
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: 4.4 Gate Definition
- **Description**: In the `WIRING_GATE = GateCriteria(...)` definition, replace `"enforcement_mode"` in `required_frontmatter_fields` list with `"enforcement_scope"` and `"resolved_gate_mode"`. The updated list should contain: `gate`, `target_dir`, `files_analyzed`, `unwired_count`, `orphan_count`, `registry_count`, `total_findings`, `analysis_complete`, `enforcement_scope`, `resolved_gate_mode`, `whitelist_entries_applied`.
- **Depends on**: T01 (TurnLedger may introduce frontmatter requirements), T02 (needs to know the new field names from Section 6.2)
- **Acceptance criteria**: `required_frontmatter_fields` list contains `enforcement_scope` and `resolved_gate_mode` instead of `enforcement_mode`. List count increases from 10 to 11.
- **Risk**: Low. No existing wiring reports to migrate.
- **Wave**: 2 (intra-wave: must complete before T06)

### Task T06: Update frontmatter contract table in Section 6.3 and Section 4.3 report format
- **Type**: edit
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: 6.3 Gate Contract, 4.3 Report Format (frontmatter example)
- **Description**: In the frontmatter contract table (Section 6.3), remove the row for `enforcement_mode` and add two rows: `enforcement_scope` (Type=string, Constraint="GateScope value; derived from `resolve_gate_mode()` at report generation") and `resolved_gate_mode` (Type=string, Constraint="GateMode value; derived from `resolve_gate_mode()` output"). Also update the report format example in Section 4.3 to replace `enforcement_mode: shadow` with `enforcement_scope: task` and `resolved_gate_mode: shadow`.
- **Depends on**: T02 (new field names from Section 6.2), T05 (frontmatter fields must match WIRING_GATE definition)
- **Acceptance criteria**: Frontmatter contract table has `enforcement_scope` and `resolved_gate_mode` rows. No `enforcement_mode` row. Section 4.3 example frontmatter updated to match.
- **Risk**: Low. No existing wiring reports to migrate (Gamma BC-3).
- **Wave**: 2 (intra-wave: must follow T05)

### Task T07: Add new Section 4.5.1 -- TurnLedger Budget Flow
- **Type**: add-section
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: 4.5.1 (NEW -- after Section 4.5)
- **Description**: Add new subsection "4.5.1 TurnLedger Budget Flow" after Section 4.5. Content: (1) Complete budget flow diagram (ASCII box-and-arrow format): task complete -> `debit_wiring(WIRING_ANALYSIS_TURNS)` -> `run_wiring_analysis()` -> `resolve_gate_mode(scope, grace_period)` -> if pass: `credit_wiring(turns, reimbursement_rate)` / if fail+BLOCKING: `attempt_remediation()` / if fail+shadow: `DeferredRemediationLog.append()`. (2) Budget accounting table showing debit/credit amounts per outcome. (3) `run_post_task_wiring_hook()` full signature: `(task: Task, config: SprintConfig, ledger: TurnLedger | None = None) -> WiringReport`. (4) Note: all budget operations gated by `if ledger is not None`. (5) Include explicit BC-5 cross-release ordering note: document that wiring gate budget flow applies per-task within a release; cross-release ordering (e.g., v3.1 -> v3.2 migration) preserves existing TurnLedger state.
- **Depends on**: T01 (TurnLedger field definitions), T02 (config field definitions)
- **Acceptance criteria**: Section 4.5.1 exists with budget flow diagram in ASCII box-and-arrow format, accounting table, and hook signature. All TurnLedger method names match Section 4.1.1. Config field names match Section 6.2. BC-5 cross-release ordering note present.
- **Risk**: Largest documentation addition. Must stay consistent with Section 4.1.1 field definitions.
- **Wave**: 2 (intra-wave: must complete before T08)

### Task T08: Add new Section 4.5.2 -- Backward Compatibility (TurnLedger is None)
- **Type**: add-section
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: 4.5.2 (NEW -- after Section 4.5.1)
- **Description**: Add new subsection "4.5.2 Backward Compatibility -- TurnLedger is None" after Section 4.5.1. Content: Null-ledger behavioral matrix with columns: Operation, `ledger is not None` behavior, `ledger is None` behavior. Rows: (1) Budget debit: debit_wiring() / skip (no tracking), (2) Budget credit: credit_wiring() / skip, (3) Analysis: runs normally / runs normally, (4) Mode resolution: resolve_gate_mode(scope, grace_period) / resolve_gate_mode(scope, grace_period) [same], (5) Blocking failure: attempt_remediation() / direct FAIL (no retry without budget tracking), (6) Shadow failure: DeferredRemediationLog.append() / DeferredRemediationLog.append() [same]. Note: phase-level execution (pre-TurnLedger sprints) continues to work via the `ledger is None` path.
- **Depends on**: T07 (references budget flow from 4.5.1)
- **Acceptance criteria**: Section 4.5.2 exists with complete behavioral matrix. All 6 operation rows present. `ledger is None` path clearly documents "direct FAIL" for blocking failures.
- **Risk**: Must accurately reflect that remediation requires budget tracking.
- **Wave**: 2 (intra-wave: must follow T07)

---

## Wave 3: Remaining New Sections and Sprint Integration

### Task T09: Add new Section 4.5.3 -- Remediation Path on Wiring Gate Failure
- **Type**: add-section
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: 4.5.3 (NEW -- after Section 4.5.2)
- **Description**: Add new subsection "4.5.3 Remediation Path on Wiring Gate Failure" after Section 4.5.2. Content: (1) `attempt_remediation()` integration for BLOCKING mode failures -- callable-based interface with `can_remediate` and `debit` callbacks to avoid direct TurnLedger import in `trailing_gate.py`. (2) `_format_wiring_failure(report: WiringReport) -> str` helper spec -- formats findings into human-readable failure message for remediation step. (3) `_recheck_wiring(target_dir: Path, config: WiringConfig) -> WiringReport` helper spec -- re-runs analysis after remediation attempt. (4) `DeferredRemediationLog` adapter: construct synthetic `TrailingGateResult` with `step_id=f"{task.task_id}_wiring"`, `gate_name="wiring-verification"`, `passed=False`, `findings=report.total_findings` from wiring findings (Gamma IE-4). (5) Budget flow during remediation: additional debit for remediation attempt, credit only if recheck passes. (6) Edge cases: budget exhaustion mid-remediation, subprocess failure, gate re-evaluation.
- **Depends on**: T07 (budget flow context), T08 (null-ledger behavior for remediation)
- **Acceptance criteria**: Section 4.5.3 exists with all 6 content items: (1) `attempt_remediation()` callable-based interface, (2) `_format_wiring_failure()` helper spec, (3) `_recheck_wiring()` helper spec, (4) `DeferredRemediationLog` adapter with `TrailingGateResult` field mapping, (5) budget flow during remediation, (6) edge cases (budget exhaustion, subprocess failure, gate re-evaluation). `DeferredRemediationLog` adapter pattern fully specified. Helper function signatures documented.
- **Risk**: `DeferredRemediationLog` type adapter must construct valid `TrailingGateResult`. This is the most integration-sensitive new section.
- **Wave**: 3

### Task T10: Add new Section 4.5.4 -- KPI Report Extensions
- **Type**: add-section
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: 4.5.4 (NEW -- after Section 4.5.3)
- **Description**: Add new subsection "4.5.4 KPI Report Extensions" after Section 4.5.3. Content: (1) 6 new `GateKPIReport` fields: `wiring_total_debits: int`, `wiring_total_credits: int`, `wiring_net_cost: int`, `wiring_analyses_run: int`, `wiring_findings_total: int`, `wiring_remediations_attempted: int`. (2) `build_kpi_report()` signature update: gains `wiring_ledger: TurnLedger | None = None` parameter. (3) Note: generalization to generic `gate_family_counts: dict[str, int]` deferred to v3.3 (per brainstorm.md Proposal B). (4) New file entry: `sprint/kpi.py` MODIFY +15-20 LOC.
- **Depends on**: T01 (TurnLedger field names)
- **Acceptance criteria**: Section 4.5.4 exists with all 6 KPI fields documented, `build_kpi_report()` signature update, and v3.3 deferral note.
- **Risk**: Low. Additive documentation.
- **Wave**: 2

### Task T11: Rewrite Section 4.5 Sprint Integration pseudocode
- **Type**: edit
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: 4.5 Sprint Integration
- **Description**: Replace the `wiring_gate_mode` string-switch pseudocode block (lines 546-569 in original spec) with TurnLedger-aware budget flow. The new pseudocode should: (1) Change hook signature to gain `ledger: TurnLedger | None = None`. (2) Replace `config.wiring_gate_mode` conditionals with `mode = resolve_gate_mode(config.wiring_gate_scope, config.wiring_gate_grace_period)`. (3) Add `if ledger is not None: ledger.debit_wiring(WIRING_ANALYSIS_TURNS)` before analysis. (4) Add `if ledger is not None: ledger.credit_wiring(WIRING_ANALYSIS_TURNS, config.reimbursement_rate)` on pass. (5) Add `attempt_remediation()` call path for BLOCKING failures with `SprintGatePolicy` instantiation -- **NOTE (IE-5)**: this is the first production instantiation of `SprintGatePolicy` in the wiring gate path; document this as a risk callout in the pseudocode comments, flagging that `SprintGatePolicy`'s constructor requirements and failure modes must be validated against `trailing_gate.py`'s existing usage. (6) Add shadow mode path with `DeferredRemediationLog.append()` using synthetic `TrailingGateResult`. (7) Replace `SprintConfig` field reference from `wiring_gate_mode` to `wiring_gate_enabled`/`wiring_gate_scope`/`wiring_gate_grace_period`. (8) Update the "Configuration" note at the end of Section 4.5 to reference the 3 new fields instead of `wiring_gate_mode`.
- **Depends on**: T02 (config fields), T07 (budget flow), T08 (null-ledger), T09 (remediation path)
- **Acceptance criteria**: No references to `wiring_gate_mode` remain in Section 4.5. Pseudocode uses `resolve_gate_mode()`. Budget debit/credit calls present with null-ledger guards. Remediation path references Section 4.5.3. `SprintConfig` reference updated. `SprintGatePolicy` first-instantiation risk callout present in pseudocode comments.
- **Risk**: Largest single edit. Must stay consistent with all new subsections (4.5.1-4.5.4). SprintGatePolicy first production instantiation is an integration risk (IE-5).
- **Wave**: 3

### Task V02: Verify Sections 4.4, 4.5, 4.5.1-4.5.4, 6.3 consistency
- **Type**: verify
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: 4.4, 4.5, 4.5.1, 4.5.2, 4.5.3, 4.5.4, 6.3
- **Description**: Verify: (1) `WIRING_GATE.required_frontmatter_fields` in 4.4 matches frontmatter contract table in 6.3. (2) Field names in Section 4.5 pseudocode match Section 6.2 config fields. (3) TurnLedger method names in 4.5 pseudocode match Section 4.1.1 definitions. (4) Budget flow in 4.5 matches 4.5.1 diagram. (5) Null-ledger behavior in 4.5 matches 4.5.2 matrix. (6) Remediation path in 4.5 references 4.5.3 correctly. (7) KPI fields in 4.5.4 reference correct TurnLedger fields from 4.1.1. (8) No orphaned references to `enforcement_mode` or `wiring_gate_mode` in any modified section.
- **Depends on**: T05, T06, T07, T08, T09, T10, T11
- **Acceptance criteria**: Zero inconsistencies found. All field names, method names, and cross-references resolve correctly.
- **Risk**: None.
- **Wave**: 4

### Task T20: Update Section 6.1 `emit_report()` signature
- **Type**: edit
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: 6.1 Public API
- **Description**: Update the `emit_report()` signature in Section 6.1 to replace the `enforcement_mode: str = "shadow"` parameter with the new scope-based parameters consistent with the Section 6.2 config field rename. The merged plan's "Sections Unchanged" table lists Section 6.1 as unchanged, but it contains a direct reference to the field being replaced (`enforcement_mode`). This is a gap in the merged plan itself. The parameter should be updated to use `enforcement_scope: GateScope = GateScope.TASK` and `resolved_gate_mode: GateMode` (or equivalent), matching the vocabulary established by T02 and T05.
- **Depends on**: T02 (config field definitions), T05 (frontmatter field names), V02 (cross-reference check confirms the inconsistency)
- **Acceptance criteria**: `emit_report()` signature in Section 6.1 no longer references `enforcement_mode`. New parameter names are consistent with Section 6.2 config fields and Section 4.4 frontmatter fields. T19 ("Sections Unchanged" validation) must be updated to note Section 6.1 is now a modified section.
- **Risk**: Medium. This fix was not in the original merged plan -- it corrects a gap where Section 6.1 was incorrectly listed as unchanged despite containing `enforcement_mode`.
- **Wave**: 4

---

## Wave 5: Manifest, Rollout, Testing, Dependencies, Tasklist, Frontmatter Scope

### Task T12: Update Section 5 File Manifest
- **Type**: edit
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: 5 File Manifest
- **Description**: Update existing rows: `sprint/models.py` LOC from +5 to +30-35. `sprint/executor.py` LOC from +25 to +50-70. Add new rows: `sprint/kpi.py` MODIFY +15-20 LOC, Purpose="GateKPIReport wiring extensions". `tests/pipeline/test_full_flow.py` MODIFY +80-100 LOC, Purpose="Budget integration test scenarios 5-8". Update totals: production code from ~360-430 to ~410-500. Test code from ~310-410 to ~400-520.
- **Depends on**: T10 (KPI section defines kpi.py changes), T11 (sprint integration defines executor.py changes)
- **Acceptance criteria**: File manifest contains updated LOC estimates for models.py and executor.py. Two new rows present. Totals updated.
- **Risk**: None. Bookkeeping.
- **Wave**: 5

### Task T13: Rewrite Section 8 Rollout Plan with config-based phases
- **Type**: edit
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: 8 Rollout Plan
- **Description**: Reframe Phase 1/2/3 subsections as TurnLedger configuration profiles. Each phase should show the `SprintConfig` field values: Phase 1 Shadow: `wiring_gate_enabled=True, wiring_gate_scope=GateScope.TASK, wiring_gate_grace_period=SHADOW_GRACE_INFINITE`. Phase 2 Soft: `wiring_gate_enabled=True, wiring_gate_scope=GateScope.TASK, wiring_gate_grace_period=0`. Phase 3 Full: `wiring_gate_enabled=True, wiring_gate_scope=GateScope.RELEASE, wiring_gate_grace_period=0`. Phase transitions become single-field changes to `wiring_gate_scope` and `wiring_gate_grace_period`. Add budget effect columns to the Rollout Decision Criteria table: "Debit on analysis" and "Credit on pass" for each phase. Add rollout transition checklist. Include explicit BC-5 cross-release ordering documentation: describe how rollout phase transitions across releases preserve TurnLedger state and config compatibility. Keep existing threshold criteria table but note values are initial inputs to Unified Audit Gating framework. Replace all references to `wiring_gate_mode` with the new config fields.
- **Depends on**: T02 (config field definitions), T07 (budget flow context for rollout phases), T11 (sprint integration uses these fields)
- **Acceptance criteria**: All 3 phases described as config profiles with explicit field values. Phase transitions are field-value changes, not prose descriptions. Budget effect columns present. No references to `wiring_gate_mode`.
- **Risk**: Shadow phase uses `SHADOW_GRACE_INFINITE` -- must reference the constant defined in Section 6.2 (T02).
- **Wave**: 5

### Task T14: Add Section 9.4 Budget Integration Tests
- **Type**: edit
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: 9 Testing Strategy
- **Description**: Add new subsection "9.4 Budget Integration Tests" after Section 9.3. Content: (1) Scenario 5 -- wiring pass budget credit: sprint task completes, wiring analysis passes, verify `ledger.wiring_gate_credits` reflects credit. **Critical**: assert `wiring_gate_credits == 0` (not `== 1`) due to `int(1 * 0.8) = 0` floor behavior. (2) Scenario 6 -- wiring fail remediation: wiring analysis fails in BLOCKING mode, `attempt_remediation()` called, verify remediation step created and budget debited. (3) Scenario 7 -- ledger=None backward compat: wiring analysis runs without budget tracking when `ledger is None`, no exceptions raised, task status unaffected. (4) Scenario 8 -- shadow deferred log: wiring fails in shadow mode, `DeferredRemediationLog.append()` called with synthetic `TrailingGateResult`, task status unaffected. Also add to Section 9.1 unit test list: `test_debit_wiring`, `test_credit_wiring`, `test_can_run_wiring_gate` for `test_models.py`. Update test LOC estimate from 310-410 to 400-520.
- **Depends on**: T01 (TurnLedger methods), T09 (remediation path), T11 (sprint integration)
- **Acceptance criteria**: Section 9.4 exists with scenarios 5-8 fully specified. Scenario 5 explicitly asserts `== 0` for credits. Model unit tests added to 9.1 list. LOC estimate updated.
- **Risk**: Test count increase affects sprint velocity estimates.
- **Wave**: 5

### Task T15: Update Section 11 Dependency Map
- **Type**: edit
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: 11 Dependency Map
- **Description**: Add 3 new nodes to the dependency diagram: `sprint/models.py (MODIFY)` for TurnLedger extensions, `sprint/kpi.py (MODIFY)` for GateKPIReport extensions, `pipeline/trailing_gate.py (CONSUME)` for `resolve_gate_mode`, `attempt_remediation`, `GateScope`, `GateMode`. Add edge from `sprint/executor.py` -> `pipeline/trailing_gate.py`. Update the "Zero changes to existing gate infrastructure" note to clarify that `trailing_gate.py` functions are consumed but not modified.
- **Depends on**: T12 (file manifest must match)
- **Acceptance criteria**: Dependency diagram contains all 3 new nodes. Edge from executor.py to trailing_gate.py present. Diagram nodes match file manifest entries.
- **Risk**: None.
- **Wave**: 5 (intra-wave: must follow T12)

### Task T16: Rewrite Section 12 Tasklist Index
- **Type**: edit
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: 12 Tasklist Index
- **Description**: Decompose T07 into: T07a (TurnLedger model extensions -- `sprint/models.py` MODIFY: add 3 fields + 3 methods to TurnLedger, add 3 new fields to SprintConfig), T07b (Sprint integration: ledger threading through executor, `resolve_gate_mode()` replacement, remediation path -- `sprint/executor.py` MODIFY), T07c (KPI extensions -- `sprint/kpi.py` MODIFY: 6 new GateKPIReport fields, `build_kpi_report()` signature update). Add T12: Budget integration test scenarios 5-8 (`tests/pipeline/test_full_flow.py` MODIFY). Update dependency graph: T07a can parallel T02-T04; T07b depends on T07a + T05; T07c depends on T07a; T12 depends on T07b. Update critical path: T01 -> T02/T03/T04/T07a (parallel) -> T05 -> T06 -> T07b -> T10 -> T11 -> T12.
- **Depends on**: T12 (file manifest alignment), T14 (test scenarios)
- **Acceptance criteria**: T07 is split into T07a/T07b/T07c. T12 added. Dependency graph updated. Critical path updated and includes T07a parallelism.
- **Risk**: Critical path lengthens by 1 task. T07a parallelism partially compensates.
- **Wave**: 5

### Task T21: Update spec frontmatter `estimated_scope`
- **Type**: edit
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: Frontmatter
- **Description**: Update spec frontmatter `estimated_scope` from "300-400 lines production code" to "410-500 lines production code" to reflect the expanded scope from TurnLedger integration (new model fields, executor changes, KPI extensions). This edit was previously embedded in V05 (a verify task), which is a process anti-pattern -- verify tasks should not make edits.
- **Depends on**: T12 (file manifest LOC totals must be finalized first)
- **Acceptance criteria**: Frontmatter `estimated_scope` field reads "410-500 lines production code". No other frontmatter fields modified.
- **Risk**: None. Bookkeeping edit.
- **Wave**: 5

---

## Wave 6: Full Spec Coherence Verification

### Task V03: Full spec coherence verification
- **Type**: verify
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: All modified sections
- **Description**: Comprehensive verification pass across entire spec. Check: (1) Zero remaining references to `wiring_gate_mode` outside of migration notes and mapping tables. (2) Zero remaining references to `enforcement_mode` outside of migration notes. (3) All `required_frontmatter_fields` in Section 4.4 have corresponding rows in Section 6.3 frontmatter contract table. (4) All file manifest entries in Section 5 have corresponding tasks in Section 12. (5) All success criteria SC-001 through SC-015 in Section 10 have corresponding test references in Section 9. (6) All risk items R1-R8 in Section 7 have mitigations that reference existing sections. (7) Section 11 dependency map nodes match Section 5 file manifest. (8) LOC estimates in Section 5 are internally consistent (individual rows sum to totals). (9) Section 8 rollout phases reference config fields from Section 6.2. (10) Interaction effects IE-1 through IE-7 from merged plan are addressed by at least one section edit.
- **Depends on**: All T01-T16, T20, T21
- **Acceptance criteria**: Zero inconsistencies. All cross-references resolve.
- **Risk**: None.
- **Wave**: 6

---

## Wave 7: Section Numbering, Validation Tests, and Final Sign-off

### Task V04: Verify section numbering and document structure
- **Type**: verify
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: Document structure
- **Description**: Verify section numbering is correct after inserting new subsections 4.1.1, 4.5.1, 4.5.2, 4.5.3, 4.5.4, and 9.4. Confirm: (1) No duplicate section numbers. (2) New subsections are correctly nested under their parents. (3) Table of contents (if any) is updated. (4) Markdown heading levels are consistent (## for major sections, ### for subsections, #### for sub-subsections). (5) All internal section references (e.g., "see Section 4.5.1") point to correct headings.
- **Depends on**: V03
- **Acceptance criteria**: Document structure is well-formed. All section references resolve.
- **Risk**: None.
- **Wave**: 7

### Task T17: Validate backward compatibility claims
- **Type**: test
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: BC-1 through BC-7 (from merged plan)
- **Description**: For each backward compatibility note (BC-1 through BC-7) from the merged adversarial plan, verify the spec now documents the corresponding handling. Check: BC-1 (SprintConfig field rename) -> Section 6.2 migration note. BC-2 (TurnLedger is None) -> Section 4.5.2. BC-3 (report frontmatter) -> Section 6.3. BC-4 (test compatibility) -> Section 9.4 note that scenarios 1-4 unchanged. BC-5 (cross-release order) -> mention in Section 4.5.1 or 8. BC-6 (DeferredRemediationLog adapter) -> Section 4.5.3. BC-7 (SHADOW_GRACE_INFINITE) -> Section 6.2. Report any BC items not addressed.
- **Depends on**: V03
- **Acceptance criteria**: All 7 BC items (BC-1 through BC-7) have corresponding spec sections with explicit handling documented. "Addressed" means: the spec section contains a concrete description of how the backward compatibility concern is handled, not merely a mention. Minimum: each BC item maps to at least one spec section by number.
- **Risk**: None.
- **Wave**: 7

### Task T18: Validate interaction effects coverage
- **Type**: test
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: IE-1 through IE-7 (from merged plan)
- **Description**: For each interaction effect (IE-1 through IE-7) from the merged adversarial plan, verify the spec documents awareness and handling. Check: IE-1 (reimbursement_rate activation) -> Section 4.1.1 floor note + Section 7 R7. IE-2 (resolve_gate_mode replaces strings) -> Section 4.5 pseudocode. IE-3 (attempt_remediation activation) -> Section 4.5.3. IE-4 (DeferredRemediationLog type mismatch) -> Section 4.5.3 adapter. IE-5 (SprintGatePolicy instantiation) -> Section 4.5 or 4.5.3. IE-6 (GateKPIReport extensions) -> Section 4.5.4. IE-7 (SprintConfig field rename downstream) -> Section 6.2 migration note. Report any IE items not addressed.
- **Depends on**: V03
- **Acceptance criteria**: All 7 IE items (IE-1 through IE-7) have corresponding spec coverage. "Addressed" means: the spec section contains a concrete description of the interaction effect and its handling. IE-5 (SprintGatePolicy first production instantiation) must be covered by an explicit risk callout, not just mechanical inclusion in pseudocode. Minimum: each IE item maps to at least one spec section by number.
- **Risk**: None.
- **Wave**: 7

### Task T19: Validate "Sections Unchanged" assertion
- **Type**: test
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: 1, 2, 3.1-3.3, 4.2, 4.3 (body), 4.6, Appendix A, Appendix B
- **Description**: Verify that sections listed as "unchanged" by all 3 adversarial plans remain unmodified after all edits. Specifically: Section 1 (Problem Statement), Section 2 (Goals/Non-Goals), Sections 3.1-3.3 (Architecture/Data Flow), Section 4.2 (Analysis Functions 4.2.1-4.2.3), Section 4.3 body (report body format -- note: frontmatter example in 4.3 IS modified per T06), Section 4.6 (Deviation Count Reconciliation), Appendix A, Appendix B. Exceptions: (1) Section 4.3 frontmatter example is updated per T06. (2) Section 6.1 (`emit_report()` signature) is now a modified section per T20 -- removed from this unchanged list.
- **Depends on**: V03
- **Acceptance criteria**: All listed sections are unchanged except the 4.3 frontmatter example. Section 6.1 is excluded from this check (modified by T20). No unintended modifications.
- **Risk**: None.
- **Wave**: 7

### Task V05: Final sign-off verification
- **Type**: verify
- **Target file**: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`
- **Section**: Frontmatter + all sections
- **Description**: Final verification. (1) Verify spec `status` field is still `draft`. (2) Verify `estimated_scope` in frontmatter has been updated to "410-500 lines production code" by T21. (3) Confirm all 17 consensus items from merged-output.md are addressed. (4) Confirm all 8 majority-agreement items are addressed (per merged plan assessments). (5) Confirm all 4 contradictions are resolved per merged plan resolutions. (6) Produce a coverage summary (Markdown table format, written to the verification output): columns = merged plan edit ID, target section, tasklist task ID, status (DONE/PARTIAL/MISSING).
- **Depends on**: T17, T18, T19, T21
- **Acceptance criteria**: Frontmatter scope verified as updated. All consensus, majority, and contradiction items from merged plan have spec coverage. Coverage summary produced as a Markdown table with per-edit-ID status.
- **Risk**: None.
- **Wave**: 7

---

## Post-Reflection Amendments

All changes below were applied from the merged reflection (`adversarial/reflection/merged-reflection.md`).
Date: 2026-03-20

1. **Added Task T20: Section 6.1 `emit_report()` signature update** (G3, Medium) -- New edit task in Wave 4 to replace `enforcement_mode` parameter in `emit_report()` with scope-based parameters. The merged plan incorrectly listed Section 6.1 as unchanged. T19 updated to exclude Section 6.1 from the "unchanged" validation list.

2. **Promoted `estimated_scope` frontmatter edit from V05 to new Task T21** (G2, Medium) -- Verify tasks should not make edits. Created explicit edit task T21 in Wave 5. V05 now only verifies the update was made. V05 dependency updated to include T21.

3. **Documented intra-wave ordering constraints** (W3/D4, Medium) -- Added explicit ordering notes to the Execution Order block: T05->T06 and T07->T08 in Wave 2, T12->T15 in Wave 5. Individual task Wave fields annotated with intra-wave sequencing requirements.

4. **Elevated Section 4.3 in T06 header** (G1, Medium) -- T06 task title and Section field now explicitly list "Section 4.3 Report Format" alongside Section 6.3, preventing executor oversight of the buried report format update.

5. **Sharpened 6 vague acceptance criteria** (AC-1 through AC-6):
   - AC-1: V01 acceptance criteria now enumerates all 5 specific cross-reference checks instead of generic "no contradictions."
   - AC-2: T02 acceptance criteria now includes negative criterion ("no remaining references to old field in Section 6.2").
   - AC-3: T07 acceptance criteria now specifies "ASCII box-and-arrow format" for the budget flow diagram.
   - AC-4: V05 acceptance criteria now specifies "Markdown table format" for coverage summary with defined columns.
   - AC-5: T09 acceptance criteria now enumerates all 6 content items by name.
   - AC-6: T17/T18 acceptance criteria now define "addressed" as containing concrete handling descriptions, with minimum of section-number mapping per item.

6. **Applied wave optimizations W1, W2, W4** -- Collapsed V01 from standalone Wave 2 into Wave 2 (W1). Moved T10 from Wave 4 to Wave 2 (W2). Merged V04 from Wave 6 into Wave 7 (W4). Net effect: eliminated single-task wave bottleneck, reduced Wave 4 load, better task distribution in final waves. Updated summary table parallel speedup estimate from ~2.5x to ~2.8x.

7. **Added BC-5 cross-release ordering content to T07 and T13** (G5, Low) -- T07 now includes an explicit BC-5 cross-release ordering note in its description and acceptance criteria. T13 now includes cross-release ordering documentation for rollout phase transitions.

8. **Added IE-5 "first production instantiation" risk flag to T11** (D3, Low) -- T11 description now contains an explicit NOTE callout for SprintGatePolicy's first production instantiation in the wiring gate path, with instruction to validate constructor requirements against `trailing_gate.py`. T11 acceptance criteria and risk updated. T18 acceptance criteria updated to require IE-5 coverage as an explicit risk callout.

9. **Added missing dependencies** (DEP-1, DEP-2, DEP-3):
   - DEP-1: T06 now declares direct dependency on T02 (previously only transitive via T05).
   - DEP-2: T13 now declares direct dependency on T07 (previously only transitive via T11).
   - DEP-3: T05 now declares dependency on T01 (TurnLedger may introduce frontmatter requirements).

10. **Updated task counts** -- Total tasks from 28 to 30 (added T20, T21). Edit tasks from 16 to 18.
