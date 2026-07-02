# Refactoring Plan

## Overview
- Base: Variant A (opus:architect). Incorporated: B (refactorer), C (qa), invariant-probe.
- Planned changes: 7 · Rejected: 2 · Overall risk: Low (additive synthesis into strongest base).
- Review: `--interactive` → auto-approved (documented; no destructive edits, pure spec synthesis).

## Planned changes
| # | Source | Into base section | Approach | Risk |
|---|---|---|---|---|
| 1 | B — sizing (NARROW, 2 hunks) | §2 | merge with A's blast-radius framing → two-axis verdict | Low |
| 2 | B — "CHANGES NOT MAKING" (9 items) | §5 (new) | insert as anti-over-engineering ledger | Low |
| 3 | B — inline/substring/OQ1 + timeout unreachability | §4 R1/R4, §5#8, §6.4 F5 | insert | Low |
| 4 | C — ~12-row contract table | §6.2 | insert as centerpiece; row 8 reconciled with INV-001 | Low |
| 5 | C — FP fixture + per-row model + parity tests | §6.1, §6.2, §6.3 | insert | Low |
| 6 | invariant-probe — INV-001/004/005 | §4 R4, §7, §9 AC1/AC2 | insert FP residual, C5-load-bearing, sufficiency trace | Low |
| 7 | A — back-compat by construction | §4 R3 | preserve as formal guarantee | Low |

## Changes NOT being made (base approach superior)
- Rejected C's implicit "assume Shape-2 single-account mirrors Shape-1 silently" in favor of B+C
  reconciliation (explicit SYNTHESIZED breakpoint fixture) — transparency over silent assumption.
- Rejected any variant text that implied touching sibling detectors or the policy — all three
  actually respected C3, so nothing to strip; recorded for provenance.

## Risk summary
All changes are additive spec synthesis. No contradictions introduced (post-merge re-scan clean).
The only substantive engineering risk surfaced anywhere is the INV-001 FP residual, which the merged
spec documents and bounds rather than hides.
