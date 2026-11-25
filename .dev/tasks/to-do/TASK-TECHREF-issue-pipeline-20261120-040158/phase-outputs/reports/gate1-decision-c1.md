# Gate 1 decision after cycle 1

**Decision: CYCLE-2-REQUIRED**

Numbers used (from the actual files):
- F_1 = 5 (qa-research-consolidated-findings.md: B-1, B-2, B-3, F-1, F-2; 0 synthetic).
- Verification reports valid: qa-research-verification-structural-c1.md (FAIL, 1 BLOCKING: N-1, new) and qa-research-verification-content-c1.md (PASS, 0 BLOCKING). Both carry `Status: Complete` and a `## Verdict:` line.
- F_2 = 1 (N-1) + 0 synthetic = 1.

Rules applied in order:
1. F_1 is not 0, so not an automatic PASS.
2. Regression check: the structural report lists N-1 as NEW content (introduced by gap-fill F-2) and states review 1 had no such row (previously-rated-PASS: no). No item rated PASS in review 1 is now FAIL. No regression.
3. Monotonicity: F_2 (1) > 0 but F_2 < F_1 (5), so the halt condition (F_2 >= F_1) does not hold.
4. F_2 is not 0, so not PASS.
5. 0 < F_2 < F_1: CYCLE-2-REQUIRED.
