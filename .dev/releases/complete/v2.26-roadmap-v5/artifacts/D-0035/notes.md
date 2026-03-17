# D-0035: FR-077 Dual-Budget-Exhaustion Placeholder

## Summary

Added dual-budget-exhaustion placeholder to `_print_terminal_halt()` per FR-077.

## Implementation

Added `spec_patch_budget_exhausted: bool = False` parameter to `_print_terminal_halt()`.

When True, appends a note:
```
Note: Both the remediation budget and the spec-patch cycle budget
are exhausted. Full dual-budget recovery is deferred to v2.26.
# TODO(v2.26): implement dual-budget-exhaustion recovery mechanism
```

## Scope

- This is a placeholder only — no functional dual-budget enforcement logic
- The `spec_patch_budget_exhausted` parameter defaults to False
- Normal single-budget terminal halt is unaffected (no dual-budget note)
- Full dual-budget mechanism is deferred to v2.26 per OQ-J resolution

## Code Reference

`src/superclaude/cli/roadmap/executor.py` — `_print_terminal_halt()` lines with `spec_patch_budget_exhausted` check.

## Test Results

- Dual-budget note appears when `spec_patch_budget_exhausted=True` ✓
- No dual-budget note for `spec_patch_budget_exhausted=False` ✓
- Placeholder does not interfere with normal single-budget terminal halt ✓
