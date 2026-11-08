# QA Report: Gate C content verification (fix cycle 2)

**Topic:** issue-watch implementation, Gate C (Phases 6 and 7), Step 7.G16
**Date:** 2026-11-08
**Phase:** fix-cycle (content verification, task-qualitative lens)
**Fix cycle:** 2
**Fix authorization:** false (report only; the only file written in the repository is this report; probes ran on a private copy under /tmp that was deleted afterwards)

---

## Overall Verdict: PASS

The one blocking finding of the cycle-2 consolidation (C2-1, verification id N-1 of cycle 1) is fixed. I replayed the probe myself and it no longer launches. The cycle-1 C-1 behaviour still holds. No assertion was weakened or deleted, and no regression and no new blocking content issue was found.

## Per blocking finding

| id | Result | Evidence |
|---|---|---|
| C2-1 (N-1) | FIXED | `cycle.py:1039-1049` (`_launch`) now tests `launch_allowed()` and the `timeout_for(GIT_TIMEOUT_S)` None guard before the git call (1039-1043), runs `_origin_ok` (1044), then tests `launch_allowed()` again (1048-1049, raises `_Skip("budget_exhausted")`) before the context build, `mark_pending`, `_save` and `d.launcher.launch(...)` (1052-1062). Design 8.5 line 647: the launch is not started when `elapsed() > 120`; the step ends with no entry and only a `budget_exhausted` decision line. Both the entry check and the post-git check match `Deadline.launch_allowed()` (`elapsed() <= 120`, `cycle.py:410-412`). `origin_mismatch` is still raised only when a git call ran and returned a mismatch (1044-1045). |

### My own replay of the N-1 probe (private /tmp copy of `src/` and `tests/issue_watch`; import path confirmed to be the copy; source of `issue_watch/` confirmed byte-identical to the repo with `diff -rq`)

