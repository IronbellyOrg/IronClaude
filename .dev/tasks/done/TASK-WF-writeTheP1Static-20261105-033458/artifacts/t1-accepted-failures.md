# T1 accepted failures (baseline, before any edit of this plan)

Baseline files (all under `./artifacts/`): `verify-sync-baseline.txt`, `ac-c3-baseline.txt`, `t1-baseline-wider.txt`, `lint-baseline.txt`, `format-baseline.txt`. These five exist, and with this file they are the six files Task 1 names.

## Result

No test fails in either test baseline taken after the dev tools were installed:
- `ac-c3-baseline.txt`: `tests/skills/`, 1109 passed, rc=0.
- `t1-baseline-wider.txt`: the wider run, 6616 passed, 29 skipped, 1 xpassed, rc=0.
- `lint-baseline.txt`: `make lint` rc=0, 0 errors, 5 size warnings (existing); `ruff check` passed.
- `format-baseline.txt`: 5 files already formatted, rc=0.
- `verify-sync-baseline.txt`: `make sync-dev` rc=0, `make verify-sync` rc=0.

So the pre-existing failure list is empty.

## First wider run (environment fault, not a pre-existing failure)

The worktree's fresh `.venv` had no `ruff`, so the first wider run (`t1-baseline-wider-no-ruff.txt`) had 5 failures that need the `ruff` program, and the first `make lint` and format check could not start (`Failed to spawn: ruff`). The repo's own dev install (`uv pip install -e ".[dev]"`, as `make install` does; it only changes the gitignored `.venv`) fixed this, and the baselines above were retaken. The five tests, listed for the record, each labelled pre-existing only in the sense that they fail without `ruff` and pass with it:
- pre-existing (needs ruff): tests/cli/eval/test_ban_import_rule.py::test_clean_tree_passes_ruff_check
- pre-existing (needs ruff): tests/cli/eval/test_ban_import_rule.py::test_synthetic_import_anthropic_is_flagged_by_ruff
- pre-existing (needs ruff): tests/cli/eval/test_ban_import_rule.py::test_ban_message_references_fr_g1
- pre-existing (needs ruff): tests/cli/eval/test_claude_process_adapter.py::test_ruff_flags_synthetic_anthropic_import_under_cli_eval
- pre-existing (needs ruff): tests/cli/eval/test_claude_process_adapter.py::test_ruff_passes_on_real_adapter_module
