# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | `_make_finding` must accept `files_affected` for S2's routing to materialize — but `_make_finding` callers in `semantic_layer.py:514` are not currently part of the contract | ADDRESSED | HIGH | S2 refactored doc §1 explicitly requires updating both `_make_finding` and `semantic_layer.py:514`; debate transcript confirms |
| INV-002 | guard_conditions | After S1 removes URL-fragment phantoms, `prd_template.md` and `tdd_template.md` still fail — S1 alone cannot reach 0 HIGHs | ADDRESSED | HIGH | S1 refactored doc §"Expected impact" explicitly states "Will NOT alone reach 0 HIGHs"; S2 routing required |
| INV-003 | count_divergence | `MAX_CONVERGENCE_BUDGET=61` allows exactly 3 cycles with no regression-validation headroom; if Run 2 triggers regression validation (+15) the loop dies at Run 2 | ADDRESSED | MEDIUM | S4 debate reconciles the math; not load-bearing for current failure but flagged |
| INV-004 | collection_boundaries | If `check_nfrs` per-section iteration (S5) produces duplicate findings across sections that contain the same primitive, dedup must happen before stable_id allocation | ADDRESSED | MEDIUM | S5 refactored doc §"Risks/downsides" notes "Must ensure stable ordering by sorting on (heading_path, term) before emission" |
| INV-005 | interaction_effects | S2 routing all findings at the same roadmap file collapses the parallel ThreadPoolExecutor to 1 worker — risk of single-patch >30% | ADDRESSED | MEDIUM | S2 §5 documents this; mitigation deferred to Phase 2 (chunking) but `check_patch_diff_size` per-patch guard partially covers it |
| INV-006 | interaction_effects | S6 `MANUAL_TRIAGE` status must be treated as terminal by downstream consumers (`remediate.py:130`, `remediate_executor.py:554`); if any consumer treats it as ACTIVE the gate inverts | ADDRESSED | HIGH | S6 §3.4 explicitly enumerates downstream consumers needing update |

## Summary

- **Total findings**: 6
- **ADDRESSED**: 6
- **UNADDRESSED**: 0
  - HIGH: 0
  - MEDIUM: 0
  - LOW: 0

All HIGH-severity invariants identified during fault-finding were already addressed by the respective refactored solutions (this is the desired outcome — the per-solution adversarial agents did their job).
