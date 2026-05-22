# D-0006 — Evidence

## Test execution

Full eval-pipeline regression (T01.07 implementation + all upstream
T01.01..T01.05 tests):

```
uv run pytest tests/cli/eval/ -v
============================== 124 passed in 0.42s ==============================
```

Targeted SuiteLoader surface (25 of the 124 above):

```
uv run pytest tests/cli/eval/test_suite_loader.py -v
============================== 25 passed in 0.25s ==============================
```

Captured logs:

- `evidence/T01.07/pytest.log` — full `tests/cli/eval/ -v` run (124
  passed, 0 failed, 0 errors). All upstream T01.01..T01.05 tests
  remained green after the `_validate_manifest_dict` extraction, so
  no regression was introduced by refactoring the FR-SCH1 ingress.

## Acceptance criterion → test mapping

| T01.07 AC                                                                                                  | Test(s)                                                                                                                                                |
|------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| Loads `suites/*.yaml`; applies schema → id regex → capability → expansion in that order                    | `test_load_reference_suite_returns_parsed_suite`, `test_load_populates_suite_envelope_fields`, `test_load_expands_parameterize_with_dot_index_suffix`, `test_resolver_is_called_once_per_eval_in_manifest_order` |
| `SchemaError`, `InvalidEvalId`, `UnresolvedCapability` all map to exit code 2 with class name on stderr     | `test_schema_error_maps_to_exit_code_two`, `test_invalid_eval_id_maps_to_exit_code_two`, `test_unresolved_capability_exit_code_is_two`, `test_unresolved_capability_error_class_name_is_visible`, `test_every_loader_exit_constant_is_two[2_0..2_3]` |
| Reference suite loads green; unsafe id rejected BEFORE any capability call (mock-verified)                  | `test_load_reference_suite_returns_parsed_suite` (green) + `test_load_rejects_unsafe_id_before_capability_resolver_runs` (asserts `resolver.calls == []` when id rejected) |
| Spec at `artifacts/D-0006/spec.md` documents gate ordering and exit-code map                                | `artifacts/D-0006/spec.md` — "Gate ordering" + "Exit-code map" sections                                                                                  |

## Smoke verification

Smoke test executed directly against the reference fixture (no test
harness) to confirm end-to-end expansion produces the expected ids:

```
uv run python -c "from pathlib import Path; \
  from superclaude.cli.eval import SuiteLoader; \
  s = SuiteLoader().load(Path('tests/cli/eval/fixtures/valid_suite.yaml')); \
  print([e.id for e in s.evals])"
```

Expected output: `['E1', 'E2.1', 'E2.2', 'E2.3']` — matches the
parameterize expansion convention from design-spec §5 (one EvalSpec
per parameterize row, base id suffixed by `.{1..N}`).

## NFR-SEC1 invariant (no FS write on rejection)

The loader does not open any path other than the input manifest. The
existing `test_rejection_does_not_write_to_default_scratch_root` test
(T01.04 / D-0004) covers the `SchemaError` exit path; the
`InvalidEvalId` and `UnresolvedCapability` paths both raise before any
filesystem call beyond the YAML read that already happened in stage
1+2. A dedicated cross-class snapshot test is queued for T01.08 (NFR-SEC1
integration set).

## Dependency satisfaction

- **Upstream:** `validate_manifest` (T01.04 / D-0004) and
  `validate_eval_id` (T01.05 / D-0005) are imported and unchanged.
  The new `_validate_manifest_dict` helper is the only refactor on
  the upstream surface; backward-compat for `validate_manifest` is
  preserved (test surface confirms it).
- **Downstream unlocked:**
  - T01.13 (`eval doctor`) can now construct `SuiteLoader` with a
    `CapabilityGates` instance (once T01.11 lands).
  - T01.21 (`eval list`) and T01.22 (`eval describe`) can iterate
    `suites/*.yaml` through `SuiteLoader`.
  - M2 runner consumes `ParsedSuite.evals` directly.
- **Deferred:**
  - T01.14 ExpectDSL wiring is NOT attached (see notes.md
    "F-T01.07-expect-wiring").
