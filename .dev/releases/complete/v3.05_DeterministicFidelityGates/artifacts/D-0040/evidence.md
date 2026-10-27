# D-0040: --allow-regeneration Flag Behavior Evidence

## Flag Definition
- Location: `src/superclaude/cli/roadmap/commands.py:89-94`
- Type: Click `is_flag=True` on `run` command
- Default: `False`

## Config Wiring
- `RoadmapConfig.allow_regeneration: bool = False` at `models.py:113`
- Passed from CLI through config kwargs at `commands.py:171`

## Guard Behavior

### Without flag (default): patches exceeding 30% threshold → REJECTED
- `check_patch_diff_size(patch)` returns `False`
- Patch marked: `rejected=True`, `rejection_reason` includes ratio and threshold
- Logged at ERROR level

### With flag: patches exceeding 30% threshold → WARNING + APPLY
- `check_patch_diff_size(patch, allow_regeneration=True)` returns `True`
- Logged at WARNING level with patch ID, actual ratio, threshold

## Test Results
```
tests/roadmap/test_remediate_executor.py::TestCheckPatchDiffSize::test_large_change_rejected PASSED
tests/roadmap/test_remediate_executor.py::TestCheckPatchDiffSize::test_large_change_allowed_with_flag PASSED
```
