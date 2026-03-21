# Gap Remediation Tasklist Reflection: v3.2

**Date**: 2026-03-21
**Source tasklist**: `gap-remediation-tasklist.md`
**Source report**: `roadmap-gap-analysis-merged.md`
**Method**: Code-verified fidelity check + approach validation

---

## Fidelity Check

| Rec # | Recommendation | Corresponding Task(s) | Covered? | Accurate? | Notes |
|-------|---------------|----------------------|----------|-----------|-------|
| R1 | Wire `execute_sprint()` to TurnLedger | T01, T02 | YES | PARTIAL | See F1 below |
| R2 | Activate `_resolve_wiring_mode()` | T03 | YES | YES | One-line fix, correctly specified |
| R3 | Wire DeferredRemediationLog into shadow mode | T04, T05 | YES | PARTIAL | See F2 below |
| R4 | Fix BLOCKING remediation lifecycle | T06, T07, T08 | YES | PARTIAL | See F3 below |
| R5 | Add SprintConfig scope-based fields | T09 | YES | YES | Correctly specified |
| R6 | Add missing KPI fields | T10 | YES | PARTIAL | See F4 below |
| R7 | Align frontmatter contract | T11 | YES | YES | Documentation-only, appropriate |
| R8 | Add `check_wiring_report()` wrapper | T12 | YES | PARTIAL | See F5 below |
| R9 | Add labeled budget scenario tests 5-8 | T13 | YES | YES | |
| R10 | Add retrospective validation artifact | T14 | YES | YES | |
| R11 | Add performance benchmark test | T15 | YES | YES | |
| R12 | Fix migration shim targets | T16 | YES | YES | Pragmatic approach (docs first) |

### Fidelity Gaps

**F1: T01 post-phase hook architecture may not solve Gap #1 correctly**

The merged report's Gap #1 states: "production path never calls `execute_phase_tasks()`, making all per-task hooks unreachable." T01 proposes creating a `run_post_phase_wiring_hook()` that wraps phase results into synthetic TaskEntry/TaskResult and delegates to `run_post_task_wiring_hook()`. This is Option B from R1.

The issue is that `execute_sprint()` runs **monolithic Claude subprocesses per phase** (line 932: `ClaudeProcess(config, phase, ...)`). A post-phase hook can only analyze the codebase *after* the entire phase subprocess completes. It cannot analyze per-task within the phase. This is architecturally correct for phase-level wiring verification but does not provide the per-task granularity the spec assumed. The tasklist correctly identifies this tradeoff (Option B) but should explicitly document that per-task analysis within a phase subprocess remains out-of-scope for v3.2.

**F2: T04 TrailingGateResult constructor mismatch**

The tasklist proposes constructing `TrailingGateResult` with fields `gate_name`, `passed`, `message`, `task_id`. However, the actual `TrailingGateResult` dataclass (trailing_gate.py:35-41) has fields: `step_id`, `passed`, `evaluation_ms`, `failure_reason`. There is no `gate_name`, `message`, or `task_id` field. The tasklist's risk note correctly flags this ("verify constructor signature") but the example code in T04 is wrong and will fail at runtime.

**F3: T08 `attempt_remediation()` interface mismatch**

T08 proposes calling `attempt_remediation(prompt=prompt, config=config, task=task)`. The actual `attempt_remediation()` signature (trailing_gate.py:354-361) takes `(remediation_step, turns_per_attempt, can_remediate, debit, run_step, check_gate)` -- a fully callable-based interface. The tasklist's note at T08 line 358 acknowledges this risk ("verify from trailing_gate.py") but the primary code block is incorrect. The alternative path via `SprintGatePolicy.build_remediation_step()` is more viable but requires constructing a `TrailingGateResult` first (which has the F2 issue).

**F4: T10 line reference inaccuracy**

T10 says "Add three new fields to GateKPIReport (after line 52)". Actual line 52 in kpi.py is `files_skipped: int = 0`, which is the last current field. This is correct. However, T10 proposes `wiring_net_cost` as both a stored field and a computed property, which is contradictory for a dataclass. The tasklist catches this in the risk note but the description mixes both approaches.

