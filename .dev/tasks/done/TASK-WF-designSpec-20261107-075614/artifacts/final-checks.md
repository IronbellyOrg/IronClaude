# Final checks (Task 13)

Run on 2026-11-07T13:16Z in the worktree for issue 375, after `make sync-dev`. Base-commit record: `./artifacts/base-full-suite.log`, `./artifacts/base-lint.log`, `./artifacts/base-format.log` (Task 1).

## Results

| Command | Result |
|---|---|
| `make sync-dev` then `make verify-sync` | exit 0, "All components in sync." |
| `make lint` | exit 0, "All checks passed!" |
| `uv run ruff format --check src/ tests/` | exit 1, 12 files would be reformatted, 1763 already formatted; the 12 files are the same list as the base record (compared by file path; base: 12 reformatted, 1757 formatted) |
| `uv run pytest -q tests` | 2 failed, 17199 passed, 137 skipped, 2 xpassed (full output: `./artifacts/t13-full-suite.log`) |
| `uv run pytest tests/cli/test_verify_sync_hooks.py tests/unit/test_cli_install.py -q` | 103 passed |

## Failing test ids against the base-commit record

Full suite failures this run:

- `tests/cli/eval/test_claude_process_adapter.py::test_ruff_flags_synthetic_anthropic_import_under_cli_eval`
- `tests/cli/eval/test_claude_process_adapter.py::test_ruff_passes_on_real_adapter_module`

Base-commit record after `make sync-dev` (3 failed, 16955 passed):

- `tests/cli/eval/test_claude_process_adapter.py::test_ruff_flags_synthetic_anthropic_import_under_cli_eval`
- `tests/cli/eval/test_claude_process_adapter.py::test_ruff_passes_on_real_adapter_module`
- `tests/unit/test_ccsession_tiers.py::test_a_busy_shim_is_never_stopped_by_a_new_launch`

Every failing id of this run is in the base record. The third base failure (`test_a_busy_shim_is_never_stopped_by_a_new_launch`) passed this run; it is a timing-dependent ccsession shim test and was not touched. No failing id is absent from the base record.

The 12 files that `ruff format --check` reports are Markdown files with Python code fences (for example `src/superclaude/examples/release-spec-template.md` and `tests/roadmap/fixtures/...`); the list, compared by file path, is identical to the base record, and this plan edited only one of them, `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`: its diagnostic is in the existing python fence (same position as in the base record), and the lines this plan added contain no python fence.

## Working tree

`git status --short` lists changes only under `src/superclaude/`, `tests/`, `docs/user-guide/` and `.dev/`; `git diff --cached --name-only` lists no `.claude/` path; `.dev/tasks` is staged with `git add .dev/tasks`.
