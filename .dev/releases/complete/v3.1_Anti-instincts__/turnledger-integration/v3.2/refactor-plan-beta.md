# Refactoring Plan: Wiring Verification Gate <- TurnLedger Integration

**Date**: 2026-03-20
**Spec**: `wiring-verification-gate-v1.0-release-spec.md`
**Design Source**: `turnledger-integration/v3.2/design.md`
**Selected Proposal**: Proposal A (Documentation-Only TurnLedger Overlay) from brainstorm.md, elevated by design.md into concrete code contracts

---

## Sections Requiring Modification

### Section 3.1: System Context

- **Current content summary**: ASCII diagram showing existing pipeline infrastructure (GateCriteria, SemanticCheck, gate_passed, SprintGatePolicy, TrailingGateRunner, resolve_gate_mode) connected to the new `audit/wiring_gate.py` component.
- **Required change**: The design (Section 3, Budget Flow) makes TurnLedger a first-class runtime dependency of the wiring gate. The system context diagram must show `sprint/models.py::TurnLedger` as a dependency of the wiring hook, and `resolve_gate_mode()` as an active participant (not just a deferred evaluator).
- **Specific edits**:
  - Add to the "Existing Pipeline Infrastructure" column:
    ```
    sprint/models.py
      TurnLedger ──────────────────────>   debit_wiring/credit_wiring (budget tracking)
    ```
  - Modify the `sprint/executor.py` entry from:
    ```
    SprintGatePolicy ─────────────────>   invokes wiring checks post-task
    ```
    to:
    ```
    SprintGatePolicy ─────────────────>   builds remediation steps on wiring failure
    execute_phase_tasks() ────────────>   threads TurnLedger to wiring hook
    ```
  - Change `TrailingGateRunner` line from "deferred evaluation (shadow mode)" to "deferred evaluation (trailing scope via resolve_gate_mode)"
  - Add under `resolve_gate_mode()`: "determines TRAILING vs BLOCKING behavior (replaces string mode switch)"
- **Cross-references**: Section 4.5 (sprint integration), Section 11 (dependency map)
- **Risk**: If the diagram is updated but the dependency map (Section 11) is not, they contradict each other.

### Section 3.2: Module Architecture

- **Current content summary**: Shows `audit/wiring_gate.py` and `audit/wiring_config.py` as new modules with their classes/functions.
- **Required change**: Design Section 2.2 adds `debit_wiring()`, `credit_wiring()`, `can_run_wiring_gate()`, `wiring_gate_cost`, and `wiring_gate_credits` to TurnLedger. These live in `sprint/models.py`, not in the new audit modules.
- **Specific edits**:
  - Add a third entry to the module list:
    ```
    src/superclaude/cli/sprint/models.py           (MODIFY -- TurnLedger extensions)
        |
        |--- TurnLedger.debit_wiring(turns)
        |--- TurnLedger.credit_wiring(turns)        # FIRST production consumer of reimbursement_rate
        |--- TurnLedger.can_run_wiring_gate()
        |--- TurnLedger.wiring_gate_cost: int
        |--- TurnLedger.wiring_gate_credits: int
    ```
  - Add `sprint/kpi.py (MODIFY -- GateKPIReport extensions)` entry showing wiring-specific KPI fields.
- **Cross-references**: Section 4.1 (data models), Section 5 (file manifest), Section 6.1 (public API)
- **Risk**: Low. Additive change.

### Section 3.3: Data Flow

- **Current content summary**: Linear flow from task completion -> git diff -> run_wiring_analysis -> emit_report -> gate_passed -> shadow/soft/full branch.
- **Required change**: Design Section 3 (Budget Flow) replaces the simple mode switch at the bottom with a TurnLedger-aware flow: budget check -> debit -> analysis -> resolve_gate_mode -> TRAILING/BLOCKING branch -> credit on pass or remediation on fail.
- **Specific edits**:
  - Replace the final decision box:
    ```
                       +--------+--------+
                       |  shadow: log    |
                       |  soft: warn     |
                       |  full: block    |
                       +--------+--------+
    ```
    with:
    ```
                       +--------+--------+
                       | ledger.debit_   |
                       | wiring(1)       |
                       +--------+--------+
                                |
                       +--------+--------+
                       | resolve_gate_   |
                       | mode(scope,     |
                       | grace_period)   |
                       +--------+--------+
                          |           |
                      TRAILING     BLOCKING
                          |           |
                     Log + credit   Gate eval
                     on pass        |
                                    +-- pass: credit_wiring()
                                    +-- fail: attempt_remediation()
    ```
  - Add a `ledger.can_run_wiring_gate()` check box between "Task completes" and "Collect changed file paths", with a "budget insufficient -> skip" exit path.
