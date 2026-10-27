# Invariant Probe Results

## Round 2.5 -- Fault-Finder Analysis

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | `ctx.get_parameter_source("agents")` breaks when called programmatically (no Click context) | ADDRESSED (Round 3: ResumableConfig with source tag) | HIGH | Click context dependency; tests/scripts that construct config directly would crash or misclassify |
| INV-002 | state_variables | Step ID reconciliation undefined when spec changes add/reorder steps between runs | UNADDRESSED | HIGH | State file step IDs from old step list may not match current `_build_steps` output |
| INV-003 | state_variables | Non-atomic state file writes risk corruption on crash (SIGKILL, OOM) | UNADDRESSED | MEDIUM | No write-then-rename atomicity or checksum validation mentioned |
| INV-004 | guard_conditions | Warn-and-confirm assumes interactive terminal; CI/cron/piped contexts have no TTY | ADDRESSED (Round 3: --on-conflict flag with ask/override/fail) | HIGH | Automated resume workflows would hang or crash without TTY |
| INV-005 | guard_conditions | Output file existence not verified when trusting state file claims | UNADDRESSED | MEDIUM | State marks step as passed but file may be deleted between runs |
| INV-006 | count_divergence | Parallel group partial completion undefined; high-water mark fence-post error | ADDRESSED (Round 3: -1 init, atomic groups, group_progress dict) | HIGH | List[Step] groups: does index 0 mean group 0 completed or no groups completed? |
| INV-007 | count_divergence | Dirty-output propagation may miss transitive dependencies on wrong iteration order | UNADDRESSED | MEDIUM | Single forward pass may miss B->C invalidation if B not yet processed when C evaluated |
| INV-008 | collection_boundaries | Silent agent restore doesn't validate agents still exist/are available | UNADDRESSED | MEDIUM | State records `haiku` but agent removed between runs; pipeline fails at execution with confusing error |
| INV-009 | collection_boundaries | Empty steps list from `_build_steps` passes silently as success | UNADDRESSED | LOW | Malformed spec could produce zero steps; pipeline reports success having done nothing |
| INV-010 | interaction_effects | Depth and agents are coupled but treated independently; quick depth + full agent list = inconsistent config | ADDRESSED (Round 3: differential treatment + WARNING for orphaned assignments) | HIGH | `--depth quick --agents opus,haiku` may reference steps that don't exist under quick depth |
| INV-011 | interaction_effects | High-water mark and per-step dirty flags encode potentially contradictory completion semantics | UNADDRESSED | MEDIUM | Step marked completed at high-water but dirty via dependency invalidation; state file loses dirty flag on crash |

## Summary

- **Total findings**: 11
- **ADDRESSED**: 4 (all HIGH, resolved in Round 3)
- **UNADDRESSED**: 7
  - HIGH: 1 (INV-002: step ID reconciliation)
  - MEDIUM: 5 (INV-003, INV-005, INV-007, INV-008, INV-011)
  - LOW: 1 (INV-009)

**Note**: INV-002 (HIGH) remains unaddressed but is out-of-scope for the immediate resume fix -- it concerns spec modification between runs, which is a separate feature (spec-change detection). The existing `spec_hash` comparison provides partial mitigation.
