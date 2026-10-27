# Merge Coordination Plan — v3.1 Anti-Instinct Gate

**Sprint**: v3.1_Anti-instincts__
**Task**: T01.01
**Date**: 2026-03-20

---

## Current State of `gates.py`

The `WIRING_GATE` is imported from `src/superclaude/cli/audit/wiring_gate.py` and inserted into `ALL_GATES` at position after `spec-fidelity`:

```python
ALL_GATES = [
    ("extract", EXTRACT_GATE),
    ("generate-A", GENERATE_A_GATE),
    ("generate-B", GENERATE_B_GATE),
    ("diff", DIFF_GATE),
    ("debate", DEBATE_GATE),
    ("score", SCORE_GATE),
    ("merge", MERGE_GATE),
    ("test-strategy", TEST_STRATEGY_GATE),
    ("spec-fidelity", SPEC_FIDELITY_GATE),
    ("wiring-verification", WIRING_GATE),
    ("deviation-analysis", DEVIATION_ANALYSIS_GATE),
    ("remediate", REMEDIATE_GATE),
    ("certify", CERTIFY_GATE),
]
```

## Insertion Strategy: Additive-Only

The `ANTI_INSTINCT_GATE` will be inserted between `merge` and `test-strategy` in Phase 2. This is **additive-only**:

1. New semantic check functions are added (no existing functions modified).
2. New `ANTI_INSTINCT_GATE = GateCriteria(...)` constant is added after existing constants.
3. `ALL_GATES` list gains one new entry at index 7 (between `merge` at 6 and `test-strategy` at current 7).

## Conflict Risk Assessment

- **No conflict with WIRING_GATE**: The wiring gate is defined in a separate file (`audit/wiring_gate.py`) and imported. No changes to that gate or import.
- **No conflict with existing semantic checks**: All new functions use unique names prefixed with `_no_undischarged_`, `_integration_contracts_`, `_fingerprint_coverage_`.
- **`gate_passed()` signature unchanged**: Per NFR-009, no modifications to the gate evaluation interface.

## Phase 1 Scope

Phase 1 creates the four detection modules as standalone libraries. No modifications to `gates.py` in Phase 1. Gate definition is Phase 2 work (T02.01).