- **Cross-references**: Section 4.5 (sprint integration pseudocode), Section 8 (rollout plan)
- **Risk**: Medium. The data flow diagram is the primary visual contract. If it shows `resolve_gate_mode()` but Section 4.5 still uses string switches, implementers get conflicting guidance.

### Section 4.1: Data Models

- **Current content summary**: Defines `WiringFinding` and `WiringReport` dataclasses with finding types, severity, and aggregate properties.
- **Required change**: Design Section 2.2 extends TurnLedger with 5 new members. These are data model additions that belong alongside the existing WiringFinding/WiringReport definitions (or cross-referenced to them).
- **Specific edits**:
  - After the `WiringReport` class definition (line 224), add a new subsection:

    ```markdown
    #### TurnLedger Extensions (v3.2)

    The following fields and methods are added to `TurnLedger` in `sprint/models.py`
    to support budget-aware wiring gate evaluation:
    ```

    ```python
    # sprint/models.py -- TurnLedger v3.2 additions

    wiring_gate_cost: int = 0                # turns debited for wiring analysis
    wiring_gate_credits: int = 0             # turns credited back on clean pass

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
        """Return True if budget allows wiring analysis (requires >= 1 turn)."""
        return self.available() >= 1
    ```

    **Note on `int(1 * 0.8) = 0`**: With `WIRING_ANALYSIS_TURNS=1` and the default
    `reimbursement_rate=0.8`, single-turn credit rounds to 0. This is intentional;
    the rate becomes meaningful with higher analysis costs or when accumulated.
    Set `reimbursement_rate=1.0` for zero-cost-on-pass behavior.

- **Cross-references**: Section 6.2 (configuration contract -- SprintConfig changes), Section 3.2 (module architecture)
- **Risk**: Medium. The `int()` floor behavior means default single-turn wiring checks are never reimbursed. This must be documented clearly or implementers will file bugs.

### Section 4.5: Sprint Integration

- **Current content summary**: Defines the hook point in `sprint/executor.py`, provides pseudocode using `config.wiring_gate_mode` string comparisons (`"shadow"`, `"soft"`, `"full"`), and adds `wiring_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"` to SprintConfig.
- **Required change**: Design Sections 2.3, 3.1, and 6.1 replace the entire mode-switch approach with TurnLedger-native control flow using `resolve_gate_mode()`, `GateScope`, and ledger debit/credit operations. This is the highest-impact section change.
- **Specific edits**:
  1. **Replace the pseudocode block** (spec lines 547-569) with the TurnLedger-aware pseudocode from design.md Section 6.1 (the null-ledger-safe version):
     ```python
     def run_post_task_wiring_hook(
         task: TaskEntry,
         config: SprintConfig,
         task_result: TaskResult,
         ledger: TurnLedger | None = None,      # NEW: budget integration
     ) -> TaskResult:
         if not config.wiring_gate_enabled:
             return task_result

         # Budget gate
         if ledger is not None and not ledger.can_run_wiring_gate():
             _wiring_logger.info("Wiring analysis skipped: budget insufficient")
             return task_result

         report = run_wiring_analysis(source_dir, config)

         if ledger is not None:
             ledger.debit_wiring(WIRING_ANALYSIS_TURNS)

         effective_mode = resolve_gate_mode(
             scope=config.wiring_gate_scope,
             grace_period=config.wiring_gate_grace_period,
         )

         if report.passed and ledger is not None:
             ledger.credit_wiring(WIRING_ANALYSIS_TURNS)

         if effective_mode == GateMode.BLOCKING and not report.passed:
             if ledger is not None:
                 # attempt_remediation() with budget (see Section 4.5.1)
                 ...
             else:
                 task_result.status = TaskStatus.FAIL
                 task_result.gate_outcome = GateOutcome.FAIL

         return task_result
     ```

  2. **Replace the SprintConfig field** (spec line 575-576):
     - Remove: `wiring_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"`
     - Add:
       ```python
       wiring_gate_enabled: bool = True
       wiring_gate_scope: GateScope = GateScope.TASK       # shadow default
       wiring_gate_grace_period: int = 999999               # trailing = shadow
       ```

  3. **Add new subsection 4.5.1: Remediation Path** with the `attempt_remediation()` integration from design.md Section 4, including `SprintGatePolicy` instantiation and `TrailingGateResult` construction.

  4. **Add the mode-to-config mapping table** from design.md Section 2.3:
     | Old mode | `wiring_gate_enabled` | `wiring_gate_scope` | `wiring_gate_grace_period` |
     |----------|-----------------------|----------------------|----------------------------|
     | off      | `False`               | N/A                  | N/A                        |
     | shadow   | `True`                | `GateScope.TASK`     | `999999`                   |
     | soft     | `True`                | `GateScope.MILESTONE`| `0`                        |
     | full     | `True`                | `GateScope.RELEASE`  | `0`                        |

  5. **Add the call-site threading** text: `execute_phase_tasks()` at line 602 must pass `ledger=ledger` to `run_post_task_wiring_hook()`.

  6. **Add backward compatibility subsection** per design.md Section 6: behavioral matrix for `ledger=None` / present-sufficient / present-exhausted states.

