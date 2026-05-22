# T01.23 evidence — execution log

Date: 2026-05-20
Task: T01.23 — Author TEST-001 schema and ID rejection pytest module
Deliverable: D-0020

## Commands

```
$ uv run pytest tests/cli/eval/test_schema_id_rejection.py -v
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0
plugins: superclaude-4.2.0, benchmark-5.2.3, cov-7.1.0
collecting ... collected 20 items

tests/cli/eval/test_schema_id_rejection.py::test_schema_violation_raises_schema_error_at_validate_manifest PASSED [  5%]
tests/cli/eval/test_schema_id_rejection.py::test_schema_violation_unknown_top_level_key_is_rejected PASSED [ 10%]
tests/cli/eval/test_schema_id_rejection.py::test_schema_violation_cli_describe_exits_two PASSED [ 15%]
tests/cli/eval/test_schema_id_rejection.py::test_schema_violation_cli_list_exits_two PASSED [ 20%]
tests/cli/eval/test_schema_id_rejection.py::test_unsafe_id_rejected_by_validate_eval_id[../home] PASSED [ 25%]
tests/cli/eval/test_schema_id_rejection.py::test_unsafe_id_rejected_by_validate_eval_id[/etc] PASSED [ 30%]
tests/cli/eval/test_schema_id_rejection.py::test_unsafe_id_rejected_by_validate_eval_id[..] PASSED [ 35%]
tests/cli/eval/test_schema_id_rejection.py::test_unsafe_id_rejected_by_validate_eval_id[] PASSED [ 40%]
tests/cli/eval/test_schema_id_rejection.py::test_unsafe_id_rejected_by_validate_eval_id[1bad] PASSED [ 45%]
tests/cli/eval/test_schema_id_rejection.py::test_unsafe_id_rejected_by_validate_eval_id[{{prefix}}] PASSED [ 50%]
tests/cli/eval/test_schema_id_rejection.py::test_unsafe_id_rejected_by_suite_loader_before_capability_resolution PASSED [ 55%]
tests/cli/eval/test_schema_id_rejection.py::test_unsafe_id_cli_describe_exits_two PASSED [ 60%]
tests/cli/eval/test_schema_id_rejection.py::test_parameterize_safe_expansion_produces_dot_index_ids PASSED [ 65%]
tests/cli/eval/test_schema_id_rejection.py::test_parameterize_unsafe_expansion_is_rejected_post_expansion PASSED [ 70%]
tests/cli/eval/test_schema_id_rejection.py::test_no_fs_write_when_schema_rejected PASSED [ 75%]
tests/cli/eval/test_schema_id_rejection.py::test_no_fs_write_when_unsafe_id_rejected PASSED [ 80%]
tests/cli/eval/test_schema_id_rejection.py::test_no_fs_write_when_cli_describe_rejects PASSED [ 85%]
tests/cli/eval/test_schema_id_rejection.py::test_every_rejection_exit_code_is_two[2_0] PASSED [ 90%]
tests/cli/eval/test_schema_id_rejection.py::test_every_rejection_exit_code_is_two[2_1] PASSED [ 95%]
tests/cli/eval/test_schema_id_rejection.py::test_every_rejection_exit_code_is_two[2_2] PASSED [100%]

============================== 20 passed in 0.21s ==============================

$ uv run pytest tests/cli/eval/ -q
============================== 319 passed in 0.91s ==============================
```

Baseline before T01.23: 299 passing tests. Delta: +20 (matches the 20
cases authored in this task). No prior tests regressed.

## Test inventory (20 cases)

### AC bullet 1 — schema-violation rejection (4 cases)
- `test_schema_violation_raises_schema_error_at_validate_manifest`
- `test_schema_violation_unknown_top_level_key_is_rejected`
- `test_schema_violation_cli_describe_exits_two`
- `test_schema_violation_cli_list_exits_two`

### AC bullet 2 — unsafe-id rejection (8 cases incl. 6 parametrized)
- `test_unsafe_id_rejected_by_validate_eval_id[../home]`
- `test_unsafe_id_rejected_by_validate_eval_id[/etc]`
- `test_unsafe_id_rejected_by_validate_eval_id[..]`
- `test_unsafe_id_rejected_by_validate_eval_id[]`
- `test_unsafe_id_rejected_by_validate_eval_id[1bad]`
- `test_unsafe_id_rejected_by_validate_eval_id[{{prefix}}]`
- `test_unsafe_id_rejected_by_suite_loader_before_capability_resolution`
- `test_unsafe_id_cli_describe_exits_two`

### AC bullet 3 — parameterize expansion (2 cases)
- `test_parameterize_safe_expansion_produces_dot_index_ids` (safe)
- `test_parameterize_unsafe_expansion_is_rejected_post_expansion` (unsafe)

### AC bullet 4 — pre-flight ordering (3 cases)
- `test_no_fs_write_when_schema_rejected`
- `test_no_fs_write_when_unsafe_id_rejected`
- `test_no_fs_write_when_cli_describe_rejects`

### Cross-cutting (3 cases via parametrize)
- `test_every_rejection_exit_code_is_two[2_0]`
- `test_every_rejection_exit_code_is_two[2_1]`
- `test_every_rejection_exit_code_is_two[2_2]`

## Implementation surface

- New file: `tests/cli/eval/test_schema_id_rejection.py` (20 cases, 0
  new fixtures — reuses T01.04 / T01.07 negative fixtures).
- New artifacts: `artifacts/D-0020/{spec,notes,evidence}.md`.
- No source-tree changes beyond the test module — every gate exercised
  here was already shipped by T01.04 (FR-SCH1), T01.05 (FR-SCH2),
  T01.07 (COMP-002), and T01.21 / T01.22 (`eval list` / `eval describe`).

## AC → test mapping

| T01.23 AC bullet | Tests |
|---|---|
| Tests for schema-violation rejection. | 4 tests (validate_manifest + CLI surfaces). |
| Tests for unsafe id rejection. | 8 tests (validate_eval_id × 6 parametrized + SuiteLoader ordering + CLI). |
| Parameterize expansion validated post-expansion (safe + unsafe). | 2 tests. |
| Pre-flight ordering (no FS writes before rejection). | 3 tests (function + CLI surfaces). |
| ≥ 4 passing tests. | 20 passed. |
| Process exit code 2 on schema-violation and unsafe-id paths. | 5 dedicated exit-2 assertions + parametrized 3-constant invariant test. |
| Cross-link FR-SCH1, FR-SCH2, NFR-SEC1 in docstrings. | Module-level docstring + every test's `Cross-links:` line. |
| `artifacts/D-0020/spec.md` documents the test matrix. | Done. |
