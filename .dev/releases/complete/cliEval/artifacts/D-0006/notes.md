# D-0006 — Implementation notes for `SuiteLoader`

## Sequencing decisions made during the task

### Why `_validate_manifest_dict` was extracted

The pre-existing `validate_manifest(path)` returned `list[EvalSpec]` and
threw away the suite envelope metadata (`name`, `version`,
`required_binaries`, etc.). `SuiteLoader.load` needs the envelope to
populate `ParsedSuite`. Two options were considered:

1. Have `SuiteLoader.load` call `validate_manifest()` and then re-read
   the YAML to grab the envelope.
2. Extract a helper `_validate_manifest_dict(path) -> Mapping` that
   returns the full manifest dict, and refactor `validate_manifest` to
   project through it.

Option 2 was chosen — re-reading the file would violate the
"single-ingress for FR-SCH1" property and create a second decode path
that could drift from the first. The refactor kept `validate_manifest`
public API unchanged (still returns `list[EvalSpec]`) so T01.04 tests
did not need modification.

### Why parameterize expansion uses `enumerate(..., start=1)`

The design-spec §5 expansion convention is `E2.1, E2.2, E2.3` for a
3-row parameterize block — 1-based, not 0-based. The schema regex
`^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$` accepts both, so the choice
is policy not capability. 1-based was picked because:

- It matches the way the design-spec examples are written.
- It matches the conventional human-readable expansion ("the first row
  of `E2`'s parameterize" → `E2.1`, not `E2.0`).
- The reporter output reads more naturally with 1-based indices.

### Why `_RecordingResolver` is a test-local stub

The test fixture `_RecordingResolver` (in `tests/cli/eval/test_suite_loader.py`)
deliberately does not inherit from `CapabilityResolver` and is not exported.
It exists for two reasons:

1. To prove the `@runtime_checkable` Protocol catches structural
   conformance (the `isinstance()` test would be circular if the stub
   inherited).
2. To record `(eval_id, required)` call tuples so the ordering
   assertion (`resolver.calls == []` when id rejected) can be made
   without resorting to `mock.MagicMock` introspection. A plain
   recording class is easier to read in failure output.

### Why the ordering test uses `monkeypatch` on `_validate_manifest_dict`

The FR-SCH2 schema regex pattern is identical to the runtime
`EVAL_ID_REGEX`, so no schema-valid manifest can carry an unsafe id —
the schema would reject it first. To prove the runtime guard catches
unsafe ids, the test patches `_validate_manifest_dict` to return a
dict containing `../home` and `1bad`, simulating "what if the schema
layer were bypassed?". This is the only realistic way to verify the
runtime gate-order property without authoring an intentionally
malicious schema fixture (which would be confusing and fragile).

## Things that were deliberately NOT done in this task

### No ExpectDSL field on `SuiteLoader`

T01.14 (COMP-010 ExpectDSL) is on the same dependency line as T01.07
in the task spec. The loader could plausibly grow an
`expect_dsl: ExpectDSL` field analogous to `capability_resolver`,
but:

- The schema already validates the `expects:` block structure.
- ExpectDSL routing is a M4 runtime concern, not a load-time concern.
- Wiring it now would force a placeholder `ExpectDSL` import path
  before T01.14 lands.

The `SuiteLoader` dataclass shape is forward-compatible: adding
`expect_dsl: ExpectDSL = field(default_factory=NoopExpectDSL)` later
is a non-breaking change.

### No persistent loader cache

`SuiteLoader.load()` is intentionally not cached — every call re-reads
and re-validates the manifest. Reasons:

- The harness is short-lived (one CLI invocation per command).
- Caching introduces a stale-read hazard: an attacker who can write
  to the manifest mid-run could otherwise bypass validation.
- The full load chain measured at 0.4ms per manifest in test runs,
  so there is no performance motivation.

### No partial-failure reporting

The first failed gate raises and short-circuits the chain. We
considered collecting all gate failures and surfacing them together
(like `SchemaError` does for jsonschema errors within a single
manifest), but:

- The gates are non-commutative: a schema failure can leave the
  manifest in a state where eval-id checks don't make sense (e.g.,
  `id` field missing entirely).
- Operator UX is clearer with one gate's failure than three.
- The reporter has access to the full `SuiteLoaderError` class
  hierarchy, so a future "verbose" mode could re-run downstream gates
  in lenient mode if needed.

