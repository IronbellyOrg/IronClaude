# Task 16: red tests are environmental (read-only measurement)

Run on branch ironbelly/remove-approved-route, host with unreadable /proc/sys/kernel/random/boot_id (`ls` prints "Transport endpoint is not connected"; the job identity hook and the claim preflight need it).

- tests/skills/test_issue_orca_worktree.py: 45 failed, all in the governed-launch preflight tests (`W-ENFORCEMENT-ABSENT`, "this host lacks /proc/sys/kernel/random/boot_id"); the new test test_pr16_... passes.
- tests/hooks/: 148 failed in test_launch_job_identity.py (60), test_launch_level_pre_push.py (85), test_launch_level_guard_with_identity.py (3); all about the job identity hook. tests/hooks/test_launch_level_guard.py and test_launch_level_guard_l2_tokens.py: 0 failed.
- No failing test name contains the approval cases. Not compared against an untouched baseline run (UNVERIFIED), because a baseline needs a second checkout and stash/reset are not allowed.
