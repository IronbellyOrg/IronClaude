# Phase 5 Eval-Module Test Suite — Summary

**Date:** 2026-06-03
**Command:** `uv run pytest tests/recommend/`
**Raw output:** `phase5-pytest.txt`

| Metric | Value |
|---|---|
| Overall | **PASSED** |
| Tests run | 37 |
| Passed | 37 |
| Failed | 0 |
| Exit code | 0 |

## Coverage added since Phase 3 (17 → 37)

| File | Tests | Covers |
|---|---|---|
| `test_dispatch.py` | 7 | 5 dispatch outcomes + cold-insert→warm-to-hit round-trip |
| `test_best_model.py` | 8 | all 4 tiers, 0.70 floor (incl. none-qualify suppression), quality tie-break confidence, balanced default, <0.5 confidence suppression, based_on |
| `test_eval_pipeline.py` | 5 | 5 grader assertion types, grade_text pass_rate, MODE_MATRIX panels, aggregate_by_model, finalize round-trip (results JSON + row best_model/eval_history patch) |
| `test_cache.py` / `test_telemetry.py` | 15 | (Phase 3 foundation, unchanged) |

**Failure table:** none.

## Note on the best_model fix during this step

Initial run surfaced 1 failure (`test_quality_picks_highest_pass_rate_tiebreak_tokens`):
a quality tie on pass_rate was suppressing the hint (confidence 0). Fixed the
`quality` tier so that when pass_rate ties, confidence is computed from the
tie-break metric (mean_tokens) within the tied-top group — a clearly-cheaper
equal-quality model is a confident pick, not model-agnostic. Re-run: 37/37 pass.

No `import anthropic` anywhere in `cli/recommend/`. ruff clean.
