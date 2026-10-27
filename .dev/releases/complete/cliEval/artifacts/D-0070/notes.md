# D-0070 — Implementation notes

## Why this task was test-only

T04.01 (D-0064) shipped the full `Expect.duration` body alongside the
package skeleton. The primitive already supported:

* Two named arguments: `max_sec` and `min_sec` (each `Optional[float]`,
  default `None`).
* The four-mode behaviour matrix (no bounds / max only / min only /
  both bounds).
* Failure payloads with `expected` / `actual` (DM-005), inclusive
  boundary semantics, and `max_sec`-first evaluation order.
* `observed_sec` surfaced in `ExpectResult.details` on every path.

T04.08's deliverable is the **per-primitive acceptance harness** that
touches every mode in the behaviour matrix, the informational-PASS
semantics for the missing-bound case, and the DM-009 envelope. No body
changes were required to `src/superclaude/cli/eval/expect.py`.

## Decisions

1. **Inclusive boundaries (`<`/`>` not `<=`/`>=`).** `observed ==
   max_sec` is PASS rather than FAIL. Manifest authors who write
   `max_sec=3` mean "three seconds is allowed," and the inclusive
   reading matches the colloquial intent. The two boundary tests
   (`test_duration_max_sec_passes_at_boundary`,
   `test_duration_min_sec_passes_at_boundary`) pin both ends so any
   future change to strict comparisons fails the suite.

2. **Single-bound missing-bound is informational, not zero/∞.** When
   only `max_sec` is set, the missing `min_sec` is treated as "no
   claim" rather than "min_sec=0" or "min_sec=-∞". A 0-second eval
   against `max_sec=5` PASSes — there is no implicit floor. Symmetric
   on the `min_sec` side. This is the COMP-010.6 informational-PASS
   contract and the two dedicated tests
   (`test_duration_max_only_does_not_fail_on_missing_min_bound`,
   `test_duration_min_only_does_not_fail_on_missing_max_bound`) pin it
   so a future refactor that "tightens" the missing bound to a
   zero-floor would visibly fail.

3. **`max_sec` evaluated before `min_sec` when both are violated.**
   The over-budget case is more operationally actionable (the eval ran
   longer than the harness's wall-clock budget), so when both bounds
   are violated the failure payload pins `max_sec`. This is exercised
   even on the degenerate `min_sec > max_sec` window via
   `test_duration_both_bounds_max_evaluated_before_min` so the
   evaluation order survives any future bound-validation refactor.

4. **`observed_sec` is in `details` on every path.** Even when the
   assertion fails or runs informationally, the observed duration is
   handed to the Reporter unconditionally so dashboards / JUnit
   payloads can chart timings without re-parsing the artifact tree.
   `test_duration_max_sec_fails_when_over_budget` explicitly asserts
   `result.details["observed_sec"] == 5.0` on the FAIL path so this
   contract cannot regress silently.

5. **No-args is the canonical informational form.** `Expect.duration()`
   with no bounds returns `passed=True` with message
   `"duration={observed:.3f}s (informational)"`. This is the explicit
   "record but don't assert" entry point — manifests that just want
   timing data on the report attach `duration: {}` to every eval
   without needing a sentinel `max_sec=float("inf")` workaround.

6. **`ExpectFailure.traceback` is `None` for predicate misses.** An
   over-budget or under-floor duration is an ordinary assertion
   failure, not an exception. The Reporter (T03.13) uses the presence
   of `traceback` to decide whether to render a stack-trace section,
   and a duration breach should not produce one.
   `test_duration_failure_traceback_field_is_none_for_predicate_miss`
   pins this contract.

## What was NOT changed in src/

* `Expect.duration` body in `src/superclaude/cli/eval/expect.py` was
  already complete after T04.01. The T04.08 acceptance suite is
  purely additive.
* `_named_callable`, `_timed_result`, and `_make_failure` helpers were
  untouched.

## Followups deferred

* Manifest-loader smoke test pairing `Expect.from_mapping` with a
  fully assembled `expects:` block that includes a `duration` entry
  (planned alongside the manifest loader landing in T05.x).
* Reporter rendering of the `observed_sec` field on the informational
  path (planned alongside the TEST-007 reporter contract suite,
  T04.17).
* Duration aggregation across a suite (mean / p95) for the
  benchmarking dashboard (post-M5).

## Linked artifacts

* Spec: `D-0070/spec.md`
* Evidence: `evidence/T04.08/pytest-output.txt`
* Source: `src/superclaude/cli/eval/expect.py` (`Expect.duration`)
* Test module: `tests/cli/eval/test_expect_duration.py`
* Roadmap: R-070, depends on T04.01 (D-0064)
