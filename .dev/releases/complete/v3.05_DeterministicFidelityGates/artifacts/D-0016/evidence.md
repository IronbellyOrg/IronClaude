# D-0016: Determinism Proof — SC-1 (T02.05, Gate B)

## Test Results

All determinism tests pass:

1. **Sequential determinism**: Two runs on identical inputs produce byte-identical findings — PASS
2. **Serialized output identical**: JSON serialization of both runs compared — zero differences — PASS
3. **Individual checker determinism**: Each of 5 checkers individually deterministic — PASS
4. **Parallel execution determinism**: ThreadPoolExecutor(max_workers=5) produces same results as sequential — PASS
5. **No shared mutable state**: 3 consecutive runs per checker produce identical counts — PASS

## Evidence

```
uv run pytest tests/roadmap/test_structural_checkers.py::TestDeterminism -v
5/5 PASS
```

## SC-1 Certification

SC-1 is proven: identical inputs produce byte-identical findings across:
- Sequential runs
- Parallel runs (NFR-4)
- Multiple consecutive executions (no state accumulation)

Determinism is guaranteed by:
1. Pure functions — no randomness, no LLM calls
2. Sorted output — findings sorted by (dimension, rule_id, location)
3. Deterministic stable_id — SHA-256 hash of structural properties
4. No shared mutable state between checkers