- **Cross-references**: Section 3.3 (data flow), Section 6.2 (configuration contract), Section 8 (rollout plan), Section 9 (testing), Section 10 (success criteria)
- **Risk**: HIGH. This is the core behavioral contract. Incorrect pseudocode here propagates to implementation. The `resolve_gate_mode()` must be verified against the actual `trailing_gate.py` signatures. The `ledger=None` backward compatibility path must be explicitly tested (design Scenario 7).

### Section 5: File Manifest

- **Current content summary**: Table of 8 files (2 CREATE, 5 MODIFY, 1 CREATE fixtures) with LOC estimates.
- **Required change**: Design Section 8 (Implementation Checklist) adds `sprint/kpi.py` as a MODIFY target and increases the scope of `sprint/models.py` changes. Test file additions differ.
- **Specific edits**:
  - Change `sprint/models.py` row from `+5` LOC to `+30` (5 new fields + 3 new methods with validation + docstrings).
  - Change `sprint/executor.py` row from `+25` to `+55` (expanded hook with ledger threading, resolve_gate_mode, attempt_remediation path, backward compat).
  - Add row: `src/superclaude/cli/sprint/kpi.py | MODIFY | +20 | GateKPIReport wiring-specific fields; build_kpi_report() wiring_ledger param`
  - Add row: `tests/sprint/test_models.py | MODIFY | +30 | Tests for debit_wiring, credit_wiring, can_run_wiring_gate`
  - Update `tests/pipeline/test_full_flow.py` or add note: `+80 | Scenarios 5-8: wiring pass credit, wiring fail remediation, ledger=None compat, shadow deferred log`
  - Update totals: new production code ~430-520 lines, new test code ~420-520 lines.
- **Cross-references**: Section 12 (tasklist index -- task dependencies shift)
- **Risk**: Low. Underestimating LOC leads to sprint overruns but not architectural errors.

### Section 6.1: Public API

- **Current content summary**: Defines `run_wiring_analysis()`, `emit_report()`, and `check_wiring_report()` signatures.
- **Required change**: Design Section 3.1 adds a modified `run_post_task_wiring_hook()` signature as a public integration point. The existing three functions are unchanged, but the hook function that orchestrates them gains the `ledger` parameter.
- **Specific edits**:
  - Add after the existing three function signatures:
    ```python
    # Sprint integration hook (modified signature)
    def run_post_task_wiring_hook(
        task: TaskEntry,
        config: SprintConfig,
        task_result: TaskResult,
        ledger: TurnLedger | None = None,      # NEW: budget integration
    ) -> TaskResult:
        """Evaluate wiring gate post-task with optional TurnLedger budget tracking.

        When ledger is provided: debit before analysis, credit on pass,
        attempt_remediation on blocking failure.
        When ledger is None: analysis runs without budget tracking;
        blocking failures set FAIL directly with no retry.
        """
    ```
- **Cross-references**: Section 4.5 (sprint integration), Section 6.2 (configuration contract)
- **Risk**: Low. Additive.

### Section 6.2: Configuration Contract

