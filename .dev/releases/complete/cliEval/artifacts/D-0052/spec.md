# D-0052 — RunSummary dataclass spec

**Task:** T03.09 (Phase 3, Roadmap DM-004 / R-052)
**Module:** `src/superclaude/cli/eval/models.py`
**Status:** Implemented 2026-05-20

## Top-level field schema (11-field contract)

| # | Field              | Type                            | Default                       | Purpose |
|---|--------------------|---------------------------------|-------------------------------|---------|
| 1 | `run_id`           | `str`                           | required                      | Opaque identifier the orchestrator stamps on the run. Stable across artifacts so reviewers can join per-eval JSONL logs against the aggregate summary. |
| 2 | `started_at`       | `str` (ISO 8601)                | required                      | Wall-clock timestamp marking the orchestrator start. Stored as `str` so the field round-trips through JSON without bespoke datetime serialisation. |
| 3 | `finished_at`      | `str` (ISO 8601)                | required                      | Wall-clock timestamp marking the orchestrator stop. May be empty for partial summaries written on SIGINT before the orchestrator completed. |
| 4 | `duration_sec`     | `float`                         | required                      | Wall-clock seconds the orchestrator ran end to end. `float` for sub-millisecond resolution. |
| 5 | `suite`            | `str`                           | required                      | Manifest path / suite identifier the orchestrator loaded. Rendered verbatim in the summary header. |
| 6 | `manifest_version` | `str`                           | required                      | Semantic version stamped on the manifest at author time. Helps the Reporter detect mismatched evals when a manifest is bumped between runs. |
| 7 | `parallel`         | `int`                           | required                      | Concurrency level the orchestrator scheduled at (post-clamp to `[1,15]`). |
| 8 | `counts`           | `RunCounts`                     | required                      | DM-012 counts sub-structure. `RunSummary.__post_init__` asserts the equation matches the boolean flag (see Invariants). |
| 9 | `totals`           | `RunTotals`                     | required                      | DM-012 totals sub-structure. Six status tallies the Reporter renders in the summary headline. |
| 10 | `evals`            | `tuple[EvalOutcome, ...]`       | `()`                          | Per-expanded-eval outcomes (DM-001 / T03.01). Tuple keeps the frozen dataclass hashable; FR-RPT1 (T03.11) enforces `len(evals) == counts.expanded_n_prime` outside this model so partial summaries (SIGINT) remain constructible. |
| 11 | `artifacts`        | `Mapping[str, str]`             | `field(default_factory=dict)` | Artifact-name → path mapping the orchestrator emits (JSONL directory, disk-budget breach side-car, ...). Each instance gets its own mapping; `to_dict()` returns a shallow copy. |

## `counts` sub-field schema (DM-012, 5 fields)

| # | Field                              | Type   | Purpose |
|---|------------------------------------|--------|---------|
| 1 | `manifest_n`                       | `int`  | Number of rows in the source manifest before parameterize expansion. |
| 2 | `expanded_n_prime`                 | `int`  | Number of expanded eval rows after parameterize expansion. Ground-truth row count for FR-RPT1 (T03.11). |
| 3 | `kept_k`                           | `int`  | Number of expanded rows that ran end-to-end (status in `{PASS,FAIL,ERRORED,TIMEOUT,XFAIL,XPASS}`). |
| 4 | `skipped_s`                        | `int`  | Number of expanded rows that were skipped (status `SKIPPED` or `INTERRUPTED`). |
| 5 | `kept_plus_skipped_equals_n_prime` | `bool` | DM-012 boolean assertion that the equation `kept_k + skipped_s == expanded_n_prime` holds. Enforced at `RunSummary` construction time. |

## `totals` sub-field schema (DM-012, 6 fields)

| # | Field         | Type  | Default | Purpose |
|---|---------------|-------|---------|---------|
| 1 | `passed`      | `int` | `0`     | Number of `PASS` (and `XPASS`) outcomes. |
| 2 | `failed`      | `int` | `0`     | Number of `FAIL` (and `XFAIL`) outcomes. |
| 3 | `skipped`     | `int` | `0`     | Number of `SKIPPED` outcomes. |
| 4 | `errored`     | `int` | `0`     | Number of `ERRORED` outcomes (harness exceptions). |
| 5 | `interrupted` | `int` | `0`     | Number of `INTERRUPTED` outcomes (SIGINT cancellation). |
| 6 | `timeout`     | `int` | `0`     | Number of `TIMEOUT` outcomes (per-eval timeout enforcement). |

## Invariants

