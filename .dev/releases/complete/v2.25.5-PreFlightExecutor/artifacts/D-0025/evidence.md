# D-0025 Evidence — T04.03: Merge Preflight Results with Main Loop Results

## Summary

After the main phase loop, preflight results and main-loop results are merged into a single
ordered list that preserves the original `config.active_phases` order.

## Merge Strategy

**File**: `src/superclaude/cli/sprint/executor.py`
**Location**: Immediately after the main `for phase` loop exits (before "Sprint finished")

```python
# Merge preflight results with main-loop results in original phase order.
# Build a lookup from phase number → PhaseResult, main-loop results win
# on conflict (they are the authoritative executor record for claude phases).
_merged: dict[int, PhaseResult] = {r.phase.number: r for r in preflight_results}
for r in sprint_result.phase_results:
    _merged[r.phase.number] = r
sprint_result.phase_results = [
    _merged[p.number]
    for p in config.active_phases
    if p.number in _merged
]
```

## Ordering Guarantees

- The final `sprint_result.phase_results` is ordered by iterating `config.active_phases`
- Phase order is always the original config order — no sorting by insertion time
- Phases with no result (e.g., not yet reached when HALTED) are simply absent from the merged list
- Main-loop results take precedence over preflight results for the same phase number
  (defensive; in practice, a phase is either python-mode OR claude-mode, never both)

## Acceptance Criteria Status

| Criterion | Status |
|---|---|
| Combined list contains one PhaseResult per executed phase in original order | ✓ |
| Preflight results (python-mode) appear at original phase indices | ✓ |
| Main loop results (claude-mode) appear at original phase indices | ✓ |
| Skip-mode results appear at original phase indices | ✓ |

## Verification

- `test_merge_ordering_python_then_skip` passes: confirms python phase result at correct index
- `test_preflight_filters_python_only_python_returns_results` confirms 1 result for python phase
- `uv run pytest tests/sprint/ -v` → **696 passed, 0 failed**
