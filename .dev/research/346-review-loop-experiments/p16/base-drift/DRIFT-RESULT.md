# Drift check result (2 fresh replicates of Stage 2 arm 3, run 2026-11-10 afternoon)

Tokens counted by PROMPT path in the short launch message (the harness's own matcher expects pasted text), each message id once.

| run | R1 | V1 | R2 | loop A | audit 1 | audit 2 | blocking (aud1/aud2) | loop end |
|---|---|---|---|---|---|---|---|---|
| a3d-r1 | 24,200 | 9,655 | 18,047 | 51,902 | 43,051 | 46,648 | 1 / 0 | PASS at R2 |
| a3d-r2 | 34,085 | 6,782 | 20,342 | 61,209 | 52,987 | 37,497 | 1 / 0 | PASS at R2 |
| p11 baseline mean (n=6) | 50,576 | 14,255 | 29,993 | 100,424 | 69,044 | - | 1.50 per audit | - |

Fresh loop mean 56,556 = 0.56 x the stored A_BASE; fresh R1 mean 29,143 = 0.58 x; fresh blocking 0.50 per audit (4 audits) vs 1.50.
Conclusion: the stored Stage 2 baseline is stale in BOTH cost and quality. Every R_LOOP and BLK comparison against it is biased in favour of later designs. n=2 is too small to set a new baseline; extend to n=6.
