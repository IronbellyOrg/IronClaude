# D-0013: Signatures and Data Models Checkers (T02.02)

## Signatures Checker (`check_signatures`)

Machine keys:
- `phantom_id` (HIGH) — Roadmap references ID not in spec
- `function_missing` (HIGH) — Spec function not found in roadmap
- `param_arity_mismatch` (MEDIUM) — Parameter count differs
- `param_type_mismatch` (MEDIUM) — Parameter type annotation differs

Extraction: Uses `parse_document()` for requirement IDs and function signatures.
Comparison: Set difference for phantom IDs, name lookup for functions, param list comparison for arity/types.

## Data Models Checker (`check_data_models`)

Machine keys:
- `file_missing` (HIGH) — Spec file path not in roadmap
- `path_prefix_mismatch` (HIGH) — Same filename, different path prefix
- `enum_uncovered` (MEDIUM) — Literal enum value not in roadmap
- `field_missing` (MEDIUM) — Dataclass field not referenced in roadmap

Extraction: Uses `file_paths`, `literal_values`, and code block field analysis.
Comparison: Path set operations, case-insensitive text search for coverage.

## Verification

- `uv run pytest tests/roadmap/test_structural_checkers.py -v -k "signatures or data_models"` — 9/9 PASS
- Both checkers assign severity via `get_severity()` lookup only
- All findings include: dimension, rule_id, severity, spec_quote, roadmap_quote, location, stable_id
