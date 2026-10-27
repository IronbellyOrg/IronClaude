# D-0046 — EvalResult dataclass spec

**Task:** T03.02 (Phase 3, Roadmap DM-003 / R-046)
**Module:** `src/superclaude/cli/eval/models.py`
**Status:** Implemented 2026-05-20

## Field schema (9-field contract)

| # | Field          | Type                            | Default                       | Purpose |
|---|----------------|---------------------------------|-------------------------------|---------|
| 1 | `eval_id`      | `str`                           | required                      | Id of the expanded eval. Already regex-guarded by FR-SCH2 (T01.05) so the Reporter uses it verbatim in artifact filenames. |
| 2 | `outcome`      | `EvalOutcome` (DM-001)          | required                      | Runner emission wrapped by the result. The pair travels together: runner builds an `EvalOutcome` and the wrapper turns it into the Reporter's input. |
| 3 | `start`        | `str` (ISO 8601)                | required                      | Wall-clock timestamp marking lifecycle start. Stored as `str` so the field round-trips through JSON without bespoke datetime serialisation. |
| 4 | `end`          | `str` (ISO 8601)                | required                      | Wall-clock timestamp marking lifecycle end (teardown complete). Same string-typing rationale as `start`. May be empty for partial summaries captured on SIGINT before teardown wrote `end`. |
| 5 | `duration_sec` | `float`                         | `0.0`                         | Wall-clock seconds. Always computed from `end - start` in `__post_init__` when both timestamps are non-empty (any caller-supplied value is overwritten so the field cannot drift). When either timestamp is empty the caller-supplied value is kept verbatim so partial summaries remain constructible. |
| 6 | `stdout`       | `str`                           | `""`                          | Captured stdout from the eval's PTY transcript (ANSI already stripped by `PtyStream` / T02.17 upstream). |
| 7 | `stderr`       | `str`                           | `""`                          | Captured stderr from the eval. |
| 8 | `artifacts`    | `Mapping[str, str]`             | `field(default_factory=dict)` | Artifact-name → path mapping. Each instance gets its own mapping via `default_factory`; `to_dict()` returns a shallow copy so callers that mutate the returned mapping do not affect the immutable source. |
| 9 | `error`        | `Optional[BaseException]`       | `None`                        | Harness-level exception captured by the runner (NOT an assertion failure — those live in `EvalOutcome.expects[*].failure`). Rendered as `{"type": "<fqcn>", "message": "<str>"}` by `to_dict()` (or `None`) so the payload stays JSON-serialisable. |

## Invariants

- `@dataclass(frozen=True)` — mutation raises `dataclasses.FrozenInstanceError` (covered by `test_eval_result_is_frozen`).
- Field declaration order matches DM-003 verbatim so `to_dict()` ordering is stable across Reporter snapshots and review diffs (covered by `test_eval_result_has_required_fields` and `test_eval_result_to_dict_field_order_matches_dm003`).
- `duration_sec` is **always** computed from `end - start` when both timestamps are non-empty; caller-supplied values are overwritten (covered by `test_eval_result_duration_sec_is_computed_from_timestamps` and `test_eval_result_duration_sec_caller_value_is_overwritten`).
- When either `start` or `end` is empty the caller's `duration_sec` is preserved so partial / interrupted runs remain constructible (covered by `test_eval_result_duration_sec_kept_when_timestamps_missing`).
- `artifacts` `default_factory=dict` hands each instance an independent mapping (covered by `test_eval_result_artifacts_default_is_independent_per_instance`).
- Two instances built from identical arguments compare equal via the `@dataclass`-generated `__eq__` (covered by `test_eval_result_deterministic_equality`).

## Serialisation

- `to_dict()` builds an explicit ordered `dict` from `_EVAL_RESULT_FIELDS` so output ordering is stable regardless of Python version or dataclass internals.
- Nested `EvalOutcome` is unwrapped via its own `to_dict()` so the Reporter never has to recurse manually (covered by `test_eval_result_to_dict_unwraps_nested_outcome`).
- `artifacts` is shallow-copied into a plain `dict` so callers that mutate the returned mapping do not affect the immutable source (covered by `test_eval_result_to_dict_artifacts_is_independent_of_source`).
- `error` is rendered through `_render_error()` into a 2-key `{"type": "<fqcn>", "message": str}` mapping (or `None`). The traceback is *not* serialised here — the per-eval JSONL log (T03.05) is the authoritative traceback source; DM-003's `error` is the Reporter-facing summary handle (covered by `test_eval_result_to_dict_renders_error_as_typed_mapping` and `test_eval_result_to_dict_error_none_when_no_error`).
- Round-trips through `json.dumps(..., sort_keys=True)` cleanly (covered by `test_eval_result_to_dict_is_json_serialisable`).

## Module symbol re-exports

`EvalResult` is re-exported from `superclaude.cli.eval` (`__init__.py`) so consumers (Reporter, RunOrchestrator) can import it without reaching into `models` (covered by `test_eval_result_reexported_from_package`).

## Caller contract (downstream consumers)

- COMP-004 EvalRunner (T03.04 / T03.05) — wraps each emitted `EvalOutcome` in an `EvalResult` after capturing stdout/stderr and the lifecycle timestamps.
- COMP-008 Reporter (T03.13) — reads `EvalResult.to_dict()` to render the per-eval rows of `summary.md` / `summary.json` and to flow into JUnit emission.
- COMP-003 RunOrchestrator (T03.15) — receives one `EvalResult` per expanded spec from the worker pool.

## Acceptance criteria → implementation map

| AC bullet (T03.02)                                                                                            | Implementation site                                                                                                       |
|---------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| `EvalResult` exposes fields `eval_id,outcome,start,end,duration_sec,stdout,stderr,artifacts,error`.           | `models.py` — `@dataclass(frozen=True) class EvalResult` (covered by `test_eval_result_has_required_fields`).             |
| `EvalResult.to_dict()` returns a JSON-serialisable mapping deterministically.                                 | `_EVAL_RESULT_FIELDS`-driven ordered dict + nested `EvalOutcome.to_dict()` + `_render_error` + shallow-copied artifacts (covered by `test_eval_result_to_dict_field_order_matches_dm003`, `test_eval_result_to_dict_is_json_serialisable`, `test_eval_result_to_dict_renders_error_as_typed_mapping`). |
| `duration_sec` is computed from `end - start` consistently.                                                   | `EvalResult.__post_init__` overwrites the field via `object.__setattr__` when both timestamps are non-empty (covered by `test_eval_result_duration_sec_is_computed_from_timestamps` and `test_eval_result_duration_sec_caller_value_is_overwritten`). |
| `TASKLIST_ROOT/artifacts/D-0046/spec.md` records the contract.                                                | This file.                                                                                                                |

## Out of scope for T03.02

- `EvalContext` (DM-010 / T03.03) — runtime context passed to each ExpectCallable.
- FR-LC1 lifecycle skeleton (T03.04) — the EvalRunner construction site for these results.
- Reporter side-effects (summary.md / summary.json writes, JUnit emission) — COMP-008 (T03.13).
- Per-eval JSONL log format — T03.05.
