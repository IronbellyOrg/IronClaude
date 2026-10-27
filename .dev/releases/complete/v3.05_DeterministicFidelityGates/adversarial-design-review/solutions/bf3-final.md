# BF-3 Resolution: Split Tracking with Structural-Only Monotonic Enforcement

## Selected Solution

**Solution A** -- Track structural and semantic HIGH counts separately; enforce monotonic progress only on structural findings.

**Why**: The root cause is mixing deterministic (structural) and non-deterministic (semantic) signals into a single progress metric. Solution B (pin temperature=0) attempts to suppress non-determinism at the source but cannot guarantee it -- LLM APIs explicitly disclaim determinism even at temperature=0. Solution A eliminates the category of false regressions entirely by scoping monotonic enforcement to the layer that IS deterministic (structural), which is exactly how NFR-1 already scopes the determinism guarantee. Scored 8.80 vs 6.90 on weighted criteria (false regression prevention 40%, convergence guarantee 30%, implementation feasibility 30%).

## Architecture Design Change

### Sec 4.5 Convergence Algorithm Modification

The `execute_fidelity_with_convergence` function in `convergence.py` changes at step 6:

**Before** (current Sec 4.5 step 6):
```
6. Check monotonic progress:
   -> run_n+1.highs > run_n.highs? -> REGRESSION
      a. Spawn 3 parallel worktree agents (FR-8)
      ...
```

**After**:
```
6. Check monotonic progress (STRUCTURAL ONLY):
   -> run_n+1.structural_high_count > run_n.structural_high_count? -> REGRESSION
      a. Spawn 3 parallel worktree agents (FR-8)
      b-e. (unchanged)
   -> run_n+1.semantic_high_count > run_n.semantic_high_count?
      -> LOG WARNING (semantic fluctuation, not regression)
      -> Do NOT trigger FR-8 parallel validation
7. (unchanged: patch remediation if budget remaining)
```

**Gate evaluation** (step 5) remains unchanged:
```
5. Evaluate gate: active_high_count == 0?  (total: structural + semantic)
   -> YES: return PASS
```

This means semantic HIGHs still block the gate from passing. They just don't trigger the expensive 3-worktree regression detection flow when they fluctuate between runs.

### FR-7 Clarification

FR-7 acceptance criterion "Run 2 must have `high_count <= run_1.high_count` or trigger FR-8" is amended to:

> Run 2 must have `structural_high_count <= run_1.structural_high_count` or trigger FR-8. Semantic high count changes are logged but do not constitute regression.

### FR-8 Trigger Condition

FR-8 acceptance criterion "Regression detected when `current_run.high_count > previous_run.high_count`" is amended to:

> Regression detected when `current_run.structural_high_count > previous_run.structural_high_count`. Semantic high count increases are not regressions.

## Tracking Model

### Registry Schema Addition

Each finding in `deviation-registry.json` gains a `source_layer` field:

```json
{
  "findings": {
    "a1b2c3d4e5f67890": {
      "stable_id": "a1b2c3d4e5f67890",
      "source_layer": "structural",
      "severity": "HIGH",
      "dimension": "signatures",
      "rule_id": "phantom_id",
      "status": "ACTIVE"
    },
    "f8e7d6c5b4a39210": {
      "stable_id": "f8e7d6c5b4a39210",
      "source_layer": "semantic",
      "severity": "HIGH",
      "dimension": "gates",
      "rule_id": "",
      "status": "ACTIVE",
      "debate_verdict": "CONFIRM_HIGH"
    }
  }
}
```

Each run record in the registry gains split counts:

```json
{
  "runs": [
    {
      "run_number": 1,
      "timestamp": "2026-03-19T10:00:00Z",
      "structural_high_count": 3,
      "semantic_high_count": 1,
      "total_high_count": 4,
      "structural_count": 12,
      "semantic_count": 3
    }
  ]
}
```

### Source Layer Assignment

