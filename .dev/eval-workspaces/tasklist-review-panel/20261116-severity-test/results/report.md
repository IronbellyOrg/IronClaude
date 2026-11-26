# Severity-rule test: analysis

Runs scored: 40 (Z0 20, S 20); seed 20261122.

**Decision: DO NOT ADOPT: failed G3 found fraction**

| Arm | runs | found fraction | blocking fraction | wrong blockers/run | blocking rows/run | blocking precision | rows/run | median s |
|---|---|---|---|---|---|---|---|---|
| S | 20 | 0.249 | 0.117 | 1.00 | 1.30 | 0.23 (6/26) | 5.0 | 81.5 |
| Z0 | 20 | 0.325 | 0.075 | 1.50 | 1.70 | 0.12 (4/34) | 6.0 | 88.2 |

## Gates

- PASS G1 wrong blockers per run: S at most 0.70 x Z0: Z0 1.50, S 1.00, ratio 0.67
- PASS G2 real blocking matched (total over runs): S at least Z0: Z0 4, S 6
- FAIL G3 found fraction: S at least Z0 - 0.02: Z0 0.325, S 0.249
- PASS G4 pooled median time: S at most 1.10 x Z0: ratio 0.92 (Z0 88.2 s, S 81.5 s)

Wrong blockers per run, S minus Z0, 90% bootstrap interval (documents, then runs): [-1.30, 0.05]

## Per document

- S HO-2: found 0.180, wrong/run 1.20, blocking rows/run 1.60, matched 2/8
- S HO-3: found 0.167, wrong/run 1.20, blocking rows/run 2.00, matched 4/10
- S HX-1: found 0.600, wrong/run 0.20, blocking rows/run 0.20, matched 0/1
- S HX-3: found 0.050, wrong/run 1.40, blocking rows/run 1.40, matched 0/7
- Z0 HO-2: found 0.100, wrong/run 1.20, blocking rows/run 1.80, matched 3/9
- Z0 HO-3: found 0.133, wrong/run 2.80, blocking rows/run 2.80, matched 0/14
- Z0 HX-1: found 1.000, wrong/run 0.60, blocking rows/run 0.60, matched 0/3
- Z0 HX-3: found 0.067, wrong/run 1.40, blocking rows/run 1.60, matched 1/8
