# D-0020 — evidence

## Test execution

```
$ uv run pytest tests/cli/eval/test_schema_id_rejection.py -v
============================== 20 passed in 0.21s ==============================

$ uv run pytest tests/cli/eval/ -q
============================== 319 passed in 0.91s ==============================
```

Baseline before T01.23: `299 passed` (post-T01.22). Delta: `+20`,
matching the 20 cases authored in this task. No prior tests
regressed.

Full per-case run log is captured in `evidence/T01.23/run.md`.

## Acceptance-criteria → test mapping

| T01.23 AC bullet | Test ID(s) |
|---|---|
| File `tests/cli/eval/test_schema_id_rejection.py` exists. | (file present at the documented path) |
| Tests for **schema-violation rejection**. | `test_schema_violation_raises_schema_error_at_validate_manifest`, `test_schema_violation_unknown_top_level_key_is_rejected`, `test_schema_violation_cli_describe_exits_two`, `test_schema_violation_cli_list_exits_two` |
| Tests for **unsafe id rejection**. | `test_unsafe_id_rejected_by_validate_eval_id` (× 6 parametrized), `test_unsafe_id_rejected_by_suite_loader_before_capability_resolution`, `test_unsafe_id_cli_describe_exits_two` |
| **Parameterize expansion validated post-expansion** (safe + unsafe). | `test_parameterize_safe_expansion_produces_dot_index_ids` (safe), `test_parameterize_unsafe_expansion_is_rejected_post_expansion` (unsafe) |
| **Pre-flight ordering** (no FS writes before rejection). | `test_no_fs_write_when_schema_rejected`, `test_no_fs_write_when_unsafe_id_rejected`, `test_no_fs_write_when_cli_describe_rejects` |
| `uv run pytest tests/cli/eval/test_schema_id_rejection.py -v` exits 0 with ≥ 4 passing tests. | 20 passed in 0.21s. |
| Tests assert **process exit code 2** on schema-violation and unsafe-id rejection paths. | `test_schema_violation_cli_describe_exits_two`, `test_schema_violation_cli_list_exits_two`, `test_unsafe_id_cli_describe_exits_two`, `test_no_fs_write_when_cli_describe_rejects`, `test_every_rejection_exit_code_is_two` (× 3). |
| Test docstrings **cross-link FR-SCH1, FR-SCH2, NFR-SEC1 by ID**. | Every test has a `Cross-links:` line in its docstring (e.g. `Cross-links: FR-SCH1 (T01.04), TEST-001 (T01.23)`). Module-level docstring documents the full cross-link map. |
| `artifacts/D-0020/spec.md` documents the test matrix. | This deliverable's `spec.md` includes the full matrix table per AC bullet. |

## Manifest / fixture inventory

No new fixtures created. Reused:

- `tests/cli/eval/fixtures/missing_name_suite.yaml` (T01.04)
- `tests/cli/eval/fixtures/unknown_top_level_suite.yaml` (T01.04)
- `tests/cli/eval/fixtures/invalid_eval_entry_suite.yaml` (T01.04)
- `tests/cli/eval/fixtures/valid_suite.yaml` (T01.02 / T01.04)

## STRICT-tier verification

Per T01.23 tier (STRICT) and sub-agent delegation = Recommended:

- All 20 cases pass on direct `uv run pytest` execution.
- Full eval suite passes (`319 passed`) — zero regressions.
- Spec.md documents the four-bullet AC test matrix with one-to-one
  mapping to test IDs (above).
- Notes.md records the mocking + snapshot strategies and the
  intentional reuse-vs-duplication trade with `test_path_traversal.py`.
- Cross-link IDs (FR-SCH1, FR-SCH2, NFR-SEC1, COMP-002) are present
  in module + per-test docstrings.

## Inputs verified from prior tasks

- `validate_manifest` (T01.04 / D-0004) — schema rejection raises `SchemaError`.
- `validate_eval_id` (T01.05 / D-0005) — FR-SCH2 regex enforced.
- `SuiteLoader.load` (T01.07 / D-0006) — five-stage gate chain with
  static + post-expansion id re-check.
- `SUITE_LOADER_ERROR_EXIT_CODE` (T01.07) — aggregate exit constant
  exposed for CLI binding.
- `eval describe` / `eval list` CLI commands (T01.21 / T01.22) — both
  raise typed errors → exit `2` with class name on stderr.
