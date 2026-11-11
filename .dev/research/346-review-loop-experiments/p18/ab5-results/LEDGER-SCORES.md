# ab5 ledger scores (n=6 per variant, Sonnet blind scorers, 44-defect ledger v1)

| arm | resid blocking /20 | weighted resid | fixed /44 | fixed per run | primary-lane tokens | parallel tokens | loop total |
|---|---|---|---|---|---|---|---|
| fresh baseline | 17.3 | 94.8 | 2.8 | 1,1,1,4,5,5 | 53.6k | 0 | 53.6k |
| ab4 | 14.3 | 84.8 | 6.3 | 3,5,6,6,8,10 | 106.5k | 0 | 106.5k |
| PN1 | 10.0 | 63.0 | 15.7 | 10,14,15,17,18,20 | ~106k | ~291k | ~408k |
| ab5 panel (ab4 + PN1 panel) | 12.7 | 79.0 | 8.5 | 6,6,7,9,11,12 | 179k (+13.6k ADJ) | 129k | 308k |
| ab5 full (ab4 + all of PN1) | 8.8 | 61.8 | 15.5 | 5,12,14,17,22,23 | 259k (+13.7k ADJ) | 176k | 435k |

Permutation tests (weighted residual / fixed): panel vs baseline p=0.003; panel vs ab4 p=0.175 (n.s.); panel vs PN1 p=0.017 (worse);
full vs baseline p=0.005; full vs ab4 p=0.016 (better); full vs PN1 p=0.93 (tie on quality).
Introduced defects per spec: panel 0.8, full 0.5, ab4 1.2, PN1 0.8, baseline 1.2.
The harness "DROP" verdicts in RESULTS-process.md use the old audit-count rule; the ledger scores above supersede them.
