# Gap Remediation Tasklist Reflection: v3.1

**Reflection Date**: 2026-03-21
**Source Tasklist**: `gap-remediation-tasklist.md`
**Source Report**: `roadmap-gap-analysis-merged.md`
**Validated Against**: Actual source files on branch `v3.0-AuditGates`

---

## Fidelity Check

| Rec ID | Priority | Corresponding Task(s) | Coverage | Accurate? | Notes |
|--------|----------|----------------------|----------|-----------|-------|
| P0 | BLOCKING | T01, T02, T04 | YES | YES | All three critical bugs (BUG-001, BUG-002, BUG-003) are addressed. T01 wires TurnLedger, T02 wires ShadowGateMetrics, T04 bridges execute_sprint() to execute_phase_tasks(). |
| P1 | HIGH | T05 | YES | YES | TrailingGateResult wrapping added to anti-instinct hook. Return type change and accumulation in sprint loop are both covered. |
| P2 | HIGH | T03, T05 (Part C) | YES | YES | DeferredRemediationLog instantiation (T03) and population from failed gates (T05 Part C) are both present. |
| P3 | MODERATE | T07 | YES | PARTIAL | Task correctly calls build_kpi_report() but uses `str(kpi_report)` for serialization. See Approach issue below. |
| P4 | MODERATE | T11, T12 | YES | YES | Integration test for production path (T11) and test updates for new return types (T12) both present. |
| P5 | LOW | T06 | YES | YES | SprintGatePolicy instantiation covered. |
| P6 | LOW | T08 | YES | YES | Documents the decision to defer attempt_remediation() wiring. Option B recommended. |
| P7 | LOW | T09 | YES | YES | Documentation-only deviation comment. |
| P8 | LOW | T10 | PARTIAL | PARTIAL | T10 covers BUG-011 (TrailingGateResult signature documentation) but does not address the structural recommendation to extract a shared PostTaskGateHook protocol. P8 explicitly said "consider," so partial coverage is acceptable for v3.1. |

**Fidelity Score**: 9/9 recommendations covered. 7 fully accurate, 2 partially accurate.

---

## Approach Validation

### T01: Construct TurnLedger in execute_sprint()
- **Line references correct?** YES. Line 874 is `sprint_result = SprintResult(config=config)`. Line 28 is the TurnLedger import.
- **Proposed fix correct?** YES. Constructor call is straightforward.
- **Sufficiency?** CONCERN. The budget formula `config.max_turns * len(config.active_phases)` may not be correct. `max_turns` is per-subprocess, and multiplying by phase count gives total turns across all phases. This seems reasonable but should be validated against the TurnLedger's actual budget model. The tasklist correctly flags this as a risk.
- **New issues?** None anticipated.

### T02: Construct ShadowGateMetrics in execute_sprint()
- **Line references correct?** YES. Line 21 is part of the models import block containing ShadowGateMetrics.
- **Proposed fix correct?** YES.
- **Sufficiency?** YES. No-arg constructor, simple metrics collector.
- **New issues?** None.

### T03: Construct DeferredRemediationLog in execute_sprint()
- **Line references correct?** YES. Line 885 shows the lazy import pattern (`from .preflight import execute_preflight_phases`).
- **Proposed fix correct?** YES. Lazy import is consistent with existing patterns.
- **Sufficiency?** YES. The tasklist correctly notes that `DeferredRemediationLog` is NOT imported at file top and needs either a lazy or top-level import.
- **New issues?** None. `config.results_dir` is created by SprintConfig initialization as noted.

