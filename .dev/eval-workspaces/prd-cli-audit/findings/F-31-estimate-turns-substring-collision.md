# F-31: `_estimate_turns` substring collision -- `verify-task-file` returns 10 instead of intended weight

**Final severity (Stage 2 preliminary)**: LOW
**Pattern tags**: P3, P7
**Identified by**: A-15
**File:line**: `src/superclaude/cli/prd/executor.py:1006-1019`

## Evidence

```python
@staticmethod
def _estimate_turns(step_id: str) -> int:
    if "qa" in step_id or "verify" in step_id or "review" in step_id:
        return 10
    if "assembly" in step_id or "build" in step_id:
        return 30
    if "investigation" in step_id or "synthesis" in step_id:
        return 20
    return 15
```

## Trace

- `verify-task-file` matches `"verify"` -> 10. Likely intended to be a heavy step (verifying a 400+ line task file end-to-end) but gets only 10 turns of budget.
- `research-qa-fix-1` matches `"qa"` -> 10, but gap-filling is heavier work than QA verification.
- `"build" in step_id` would also match a hypothetical `"build-investigation"` (would hit 30 before the 20 branch). Brittle to future step naming.

## Reproduction sketch

Add a step_id like `"build-investigation-1"` -> returns 30, even though investigation logic intends 20.

## Confidence (aggregated)

0.75 -- Agent A verified the substring collision. Impact depends on turn-budget headroom.

## Cross-agent corroboration

- **Agent A** identified the ordering-dependent substring matching and its consequence for `verify-task-file` and future step names.
