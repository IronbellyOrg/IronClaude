# Installer Mapping Pytest Summary

**Test selection:** Five node IDs co-located in `tests/cli/test_init_lite.py` (per task Step 3.3 explicit allowance: "even if they live inside `tests/cli/test_init_lite.py`"):

- `tests/cli/test_init_lite.py::test_installer_maps_sc_init_lite_protocol_to_init_lite_command`
- `tests/cli/test_init_lite.py::test_installer_keeps_existing_sc_prefix_mapping`
- `tests/cli/test_init_lite.py::test_installer_rejects_non_sc_prefix`
- `tests/cli/test_init_lite.py::test_installer_rejects_sc_skill_without_matching_command`
- `tests/cli/test_init_lite.py::test_installer_rejects_protocol_skill_without_matching_command`

**Command:** `uv run pytest <five node IDs above> -v`
**Run from:** worktree root.
**Date:** 2026-05-27

## Overall Result

PASS

## Counts

- Total tests collected: 5
- Passed: 5
- Failed: 0
- Errors: 0
- Skipped: 0
- Duration: 0.17s

## Failed Test Names

None.

## Pytest Summary Line

```
============================== 5 passed in 0.17s ===============================
```

Raw output: `phase-outputs/test-results/installer-pytest-output.txt`
