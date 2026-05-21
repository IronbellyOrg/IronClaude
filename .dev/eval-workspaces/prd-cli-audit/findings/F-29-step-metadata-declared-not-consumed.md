# F-29: Step metadata declared but not consumed -- `is_parallel` unused, Stage B missing from TUI

**Final severity (Stage 2 preliminary)**: LOW
**Pattern tags**: P1, P2, P8
**Identified by**: A-5, A-6
**File:line**: `src/superclaude/cli/prd/executor.py:300-316, 366-367, 371`

## Evidence

```python
# 300 -- step tuples include is_parallel slot
_STAGE_A_STEPS: list[tuple[str, str, str, bool]] = [
    ("check-existing", "Check Existing Work", "_check_existing", False),
    ...
]

# 371 -- is_parallel slot discarded
for step_id, step_name, builder_name, _ in _STAGE_A_STEPS:

# 366-367 -- only Stage A registered in TUI
all_step_ids = [(s[0], s[1]) for s in _STAGE_A_STEPS]
self._tui.register_steps(all_step_ids)
```

## Trace

- `is_parallel`: 4th tuple slot reserved for parallelism control. The loop always discards it (`_`). Zero readers in the entire codebase (`grep -rn "is_parallel" src/superclaude/cli/prd/` returns one match -- the comment at line 300).
- TUI registration: Only `_STAGE_A_STEPS` (9 entries) registered. Stage B (investigation-N, web-research-N, synthesis-N, QA steps, assembly) and Step 15 (`present-complete`) never appear. Later `PrdTUI.update_step` calls with unregistered step_ids silently no-op or produce incomplete progress display.

## Reproduction sketch

Change any tuple's `False` to `True`; observe no behavioral change. Watch a real `prd run` with TUI enabled -- progress display freezes at "Preparation" while Stage B runs underneath.

## Confidence (aggregated)

0.92 -- Agent A verified both via direct grep. The unused field and missing registration are mechanically verifiable.

## Cross-agent corroboration

- **Agent A** identified both the unused `is_parallel` field and the Stage B TUI registration gap, noting they are different defects (one is dead code, the other is missing coverage) in the same metadata surface.
