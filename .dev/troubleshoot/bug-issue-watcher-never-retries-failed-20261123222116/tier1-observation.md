# Tier 1 observation (static; no live run)
- dispatch.py:415-427: `if not config_path.exists():` ... `if outcome.status == "generated": ... first_run(config_path, defaults, runner, deps_factory)` is the only call to first_run (grep over src/superclaude/cli/issue_watch: single call site, dispatch.py:427).
- dispatch.py:428-436: when the config exists and `_enabled()` is not True, the repo is skipped with `not_enabled` (or `config_unreadable`).
- generate.py:252: generated config has `"enabled": False`; generate.py:256: worktree is `<worktrees_dir>/<name>/Coordinator` (may not exist yet).
- cycle.py:396-402 `validate_setup` raises ConfigError("worktree_invalid") when the worktree is not a directory; first_run.py:176-183 turns that into step `config` failed and `done(step)` leaves enabled false and writes `first-run.txt` ("first-run: failed config: worktree_invalid") to the config's state_dir (first_run.py:138, 170).
- first_run.py:136-137: an already-enabled config returns `already_enabled` without any check (idempotent).
- first_run.py:208-216: an existing store is kept (`state_exists` counts as ok), so a retry does not reset history. record.py:773-775 raises StateExists before touching anything.
- tests/issue_watch/test_dispatch.py:421-426 pins `not_enabled` for a config written with enabled False and no report file; tests/issue_watch/test_first_run.py:179-180 pins the report text "first-run: failed config" + "worktree_invalid".
## Behaviour definitions
(none needed: all behaviours observed directly in source above)
