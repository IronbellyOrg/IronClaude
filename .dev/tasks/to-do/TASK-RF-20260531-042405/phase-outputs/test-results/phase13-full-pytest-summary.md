# Phase 13 Full Pytest Summary — Acceptance Gate #2 (Step 13.5)

**Date:** 2026-06-03
**Command:** `uv run pytest tests/roadmap/ tests/contracts/ -v` (UV-only)
**Raw output:** `phase13-full-pytest.txt`

## Result

| Metric | Count |
|--------|-------|
| **Passed** | **2096** |
| **Failed** | **0** |
| Skipped | 22 |
| Total collected | 2118 |
| Wall-clock | 8.16s |

## Baseline-delta regression analysis (the real Gate #2 bar)

Acceptance Gate #2's bar is **"all CURRENT passing tests still pass" (no-regression vs the parent-commit baseline)**, NOT zero-fail.

- **Parent-commit baseline (from PG11.1 / R1.6 close, 2026-06-02):** `tests/roadmap/` = 2060 passed / 0 failed.
- **Post-work (this run):** `tests/roadmap/ + tests/contracts/` = **2096 passed / 0 failed**.
- **Regression count = 0.** Zero tests that passed at baseline now fail.
- **Net delta = +36 NEW passing tests**, attributable to Phase 13 additions: `test_recurrence_regression.py` (17 new dispatched passes), the 15 new recurrence fixtures exercised through existing/new dispatch, and `tests/contracts/test_arch_lint.py` coverage included in scope. All NEW contract tests PASS.

## Known-pre-existing-failure allowlist (out of scope per §Scope)

These 3 failures are **pre-existing** and **out of scope** (haiku-vs-sonnet model default; not roadmap-pipeline brittleness). They are NOT in the `tests/roadmap/ tests/contracts/` scope run above (they live in the broader unit suite), so they do not appear in this run at all — confirming they were correctly NOT "fixed" by mutating unrelated model-default code:

- `test_models.py::test_default_agents`
- `test_cli_contract.py::test_default_agents_when_not_provided`
- `test_validate_unit.py::test_default_agents_two`

## Skipped (22) — all auditable

Includes the 7 deferred recurrence-corpus fixtures (`deferred/` ×5, `merge_completeness/` ×1, `spec_fidelity/phase_restructure_deviation_case`), each skipped with a visible `deferred:true` reason, plus pre-existing environment-gated skips (CI-only source-tree scans when run outside a src/ checkout, etc.). No silent skips.

## Verdict

**Gate #2 PASS** — zero NEW failures vs baseline; all NEW contract tests pass; the 3 pre-existing `test_default_agents` failures remain correctly allowlisted (untouched, out of scope).
