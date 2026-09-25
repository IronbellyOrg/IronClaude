# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | guard_conditions | Non-compliant task cannot become `complete` without a three-field Ruling | ADDRESSED | HIGH | X-002 merge: one-fix then HALT; operator Ruling required to complete non-compliant |
| INV-002 | state_variables | Resume uses first non-complete task; start-SHA scopes the diff | ADDRESSED | HIGH | All variants: ledger on disk; V1/V3 start-SHA stolen into merge |
| INV-003 | guard_conditions | Executor-authored Ruling on `extra` can launder drive-by files | ADDRESSED | HIGH | V3 R2 rejected V2 extra-ruling; merge: only operator-supplied Ruling completes non-compliant |
| INV-004 | sufficiency_challenge | One-fix pass alone does not start T{i+1} | ADDRESSED | HIGH | V1 R-032: second QA must be `compliant` or HALT. Merge keeps this. |
| INV-005 | collection_boundaries | Zero enumerable tasks / empty file / pitch-only | ADDRESSED | MEDIUM | All: STOP no-tasks. V3 E-NO-TASKS. |
| INV-006 | count_divergence | 20-task cap inclusive vs exclusive | ADDRESSED | LOW | Merge: no hard cap; warn at N≥20. No off-by-one STOP. |
| INV-007 | interaction_effects | Green extras + missing citations → `compliant` | ADDRESSED | HIGH | C-003 + V3 AC-009.5: extras never sole-gate; zero citations → cannot-verify |
| INV-008 | guard_conditions | `- [ ] auth` reaches Write before QA | ADDRESSED | HIGH | C-002 QUALIFY: verb+object or E-NO-AC before edit |
| INV-009 | sufficiency_challenge | MDTM detector “prevents /task overlap” without invoking /task | ADDRESSED | MEDIUM | Merge: no detector; Boundaries will-not invoke /task. Detector was untestable (V2 R2). |
| INV-010 | state_variables | Truncated ledger last line → double-implement | ADDRESSED | MEDIUM | Steal V3 E-LEDGER-CORRUPT / STOP don't guess |

## Summary

- **Total findings**: 10
- **ADDRESSED**: 10
- **UNADDRESSED**: 0
  - HIGH: 0
  - MEDIUM: 0
  - LOW: 0
