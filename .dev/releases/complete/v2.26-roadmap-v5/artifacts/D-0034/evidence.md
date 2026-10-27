# D-0034: _apply_resume_after_spec_patch() Retired as Dormant

## Summary

`_apply_resume_after_spec_patch()` has been retired from the active v2.26 execution flow per FR-059 (NFR-019).

## Changes Made

In `execute_roadmap()`, replaced the spec-fidelity failure branch:

**Before (active invocation):**
```python
if spec_fidelity_failed:
    resumed = _apply_resume_after_spec_patch(...)
    if resumed:
        ...
        return
```

**After (retired):**
```python
# FR-059: spec-patch cycle retired from active execution.
# _apply_resume_after_spec_patch() retained as dormant (NFR-019).
_ = _spec_patch_cycle_count  # dormant; kept for NFR-019 retention
halt_msg = _format_halt_output(results, config)
print(halt_msg, file=sys.stderr)
sys.exit(1)
```

## Preserved Dormant Code

- `_apply_resume_after_spec_patch()` function definition: RETAINED
- `_spec_patch_cycle_count` variable: RETAINED (referenced dormantly)
- `_find_qualifying_deviation_files()`: RETAINED

## Independent Counters (FR-076)

- Spec-patch counter: `_spec_patch_cycle_count` (dormant, local variable in execute_roadmap)
- Remediation counter: `remediation_attempts` in .roadmap-state.json (active)
- These are entirely independent; no shared state.

## Verification

`uv run pytest tests/sprint/test_executor.py -v -k "spec_patch"` — **2 passed**
- `_apply_resume_after_spec_patch` is still importable (retained as dormant)
- Not called on spec-fidelity failure in v2.26 execution flow
