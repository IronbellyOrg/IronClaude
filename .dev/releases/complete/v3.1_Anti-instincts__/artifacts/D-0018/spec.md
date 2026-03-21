# D-0018: SprintConfig gate_rollout_mode Field

**Task**: T03.01
**Status**: COMPLETE

## Change

Added `gate_rollout_mode: Literal["off", "shadow", "soft", "full"] = "off"` to `SprintConfig` in `src/superclaude/cli/sprint/models.py`.

## Diff Summary

```python
# Added after wiring_gate_mode field (line 324):
gate_rollout_mode: Literal["off", "shadow", "soft", "full"] = "off"
```

## Verification

- `uv run pytest tests/sprint/test_models.py tests/sprint/test_shadow_mode.py -v` — 131 passed, 0 regressions
- Field accessible from SprintConfig instance with default `"off"`
- No behavioral change: default `"off"` means gate evaluates but result is ignored (NFR-006)
- `Literal` type already imported at line 15
