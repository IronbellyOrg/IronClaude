# D-0018 — evidence

## Acceptance criteria → test coverage

| AC bullet | Test(s) |
|---|---|
| Command exits 0 with at least one suite present. | `test_cli_list_prints_name_version_eval_count` |
| Command exits 0 with zero suites present (empty directory). | `test_cli_list_exits_zero_on_empty_directory`, `test_cli_list_exits_zero_with_default_suites_dir`, `test_cli_list_json_empty_directory_returns_empty_array` |
| `--json` emits a JSON array with `{name, version, eval_count}` entries. | `test_cli_list_json_emits_array_of_summaries`, `test_list_payload_shape` |
| Output is deterministic for a given suite directory (sorted by filename). | `test_cli_list_json_is_deterministic_across_invocations`, `test_cli_list_output_is_sorted_by_filename`, `test_discover_returns_sorted_yaml_files` |
| `artifacts/D-0018/spec.md` records the output schema. | `artifacts/D-0018/spec.md` (this deliverable). |

## Unit-level coverage

| Helper | Test(s) |
|---|---|
| `discover_suite_manifests` (missing dir → `[]`) | `test_discover_returns_empty_for_missing_directory` |
| `discover_suite_manifests` (filters non-YAML) | `test_discover_returns_empty_for_directory_with_no_yaml`, `test_discover_returns_sorted_yaml_files` |
| `summarize_suites` (post-expansion count) | `test_summarize_suites_returns_post_expansion_eval_count` |
| `summarize_suites` (static-only manifest) | `test_summarize_suites_handles_static_only_manifest` |
| `summarize_suites` (sort order) | `test_summarize_suites_preserves_filename_order` |
| `summarize_suites` (empty) | `test_summarize_suites_returns_empty_for_empty_directory` |
| `render_list_text` (empty) | `test_render_list_text_empty_directory_message` |
| `render_list_text` (populated, plural toggle) | `test_render_list_text_lists_each_summary` |

## Failure-path coverage

| Failure | Test |
|---|---|
| Schema violation surfaces exit 2 + `SchemaError` on stderr | `test_cli_list_exits_two_on_schema_violation` |
| Eval-id / nested validation surfaces exit 2 | `test_cli_list_exits_two_on_invalid_eval_id` |

## Command log

```
$ uv run pytest tests/cli/eval/test_list.py -v
============================== 19 passed in 0.27s ==============================

$ uv run pytest tests/cli/eval/ -q
============================= 274 passed in 0.64s ==============================

$ uv run superclaude eval list
superclaude eval list:
  (no suites found)
$ echo $?
0

$ uv run superclaude eval list --json
[]
$ echo $?
0

$ uv run superclaude eval list --suites-dir tests/cli/eval/fixtures
eval list: SchemaError: Manifest schema validation failed: tests/cli/eval/fixtures/invalid_eval_entry_suite.yaml
  - $.evals[0]: 'title' is a required property
  - $.evals[0].id: 'lowercase-bad' does not match '^[A-Z][A-Za-z0-9]*([0-9]+(\\.[0-9]+)?)?$'
$ echo $?
2
```

The exit-2 case demonstrates that `eval list` fails closed when a
schema-violating manifest is in scope — the same gate chain that
protects `eval run` is enforced for the listing surface too.
