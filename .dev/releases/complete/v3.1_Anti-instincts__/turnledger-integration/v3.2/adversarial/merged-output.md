# Adversarial Compare: v3.2 Wiring Verification Gate <- TurnLedger Integration

**Date**: 2026-03-20
**Plans compared**:
- **Alpha** (Design-First strategy)
- **Beta** (Spec-First strategy)
- **Gamma** (Interleaved strategy)

---

## Consensus (all 3 agree)

High confidence -- all 3 plans agree on both the section affected AND the nature of the change.

1. **Section 4.5 (Sprint Integration)**: Replace `wiring_gate_mode` string-switch pseudocode with `resolve_gate_mode(scope, grace_period)` integration. Hook signature gains `ledger: TurnLedger | None`. Budget flow: debit before analysis, credit on pass. This is the largest single change.

2. **Section 5 (File Manifest)**: `sprint/models.py` LOC estimate increases from +5 to +25-40. `sprint/executor.py` LOC estimate increases. New row for `sprint/kpi.py` MODIFY (+15-20 LOC). Total production LOC estimate rises.

3. **Section 6.2 (Configuration Contract)**: Replace `wiring_gate_mode: Literal["off","shadow","soft","full"]` with three fields: `wiring_gate_enabled: bool`, `wiring_gate_scope: GateScope`, `wiring_gate_grace_period: int`. Add old-to-new mapping table from design Section 2.3. Add `__post_init__` migration note.

4. **Section 8 (Rollout Plan)**: Reframe phases as TurnLedger configuration profiles / SprintConfig field transitions. Phase transitions become single-field changes to `wiring_gate_scope`. Add budget effect columns. Replace prose with config-based phase definitions from design Section 5.

5. **Section 9 (Testing Strategy)**: Add 4 new scenarios (5-8) to `test_full_flow.py`: wiring pass budget credit, wiring fail remediation, ledger=None backward compat, shadow deferred log. Add unit tests for `debit_wiring`, `credit_wiring`, `can_run_wiring_gate`.

6. **Section 10 (Success Criteria)**: Add SC-012+ for TurnLedger budget accounting, `reimbursement_rate` production consumption, ledger=None backward compat, KPI wiring metrics.

7. **Section 12 (Tasklist Index)**: T07 scope expands significantly. New tasks for TurnLedger model extensions, KPI extensions, and integration test scenarios 5-8. Critical path lengthens.

8. **`int(1 * 0.8) = 0` floor risk**: All 3 plans flag that single-turn reimbursement via `credit_wiring()` floors to zero. Tests must assert `wiring_gate_credits == 0` explicitly.

9. **New Section: TurnLedger Budget Flow**: All 3 agree a new subsection is needed to document the complete debit-before-analysis, credit-on-pass, remediation-on-blocking-fail path from design Section 3.

10. **New Section: Backward Compatibility / Null-Ledger Contract**: All 3 agree a new section is needed for the `ledger is None` behavioral matrix from design Section 6.

11. **Sections Unchanged (unanimous)**: Section 1 (Problem Statement), Section 2 (Goals/Non-Goals), Section 3.1-3.3 (Architecture/Data Flow), Section 4.2 (Analysis Functions), Section 4.6 (Deviation Count Reconciliation), Appendix A, Appendix B.

12. **Migration: `wiring_gate_mode` deprecation**: All agree on `__post_init__` migration shim with deprecation warning.

13. **Migration: `ledger is None` safety**: All agree all TurnLedger interactions must be gated behind `if ledger is not None`.

14. **Migration: Test compatibility**: All agree existing scenarios 1-4 are unchanged; new scenarios are additive.

15. **Interaction Effect: `reimbursement_rate` activation**: All 3 identify `credit_wiring()` as the first production consumer of `reimbursement_rate`, with cross-release ordering implications.

16. **Interaction Effect: `resolve_gate_mode()` replaces string switches**: All 3 identify this as a pattern-setting precedent.

17. **Interaction Effect: `attempt_remediation()` production activation**: All 3 identify this as promoting a tested-but-never-called function to production.

---

## Majority Agreement (2 of 3 agree)

Medium confidence -- 2 plans agree, 1 dissents or omits.

