# Test-by-test comparison, baseline (unmodified master) vs after (this branch)

Baseline:  1 failed, 25073 passed, 157 skipped, 2 xpassed, 55 warnings in 925.98s (0:15:25) 
After:     2 failed, 25115 passed, 157 skipped, 2 xpassed, 55 warnings in 869.43s (0:14:29) 

Test ids in baseline: 25076 | in after: 25119
Passed in baseline: 25073 | passed after: 25115

## Passed in baseline but not passed after (regressions)
tests/cli/test_install_keep.py::test_same_content_is_true_only_for_identical_readable_files

## Test ids present in baseline and absent after (disappeared)
(count: 0)

## Test ids only after (new), by file
      8 tests/pr_submit/test_late_inline_comment.py
     35 tests/pr_submit/test_marker_malformed.py

## Failing ids
baseline:
FAILED tests/unit/test_ccsession_tiers.py::test_shim_outlives_the_terminal_that_started_it
after:
FAILED tests/cli/test_install_keep.py::test_same_content_is_true_only_for_identical_readable_files
FAILED tests/unit/test_ccsession_tiers.py::test_shim_outlives_the_terminal_that_started_it

## Non-test steps (exit codes)
sync-dev exit=0   baseline | after: exit=0
test exit=1   baseline | after: exit=1
swarm-imm exit=0   baseline | after: exit=0
swarm-inv exit=0   baseline | after: exit=0
ruff-check exit=0   baseline | after: exit=0
ruff-format exit=0   baseline | after: exit=0
plugin-loaded exit=0   baseline | after: exit=0
fixtures exit=0   baseline | after: exit=0
verify-deps exit=0   baseline | after: exit=0
verify-sync exit=0   baseline | after: exit=0
lint-architecture exit=0   baseline | after: exit=0
verify-sync-hooks exit=0   baseline | after: exit=0
git-diff-check exit=0   baseline | after: exit=0

## Swarm lanes and serial hook tests
swarm-imm baseline:  84 passed, 2819 deselected in 3.84s  | after:  84 passed, 2819 deselected in 3.70s 
swarm-inv baseline:  107 passed, 2796 deselected in 2.29s  | after:  107 passed, 2796 deselected in 1.27s 
verify-sync-hooks baseline:  7 passed in 11.58s  | after:  7 passed in 10.82s 
