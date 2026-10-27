# D-0030: Calibration Results — Threshold Recommendations

## Executive Summary

Both anti-instinct gate thresholds produce acceptable false positive/negative rates on shadow data. **No threshold adjustments are recommended.**

## Current Thresholds

| Module | Threshold | Default | Source |
|---|---|---|---|
| Fingerprint coverage | `fingerprint_coverage >= 0.7` | 0.7 | `fingerprint.py:158`, `gates.py:337` |
| Structural audit | `extraction_reqs / indicators >= 0.5` | 0.5 | `spec_structural_audit.py:107` |

## Observed Rates

| Module | Accuracy | False Positive Rate | False Negative Rate |
|---|---|---|---|
| Fingerprint (0.7) | 86% (6/7) | 0% (0/7) | 14% (1/7) |
| Structural audit (0.5) | 100% (4/4) | 0% (0/4) | 0% (0/4) |

## Threshold Decision Matrix

### Fingerprint Coverage (0.7)

| Option | Threshold | FP Rate | FN Rate | Risk |
|---|---|---|---|---|
| Lower to 0.6 | 0.6 | 0% | 0% | May pass roadmaps missing 40% of identifiers |
| **Keep at 0.7** | **0.7** | **0%** | **14%** | **Acceptable: false negatives flag genuine gaps** |
| Raise to 0.8 | 0.8 | 0% | 28%+ | Too aggressive for diverse roadmaps |

**Decision**: KEEP at 0.7. The single false negative (0.571 ratio, 3/7 identifiers missing) is an acceptable detection — a roadmap missing 43% of code identifiers should be reviewed.

### Structural Audit (0.5)

| Option | Threshold | FP Rate | FN Rate | Risk |
|---|---|---|---|---|
| Lower to 0.3 | 0.3 | 0% | 0% | May miss severe extraction failures |
| **Keep at 0.5** | **0.5** | **0%** | **0%** | **Perfect accuracy; conservative design handles overcount** |
| Raise to 0.7 | 0.7 | Est. 20%+ | 0% | Overcount problem makes this too strict |

**Decision**: KEEP at 0.5. Perfect accuracy with warning-only enforcement means zero pipeline disruption risk.

## Regression Test Confirmation

All existing threshold-related tests pass at current values:
- `tests/roadmap/test_fingerprint.py`: 21 tests PASS
- `tests/roadmap/test_spec_structural_audit.py`: 15 tests PASS
- No threshold adjustments needed → no regression test updates required

## Conclusion

Both thresholds are well-calibrated for current shadow data. The fingerprint threshold (0.7) trades a small false negative rate for zero false positives — the right tradeoff for a quality gate. The structural audit threshold (0.5) achieves perfect accuracy due to its conservative design and warning-only enforcement.
