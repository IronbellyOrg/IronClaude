# Phase 2 Scoring Formula Verification

- TDD formula domain_spread uses denominator 7: CONFIRMED (`min(domains / 7, 1.0)`)
- Standard formula domain_spread uses denominator 5: CONFIRMED (`min(domains / 5, 1.0)`)
- TDD formula weights sum to 1.00: CONFIRMED (0.20 + 0.20 + 0.15 + 0.10 + 0.15 + 0.10 + 0.10 = 1.00)
- Standard formula unchanged: CONFIRMED (weights 0.25/0.25/0.20/0.15/0.15 = 1.00)
