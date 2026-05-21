# D-0053 — Implementation notes

## Design decisions

### Required-field set deliberately excludes `finished_at` and `artifacts`

T03.10 acceptance enumerates the required fields as:

```
run_id, started_at, duration_sec, suite, manifest_version,
parallel, counts, totals, evals
```

Both `finished_at` and `artifacts` are declared as `properties` but NOT
listed in `required`:

- `finished_at` is empty (`""`) for partial summaries written on SIGINT
  before the orchestrator completed (NFR-REL1 / T03.07 path). Making it
  required here would force the SIGINT path to emit either an unhelpful
  empty string or a synthetic timestamp.
- `artifacts` defaults to an empty mapping on `RunSummary`. Forcing it
  to appear at the top level would push every minimal run to write `{}`
  for no value-add.

The dataclass *does* emit both fields (`RunSummary.to_dict()` is
deterministic), so reference-fixture validation still exercises the
shape — the schema just leaves the two fields optional so future writers
(or partial summaries) can omit them.

### `additionalProperties: true` at the top level, `false` on sub-objects

We want the schema to be forward-compatible at the top level: if DM-012
grows a 10th field in M5, existing producers (Reporter, orchestrator)
should still write a valid file until they catch up. So
`additionalProperties: true` keeps the door open at the document root.

`counts` and `totals` are the opposite case: they are closed accounting
records — any extra key in `counts` is a contract bug (it would corrupt
the FR-RPT1 invariant audit trail). So both sub-objects use
`additionalProperties: false`.

`evals[]` items also use `additionalProperties: false`: DM-001 declared
the 9-field shape exactly, and an orchestrator that smuggles extra keys
into an EvalOutcome serialisation is misreporting per §9.

### Schema lives next to its loader, not next to the suite schema

`suite.schema.json` (T01.02) sits under `src/superclaude/cli/eval/suites/`
because it is paired with the suite YAML loader. The summary schema is
paired with the Reporter, not the loader, so co-locating it under
`schemas/` (rather than `reporter/`) keeps the artefact discoverable
even before the Reporter module lands (T03.13).

`schemas/__init__.py` exports `load_summary_schema()` so callers — the
Reporter, tests, and future schemas — go through one read path. This
ride-along loader uses `importlib.resources` rather than
`__file__.parent` to keep the schema importable from a built wheel.

### `parallel` carries the [1,15] clamp in the schema

The clamp is enforced at runtime by COMP-003 RunOrchestrator (T03.15),
but encoding it on the wire schema has two upsides:

1. A summary file that names `parallel: 0` or `parallel: 16` is
   immediately a contract bug — the schema rejects it without the
   reviewer having to remember the clamp from FR-G2 / T03.16.
2. The schema becomes a stand-alone source of truth: tools that build
   `summary.json` outside the Python codebase (CI dashboards, badge
   generators) cannot wander outside the documented range.

### Field-order constants are not exported

Field declaration order inside `properties` is informational —
JSON-schema validation is order-independent. The runtime contract
(`_EVAL_OUTCOME_FIELDS`, `_RUN_SUMMARY_FIELDS`, etc.) is where the
canonical order lives; the schema mirrors it for readability but tests
assert ordering against the runtime constants, not the schema.

### `status` enum order mirrors `EVAL_STATUSES` exactly

`test_schema_status_enum_matches_runtime_model` pins the enum order to
`get_args(EvalStatus)` (T03.01). If a future refactor renames or
reorders a status literal, the test fails immediately rather than
letting the schema drift silently from the runtime model.

### Tests deliberately avoid asserting against fixture filenames in error messages

`pytest.raises(ValidationError) ... assert "BOGUS" in str(exc_info.value)`
keeps the failure case dependent on the schema-level rejection, not on
jsonschema's traceback format. If we upgrade `jsonschema` and the
traceback shape shifts, the tests still pass.

## Cross-references

- **Tests** — `tests/cli/eval/test_summary_schema.py` (17 tests; all
  passing).
- **Fixtures** — `tests/cli/eval/fixtures/summary_schema/{valid,invalid}_*.json`.
- **Loader** — `superclaude.cli.eval.schemas.load_summary_schema`.
- **Runtime model** — `RunSummary.to_dict()` in
  `superclaude.cli.eval.models` (T03.09).
- **Reference snippet** — design-spec §9 ("`summary.json` (machine-
  readable)") drove the fixture shape; `valid_full.json` mirrors it
  verbatim except for `expects[].evidence` which is folded into
  `details + message` per the DM-009 model (T01.15).

## Out-of-scope items (forward references)

- FR-RPT1 `write_aggregated_report` and `ReporterContractViolation` (exit
  2) on N'-vs-K mismatch — T03.11.
- TEST-007 schema fidelity test suite (round-trip recorded summaries
  through the schema) — T04.17.
- JUnit schema parity (`junit.xml`) — out of scope; the JUnit emitter
  uses its own XSD upstream.
