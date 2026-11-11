# Task 3: pin check (2026-11-08)

U-14(a): `grep -rn 'L2_VERSION_LINE\|sha256' tests/cli/test_install_hooks.py tests/hooks` found no owner (one unrelated hit, `tests/hooks/fixtures/launch_level/live_probe.py:82`, hashes a command string). `L2_VERSION_LINE` and `L2_HOOK_SHA256` were therefore both placed in `tests/cli/test_install_hooks.py`.

Pinned sha256 of the packaged hook: `963847f218b4f553c89392dc5a58521b6c3a268b323eb16f0a954dde2f710d9c` (both copies, 7517 bytes).

## Tamper check

- Backups: `cp -p` of each copy to a private `/tmp/t3-pin.*` directory.
- Change: one byte at offset 7000 overwritten with `X` (`dd conv=notrunc`), first in `src/superclaude/hooks/scripts/launch-level-pre-push.sh`, then (after restoring it) in `plugins/superclaude/hooks/scripts/launch-level-pre-push.sh`.
- Result, each time: `pytest -k pre_push` gave 2 failed: `test_launch_level_pre_push_script_is_packaged_listed_executable_and_mirrored` (mirror mismatch) and `test_launch_level_pre_push_script_sha256_pin`.
- Restore: `cp -p` from the backup; `cmp` against the backup reported identical for both copies; both sha256 values back to the pinned value; modes still 0755. The hook files are untracked, so `git diff --stat` on them is empty before and after; `git status` for them is unchanged (`??`).
- Full run after restore: `uv run pytest tests/cli/test_install_hooks.py` 49 passed.

## Sync

- `make sync-dev`: exit 0.
- `make verify-sync`: exit 0, "All components in sync", including "_FRESHNESS_SCRIPTS matches src/superclaude/hooks/scripts/*.sh and *.js".