- **Current content summary**: Defines `WiringConfig` dataclass with `registry_patterns`, `provider_dir_names`, `whitelist_path`, `exclude_patterns`.
- **Required change**: Design Section 2.3 replaces the `wiring_gate_mode` field on `SprintConfig` with three new fields. `WiringConfig` itself is unchanged, but the spec must document the SprintConfig changes in this section since it defines configuration contracts.
- **Specific edits**:
  - Add a new `SprintConfig` subsection after the `WiringConfig` definition:
    ```python
    # SprintConfig v3.2 additions (replaces wiring_gate_mode)
    wiring_gate_enabled: bool = True
    wiring_gate_scope: GateScope = GateScope.TASK
    wiring_gate_grace_period: int = 999999  # default = shadow behavior
    ```
  - Add the `__post_init__` migration note from design.md Risk table: provide backward-compatible mapping from old `wiring_gate_mode` strings to new fields with deprecation warning.
  - Add note: "`WiringConfig` is unchanged by TurnLedger integration. It governs analysis behavior (patterns, whitelists). `SprintConfig` governs enforcement behavior (scope, budget, grace period)."
- **Cross-references**: Section 4.5 (sprint integration), Section 8 (rollout plan), Section 9 (testing -- migration tests)
- **Risk**: Medium. The `wiring_gate_mode` -> three-field migration is a breaking change. The `__post_init__` migration shim must be specified precisely or existing configs will error.

### Section 8: Rollout Plan

- **Current content summary**: Three phases (Shadow, Soft, Full) described in prose with behavioral descriptions and threshold tables. Includes pre-activation checklist, FPR calibration guidance, and rollout decision criteria.
- **Required change**: Design Section 5 reframes all three phases as TurnLedger configuration profiles with concrete `SprintConfig` values. Rollout transitions become config-field changes, not code changes.
- **Specific edits**:
  1. **Phase 1 (Shadow)**: After the existing pre-activation checklist, add the TurnLedger configuration block:
     ```python
     SprintConfig(
         wiring_gate_enabled=True,
         wiring_gate_scope=GateScope.TASK,
         wiring_gate_grace_period=999999,  # trailing, never blocks
     )
     ```
     Add bullet: "TurnLedger behavior: `debit_wiring(1)` on every task; `credit_wiring(1)` on clean pass; failures logged via `DeferredRemediationLog` but never block; `resolve_gate_mode()` returns `GateMode.TRAILING`."

  2. **Phase 2 (Soft)**: Add config block:
     ```python
     SprintConfig(
         wiring_gate_enabled=True,
         wiring_gate_scope=GateScope.MILESTONE,
         wiring_gate_grace_period=0,
     )
     ```
     Replace `--skip-wiring-gate` override with: "Override: `--wiring-gate-scope task` (demotes to shadow behavior)."

  3. **Phase 3 (Full)**: Add config block:
     ```python
     SprintConfig(
         wiring_gate_enabled=True,
         wiring_gate_scope=GateScope.RELEASE,
         wiring_gate_grace_period=0,
     )
     ```
     Replace "No override without explicit whitelist entry" with: "Failures trigger `attempt_remediation()` immediately; remediation turns debited from same ledger; clean passes still receive reimbursement credit."

  4. **Add Section 8.4: Rollout Transition Checklist** from design.md Section 5.4:
     | Transition | Config change | Code change |
     |------------|---------------|-------------|
     | off -> shadow | `wiring_gate_enabled = True` | None |
     | shadow -> soft | `wiring_gate_scope = GateScope.MILESTONE` | None |
     | soft -> full | `wiring_gate_scope = GateScope.RELEASE` | None |
     | full -> soft (rollback) | `wiring_gate_scope = GateScope.MILESTONE` | None |
     | any -> off (emergency) | `wiring_gate_enabled = False` | None |

  5. **Add KPI data collection requirements** for Phase 1 (design.md Section 5.1):
     ```python
     wiring_gates_evaluated: int = 0
     wiring_gates_passed: int = 0
     wiring_gates_failed: int = 0
     wiring_analysis_latency_ms: list[float]
     wiring_total_debit: int = 0
     wiring_total_credit: int = 0
     ```

- **Cross-references**: Section 4.5 (sprint integration), Section 6.2 (configuration contract), Section 10 (success criteria)
- **Risk**: Medium. The existing rollout decision criteria table (FPR thresholds, whitelist stability) must be preserved alongside the new TurnLedger framing. If the threshold table is accidentally removed, Phase 2 activation has no defined criteria.

