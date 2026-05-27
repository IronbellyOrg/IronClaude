# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | guard_conditions | Unknown flag keys must be rejected consistently across show, set, unset, and validation paths. | ADDRESSED | HIGH | All variants require unknown-key rejection or validation failure. |
| INV-002 | interaction_effects | Environment overrides, if supported, can change behavior without persisted state. | ADDRESSED | MEDIUM | X-001 records the disagreement; merged requirement makes env support optional and read-only if included. |
| INV-003 | collection_boundaries | Registry validation must handle zero flags, one flag, and duplicate keys. | ADDRESSED | MEDIUM | Seed brief and variants require duplicate-key validation; merged requirements add empty/duplicate registry test coverage. |

## Summary

- **Total findings**: 3
- **ADDRESSED**: 3
- **UNADDRESSED**: 0
  - HIGH: 0
  - MEDIUM: 0
  - LOW: 0
