# A.10.5 Qualitative Gate — Consolidated (fix cycle 1)

**Verdicts:** verification-sufficiency = PASS · operational-correctness = FAIL (2 findings) → fixed → resolved.
**Fix actor:** orchestrator (single serialized actor, I20). 1 fix cycle.

## Findings + resolution

| ID | Sev | Finding | Fix applied |
|----|-----|---------|-------------|
| F-1 | IMPORTANT | A naive file-level stdout-write detector (Step 3.1) would flag the 3 unconditional `print(`s in `parallel.py`'s `if __name__ == "__main__":` demo block (live lines ~331/334/336) + the `example_*`/`parallel_file_operations` convenience prints — none of which are on the swarm dispatch path and which Step 1.5 deliberately leaves untouched. Result: `test_worker_surfaces_have_zero_tui_reachability` RED even after a 100%-correct Phase-1 fix → Step 3.6 suite RED. | Step 3.1 amended: detector MUST scope to dispatch-reachable callables only — `ParallelExecutor` class methods (parallel.py) + dispatch-path functions (dispatch.py) — EXEMPTING the `__main__` demo block and the named standalone convenience/example functions, implemented via AST ancestry. Reconciles with Step 1.5. |
| F-2 | MINOR | DRIFT-3 guard's suggested bare `continue` (Step 2.1) skips both the `is_alive()` break and `time.sleep`, so a persistently-raising reader under production `max_iterations=None` busy-spins forever and never reaches the `exc_box` re-raise — opposite of FR-5 intent. | Step 2.1 amended: on a reader exception, keep last-good snapshot and FALL THROUGH to the loop tail (update with last-good → `is_alive()` break → ceiling check → `time.sleep`) — explicitly NOT a bare `continue`. Seed safe defaults (`state=None, events=[], offset=0`) before the loop. |

## Verified-correct (operational lens, 15/17)
REG-1 cause-1 (Live constructor fit) · REG-1 cause-2 (`quiet` class-attr preserves `inspect.signature(__init__)` → frozen-sig pin green) · DRIFT-3/DRIFT-4 premises real in live poll loop · DRIFT-4 reorder preserves Exit(130) for SIGINT-only (FR-6) · all 4 test seams viable (proven by existing analogous tests) · injected-executor tests have no stdout-capture assertions (quiet flip safe).

## Sufficiency lens (PASS)
Verification net catches both REG-1 co-causes (audit + PTY smoke), frozen-sig drift (tripwire), DRIFT-3/4 (pre-fix-FAIL/post-fix-PASS regressions), CI parity (ruff check + format --check), and the executor-disjoint POST reflect gate. No coverage hole where a regression passes all-green. One non-blocking advisory (guard detection needs AST ancestor tracking — already covered by the Step 3.2 mutation guard's two-polarity test, now reinforced by the F-1 scope amendment).
