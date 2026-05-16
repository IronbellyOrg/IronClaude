# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | OutputMonitor `_last_read_pos` can be safely reset between tasks without losing in-flight events | UNADDRESSED → ADDRESSED (R3) | HIGH | P-01 proposal text on shared NDJSON file. Mitigated in R3 by mandatory unit test contract. |
| INV-002 | state_variables | `phase_started_at` populated correctly on per-task path via monitor.reset or TUI fallback | UNADDRESSED | MEDIUM | P-02 proposal admits dual-writer fallback. Accepted as follow-on cleanup. |
| INV-003 | guard_conditions | Rich Spinner renders correctly in `box=None` Table.add_row | ADDRESSED | LOW | Rich docs confirm Table accepts RenderableType cells; smoke test recommended in P-05. |
| INV-004 | count_divergence | `Phase.prompt_preview` bumped to `[:240]` does not break downstream consumers | UNADDRESSED | MEDIUM | P-03 proposal lacks downstream audit. Accepted: 15-min grep audit added to P-03 PR description. |
| INV-005 | collection_boundaries | `_seen_files` set handles post-reset edge case without skipping first event of a fresh task | UNADDRESSED → ADDRESSED (R3) | HIGH | Same evidence base as INV-001. Mitigated in R3 by same unit test contract. |
| INV-006 | interaction_effects | P-03 + P-07 + P-05 do not introduce rendering ordering conflicts | ADDRESSED | LOW | Distinct render-tree positions; no shared mutable state. |
| INV-007 | guard_conditions | Live's 2 Hz refresh does not infinite-loop with Spinner frame mutation | ADDRESSED | MEDIUM | Rich's documented design — Live triggers on its own clock, not render-tree mutation. |

## Summary

- **Total findings**: 7
- **ADDRESSED**: 5 (3 pre-R3 + 2 mitigated in R3)
- **UNADDRESSED**: 2
  - HIGH: 0 (both downgraded in R3)
  - MEDIUM: 2 (INV-002, INV-004 — both accepted with stated follow-on actions)
  - LOW: 0

**Convergence gate**: HIGH UNADDRESSED count = 0. Gate PASSED.

## Required Follow-On Actions (consolidated from R3 resolutions)

1. **For P-01 PR (mandatory)**: Add `tests/sprint/test_monitor_reset_between_tasks.py` with the 3-task event-count invariant test. Promote reset to a public method `OutputMonitor.reset_for_next_task()`. This mitigation absorbs INV-001 and INV-005.
2. **For P-03 PR (mandatory)**: 15-minute grep audit of `prompt_preview` downstream consumers before merge. Addresses INV-004.
3. **For follow-on cleanup (after P-01 lands)**: Reconcile the two writers of `phase_started_at` (monitor.reset vs TUI fallback) into a single owner. Addresses INV-002.
