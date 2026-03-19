# D-0042: Soft Mode Activation

**Task**: T09.01
**Status**: COMPLETE
**Date**: 2026-03-19

## Readiness Check

Phase 8 readiness report (D-0041/spec.md) recommendation: **PROCEED TO SOFT MODE**

All four readiness criteria were MET:
- FPR + 2sigma = 4.78% < 15% (margin: 10.22pp)
- TPR = 100% > 50%
- p95 latency = 0.554s < 5s
- Alias-attributable FPR = 0%

## Changes Made

### 1. SprintConfig default
- **File**: `src/superclaude/cli/sprint/models.py:321`
- **Change**: `wiring_gate_mode` default from `"shadow"` to `"soft"`
- **Effect**: All sprint executions now default to soft mode enforcement

### 2. Roadmap pipeline wiring-verification step
- **File**: `src/superclaude/cli/roadmap/executor.py:248`
- **Change**: `WiringConfig(rollout_mode="shadow")` to `WiringConfig(rollout_mode="soft")`
- **Effect**: Roadmap pipeline wiring-verification step operates in soft mode

## Soft Mode Behavior
- Warns on critical findings (does not block)
- Allows major and minor findings to pass silently
- No change to task status (unlike full mode which sets FAIL)

## Verification

```
102 tests passed in 0.23s
- tests/audit/test_wiring_gate.py: 38 passed
- tests/integration/test_sprint_wiring.py: 14 passed (including 2 soft_mode specific)
- tests/integration/test_wiring_pipeline.py: 10 passed
```

Soft mode tests confirmed:
- `test_soft_mode_warns_on_critical`: PASSED
- `test_soft_mode_clean_no_warning`: PASSED

## Traceability
- **Readiness report**: D-0041/spec.md
- **FPR threshold validation**: D-0040/evidence.md
- **Shadow data**: D-0036/evidence.md
- **Activation timestamp**: 2026-03-19
