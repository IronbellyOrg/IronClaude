# D-0046: Alias Noise v2.1 Improvement Decision

**Task**: T09.05
**Status**: COMPLETE
**Date**: 2026-03-19

## Decision: Alias Noise Resolved — No v2.1 Improvements Required

### Evidence

| Source | Finding |
|--------|---------|
| D-0039/evidence.md (T08.04 noise floor) | Alias-attributable FPR = 0% |
| D-0044/evidence.md (T09.03 criteria) | T09.03 FAIL due to insufficient observation period (1/5 sprints), NOT due to FPR breach |

### Analysis

The T09.03 FAIL result was caused by the whitelist stability observation period requirement (5+ sprints), not by alias noise. Specifically:

- **FPR met the stricter threshold**: 4.44% < 5% (PASS)
- **Alias-attributable FPR**: 0% — all 7 FPs are from dynamic dispatch, not aliases
- **Import alias (`as`) FPs**: 0
- **Re-export (`__init__.py`) FPs**: 0 (excluded by default config)

R6 originally predicted 30-70% FPR attributable to aliases. Actual measurement: **0%**.

### Conclusion

**Alias noise is resolved; no v2.1 improvements required.**

The import alias pre-pass and re-export chain handling features described in R6 deferred mitigation are not needed because:
1. The existing `exclude_patterns` configuration already handles `__init__.py` re-exports
2. No `import X as Y` aliases produce false positive findings
3. The noise floor is zero with comfortable margin

### Acceptance Criteria

- [x] Decision document exists with clear determination: alias noise **resolved**
- [x] Document references T08.04 noise floor characterization (D-0039)
- [x] Document references T09.03 criteria evaluation (D-0044)
- [x] Decision is traceable to measured evidence (0% alias FPR), not speculation
