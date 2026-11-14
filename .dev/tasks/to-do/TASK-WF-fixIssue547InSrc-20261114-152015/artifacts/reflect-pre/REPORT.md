# Reflect (pre-execution, Tier 1, inline) of the issue 547 plan

Run 2026-11-14. Mode pre. Tier reached 1. Status: partial (degraded: the calibrator and evidence-validator agents were not spawned; the session ran a bounded inline Tier 1 pass, recorded here so nothing reads as a full reflect).

## Coverage of the source (all 12 requirements mapped)

- every git call carries `-c core.fsmonitor=false` after `-C <path>`: Task 2
- status gets `--ignore-submodules=all`: Task 2 (owner design A)
- config read before status; filter selected by a tracked path (`ls-files -z` then `check-attr --stdin -z filter`) skips status: Task 4
- reported through the existing `unscanned` row with a new reason: Task 4
- config unreadable or unclear refused: Task 4 (fail closed, `GitCallFailed`)
- `_git` stdin support and three new allow-list entries: Task 2
- T1 counts `len(raw)`: Task 6
- separate commits for T2 and T1: Tasks 5 and 6
- regression tests first, shown failing on old code: Task 1 and Task 6
- pinned tests edited only where forced: Task 3
- no JSON key: Constraints
- do not push: Constraints
Coverage 12 of 12.

## Findings (advisory; the plan is not edited from them)

- Blocking-looking but handled in execution: tests/sweep/test_readonly.py lines 144 to 158 (`test_collect_reaches_git_with_a_lock_free_argv_for_each_worktree`) records every real `_git` subprocess call through `recorder`. After Task 4 there are one to three inspection calls plus one status call per worktree, so its `[c["argv"][3] ...] == expected` assertion must be restricted to the status calls. The plan names only lines 88 and 157 of that file. The executor must make this forced edit in Task 4 and list it in the commit body. Evidence: tests/sweep/test_readonly.py:153-158 and the `_RunRecorder` stub at lines 52-62 (returns the same bytes for every call).
- Minor: Task 2's acceptance names tests that pass "after Task 2" for the submodule cases; both submodule routes are closed by `--ignore-submodules=all` and the `-c` pair, so the statement holds (measured in ./artifacts/validation.md, repro3 and repro4).
- Minor: `OUTPUT_LIMIT` applies to the `ls-files` output; a repository with a huge index fails closed as "worktree not readable". Acceptable and conservative.

## Verdict

Plan is executable. 0 blocking defects in the plan text; 1 forced test edit to expect during Task 4.
