# D-0064 — Design notes

## Why a sentinel for `settings_json.equals` and `exit_code.equals`

JSON values include `null` (Python `None`). A naive default of `None`
collapses two distinct intents: "the manifest did not set `equals`" and
"compare the JSON value against `null`". The module-level `_SENTINEL =
object()` lets both primitives distinguish absence from `None`-compare.

Initial implementation used a walrus inside a default-argument
expression (`equals: Any = _SENTINEL := object()`) which is invalid
Python syntax. Fixed by hoisting the sentinel to module scope above the
class definition; default arguments are evaluated at class-definition
time, so the forward order matters.

## Why exit_code mutual-exclusion fires only on explicit kwargs

The default `Expect.exit_code()` asserts `equals=0`. A manifest writing
`{exit_code: {in_set: [0, 1]}}` should not trip the mutual-exclusion
guard just because the default value of `equals` happens to be set.

We detect explicit `equals=` via the same `_SENTINEL` sentinel: the
default parameter is `_SENTINEL`, and the guard only fires when the
caller passes something other than the sentinel along with `in_set`.

## Why ANSI stripping is re-applied at predicate time

`PtyStream` already strips ANSI escapes on capture (T02.17). The
primitive re-applies `ANSI_ESCAPE_RE.sub("", text)` defensively so:

1. Manifest authors who feed `transcript_path` (raw PTY transcript with
   ANSI preserved) into a custom predicate still get clean predicate
   matches.
2. A future bypass that injects raw ANSI into `EvalContext.stdout`
   (e.g. test fixtures) cannot accidentally pass through unstripped.

The cost is one regex sub per assertion call; negligible compared to
PTY capture itself.

## Why `_named_callable` matters

The runner's JSONL log wrapper (T03.08 — `_wrap_expect_with_log`)
reads `expect_callable.__name__` to populate the `expect` field on
each `expect.start` / `expect.end` event. Closures default to
`__name__ == "_run"`; tagging them with `_named_callable("file", fn)`
keeps log events keyed by the primitive name rather than the inner
function name.

## Why `_timed_result` wraps the inner builder

Every primitive returns the same `(passed, message, details, failure)`
4-tuple from its `_build` closure and then constructs the
`ExpectResult` via `_timed_result(name, _build)`. Centralising the
timing here keeps `duration_sec` consistent across primitives (single
`time.monotonic()` bracket) and lets future per-primitive changes
focus on the predicate, not the wrapping.

## Forward-looking: when does this need to change?

* When FR-EXP2 (custom Python `expect_callable: "module:fn"`) lands —
  the loader will need to expose `Expect`-like contract validation so
  third-party callables can be plugged in without losing the JSONL
  event surface.
* When `Expect.jsonl` grows event-shape schemas — currently `filter` /
  `assert_each` / `assert_any` take arbitrary Python predicates, which
  works for in-process callers but breaks for pure-YAML manifests.
  A typed `match: {event: "PreToolUse"}` shorthand likely lands in
  T04.04 alongside the per-primitive coverage tests.
