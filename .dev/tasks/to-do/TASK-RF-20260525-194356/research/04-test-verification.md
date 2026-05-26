# Test & Verification Research

Status: Complete

## Test infrastructure findings

Evidence tags: `[CODE-VERIFIED]` means the claim is verified against repository files cited on the same bullet; `[TASK-DECISION]` means a design/task choice derived from the critiqued feature design rather than pre-existing code.

- [CODE-VERIFIED] `pyproject.toml` defines the package CLI entry point as `superclaude = "superclaude.cli.main:main"` at `pyproject.toml:64` through `pyproject.toml:66`, so CLI tests should import `superclaude.cli.main:main` or invoke that Click object.
- [CODE-VERIFIED] `pyproject.toml` configures pytest to discover `tests/`, `test_*.py`, `Test*`, and `test_*` at `pyproject.toml:101` through `pyproject.toml:110`.
- [CODE-VERIFIED] `tests/cli/test_cli_registration.py` uses `click.testing.CliRunner`, imports `main` from `superclaude.cli.main`, and exercises the live Click object at `tests/cli/test_cli_registration.py:23` through `tests/cli/test_cli_registration.py:26` and `tests/cli/test_cli_registration.py:57` through `tests/cli/test_cli_registration.py:59`.
- [CODE-VERIFIED] `tests/cli/test_cli_registration.py` pins top-level commands in `EXPECTED_TOP_LEVEL_COMMANDS` at `tests/cli/test_cli_registration.py:29` through `tests/cli/test_cli_registration.py:48`; add `init-lite` there.
- [CODE-VERIFIED] The roster test compares `main.commands.keys()` against the frozen set at `tests/cli/test_cli_registration.py:73` through `tests/cli/test_cli_registration.py:82`; new command registration must update this test intentionally.
- [CODE-VERIFIED] The help smoke test invokes `--help` for each top-level command at `tests/cli/test_cli_registration.py:108` through `tests/cli/test_cli_registration.py:119`; `init-lite --help` must exit 0.
- [CODE-VERIFIED] `Makefile` requires UV-based commands: `make test` runs `uv run pytest` at `Makefile:12` through `Makefile:15`, `make lint` runs `uv run ruff check .` at `Makefile:47` through `Makefile:50`, and `make format` runs `uv run ruff format .` at `Makefile:52` through `Makefile:55`.
- [CODE-VERIFIED] `Makefile` syncs `src/superclaude/skills`, `src/superclaude/agents`, and `src/superclaude/commands` into `.claude/` via `make sync-dev` at `Makefile:108` through `Makefile:136`; task validation should include `make sync-dev` and `make verify-sync` after adding command/skill sources.

## Required test cases

[TASK-DECISION] Add a focused test file, suggested `tests/cli/test_init_lite.py`, covering:

1. Token estimate: a helper returns `ceil(bytes / 4)` for representative sizes, including 0 and non-multiple-of-4 byte counts.
2. Surface discovery: temporary project with `CLAUDE.md`, `.mcp.json`, `.claude/settings.json`, `.claude/commands/sc/foo.md`, `.claude/skills/foo/SKILL.md`, `.claude/agents/foo.md` returns exactly those surfaces.
3. Dry run: `runner.invoke(main, ["init-lite", "--context-optimized", "--project-root", tmp_path, "--dry-run"])` exits 0 and creates no `.dev/superclaude` directory.
4. Default report: default run writes `.dev/superclaude/context-audit.md`, includes generated marker, includes token summary, and does not create project-guidance scaffold.
5. Scaffold opt-in: `--scaffold` creates `.dev/superclaude/project-guidance/SKILL.md` and `refs/README.md` only under `.dev/superclaude/`.
6. CLAUDE.md preservation: hash or bytes of existing `CLAUDE.md` before/after are identical for dry-run, default, scaffold, and force modes.
7. Idempotency: second default run succeeds and either overwrites only marked generated report or leaves content stable; second `--scaffold` run does not fail when scaffold exists.
8. CLI help: `init-lite --help` includes `--context-optimized`, `--dry-run`, `--output`, `--project-root`, `--scaffold`, and `--force`.
9. Registration: update `EXPECTED_TOP_LEVEL_COMMANDS` to include `init-lite` and ensure existing registration tests pass.
10. No `.claude` writes: test run against temporary project does not create `.claude/` when it was absent and does not write under `.claude/` when present.

## Validation commands

Use UV only:

- `uv run pytest tests/cli/test_init_lite.py tests/cli/test_cli_registration.py -v`
- `make sync-dev`
- `make verify-sync`
- `make lint`

## Summary

The implementation should be verified by focused CLI tests plus sync verification. The most important regression assertions are dry-run writes nothing, `CLAUDE.md` bytes never change, and no target-project `.claude/` files are created or modified.
