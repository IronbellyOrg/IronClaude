# Phase 7-8 tests-gate summary (item 9.1)

WT=/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/
TASK_DIR=/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/

## File manifest (absolute WT tests/troubleshoot/ paths)

Harness:
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/_assertions.py`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/_procedures.py`

21 new tests + 2 edited: see `qa-input-manifest-tests.md`. All live under `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/`.

## Per-file test counts (item 8.1)

175 new + 70 pre-existing pass + 1 known-red e4 = 246 collected, 245 passed.

## Fixture tree

125 files: 88 assertion + 27 procedure/counter + 9 regression + MANIFEST. Harness §4.1 129 overcounted procedure files by 4.

## Known-red

`tests/troubleshoot/backtest/test_backtest_e4.py::test_backtest_e4_new_gate_catches_via_contract_enumeration_ref` — do not fix.

## Sources every lens must open

- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/research/07-gap-fill-test-harness.md`
- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/research/07-gap-fill-reconcile.md` §X-3 / depth-3
- merged-report-v2.md R-14 + R-19
- Phase 8 verdict PASS at `phase-outputs/plans/phase8-verdict.md`
