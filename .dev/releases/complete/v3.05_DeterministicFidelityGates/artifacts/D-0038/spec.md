# D-0038: Structured Patches with Per-Patch Diff-Size Guard (FR-9)

## Changes Implemented

### 1. RemediationPatch Dataclass
- Added `RemediationPatch` dataclass to `remediate_executor.py` with MorphLLM-compatible fields:
  - `target_file`, `finding_id`, `original_code`, `instruction`, `update_snippet`, `rationale`
  - Tracking fields: `applied`, `rejected`, `rejection_reason`, `rolled_back`, `diff_ratio`
  - `to_morphllm_json()` serialization method

### 2. Diff-Size Threshold Change
- `_DIFF_SIZE_THRESHOLD_PCT` changed from 50 to 30
- Per-patch evaluation via `check_patch_diff_size()`: `changed_lines / patch_original_lines > 0.30` triggers rejection

### 3. Per-File Rollback
- `_handle_file_rollback()` — rollback a single file from snapshot, mark its findings FAILED
- `_check_cross_file_coherence()` — evaluates whether successful files should be rolled back when related files fail
- `execute_remediation()` now returns "PASS", "PARTIAL", or "FAIL"

### 4. Partial Rejection
- Valid patches applied even when others for same file rejected
- Per-file rollback replaces all-or-nothing `_handle_failure()` in the convergence path
- Legacy `_handle_failure()` retained for backward compatibility

### 5. Snapshot/Restore Mechanism
- Existing `create_snapshots()` / `restore_from_snapshots()` / `cleanup_snapshots()` retained unchanged

## Verification
- `uv run pytest tests/roadmap/test_remediate_executor.py -v` — 39/39 pass (zero regressions)