### T04: Wire execute_sprint() to execute_phase_tasks()
- **Line references correct?** PARTIAL. Lines 890-1156 correspond to the phase loop body. However, the tasklist says "after the execution_mode checks (lines 896-911)" -- actual execution_mode checks are at lines 896-911 (python mode skip at 896, skip mode at 900-911). The next code after line 911 is the isolation directory setup at line 913-916, NOT the ClaudeProcess launch. The tasklist's instruction to add the task-inventory check "before launching ClaudeProcess" is conceptually correct but the insertion point needs refinement -- it should be after line 911's `continue` and before line 913's isolation directory setup.
- **Proposed fix correct?** MOSTLY. The approach of adding a `_parse_phase_tasks()` helper and conditionally delegating to `execute_phase_tasks()` is architecturally sound. However:
  - The `_parse_phase_tasks` helper is mentioned but not specified. Its implementation is critical and non-trivial -- it must parse tasklist markdown files for TaskEntry objects. This is the hardest part of T04 and is underspecified.
  - The `PhaseResult` construction in the code snippet uses `datetime.now()` for `started_at` which would be AFTER execution, not before. Should capture `started_at` before calling `execute_phase_tasks()`.
- **Sufficiency?** PARTIAL. The fallback to ClaudeProcess is preserved (correct), but the `_parse_phase_tasks` helper needs a specification or pointer to an existing parser.
- **New issues?** The isolation directory setup (lines 913-916) would be skipped for per-task phases since the `continue` statement exits the loop iteration before reaching it. This is probably correct (per-task execution has its own isolation via `_run_task_subprocess`), but should be explicitly noted.
- **Risk assessment accurate?** YES. HIGH risk is appropriate.

### T05: Add TrailingGateResult wrapping
- **Line references correct?** YES. Line 629 is `evaluation_ms = ...`. Lines 661-684 are the fail path. Line 611 is the `mode == "off"` check (actually line 610-612). Line 792-794 is the anti-instinct hook call in `execute_phase_tasks()`.
- **Proposed fix correct?** YES. The return type change from `TaskResult` to `tuple[TaskResult, TrailingGateResult | None]` is clean.
- **Sufficiency?** YES for Parts A and B. Part C (accumulation in execute_sprint) depends on T04's delegation branch existing.
- **New issues?** The shadow mode early return at line 645 also needs to return a `TrailingGateResult` (not None) because the gate WAS evaluated. The tasklist only mentions returning None for the `mode == "off"` path (line 611). Shadow mode should return `(task_result, gate_result)` with the evaluated result, not `(task_result, None)`. This is a **gap in the tasklist**.

### T06: Instantiate SprintGatePolicy
- **Line references correct?** YES. Line 56 is `class SprintGatePolicy`.
- **Proposed fix correct?** YES.
- **Sufficiency?** YES for v3.1 scope (just making the object reachable).
- **New issues?** None.

### T07: Call build_kpi_report()
- **Line references correct?** YES. Line 1179 is `logger.write_summary(sprint_result)`. Line 137 in kpi.py is `def build_kpi_report(...)`.
- **Proposed fix correct?** **BUG FOUND**. The tasklist says `kpi_path.write_text(str(kpi_report))`. However, `GateKPIReport` has no `__str__` method. It has a `format_report()` method (kpi.py line 102) that returns formatted text. Using `str()` would produce the default dataclass repr, not a human-readable report.
  - **Fix**: Change `str(kpi_report)` to `kpi_report.format_report()`.
- **Sufficiency?** YES (with the str() fix).
- **New issues?** None beyond the serialization method.

### T08: Wire attempt_remediation() or document
- **Line references correct?** YES.
- **Proposed fix correct?** **BUG FOUND in Option A**. The tasklist suggests calling `attempt_remediation(gate_result=gate_result, policy=gate_policy, ledger=ledger)`. The actual signature of `attempt_remediation()` (trailing_gate.py line 354) is: `attempt_remediation(remediation_step, turns_per_attempt, can_remediate, debit, run_step, check_gate)` -- six callable/value arguments, not keyword gate_result/policy/ledger. Option A's code snippet would fail at runtime.
  - This reinforces the recommendation to use Option B (document deviation) for v3.1.
- **Sufficiency?** YES for Option B. Option A would need a complete rewrite to match the actual API.

### T09: Document reimbursement operand deviation
- **Line references correct?** YES. Line 651 is `credit_amount = int(task_result.turns_consumed * ledger.reimbursement_rate)`.
- **Proposed fix correct?** YES. Documentation-only, no behavioral change.
- **Sufficiency?** YES.