- Findings produced by `structural_checkers.py` (the 5 checker callables): `source_layer = "structural"`
- Findings produced by `semantic_layer.py` (residual LLM pass): `source_layer = "semantic"`
- The `merge_findings` method in `DeviationRegistry` accepts structural and semantic finding lists as separate parameters (it already does -- see Sec 4.4.2) and tags each with the appropriate `source_layer`

### Backward Compatibility

Registries created before this change (without `source_layer`) are handled by defaulting missing `source_layer` to `"structural"`. This is safe because pre-change registries contain only structural findings (the semantic layer and convergence engine are new in v3.05).

## Regression Detection Rules

### Regression IS triggered when:

1. `current_run.structural_high_count > previous_run.structural_high_count`
   - This indicates a deterministic regression: the structural checkers found MORE issues after remediation, which should be impossible if patches were correctly applied
   - Response: spawn 3 parallel worktree agents (FR-8), full validation flow

### Regression is NOT triggered when:

1. `current_run.semantic_high_count > previous_run.semantic_high_count` (but structural count is stable or decreasing)
   - This is expected LLM non-determinism
   - Response: log warning with counts, continue to remediation or gate evaluation
   - Log format: `"Semantic HIGH fluctuation: {prev} -> {curr} (delta: +{delta}). Not a regression."`

2. `current_run.total_high_count > previous_run.total_high_count` due solely to semantic increase
   - Same as above -- the total count increase is attributed to semantic noise
   - The convergence engine decomposes the total to determine which layer caused the increase

### Progress Logging Format

```
Run 1 -> Run 2 progress:
  Structural HIGHs: 3 -> 2 (monotonic: PASS)
  Semantic HIGHs:   1 -> 2 (fluctuation: LOGGED, not regression)
  Total HIGHs:      4 -> 4
  Gate: FAIL (4 active HIGHs remain)
```

## Validation

### How to verify false regressions are prevented

1. **Unit test -- structural regression triggers correctly**:
   - Create registry with run 1: `structural_high_count=3`
   - Simulate run 2: `structural_high_count=4`
   - Assert: `handle_regression()` IS called

2. **Unit test -- semantic fluctuation does NOT trigger regression**:
   - Create registry with run 1: `structural_high_count=3, semantic_high_count=1`
   - Simulate run 2: `structural_high_count=2, semantic_high_count=3`
   - Assert: `handle_regression()` is NOT called
   - Assert: warning log emitted with semantic fluctuation message

3. **Unit test -- gate still requires 0 total HIGHs**:
   - Create registry with `structural_high_count=0, semantic_high_count=1`
   - Assert: gate returns FAIL (not PASS)
   - This confirms semantic HIGHs are not ignored for the final gate, only for regression detection

4. **Integration test -- identical inputs, semantic variation**:
   - Run fidelity pipeline twice on same inputs
   - If semantic HIGH count differs between runs: confirm no regression was triggered
   - If structural HIGH count is identical between runs: confirm NFR-1 determinism holds

5. **Property test -- source_layer tagging correctness**:
   - Run `structural_checkers.run_all_checkers()`: all findings have `source_layer="structural"`
   - Run `semantic_layer.run_semantic_layer()`: all findings have `source_layer="semantic"`
   - No finding has `source_layer=""` or `source_layer=None`

### Implementation Checklist

- [ ] Add `source_layer: str` field to `Finding` dataclass in `models.py`
- [ ] Update `DeviationRegistry.merge_findings()` to tag `source_layer` on each finding
- [ ] Add `structural_high_count` and `semantic_high_count` to run metadata in registry
- [ ] Update `execute_fidelity_with_convergence()` step 6 to check only `structural_high_count`
- [ ] Add semantic fluctuation warning log
- [ ] Update progress log format to show split counts
- [ ] Add 5 validation tests (listed above)
- [ ] Update FR-7 and FR-8 acceptance criteria text in requirements spec
