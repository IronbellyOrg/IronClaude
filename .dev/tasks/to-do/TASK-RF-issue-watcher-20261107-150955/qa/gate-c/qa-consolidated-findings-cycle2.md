# Gate C cycle 2: consolidated findings (Step 7.G13)

Sources (cycle-1 files, untouched): qa-consolidated-findings.md, qa-fix-report.md, qa-verification-structural-report.md (PASS, 13 of 13 fixed, no new blocking), qa-verification-content-report.md (FAIL: 12 of 13 fixed as stated, 1 new blocking finding introduced by the fix of C-1).

blocking: 1, minor: 3 (new, from the cycle-1 verification) plus the 56 minor notes of qa-consolidated-findings.md carried forward unchanged and never rechecked.

Cycle-1 findings marked NOT FIXED: none. (C-1 is FIXED "with the side effect in N-1".)

## Blocking

| id | originating report | file | evidence |
|---|---|---|---|
| C2-1 (verification id N-1) | qa-verification-content-report.md | `src/superclaude/cli/issue_watch/cycle.py:1039-1058` (`_launch`) | The only `launch_allowed()` call (cycle.py:1039) now runs before the origin re-check, which can take up to 10 s, and nothing re-tests the 120 s cut-off between the git call, the pending write and `d.launcher.launch(...)`. Probe on a temporary copy: clock +115 s at the reserved `items` re-read (cut-off passes), then +10 s inside the second `origin` call (elapsed 125 s) gave exit 0, `launched_issue` 9 and one launcher call. Design 8.5 line 647: the launch is not started when `elapsed() > 120`; the step ends with a `budget_exhausted` decision line and no entry. No test advances the clock inside the origin call. Required fix: keep the `timeout_for(GIT_TIMEOUT_S)` None guard before the git call and test `launch_allowed()` after the origin check (or both before and after); add a case where the clock advances inside the second origin call and expect exit 0, a `budget_exhausted` decision and no entry; adjust the C-1 tests that assert "origin called once" after a 236 s jump deliberately (keep the pre-check as well so they stay valid). |

## Minor notes (new, not rechecked)

- M-1 (content verifier): `test_cycle.py:4606-4608` uses `pytest.skip(...)`; the task's test rule says no test uses skip, skipif or xfail. Package is Linux-only, so the skip never fires here. Replace by an unconditional assertion.
- M-2 (content verifier): once C2-1 is fixed by checking the cut-off after the git call, the `timeout_for(GIT_TIMEOUT_S)` None guard in `_launch` becomes reachable with the real constants again.
- M-3 (structural verifier): the C-3 crash test raises only `RuntimeError`; catching only `RuntimeError` instead of `Exception` survives. Minor.

|F_n| = 1.
