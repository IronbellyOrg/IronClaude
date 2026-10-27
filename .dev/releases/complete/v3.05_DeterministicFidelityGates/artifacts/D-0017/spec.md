# D-0017: DeviationRegistry Extension with source_layer and Stable IDs

## Overview

Extended `DeviationRegistry` in `convergence.py` with:
- `source_layer` field (`"structural"` | `"semantic"`) on every finding
- Stable ID computation from `(dimension, rule_id, spec_location, mismatch_type)` via SHA-256 truncated to 16 hex chars
- Cross-run comparison matching by stable ID
- FIXED status transition when finding not reproduced in subsequent run

## Implementation

### Stable ID Computation
- Function: `compute_stable_id(dimension, rule_id, spec_location, mismatch_type) -> str`
- Algorithm: `sha256(f"{dimension}:{rule_id}:{spec_location}:{mismatch_type}")[:16]`
- Collision-free on test corpus (8 distinct inputs verified)

### source_layer Tracking
- Each finding in the registry dict carries `source_layer: "structural" | "semantic"`
- Set during `merge_findings()` based on which list the finding came from
- Used by `get_structural_high_count()` and `get_semantic_high_count()`

### Cross-Run Comparison
- `merge_findings()` matches by stable ID:
  - Existing finding: updates `last_seen_run`, sets status `ACTIVE`
  - New finding: creates entry with `first_seen_run = run_number`
  - Missing finding: transitions status from `ACTIVE` to `FIXED`

## Verification

```
uv run pytest tests/roadmap/test_convergence.py -v -k "registry"
```

All tests pass: `TestRegistryStableIDs` (6 tests), `TestRegistryPersistence` (3 tests).
