# D-0052 — Evidence

## Test execution

Command:

```bash
uv run pytest tests/cli/eval/test_run_summary.py -v
```

Result: **22 passed in 0.16s** (full transcript at
`.dev/releases/current/cliEval/evidence/T03.09/test-output.txt`).

| Test                                                              | Acceptance bullet covered                                                                                                                |
|-------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| `test_run_summary_has_required_fields`                            | "Class `RunSummary` exposes the 11 fields listed in DM-004"                                                                              |
| `test_run_counts_has_required_sub_fields`                         | "...with nested `counts` containing the 5 sub-fields"                                                                                    |
| `test_run_totals_has_required_sub_fields`                         | DM-012 totals sub-structure shape                                                                                                        |
| `test_run_summary_is_frozen` / `test_run_counts_is_frozen`        | Frozen-dataclass mutation refusal                                                                                                        |
| `test_run_summary_defaults`                                       | Tail defaults (`evals=()`, `artifacts={}`)                                                                                               |
| `test_run_summary_artifacts_default_is_independent_per_instance`  | `default_factory=dict` hands each instance its own mapping                                                                               |
| `test_run_summary_accepts_consistent_counts`                      | Happy-path construction with non-trivial kept/skipped split                                                                              |
| `test_run_summary_rejects_mismatched_counts_when_flag_true`       | "Constructor validates `counts.kept_plus_skipped_equals_n_prime` boolean and asserts the equation holds" — direction A (flag claims True) |
| `test_run_summary_rejects_mismatched_counts_when_flag_false`      | Same AC — direction B (flag claims False but math holds)                                                                                 |
| `test_run_summary_accepts_consistent_false_flag`                  | Partial-summary path (SIGINT) where flag mirrors a False reality                                                                          |
| `test_run_summary_to_dict_field_order_matches_dm004`              | "`to_dict()` returns a deterministic JSON-serializable mapping" — top-level ordering                                                      |
| `test_run_summary_to_dict_counts_sub_field_order`                 | Same AC — counts sub-field ordering                                                                                                       |
| `test_run_summary_to_dict_totals_sub_field_order`                 | Same AC — totals sub-field ordering                                                                                                       |
| `test_run_summary_to_dict_is_json_serialisable`                   | Same AC — `json.dumps(..., sort_keys=True)` round-trip                                                                                    |
| `test_run_summary_to_dict_unwraps_nested_outcomes`                | Reporter receives plain dicts in `evals`                                                                                                  |
| `test_run_summary_to_dict_artifacts_is_independent_of_source`     | Returned mapping is shallow-copied                                                                                                        |
| `test_run_summary_deterministic_equality`                         | `@dataclass`-generated `__eq__` is structural                                                                                             |
| `test_run_summary_unequal_when_field_differs`                     | Equality fails for each differing head field                                                                                              |
| `test_run_counts_to_dict_is_json_serialisable`                    | DM-012 counts sub-object round-trips through `json.dumps`                                                                                |
| `test_run_totals_to_dict_is_json_serialisable`                    | DM-012 totals sub-object round-trips through `json.dumps`                                                                                |
| `test_run_summary_reexported_from_package`                        | Consumers import from `superclaude.cli.eval`, not the private `models` module                                                            |

## Acceptance criteria → evidence pointers

| AC bullet (T03.09)                                                                                                                | Evidence                                                                                                                                                                                  |
|-----------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Class `RunSummary` exposes the 11 fields listed in DM-004 with nested `counts` containing the 5 sub-fields.                       | `test_run_summary_has_required_fields` (len == 11) + `test_run_counts_has_required_sub_fields` (len == 5).                                                                                |
| `to_dict()` returns a deterministic JSON-serializable mapping.                                                                    | `test_run_summary_to_dict_field_order_matches_dm004` + `test_run_summary_to_dict_is_json_serialisable` (round-trips through `json.dumps(..., sort_keys=True)`).                            |
| `RunSummary` constructor validates `counts.kept_plus_skipped_equals_n_prime` boolean and asserts the equation holds.              | `test_run_summary_rejects_mismatched_counts_when_flag_true` + `test_run_summary_rejects_mismatched_counts_when_flag_false`.                                                                |
| `TASKLIST_ROOT/artifacts/D-0052/spec.md` records the contract.                                                                    | `.dev/releases/current/cliEval/artifacts/D-0052/spec.md`.                                                                                                                                  |