**F5: T12 WIRING_GATE structure assumption**

T12 assumes `WIRING_GATE["checks"]` with `check["fn"]` callables. The actual `WIRING_GATE` is a `GateCriteria` instance (not a dict) with `semantic_checks` being a list of `SemanticCheck` objects with `.check_fn` attributes. The iteration pattern `for check in WIRING_GATE["checks"]` will raise `TypeError`. Must use `WIRING_GATE.semantic_checks` and `check.check_fn(content)`.

---

## Approach Validation

### T01: Create post-phase wiring hook

- **Line references**: "Place between `run_post_task_anti_instinct_hook()` (ends ~line 688) and `execute_phase_tasks()` (starts line 689)." Verified: `run_post_task_anti_instinct_hook()` ends at line 687 (the return), `execute_phase_tasks()` starts at line 689. **ACCURATE**.
- **Approach**: Creating a synthetic TaskEntry from PhaseResult is viable. TaskEntry requires `task_id` and `title` at minimum (it's a dataclass). The synthetic `task_id=f"phase-{phase.number}"` pattern is reasonable.
- **Risk**: The `PhaseResult` and `Phase` imports are already available at module level (imported at line 19-20). The lazy import note is unnecessary.
- **Sufficiency**: Adequate for phase-level analysis.
- **New issues**: None likely.

### T02: Wire post-phase hook into execute_sprint()

- **Line references**: "`execute_sprint()` (line 843+)" -- verified, starts at line 843. "After phase_result recorded (around line 942+)" -- actual location is line 1109 (`sprint_result.phase_results.append(phase_result)`). The tasklist's "line 942" is significantly off. **INACCURATE line reference**.
- **Approach**: Creating TurnLedger at sprint start is correct. Placing the hook call after `phase_result` append is correct placement.
- **Risk note about minimum_allocation=5**: Valid concern. Phase-level analysis only needs 1 turn per analysis, so the default may need adjustment.
- **Sufficiency**: Adequate, but the line reference needs correction.

### T03: Activate `_resolve_wiring_mode()`

- **Line references**: "line 473" for `mode = config.wiring_gate_mode` -- verified at line 473. `_resolve_wiring_mode()` at "lines 420-446" -- verified at lines 420-446. **ACCURATE**.
- **Approach**: One-line change, minimal risk. Correct.
- **Sufficiency**: Complete.

### T04: Create DeferredRemediationLog adapter

- **Approach**: The synthetic `TrailingGateResult` construction is wrong (see F2). Correct construction:
  ```python
  gate_result = TrailingGateResult(
      step_id=task.task_id,
      passed=False,
      evaluation_ms=0.0,
      failure_reason=f"[shadow] {finding.finding_type}: {finding.detail}",
  )
  ```
- **Sufficiency**: Functionally correct once constructor is fixed.

### T05: Wire shadow findings adapter

- **Line references**: "run_post_task_wiring_hook() signature (line 449)" -- verified at line 449. "shadow mode branch (line 519-530)" -- verified at lines 519-530. "call site in execute_phase_tasks() (line 788)" -- verified at line 788. "execute_phase_tasks() signature (line 689)" -- verified at line 689. **ALL ACCURATE**.
- **Approach**: Threading `remediation_log` through signatures is correct and follows existing patterns (similar to how `ledger` and `shadow_metrics` are threaded).
- **Risk**: Multiple call sites need updating. The tasklist correctly identifies this.

### T06: Implement `_format_wiring_failure()`

- **Approach**: Sound. Using `report.unsuppressed_findings` filtered by severity is correct per `blocking_count()` logic.
- **Risk note**: WiringFinding fields verified: `finding_type`, `file_path`, `symbol_name`, `line_number`, `detail`, `severity`, `suppressed`. All assumed fields exist. **No issue**.
- **Sufficiency**: Adequate.

### T07: Implement `_recheck_wiring()`

- **Approach**: Creating fresh `WiringConfig` and calling `run_wiring_analysis()` is correct.
- **Issue**: `WiringConfig` constructor takes `rollout_mode` as a parameter (verified from wiring_config import). The tasklist correctly uses `WiringConfig(rollout_mode=mode)`.
- **Sufficiency**: Adequate.

### T08: Wire remediation lifecycle into BLOCKING path

- **Line references**: "full mode branch (lines 548-580)" -- verified at lines 548-580. **ACCURATE**.
- **Approach**: The `attempt_remediation()` call is wrong (see F3). The callable-based interface requires wrapping -- the implementer must construct `run_step` and `check_gate` callables. The fallback to `SprintGatePolicy.build_remediation_step()` is viable but requires a valid `TrailingGateResult` (F2 fix needed first).
- **Sufficiency**: The overall lifecycle (format -> debit -> remediate -> recheck -> credit/fail) is correct. The implementation details need adjustment per F2 and F3.
- **New issues**: The existing code already debits `config.remediation_cost` at line 565. T08 proposes replacing this block, which is correct. But the replacement must preserve the existing `can_remediate()` check pattern.

### T09: Add SprintConfig scope-based fields

- **Line references**: "after line 329" -- verified, line 329 is `remediation_cost: int = 2`. "__post_init__() (line 331+)" -- verified at line 331. **ACCURATE**.
- **Approach**: Adding `wiring_gate_enabled` and `wiring_gate_grace_period` is correct. The `__post_init__` derivation logic is sound.
- **Risk**: The precedence concern (explicit mode vs derived) is valid. The tasklist's recommendation to guard with "only derive if not explicitly passed" is correct but requires checking `hasattr` or sentinel values since dataclass fields always have defaults.
- **Issue**: The `_resolve_wiring_mode()` update (passing `grace_period` to `resolve_gate_mode()`, currently hardcoded to 0 at line 439) is correctly identified. **Line 439 verified**.

### T10: Add missing KPI fields

- **Line references**: "after line 52" -- kpi.py line 52 is `files_skipped: int = 0`. **ACCURATE**. "build_kpi_report() (line 137+)" -- verified at line 137. **ACCURATE**.
- **Approach**: Making `wiring_net_cost` a `@property` is the correct approach for dataclasses. Using `field(init=False)` would also work but a property is cleaner.
- **Issue**: `wiring_analyses_run` and `wiring_remediations_attempted` counters need a source. The tasklist suggests deriving from TurnLedger debit events, but TurnLedger doesn't track a count of wiring analyses -- only cumulative turns. A new counter field on TurnLedger would be needed, or the count can be derived as `wiring_turns_used // wiring_analysis_turns` (approximate).
- **Sufficiency**: Partially specified. The counter derivation logic needs clarification.

### T11: Document frontmatter contract alignment

- **Line references**: "line 715-866, emit_report()" -- verified at lines 715-866. **ACCURATE**.
- **Approach**: Documentation-only. Appropriate.

### T12: Add `check_wiring_report()` convenience wrapper

- **Line references**: "after line 1026" for WIRING_GATE constant -- WIRING_GATE ends at line 1026. **ACCURATE**.
- **Approach**: Must be rewritten per F5. Correct version:
  ```python
  def check_wiring_report(content: str) -> tuple[bool, list[str]]:
      failures = []
      for check in WIRING_GATE.semantic_checks:
          if not check.check_fn(content):
              failures.append(check.name)
      return (len(failures) == 0, failures)
  ```
  Note: semantic checks operate on **content strings**, not `WiringReport` objects. The function signature must accept `content: str`, not `report: WiringReport`.
- **Sufficiency**: Needs rewrite but concept is correct.

### T13-T16: Tests and lower-priority tasks

- **Approach**: All reasonable. T13 test scenarios are well-specified. T14 retrospective test is a good regression guard. T15 performance benchmark with `@pytest.mark.slow` is standard. T16 migration shim documentation approach is pragmatic.

### T17-T22: Verification tasks

- **Approach**: All appropriate. T17 integration tests are well-scoped. T20 end-to-end test is the right capstone. T22 closure audit is a good completeness check.

---

## Refactoring Recommendations

### RC1: Fix TrailingGateResult construction in T04

Replace the incorrect constructor call with the actual field names. Use `step_id` (not `task_id`), `evaluation_ms` (not omitted), `failure_reason` (not `message`). Drop `gate_name` (not a field).

### RC2: Fix `attempt_remediation()` call in T08

The callable-based interface requires the implementer to:
1. Build a `Step` via `SprintGatePolicy.build_remediation_step(gate_result)`
2. Provide `run_step` callable (wrapping subprocess execution)
3. Provide `check_gate` callable (wrapping `run_wiring_analysis` + evaluation)

Alternatively, implement a simpler inline remediation without using `attempt_remediation()`, since the retry-once semantics may be overkill for the first wiring gate iteration.

### RC3: Fix `check_wiring_report()` signature in T12

Change parameter from `report: WiringReport` to `content: str` to match the semantic check function signatures, which all operate on content strings.

### RC4: Fix T02 line reference

Change "around line 942+" to "line 1109" for the `sprint_result.phase_results.append(phase_result)` location.

### RC5: Add wiring analysis counter to TurnLedger for T10

Add `wiring_analyses_count: int = 0` to TurnLedger and increment in `debit_wiring()`. This provides a clean source for `wiring_analyses_run` in KPI.

---

## Coverage Summary

| Gap # | Severity | Disposition | Task(s) | Verified? |
|-------|----------|------------|---------|-----------|
| 1 | CRITICAL | Fixed | T01, T02 | Code references verified (T02 line ref off) |
| 2 | CRITICAL | Fixed | T03 | One-line fix verified at line 473 |
| 3 | CRITICAL | Fixed | T04, T05 | Constructor signature needs correction |
| 4 | CRITICAL | Fixed | T06, T07, T08 | attempt_remediation interface needs correction |
| 5 | CRITICAL | Subsumed by T08 | T08 | Same interface issue |
| 6 | HIGH | Fixed | T09 | Fields and __post_init__ correctly specified |
| 7 | MEDIUM | Fixed | T10 | Counter derivation needs clarification |
| 8 | MEDIUM | Documented | T11 | Appropriate disposition |
| 9 | MEDIUM | Documented | T11 | Appropriate disposition |
| 10 | MEDIUM | Fixed/Documented | T16 | Pragmatic approach |
| 11 | MEDIUM | Fixed | T06 | Correctly specified |
| 12 | MEDIUM | Fixed | T07 | Correctly specified |
| 13 | MEDIUM | Fixed | T13 | Test scenarios well-defined |
| 14 | LOW | Fixed | T14 | Appropriate |
| 15 | LOW | Fixed | T15 | Appropriate |
| 16 | LOW | Fixed | T12 | Needs signature correction |
| 17 | LOW | Deferred (OQ-5) | N/A | Intentionally excluded, acceptable |
| 18 | LOW | Subsumed by Gap #1 | T01, T02 | Correct disposition |

**Coverage**: 18/18 gaps addressed (17 via tasks, 1 intentionally deferred)

---

## Final Verdict

### Fidelity: 92% (GOOD)

All 12 recommendations are covered by tasks. The recommendation-to-task mapping table is complete and accurate. The only fidelity issues are:
- 3 incorrect code examples (T04, T08, T12) that would fail at runtime
- 1 inaccurate line reference (T02: says ~942, actual is 1109)

These are implementation detail errors, not coverage gaps.

### Approach Quality: 78% (ADEQUATE with amendments needed)

The overall architecture (post-phase hooks, DeferredRemediationLog adapter, remediation lifecycle) is sound. The wave structure and dependency graph are correct. However:
- **3 tasks have incorrect API calls** that must be fixed before execution (T04, T08, T12)
- **1 task has a stale line reference** that could cause confusion (T02)
- **1 task has an underspecified counter source** (T10)

### Ready for Execution: NO -- amendments required

The tasklist should not be executed as-is due to the 3 incorrect API assumptions. After applying the amendments below, the tasklist is ready.

### Blocking Amendments Applied: 5 (see Post-Reflection Amendments in tasklist)
