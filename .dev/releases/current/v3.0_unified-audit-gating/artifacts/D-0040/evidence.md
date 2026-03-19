# D-0040: FPR Threshold Validation

**Task**: T08.05
**Status**: COMPLETE
**Date**: 2026-03-19

## Section 7 Phase 2 FPR Calibration Gate

### Formula
```
measured_FPR + 2 * sigma_FPR < 0.15
```

### Input Values (from T08.02 / D-0037)
| Variable | Value | Source |
|----------|-------|--------|
| measured_FPR | 0.044438 (4.44%) | Mean of per-cycle FPRs: [4.35%, 4.64%, 4.35%] |
| sigma_FPR | 0.001662 (0.17%) | Standard deviation of 3 cycle FPRs |

### Computation
```
measured_FPR + 2 * sigma_FPR
= 0.044438 + 2 * 0.001662
= 0.044438 + 0.003325
= 0.047763
= 4.78%
```

### Threshold Evaluation
```
0.047763 < 0.15 → TRUE
4.78% < 15% → PASS
```

## Result: **PASS**

The measured FPR plus 2 standard deviations (4.78%) is well below the 15% threshold, with a margin of 10.22 percentage points.

### Cross-Check
Re-deriving from raw data:
- Cycle 1: 7 FP / 161 files = 0.04348
- Cycle 2: 7 FP / 151 files = 0.04636
- Cycle 3: 7 FP / 161 files = 0.04348
- Mean = (0.04348 + 0.04636 + 0.04348) / 3 = 0.04444 ✓
- Variance = ((0.04348-0.04444)² + (0.04636-0.04444)² + (0.04348-0.04444)²) / 2 = 2.762e-06
- Sigma = √(2.762e-06) = 0.001662 ✓
- FPR + 2σ = 0.04444 + 0.00332 = 0.04776 ✓

## Acceptance Criteria
- [x] Threshold computation documented with exact FPR value, sigma value, and result
- [x] Result is unambiguous: **PASS** (proceed to soft mode)
- [x] Computation reproducible from T08.02 metrics
- [x] N/A for FAIL remediation (result is PASS)
