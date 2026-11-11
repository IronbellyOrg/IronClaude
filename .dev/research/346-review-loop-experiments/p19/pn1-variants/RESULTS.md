# PN1 variants: cost-matched (pn1m, 3 Sonnet + 3 Haiku) and doubled-Haiku (pn1d, 1 Sonnet + 6 Haiku), n=6 each, ledger v1, blind Sonnet scoring

| arm | resid blocking /20 | weighted resid | fixed /44 | fixed per run | introduced/spec | loop primary lane (Sonnet) | loop parallel lane (Haiku) |
|---|---|---|---|---|---|---|---|
| fresh baseline | 17.3 | 94.8 | 2.8 | 1,1,1,4,5,5 | 1.2 | 54k | 0 |
| ab4 | 14.3 | 84.8 | 6.3 | 3,5,6,6,8,10 | 1.2 | 107k | 0 |
| PN1 original (1S+3H) | 10.0 | 63.0 | 15.7 | 10,14,15,17,18,20 | 0.8 | see note | see note |
| ab5 full | 8.8 | 61.8 | 15.5 | 5,12,14,17,22,23 | 0.5 | 259k | 176k |
| **pn1m** (3S+3H) | 7.2 | 54.0 | 18.7 | 10,14,21,21,22,24 | 1.0 | 377k | 176k |
| **pn1d** (1S+6H) | 7.2 | 53.0 | **19.3** | 17,18,19,20,20,22 | 1.0 | 247k | 345k |

Permutation tests on fixed count: pn1m vs baseline p=0.003, vs ab4 p=0.004, vs PN1 +3.0 p=0.32, vs ab5 full +3.2 p=0.41. pn1d vs baseline p=0.003, vs ab4 p=0.003, vs PN1 +3.7 p=0.057, vs ab5 full +3.8 p=0.24. pn1d vs pn1m +0.7 p=0.84.
ROI model prediction (analysis in ../roi): 3S+3H +4.3 over PN1 (observed +3.0), 1S+6H +2.8 (observed +3.7). Both inside the 90% intervals.
Run-order check: fixed vs run index rho pn1m about -0.6 (n=6, ties ranked low), pn1d about +0.5 (mixed: pn1m shows a moderate decline with start order, pn1d none; with n=6 neither is conclusive).

Notes: (1) the PN1 harness requested a Fable adjudicator; it was run on Sonnet (owner rule), harness patched, logged in anomalies. The original PN1 b1 runs used Fable ADJ (about 11k tokens). (2) m1-r5 t1b-1's report lacked the findings-block heading and was dropped by the harness gate. (3) Reviewers in pn1m wrote scratch files outside their sandbox in two cases (self-reported, deleted). (4) Lane token figures for these arms come from the harness per-step log (loop only, audits excluded, Sonnet vs Haiku by model); the original PN1 row has no comparable log (its tokens were null) and its earlier 106k/291k lane figures came from a transcript matcher, so primary-lane comparisons with the original PN1 are indicative only. (5) pn1m was meant to match ab5 full's primary lane (259k) but landed at 377k because three Sonnet first-round reviewers also lengthen the revise and re-review steps.