### Section 9: Testing Strategy

- **Current content summary**: Defines minimum 14 unit tests across 4 analyzers, 2 integration tests (SC-010 fixture, SC-006 shadow non-interference), and test infrastructure requirements.
- **Required change**: Design Section 7 adds 4 new test scenarios (Scenarios 5-8) for TurnLedger integration and extends KPI report testing.
- **Specific edits**:
  1. **Add Section 9.1.5: TurnLedger Integration Tests** (minimum 4 tests):
     - Scenario 5: Wiring gate passes, `debit_wiring` + `credit_wiring` applied, verify `wiring_gate_cost` and `wiring_gate_credits` fields
     - Scenario 6: Wiring gate fails in BLOCKING mode, `attempt_remediation()` called, budget debited for remediation attempts
     - Scenario 7: Wiring gate with `ledger=None` (backward compat), analysis runs, enforcement applies, no budget tracking, `TaskResult.status` set to FAIL on blocking failure
     - Scenario 8: Shadow mode with ledger, findings logged to `DeferredRemediationLog`, task status unchanged, `wiring_gate_cost` incremented but `wiring_gate_credits` remains 0

  2. **Add Section 9.1.6: TurnLedger Model Tests** (minimum 3 tests):
     - `debit_wiring()` increments both `wiring_gate_cost` and `consumed`
     - `credit_wiring()` applies `reimbursement_rate` via `int()` floor; with rate=0.8 and turns=1, credit is 0
     - `can_run_wiring_gate()` returns False when `available() < 1`

  3. **Modify SC-006** description to add: "When ledger is provided, `ledger.wiring_gate_cost` must reflect the analysis debit, and task status must be unchanged."

  4. **Add Section 9.1.7: KPI Report Extension Tests** (minimum 2 tests):
     - `build_kpi_report()` with `wiring_ledger` parameter includes wiring debit/credit totals
     - `build_kpi_report()` without `wiring_ledger` omits wiring fields (backward compat)

  5. **Update test count**: Minimum unit tests from 14 to 23. Integration tests from 2 to 6.

  6. **Update Section 9.3 Test Infrastructure**: Add `tests/sprint/test_models.py` to modified files. Add `tests/pipeline/test_full_flow.py` to modified files (Scenarios 5-8).

- **Cross-references**: Section 10 (success criteria -- new SC entries), Section 5 (file manifest -- test LOC)
- **Risk**: Medium. If the Scenario 5 budget accounting test does not assert the `int()` floor behavior explicitly, the "credit rounds to 0" edge case may be missed.

### Section 10: Success Criteria

- **Current content summary**: 11 success criteria (SC-001 through SC-011) covering detection, reporting, shadow mode, whitelist, deviation reconciliation, performance, and pre-activation validation.
- **Required change**: Design Section 7 introduces 4 new behavioral contracts that need success criteria.
- **Specific edits**:
  - Add:
    ```
    SC-012 | Wiring gate debit/credit tracked on TurnLedger | Unit test: debit_wiring increments wiring_gate_cost; credit_wiring applies reimbursement_rate |
    SC-013 | reimbursement_rate is consumed by production code for first time | credit_wiring() calls int(turns * self.reimbursement_rate); verified by unit test and Scenario 5 |
    SC-014 | Wiring gate works with ledger=None (backward compatibility) | Integration test: Scenario 7 -- analysis runs, enforcement applies, no budget tracking |
    SC-015 | Rollout phases configurable via SprintConfig without code changes | Config-only transition from shadow to soft to full per Section 8.4 checklist |
    SC-016 | KPI report includes wiring-specific debit/credit metrics | Unit test: build_kpi_report with wiring_ledger param produces wiring counters |
    SC-017 | attempt_remediation() invoked on BLOCKING wiring failure with ledger budget | Integration test: Scenario 6 -- remediation debits from ledger, success credits back |
    ```
  - Modify SC-006 verification from "Integration test in sprint context" to "Integration test in sprint context; ledger.wiring_gate_cost reflects analysis debit when ledger is provided."
- **Cross-references**: Section 9 (testing strategy -- each SC maps to a test)
- **Risk**: Low. Success criteria are documentation; incorrect entries cause test gaps, not runtime failures.