- `@dataclass(frozen=True)` on `RunSummary`, `RunCounts`, `RunTotals` — mutation raises `dataclasses.FrozenInstanceError` (covered by `test_run_summary_is_frozen`, `test_run_counts_is_frozen`).
- Field declaration order matches DM-004 verbatim so `to_dict()` ordering is stable across reporter snapshots and review diffs (covered by `test_run_summary_to_dict_field_order_matches_dm004`).
- `counts` sub-field order matches DM-012 verbatim (covered by `test_run_summary_to_dict_counts_sub_field_order`).
- `totals` sub-field order matches DM-012 verbatim (covered by `test_run_summary_to_dict_totals_sub_field_order`).
- `RunSummary.__post_init__` enforces that `counts.kept_plus_skipped_equals_n_prime` reflects the actual math: `(kept_k + skipped_s) == expanded_n_prime`. Any disagreement raises `ValueError` so a misreporting orchestrator fails loudly rather than emitting an internally inconsistent summary (covered by `test_run_summary_rejects_mismatched_counts_when_flag_true`, `test_run_summary_rejects_mismatched_counts_when_flag_false`, `test_run_summary_accepts_consistent_counts`, `test_run_summary_accepts_consistent_false_flag`).
- `artifacts` `default_factory=dict` hands each instance an independent mapping (covered by `test_run_summary_artifacts_default_is_independent_per_instance`).
- Two instances built from identical arguments compare equal via the `@dataclass`-generated `__eq__` (covered by `test_run_summary_deterministic_equality`).

## Serialisation

- `to_dict()` builds an explicit ordered `dict` from `_RUN_SUMMARY_FIELDS` so output ordering is stable regardless of Python version or dataclass internals.
- Nested `RunCounts` and `RunTotals` are unwrapped via their own `to_dict()` so the Reporter never has to recurse manually (covered by `test_run_summary_to_dict_counts_sub_field_order`, `test_run_summary_to_dict_totals_sub_field_order`).
- Nested `EvalOutcome` values in `evals` are unwrapped via `EvalOutcome.to_dict()` (covered by `test_run_summary_to_dict_unwraps_nested_outcomes`).
- `artifacts` is shallow-copied into a plain `dict` so callers that mutate the returned mapping do not affect the immutable source (covered by `test_run_summary_to_dict_artifacts_is_independent_of_source`).
- Round-trips through `json.dumps(..., sort_keys=True)` cleanly (covered by `test_run_summary_to_dict_is_json_serialisable`, `test_run_counts_to_dict_is_json_serialisable`, `test_run_totals_to_dict_is_json_serialisable`).

## Module symbol re-exports

`RunSummary`, `RunCounts`, and `RunTotals` are re-exported from `superclaude.cli.eval` (`__init__.py`) so consumers (Reporter, RunOrchestrator) can import them without reaching into `models` (covered by `test_run_summary_reexported_from_package`).

## Caller contract (downstream consumers)

- COMP-003 RunOrchestrator (T03.15) — emits one `RunSummary` per `superclaude eval run` invocation after collecting per-eval `EvalOutcome`s.
- COMP-008 Reporter (T03.13) — reads `RunSummary.to_dict()` to render `summary.md`, `summary.json`, and (optionally) `junit.xml`. The FR-RPT1 invariant guard (T03.11) reads `counts.expanded_n_prime` as ground truth.
- DM-012 summary.json schema (T03.10) — validates the serialised output against the canonical JSON schema. `counts` and `totals` ordering aligns with the schema's `required` arrays so review diffs stay clean.

## Acceptance criteria → implementation map

| AC bullet (T03.09)                                                                                                                                            | Implementation site                                                                                                                                                                                |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `RunSummary` exposes the 11 fields listed in DM-004 with nested `counts` containing the 5 sub-fields.                                                          | `models.py` — `@dataclass(frozen=True) class RunSummary` + `class RunCounts` (covered by `test_run_summary_has_required_fields`, `test_run_counts_has_required_sub_fields`).                       |
| `to_dict()` returns a deterministic JSON-serialisable mapping.                                                                                                | `_RUN_SUMMARY_FIELDS`-driven ordered dict + nested `RunCounts/RunTotals/EvalOutcome.to_dict()` + shallow-copied artifacts (covered by the four `to_dict` tests including the json round-trip).      |
| `RunSummary` constructor validates `counts.kept_plus_skipped_equals_n_prime` boolean and asserts the equation holds.                                          | `RunSummary.__post_init__` raises `ValueError` when the flag and the actual math disagree (covered by `test_run_summary_rejects_mismatched_counts_when_flag_true` and the `_when_flag_false` test). |
| `TASKLIST_ROOT/artifacts/D-0052/spec.md` records the contract.                                                                                                | This file.                                                                                                                                                                                          |

## Out of scope for T03.09

- DM-012 `summary.schema.json` definition — T03.10.
- FR-RPT1 (`write_aggregated_report` + `ReporterContractViolation` guard) — T03.11.
- Reporter side-effects (`to_markdown` / `to_yaml` / `to_json` / `to_junit` emitters) — T03.13.
- RunOrchestrator construction site for `RunSummary` instances — T03.15.