### 1. Section 4.1 (Data Models) requires modification
- **Agree**: Beta, Gamma -- both identify Section 4.1 as needing a TurnLedger extensions subsection documenting the 3 new fields and 3 new methods.
- **Dissent**: Alpha omits Section 4.1 from its modification list. Alpha places TurnLedger model changes under Section 5 (File Manifest) only, treating them as implementation detail rather than spec-level data model documentation.
- **Assessment**: Beta/Gamma are correct. The spec's data model section should document all domain models, including TurnLedger extensions. Alpha's omission is a gap.

### 2. Section 11 (Dependency Map) requires modification
- **Agree**: Beta, Gamma -- both explicitly list Section 11 as needing new nodes (`sprint/models.py MODIFY`, `sprint/kpi.py MODIFY`, `pipeline/trailing_gate.py CONSUME`).
- **Dissent**: Alpha mentions Section 11 only in its "Sections Unchanged" list, noting it "needs one addition" but not treating it as a full modification. This is internally inconsistent in Alpha's plan.
- **Assessment**: Beta/Gamma are correct. Adding 3 nodes to the dependency diagram is a modification, not "unchanged."

### 3. Section 6.3 (Gate Contract / Frontmatter) requires modification
- **Agree**: Beta, Gamma -- both identify that `enforcement_mode` frontmatter needs updating to reflect `resolve_gate_mode()` output.
- **Dissent**: Alpha identifies the issue but places it under Section 6.2 cross-refs and migration notes rather than calling Section 6.3 out as a separate modification target.
- **Assessment**: Beta/Gamma's explicit treatment is cleaner. The frontmatter contract table in Section 6.3 is a distinct artifact that should be listed as modified.

### 4. Section 7 (Risk Assessment) requires modification
- **Agree**: Gamma explicitly lists Section 7 as needing R7 (floor-to-zero) and R8 (field rename migration). Alpha mentions "4 new risks from design Section 9 should be appended" in its unchanged list.
- **Dissent**: Beta omits Section 7 from both its modification list and unchanged list, stating "existing risks unchanged (new risks added inline to modified sections)."
- **Assessment**: Gamma is most correct. New risks should be added to the canonical risk table (Section 7), not scattered inline. Alpha recognizes this but misclassifies the section as "unchanged."

### 5. Tasklist decomposition strategy
- **Agree**: Alpha, Gamma -- split T07 into sub-tasks (Alpha: T07a/T07b/T07c; Gamma: expand T01 + keep T07 expanded).
- **Dissent**: Beta proposes splitting T01 instead (T01a/T01b) and adding T12/T13 as new tasks, keeping T07 as a single expanded task.
- **Assessment**: Alpha's T07a/T07b/T07c split is most granular and enables parallel execution (T07a parallels T02-T04). Beta's T01 split is valid for model-layer separation. Merged plan adopts Alpha's approach for T07 with Beta's T12/T13 additions.

### 6. executor.py LOC estimate
- **Agree**: Alpha, Beta -- Alpha estimates +60-80 LOC, Beta estimates +40 LOC for executor.py.
- **Dissent**: Gamma does not provide a specific executor.py LOC estimate, deferring to the overall total.
- **Assessment**: Alpha's higher estimate is more realistic given the remediation path, `_format_wiring_failure()`, and `_recheck_wiring()` helpers. Use +50-70 as merged estimate.

### 7. New Section: Remediation Path
- **Agree**: Alpha (mentions remediation in Section 4.5 edits), Gamma (proposes explicit Section 4.5.2 for remediation path).
- **Dissent**: Beta folds remediation into the Section 4.5 modification without a separate subsection.
- **Assessment**: Gamma is correct that remediation warrants its own subsection given its complexity (helper specs, budget flow diagram).

### 8. New Section: KPI Report Extensions
- **Agree**: Alpha (mentions KPI in Section 5 manifest), Gamma (proposes explicit Section 4.5.3 for KPI extensions).
- **Dissent**: Beta mentions KPI in Section 5 and testing but does not propose a dedicated subsection.
- **Assessment**: Gamma's explicit subsection is better for spec completeness.

---

## Unique Findings (only 1 plan identified)

Flag for manual review.

### Alpha-only