### Section 11: Dependency Map

- **Current content summary**: ASCII diagram showing existing pipeline infrastructure (unchanged) and new components with their import relationships. States "Zero changes to existing gate infrastructure."
- **Required change**: Design introduces `sprint/models.py` as a modified dependency (TurnLedger extensions) and `sprint/kpi.py` as a new modification target. The "zero changes" claim remains true for gate infrastructure, but the sprint infrastructure has new internal dependencies.
- **Specific edits**:
  - Under the `NEW` section, add:
    ```
    sprint/models.py (MODIFY) -> TurnLedger gains debit_wiring/credit_wiring
      |
      v
    sprint/executor.py (MODIFY) -> threads ledger to wiring hook
      |
      v
    sprint/kpi.py (MODIFY) ----> reads ledger.wiring_gate_cost/credits
    ```
  - Add `pipeline/trailing_gate.py` under EXISTING with note: "resolve_gate_mode() (consumed by new wiring hook); attempt_remediation() (consumed by BLOCKING path)"
  - Update the summary line to: "Zero changes to existing gate infrastructure. Sprint infrastructure gains TurnLedger threading and resolve_gate_mode() consumption."
- **Cross-references**: Section 3.1 (system context), Section 5 (file manifest)
- **Risk**: Low. Diagram accuracy.

### Section 12: Tasklist Index

- **Current content summary**: 11 tasks (T01-T11) with dependencies and critical path.
- **Required change**: Design Section 8 (Implementation Checklist) adds 8 items. Several map onto existing tasks with expanded scope; others are net-new.
- **Specific edits**:
  - **T01** (Data models): Expand scope to include TurnLedger extensions (`debit_wiring`, `credit_wiring`, `can_run_wiring_gate`, `wiring_gate_cost`, `wiring_gate_credits`). Add SprintConfig field replacement (`wiring_gate_mode` -> `wiring_gate_enabled`/`scope`/`grace_period`).
  - **T07** (Sprint integration): Expand scope significantly -- now includes `ledger` parameter threading, `resolve_gate_mode()` replacement of string switches, `attempt_remediation()` call path, `DeferredRemediationLog` wiring for trailing mode, and backward-compat `ledger=None` path. Deps add T01 (TurnLedger extensions).
  - **Add T12**: `sprint/kpi.py` -- Extend `GateKPIReport` with wiring-specific fields; update `build_kpi_report()` to accept `wiring_ledger` parameter. Deps: T01.
  - **Add T13**: TurnLedger model unit tests -- `debit_wiring`, `credit_wiring`, `can_run_wiring_gate`, `reimbursement_rate` floor behavior. Deps: T01.
  - **Add T14**: Integration test scenarios 5-8 in `test_full_flow.py`. Deps: T07, T12.
  - **Update critical path**: T01 -> T02/T03/T04 (parallel) -> T05 -> T06 -> T07 -> T10 -> T11
    becomes: T01 (expanded) -> T02/T03/T04/T13 (parallel) -> T05 -> T06 -> T07 (expanded) -> T12 -> T10/T14 (parallel) -> T11
  - **Parallel track** (unchanged): T08 -> T09
- **Cross-references**: Section 5 (file manifest), Section 9 (testing strategy)
- **Risk**: Medium. T07 is now the most complex task. If its expanded scope is not decomposed, it becomes a bottleneck.

### Section 7: Risk Assessment

- **Current content summary**: 6 risks (R1-R6) covering false positives, AST parsing, shadow data, performance, naming conventions, and provider_dir_names mismatch.
- **Required change**: Design Section 9 (Risks and Mitigations) identifies 4 new risks specific to TurnLedger integration.
- **Specific edits**:
  - Add:
    ```
    R7 | int(1 * 0.8) = 0 makes single-turn reimbursement a no-op | Low | Low | Document in budget table; recommend reimbursement_rate=1.0 for zero-cost-on-pass |
    R8 | SprintConfig field rename breaks existing configs | Medium | Medium | Provide __post_init__ migration shim reading old wiring_gate_mode and mapping to new fields with deprecation warning |
    R9 | ledger=None path skips remediation entirely | Low | Medium | Acceptable for phase-level mode; document that task-level ledger is recommended for full-mode deployments |
    R10 | resolve_gate_mode() import adds coupling to trailing_gate | Low | Low | Already imported at executor.py line 37; no new coupling |
    ```
