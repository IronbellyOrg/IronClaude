# Baseline on the unmodified tree (Task 1)

Tree: the branch `clayphi/issue-599` at HEAD `862384852faebe3255c2876527103696cfd3cf3b`, with only untracked `.dev/` paths (Q0 snapshot tree ce2a3f5e4c9bcd637ed79391d392bb175bd17671).

## Run order

1. `make sync-dev` ran first (exit code 0, started 2026-11-26T14:34:26Z; agents 49 files, commands 36, hooks 17, templates 52). It ran before `uv run pytest`.
2. `uv run ruff --version` and the three ruff commands below (after the sync).
3. `PYTHONDONTWRITEBYTECODE=1 uv run pytest -p no:cacheprovider -rfE` on the whole suite (`testpaths = ["tests"]`), started 2026-11-26T14:34:37Z, ended 2026-11-26T15:02:00Z.

## pytest result

pytest summary line: `===== 2 failed, 25308 passed, 64 skipped, 9 warnings in 1639.49s (0:27:19) =====`

- pass count: 25308
- fail count: 2
- error count: 0
- skipped: 64

Failing node ids (both fail on the unmodified tree for an environment reason: the venv's `python -m ruff` is not installed, `No module named ruff`; they are in `tests/cli/eval/` and unrelated to this change):

- `tests/cli/eval/test_claude_process_adapter.py::test_ruff_flags_synthetic_anthropic_import_under_cli_eval`
- `tests/cli/eval/test_claude_process_adapter.py::test_ruff_passes_on_real_adapter_module`

## ruff baseline

Output of `uv run ruff --version`: `ruff 0.17.3` (the project pins `ruff==0.15.20` in the optional `dev` extra, `pyproject.toml:54`).

| Command | Exit code | Result |
|---|---|---|
| `uv run ruff check src/ tests/` | 0 | `All checks passed!` |
| `uv run ruff format --check src/ tests/` | 1 | `6 files would be reformatted, 1541 files already formatted` |
| `uv run ruff format --check .` | 1 | `8 files would be reformatted, 1705 files already formatted` |

Files the `src/ tests/` format check lists (all untouched by this plan):

- `src/superclaude/examples/release-spec-template.md`
- `src/superclaude/skills/sc-cleanup-audit-protocol/rules/dynamic-use-checklist.md`
- `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`
- `src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md`
- `src/superclaude/skills/sc-validate-tests-protocol/SKILL.md`
- `src/superclaude/templates/documents/release-spec-template.md`

Files the whole-repo format check (`uv run ruff format --check .`) lists: the six above plus `CLAUDE.md` and `repro/boundary_fork_repro.py`.

Because the whole-repo format check exited 1, `make format` is not allowed in this plan (Constraints); formatting is done per edited file with `uv run ruff format <file>`.
