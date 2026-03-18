# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | No shared utility for semantic checks to extract typed frontmatter values from raw string | ADDRESSED | HIGH | Resolved: private `_extract_frontmatter_values()` helper in `audit/wiring_gate.py` |
| INV-002 | state_variables | WiringReport.clean does not respect mode; consumers outside gate path will over-report | ADDRESSED | MEDIUM | Resolved: renamed to `.clean`, added `blocking_for_mode()` method |
| INV-003 | state_variables | `_build_steps()` and `_get_all_step_ids()` are already desynchronized; insertion point ambiguous | ADDRESSED | HIGH | Resolved: desync is intentional; insert in both after spec-fidelity, before remediate |
| INV-004 | state_variables | Resume with stale rollout_mode artifact bypasses intended enforcement | ADDRESSED | MEDIUM | Resolved: deterministic step re-runs produce mode-correct output; documented in resume section |
| INV-005 | guard_conditions | Semantic checks need typed value extraction but no shared parser exists | ADDRESSED | HIGH | Resolved: merged with INV-001 |
| INV-006 | guard_conditions | `resolve_gate_mode()` forces BLOCKING at release scope, defeating shadow mode | ADDRESSED | HIGH | Resolved: mode-aware `blocking_findings` computation survives BLOCKING; `grace_period` note added |
| INV-007 | guard_conditions | Pre-activation checklist has no implementation contract | ADDRESSED | MEDIUM | Resolved: runtime check in `run_wiring_analysis()`, raises on shadow, warns on soft/full |
| INV-008 | count_divergence | Three-way invariant requires single-source computation guarantee | ADDRESSED | HIGH | Resolved: both projections derive from same `list[WiringFinding]` data |
| INV-009 | count_divergence | Info severity never blocking even in full mode — not stated | ADDRESSED | MEDIUM | Resolved: explicit documentation that info findings are non-blocking in all modes |
| INV-010 | collection_boundaries | `files_analyzed=0` passes gate silently | ADDRESSED | MEDIUM | Resolved: `files_skipped` field added; pre-activation checklist catches zero-file scope |
| INV-011 | collection_boundaries | Empty whitelist file vs absent whitelist file boundary unhandled | ADDRESSED | LOW | Resolved: whitelist loader handles None/empty YAML gracefully |
| INV-012 | interaction_effects | `retry_limit=0` semantics ambiguous | ADDRESSED | HIGH | Resolved: confirmed `max_attempts = retry_limit + 1` from executor code |
| INV-013 | interaction_effects | Wiring gate detecting unwired DEVIATION_ANALYSIS_GATE creates circular dependency | ADDRESSED | MEDIUM | Resolved: acceptable; wiring gate detects current state, not future state |
| INV-014 | interaction_effects | Nested severity_summary YAML block collides with flat key extraction | ADDRESSED | HIGH | Resolved: flat frontmatter adopted (no nested blocks) |

## Summary

- **Total findings**: 14
- **ADDRESSED**: 14
- **UNADDRESSED**: 0
  - HIGH: 0
  - MEDIUM: 0
  - LOW: 0
