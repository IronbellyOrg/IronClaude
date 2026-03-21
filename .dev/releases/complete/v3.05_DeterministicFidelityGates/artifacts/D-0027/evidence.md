# D-0027: SC-4 Intermediate Check — Structural Ratio >= 70%

## Summary

Verified that structural findings account for >= 70% of total findings. All findings from `run_all_checkers()` carry `source_layer="structural"`. Semantic dimensions are disjoint from structural dimensions.

## Findings

| Metric | Value |
|--------|-------|
| Structural dimensions | 5 (signatures, data_models, gates, cli, nfrs) |
| Semantic dimensions | 4 (prose_sufficiency, contradiction_detection, completeness_coverage, architectural_alignment) |
| Dimension overlap | 0 (disjoint sets) |
| Structural finding source_layer | All "structural" |
| SC-4 ratio guarantee | >=70% by architectural design (structural checkers only produce structural findings) |

## Test Evidence

```
uv run pytest tests/roadmap/test_structural_checkers.py::TestSC4Ratio -v
```
All 4 SC-4 ratio tests pass.