- **Cross-references**: Section 4.5 (sprint integration -- backward compat), Section 6.2 (configuration contract -- migration)
- **Risk**: Low. Risk documentation.

---

## New Sections Required

### Section 4.5.1: Remediation Path (NEW)

- **Location**: After Section 4.5 Sprint Integration
- **Content**: The `attempt_remediation()` integration from design.md Section 4, including:
  - `SprintGatePolicy` instantiation
  - `TrailingGateResult` construction from `WiringReport`
  - `attempt_remediation()` call with `ledger.can_remediate` and `ledger.debit` bound callables
  - `_format_wiring_failure()` and `_recheck_wiring()` helper function signatures
  - Remediation budget flow diagram from design.md Section 4.2
- **Rationale**: The existing spec's full-mode path ends with `# Trigger remediation via SprintGatePolicy ... ` (literal ellipsis). This section replaces the ellipsis with a concrete contract.

### Section 4.5.2: Backward Compatibility -- TurnLedger is None (NEW)

- **Location**: After Section 4.5.1
- **Content**: Design.md Section 6 (Null Ledger Contract) including:
  - The behavioral matrix (ledger=None / present-sufficient / present-exhausted)
  - The null-safe conditional pattern
- **Rationale**: The `ledger: TurnLedger | None = None` parameter creates a dual-mode execution path that must be specified.

### Section 4.5.3: Budget Accounting Table (NEW)

- **Location**: After Section 4.5.2
- **Content**: Design.md Section 3.2 budget accounting table:

  | Event | debit | credit | Net cost |
  |-------|-------|--------|----------|
  | Wiring analysis runs, passes | 1 | `int(1 * 0.8)` = 0 | 1 |
  | Wiring analysis runs, fails (trailing) | 1 | 0 | 1 |
  | Wiring analysis runs, fails (blocking) | 1 + remediation_turns | 0 | 1 + remediation |
  | Wiring analysis skipped (budget) | 0 | 0 | 0 |
  | Wiring gate disabled | 0 | 0 | 0 |

- **Rationale**: Budget economics are the core TurnLedger contract. Implementers need a lookup table.

### Appendix C: reimbursement_rate Production Wiring Audit (NEW)

- **Location**: After Appendix B
- **Content**: Design.md Section 10 -- the before/after audit of `reimbursement_rate` consumption across the codebase. Documents that `credit_wiring()` is the first production consumer.
- **Rationale**: This is the key dead-code activation story. Traceability for reviewers who question why `reimbursement_rate` matters.

---

## Sections Unchanged

### Section 1: Problem Statement
No changes. The problem (Link 3 has zero programmatic coverage) is unaffected by TurnLedger integration. The defect table remains accurate.

### Section 2: Goals and Non-Goals
No changes. TurnLedger integration does not add new detection goals or remove non-goals. Budget tracking is an implementation concern, not a detection goal.

### Section 4.2: Analysis Functions (4.2.1, 4.2.2, 4.2.3)
No changes. The three analysis algorithms (unwired callables, orphan modules, unwired registries) are pure AST analysis functions. They do not interact with TurnLedger. Their signatures, algorithms, known limitations, and whitelist mechanisms are all unchanged.

### Section 4.3: Report Format
No changes. The Markdown + YAML frontmatter report format is independent of budget tracking. The frontmatter fields, serialization requirements (4.3.1), and whitelist audit visibility (4.3.2) are all unchanged.

### Section 4.4: Gate Definition
No changes. The `WIRING_GATE` constant, its `required_frontmatter_fields`, `semantic_checks`, and `enforcement_tier` are unchanged. The gate evaluates report content, not budget state.

### Section 4.6: Deviation Count Reconciliation
No changes. This companion feature is independent of TurnLedger. It adds a semantic check to `SPEC_FIDELITY_GATE`, which operates in the roadmap domain, not the sprint/budget domain.

### Section 6.3: Gate Contract
No changes. The frontmatter contract table (field types and constraints) is unchanged. TurnLedger state is not serialized into the wiring report frontmatter.

### Appendix A: Forensic Report Cross-Reference
No changes. The mapping from forensic findings to spec sections remains accurate. TurnLedger integration does not change which forensic findings are addressed.

