# Reviewer card — coverage completeness (sonnet/analyzer)

self_confidence: 0.87 → calibrated 0.80 (missed the F1 base-acquisition risk — risk-surface coverage docked)

coverage_pct: 0.917 (20 COVERED + 4 PARTIAL/24). Full FR/NFR/AC→step table reproduced in REPORT §3.
- PARTIAL: NFR-2 (G4 cost-band doc), NFR-5 (G3 companion coordination), AC-7 (G2 emit↔read test), AC-9 (G1 mapping omits AC-9).
- Positive: bootstrap trap correctly avoided; FR-9 headless signal pinned (TTY-absence).
