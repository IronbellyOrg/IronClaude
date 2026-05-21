# D-0066 — `Expect.jsonl` primitive spec (COMP-010.2)

**Task:** T04.03 (Phase 4, Roadmap R-066 / COMP-010.2)
**Module:** `src/superclaude/cli/eval/expect.py` — `Expect.jsonl`
**Tests:** `tests/cli/eval/test_expect_jsonl.py` (19 cases)
**Status:** Implemented 2026-05-20

## Signature

```python
Expect.jsonl(
    *,
    path: str | Path,
    line_count: Optional[int] = None,
    filter: Optional[Callable[[Mapping[str, Any]], bool]] = None,
    assert_each: Optional[Callable[[Mapping[str, Any]], bool]] = None,
    assert_any: Optional[Callable[[Mapping[str, Any]], bool]] = None,
) -> ExpectCallable
```

All four predicate arguments are independent and may be combined. Returns
an `ExpectCallable = Callable[[EvalContext], ExpectResult]` (DM-009).

## Argument semantics

| Arg | Type | When set | Pass condition |
|---|---|---|---|
| `path` | `str | Path` | Always required | First looked up in `ctx.jsonl_paths` (named registry — runner-provided). Falls back to `_resolve_path(ctx, path)`: relative paths resolve against `ctx.home_path` (DM-006); absolute paths used verbatim. |
| `line_count` | `Optional[int]` | Exact row count | The **filtered** row set has exactly this many entries. Blank / whitespace-only lines are skipped at parse time so a trailing newline is not counted. |
| `filter` | `Optional[predicate]` | Row narrowing | When set, `filtered = [r for r in rows if filter(r)]`; all subsequent assertions evaluate against this subset. |
| `assert_each` | `Optional[predicate]` | ∀ rows | Every row in the filtered set must return truthy from the predicate. Short-circuits on the first failing row. |
| `assert_any` | `Optional[predicate]` | ∃ row | At least one row in the filtered set must return truthy. Failure when the filtered set is empty or no row matches. |

Evaluation order inside the primitive:

1. Resolve `path` (named lookup → filesystem fallback).
2. FAIL early if the path does not exist (`expected={"exists": True}` payload).
3. Parse the file line-by-line, skipping blank lines. Invalid JSON on
   any line yields a structured FAIL (`expected="valid JSON per line"`,
   `actual=<raw line>`, message includes the line number).
4. Apply `filter` (or accept all rows when unset).
5. Check `line_count` (filtered length).
6. Check `assert_each` (short-circuits on first miss; records
   `details["row_index"]` and the offending row in `failure.actual`).
7. Check `assert_any` (FAIL if no row satisfies the predicate).

The first failing check produces the `ExpectResult.failure` (DM-005); the
remaining checks are not evaluated.

## Predicate signatures

All three predicates share the same shape:

```python
predicate: Callable[[Mapping[str, Any]], bool]
```

Each row is the deserialised JSON object for that line; primitive
callers must accept a mapping (not a class) so the same predicate works
for manifest-loaded rows (`dict`) and runner-emitted rows (potentially
`MappingProxyType`). Predicates are invoked under the same exception
contract as the rest of the primitive: an uncaught exception bubbles
out and is caught one level up by the runner's ExpectCallable harness
(T03.04), which records the failure with a traceback.

## Failure payload by branch

| Branch | `expected` | `actual` | `message` shape |
|---|---|---|---|
| Missing file | `{"exists": True}` | `{"exists": False}` | `"jsonl path <abs> does not exist"` |
| Invalid JSON line | `"valid JSON per line"` | `<raw line text>` | `"line <N> not valid JSON: <decoder error>"` (with `traceback` populated) |
| `line_count` mismatch | `{"line_count": <expected>}` | `{"line_count": <observed>}` | `"line_count expected <X> got <Y>"` |
| `assert_each` fail | `{"assert_each": "predicate true"}` | `<offending row mapping>` | `"assert_each failed at index <N>"`; `details["row_index"] = N` |
| `assert_any` empty | `{"assert_any": "any matching row"}` | `[<all filtered rows>]` | `"assert_any predicate satisfied by no row"` |

On the PASS path, `details` carries
`{"path": <resolved abs>, "rows_inspected": <len(filtered)>}` so the
Reporter can render the row count it actually exercised even when no
predicate was set.

## Path resolution invariants

