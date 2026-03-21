# Merged Roadmap Gap Analysis: v3.1 Anti-Instincts Gate

**Sources**: Agent A (full-spectrum analysis), Agent B (TurnLedger integration focus)
**Analysis Date**: 2026-03-21
**Branch**: v3.0-AuditGates
**Execution Log**: 4 phases, all PASS, 49m 18s total

---

## Agreement Summary

Both agents converge on the following conclusions:

1. **Phases 1-2 are fully implemented**. All four core detection modules (`obligation_scanner.py`, `integration_contracts.py`, `fingerprint.py`, `spec_structural_audit.py`) exist with correct functionality. The `ANTI_INSTINCT_GATE` is defined in `gates.py`, wired into the executor, and prompt blocks are in place.

2. **Phase 3 is partially implemented**. The `gate_rollout_mode` field exists on `SprintConfig`. The `run_post_task_anti_instinct_hook()` function is correctly implemented with rollout mode matrix, None-safe TurnLedger guards, ShadowGateMetrics recording, and credit/fail paths.

3. **Phase 4 is deferred** (operational, requires live sprint runs).

4. **The core bug is identical**: `execute_sprint()` (the production entry point) never constructs a `TurnLedger`, never instantiates `ShadowGateMetrics` or `DeferredRemediationLog`, never calls `execute_phase_tasks()`, and never calls `build_kpi_report()`. The entire per-task orchestration layer with hooks is unreachable from production.

5. **Root cause agreement**: Architectural mismatch between `execute_sprint()` (per-phase subprocess model) and `execute_phase_tasks()` (per-task model with hooks). The v3.1 implementation targeted the per-task path, which is only reachable through test factories.

6. **Both agents note the irony**: This is exactly the class of bug the anti-instinct gate was designed to catch -- components built but never wired into the production dispatch path.

---

## Disagreements & Resolutions

### D1: Test file existence

| Test File | Agent A | Agent B | Resolution |
|-----------|---------|---------|------------|
| `tests/roadmap/test_anti_instinct_integration.py` | NOT VERIFIED | PRESENT | **PRESENT** -- Agent B confirmed on disk. Agent A scoped out verification. |
| `tests/sprint/test_shadow_mode.py` | NOT FOUND | PRESENT | **PRESENT** -- Agent B confirmed. Agent A missed it. |
| `tests/pipeline/test_full_flow.py` | NOT FOUND | PRESENT | **PRESENT** -- Agent B confirmed. Agent A missed it. |

**Verdict**: Agent B's inventory is authoritative. All 8 test files exist. Agent A's "NOT FOUND / NOT VERIFIED" entries were scope limitations, not confirmed absences.

### D2: `attempt_remediation()` usage

