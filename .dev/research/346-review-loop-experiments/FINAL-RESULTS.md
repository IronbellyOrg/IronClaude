# #346 review-loop experiments: final results (2026-11-10)

Uniform rescoring: every audit scored with central/score_themes.blocking_findings; per-run mean blockers compared by a two-sided permutation test (20,000 shuffles) against the FRESH baseline (Sonnet) or the Haiku baseline (Haiku rows). Tokens are output tokens, each message id once, matched by prompt text or prompt path.

| arm | runs | audits | blocking/audit | sd | p vs ref | loop tokens (mean) | vs fresh baseline |
|---|---|---|---|---|---|---|---|
| stored baseline (Stage 2 a3, earlier) | 6 | 12 | 1.50 | 0.67 | 0.48 | 100,424 | 1.87x |
| FRESH baseline (same design, now) | 6 | 12 | 1.17 | 0.72 | - | 53,623 | 1.00x |
| ab1 k=3 union + verify (replayed, clean) | 6 | 12 | 0.83 | 0.58 | 0.38 | 122,146 | 2.28x |
| ab2 verify gate, k=1 | 6 | 12 | 1.33 | 1.07 | 0.84 | ~74,152 (recount 43,152 + ~31k baseline R1; CORRECTED 2026-11-10, was 105,354) | 1.38x |
| ab3 final whole-document gate | 6 | 12 | 1.25 | 0.75 | 1.00 | ~122,552 (recount 91,552 + ~31k baseline R1; CORRECTED, was 167,382, a copy of the Haiku baseline figure) | 2.29x |
| PN1 panel + merge + ledger | 6 | 12 | 1.25 | 1.06 | 1.00 | ~408,316 (complete runs r4-r6; CORRECTED, 66,240 withdrawn) | 7.61x |
| PN2 mechanical lint | 6 | 12 | 1.33 | 0.98 | 0.83 | 47,033 | 0.88x |
| ab4 lint + k=2 (AC sweep) + clean verify | 6 | 12 | 0.92 | 0.79 | 0.67 | 106,519 | 1.99x |
| HAIKU baseline | 6 | 12 | 1.75 | 0.97 | - | 167,382 | - |
| HAIKU ab1 | 4 | 8 | 1.62 | 0.74 | 0.82 | 419,037 | - |
| HAIKU ab2 | 4 | 8 | 1.88 | 0.64 | 0.83 | 235,803 | - |
| HAIKU ab3 | 4 | 8 | 1.25 | 1.04 | 0.47 | 319,005 | - |
| HAIKU ab4 | 4 | 8 | 1.38 | 1.06 | 0.56 | ~254,000 | - |

Findings: (1) no design differs from the fresh baseline beyond noise (all p >= 0.38); (2) the cost of the unchanged design fell to 0.53x of the stored baseline (real drift; R1 31k vs 51k), so earlier cost ratios were biased in favour of the variants; (3) the stored-vs-fresh quality gap (1.50 vs 1.17) is itself noise (p 0.48); (4) per-audit sd ~0.75 means n=6 can only detect very large effects: a 30% reduction needs about 35-40 runs per arm with this instrument.
Jev E1-E5 and capture-recapture: NO-GO-OFFLINE / BLOCKED at their pre-registered offline gates (see central/MATRIX.md).

**Update 2026-11-10 (defect-ledger rescoring):** the audit-based scores above cannot separate the designs (a frozen audit samples about 7% of the blocking defects present). Rescoring all 70 final specs against a validated ledger of 44 spec defects (see `p17/LEDGER-RESULTS.md`) shows PN1, ab3 and ab4 reduce residual defects significantly (p 0.003, 0.022, 0.027), ab1 marginally (0.08), ab2 and PN2 not at all, and no design makes the loop converge. Token figures for ab2, ab3 and PN1 in the table above were corrected in the same update.
