# D-0053: Internal Convergence Loop and 1200s Timeout — Implementation Spec

## Task

T08.06 — Enforce Internal Convergence Loop and 1200s Timeout (R-057)

## Deliverable

`src/superclaude/cli/cli_portify/executor.py` — STEP_REGISTRY panel-review entry (AC-011, NFR-001)

## Implementation

### STEP_REGISTRY entry

```python
"panel-review": {
    "step_id": "panel-review",
    "phase_type": PortifyPhaseType.CONVERGENCE,
    "timeout_s": 1200,
    "retry_limit": 0,
},
```

**Key properties:**
- `retry_limit = 0` — NO outer retry; panel-review uses internal `ConvergenceEngine` loop (AC-011)
- `timeout_s = 1200` — 20-minute budget per NFR-001

### Internal convergence

`run_panel_review()` in `steps/panel_review.py` calls `ConvergenceEngine(max_iterations=3)` directly, NOT through `_execute_step_with_retry()`. The engine manages up to 3 internal iterations before reaching a terminal state.

## Verification

```
grep -A 6 '"panel-review"' src/superclaude/cli/cli_portify/executor.py
```

Output confirms `retry_limit: 0` and `timeout_s: 1200`.

**Result:** Verified
