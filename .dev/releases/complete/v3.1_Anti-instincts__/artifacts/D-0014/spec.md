# D-0014: Sprint-side Integration Exports

## Status: COMPLETE

## Changes

`src/superclaude/cli/roadmap/executor.py`:
- `_get_all_step_ids()` updated to include `"anti-instinct"` between `"merge"` and `"test-strategy"`
- ANTI_INSTINCT_GATE imported from gates module
- Step ordering maintained: merge → anti-instinct → test-strategy

## Verification
- `uv run pytest tests/roadmap/ -x` → 1247 passed, 0 failed
