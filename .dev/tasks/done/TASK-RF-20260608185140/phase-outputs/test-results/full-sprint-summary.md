# Full Sprint Suite — Validation Summary

- **Command:** `uv run pytest tests/sprint/ -q`
- **Result:** **1172 passed, 0 failed**, 20 warnings (deprecation only).
- **Base was 1163** → +9 new tests, all passing:
  - FIX-1 (3): `test_primary_argv_includes_index_path_positional`, `test_primary_argv_parses_through_click_command`, `test_base_argv_without_positional_is_rejected`
  - FIX-2 (1): `test_recovered_report_never_injects_gate_tokens`
  - FIX-3 (1): `test_merge_partial_when_declared_not_landed_in_canonical`
  - FIX-4 (4): `test_recover_reevaluates_stale_blocked_to_unknown`, `test_recover_reevaluates_body_only_stale_verdict`, `test_recover_restamp_is_idempotent_on_second_run`, `test_recover_default_off_preserves_fail_even_with_evidence`
- **Ruff:** `ruff check src/superclaude/cli/sprint/ tests/sprint/` → All checks passed. `ruff format` reformatted the 4 edited files (cosmetic), then `ruff format --check` → idempotent (118 already formatted). New-tests subset re-run after format: 82 passed.
- **Out of scope (untouched):** the pre-existing `lint-architecture` failure in `recommend.md` is outside the scoped paths and was not touched.
