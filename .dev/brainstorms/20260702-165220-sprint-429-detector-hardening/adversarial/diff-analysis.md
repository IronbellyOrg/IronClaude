# Diff Analysis: spec Comparison (blind)

## Metadata
- Generated: 2026-07-02
- Variants compared: 3 (blind: variant-A/B/C; identities architect/refactorer/qa revealed post-scoring)
- Mode: B (generated from seed-brief.md)
- Total material differences: 8 (all L2/L3); shared assumptions surfaced: 3

## Content Differences (C-NNN)

| # | Topic | A (architect) | B (refactorer) | C (qa) | Severity |
|---|---|---|---|---|---|
| C-001 | Sizing framing | SMALL (blast-radius) | NARROW (~3 lines) | SMALL-diff / MEDIUM-contract | Low — complementary; merged as two-axis |
| C-002 | Timeout branch (OQ5) | debt-ledger follow-up | proved unreachable + F5 test, byte-unchanged | out-of-scope, pinned as matrix row T1 | Medium — reconciled: all three harvested |
| C-003 | C1 disjunct impl | (unspecified) | INLINE, no helper (anti-ceremony) | (neutral) | Low — refactorer uncontested |
| C-004 | OQ1 nested escaping | raw substring ok | substring not regex/not JSON-path (crash-mode arg) | raw substring ok | Low — unanimous, B strongest rationale |
| C-005 | OQ2 Shape-2 single-account | assume mirrors Shape 1 | reject speculation | SYNTHESIZED breakpoint fixture | Medium — reconciled: documented breakpoint |
| C-006 | Back-compat proof | old_match ⊆ new_match by construction | fixture-pass argument | regression test | Low — A's formal proof adopted |
| C-007 | Contract-table detail | 11-row + per-row model | (defers to qa) | 11-row, xfail empty cells, per-row model | Low — qa centerpiece adopted |
| C-008 | Live/offline parity | notes shared inner | notes shared inner | 4 explicit parity tests incl. PASS_RECOVERED | Low — qa detail adopted |

## Contradictions (X-NNN)
None. No opposing claims; all three respect C1-C8. C-002/C-005 are emphasis differences, reconciled by harvesting.

## Unique Contributions (U-NNN)

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | architect | "coupling defect not regex defect" reframing; detection-contract as first-class boundary with 2 named consumers | High |
| U-002 | architect | back-compat by construction (old ⊆ new) | High |
| U-003 | refactorer | 9-item "CHANGES WE ARE NOT MAKING" ledger | High |
| U-004 | refactorer | timeout-branch unreachability proof + F5 test (net mandated edits = 2 hunks) | High |
| U-005 | qa | ~12-row detection-contract table, xfail empty cells | High |
| U-006 | qa | is_error:false FP fixture + per-row resolved_model assertion | High |
| U-007 | qa | 4 live/offline parity tests incl. PASS_RECOVERED intercept | Medium |

## Shared Assumptions (A-NNN)

| # | Assumption | Source agreement | Classification | Promoted |
|---|---|---|---|---|
| A-001 | `rate_limit_error` is present in BOTH real result bodies and is low-FP | all 3 key C1 on it | STATED | probed → INV-001 |
| A-002 | Detection alone suffices; consumer chain already correct/wired | all 3 assume recovery fires post-fix | UNSTATED | promoted → INV-005 sufficiency probe |
| A-003 | Text scan scoped to result-event body prevents transcript-wide FP | all 3 rely on C5 | UNSTATED | promoted → INV-004 (C5 load-bearing) |

## Summary
- Content differences: 8 (0 High, 3 Medium reconciled, 5 Low) · Contradictions: 0 · Unique: 7 · Shared assumptions: 3 (1 STATED, 2 UNSTATED→promoted)
- Highest-value items: U-001, U-003, U-004, U-005; promoted assumptions A-002/A-003 drove the two most valuable invariant-probe findings.
