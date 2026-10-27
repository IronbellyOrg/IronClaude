# D-0070 — `Expect.duration` primitive spec (COMP-010.6)

**Task:** T04.08 (Phase 4, Roadmap R-070 / COMP-010.6)
**Module:** `src/superclaude/cli/eval/expect.py` — `Expect.duration`
**Tests:** `tests/cli/eval/test_expect_duration.py` (19 cases)
**Status:** Implemented 2026-05-21

## Signature

```python
Expect.duration(
    max_sec: Optional[float] = None,
    min_sec: Optional[float] = None,
) -> ExpectCallable
```

`Expect.duration` reads `EvalContext.duration_sec` (DM-010) — the
elapsed time of the eval body as recorded by the runner (T03.05) — and
asserts it falls within an optional `[min_sec, max_sec]` envelope. The
returned callable has type `ExpectCallable = Callable[[EvalContext],
ExpectResult]` (DM-009) and carries `__name__ == "duration"` so the
runner's JSONL log records the originating primitive.

## Behaviour matrix

| `max_sec` | `min_sec` | Pass condition | Mode |
|---|---|---|---|
| `None` | `None` | always pass | informational |
| set | `None` | `observed <= max_sec` | upper-bound only |
| `None` | set | `observed >= min_sec` | lower-bound only |
| set | set | `min_sec <= observed <= max_sec` | windowed |

`observed` is `ctx.duration_sec`, surfaced verbatim in
`ExpectResult.details["observed_sec"]` on every path (pass, fail,
informational) so the Reporter (T03.13) can chart benchmark numbers
regardless of whether the assertion fired.

## Informational-PASS semantics

The COMP-010.6 acceptance criterion says: *"when only one bound is set,
the primitive records duration informationally even if the (missing)
other bound would have failed."* The implementation honours this by
treating the absent bound as "no claim" rather than "bound = 0" or
"bound = ∞":

* `Expect.duration(max_sec=5)` against `duration_sec=0.0` → PASS, even
  though a hypothetical `min_sec=1` would have failed.
* `Expect.duration(min_sec=1)` against `duration_sec=10_000.0` → PASS,
  even though a hypothetical `max_sec=10` would have failed.
* `Expect.duration()` (no bounds) → PASS with message
  `"duration={observed:.3f}s (informational)"`. The empty-args invocation
  is the canonical "I want this charted but I don't want to fail the
  run" entry point.

`test_duration_max_only_does_not_fail_on_missing_min_bound` and
`test_duration_min_only_does_not_fail_on_missing_max_bound` pin the
single-bound informational behaviour. The no-bounds variants
(`test_duration_no_bounds_passes_informationally`,
`test_duration_no_bounds_records_zero_duration`) pin the zero-args path.

## Boundary inclusivity

Both bounds are **inclusive**:

* `observed == max_sec` → PASS (the failure check is strict `>`).
* `observed == min_sec` → PASS (the failure check is strict `<`).

This matches manifest authors' intuition (set `max_sec=3` to mean
"three seconds is allowed, four is not"). `test_duration_max_sec_passes_at_boundary`
and `test_duration_min_sec_passes_at_boundary` pin the boundary
contract.

## Evaluation order

When both bounds are set and both are violated (e.g. `min_sec=10,
max_sec=3` with `observed=5`), `max_sec` is evaluated first. The
failure payload pins the over-budget bound regardless of which bound
the manifest author considered "more wrong" — this matches the most
common operational concern (eval ran longer than budget) and gives
the report a single actionable bound to surface.
`test_duration_both_bounds_max_evaluated_before_min` pins this.

## Failure payload

| Branch | `expected` | `actual` | Message |
|---|---|---|---|
| over budget | `{"max_sec": float}` | `float` (observed seconds) | `f"duration {observed:.3f}s exceeds max_sec {max_sec}"` |
| under floor | `{"min_sec": float}` | `float` (observed seconds) | `f"duration {observed:.3f}s below min_sec {min_sec}"` |

`ExpectFailure.traceback` is `None` for a predicate miss — a duration
breach is an ordinary assertion failure, not an exception, so the
Reporter does not render a stack trace.
`test_duration_failure_traceback_field_is_none_for_predicate_miss`
pins this contract.

## Test matrix (`tests/cli/eval/test_expect_duration.py`)

| # | Test | Mode | Direction |
|---|---|---|---|
| 1 | `test_duration_no_bounds_passes_informationally` | no bounds | PASS |
| 2 | `test_duration_no_bounds_records_zero_duration` | no bounds, 0s edge | PASS |
| 3 | `test_duration_max_sec_passes_when_under_budget` | `max_sec` only | PASS |
| 4 | `test_duration_max_sec_passes_at_boundary` | `max_sec` boundary | PASS |
| 5 | `test_duration_max_sec_fails_when_over_budget` | `max_sec` only | FAIL |
| 6 | `test_duration_min_sec_passes_when_above_floor` | `min_sec` only | PASS |
| 7 | `test_duration_min_sec_passes_at_boundary` | `min_sec` boundary | PASS |
| 8 | `test_duration_min_sec_fails_when_below_floor` | `min_sec` only | FAIL |
| 9 | `test_duration_both_bounds_pass_when_within_window` | both bounds | PASS |
| 10 | `test_duration_both_bounds_fail_via_max_sec` | both bounds | FAIL (max) |
| 11 | `test_duration_both_bounds_fail_via_min_sec` | both bounds | FAIL (min) |
| 12 | `test_duration_both_bounds_max_evaluated_before_min` | evaluation order | FAIL (max) |
| 13 | `test_duration_max_only_does_not_fail_on_missing_min_bound` | informational on missing | PASS |
| 14 | `test_duration_min_only_does_not_fail_on_missing_max_bound` | informational on missing | PASS |
| 15 | `test_from_mapping_threads_duration_max_sec` | declarative form | PASS |
| 16 | `test_from_mapping_threads_duration_both_bounds` | declarative form | PASS |
| 17 | `test_from_mapping_threads_duration_no_bounds` | declarative form | PASS |
| 18 | `test_duration_result_carries_primitive_name_and_timing` | DM-009 envelope | PASS |
| 19 | `test_duration_failure_traceback_field_is_none_for_predicate_miss` | failure payload | FAIL |

All 19 cases pass under
`uv run pytest tests/cli/eval/test_expect_duration.py -v` in 0.19 s on
2026-05-21.

## Declarative form

`Expect.from_mapping({"duration": {...}})` resolves to the same
callable as the programmatic form. Three declarative shapes are
supported:

```yaml
expects:
  - duration: {}                          # informational PASS
  - duration: {max_sec: 3.0}              # upper bound only
  - duration: {min_sec: 1.0, max_sec: 3.0}  # windowed
```

The empty mapping `{}` is the manifest sugar for the zero-args
informational form. `test_from_mapping_threads_duration_no_bounds`,
`test_from_mapping_threads_duration_max_sec`, and
`test_from_mapping_threads_duration_both_bounds` pin all three shapes.

## Downstream consumers

* Benchmarking manifests — `duration: {}` records observed timings on
  every eval without forcing an assertion, so the Reporter can produce
  a "duration trend" panel from the artifact tree.
* T05.x (eval suite) — evals that have a known operational budget pin
  `duration: {max_sec: N}` so a regression that doubles eval runtime
  surfaces as FAIL even if the functional Expects still pass.

## Linked roadmap entries

* R-070 — COMP-010.6 / D-0070
* Depends on: T04.01 (Expect package skeleton, D-0064)
* Used by: T05.x manifests; benchmarking surface (post-M5)