| Aspect | Agent A | Agent B | Resolution |
|--------|---------|---------|------------|
| Flagged as gap? | Yes (Missing #7, Gap 3) | Not flagged directly | **Valid gap, LOW severity**. Agent A correctly identified that the hook implements inline fail logic rather than delegating to `attempt_remediation()`. Agent B focused on the higher-level accumulation gap instead. Both are correct -- the inline approach is simpler but skips the retry-once state machine. Classified as LOW because the spec does not mandate the specific function be used, only the retry-once behavior. |

### D3: `SprintGatePolicy` instantiation

| Aspect | Agent A | Agent B | Resolution |
|--------|---------|---------|------------|
| Flagged as gap? | Yes (Missing #3, MEDIUM) | Not flagged | **Valid gap, MEDIUM severity**. `SprintGatePolicy` is defined but never instantiated. Agent B covered the downstream effect (remediation not wired) but did not flag the policy object itself. Both agents agree remediation is not wired; Agent A was more granular in identifying the specific unused class. |

### D4: Reimbursement operand divergence

| Aspect | Agent A | Agent B | Resolution |
|--------|---------|---------|------------|
| Flagged? | Not flagged | Yes (Gap 4, LOW) | **Valid finding, LOW severity**. Agent B identified that the spec says reimbursement should be based on upstream merge step turns, but code uses `task_result.turns_consumed`. This is a semantic divergence. The current approach is more practical (reimburses based on the task that ran) and defensible. Recommend documenting the intentional deviation rather than changing behavior. |

### D5: `TrailingGateResult` not accumulated

| Aspect | Agent A | Agent B | Resolution |
|--------|---------|---------|------------|
| Flagged? | Implied (under Gap 1 and Missing #4) | Explicitly flagged (M3, Gap 1 CRITICAL) | **Both agree**. Agent B was more precise in articulating that `TrailingGateResult` objects are never created by the anti-instinct hook, which breaks the KPI accumulation pipeline. Agent A covered the effect (no KPI report) without pinpointing the missing wrapping step. Merged as a single HIGH-severity gap. |

### D6: `TrailingGateResult` signature deviation (DEV-002)

| Aspect | Agent A | Agent B | Resolution |
|--------|---------|---------|------------|
| Flagged? | No | Yes (M6) | **Valid finding, LOW severity**. The spec says `TrailingGateResult(passed, evaluation_ms, gate_name)` but the codebase uses `TrailingGateResult(step_id, passed, evaluation_ms, failure_reason)`. The codebase follows the roadmap's version. This is a spec-vs-implementation documentation drift, not a functional bug. |

### D7: `gate_scope=GateScope.TASK` verification

| Aspect | Agent A | Agent B | Resolution |
|--------|---------|---------|------------|
| Flagged? | Agent A confirms `GateScope.TASK` | Agent B flags as unverified (M5, MEDIUM) | **Resolved: PRESENT**. Agent A's evidence (line 995 in gates.py, `enforcement_tier="STRICT"`, `GateScope.TASK`) is more specific. Agent B's uncertainty was conservative but the gate scope is correctly set. |

---

## Merged Findings

### Confirmed Present (deduplicated)

#### Phase 1 -- Core Detection Modules (4/4)
- `obligation_scanner.py` -- scaffold-discharge detection, compiled regex, `ObligationReport`/`Obligation` dataclasses, phase splitting, component context extraction
- `integration_contracts.py` -- 7-category dispatch pattern scanner, `IntegrationAuditResult`/`IntegrationContract`/`WiringCoverage` dataclasses, `check_roadmap_coverage()`
- `fingerprint.py` -- 3-source extraction (backtick, code-block def/class, ALL_CAPS), `_EXCLUDED_CONSTANTS` frozenset, threshold gate logic (0.7 default)
- `spec_structural_audit.py` -- 7 structural indicator counters, `check_extraction_adequacy()` with 0.5 threshold

#### Phase 2 -- Pipeline Wiring (complete)
- `ANTI_INSTINCT_GATE` in `gates.py` (L995) with 3 semantic checks, `enforcement_tier="STRICT"`, `GateScope.TASK`, inserted into `ALL_GATES` (L1084)
- `_run_anti_instinct_audit()` in `executor.py` (L265) -- runs all 3 modules, writes `anti-instinct-audit.md` with YAML frontmatter
- `_run_structural_audit()` in `executor.py` (L220) -- post-extract warning-only hook
- `"anti-instinct"` step (L846) between `"merge"` and `"test-strategy"`, `retry_limit=0`, `timeout_seconds=30`, registered in `_get_all_step_ids()` (L963)
- `INTEGRATION_ENUMERATION_BLOCK` (L38) and `INTEGRATION_WIRING_DIMENSION` (L51) in `prompts.py`, wired into `build_generate_prompt` (L199) and `build_spec_fidelity_prompt` (L357)

#### Phase 3 -- Sprint Integration (hook-level complete, orchestration incomplete)
- `gate_rollout_mode` on `SprintConfig` (L325): `Literal["off", "shadow", "soft", "full"] = "off"`
- `run_post_task_anti_instinct_hook()` in `sprint/executor.py` (L585-686) with full rollout mode matrix
- Anti-instinct hook invoked from `execute_phase_tasks()` after wiring hook (NFR-010 independence preserved)
- `ShadowGateMetrics.record()` called in shadow/soft/full modes (FR-SPRINT.4)
- None-safe TurnLedger guards throughout (NFR-007)
- Credit path: `ledger.credit(int(task_result.turns_consumed * ledger.reimbursement_rate))` on PASS (soft/full)
- Fail path: `GateOutcome.FAIL` set; `TaskStatus.FAIL` only in full mode
- Budget exhaustion path: checks `ledger.can_remediate()` before remediation

#### Test Files (8/8 present)
- `tests/roadmap/test_obligation_scanner.py`
- `tests/roadmap/test_integration_contracts.py`
- `tests/roadmap/test_fingerprint.py`
- `tests/roadmap/test_spec_structural_audit.py`
- `tests/roadmap/test_anti_instinct_integration.py`
- `tests/sprint/test_anti_instinct_sprint.py`
- `tests/sprint/test_shadow_mode.py`
- `tests/pipeline/test_full_flow.py`

#### Infrastructure (from v3.0)
- `TurnLedger` class with budget tracking, `credit()`, `debit()`, `can_launch()`, `can_remediate()`, `reimbursement_rate=0.8`
- `TrailingGateResult` dataclass (with `step_id`, `passed`, `evaluation_ms`, `failure_reason`)
- `TrailingGateRunner` with daemon-thread gate evaluation
- `DeferredRemediationLog` with persistence and `--resume` support
- `TrailingGatePolicy` protocol and `SprintGatePolicy` implementation
- `attempt_remediation()` with retry-once semantics
- `GateKPIReport` and `build_kpi_report()` in `sprint/kpi.py`
- `GateScope`, `resolve_gate_mode()` in `pipeline/trailing_gate.py`
- `TaskResult` with `gate_outcome`, `reimbursement_amount` fields

### Confirmed Missing/Bugs (deduplicated, severity-rated)

#### CRITICAL (3)

| ID | Finding | Spec Ref | Severity | Both Agents? |
|----|---------|----------|----------|--------------|
| BUG-001 | `execute_sprint()` never constructs a `TurnLedger` or passes one downstream. All TurnLedger paths are dead code in production. | FR-SPRINT.2, FR-SPRINT.5, A-011 | CRITICAL | Yes (A:#1, B:implicit) |
| BUG-002 | `execute_sprint()` never constructs `ShadowGateMetrics`. Shadow metrics collection never occurs in production sprint runs. | FR-SPRINT.4 | CRITICAL | Yes (A:#2, B:implicit) |
| BUG-003 | `execute_sprint()` never calls `execute_phase_tasks()`. The per-task orchestration with hooks is unreachable from the production sprint loop. The main loop uses per-phase `ClaudeProcess` subprocesses with no post-step gate evaluation. | FR-SPRINT.2 | CRITICAL | Yes (A:#6, B:Root Cause #3) |

#### HIGH (2)

| ID | Finding | Spec Ref | Severity | Both Agents? |
|----|---------|----------|----------|--------------|
| BUG-004 | Anti-instinct hook does not wrap results in `TrailingGateResult` or accumulate them. No `_all_gate_results` accumulator exists in `execute_sprint()`. `build_kpi_report()` cannot aggregate anti-instinct metrics. | Section 9.5 steps 2-3 | HIGH | Yes (A:#4, B:M3/Gap1) |
| BUG-005 | `DeferredRemediationLog` never instantiated in sprint. Gate failures not persisted. `--resume` cannot recover from anti-instinct gate failures. | Section 9.5 step 5, Section 16.5, FR-SPRINT.3 | HIGH | Yes (A:#5, B:M2/Gap2) |

#### MEDIUM (3)

| ID | Finding | Spec Ref | Severity | Both Agents? |
|----|---------|----------|----------|--------------|
| BUG-006 | `SprintGatePolicy` defined but never instantiated in `execute_sprint()`. Remediation workflow unreachable. | A-014 | MEDIUM | A only |
| BUG-007 | `build_kpi_report()` never called at sprint completion. No KPI report produced. | Section 9.6, FR-SPRINT.4 | MEDIUM | Yes (A:#4, B:M1/M4/Gap3) |
| BUG-008 | No integration test verifies that `execute_sprint()` invokes TurnLedger, ShadowGateMetrics, or gate hooks. Current tests only cover `execute_phase_tasks()` path. | Section 12 | MEDIUM | Yes (A:Root Cause #2, B:implicit) |

#### LOW (3)

| ID | Finding | Spec Ref | Severity | Both Agents? |
|----|---------|----------|----------|--------------|
| BUG-009 | `attempt_remediation()` never called from sprint executor. Hook implements simpler inline fail logic instead of retry-once state machine. | FR-SPRINT.3 | LOW | A only |
| BUG-010 | Reimbursement uses `task_result.turns_consumed` instead of upstream merge step turns as spec states. Semantic divergence -- current approach is more practical. | Section 16.5 | LOW | B only |
| BUG-011 | `TrailingGateResult` signature differs from spec (`step_id` vs `gate_name`, extra `failure_reason`). Codebase follows roadmap version, not spec. Documentation drift. | DEV-002 | LOW | B only |

### TurnLedger Wiring Status (merged)

| Component | Defined? | Instantiated in `execute_sprint()`? | Reachable in production? |
|-----------|----------|--------------------------------------|--------------------------|
| `TurnLedger` | Yes (`sprint/models.py`) | NO | NO |
| `ShadowGateMetrics` | Yes | NO | NO |
| `SprintGatePolicy` | Yes (L56-99) | NO | NO |
| `DeferredRemediationLog` | Yes (`pipeline/trailing_gate.py` L489) | NO | NO |
| `build_kpi_report()` | Yes (`sprint/kpi.py` L137) | NO (never called) | NO |
| `TrailingGateResult` | Yes (`pipeline/trailing_gate.py` L36) | N/A (not created by hook) | NO |
| `run_post_task_anti_instinct_hook()` | Yes (`sprint/executor.py` L585) | N/A (in `execute_phase_tasks()`) | NO -- `execute_sprint()` does not call `execute_phase_tasks()` |
| `run_post_task_wiring_hook()` | Yes | N/A (in `execute_phase_tasks()`) | NO -- same reason |

**Net status**: Every sprint-side component is correctly implemented in isolation, but the production entry point (`execute_sprint()`) uses a per-phase subprocess model that bypasses all of them. The per-task orchestration layer is only reachable through test factories.

### Root Cause Analysis (merged)

**Primary cause**: Architectural mismatch between two execution models in the sprint executor.

1. **`execute_sprint()`** (production entry point) uses a **per-phase subprocess model**: one `ClaudeProcess` per phase, monitored via a poll loop. No concept of individual tasks, TurnLedger budget tracking, or post-step gate evaluation.

2. **`execute_phase_tasks()`** (per-task function) uses a **per-task subprocess model**: iterates over `TaskEntry` objects, manages budget via `TurnLedger`, runs post-task hooks (wiring + anti-instinct). Correctly wired but **never called from `execute_sprint()`**.

The v3.1 implementation targeted `execute_phase_tasks()` correctly. All hooks, guards, and integrations work as designed within that function. But `execute_sprint()` was not updated to delegate to `execute_phase_tasks()` or replicate its behavior.

**Contributing factors** (merged from both agents):

1. **Dual execution context confusion**: The spec identified the dual context (standalone roadmap vs sprint-invoked) but the sprint executor's internal dual architecture (per-phase vs per-task) was not surfaced in the spec or roadmaps.

2. **Hook-based integration without accumulation**: The hooks were implemented as self-contained functions that mutate `TaskResult` in-place. This works operationally but bypasses the `TrailingGateResult` -> `DeferredRemediationLog` -> `build_kpi_report()` accumulation pipeline described in Section 9.5.

3. **Test coverage gap**: Tests exercise `run_post_task_anti_instinct_hook()` directly and `execute_phase_tasks()` with factories. No test verifies that `execute_sprint()` invokes these paths. The execution log showed all phases PASS, but "success" referred to task implementation, not production wiring.

4. **Missing glue code**: All infrastructure components exist. The only missing piece is the orchestration glue in `execute_sprint()` that instantiates `TurnLedger`, `ShadowGateMetrics`, `DeferredRemediationLog`, delegates to `execute_phase_tasks()`, accumulates `TrailingGateResult` objects, and calls `build_kpi_report()` at sprint end.

---

## Recommendations (priority-ordered)

### P0: Wire `execute_sprint()` to `execute_phase_tasks()` [BLOCKING]

Refactor `execute_sprint()` to delegate task-level orchestration to `execute_phase_tasks()`. This is the single fix that resolves BUG-001 through BUG-003 and unblocks all downstream components. The per-task model is required because it enables per-task budget tracking, post-task gate evaluation, and hook invocation.

Alternatively, if per-phase granularity must be preserved, add TurnLedger construction, ShadowGateMetrics instantiation, and post-phase gate hooks directly to the `execute_sprint()` poll loop. The per-task approach is strongly preferred.

### P1: Add `TrailingGateResult` wrapping in anti-instinct hook [HIGH]

Modify `run_post_task_anti_instinct_hook()` to create a `TrailingGateResult` for each evaluation and return it. Add an `_all_gate_results: list[TrailingGateResult]` accumulator in the sprint loop. Resolves BUG-004.

### P2: Instantiate `DeferredRemediationLog` in sprint entrypoint [HIGH]

Create `DeferredRemediationLog` with persist path (e.g., `results_dir / "remediation.json"`) at sprint start. Pass to hooks so gate failures are recorded. Enables `--resume` recovery. Resolves BUG-005.

### P3: Call `build_kpi_report()` at sprint completion [MODERATE]

After all phases complete, aggregate `TrailingGateResult` objects and call `build_kpi_report()`. Write formatted report to disk alongside sprint summary. Resolves BUG-007.

### P4: Integration test for production path [MODERATE]

Add a test that exercises `execute_sprint()` end-to-end (with mocked `ClaudeProcess`) and verifies that TurnLedger, ShadowGateMetrics, DeferredRemediationLog, hooks, and KPI report are invoked. Resolves BUG-008.

### P5: Instantiate `SprintGatePolicy` [LOW]

Wire `SprintGatePolicy` into `execute_sprint()` so the remediation workflow is reachable. Resolves BUG-006.

### P6: Reconcile `attempt_remediation()` vs inline logic [LOW]

Decide whether the inline fail logic in the hook should delegate to `attempt_remediation()` for the retry-once state machine, or whether the simpler approach is intentional for v3.1. Document the decision. Resolves BUG-009.

### P7: Document reimbursement operand deviation [LOW]

The current `task_result.turns_consumed` approach is more practical than the spec's "upstream merge step turns." Document this as an intentional deviation. Resolves BUG-010.

### P8: Consider unified gate hook protocol [LOW]

Extract a shared `PostTaskGateHook` protocol for both wiring and anti-instinct hooks that returns `TrailingGateResult`, appends to `DeferredRemediationLog`, and feeds the sprint-level accumulator. Resolves BUG-004 and Gap 5 structurally.

---

## Final Verdict

| Metric | Value |
|--------|-------|
| **Implementation completeness** | **72%** |
| **Critical bugs** | **3** (BUG-001, BUG-002, BUG-003 -- all stem from `execute_sprint()` not calling `execute_phase_tasks()`) |
| **Blocking gaps** | **2** (P0: sprint wiring, P1: gate result accumulation) |
| **High-severity gaps** | **2** (BUG-004, BUG-005) |
| **Medium-severity gaps** | **3** (BUG-006, BUG-007, BUG-008) |
| **Low-severity gaps** | **3** (BUG-009, BUG-010, BUG-011) |
| **Total bugs/gaps** | **11** |

**Breakdown by area**:
- Roadmap pipeline (Phases 1-2): **100%** complete
- Sprint hook implementation (Phase 3 hooks): **100%** correct in isolation
- Sprint orchestration wiring (Phase 3 glue): **0%** -- production entry point bypasses all per-task infrastructure
- Phase 4 (operational): Deferred (by design)

**Bottom line**: The anti-instinct gate is fully implemented at the component level but completely disconnected from the production sprint loop. A single architectural fix (wiring `execute_sprint()` to `execute_phase_tasks()`) would resolve all 3 critical bugs and unblock the remaining gaps. The estimated effort is moderate -- the components are sound and tested; only the orchestration glue is missing.
