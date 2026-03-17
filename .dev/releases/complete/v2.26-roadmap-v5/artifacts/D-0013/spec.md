# D-0013: 9 Semantic Check Functions — spec.md

**Task:** T02.04
**Roadmap Items:** R-024 through R-032
**Date:** 2026-03-16
**Status:** COMPLETE

---

## Functions Implemented

All 9 functions added to `src/superclaude/cli/roadmap/gates.py`, after existing semantic checks and before GateCriteria instances.

| Function | FR | Description |
|----------|----|-------------|
| `_certified_is_true` | FR-028 | `certified: true` in frontmatter |
| `_validation_complete_true` | FR-053 | `validation_complete: true` in frontmatter |
| `_no_ambiguous_deviations` | FR-026 | `ambiguous_deviations: 0` in frontmatter |
| `_routing_consistent_with_slip_count` | FR-056 | `len(valid routing tokens) == slip_count` |
| `_pre_approved_not_in_fix_roadmap` | FR-079 | `pre_approved_ids ∩ fix_roadmap_ids == ∅` (OQ-A Option B: frontmatter embedding) |
| `_slip_count_matches_routing` | FR-081 | Aliases `_routing_consistent_with_slip_count` |
| `_total_annotated_consistent` | FR-085 | `total_annotated == slip_count + pre_approved_count + ambiguous_deviations` |
| `_total_analyzed_consistent` | FR-086 | `total_analyzed == total_annotated + unclassified_count` |
| `_routing_ids_valid` | FR-074 | All routing_list tokens match `^DEV-\\d+$` |

## Fail-Closed Behavior

All functions return `False` for:
- Missing frontmatter
- Missing required field(s)
- Malformed/non-parseable values
- Semantic inconsistency (mismatch, overlap, etc.)

## OQ-A Resolution Applied

`_pre_approved_not_in_fix_roadmap()` uses **Option B (frontmatter embedding)**: reads `pre_approved_ids` and `fix_roadmap_ids` directly from frontmatter YAML fields. No `aux_inputs` field on `GateCriteria`.

## Test Results

- `uv run pytest tests/roadmap/test_gates_data.py -v` → **105 passed**
- All boundary inputs covered: valid, invalid, missing, malformed
