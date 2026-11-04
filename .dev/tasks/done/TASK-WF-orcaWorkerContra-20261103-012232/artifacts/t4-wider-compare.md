# Task 4: wider suite compared with the Task 1 baseline

Command, run after the Orca section was added, copied and synced (`make sync-dev`):

```sh
PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/core tests/commands tests/recommend tests/cli -q -rf --ignore=tests/cli/eval/test_perf_home_setup.py -p no:cacheprovider
```

| Run | File | Summary line |
|---|---|---|
| Baseline (Task 1) | `./artifacts/t1-baseline-wider.txt` | `8 failed, 3008 passed, 5 skipped, 1 xpassed, 5 warnings in 56.92s` |
| After Task 4 | `./artifacts/t4-wider.txt` | `5 failed, 3011 passed, 5 skipped, 1 xpassed, 5 warnings in 60.60s` |

Both runs collected the same 3022 tests (8 + 3008 + 5 + 1 and 5 + 3011 + 5 + 1).

## Per-test comparison

`-q` lists only failing tests by name, so the comparison is over the `FAILED` lines: a test that passed in the baseline and fails now would appear as a `FAILED` line in the new run that is absent from the baseline. `comm -13` of the two sorted `FAILED` lists printed nothing, so no such test exists.

| Test | Baseline | After Task 4 | Label in `./artifacts/t1-accepted-failures.md` |
|---|---|---|---|
| `tests/cli/eval/test_ban_import_rule.py::test_clean_tree_passes_ruff_check` | failed | failed | accepted |
| `tests/cli/eval/test_ban_import_rule.py::test_synthetic_import_anthropic_is_flagged_by_ruff` | failed | failed | accepted |
| `tests/cli/eval/test_ban_import_rule.py::test_ban_message_references_fr_g1` | failed | failed | accepted |
| `tests/cli/eval/test_claude_process_adapter.py::test_ruff_flags_synthetic_anthropic_import_under_cli_eval` | failed | failed | accepted |
| `tests/cli/eval/test_claude_process_adapter.py::test_ruff_passes_on_real_adapter_module` | failed | failed | accepted |
| `tests/cli/test_verify_sync_hooks.py::test_V1_clean_tree_exits_zero` | failed | passed | accepted |
| `tests/cli/test_verify_sync_hooks.py::test_V2_missing_claude_hook_detected` | failed | passed | accepted |
| `tests/cli/test_verify_sync_hooks.py::test_V7_regression_to_master` | failed | passed | accepted |

Every remaining failure is labelled `accepted` in `./artifacts/t1-accepted-failures.md`. The five that still fail need the `ruff` executable, which this environment does not have (`uv run ruff` reports `Failed to spawn: ruff`). The three `test_verify_sync_hooks.py` tests now pass. This task ran `make sync-dev` before the run, which is the likely reason; the cause was not traced further, and a failure that turned into a pass cannot break the comparison.

Result: no test that passed in the baseline fails now.

## Tracked files

`git status --short` was captured before and after the run; the two outputs are identical, so the run changed no tracked file.
