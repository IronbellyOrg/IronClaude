# Baseline before any change (Task 1)

Commit: a6fec24480e8cc65abbb16b194625e2ea52238c7 (`git rev-parse HEAD`, branch clayphi/issue-765, unchanged checkout; only untracked `.dev/` files present).
Recorded: 2026-11-25. Tools: uv 0.11.8, jq 1.7 (both present).

| Command | Exit code | Result | Log |
|---|---|---|---|
| `make sync-dev` | 0 | components copied (Hooks 17 files, Templates 52 files) | ./baseline/sync-dev.log |
| `make verify-sync` | 0 | "All components in sync." | ./baseline/verify-sync.log |
| `uv run pytest` | 1 | 2 failed, 25163 passed, 69 skipped, 0 errors (1633.19s) | ./baseline/pytest.log |
| `make lint` | 0 | "All checks passed!" (architecture policy compliant, 4 warnings) | ./baseline/lint.log |
| `uv run ruff format --check .` | 1 | 8 files would be reformatted, 1700 already formatted | ./baseline/ruff-format.log |

## Baseline failures (recorded, not fixed)

- pytest, 2 failures, both because the `ruff` module is missing from the checkout venv (`No module named ruff`, log line 25255):
  - tests/cli/eval/test_claude_process_adapter.py::test_ruff_flags_synthetic_anthropic_import_under_cli_eval
  - tests/cli/eval/test_claude_process_adapter.py::test_ruff_passes_on_real_adapter_module
- ruff format --check, 8 files (none is a ccsession file): CLAUDE.md, repro/boundary_fork_repro.py, src/superclaude/examples/release-spec-template.md, src/superclaude/skills/sc-cleanup-audit-protocol/rules/dynamic-use-checklist.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md, src/superclaude/skills/sc-validate-tests-protocol/SKILL.md, src/superclaude/templates/documents/release-spec-template.md.

Later tasks compare with "no new failure" against this record.
