# Atom 1 — Confirmed Signatures & Line Numbers

**Confirmed:** 2026-06-08, read directly from live source. No fabrication.

## `src/superclaude/cli/prd/models.py`

### PrdStepStatus enum members (lines 106-118)

Confirmed all 13 members present:
PENDING, RUNNING, PASS, PASS_NO_SIGNAL, PASS_NO_REPORT, INCOMPLETE, HALT, TIMEOUT, ERROR, SKIPPED, QA_FAIL, QA_FAIL_EXHAUSTED, VALIDATION_FAIL.

### `is_failure` property — **lines 144-153** (matches expected ~144-153)

```python
@property
def is_failure(self) -> bool:
    """True if the step ended in a non-recoverable failure."""
    return self in (
        PrdStepStatus.HALT,
        PrdStepStatus.TIMEOUT,
        PrdStepStatus.ERROR,
        PrdStepStatus.QA_FAIL_EXHAUSTED,
        PrdStepStatus.VALIDATION_FAIL,
    )
```

Note: existing idiom uses a **tuple** `(...)` for membership, not a set `{...}`. The new
`is_hard_failure` will follow the same style (tuple) for consistency — functionally equivalent.

### `needs_fix_cycle` property — **lines 155-161** (matches expected ~155-161)

Returns QA_FAIL / INCOMPLETE. Confirmed.

**Edit target for Step 2.2:** add `is_hard_failure` as a `@property` sibling immediately
following `is_failure` (after line 153, before `needs_fix_cycle` at 155).

## `src/superclaude/cli/prd/executor.py`

### Stage-A halt block — **lines 566-575** (matches expected ~566-575)

```python
# STRICT gate failure halts pipeline
if step_result.status.is_failure:
    gate = GATE_CRITERIA.get(step_id)
    if gate and gate.enforcement_tier == "STRICT":
        result.outcome = "halt"
        result.halt_step = step_id
        result.halt_reason = (
            f"STRICT gate failure: {step_result.status.value}"
        )
        break
```

**Edit target for Step 2.3:** rewrite this block to compute `strict_gate_fail` and halt on
`step_result.status.is_hard_failure or strict_gate_fail`, with the distinguishing halt_reason.

### `GATE_CRITERIA` import — **line 46** (`from .gates import GATE_CRITERIA`)

Confirmed in scope. Also used at 568, 727, 944, 1131.

## Drift summary

No drift. All structures match the task's expected line numbers exactly.
