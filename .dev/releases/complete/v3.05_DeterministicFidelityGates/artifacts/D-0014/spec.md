# D-0014: Gates, CLI Options, and NFRs Checkers (T02.03)

## Gates Checker (`check_gates`)

Machine keys:
- `frontmatter_field_missing` (HIGH) — Required frontmatter field not covered
- `step_param_missing` (MEDIUM) — Step(...) parameter missing
- `ordering_violated` (MEDIUM) — Gate/step ordering constraint violated
- `semantic_check_missing` (MEDIUM) — Named semantic check not mapped

Extraction: Regex for frontmatter fields, Step() params, ordering numbers, semantic check names.

## CLI Options Checker (`check_cli`)

Machine keys:
- `mode_uncovered` (MEDIUM) — Config mode or CLI option not covered
- `default_mismatch` (MEDIUM) — Default value differs between spec and roadmap

Extraction: `Literal[...]` values, backtick-quoted options, `default=` patterns.

## NFRs Checker (`check_nfrs`)

Machine keys:
- `threshold_contradicted` (HIGH) — Numeric threshold contradicted or missing
- `security_missing` (HIGH) — Security primitive not addressed
- `dep_direction_violated` (HIGH) — Dependency direction reversed
- `coverage_mismatch` (MEDIUM) — Coverage threshold lower in roadmap
- `dep_rule_missing` (MEDIUM) — Dependency rule not addressed

Extraction: Thresholds via `extract_thresholds()`, security keyword set, dependency direction regex, coverage patterns.

## Verification

- `uv run pytest tests/roadmap/test_structural_checkers.py -v -k "gates or cli or nfrs"` — 12/12 PASS
- All 3 checkers share no mutable state
- All findings include dimension, rule_id, severity, spec_quote, roadmap_quote, location
