# D-0015: Severity Rule Table Evidence (T02.04)

## Rule Coverage

Total rules: 19 (8 HIGH, 11 MEDIUM)

| # | Dimension | Machine Key | Severity |
|---|-----------|------------|----------|
| 1 | signatures | phantom_id | HIGH |
| 2 | signatures | function_missing | HIGH |
| 3 | signatures | param_arity_mismatch | MEDIUM |
| 4 | signatures | param_type_mismatch | MEDIUM |
| 5 | data_models | file_missing | HIGH |
| 6 | data_models | path_prefix_mismatch | HIGH |
| 7 | data_models | enum_uncovered | MEDIUM |
| 8 | data_models | field_missing | MEDIUM |
| 9 | gates | frontmatter_field_missing | HIGH |
| 10 | gates | step_param_missing | MEDIUM |
| 11 | gates | ordering_violated | MEDIUM |
| 12 | gates | semantic_check_missing | MEDIUM |
| 13 | cli | mode_uncovered | MEDIUM |
| 14 | cli | default_mismatch | MEDIUM |
| 15 | nfrs | threshold_contradicted | HIGH |
| 16 | nfrs | security_missing | HIGH |
| 17 | nfrs | dep_direction_violated | HIGH |
| 18 | nfrs | coverage_mismatch | MEDIUM |
| 19 | nfrs | dep_rule_missing | MEDIUM |

## Verification

- `get_severity()` returns correct severity for all 19 rules: PASS
- `get_severity("signatures", "unknown_key")` raises `KeyError`: PASS
- Rule table is extensible (dict addition works without checker changes): PASS
- `uv run pytest tests/roadmap/test_structural_checkers.py::TestSeverityRules -v` — 8/8 PASS