1. **`debit_wiring`/`credit_wiring` genericity concern**: Alpha flags that wiring-specific helpers on a generic class may warrant generalization to `debit_gate(gate_name, turns)`. Cross-release summary recommends this. Beta's migration section acknowledges this ("keep wiring-specific for v3.2; generalize in v3.3") but Alpha frames it as a decision to make before implementation.

2. **`SprintGatePolicy` instantiation**: Alpha mentions this in executor.py edits. Gamma identifies it as an interaction effect (IE-5). Beta omits entirely.

3. **Report frontmatter option analysis**: Alpha provides two options for `enforcement_mode` handling: (a) keep as derived display field, (b) replace with `enforcement_scope` + `enforcement_blocking`. Alpha recommends option (a) for lower risk.

### Beta-only

1. **`SHADOW_GRACE_INFINITE` constant**: Beta recommends defining a named constant for the shadow phase `grace_period=999999` magic number. Neither Alpha nor Gamma flag this.

2. **Section 9.4 as separate subsection**: Beta explicitly names the new testing subsection "9.4 TurnLedger Integration Tests" with clear separation rationale (different integration surface than 9.1/9.2).

3. **Explicit confirmation that `wiring_gate_mode` consumers are v3.2-new code**: Beta's Section 6.2 risk note confirms (via analyze.md) that only `run_post_task_wiring_hook()` and `run_wiring_safeguard_checks()` read `wiring_gate_mode` -- both are new, so no legacy breakage. Alpha and Gamma warn about breakage more generally without this confirmation.

### Gamma-only

1. **IE-4: `DeferredRemediationLog` type mismatch**: Gamma uniquely identifies that `DeferredRemediationLog.append()` takes `TrailingGateResult`, not `WiringReport`, and documents the adapter approach (synthetic `TrailingGateResult` with `step_id=f"{task.task_id}_wiring"`). Critical integration detail missed by Alpha and Beta.

2. **IE-5: `SprintGatePolicy` first production instantiation**: Gamma explicitly documents this as an interaction effect. Alpha mentions it in passing; Beta omits.

3. **BC-1 refinement -- no legacy migration burden**: Gamma uniquely observes that since `wiring_gate_mode` is new in v3.2 (not yet shipped), there is no actual legacy migration burden. The `__post_init__` migration is purely defensive for development branches. Alpha and Beta treat the migration as production-facing.

4. **Section 4.4 (Gate Definition) may need frontmatter field list update**: Gamma notes that `WIRING_GATE.required_frontmatter_fields` needs updating if frontmatter fields change. Alpha and Beta miss this.

5. **`models.py:488-525` reference**: Gamma provides exact line references for the TurnLedger base class, grounding the refactoring in concrete code locations.

6. **Explicit brainstorm.md reference**: Gamma cross-references brainstorm.md proposals (e.g., Proposal B for generic `gate_family_counts`), providing richer provenance than Alpha or Beta.

---

## Contradictions

### 1. Section 6.3 (Frontmatter) -- preserve vs replace `enforcement_mode`
- **Alpha**: Recommends keeping `enforcement_mode` as a derived display field (option a) to preserve `WIRING_GATE.required_frontmatter_fields` unchanged. Lower risk.
- **Gamma**: Recommends replacing `enforcement_mode` with `enforcement_scope` + `resolved_gate_mode`. Notes "no existing consumers" makes this safe.
- **Beta**: Takes a middle position -- notes `enforcement_mode` value is derived from `resolve_gate_mode()` but keeps the field name, just changing the source.
- **Resolution**: Gamma's observation that no wiring reports exist yet is decisive. Since there are no consumers, the cleaner approach (Gamma) is safe. However, Alpha's concern about `WIRING_GATE.required_frontmatter_fields` is valid and must be addressed. **Merged decision**: Replace with `enforcement_scope` + `resolved_gate_mode` AND update `WIRING_GATE.required_frontmatter_fields`.

### 2. models.py LOC estimate
- **Alpha**: +35-40 LOC (TurnLedger + SprintConfig combined)
- **Beta**: +25 LOC
- **Gamma**: +25 LOC
- **Resolution**: Alpha includes SprintConfig field additions in the models.py estimate (3 new fields replacing 1 = +5 LOC). Beta/Gamma count SprintConfig separately. Using Alpha's combined estimate (+30-35) is more accurate for the file manifest.

