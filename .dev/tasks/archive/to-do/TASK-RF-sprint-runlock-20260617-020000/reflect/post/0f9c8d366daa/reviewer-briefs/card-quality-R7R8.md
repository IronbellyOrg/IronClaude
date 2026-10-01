# Reviewer Card — quality-engineer (scope: R7 / R8 test coverage)

R7: all 13 cases present & named in TestRunLock (test_recovery.py:529-738); 29 tests pass.

| F | Finding | file:line | Severity | Class | Conf |
|---|---------|-----------|----------|-------|------|
| F1 | --ignore-run-lock dropped on tmux relaunch; zero test of flag survival | tmux.py:176-210; models.py:591-594 | HIGH | regression+gap | 0.90 |
| F2 | R8 unmet: no run-lock acquire/release assertions in resume/tmux tests | test_resume.py, test_tmux.py (no refs) | HIGH | gap/drift | 0.95 |
| F3 | Cases 7/8 stub getsignal->SIG_DFL; chain-to-prev branch never fired | test_recovery.py:645,665 | MED | drift | 0.85 |
| F4 | Closure late-binding loop-capture untested across both signals | recovery.py loop; test_recovery.py:632-670 | LOW | gap | 0.80 |
| F5 | Case 5 unconditional FileExistsError tests exhaustion, not single-loser race; coarse assertion | test_recovery.py:602-617 | LOW | drift | 0.80 |
| F6 | Case 2 starttime:None — starttime-match-alive branch untested w/ naming surface | test_recovery.py:557-561 | LOW | gap | 0.75 |

R8 regression suite green (81 passed) but the explicitly-required NEW integration assertions were not added.