I wrote five probes of my own (not the fix agent's test), appended to a copy of `test_cycle.py`, all using the existing `gh_world` fake clock and runner hooks:

| Probe | Clock | Result on the fixed code |
|---|---|---|
| P1 (the N-1 case) | +115 s at the reserved `items` re-read, +10 s inside the second `origin` call (125 s) | exit 0 `cycle_complete`, `launched_issue` None, decisions `[(9, 'budget_exhausted')]`, 2 `origin` calls, 0 launcher calls, store entries `{}` |
| P2 (boundary) | +110 s, then +10 s inside the origin call (exactly 120 s) | launches issue 9, one launcher call (120 s is allowed: `<= 120`), so the new check does not over-block |
| P3 (cycle-1 C-1) | +236 s at the re-read, nothing inside origin | exit 0 `cycle_complete`, `origin` called once, decisions `[(9, 'budget_exhausted')]`, 0 launcher calls, no entry |
| P4 | only +121 s inside the second origin call | exit 0, `budget_exhausted`, 2 `origin` calls, no launcher call, no entry |
| P5 | issues 9 and 10, +115 s then +10 s inside origin | exit 0, no launch, no entry, one `budget_exhausted` decision (issue 9) |

Mutant check on the same copy: I deleted the post-origin check (`cycle.py` lines 1048-1049) and ran the whole copied suite. Result: 4 failed, 2244 passed. The failures are the fix agent's new test `test_a_clock_that_crosses_the_cut_off_inside_the_origin_call_starts_no_launch__fr029_n1` and my P1, P4 and P5. With the check removed, P5 shows the original defect exactly (`launched`, `duration_ms` 125000, entry `launched` with `launches` 1). All cycle-1 C-1 tests and P2/P3 still pass under the mutant, so the new test covers the new check alone and the old tests cover the pre-check. The copy was restored and diffed against the repo file (identical), then deleted.

On the unmutated copy, `tests/issue_watch` gave 2243 passed (2242 in cycle 1 plus the one new test).

### C-1 behaviour (cycle 1) still holds

- P3 above: after a 236 s jump at the re-read, `origin` is called once, exit 0, `budget_exhausted` decision, no entry.
- Repository tests `test_cycle.py:4227-4290` (cycle-start no time left gives exit 3 `gh_timeout` with no git call; 236 s jump at the re-read; the 5 s floor alone with the cut-off patched; fewer than 5 s before the probe) are present and unchanged, and `test_cycle.py:4320-4332` still pins exit 2 `origin_mismatch` for a git call that ran and failed (`failed`, `timeout`, `spawn_error`).

## Assertion weakening check

- The tree is untracked, so there is no diff. I compared line positions instead: every test that the cycle-1 reports cited after the insertion point sits exactly 27 lines lower than cited (C-6 pending-save 4363 to 4390, outcome-save 4390 to 4417, C-7 4421 to 4448, C-8 4447 to 4474, C-9 4492/4508 to 4519/4535, C-10 4567/4582 to 4594/4609, C-13 4602-4631 to 4629-4658, the `pytest.skip` line 4608 to 4635), and every test before the insertion point (4227-4290) is at its old position. The new test occupies 4293-4317 plus blank lines. The same holds in `cycle.py`: `_cycle_reason` moved from 1123 to 1127 (4 added lines in `_launch`), and the cited lines before `_launch` (727, 815, 1017-1019) are unchanged. So the only change in these two files after the consolidation is the added code and the added test.
- The test count rose by exactly one (2242 to 2243). `find ... -newer` over `tests/issue_watch` and `src/superclaude/cli/issue_watch` shows only `test_cycle.py` and `cycle.py` changed after the cycle-2 consolidation file.
- The new test asserts literals (exit 0, `cycle_complete`, `[(9, "budget_exhausted")]`, two `origin` calls, no launcher call, `entries == {}`, issue 9 not in `considered`); it is not derived from the code under test, and it kills the mutant above.
- No new `skip`, `skipif` or `xfail` was added by the fix.

## Regression section

None. Every cycle-1 item marked FIXED or PASS (C-1 to C-13) is still in place: the C-1 tests, C-2 `cycle_complete` and its strict kind check, C-3 crash fallback, C-4 fixtures, C-5, C-6 write-failure tests, C-7, C-8, C-9, C-10, C-11, C-12 and C-13 tests are all present at positions consistent with the uniform 27-line shift, and the full suite passes (2243). No cycle-1 behaviour was altered by the fix beyond the added second check.

## New blocking findings

None. I looked for side effects of the new `_Skip("budget_exhausted")` position: it fires before `mark_pending`, so no pending entry exists to leave behind (confirmed by `entries == {}` in P1, P4, P5); it is a skip, not a stop, so the cycle still ends 0 `cycle_complete` and issue 9 is not stamped into `considered` (never stamped for `budget_exhausted`, as in the existing C-1 tests); the launch timeout stays 120 s and is not shortened.

## Minor notes (not rechecked)

- M-1 (carried from cycle 1): `test_cycle.py:4635` still has `pytest.skip("/proc/self/mountinfo exists on Linux only")`, and `test_cycle.py:735` has a `skipif(os.geteuid() == 0, ...)`; the task's test rule says no test uses skip or skipif. Neither was introduced by cycle 2. Replace by unconditional assertions in a later cleanup.
- M-2: after the second `launch_allowed()` check the `timeout_for(GIT_TIMEOUT_S)` None guard in `_launch` (cycle.py:1041-1043) is again reachable with real constants only when the clock is between 235 s and 240 s at that point and the cut-off passes first; effectively it is covered by `test_fewer_than_5_s_left_before_the_origin_re_check_is_budget_exhausted__fr029_c1_c11` with the cut-off patched. Not a defect.
- M-3 (carried): the C-3 crash test raises only `RuntimeError`.
- The design's worst-case line 649 ("ends at 240 s") is not strictly true when a git call straddles the cut-off (a launch can start at up to 120 s and end at 240 s; that remains inside the budget now that the check follows the git call). No action needed.

## Self-Audit

**(a) Reliance list:** no `## Inherited Structural Verdict` section was in the prompt; I relied on no structural PASS (standalone behaviour). I did not re-run the pinned ruff check or the Python 3.10 run; those are the structural verifier's scope (Step 7.G15).

**(b) Independent semantic checks:**
- Read design 8.5 (lines 638-649), `Deadline` (cycle.py:383-412) and `_launch` (cycle.py:1007-1075), and checked that the post-git check precedes `mark_pending`, `_save` and `launcher.launch`.
- Ran my own five probes (P1 to P5) on a private copy: P1 and P4/P5 confirm no launch and no entry after the cut-off passes inside the origin call; P2 confirms the 120 s boundary still launches; P3 confirms the cycle-1 C-1 behaviour (origin once, exit 0).
- Ran a mutant (post-origin check deleted): the fix agent's new test and three of my probes failed (4 failed, 2244 passed), showing the check is what prevents the launch; the C-1 tests pass under the mutant, so they were not weakened to hide anything.
- Verified "nothing deleted, nothing weakened" by line-position arithmetic over the cycle-1 citations (uniform +27 shift in `test_cycle.py`, +4 in `cycle.py`), by the test count (2242 to 2243) and by the file mtimes.

**Confidence:** Verified: 6/6 (C2-1 fix; N-1 replay; C-1 behaviour; assertion-weakening check; regression sweep; new-blocking-issue sweep) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 9 | Grep: 4 | Glob: 0 | Bash: 7

## QA Complete