### 3. Tasklist structure (T07 split vs T01 split)
- **Alpha**: Split T07 into T07a/T07b/T07c.
- **Beta**: Split T01 into T01a/T01b, add T12/T13.
- **Gamma**: Expand T01 and T07 in-place, add T12/T13.
- **Resolution**: These are compatible approaches. Merged plan: Split T07 (Alpha's approach for parallelism) AND add T12/T13 (Beta/Gamma for KPI and test tasks).

### 4. Where to document Section 3.3 (Data Flow) changes
- **Alpha**: States Section 3.3 "should add a TurnLedger debit/credit annotation" but classifies as unchanged.
- **Beta**: Lists Section 3.3 as unchanged ("budget is a parallel concern").
- **Gamma**: Lists Section 3.1-3.3 as unchanged.
- **Resolution**: Minor annotation is not a structural change. Classify as unchanged with a note that an annotation may be added for clarity.

---

## Completeness Assessment

### Which plan was most thorough?
**Gamma** (Interleaved) was most thorough overall:
- Only plan to identify the `DeferredRemediationLog` type mismatch (IE-4)
- Only plan to note `WIRING_GATE.required_frontmatter_fields` needs updating
- Provided exact code line references (`models.py:488-525`, spec lines 546-569)
- Cross-referenced brainstorm.md proposals, not just design.md
- Most new sections proposed (3 vs 2 for Alpha and Beta)
- Most interaction effects documented (6 vs 5 for Alpha/Beta)

### Which plan identified the most cross-cutting concerns?
**Gamma** with 6 explicit interaction effects (IE-1 through IE-6), including the unique `DeferredRemediationLog` type mismatch and `SprintGatePolicy` instantiation findings.

**Alpha** is a close second with strong cross-release ordering analysis and the `debit_gate()` genericity concern.

### Were any spec sections missed by ALL plans?
- **Section 4.4 (Gate Definition)**: Only Gamma notes that `WIRING_GATE.required_frontmatter_fields` needs updating if frontmatter changes. Alpha and Beta miss this entirely. This is a real gap -- if `enforcement_mode` is replaced, the constant that validates it must be updated.
- **Section 3.3 (Data Flow diagram)**: Alpha notes a minor annotation is needed but all 3 classify as unchanged. This is arguably correct (the annotation is cosmetic).
- **CLI argument parsing**: Alpha mentions it in passing (Section 6.2 risk), but no plan provides a concrete edit for CLI flags that might reference `wiring_gate_mode`. If any CLI arg parser exists, it needs updating.

---

## Merged Refactoring Plan

### Section 4.1: Data Models
- **Change**: Add subsection "4.1.1 TurnLedger Extensions" documenting 3 new fields (`wiring_gate_cost`, `wiring_gate_credits`, `wiring_gate_scope`) and 3 new methods (`debit_wiring()`, `credit_wiring()`, `can_run_wiring_gate()`) on TurnLedger. Explicitly acknowledge `int(turns * reimbursement_rate)` floor-to-zero behavior for single-turn debits.
- **Edits**: Add subsection after `WiringReport` definition. Reference `models.py:488-525` as the base class. Keep `WiringFinding`/`WiringReport` unchanged.
- **Cross-refs**: Section 4.5, Section 5 (models.py LOC +30-35), Section 6.2, Section 12.
- **Risk**: `credit_wiring()` floor behavior must be documented explicitly. Decision on generic vs wiring-specific methods deferred to v3.3.

### Section 4.4: Gate Definition (WIRING_GATE constant)
- **Change**: Update `WIRING_GATE.required_frontmatter_fields` to reflect frontmatter field changes (`enforcement_scope`, `resolved_gate_mode` replacing `enforcement_mode`).
- **Edits**: Replace `enforcement_mode` in the required fields list with `enforcement_scope` and `resolved_gate_mode`.
- **Cross-refs**: Section 6.3 (frontmatter contract).
- **Risk**: Low. No existing wiring reports to migrate.

### Section 4.5: Sprint Integration
- **Change**: Replace `wiring_gate_mode` string-switch pseudocode with TurnLedger-aware budget flow. Hook signature gains `ledger: TurnLedger | None = None`. Replace `config.wiring_gate_mode` conditionals with `resolve_gate_mode(scope, grace_period)`. Add debit/credit calls around wiring analysis. Add `attempt_remediation()` call path for BLOCKING failures. Add `DeferredRemediationLog` integration using synthetic `TrailingGateResult` adapter (Gamma IE-4).
- **Edits**: Replace pseudocode block (spec lines 546-569) with design Section 3 budget flow. Add `SprintGatePolicy` instantiation, `_format_wiring_failure()` helper, `_recheck_wiring()` helper. Add null-ledger guard contract (`if ledger is not None` wrappers).
- **Cross-refs**: Section 5 (executor.py +50-70 LOC), Section 6.2, Section 8, Section 12.
- **Risk**: Largest single change. `DeferredRemediationLog` type adapter must construct valid `TrailingGateResult` from wiring findings. `ledger is None` path must preserve phase-level execution mode.

### Section 5: File Manifest
- **Change**: Update LOC estimates. `sprint/models.py` from +5 to +30-35. `sprint/executor.py` from +25 to +50-70. Add `sprint/kpi.py` MODIFY +15-20. Add `tests/pipeline/test_full_flow.py` MODIFY +80-100. Total production code estimate from ~360-430 to ~410-500.
- **Edits**: Update existing rows, add 2 new rows.
- **Cross-refs**: Section 12 (tasklist alignment).
- **Risk**: None. Bookkeeping.

### Section 6.2: Configuration Contract
- **Change**: Replace `wiring_gate_mode: Literal[...]` with `wiring_gate_enabled: bool = True`, `wiring_gate_scope: GateScope = GateScope.TASK`, `wiring_gate_grace_period: int = 0`. Add old-to-new mapping table. Add `__post_init__` migration note (defensive only -- `wiring_gate_mode` is v3.2-new code per Beta's analysis).
- **Edits**: Replace field definition, add mapping table, add migration note.
- **Cross-refs**: Section 4.5, Section 8.
- **Risk**: Only v3.2 development branches are affected (no production legacy). Define `SHADOW_GRACE_INFINITE = 999_999` constant per Beta recommendation.

### Section 6.3: Gate Contract (Frontmatter)
- **Change**: Replace `enforcement_mode` with `enforcement_scope: GateScope` and `resolved_gate_mode: GateMode` in the frontmatter contract table. These are derived from `resolve_gate_mode()` output at report generation time.
- **Edits**: Update frontmatter contract table. Update Section 4.3 report format example.
- **Cross-refs**: Section 4.4 (`WIRING_GATE.required_frontmatter_fields` must match).
- **Risk**: Low. No existing wiring reports to migrate (Gamma BC-3).

### Section 7: Risk Assessment
- **Change**: Add R7 (`int(turns * reimbursement_rate)` floor-to-zero at WIRING_ANALYSIS_TURNS=1) and R8 (SprintConfig field rename migration for development branches).
- **Edits**: Add 2 rows to risk table.
- **Cross-refs**: Section 9 (tests cover budget edge cases).
- **Risk**: None. Additive.

### Section 8: Rollout Plan
- **Change**: Replace phase descriptions with TurnLedger budget behavior tables from design Section 5. Phase transitions become `wiring_gate_scope` field changes. Add transition checklist. Keep existing threshold criteria with budget metrics column added.
- **Edits**: Replace Phase 1/2/3 subsections with config-based definitions. Add rollout transition checklist. Add budget effect columns (debit on analysis, credit on pass).
- **Cross-refs**: Section 4.5, Section 6.2.
- **Risk**: Shadow phase uses `grace_period=999999` -- define as `SHADOW_GRACE_INFINITE` constant.

### Section 9: Testing Strategy
- **Change**: Add Section 9.4 "Budget Integration Tests" with scenarios 5-8 from design Section 7.1 (wiring pass credit, wiring fail remediation, ledger=None compat, shadow deferred log). Add `test_models.py` tests for `debit_wiring`, `credit_wiring`, `can_run_wiring_gate`. Scenario 5 must assert `wiring_gate_credits == 0` (not `== 1`) due to floor behavior.
- **Edits**: Add Section 9.4. Add model unit tests to Section 9.1 list. Update test LOC estimate from 310-410 to 400-520.
- **Cross-refs**: Section 10 (success criteria mapping), Section 5 (test file manifest), Section 12.
- **Risk**: Test count increase affects sprint velocity estimates.

### Section 10: Success Criteria
- **Change**: Add SC-012 through SC-015.
- **Edits**: SC-012: `debit_wiring`/`credit_wiring` correctly track wiring-specific costs. SC-013: `reimbursement_rate` consumed in production via `credit_wiring()`. SC-014: Wiring gate operates correctly when `ledger is None`. SC-015: KPI report includes wiring-specific debit/credit totals.
- **Cross-refs**: Section 9 (test scenarios verify each SC).
- **Risk**: None. Additive.

### Section 11: Dependency Map
- **Change**: Add 3 nodes: `sprint/models.py (MODIFY)` for TurnLedger extensions, `sprint/kpi.py (MODIFY)` for GateKPIReport extensions, `pipeline/trailing_gate.py (CONSUME)` for `resolve_gate_mode`, `attempt_remediation`, `GateScope`, `GateMode`. Add edge from `sprint/executor.py` -> `pipeline/trailing_gate.py`.
- **Edits**: Add nodes and edges to dependency diagram.
- **Cross-refs**: Section 5 (file manifest must match).
- **Risk**: None.

### Section 12: Tasklist Index
- **Change**: Split T07 into T07a (TurnLedger model extensions), T07b (Sprint integration: ledger threading, `resolve_gate_mode()`, remediation path), T07c (KPI extensions). Add T12: Budget integration test scenarios 5-8. Update critical path: T07a can parallel T02-T04; T07b depends on T07a + T05; T12 depends on T07b.
- **Edits**: Decompose T07, add T12. Update dependency graph and critical path.
- **Cross-refs**: Section 5, Section 9.
- **Risk**: Critical path lengthens by 1 task. T07a parallelism partially compensates.

---

## New Sections Required (merged)

### Section 4.5.1: TurnLedger Budget Flow (NEW)
- **Content**: Complete budget flow diagram from design Section 3 (task complete -> debit -> analysis -> mode resolution -> credit/remediation). Budget accounting table (design Section 3.2). `run_post_task_wiring_hook()` full signature.
- **Placement**: After Section 4.5.
- **Source**: All 3 plans agree.

### Section 4.5.2: Backward Compatibility -- TurnLedger is None (NEW)
- **Content**: Null-ledger behavioral matrix from design Section 6.2. When `ledger is None`, wiring analysis runs without budget tracking, remediation is direct FAIL with no retry. Documents phase-level execution mode.
- **Placement**: After Section 4.5.1.
- **Source**: All 3 plans agree.

### Section 4.5.3: Remediation Path on Wiring Gate Failure (NEW)
- **Content**: `attempt_remediation()` integration for BLOCKING mode failures. `_format_wiring_failure()` and `_recheck_wiring()` helper specs. `DeferredRemediationLog` adapter using synthetic `TrailingGateResult` (Gamma IE-4). Budget flow during remediation.
- **Placement**: After Section 4.5.2.
- **Source**: Gamma explicit, Alpha implicit. Beta omits dedicated subsection.

### Section 4.5.4: KPI Report Extensions (NEW)
- **Content**: 6 new `GateKPIReport` fields for wiring-specific metrics. `build_kpi_report()` gains `wiring_ledger: TurnLedger | None` parameter. Deferred generalization to v3.3.
- **Placement**: After Section 4.5.3.
- **Source**: Gamma explicit. Alpha/Beta fold into file manifest.

---

## Sections Unchanged (merged, verified by majority)

All 3 plans agree these sections require no modification:

| Section | Reason |
|---------|--------|
| 1. Problem Statement | TurnLedger integration doesn't change the problem definition |
| 2. Goals and Non-Goals | Wiring analysis goals unchanged; TurnLedger is integration concern |
| 3.1-3.3 Architecture / Data Flow | Core analysis architecture unchanged (minor annotation possible in 3.3) |
| 4.2 Analysis Functions (4.2.1-4.2.3) | Analyzer algorithms are pure functions; zero TurnLedger dependency |
| 4.3 Report Format (body) | Report body unchanged; frontmatter changes covered in Section 6.3 |
| 4.6 Deviation Count Reconciliation | Independent companion; no TurnLedger interaction |
| 6.1 Public API | `run_wiring_analysis()` and `emit_report()` signatures unchanged |
| Appendix A: Forensic Cross-Reference | Unchanged |
| Appendix B: Naming Conventions | Unchanged |

---

## Interaction Effects (merged)

### IE-1: `reimbursement_rate` activation sequence (all 3)
`credit_wiring()` becomes the first production consumer of `reimbursement_rate`. If v3.1 lands first, it establishes the activation pattern; v3.2 becomes the second consumer. If v3.2 lands first, it self-contains the activation. Changing the default rate (0.8) now has production consequences. The floor-to-zero issue at WIRING_ANALYSIS_TURNS=1 means the rate is effectively inert for single-turn debits unless set to 1.0.

### IE-2: `resolve_gate_mode()` replaces string switches (all 3)
The wiring gate becomes the first sprint-loop consumer of `resolve_gate_mode()` from `trailing_gate.py`. Sets precedent: future gates should use scope-based resolution, not mode strings. Import already exists at `executor.py` line 37 (Gamma confirm).

### IE-3: `attempt_remediation()` production activation (all 3)
Promotes a tested-but-never-called function to production. The callable-based interface (`can_remediate`, `debit`) avoids direct TurnLedger import in `trailing_gate.py`. Must handle edge cases: budget exhaustion mid-remediation, subprocess failure, gate re-evaluation.

### IE-4: `DeferredRemediationLog` type mismatch (Gamma only -- critical)
`DeferredRemediationLog.append()` takes `TrailingGateResult`, not `WiringReport`. Resolved via synthetic `TrailingGateResult` adapter with `step_id=f"{task.task_id}_wiring"`. This adapter pattern must be implemented in the executor hook.

### IE-5: `SprintGatePolicy` first production instantiation (Alpha, Gamma)
`SprintGatePolicy` exists but is never instantiated in production. Design Section 4 instantiates it in the BLOCKING remediation path. Additive -- no conflict with existing code.

### IE-6: `GateKPIReport` wiring extensions (Gamma)
6 new fields are wiring-specific. Generalization to generic `gate_family_counts: dict[str, int]` deferred to v3.1/v3.3.

### IE-7: `SprintConfig` field rename downstream (Alpha)
Replacing `wiring_gate_mode` with three fields is a breaking config change for any YAML config files, CLI argument parsers, or documentation. However, Beta confirms only v3.2-new code reads this field, so no production legacy. The `__post_init__` migration is defensive only.

---

## Migration / Backward Compatibility Notes (merged)

### BC-1: SprintConfig field rename
`wiring_gate_mode` -> `wiring_gate_enabled` + `wiring_gate_scope` + `wiring_gate_grace_period`. Since `wiring_gate_mode` is v3.2-new code (not yet shipped), no production migration burden (Gamma). Add `__post_init__` migration as defensive measure for development branches. Emit deprecation warning. Remove after 1 release.

### BC-2: TurnLedger is None safety
All TurnLedger interactions guarded by `if ledger is not None`. Phase-level execution (pre-TurnLedger sprints) continues to work. Direct FAIL on blocking failure when no ledger (no remediation without budget tracking). Behavioral matrix from design Section 6.2 is normative.

### BC-3: Report frontmatter evolution
`enforcement_mode` replaced by `enforcement_scope` + `resolved_gate_mode`. No existing wiring reports to migrate. `WIRING_GATE.required_frontmatter_fields` updated to match.

### BC-4: Test backward compatibility
Existing `test_full_flow.py` scenarios 1-4 unchanged. New scenarios 5-8 additive. Existing `test_models.py` TurnLedger tests valid -- new fields have defaults, new methods are independent.

### BC-5: Cross-release execution order
v3.1-first is recommended (establishes `reimbursement_rate` activation and `TrailingGateRunner` wiring). If v3.2 lands first, design is self-sufficient via `ledger is None` path. No hard ordering constraint.

### BC-6: `DeferredRemediationLog` adapter
Shadow mode deferred logging requires constructing synthetic `TrailingGateResult` from wiring findings. This is a new adapter pattern -- document in Section 4.5.3.

### BC-7: Define `SHADOW_GRACE_INFINITE` constant
Replace magic number `999999` with named constant. Apply in SprintConfig default and rollout Phase 1 configuration.