* The named lookup (`ctx.jsonl_paths[path_str]`) takes precedence. This
  is how the runner advertises per-eval log files (`hook_log`,
  `claude_session_log`) without manifest authors having to know the
  on-disk path under the scratch HOME.
* When `path` is not a registered name, it falls back to filesystem
  resolution: absolute paths used verbatim; relative paths joined
  against `ctx.home_path` (DM-006).
* Resolution happens at *callable invocation time*, not construction,
  so one primitive can run against many EvalContexts (one per eval
  invocation).

## Hook-telemetry shape used by the test matrix

The acceptance test fixture mirrors the per-eval `hooks.jsonl` written
by HookAdapter (T02.16) / EvalRunner (T03.06):

```jsonl
{"event": "PreToolUse",  "matcher": "mcp__auggie__*",            "tool": "mcp__auggie__codebase-retrieval", "status": "allow",       "ts": 1}
{"event": "PostToolUse", "matcher": "mcp__auggie__*",            "tool": "mcp__auggie__codebase-retrieval", "status": "ok",          "ts": 2}
{"event": "PreToolUse",  "matcher": "mcp__airis-mcp-gateway__*", "tool": "mcp__airis-mcp-gateway__list",    "status": "allow",       "ts": 3}
{"event": "PostToolUse", "matcher": "mcp__airis-mcp-gateway__*", "tool": "mcp__airis-mcp-gateway__list",    "status": "ok",          "ts": 4}
{"event": "Stop",        "matcher": null,                        "tool": null,                              "status": "session_end", "ts": 5}
```

E1 (sticky-lifecycle, T05.02) and E2.x (matcher-coverage, T05.10) use
this exact shape with `Expect.jsonl` to assert hook invariants.

## Test matrix (`tests/cli/eval/test_expect_jsonl.py`)

| # | Test | Argument under test | Direction |
|---|---|---|---|
| 1 | `test_named_path_resolves_via_jsonl_paths` | `path` (named lookup) | PASS |
| 2 | `test_relative_path_resolves_under_home` | `path` (relative fallback) | PASS |
| 3 | `test_absolute_path_is_used_verbatim` | `path` (absolute) | PASS |
| 4 | `test_missing_file_fails_with_existence_payload` | `path` (missing) | FAIL |
| 5 | `test_line_count_passes_on_exact_match` | `line_count` | PASS |
| 6 | `test_line_count_fails_on_mismatch` | `line_count` | FAIL |
| 7 | `test_line_count_zero_passes_on_empty_jsonl` | `line_count=0` | PASS |
| 8 | `test_line_count_ignores_blank_lines` | parser robustness | PASS |
| 9 | `test_filter_narrows_rows_before_line_count` | `filter` + `line_count` | PASS |
| 10 | `test_filter_to_zero_rows_passes_with_count_zero` | `filter` (empty result) | PASS |
| 11 | `test_assert_each_passes_when_all_rows_match` | `assert_each` (∀) | PASS |
| 12 | `test_assert_each_fails_on_first_mismatch` | `assert_each` (∀) | FAIL |
| 13 | `test_assert_any_passes_when_one_row_matches` | `assert_any` (∃) | PASS |
| 14 | `test_assert_any_fails_when_no_row_matches` | `assert_any` (∃) | FAIL |
| 15 | `test_assert_any_runs_against_filtered_subset` | `filter` + `assert_any` | FAIL |
| 16 | `test_invalid_json_line_fails_with_lineno` | parser error path | FAIL |
| 17 | `test_no_assertions_passes_when_file_parsable` | all-None | PASS |
| 18 | `test_combined_filter_line_count_assert_each` | combined | PASS |
| 19 | `test_result_carries_primitive_name_and_timing` | result envelope | PASS |

All 19 cases pass under `uv run pytest tests/cli/eval/test_expect_jsonl.py -v`
in 0.15 s on 2026-05-20.

## Downstream consumers

* T05.02 E1 sticky-lifecycle eval — asserts the hook JSONL contains a
  matching PreToolUse / PostToolUse pair per `mcp__auggie__*` invocation
  via `Expect.jsonl(path="hook_log", filter=..., assert_each=...)`.
* T05.10 E2.x matcher-coverage evals — assert per-matcher row counts and
  presence of `status="allow"` rows for each declared matcher pattern.

## Linked roadmap entries

* R-066 — COMP-010.2 / D-0066
* Depends on: T04.01 (Expect package skeleton)
* Used by: T05.02 (E1), T05.10 (E2.x)
