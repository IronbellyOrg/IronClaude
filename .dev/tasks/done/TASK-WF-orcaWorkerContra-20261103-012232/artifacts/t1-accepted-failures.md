# Task 1 baselines and accepted failures

Both baseline files were written on 2026-11-03 (UTC 20:31-20:33), after the T1 start snapshot and before any file this plan edits was changed. No product file had been edited when they ran.

| Baseline | Command | File | Result line |
|---|---|---|---|
| AC-C3 baseline | `uv run pytest tests/skills/ -q -rf -p no:cacheprovider` | `./artifacts/ac-c3-baseline.txt` | `608 passed in 12.65s`, `rc=0` |
| Wider baseline (for Task 4) | `uv run pytest tests/core tests/commands tests/recommend tests/cli -q -rf --ignore=tests/cli/eval/test_perf_home_setup.py -p no:cacheprovider` | `./artifacts/t1-baseline-wider.txt` | `8 failed, 3008 passed, 5 skipped, 1 xpassed, 5 warnings in 56.92s`, `rc=1` |

Both runs were made with `PYTHONDONTWRITEBYTECODE=1`. `-p no:cacheprovider` only stops pytest writing its `.pytest_cache`; it selects no different tests.

## Tracked files

`git status --short` was captured before the first run, between the runs and after the second run. The three outputs are identical (only the four untracked folders that existed before the plan, plus this package's new `artifacts/` and `progress.md`), so the runs changed no tracked file.

## Failing tests

The AC-C3 baseline has no failing test.

The wider baseline has 8 failing tests. Each is labelled `accepted` (in the plan's list of eight known failures) or `pre-existing` (failing before this plan but not in that list).

| Test | Baseline | Label |
|---|---|---|
| `tests/cli/eval/test_ban_import_rule.py::test_clean_tree_passes_ruff_check` | wider | accepted |
| `tests/cli/eval/test_ban_import_rule.py::test_synthetic_import_anthropic_is_flagged_by_ruff` | wider | accepted |
| `tests/cli/eval/test_ban_import_rule.py::test_ban_message_references_fr_g1` | wider | accepted |
| `tests/cli/eval/test_claude_process_adapter.py::test_ruff_flags_synthetic_anthropic_import_under_cli_eval` | wider | accepted |
| `tests/cli/eval/test_claude_process_adapter.py::test_ruff_passes_on_real_adapter_module` | wider | accepted |
| `tests/cli/test_verify_sync_hooks.py::test_V1_clean_tree_exits_zero` | wider | accepted |
| `tests/cli/test_verify_sync_hooks.py::test_V2_missing_claude_hook_detected` | wider | accepted |
| `tests/cli/test_verify_sync_hooks.py::test_V7_regression_to_master` | wider | accepted |

No failing test is labelled `pre-existing`: the wider baseline's failures are exactly the eight accepted ones.
