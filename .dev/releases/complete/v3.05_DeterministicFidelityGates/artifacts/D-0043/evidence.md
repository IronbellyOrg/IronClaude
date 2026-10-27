# D-0043: SC-1 — Deterministic Structural Findings Evidence

## Proof of Determinism

5 tests verify SC-1 at both field-level and serialized-output level:

| Test | What it verifies |
|------|-----------------|
| `test_sequential_determinism` | Two runs produce identical Finding fields (id, severity, dimension, rule_id, location, spec_quote, roadmap_quote, stable_id) |
| `test_serialized_output_identical` | JSON serialization is byte-identical across runs |
| `test_individual_checker_determinism` | Each of the 5 checkers independently produces identical output |
| `test_parallel_execution_determinism` | Parallel execution produces same findings as sequential |
| `test_no_shared_mutable_state` | Checkers share no mutable state (NFR-4) |

## Test Results
```
tests/roadmap/test_structural_checkers.py::TestDeterminism::test_sequential_determinism PASSED
tests/roadmap/test_structural_checkers.py::TestDeterminism::test_serialized_output_identical PASSED
tests/roadmap/test_structural_checkers.py::TestDeterminism::test_individual_checker_determinism PASSED
tests/roadmap/test_structural_checkers.py::TestDeterminism::test_parallel_execution_determinism PASSED
tests/roadmap/test_structural_checkers.py::TestDeterminism::test_no_shared_mutable_state PASSED
```

## Implementation Guarantees
- `run_all_checkers()` sorts findings by `(dimension, rule_id, location)` (line 680)
- `compute_stable_id()` uses SHA-256 of structural properties for deterministic IDs
- No LLM calls in structural checkers
- No shared mutable state between checkers
