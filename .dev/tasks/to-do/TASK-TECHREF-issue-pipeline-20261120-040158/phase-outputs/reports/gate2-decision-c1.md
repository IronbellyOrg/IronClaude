# Gate 2 decision after cycle 1

**Decision: CYCLE-2-REQUIRED**

Numbers used:
- F_1 = 9 (qa-synthesis-consolidated-findings.md: G2-1..G2-9; 0 synthetic).
- Verification reports valid (Status: Complete, `## Verdict:` line): qa-synthesis-verification-structural-c1.md PASS (0 BLOCKING); qa-synthesis-verification-content-c1.md FAIL (1 BLOCKING, N-1, new).
- F_2 = 1 + 0 synthetic = 1.

Rules in order: (1) F_1 not 0; (2) regression check: N-1 is new content (the 14.3 row was not rated in review 1; previously-rated-PASS: no), and no item previously rated PASS now FAILs: no regression; (3) monotonicity: F_2 = 1 < F_1 = 9, no halt; (4) F_2 not 0; (5) 0 < F_2 < F_1: CYCLE-2-REQUIRED.
