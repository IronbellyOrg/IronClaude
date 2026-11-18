# Wave 3C — blind calibration, reviewer-1 card (haiku-class calibrator, disjoint from sonnet reviewer)

## Card scores

Citation grounding 0.85 / Coverage completeness 0.60 / Deviation-classification clarity 0.60 / Risk surface coverage 0.50 / Recommendation actionability 0.25 → **mean 0.56**.

## per_finding (shadow step 5)

```yaml
calibration:
  per_finding:
    F1: 0.92
    F2: 0.80
    F3: 0.45
```

## Calibrator verdicts on self-reported confidence

F1 0.90 about right → 0.92 (supports a wording-claim finding; not a conclusion that the added metadata violates the spec — the metadata comes from the spec itself); F2 0.80 about right ("only count grep hits" slightly overstates; ACs also constrain diff shape); F3 0.60 too high → 0.45 (observable but less firmly supported; spec explicitly requires the added metadata).

Limits: issue-summary unavailable to calibrator; card file updated to the verbatim findings-block version during inspection.
