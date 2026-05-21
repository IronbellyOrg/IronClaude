# D-0068 — `Expect.exit_code` primitive spec (COMP-010.4)

**Task:** T04.05 (Phase 4, Roadmap R-068 / COMP-010.4)
**Module:** `src/superclaude/cli/eval/expect.py` — `Expect.exit_code`
**Tests:** `tests/cli/eval/test_expect_exit_code.py` (20 cases)
**Status:** Implemented 2026-05-20

## Signature

```python
Expect.exit_code(
    equals: Any = _SENTINEL,            # default behaviour: equals=0
    in_set: Optional[Iterable[int]] = None,
    not_equals: Optional[int] = None,
) -> ExpectCallable
```

Arguments are positional-or-keyword (matching the M1 stub interface and
the YAML mapping form `{exit_code: {equals: 0}}`). The returned callable
has type `ExpectCallable = Callable[[EvalContext], ExpectResult]` (DM-009).

The default for `equals` is the module-level sentinel `_SENTINEL` (not
`0`) so the primitive can distinguish three states at construction time:

| State | Detection | Behaviour |
|---|---|---|
| Implicit equals (no args, default applies) | `equals is _SENTINEL`, `in_set is None` | `effective_equals = 0` |
| Explicit equals | `equals is not _SENTINEL` | `effective_equals = equals`; mutex with `in_set` |
| `in_set` only | `in_set is not None`, `equals is _SENTINEL` | `in_set` wins; no equals check |

This sentinel-aware default is what makes
`Expect.exit_code(in_set={0, 1})` legal: a naive `equals=0` default
would trip the mutual-exclusion guard on every `in_set` call.

## Argument semantics

| Arg | Type | When set | Pass condition |
|---|---|---|---|
| `equals` | `int` (sentinel default) | Strict equality | `ctx.exit_code == equals`. Default `equals=0` applies only when neither `equals` nor `in_set` is supplied. |
| `in_set` | `Iterable[int]` | Membership | `ctx.exit_code` is a member of the normalised `frozenset(in_set)`. Accepts `set`, `list`, `tuple`, or any other iterable of ints. |
| `not_equals` | `Optional[int]` | Negative equality | `ctx.exit_code != not_equals`. Composable with either `equals` or `in_set`. |

## Mutual-exclusion guard

`equals` and `in_set` are mutually exclusive *only when `equals` is set
explicitly*. Supplying both at construction time raises:

```python
ValueError("Expect.exit_code: 'equals' and 'in_set' are mutually exclusive")
```

`not_equals` is never mutually exclusive with the other two arguments.

## Evaluation order

Inside the callable, given `code = ctx.exit_code`:

1. If `in_set` is set:
   - If `code not in normalized_set` → FAIL with
     `expected={"in_set": sorted(normalized_set)}`, `actual=code`,
     message `f"exit_code {code} not in {sorted(normalized_set)}"`.
   - Else fall through to step 3.
2. Else if `effective_equals is not None` and `code != effective_equals`:
   - FAIL with `expected=effective_equals`, `actual=code`,
     message `f"exit_code expected {effective_equals} got {code}"`.
3. If `not_equals is not None` and `code == not_equals`:
   - FAIL with `expected={"not_equals": not_equals}`, `actual=code`,
     message `f"exit_code expected != {not_equals}, got {code}"`.
4. Otherwise PASS with `details={"actual": code}`, message
   `f"exit_code={code}"`.

The first failing check produces the `ExpectResult.failure` (DM-005);
the `not_equals` guard is only reached when the equals/in_set branch
passed, so `Expect.exit_code(equals=0, not_equals=1)` against
`exit_code=1` reports the *equals mismatch*, not the not_equals
violation. `test_not_equals_combines_with_equals` pins this ordering.

## Failure payload

| Branch | `expected` | `actual` | Message |
|---|---|---|---|
| `in_set` mismatch | `{"in_set": sorted([...])}` | `int` | `exit_code {code} not in {sorted([...])}` |
| `equals` mismatch | `int` | `int` | `exit_code expected {N} got {code}` |
| `not_equals` violation | `{"not_equals": N}` | `int` | `exit_code expected != {N}, got {code}` |

`sorted(normalized_set)` is used in both the `expected` payload and the
message so golden-log comparisons stay deterministic regardless of the
caller's iteration order. `test_failure_message_includes_in_set_membership`
pins the deterministic-ordering invariant.

## Empty `in_set` behaviour

An empty `in_set` (e.g. `set()`, `[]`) is treated as a permanent FAIL
rather than degenerating to "no check applied". This avoids the trap
where a manifest mistakenly emits an empty list and silently passes.
`test_in_set_empty_iterable_always_fails` pins it.

## Test matrix (`tests/cli/eval/test_expect_exit_code.py`)

| # | Test | Argument under test | Direction |
|---|---|---|---|
| 1 | `test_default_passes_on_zero` | implicit `equals=0` | PASS |
| 2 | `test_default_fails_on_nonzero` | implicit `equals=0` | FAIL |
| 3 | `test_equals_explicit_passes_on_match` | `equals` (int) | PASS |
| 4 | `test_equals_explicit_fails_on_mismatch` | `equals` (int) | FAIL |
| 5 | `test_equals_supports_nonzero_default_override` | `equals` (137) | PASS |
| 6 | `test_in_set_passes_when_member` | `in_set` (set) | PASS |
| 7 | `test_in_set_fails_when_not_member` | `in_set` (set) | FAIL |
| 8 | `test_in_set_accepts_list_input` | `in_set` (list) | PASS |
| 9 | `test_in_set_accepts_tuple_input` | `in_set` (tuple) | PASS |
| 10 | `test_in_set_empty_iterable_always_fails` | `in_set=set()` | FAIL |
| 11 | `test_not_equals_passes_when_different` | `not_equals` | PASS |
| 12 | `test_not_equals_fails_when_equal` | `not_equals` | FAIL |
| 13 | `test_not_equals_combines_with_in_set` | combined | PASS + FAIL |
| 14 | `test_not_equals_combines_with_equals` | combined | PASS + FAIL |
| 15 | `test_equals_and_in_set_raises_value_error` | mutex guard | raises |
| 16 | `test_default_equals_does_not_collide_with_in_set` | sentinel invariant | PASS |
| 17 | `test_from_mapping_threads_in_set` | declarative form | PASS |
| 18 | `test_from_mapping_threads_not_equals` | declarative form | PASS |
| 19 | `test_result_carries_primitive_name_and_timing` | DM-009 envelope | PASS |
| 20 | `test_failure_message_includes_in_set_membership` | message determinism | FAIL |

All 20 cases pass under
`uv run pytest tests/cli/eval/test_expect_exit_code.py -v` in 0.17 s
on 2026-05-20.

## Downstream consumers

`Expect.exit_code` is the most common Expect across the M5 eval suite —
every eval that drives the Claude subprocess via the PTY harness asserts
the exit code as the first line of its `expects:` block. Specifically:

* T05.02 (E1, sticky lifecycle) — `Expect.exit_code(equals=0)`.
* T05.03..T05.16 (E2..E15) — default-form `Expect.exit_code()` covers
  the implicit zero-exit happy path; the matcher-coverage and capability
  evals also use the `not_equals` form to confirm error paths.
* T04.19 (TEST-008 exit-code semantics) — reuses `Expect.exit_code` to
  drive the process-boundary exit-code matrix (0/1/2/3).

## Linked roadmap entries

* R-068 — COMP-010.4 / D-0068
* Depends on: T04.01 (Expect package skeleton, D-0064)
* Used by: T05.02..T05.16 (eval suite), T04.19 (TEST-008)
