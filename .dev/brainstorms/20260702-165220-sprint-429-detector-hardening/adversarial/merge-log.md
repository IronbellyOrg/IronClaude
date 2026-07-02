# Merge Log

## Metadata
- Base: Variant A (opus:architect) · Executor: merge (inline) · Changes applied: 7 · Status: success
- Merged output: `adversarial/merged-output.md` → copied to `merged-requirements.md`
- Date: 2026-07-02

## Changes applied
| # | Change | Status | Provenance tag |
|---|---|---|---|
| 1 | Two-axis sizing verdict (§2) | applied | Base + Variant 2 |
| 2 | "CHANGES WE ARE NOT MAKING" ledger, 9 items (§5) | applied | Variant 2 |
| 3 | R1 inline/substring + OQ1 no-nested-parse + F5 unreachability (§4/§6.4) | applied | Variant 2 |
| 4 | ~12-row detection-contract table (§6.2) | applied | Variant 3 (row 8 reconciled w/ INV-001) |
| 5 | FP fixture + per-row model + 4 parity tests (§6.1-6.3) | applied | Variant 3 |
| 6 | FP residual / C5-load-bearing / sufficiency trace (§4 R4, §7, §9) | applied | invariant-probe |
| 7 | Back-compat by construction (§4 R3) | applied | Base (architect) |

## Post-merge validation
- Structural integrity: ✅ Pass (H1→H2→H3 consistent, no orphaned subsections)
- Internal references: Total 6 (C1-C8, SC1-SC6, OQ1-OQ5, INV-00x); Resolved 6; Broken 0
- Contradiction re-scan: 0 new contradictions introduced

## Summary
- Planned 7 / Applied 7 / Failed 0 / Skipped 0. Convergence 0.90 (threshold 0.75). Status: success.
