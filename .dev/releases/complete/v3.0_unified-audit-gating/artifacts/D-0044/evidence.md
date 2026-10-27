# D-0044: Full-Mode Criteria Validation

**Task**: T09.03
**Status**: COMPLETE
**Date**: 2026-03-19

## Section 7 Phase 3 Full-Mode Activation Gate

### Required Thresholds
- FPR < 5%
- TPR > 80%
- Whitelist stable for 5+ sprints

### Input Data (from T08.02 / D-0037, soft-mode Sprint 1)

| Variable | Value | Source |
|----------|-------|--------|
| measured_FPR | 4.44% | Mean of per-cycle FPRs: [4.35%, 4.64%, 4.35%] |
| sigma_FPR | 0.17% | Standard deviation of 3 cycle FPRs |
| FPR + 2sigma | 4.78% | Upper bound of 95% confidence interval |
| TPR | 100% | 53/53 true positives, 0 false negatives |
| Whitelist stability | 1 sprint (of 5 required) | No changes since activation |

## Threshold Evaluation

### FPR < 5%

```
measured_FPR = 4.44%
4.44% < 5% → TRUE

FPR + 2sigma = 4.78%
4.78% < 5% → TRUE (margin: 0.22pp)
```

**Result**: PASS — FPR meets full-mode threshold, though margin is tight (0.22pp).

### TPR > 80%

```
TPR = 100%
100% > 80% → TRUE (margin: 20pp)
```

**Result**: PASS — TPR comfortably exceeds full-mode threshold.

### Whitelist Stability (5+ sprints)

```
Sprints with stable whitelist: 1
Required: >=5
1 < 5 → FAIL
```

**Result**: FAIL — Insufficient observation period. Only 1 sprint of soft-mode data available.

## Overall Determination

### Result: **FAIL** — Continue Soft Mode

**Rationale**: While FPR and TPR metrics meet the stricter full-mode thresholds, the whitelist stability requirement (5+ sprints) is not met. Only 1 sprint of soft-mode operational data has been collected. Per Section 7 Phase 3, full-mode activation requires stability evidence over 5+ consecutive sprints.

### Specific Remediation Path

1. Continue operating in soft mode for 4+ additional sprints
2. Collect stability data per D-0043 tracking template each sprint
3. Re-evaluate T09.03 after sprint 5 of soft-mode operation
4. If FPR remains < 5% and TPR remains > 80% across all 5 sprints, activate full mode

### Risk Notes

- FPR margin is tight (0.22pp below 5% threshold). If any sprint introduces new false positives, FPR could breach the threshold.
- The 7 dynamic dispatch FPs are major severity — they don't affect soft-mode operation but would block in full mode. Whitelisting may be needed before full-mode activation.
- kwonlyargs gap (SC-009) slightly affects production TPR but not below 80% threshold.

## Acceptance Criteria

- [x] FPR and TPR computed from soft-mode operational data with documented methodology
- [x] Result is unambiguous: FAIL (continue soft mode)
- [x] Whitelist stability verified: insufficient data (1 of 5 sprints)
- [x] FAIL recommendation includes specific remediation path