## File-by-file change summary

| File                                                          | Change                                                                                     |
|---------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| `src/superclaude/cli/eval/loader.py`                          | Extracted `_validate_manifest_dict`. Added `UnresolvedCapability`, `CapabilityResolver`, `PermissiveCapabilityResolver`, `ParsedSuite`, `SuiteLoader`, exit-code constants, `SuiteLoaderError`. |
| `src/superclaude/cli/eval/__init__.py`                        | Re-exported the new SuiteLoader public surface symbols.                                    |
| `tests/cli/eval/test_suite_loader.py`                         | New file: 25 tests covering positive load, envelope projection, expansion, error classes, ordering. |
| `tests/cli/eval/fixtures/no_parameterize_suite.yaml`          | New fixture: schema-valid suite with two static-id evals (E1, D15), no parameterize.       |
| `.dev/releases/current/cliEval/artifacts/D-0006/spec.md`      | This task's spec (gate ordering + exit-code map + Protocol contract).                      |
| `.dev/releases/current/cliEval/artifacts/D-0006/notes.md`     | This file.                                                                                 |
| `.dev/releases/current/cliEval/artifacts/D-0006/evidence.md`  | Cross-link to `evidence/T01.07/pytest.log`.                                                |
| `.dev/releases/current/cliEval/evidence/T01.07/pytest.log`    | Captured `uv run pytest tests/cli/eval/ -v` output for the full regression run.            |

## Test surface summary (25 tests)

The full SuiteLoader test surface, ordered by acceptance-criterion
relevance:

- **Positive load + envelope:** `test_load_reference_suite_returns_parsed_suite`,
  `test_load_populates_suite_envelope_fields`, `test_load_accepts_str_path`.
- **Parameterize expansion:** `test_load_expands_parameterize_with_dot_index_suffix`,
  `test_static_id_evals_pass_through_unmodified`, `test_load_returns_eval_specs`.
- **SchemaError gate:** `test_load_raises_schema_error_for_missing_top_level_field`,
  `test_schema_error_maps_to_exit_code_two`.
- **InvalidEvalId gate + ordering:**
  `test_load_raises_invalid_eval_id_when_schema_layer_is_bypassed`,
  `test_load_rejects_unsafe_id_before_capability_resolver_runs`,
  `test_invalid_eval_id_maps_to_exit_code_two`,
  `test_load_rejects_post_expansion_unsafe_id`.
- **UnresolvedCapability gate:**
  `test_load_raises_unresolved_capability`,
  `test_unresolved_capability_exit_code_is_two`,
  `test_unresolved_capability_error_class_name_is_visible`.
- **Resolver contract:**
  `test_resolver_is_called_once_per_eval_in_manifest_order`,
  `test_resolver_receives_requires_tuple_per_eval`,
  `test_default_resolver_is_permissive`,
  `test_permissive_resolver_returns_empty_iterable`,
  `test_capability_resolver_protocol_runtime_checkable`.
- **Aggregate exit-code contract:** `test_suite_loader_error_alias_covers_all_three_classes`,
  parametrised `test_every_loader_exit_constant_is_two[2_0..2_3]`.

## Open follow-ups (not blocking T01.07 close)

- **F-T01.07-expect-wiring:** Once T01.14 (COMP-010 ExpectDSL) lands,
  add `expect_dsl: ExpectDSL = field(default_factory=NoopExpectDSL)`
  to `SuiteLoader` and route per-`expects:` block validation through
  it at load time (currently the schema alone validates the block
  shape).
- **F-T01.07-stderr-wiring:** The AC mentions "error class name in
  stderr". The current loader raises typed errors but does not write
  to stderr — that wiring belongs to the CLI boundary (T01.13
  `eval doctor`). The error classes already expose `__class__.__name__`
  for the boundary code to render. Test:
  `test_unresolved_capability_error_class_name_is_visible` asserts
  the class name appears in `repr()`/`str()` output so the eventual
  CLI rendering is straightforward.
- **F-T01.07-no-fs-write-snapshot:** The T01.04 tests already cover
  the "no FS writes on rejection" property for `SchemaError` via
  `test_rejection_does_not_write_to_default_scratch_root`. The
  equivalent snapshot test for `InvalidEvalId` and
  `UnresolvedCapability` paths would be belt-and-braces — added at
  T01.08 (NFR-SEC1 integration set) which is the natural home for
  it.
