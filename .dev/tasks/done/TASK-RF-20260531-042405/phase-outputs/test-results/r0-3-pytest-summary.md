# R0.3 Pytest + Arch-Lint Summary

**Phase:** 4 (R0.3 — `superclaude.contracts` SoT + arch-lint)
**Run date:** 2026-06-01
**Command:** `uv run pytest tests/roadmap/test_threshold_registry.py tests/contracts/ tests/roadmap/test_spec_parser.py tests/roadmap/test_models.py tests/roadmap/test_spec_structural_audit.py -v`
**Adjacent target:** `make lint-architecture` (Check 11 added in this phase)

## Overall result

- Pytest: **107 passed, 1 failed (pre-existing, NOT R0.3 regression), 10 skipped**
- Arch-lint: **PASS** (exit 0)

## R0.3 contract tests — all PASS

### `tests/roadmap/test_threshold_registry.py` (12 tests, Contract #5 + #8)

| Test | Result |
|---|---|
| `test_constant_defined_exactly_once_in_src[ID_PATTERNS]` | PASS |
| `test_constant_defined_exactly_once_in_src[CONVERGENCE_THRESHOLDS]` | PASS |
| `test_constant_defined_exactly_once_in_src[GATE_FIELD_NAMES]` | PASS |
| `test_r0_3_consumers_import_from_contracts[id_registry]` | PASS |
| `test_r0_3_consumers_import_from_contracts[spec_parser]` | PASS |
| `test_r0_3_consumers_import_from_contracts[gates]` | PASS |
| `test_arch_lint_passes_on_clean_repo` | PASS |
| `test_arch_lint_fails_on_duplicate` | PASS |
| `test_no_orphan_id_pattern_literals_in_cli` | PASS |
| `test_g_family_present_in_id_patterns` | PASS |
| `test_convergence_thresholds_shape_matches_build_request` | PASS |
| `test_gate_field_names_shape_matches_build_request` | PASS |

### `tests/contracts/test_arch_lint.py` (11 tests, walker unit coverage)

| Test | Result |
|---|---|
| `test_clean_file_yields_no_violations` | PASS |
| `test_name_rebind_violation_detected` | PASS |
| `test_literal_duplicate_violation_detected` | PASS |
| `test_allow_marker_suppresses_violation` | PASS |
| `test_canonical_file_is_skipped` | PASS |
| `test_violation_format_includes_canonical_pointer` | PASS |
| `test_check_paths_aggregates_across_files` | PASS |
| `test_main_returns_nonzero_on_violations` | PASS |
| `test_main_returns_zero_on_clean_scan` | PASS |
| `test_main_returns_two_on_missing_path` | PASS |
| `test_violation_dataclass_is_hashable` | PASS |

**5 new Contract #8 tests called out in Step 4.5:** `test_no_duplicate_id_patterns`, `test_no_duplicate_convergence_thresholds`, `test_no_duplicate_gate_field_names`, `test_consumers_import_from_contracts`, `test_arch_lint_fails_on_duplicate`. Equivalent coverage delivered as `test_constant_defined_exactly_once_in_src[ID_PATTERNS|CONVERGENCE_THRESHOLDS|GATE_FIELD_NAMES]` (parametrized), `test_r0_3_consumers_import_from_contracts` (parametrized), and `test_arch_lint_fails_on_duplicate` (direct match).

## Arch-lint result

```
=== Check 11: Contract Constant Anti-Duplication (Contract #5 + #8) ===
  ✅ [Check 11]: no contract-constant duplications

=== Summary ===
  Errors:   0
  Warnings: 5
  ✅ PASS — architecture policy compliant (5 warning(s))
```

`make lint-architecture` exit code 0. The 5 warnings are unrelated pre-existing
command-size warnings (Check 3) — not R0.3 regressions.

## Existing-test regression check

| Test file | Result |
|---|---|
| `tests/roadmap/test_spec_parser.py` | **all pass** (no regression from spec_parser.py migration) |
| `tests/roadmap/test_spec_structural_audit.py` | **all pass** |
| `tests/roadmap/test_models.py` | 1 pre-existing failure (`test_default_agents` — confirmed on clean baseline before R0.3 changes via `git stash`; CRITICAL=NO, R0.3-related=NO) |

## Contract #5 + #8 satisfaction assertion

**Contract #5 (no fail-open / `return True` stubs introduced):** R0.3 did NOT
add any `return True` stubs. Migrations in `id_registry.py:37`,
`spec_parser.py:324-330`, and `gates.py:398-407` are pure substitution of
literal values with imports — behavior preserved.

**Contract #8 (no duplicate cross-skill constants):** Verified by 3
parametrized AST-walk tests (`test_constant_defined_exactly_once_in_src`),
end-to-end CLI invocation (`test_arch_lint_passes_on_clean_repo`), AND
`make lint-architecture` Check 11. The arch-lint walker is the static
enforcement; the pytest suite is the CI gate.

## Pre-existing failure note

`tests/roadmap/test_models.py::TestRoadmapConfig::test_default_agents` —
expects `config.agents[1].model == "haiku"`, actual `"sonnet"`. Reproduced
on `git stash`-clean baseline (commit `665d34ca`) before any R0.3 edits.
This is a pre-existing test-config drift independent of R0.3 scope. Logged
to Phase 4 Findings; not a Contract gate regression.
