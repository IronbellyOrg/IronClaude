# D-0007 — evidence index

**Task:** T01.08 — Author NFR-SEC1 path-traversal prevention test set
**Date:** 2026-05-20

## Code artefacts

| Path | Role |
|------|------|
| `tests/cli/eval/test_path_traversal.py` | NFR-SEC1 security checklist; 7 named AC tests + 2 cross-cutting invariants (15 cases total after parametrize expansion). |

No production code changed in this task. The function under test
(`validate_eval_id`) is already exported from
`src/superclaude/cli/eval/loader.py` (D-0005, T01.05).

## Test runs

- **Targeted:** `uv run pytest tests/cli/eval/test_path_traversal.py -v` → **15 passed in 0.15s** (≥ 7 named cases, AC bullet 2 satisfied).
- **Regression:** `uv run pytest tests/cli/eval/ -v` → **139 passed in 0.44s** (no upstream regressions from adding this file).

Full logs captured under
`.dev/releases/current/cliEval/evidence/T01.08/`:

- `pytest-targeted.log` — verbose run of the new test module.
- `pytest-regression.log` — full eval-suite regression.

## Acceptance criteria coverage

| AC bullet                                                                                                              | Where evidenced                                                                                                  |
|------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| File `tests/cli/eval/test_path_traversal.py` exists with the 7 named negative cases.                                   | Targeted log shows all 7 named tests present and PASSED.                                                          |
| `uv run pytest tests/cli/eval/test_path_traversal.py -v` exits 0 with ≥ 7 passing tests.                                | Targeted log final line: `============================== 15 passed in 0.15s ==============================`.    |
| Cross-link to FR-SCH2 (T01.05) and TEST-001 (T01.23) in test docstring header.                                          | `test_path_traversal.py` module docstring "Cross-links" section.                                                  |
| `TASKLIST_ROOT/artifacts/D-0007/spec.md` documents the negative-case checklist.                                         | `artifacts/D-0007/spec.md` (this directory).                                                                      |
