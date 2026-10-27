# freshness-hook-fix — closeout

**Status:** complete (shipped on master via commit `184edf7`).
**Closeout commit:** see PR for `feat/freshness-auggie-closeout` branch.

## What shipped

- `src/superclaude/hooks/scripts/freshness-pre-edit.sh:83` — new `create_allowed` decision arm. `Write` to a path with no on-disk file is allowed (resolves the catch-22 where the gate blocked new-file creation because there was no prior `Read`, and the `Read` itself failed because the file did not exist).
- `tests/hooks/test_freshness_pre_edit_create_case.py` — 3 behavioral tests for the create-vs-edit distinction (all green).
- `tests/cli/test_install_hooks.py::test_real_hooks_json_gates_write_in_pre_tool_use` — Proposal B's matcher-pinning regression guard (defense-in-depth concession from the adversarial debate).
- `CHANGELOG.md` Unreleased — `create_allowed` reason documented.
- `docs/user-guide/freshness-hooks.md` — telemetry enum updated; "Write to nonexistent files is blocked" known-limitation section marked resolved.

## Decision artifact

`freshness-hook-fix-debate.md` (in this directory) — Proposal A vs B adversarial scoring; Proposal A won 4.275 vs 0.308.
