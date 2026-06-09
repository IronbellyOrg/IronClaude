# Phase 1 Baseline

- **start_commit:** `ac80f176389572eaa8c902764dc91cb2a3fac2a1` (written to frontmatter `start_commit:`)
- **Baseline test:** `uv run pytest tests/cli/prd/ -q` → **160 passed in 0.57s** (PASS)
- `tests/cli/prd/test_spec_flag.py`: 30 passed (the `--file` `TestSpecFileAttach` assertions are GREEN now; they will be intentionally INVERTED in Phase 3/4 — a change there is EXPECTED, not a regression).
- Raw output: `phase-outputs/test-results/phase1-baseline-pytest.txt`