### Appendix B: Naming Convention Reference
No changes. The naming conventions used by analysis functions are independent of budget tracking.

---

## Interaction Effects

### Effect 1: Section 4.5 <-> Section 8 Coupling

The rollout plan (Section 8) and sprint integration (Section 4.5) are now tightly coupled through `GateScope` and `resolve_gate_mode()`. Previously, they were loosely coupled through the `wiring_gate_mode` string. Any change to the scope-to-behavior mapping in Section 8 must be reflected in Section 4.5's pseudocode, and vice versa.

**Mitigation**: The mode-to-config mapping table (design.md Section 2.3) must appear in BOTH sections as a shared reference.

### Effect 2: Section 4.1 <-> Section 5 <-> Section 12 LOC Cascade

Adding TurnLedger data models (Section 4.1) increases `sprint/models.py` LOC (Section 5), which increases T01 scope (Section 12), which shifts the critical path. These three sections must be updated atomically.

### Effect 3: Section 9 <-> Section 10 Test/SC Cascade

Every new success criterion (SC-012 through SC-017) must have a corresponding test in Section 9. Every new test scenario (5-8) must have a corresponding SC. These two sections must be updated in lockstep.

### Effect 4: resolve_gate_mode() Assumption

The design assumes `resolve_gate_mode()` returns `GateMode.TRAILING` for `GateScope.TASK` with high grace period. This must be verified against the actual implementation in `trailing_gate.py`. If `resolve_gate_mode()` has different semantics (e.g., always returns BLOCKING for TASK scope), the shadow-mode behavior breaks.

### Effect 5: DeferredRemediationLog Type Mismatch

The analyze.md (Section 5) identifies that `DeferredRemediationLog.append()` takes `TrailingGateResult`, not `WiringReport`. The design.md assumes wiring findings can be wrapped in `TrailingGateResult` via `_format_wiring_failure()`. This adapter pattern is implied but not explicitly specified. The spec should include the adapter contract.

### Effect 6: Cross-Release Dependency on v3.1

The cross-release summary recommends v3.1 lands first (establishing gate-pass reimbursement in `execute_phase_tasks()`). If v3.2 ships before v3.1, all TurnLedger integration code must work standalone -- which it does via `ledger=None` backward compat, but the `reimbursement_rate` activation story becomes v3.2-specific rather than building on v3.1 infrastructure.

---

## Migration / Backward Compatibility Notes

### 1. SprintConfig Field Migration

**Breaking change**: `wiring_gate_mode: Literal["off", "shadow", "soft", "full"]` is replaced by three fields (`wiring_gate_enabled`, `wiring_gate_scope`, `wiring_gate_grace_period`).

**Required migration**: `SprintConfig.__post_init__()` must detect the old field (if present in deserialized config) and map it:
- `"off"` -> `wiring_gate_enabled=False`
- `"shadow"` -> `enabled=True, scope=TASK, grace=999999`
- `"soft"` -> `enabled=True, scope=MILESTONE, grace=0`
- `"full"` -> `enabled=True, scope=RELEASE, grace=0`

Emit a deprecation warning on migration. Remove migration shim after 2 releases.

### 2. run_post_task_wiring_hook Signature Change

**Non-breaking**: The new `ledger` parameter has default `None`. All existing call sites that pass positional `(task, config, result)` continue to work. Only `execute_phase_tasks()` needs updating to pass `ledger=ledger`.

### 3. TurnLedger Field Additions

**Non-breaking**: New fields (`wiring_gate_cost`, `wiring_gate_credits`) have defaults of 0. Existing `TurnLedger` consumers see no change. `debit_wiring()` and `credit_wiring()` are additive methods.

### 4. GateKPIReport Extension

**Non-breaking**: New fields on `GateKPIReport` have defaults. `build_kpi_report()` gains an optional `wiring_ledger` parameter with default `None`. Existing callers are unaffected.

### 5. Test Compatibility

Existing test scenarios 1-4 in `test_full_flow.py` are unchanged. New scenarios 5-8 are additive. Existing `test_models.py` tests for TurnLedger remain valid since all new methods and fields are additive.

### 6. resolve_gate_mode() Coupling

This function is already imported in `executor.py` (line 37 per design.md). No new import coupling is introduced. However, the wiring gate becomes the first consumer to use it with configurable `grace_period`, which may expose untested edge cases in `resolve_gate_mode()`.
