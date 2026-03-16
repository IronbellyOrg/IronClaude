# D-0017 Evidence — TestIsolationWiring

## Task: T05.01

**Command:** `uv run pytest tests/sprint/test_phase8_halt_fix.py::TestIsolationWiring -v`

## Result: 4 PASSED

```
tests/sprint/test_phase8_halt_fix.py::TestIsolationWiring::test_isolation_dir_created_with_one_file_before_subprocess_launch PASSED
tests/sprint/test_phase8_halt_fix.py::TestIsolationWiring::test_isolation_dir_removed_after_successful_phase PASSED
tests/sprint/test_phase8_halt_fix.py::TestIsolationWiring::test_isolation_dir_removed_after_failed_phase PASSED
tests/sprint/test_phase8_halt_fix.py::TestIsolationWiring::test_startup_orphan_cleanup_removes_stale_isolation_tree PASSED
============================== 4 passed in 0.10s ==============================
```

## Tests Implemented

- **T04.01**: `test_isolation_dir_created_with_one_file_before_subprocess_launch` — asserts isolation dir exists with exactly 1 file at Popen boundary
- **T04.02**: `test_isolation_dir_removed_after_successful_phase` — asserts isolation dir absent after phase completes successfully
- **T04.03**: `test_isolation_dir_removed_after_failed_phase` — asserts isolation dir absent after HALT result (finally block)
- **T04.04**: `test_startup_orphan_cleanup_removes_stale_isolation_tree` — asserts shutil.rmtree called on base .isolation dir at startup

## Acceptance Criteria

- [x] `tests/sprint/test_phase8_halt_fix.py` exists with `TestIsolationWiring` class containing 4 test methods
- [x] All 4 tests pass
- [x] Tests verify isolation directory lifecycle at subprocess launch boundary
