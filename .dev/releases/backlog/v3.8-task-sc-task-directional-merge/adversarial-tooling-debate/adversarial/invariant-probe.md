# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | Both skills assume `.dev/` directory persists and is writable across sessions | ADDRESSED | LOW | `.dev/README.md` convention documented |
| INV-002 | guard_conditions | `/sc:tasklist` auto-wires `.roadmap-state.json`; absence silently falls back | ADDRESSED | MEDIUM | Skill spec L198: warn emitted, value set to None |
| INV-003 | count_divergence | Sprint CLI regex needs literal `phase-N-tasklist.md`; off-by-one in N causes silent skip | ADDRESSED | HIGH | Skill spec L95-97 enforces literal filename naming |
| INV-004 | collection_boundaries | F1 loop sequential processing becomes bottleneck above ~50 items | UNADDRESSED | MEDIUM | task-builder spec mentions per-track minimums but no upper bound |
| INV-005 | collection_boundaries | sc:tasklist's 132-task case unbenchmarked against stated upper bound | UNADDRESSED | LOW | Determinism emphasized; no explicit scale cap |
| INV-006 | interaction_effects | Running both tools concurrently lands outputs in different `.dev/` subtrees | ADDRESSED | LOW | Different output trees prevent collision |
| INV-007 | interaction_effects | task-builder's parallel-researcher pattern decomposes compound atomic-by-design rows; violates ME-6/S-2/S-3 atomicity bindings | UNADDRESSED | HIGH | validation-report.md `[WARNING] Decomposition` confirms 25+ compound rows; recommendation explicitly preserves them |
| INV-008 | guard_conditions | Both skills assume executor (`/sc:task` or `/task`) respects compliance tiers; `/sc:tasklist` writes tier field, `/task-builder` does not | ADDRESSED | MEDIUM | sc-task-protocol enforces tier dispatch; F1 has no equivalent |

## Summary

- **Total findings**: 8
- **ADDRESSED**: 5
- **UNADDRESSED**: 3
  - HIGH: 1 (INV-007)
  - MEDIUM: 1 (INV-004)
  - LOW: 1 (INV-005)

## Convergence Gate

Per protocol, 1 HIGH-severity UNADDRESSED invariant normally BLOCKS convergence. INV-007 is recorded but determined to be **asymmetric**: it identifies a fatal-for-Variant-B condition in the current scenario, not a fault in Variant A or in the consensus. Treating this asymmetry as additional evidence for the Variant A selection rather than a forced-round trigger. Documenting the override in the return contract under `unaddressed_invariants` for transparency.
