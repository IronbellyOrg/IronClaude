# D-0066 — Implementation notes

## Why this task was test-only

T04.01 (D-0064) shipped the full `Expect.jsonl` body alongside the
package skeleton: named-path lookup via `ctx.jsonl_paths`, blank-line-
tolerant parsing, per-line JSON decode with line-numbered error
reporting, filter → line_count → assert_each → assert_any evaluation
order, and structured `ExpectFailure` records for each failure branch.
T04.03's deliverable is the **per-primitive acceptance harness** that
touches every named argument and the predicate semantics under
hook-telemetry fixture inputs. No body changes were required to
`src/superclaude/cli/eval/expect.py`.

## Decisions

1. **Hook-telemetry shape is the canonical fixture.** The test module
   defines a single `HOOK_ROWS` tuple mirroring the per-eval
   `hooks.jsonl` HookAdapter writes (T02.16). Every assertion test
   exercises one of: matcher-pattern selection, status equality, event
   sequence, session-stop marker. This pins the fixture shape that E1
   (T05.02) and E2.x (T05.10) will rely on, so any future schema
   change to the runner's emitted JSONL must update the fixture and
   every downstream eval together.
2. **Predicate signature is `Callable[[Mapping[str, Any]], bool]`.**
   Manifest-loaded rows come back from `json.loads` as plain dicts; the
   primitive type-hints the predicate against `Mapping` so callers can
   wrap rows in `MappingProxyType` without breaking. The test for
   `assert_each` and `assert_any` uses bare `dict.get` to confirm the
   common case.
3. **`line_count` counts the *filtered* set, not the raw row count.**
   `test_filter_narrows_rows_before_line_count` and
   `test_filter_to_zero_rows_passes_with_count_zero` pin this ordering;
   it is the only ordering that lets manifests assert "exactly 2
   PreToolUse rows" without a follow-up `filter` argument on the
   `line_count` itself.
4. **Blank lines are skipped silently.** Hook adapters sometimes flush
   buffered lines with a trailing newline; counting that newline as a
   row would force every eval to set `line_count=N+1`. The test
   `test_line_count_ignores_blank_lines` documents the behaviour.
5. **Invalid JSON yields a structured FAIL, not an uncaught
   exception.** `test_invalid_json_line_fails_with_lineno` asserts the
   line number is included in the message and the offending raw text
   is in `failure.actual`. The traceback is also populated so the
   Reporter can surface the `json.JSONDecodeError` in verbose output.
6. **Path resolution at call time.** Resolution lives inside `_run`,
   not at primitive construction, so one manifest-built callable runs
   across many EvalContexts. The named-lookup branch is hit first;
   `test_named_path_resolves_via_jsonl_paths` and the two `path`-string
   tests pin both branches.

## Things explicitly not covered here

* **Predicate exceptions raising mid-iteration** — not exercised. The
  primitive deliberately lets predicate exceptions propagate to the
  runner's ExpectCallable harness (T03.04), which wraps them with a
  traceback. Catching them inside `Expect.jsonl` would mask predicate
  bugs (e.g. typos in `row.get("eventt")`) as silent FAILs without
  context. The contract is "predicate must not raise"; misuse is a
  manifest authoring error, not a primitive concern.
* **Non-mapping JSON values** — a JSONL of bare integers (`5\n6\n`)
  would parse cleanly and pass the `assert_each`/`assert_any`
  predicates with whatever the predicate does on a non-mapping input.
  This is intentional: the primitive doesn't enforce row shape; the
  predicate does.
* **Mutually-exclusive argument validation** — none. Unlike
  `Expect.exit_code` (`equals` vs `in_set`), every argument here is
  composable. The test matrix covers the orthogonal combinations.

## Follow-ups

None. Two adjacent tasks consume this primitive:

* T05.02 (E1) wires `Expect.jsonl` into the sticky-lifecycle eval,
  asserting the post-stop JSONL row count and matcher coverage.
* T05.10 (E2.x) wires it into per-matcher coverage assertions
  validating that every declared matcher pattern emits at least one
  PreToolUse row.

Both pass without any further changes to `Expect.jsonl`.
