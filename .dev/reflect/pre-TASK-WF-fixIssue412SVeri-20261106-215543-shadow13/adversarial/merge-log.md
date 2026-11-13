# Merge Execution Log — reflect Wave 4

Base: Variant 1 (analyzer/sonnet card, selected via Level-1 tiebreaker after 0.04 combined-score margin)

## Changes Applied

| # | Change | Source | Status | Provenance |
|---|--------|--------|--------|------------|
| 1 | Keep V1 F1 (staging discipline ungated) as merged finding M-001, calibrated 0.70 | Base | applied | Base (original) |
| 2 | Keep V1 F2 (no-commit/no-push ungated) as M-002, calibrated 0.65 | Base | applied | Base (original) |
| 3 | Keep V1 F3 (AC2 force-path wording ambiguity) as M-003, calibrated 0.75, downgraded to advisory per Round-2 resolution | Base (modified) | applied | Base (original, modified) — shipped tests resolve the ambiguity; wording nit |
| 4 | Add scope qualifier: V2's 9/9 unit coverage stands (INF-001..009 all carried); M-001/M-002 are gating gaps, not coverage gaps | V2 | applied | Variant 2, adherence summary |
| 5 | Record V3 F1/F2 as REFUTED with evidence (17-item pin test:17-35 + AC2-mandated divergence plan:36; contents assertion test:367-368), retained as a residual advisory line | V3 | applied | Variant 3, findings + Round 2 rebuttals |

## Post-Merge Validation
- Structural integrity: merged verdict is flat YAML with 3 findings + 1 advisory — pass
- Internal references: every citation resolves to a file read this run — pass
- Contradiction re-scan: refuted findings are recorded as refuted, not asserted — no new contradictions

## Summary
Planned 5, applied 5, failed 0, skipped 0. Convergence 100% (6/6 points resolved).
