# D-0011: ANTI_INSTINCT_GATE Definition

## Status: COMPLETE

## Changes Made

### `src/superclaude/cli/roadmap/gates.py` (additive-only)

1. **Three semantic check functions added:**
   - `_no_undischarged_obligations(content)` — asserts `undischarged_obligations == 0` in frontmatter
   - `_integration_contracts_covered(content)` — asserts `uncovered_contracts == 0` in frontmatter
   - `_fingerprint_coverage_check(content)` — asserts `fingerprint_coverage >= 0.7` in frontmatter

2. **`ANTI_INSTINCT_GATE` defined as `GateCriteria`:**
   - `required_frontmatter_fields`: `undischarged_obligations`, `uncovered_contracts`, `fingerprint_coverage`
   - `min_lines`: 10
   - `enforcement_tier`: "STRICT"
   - `semantic_checks`: all three functions above

3. **`ALL_GATES` updated:**
   - `("anti-instinct", ANTI_INSTINCT_GATE)` inserted between `("merge", MERGE_GATE)` and `("test-strategy", TEST_STRATEGY_GATE)`
   - ALL_GATES count: 13 → 14

### Test Fixture Updates

- `tests/roadmap/test_eval_gate_rejection.py`: Added `anti-instinct` passing frontmatter fixture
- `tests/roadmap/test_gates_data.py`: Updated gate count assertion from 13 to 14

## Verification

- `gate_passed()` signature unchanged: `gate_passed(output_file: Path, criteria: GateCriteria) -> tuple[bool, str | None]`
- `uv run pytest tests/roadmap/ -x` → 1247 passed, 0 failed
- Changes are additive-only — no existing gate definitions modified
