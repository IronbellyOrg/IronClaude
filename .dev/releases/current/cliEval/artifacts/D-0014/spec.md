# D-0014 — ExpectFailure dataclass spec

**Task:** T01.16 (Phase 1, Roadmap DM-005 / R-014)
**Module:** `src/superclaude/cli/eval/models.py`
**Status:** Implemented 2026-05-20

## Field schema (8-field contract)

| # | Field          | Type             | Default | Purpose |
|---|----------------|------------------|---------|---------|
| 1 | `eval_id`      | `str`            | required | Eval id (already FR-SCH2 regex-guarded upstream by T01.05) so the reporter can use it verbatim in artifact filenames. |
| 2 | `expect_id`    | `str`            | required | Stable per-Expect identifier (e.g. `"exit_code[0]"`, `"file.contains_event[2]"`); used by the reporter to dedupe failures across re-runs. |
| 3 | `expect_name`  | `str`            | required | DSL method name that produced the failure; matches `ExpectResult.name` so paired records line up in the JSON report. |
| 4 | `expected`     | `Any`            | required | Expected value from the manifest. Typed `Any` because primitives (COMP-010.1–6) accept JSON-shaped payloads of arbitrary shape. |
| 5 | `actual`       | `Any`            | required | Observed value the Expect saw on the run; same typing rationale as `expected`. |
| 6 | `message`      | `str`            | `""`    | Human-readable one-liner summarising the diff. Default empty when the `expected`/`actual` diff is self-explanatory. |
| 7 | `artifact_ref` | `Optional[str]`  | `None`  | Path-or-URI to a side-car artifact (rendered diff, dumped JSONL, stderr). `None` when no artifact was written. |
| 8 | `traceback`    | `Optional[str]`  | `None`  | Captured Python traceback string when the Expect itself raised. `None` for clean-diff assertion failures. |

## Invariants

- `@dataclass(frozen=True)` — mutation raises `dataclasses.FrozenInstanceError` (`test_expect_failure_is_frozen`).
- Field declaration order matches DM-005 verbatim; `to_dict()` enforces the same ordering through an explicit field tuple so the output is stable regardless of Python version or dataclass internals (`test_expect_failure_to_dict_field_order_matches_dm005`).
- Two instances built from identical arguments compare equal via the `@dataclass`-generated `__eq__` (`test_expect_failure_deterministic_equality`).
- One `ExpectFailure` entry per failing Expect: the Reporter (COMP-008 / T03.13) constructs a fresh record per assertion. Validated structurally via `test_expect_failure_two_per_eval_pattern`; the end-to-end aggregation lives in T03.13.

## Serialisation

- `to_dict()` builds the dict explicitly from `_EXPECT_FAILURE_FIELDS` so key ordering is locked. `expected` / `actual` are passed through as-is — manifest authors populate them with JSON-shaped payloads, so `json.dumps` over the result is direct.
- Round-trips through `json.dumps(..., sort_keys=True)` cleanly (`test_expect_failure_to_dict_is_json_serialisable`).
- Recursive unwrap path: `ExpectResult(failure=ExpectFailure(...)).to_dict()["failure"]` is a plain dict matching the DM-005 schema. Locked by `test_expect_failure_round_trips_inside_expect_result`.
- `dataclasses.asdict(failure)` agrees on values with `to_dict()` (`test_expect_failure_asdict_matches_to_dict`); the ordering guarantee is owned exclusively by `to_dict()`.

## Caller contract (downstream consumers)

- **COMP-008 Reporter (T03.13)** — constructs one `ExpectFailure` per failing assertion within each `EvalOutcome` (T03.01); emits `failure.to_dict()` into the JSON report.
- **DM-009 `ExpectResult` (T01.15)** — holds an `Optional[ExpectFailure]` on the `failure` field. T01.15 had been using a forward-reference annotation (`Optional["ExpectFailure"]`); T01.16 satisfies the reference without changing any production code in T01.15.
- **EvalOutcome (T03.01)** — aggregates a list of `ExpectFailure` per eval; the Reporter renders them grouped by `eval_id`.

## Acceptance criteria → implementation map

| AC bullet (T01.16)                                                                              | Implementation site                                                                                       |
|-------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| Frozen `ExpectFailure` with the 8 fields named in DM-005.                                       | `models.py` — `@dataclass(frozen=True) class ExpectFailure` (covered by `test_expect_failure_has_required_fields`, `test_expect_failure_is_frozen`). |
| `to_dict()` output is JSON-serializable per DM-005 implicit serialization requirement.           | `to_dict()` returns explicit ordered dict; covered by `test_expect_failure_to_dict_is_json_serialisable`, `test_expect_failure_to_dict_field_order_matches_dm005`. |
| Reporter produces exactly one `ExpectFailure` per failing Expect.                                | Construction pattern locked by `test_expect_failure_two_per_eval_pattern`; the integration assertion (multi-Expect single-eval) is owned by COMP-008 / T03.13. |
| `spec.md` documents the 8-field contract.                                                        | This file.                                                                                                |

## Out of scope for T01.16

- Real `ExpectCallable` primitives that emit populated `ExpectFailure`s — COMP-010.1–6 (M4).
- Reporter side-effects (JSONL writes, terminal rendering, artifact ref resolution) — COMP-008 (T03.13).
- `EvalOutcome` aggregation of multiple `ExpectFailure`s per eval — T03.01.
- Schema-level constraints on `expected` / `actual` payload shape — manifest authors are free to use any JSON-serialisable value.
