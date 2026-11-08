# Gate C fix report, cycle 2 (Step 7.G14)

**Fix agent:** one `rf-qa` agent with `fix_authorization: true`. **Scope:** `src/superclaude/cli/issue_watch/cycle.py` and `tests/issue_watch/test_cycle.py` only. Cycle-1 fixes were not undone. Minor notes M-1 to M-3 were not fixed.

**Result:** the one blocking finding (C2-1 = N-1) is fixed. `uv run pytest tests/issue_watch/ -q`: 2243 passed (2242 before, plus the new test). `make lint`: pass (0 errors, 5 existing warnings). Pinned `uvx --offline ruff@0.15.20 check` and `format --check` on the 2 changed files: all checks passed, 2 files already formatted.

## Per blocking finding

| id | files changed | what changed |
|---|---|---|
| C2-1 (N-1) | `src/superclaude/cli/issue_watch/cycle.py` (`_launch`) | Kept the cycle-1 pre-check (`launch_allowed()` then the `timeout_for(GIT_TIMEOUT_S)` None guard, both before the git call). Added a second `launch_allowed()` check right after `_origin_ok(...)` succeeds and before the pending write and `launcher.launch(...)`: if the cut-off passed during the git call it raises `_Skip("budget_exhausted")` (exit 0, `budget_exhausted` decision line, no entry, not stamped). `origin_mismatch` is still only for a git call that ran and failed. |
| C2-1 (N-1) | `tests/issue_watch/test_cycle.py` | New test `test_a_clock_that_crosses_the_cut_off_inside_the_origin_call_starts_no_launch__fr029_n1`: clock +115 s at the reserved `items` re-read (pre-check passes), then +10 s inside the second `origin` call (125 s). Asserts exit 0 `cycle_complete`, decisions `[(9, "budget_exhausted")]`, two `origin` calls, no launcher call, no entry, issue 9 not in `considered`. No existing assertion was changed; the C-1 tests that assert one `origin` call after a 236 s jump stay valid because the pre-check is kept. |

## Mutant check (copy under `/tmp`, repo not mutated, copy deleted)

The mutant removes the new post-origin `launch_allowed()` check from a `/tmp` copy of `src/` and runs the copied `tests/issue_watch` with `PYTHONPATH` set to the copy (import path confirmed to be the copy). Result: 1 failed, 2242 passed. The one failure is the new test (`(9, 'launched') != (9, 'budget_exhausted')`). All C-1 tests still pass under the mutant, which shows they are covered by the pre-check and the new test covers the new check alone. `git status` after cleanup shows only the existing untracked and modified paths.

## Notes

- M-2 is now moot in the other direction: with the real constants the `timeout_for(GIT_TIMEOUT_S)` None guard stays reachable only as before; no change made.
- M-1 (`pytest.skip` in `test_cycle.py`) and M-3 (C-3 test raises only `RuntimeError`) are unchanged minor notes.
