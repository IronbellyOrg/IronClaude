# T03.22 Evidence — TEST-006 PTY lifecycle integration tests + FR-G1 ban-import

## Task
Author `tests/cli/eval/test_pty_lifecycle.py` (real claude spawn, prompt
readiness, input injection, timeout reaping, transcript existence) and
`tests/cli/eval/test_ban_import_rule.py` (`anthropic` import ban
enforcement). Pin `[tool.ruff.lint.flake8-tidy-imports.banned-api]` for
COMP-013.

## Acceptance Criteria Verification

| AC | Requirement | Verified by |
|----|-------------|-------------|
| AC1 | `tests/cli/eval/test_pty_lifecycle.py` runs a single-eval fixture spawning the real claude binary via PTY and exits 0. | `test_real_claude_help_spawn_and_transcript` PASSED in `pytest-pty-lifecycle-and-ban-import.txt`. |
| AC2 | Test asserts: prompt readiness observed, input injected, transcript file written, timeout reaps the child. | `test_lifecycle_prompt_ready_and_input_injection`, `test_lifecycle_transcript_persisted_end_to_end`, `test_lifecycle_timeout_reaps_child` all PASSED. |
| AC3 | `uv run ruff check src/superclaude/cli/eval/` exits 0 on clean tree AND non-zero on synthetic `import anthropic`; `tool.ruff.lint.flake8-tidy-imports.banned-api` declares the rule per COMP-013. | `ruff-clean-tree.txt` (exit 0) + `ruff-synthetic-import-anthropic.txt` (exit 1, TID251 + FR-G1 message); test trio in `test_ban_import_rule.py` (3/3 PASSED). |
| AC4 | `TASKLIST_ROOT/artifacts/D-0063/spec.md` documents lifecycle test matrix and ban-import rule configuration. | `.dev/releases/current/cliEval/artifacts/D-0063/spec.md` (+ `notes.md`, `evidence.md`) written. |

## Test Result
`uv run pytest tests/cli/eval/test_pty_lifecycle.py tests/cli/eval/test_ban_import_rule.py -v` → **8 passed in 1.83s**
(see `pytest-pty-lifecycle-and-ban-import.txt`).

## Regression Check
`uv run pytest tests/cli/eval/ -q` → **1039 passed in 16.65s** — no
regressions across cli/eval. See `pytest-cli-eval-regression.txt`.

## Ruff Check
`uv run ruff check src/superclaude/cli/eval/` → **All checks passed!**
(see `ruff-clean-tree.txt`).

Synthetic injection verified: `ruff-synthetic-import-anthropic.txt`
shows exit 1 with `TID251` + the FR-G1 remediation message; probe
directory removed after capture; tree restored to clean state.

## Files Added / Modified
- `tests/cli/eval/test_pty_lifecycle.py` — new (5 tests).
- `tests/cli/eval/test_ban_import_rule.py` — new (3 tests).
- `pyproject.toml` — `N818` added to project-wide `ignore` list (justified by stable public-API exception names in `cli/eval/`). The `[tool.ruff.lint.flake8-tidy-imports.banned-api]` table itself was wired in T02.19; T03.22 pins it via tests.
- `src/superclaude/cli/eval/hook_adapter.py` — one relative import made absolute to clear a pre-existing TID252 finding (necessary for AC3 clean-tree).
- `src/superclaude/cli/eval/pty_driver.py` — `ruff --fix` autocorrect of I001/F401 (no semantic change).
- `.dev/releases/current/cliEval/artifacts/D-0063/{spec,notes,evidence}.md` — new.
- `.dev/releases/current/cliEval/evidence/T03.22/{SUMMARY,pytest-*,ruff-*}` — new.
