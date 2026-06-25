# FIX-1 Summary — PRIMARY checkpoint re-run missing INDEX_PATH (DEV-1, Regression HIGH)

- **New positive tests** (`tests/sprint/test_rerun_tasks.py::TestPrimaryCheckpointRerunArgv`):
  - `test_primary_argv_includes_index_path_positional`
  - `test_primary_argv_parses_through_click_command`
  - `test_base_argv_without_positional_is_rejected` (control)
- **FAIL-on-base:** confirmed (`fix1-test-fail-on-base.txt`) — the two helper-based tests fail with `ImportError: cannot import name '_primary_checkpoint_rerun_argv'`; the control test PASSES, proving the base no-positional argv yields exit-2 `Missing argument 'INDEX_PATH'` (the exact DEV-1 mechanism).
- **PASS-on-fix:** confirmed (`fix1-test-pass-on-fix.txt`) — 3 passed.
- **Fix applied:** extracted `_primary_checkpoint_rerun_argv(config, phase, checkpoint_tid)` in `rerun_tasks.py` (inserts `str(config.index_path)` as the INDEX_PATH positional before `--phase`); PRIMARY branch now calls it and warns on a non-zero return code (keeps `check=False` so a genuine re-failure still propagates as a FAIL gate).
- **Landed-path assertion:** the parse test asserts the command no longer trips the missing-positional usage error (exit_code != 2 and `Missing argument` absent).
