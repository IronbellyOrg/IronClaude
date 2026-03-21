# D-0023: Prompt Budget Enforcement (FR-4.2)

## Summary

Enhanced prompt budget enforcement with section-heading truncation markers and truncation priority ordering.

## Implementation

- **Truncation marker format**: `[TRUNCATED: N bytes omitted from '<heading>']` — includes section heading per FR-4.2.
- **`_truncate_to_budget()`** updated with `heading` parameter.
- **Template ValueError**: Template exceeding 5% allocation (1,536 bytes) raises `ValueError`.
- **Truncation priority**: Prior summary (cut first) → Structural context (secondary) → Spec/roadmap sections (last resort).
- **SC-6 assert**: `assert len(prompt) <= 30720` precedes every LLM call.

## Acceptance Criteria Verification

| Criterion | Status |
|-----------|--------|
| Truncation markers include section heading | PASS |
| Template exceeding 5% raises ValueError | PASS |
| Truncation priority: prior → structural → spec/roadmap | PASS |
| assert <= 30720 before every LLM call | PASS |

## Test Evidence

```
uv run pytest tests/roadmap/test_semantic_layer.py -v -k "budget or truncat"
```
All budget enforcement tests pass.
