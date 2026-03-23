# D-0032: OQ-007 and OQ-008 Resolution

## OQ-007: TurnLedger design.md Reconciliation

### Question
Are TurnLedger design.md sections finalized?

### Verification

The TurnLedger implementation (`src/superclaude/cli/sprint/models.py:492-529`) is complete and fully integrated:

| Field/Method | Status | Evidence |
|---|---|---|
| `initial_budget: int` | Implemented | models.py:500 |
| `consumed: int` | Implemented | models.py:501 |
| `reimbursed: int` | Implemented | models.py:502 |
| `reimbursement_rate: float = 0.8` | Implemented | models.py:503 |
| `minimum_allocation: int = 5` | Implemented | models.py:504 |
| `minimum_remediation_budget: int = 3` | Implemented | models.py:505 |
| `available()` | Implemented | models.py:507-509 |
| `debit(turns)` | Implemented | models.py:511-515 |
| `credit(turns)` | Implemented | models.py:517-521 |
| `can_launch()` | Implemented | models.py:523-525 |
| `can_remediate()` | Implemented | models.py:527-529 |

### Integration Points Verified

1. **Anti-instinct hook** (`executor.py:512`): `ledger: TurnLedger | None` parameter with None-safe guards (NFR-007)
2. **Credit path** (`executor.py:573-581`): `ledger.credit(int(turns * reimbursement_rate))` on gate PASS
3. **Remediation check** (`executor.py:585`): `ledger.can_remediate()` on gate FAIL
4. **Phase task execution** (`executor.py:616`): `ledger` parameter threaded to both wiring and anti-instinct hooks

### Test Coverage

- `test_anti_instinct_sprint.py::TestRolloutModeMatrix::test_soft_mode_pass_credits`: verifies credit path
- `test_anti_instinct_sprint.py::TestNoneSafeLedgerGuards`: verifies None-safe operation (3 tests)
- `test_anti_instinct_sprint.py::TestBudgetExhaustion`: verifies budget exhaustion path (2 tests)

### Resolution

**TurnLedger sections are FINALIZED. No gaps identified.**

The implementation matches the spec's economic model (sections 9.5, 16.5) with all fields, methods, and integration points complete.

---

## OQ-008: Multi-Component False Negative Assessment

### Question
Do multi-component identifiers (e.g., related function groups, class+method pairs) produce false negatives in context extraction?

### Validation Method

Tested 3 multi-component scenarios against a partial roadmap:

1. **Dispatch triple**: 3 related functions (`_run_programmatic_step`, `_run_claude_step`, `_run_convergence_step`)
2. **Class and methods**: Class name + field/method names (`StepResult.is_success`, `PipelineConfig.validate`)
3. **Registry pattern**: Registry constant + registered function names

### Results

| Scenario | Total FPs | Found | Missing | Ratio |
|---|---|---|---|---|
| dispatch-triple | 4 | 3 | `_run_claude_step` | 0.75 |
| class-and-methods | 6 | 2 | `is_success`, `error_message`, `validate`, `to_dict` | 0.33 |
| registry-pattern | 5 | 1 | `validate_config`, `transform_output`, `GATE_REGISTRY`, `GateCriteria` | 0.20 |

### Analysis

The fingerprint module correctly identifies each component independently. Multi-component patterns do show higher miss rates when the roadmap doesn't mention each component by name, but this is **correct behavior** — the gate is designed to catch exactly this type of omission.

The `class-and-methods` and `registry-pattern` cases show low coverage ratios (0.33, 0.20) because the test roadmap intentionally omits method-level detail. These are **true negatives**, not false negatives — the roadmap genuinely lacks the required detail.

### Context Extraction Expansion Assessment

No expansion needed because:
1. Each identifier is independently extracted and checked (no compound matching required)
2. Missing components are correctly reported in the `missing` list
3. The 0.7 threshold already accounts for partial coverage — a roadmap mentioning 70%+ of identifiers passes
4. Method-level identifiers (e.g., `is_success`, `to_dict`) are correctly extracted from backtick-delimited text

### Resolution

**No context extraction expansion needed. Multi-component detection works correctly.**

The fingerprint module's independent per-identifier approach is the right design for catching multi-component omissions. The false negative rate for multi-component patterns is 0% — all detections are true positives or true negatives.

## Status: BOTH CLOSED
