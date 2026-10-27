# D-0019 — evidence

## Test execution

```
$ uv run pytest tests/cli/eval/test_describe.py -v
============================== 25 passed in 0.33s ==============================

$ uv run pytest tests/cli/eval/ -q
============================= 299 passed in 0.81s ==============================
```

The full eval test suite expanded from 274 → 299 passing (25 new
`test_describe.py` tests). No prior tests regressed.

## CLI smoke tests

```
$ cp tests/cli/eval/fixtures/valid_suite.yaml /tmp/reference.yaml

$ uv run superclaude eval describe --suite reference --suites-dir /tmp
name: reference
version: '1.0'
description: Reference v1 manifest exercising every DM-011 field including parameterize.
defaults:
  per_eval_timeout_sec: 120
  per_eval_memory_mb: 512
  capture_tty: true
  keep_home_on_success: false
required_binaries:
  ...
evals:
- id: E1
  title: ...
- id: E2.1   ← post-parameterize expansion verified
- id: E2.2
- id: E2.3
$ echo $?
0

$ uv run superclaude eval describe --suite reference --eval E1 --suites-dir /tmp
id: E1
title: auggie-first sticky lifecycle — set then clear
category: hook-lifecycle
...
$ echo $?
0

$ uv run superclaude eval describe --suite ghost --suites-dir /tmp
eval describe: SuiteNotFound: no manifest matched --suite 'ghost' in /tmp
$ echo $?
2
```

## Acceptance-criteria coverage

| AC bullet (T01.22) | Test(s) |
|---|---|
| `superclaude eval describe --suite <name>` prints validated post-parameterize manifest content. | `test_cli_describe_prints_yaml_envelope`, `test_cli_describe_json_emits_valid_json` |
| `--eval <id>` filters to a single eval; missing id exits 2 with `EvalNotFound`. | `test_cli_describe_filters_to_single_eval_yaml`, `test_cli_describe_filters_to_post_expansion_id`, `test_cli_describe_exit2_on_missing_eval`, `test_describe_suite_raises_eval_not_found` |
| Validation runs before any print operation; invalid manifest exits 2. | `test_cli_describe_exit2_on_schema_violation`, `test_cli_describe_exit2_on_invalid_eval_id`, `test_cli_describe_validation_runs_before_any_stdout` |
| `artifacts/D-0019/spec.md` records flag semantics. | `spec.md` co-located in this directory; covers flag table, exit codes, resolution rules, output schema, validation order, and acceptance-criteria → implementation map. |

## Cross-cut verification

| Cross-cut | Evidence |
|---|---|
| FR-SCH1 schema rejection → exit 2. | `test_cli_describe_exit2_on_schema_violation` asserts `result.exit_code == SUITE_LOADER_ERROR_EXIT_CODE` and `"SchemaError" in result.stderr`. |
| FR-SCH2 unsafe id rejection → exit 2. | `test_cli_describe_exit2_on_invalid_eval_id` asserts `SUITE_LOADER_ERROR_EXIT_CODE` on the `invalid_eval_entry_suite.yaml` fixture. |
| Validation precedes print. | `test_cli_describe_validation_runs_before_any_stdout` asserts `result.stdout == ""` on rejection paths. |
| Determinism (YAML + JSON). | `test_render_describe_json_is_deterministic`, `test_cli_describe_yaml_is_deterministic`. |
| Three-rule `--suite` resolution. | `test_resolve_suite_manifest_accepts_direct_path`, `test_resolve_suite_manifest_finds_by_filename_stem`, `test_resolve_suite_manifest_finds_by_name_field`, `test_resolve_suite_manifest_skips_broken_neighbours`, `test_resolve_suite_manifest_raises_when_missing`. |

## Module exports

`commands.py` exposes the new surface for downstream callers and tests:

- `eval_describe` — Click handler registered as `eval_group.command("describe")`.
- `describe_suite(suite, *, suites_dir, eval_id=None, loader=None)` —
  function the handler delegates to.
- `resolve_suite_manifest(suite, suites_dir)` — three-rule lookup.
- `_evalspec_to_dict(spec)` / `_parsed_suite_to_dict(parsed)` — pure
  projections (private but importable for tests).
- `render_describe_yaml(payload)` / `render_describe_json(payload)` —
  deterministic renderers.
- `SuiteNotFound`, `EvalNotFound` — typed exceptions mapped to
  `SUITE_NOT_FOUND_EXIT_CODE` / `EVAL_NOT_FOUND_EXIT_CODE` (both `2`).
