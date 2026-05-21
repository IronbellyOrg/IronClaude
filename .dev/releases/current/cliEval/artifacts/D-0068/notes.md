# D-0068 — Implementation notes

## Why this task was test-only

T04.01 (D-0064) shipped the full `Expect.exit_code` body alongside the
package skeleton. The primitive already supported:

* Sentinel-aware default `equals=0` (so `Expect.exit_code()` works).
* Mutually-exclusive `equals` + `in_set` guard at construction time.
* `in_set` normalised to a `frozenset[int]` (accepts any iterable).
* `not_equals` composable with either `equals` or `in_set`.
* Failure payloads with `expected` / `actual` (DM-005).

T04.05's deliverable is the **per-primitive acceptance harness** that
touches every named argument and the sentinel-default invariant. No
body changes were required to `src/superclaude/cli/eval/expect.py`.

## Decisions

1. **Sentinel-aware `equals` default is the right call.** A naive
   `equals=0` default would trip the mutex guard on every
   `Expect.exit_code(in_set={0, 1})` invocation — the runtime cannot
   distinguish "caller passed equals=0" from "caller passed nothing and
   the default applied". The module-level `_SENTINEL` cleanly separates
   the two, and `test_default_equals_does_not_collide_with_in_set` pins
   the resulting invariant.
2. **`in_set` accepts any iterable, not just `set`.** YAML / JSON
   loaders emit lists; tests should not have to massage `list -> set`
   at the call site. The primitive does `frozenset(in_set)`
   internally, which is a single linear pass — cheap, and converts
   duplicates into the expected dedup behaviour. `test_in_set_accepts_list_input`
   and `test_in_set_accepts_tuple_input` pin both forms.
3. **Empty `in_set` is a permanent FAIL, not "skip the check."**
   A manifest that emits `in_set: []` is almost certainly a bug — the
   author meant to allow some codes but forgot to fill them in. The
   primitive treats it as an empty membership set (no exit code can
   satisfy it) so the FAIL surfaces immediately rather than the eval
   silently passing on every run. `test_in_set_empty_iterable_always_fails`
   pins it.
4. **Failure-message ordering is deterministic.** Both the `expected`
   payload and the human-readable message use `sorted(normalized_set)`
   so golden-log comparisons stay stable regardless of the caller's
   iteration order. `test_failure_message_includes_in_set_membership`
   pins the message form `"exit_code 9 not in [0, 1, 2]"`.
5. **`equals` check runs before `not_equals`.** When both are set and
   both would fail, the equals branch wins — the resulting failure is
   the more specific / informative one. `test_not_equals_combines_with_equals`
   pins this ordering by asserting that
   `Expect.exit_code(equals=0, not_equals=1)` against `exit_code=1`
   reports the equals mismatch, not the not_equals violation.

## Argument-space coverage rationale

The 3-argument signature has 7 non-empty combinations plus the
no-argument default = 8 states. Coverage by test:

| Combination | Pass test | Fail test |
|---|---|---|
| (none) — implicit equals=0 | test_default_passes_on_zero | test_default_fails_on_nonzero |
| equals only | test_equals_explicit_passes_on_match + test_equals_supports_nonzero_default_override | test_equals_explicit_fails_on_mismatch |
| in_set only | test_in_set_passes_when_member + test_in_set_accepts_list_input + test_in_set_accepts_tuple_input | test_in_set_fails_when_not_member + test_in_set_empty_iterable_always_fails |
| not_equals only | test_not_equals_passes_when_different | test_not_equals_fails_when_equal |
| equals + not_equals | test_not_equals_combines_with_equals (pass arm) | test_not_equals_combines_with_equals (fail arm) |
| in_set + not_equals | test_not_equals_combines_with_in_set (pass arm) | test_not_equals_combines_with_in_set (fail arm) |
| equals + in_set | n/a — raises ValueError | test_equals_and_in_set_raises_value_error |
| equals + in_set + not_equals | n/a — equals+in_set rejected first | n/a |

That accounts for every reachable combination. The declarative-form
tests (`test_from_mapping_threads_in_set` /
`test_from_mapping_threads_not_equals`) plus the envelope test
(`test_result_carries_primitive_name_and_timing`) round out the
manifest-side surface.

## Things explicitly not covered here

* **Non-int exit codes.** Python's `subprocess.Popen.returncode` only
  ever produces `int` (negative for signals, non-negative otherwise),
  so the primitive does not coerce or validate the type. A manifest
  that supplies `equals="0"` (string) would fail equality against the
  int, which is the correct behaviour — manifest authors should write
  integer literals.
* **Signal-derived exit codes (negative ints).** Negative codes pass
  through transparently; `Expect.exit_code(equals=-15)` would match a
  SIGTERM-killed subprocess. Not specifically tested because the FR-EXP1
  contract treats them like any other int — `subprocess.returncode`
  delivers the signed value and the primitive compares verbatim.
* **`in_set` containing non-int values.** Python's `set` membership
  short-circuits on type mismatch (`0 in {0.0}` is `True` by accident),
  but no manifest in the M5 inventory mixes types and the schema
  validator (T01.02) requires integer literals.

## Follow-ups

None. Downstream consumers (T05.02..T05.16, T04.19) wire `Expect.exit_code`
directly and pass without further changes.
