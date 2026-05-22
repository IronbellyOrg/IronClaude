# D-0005 — evidence index

**Task:** T01.05 — Implement FR-SCH2 eval-id regex guard
**Date:** 2026-05-20

## Code artefacts

| Path | Role |
|------|------|
| `src/superclaude/cli/eval/loader.py` | Adds `EVAL_ID_REGEX`, `InvalidEvalId`, `INVALID_EVAL_ID_EXIT_CODE`, `validate_eval_id`. |
| `src/superclaude/cli/eval/__init__.py` | Re-exports the four new symbols alongside the existing `SchemaError` surface. |
| `tests/cli/eval/test_eval_id_regex.py` | 66 unit assertions covering the full FR-SCH2 contract. |

## Test runs

- Targeted: `uv run pytest tests/cli/eval/test_eval_id_regex.py -v` → **66 passed in 0.15s**.
- Regression: `uv run pytest tests/cli/eval/ -v` → **99 passed in 0.29s** (no upstream regressions).

Full logs captured under `.dev/releases/current/cliEval/evidence/T01.05/`:

- `pytest-targeted.log` — verbose run of the new test module.
- `pytest-regression.log` — verbose run of every test under `tests/cli/eval/`.

## Acceptance-criteria cross-reference

See `spec.md` ("Acceptance criteria → implementation map") for the
per-bullet → per-test mapping.
