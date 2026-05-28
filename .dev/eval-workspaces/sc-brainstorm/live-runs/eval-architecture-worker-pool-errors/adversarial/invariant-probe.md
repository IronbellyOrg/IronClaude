# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | Every work item has a stable identity through retry, quarantine, and replay | ADDRESSED | HIGH | Promoted as A-002 and incorporated into FR1/FR2 |
| INV-002 | guard_conditions | Non-idempotent tasks are not auto-replayed | ADDRESSED | HIGH | Security and DevOps proposals require approval and replay eligibility |
| INV-003 | interaction_effects | Rollback policy and partial success reporting do not conflict | ADDRESSED | MEDIUM | Architect proposal requires configured atomic groups; QA requires mixed-batch reporting |
| INV-004 | collection_boundaries | Empty, single-task, and mixed-outcome batches are represented distinctly | ADDRESSED | MEDIUM | QA contract tests require mixed success/failure and terminal status coverage |
| INV-005 | sufficiency_challenge | Envelope alone is sufficient to prevent retry storms | ADDRESSED | HIGH | Performance proposal adds bounded retry, jitter, and backpressure; merged requirements do not rely on envelope alone |

## Summary

- **Total findings**: 5
- **ADDRESSED**: 5
- **UNADDRESSED**: 0
  - HIGH: 0
  - MEDIUM: 0
  - LOW: 0