### T10: Document TrailingGateResult signature deviation
- **Line references correct?** YES. Line 35 in trailing_gate.py is the `TrailingGateResult` dataclass.
- **Proposed fix correct?** YES. Documentation-only.
- **Sufficiency?** YES for BUG-011. Does not address P8's structural extraction recommendation (acceptable for v3.1).

### T11: Integration test for production path
- **Proposed fix correct?** YES. Mocking strategy is sound.
- **Sufficiency?** YES. Covers all critical verification points.
- **New issues?** Mocking complexity is correctly flagged as a risk.

### T12: Update existing tests for new return types
- **Proposed fix correct?** YES. The tuple unpacking update is straightforward.
- **Sufficiency?** YES, provided all call sites are found via grep.
- **New issues?** None.

### T13: Full regression check
- **Correct?** YES. Standard regression sweep.

### T14: Manual smoke verification
- **Correct?** YES. All 8 grep checks are well-specified.

---

## Refactoring Recommendations

### RR-1: Fix T07 KPI report serialization (REQUIRED)
Replace `str(kpi_report)` with `kpi_report.format_report()` in the T07 code snippet. Without this, the KPI report file will contain a raw dataclass repr instead of formatted markdown.

### RR-2: Fix T05 shadow mode return value (REQUIRED)
The tasklist should specify that shadow mode (line 643-645 in executor.py) must also return `(task_result, gate_result)` with the evaluated TrailingGateResult, not `(task_result, None)`. The gate IS evaluated in shadow mode; the result should be captured for metrics/KPI purposes. Only the `mode == "off"` path should return None for the gate result.

### RR-3: Specify _parse_phase_tasks() in T04 (RECOMMENDED)
T04 references a `_parse_phase_tasks(phase, config)` helper but does not specify how it distinguishes task-inventory phases from freeform phases. Either:
- Point to an existing parser (if one exists in the codebase), or
- Provide a minimal specification: e.g., "Parse the phase file for markdown headings matching `### Task T\\d+` pattern, extract TaskEntry objects from structured blocks."

### RR-4: Fix T04 started_at timing (MINOR)
The T04 code snippet sets `started_at = datetime.now(timezone.utc)` AFTER calling `execute_phase_tasks()`. It should be captured BEFORE the call to accurately reflect phase start time.

### RR-5: Fix T08 Option A signature mismatch (INFORMATIONAL)
Option A's code snippet does not match `attempt_remediation()`'s actual signature. Since Option B is recommended, this is informational only, but should be corrected to avoid confusion if v3.2 revisits this task.

---

## Coverage Summary

| Category | Total | Covered | Gaps |
|----------|-------|---------|------|
| Recommendations (P0-P8) | 9 | 9 (7 full, 2 partial) | P8 structural extraction deferred |
| Bugs (BUG-001 to BUG-011) | 11 | 11 | None |
| Line number references | 20+ | 18 accurate, 2 minor offsets | T04 insertion point needs refinement |
| Code snippet correctness | 14 snippets | 11 correct, 3 with issues | T07 str(), T05 shadow return, T08 Option A signature |

---

## Final Verdict

| Dimension | Rating | Notes |
|-----------|--------|-------|
| **Fidelity** | **PASS** (9/9 recommendations covered) | All bugs and recommendations mapped to tasks. P8 structural extraction appropriately deferred. |
| **Approach Quality** | **PASS WITH AMENDMENTS** | Two code-level bugs found (T07 serialization, T05 shadow return). One underspecified helper (T04 _parse_phase_tasks). One incorrect API signature (T08 Option A). All fixable without architectural changes. |
| **Ready for Execution** | **YES, after amendments** | Apply RR-1 and RR-2 before starting. RR-3 should be addressed during T04 implementation. RR-4 and RR-5 are minor. |

**Overall Assessment**: The tasklist is well-structured with correct wave dependencies, accurate line references (with minor exceptions), and comprehensive bug-to-task mapping. The two required amendments (T07 serialization method, T05 shadow mode return) are small fixes that do not affect the architecture. The tasklist is ready for execution after these amendments are applied.
