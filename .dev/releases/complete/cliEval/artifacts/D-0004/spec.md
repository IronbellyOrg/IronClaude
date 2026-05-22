# D-0004 — `validate_manifest()` schema validation entry point

**Task:** T01.04 (Phase 1, Roadmap FR-SCH1 / R-004)
**Module:** `src/superclaude/cli/eval/loader.py`
**Public surface:** `validate_manifest`, `SchemaError`, `SCHEMA_ERROR_EXIT_CODE`
**Status:** Implemented 2026-05-20

## Function contract

```python
def validate_manifest(path: Path | str) -> list[EvalSpec]
```

- **Input:** filesystem path to a `suites/*.yaml` manifest (either `Path` or
  `str`; the value is normalised to `Path` internally).
- **Output:** ordered `list[EvalSpec]` mirroring `manifest["evals"]` (so
  downstream reporter ordering is deterministic).
- **Error behaviour:** raises `SchemaError` for any read failure, YAML
  decode failure, non-mapping decoded root, or `suite.schema.json`
  violation. The exception carries one `(json_path, message)` tuple per
  underlying `jsonschema.ValidationError`. CLI callers MUST map
  `SchemaError` to process exit code `SCHEMA_ERROR_EXIT_CODE` (= 2).

## Pipeline (FR-SCH1 ordering)

1. **Read** the manifest from disk (`Path.read_text`). No scratch dirs or
   artifact paths are touched.
2. **Decode** YAML with `yaml.safe_load`. Decode errors are wrapped in
   `SchemaError` with path `$`.
3. **Type-check root** — manifest must decode to a mapping; scalars and
   lists raise `SchemaError`.
4. **Validate** against `suite.schema.json` using
   `jsonschema.Draft202012Validator`. All errors are collected, sorted by
   `(absolute_path, message)`, and rendered into `$`-rooted JSON paths
   (e.g. `$.evals[0].id`).
5. **Project** each `manifest["evals"]` row through `EvalSpec.from_dict`
   (T01.03 / DM-002).

> No filesystem writes occur in any branch of this function — that is the
> NFR-SEC1 / FR-SCH1 invariant verified by
> `test_rejection_does_not_write_to_default_scratch_root`.

## Error → exit-code mapping

| Trigger | Raised | Exit code |
|---|---|---|
| Manifest file not found / unreadable | `SchemaError` | 2 |
| YAML decode failure | `SchemaError` | 2 |
| Decoded root is not a mapping | `SchemaError` | 2 |
| `suite.schema.json` validation error (any field, any path) | `SchemaError` | 2 |
| **Schema-valid manifest** | *(no exception; returns `list[EvalSpec]`)* | n/a |

`SCHEMA_ERROR_EXIT_CODE = 2` is the single source of truth — the CLI
boundary (`eval doctor`, `eval run`) imports it instead of duplicating
the literal. The value matches design-spec §4 ("Exit codes" table) which
reserves `2` for "Harness error (manifest invalid, claude binary missing,
etc.)".

> **Out of scope for T01.04:** FR-SCH2 eval-id regex enforcement.
> `validate_eval_id` and `InvalidEvalId` land in T01.05 and are wired
> into the SuiteLoader orchestrator (T01.07) both pre- and
> post-parameterize-expansion. `validate_manifest` only enforces
> shape — including the schema-level `evalIdString` regex that is part
> of `suite.schema.json` — and never reaches the runtime guard.

## JSON-path rendering

`_format_json_path` projects a `jsonschema.ValidationError.absolute_path`
into a `$`-rooted notation:

| Underlying path | Rendered |
|---|---|
| (empty — top-level missing required) | `$` |
| `("name",)` | `$.name` |
| `("evals", 0, "id")` | `$.evals[0].id` |
| `("required_binaries", 0, "failure_mode")` | `$.required_binaries[0].failure_mode` |

The rendering is deterministic across runs (verified by
`test_violations_ordering_is_deterministic`) so reporter output stays
diff-friendly.

## Acceptance criteria → implementation map

| AC bullet (T01.04) | Implementation site |
|---|---|
| `validate_manifest(path)` in `src/superclaude/cli/eval/loader.py` raises `SchemaError` for a fixture manifest missing a required field; error message names the offending JSON path. | `tests/cli/eval/test_schema_validate.py::test_missing_required_field_raises_schema_error_with_field_name` against `fixtures/missing_name_suite.yaml`. |
| Valid fixture manifest returns a list of `EvalSpec` instances matching the schema's `evals[]` length. | `test_valid_manifest_length_matches_evals_block` against `fixtures/valid_suite.yaml` (2 evals → 2 `EvalSpec`s). |
| No filesystem writes occur before validation succeeds (verified by a pytest fixture that snapshots `/tmp/eval-runs` before and after a rejection). | `test_rejection_does_not_write_to_default_scratch_root` snapshots `Path('/tmp/eval-runs')` before and after a `SchemaError`. |
| `TASKLIST_ROOT/artifacts/D-0004/spec.md` records error → exit-code mapping. | This document (see "Error → exit-code mapping" table). |

## Caller contract (downstream consumers)

- **FR-CLI4 `eval doctor` (T01.13)** — invokes `validate_manifest` and maps
  `SchemaError` to exit `SCHEMA_ERROR_EXIT_CODE` with the rendered
  violations on stderr.
- **`eval run` (M2 commands)** — calls `validate_manifest` at the top of
  the run command before any HomeIsolation / scratch-root setup, so a
  bad manifest cannot leave a half-created scratch tree on disk.
- **COMP-002 `SuiteLoader` (T01.07)** — wraps `validate_manifest` and
  layers `validate_eval_id` + capability resolution + parameterize
  expansion on top of the parsed `list[EvalSpec]`.

## Notes / deferred work

- The schema already enforces the FR-SCH2 regex on `evalEntry.id` via
  `evalIdString` (T01.02). `validate_manifest` therefore rejects unsafe
  static ids at the schema layer too; the runtime `validate_eval_id`
  guard (T01.05) is still authoritative for post-parameterize-expanded
  ids (E2 → E2.1, …).
- `SchemaError.violations` is an ordered tuple of `(path, message)` pairs
  so reporters can render every violation rather than just the first.
  This matches the FR-SCH1 spirit of "fail closed with full context."
- `Path.read_text` is used directly (no `open()` context manager) to make
  the FR-SCH1 invariant ("no filesystem writes before validation
  succeeds") obvious — every IO call in this module is a pure read.
