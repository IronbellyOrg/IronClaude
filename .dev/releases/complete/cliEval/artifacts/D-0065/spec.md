# D-0065 — `Expect.file` primitive spec (COMP-010.1)

**Task:** T04.02 (Phase 4, Roadmap R-065 / COMP-010.1)
**Module:** `src/superclaude/cli/eval/expect.py` — `Expect.file`
**Tests:** `tests/cli/eval/test_expect_file.py` (18 cases)
**Status:** Implemented 2026-05-20

## Signature

```python
Expect.file(
    *,
    path: str | Path,
    exists: Optional[bool] = None,
    contains: Optional[str] = None,
    regex: Optional[str] = None,
    equals: Optional[str] = None,
) -> ExpectCallable
```

All five named arguments are independent and may be combined. Returns an
`ExpectCallable = Callable[[EvalContext], ExpectResult]` (DM-009).

## Argument semantics

| Arg | Type | When set | Pass condition |
|---|---|---|---|
| `path` | `str | Path` | Always required | Resolves relative paths against `ctx.home_path` (DM-006); absolute paths used verbatim. |
| `exists` | `Optional[bool]` | Existence check | Filesystem `Path.exists()` matches the expected boolean. If `exists=False` and the file is absent, downstream content checks are short-circuited (PASS). |
| `contains` | `Optional[str]` | Substring check | The literal substring appears in the UTF-8 decoded body. |
| `regex` | `Optional[str]` | Pattern check | `re.compile(regex).search(content)` returns a match. Compiled once at primitive construction. |
| `equals` | `Optional[str]` | Exact-content check | UTF-8 body equals the expected string. Failure carries a unified diff in `details["diff"]`. |

Evaluation order inside the primitive:

1. `exists` (existence delta)
2. early return PASS when `exists=False` and file is absent
3. read body as UTF-8 with `errors="replace"`
4. `equals` (exact match) → unified diff on failure
5. `contains` (substring)
6. `regex` (compiled-pattern search)

The first failing check produces the `ExpectResult.failure` (DM-005); the
remaining checks are not evaluated.

## Diff format (AC contract)

On `equals` mismatch, the failure ExpectResult populates two surfaces:

* `result.details["diff"]` — unified-diff string produced by
  `difflib.unified_diff` with:
  * `fromfile = f"expected/{resolved_path}"`
  * `tofile   = f"actual/{resolved_path}"`
  * context = 3 lines (default)
* `result.failure.expected` / `result.failure.actual` — the raw expected
  string and the raw file body so a Reporter can re-render the diff at a
  different context-width.

Example failure diff (from `test_equals_fails_with_unified_diff_in_details`):

```diff
--- expected/.../x.txt
+++ actual/.../x.txt
@@ -1,3 +1,3 @@
 line one
-LINE TWO
+line two
 line three
```

## Failure payload (other branches)

* `exists` mismatch → `expected={"exists": <bool>}`, `actual={"exists": <bool>}`.
* `contains` miss → `expected={"contains": <substr>}`, `actual=<full body>`.
* `regex` miss → `expected={"regex": <pattern>}`, `actual=<full body>`.

This keeps the Reporter (T03.13) and Eval JSONL log (T03.05) free to
render content-aware diffs even for non-`equals` failures, without the
primitive paying the diff cost on every assertion.

## Path resolution invariants

* Absolute `path` arguments bypass `home_path` entirely.
* Relative `path` arguments resolve via `home_path / path` (DM-006).
* Resolution is performed at *callable invocation time*, not construction
  time, so a manifest authored once can run against multiple per-eval
  HOMEs.

## Test matrix (`tests/cli/eval/test_expect_file.py`)

| # | Test | Argument under test | Direction |
|---|---|---|---|
| 1 | `test_relative_path_resolves_under_home` | `path` | PASS |
| 2 | `test_absolute_path_is_used_verbatim` | `path` | PASS |
| 3 | `test_exists_true_passes_when_present` | `exists=True` | PASS |
| 4 | `test_exists_true_fails_when_missing` | `exists=True` | FAIL |
| 5 | `test_exists_false_passes_when_missing` | `exists=False` | PASS |
| 6 | `test_exists_false_fails_when_present` | `exists=False` | FAIL |
| 7 | `test_contains_passes_on_substring_hit` | `contains` | PASS |
| 8 | `test_contains_fails_on_substring_miss` | `contains` | FAIL |
| 9 | `test_contains_supports_utf8` | `contains` (UTF-8) | PASS |
| 10 | `test_regex_passes_on_match` | `regex` | PASS |
| 11 | `test_regex_fails_on_no_match` | `regex` | FAIL |
| 12 | `test_regex_matches_across_lines_via_search` | `regex` (search semantics) | PASS |
| 13 | `test_equals_passes_on_exact_match` | `equals` | PASS |
| 14 | `test_equals_fails_with_unified_diff_in_details` | `equals` + diff contract | FAIL |
| 15 | `test_contains_and_regex_both_evaluated` | combined | PASS + FAIL |
| 16 | `test_exists_true_with_contains_fails_when_substring_missing` | combined | FAIL |
| 17 | `test_no_assertions_passes_when_file_readable` | all-None | PASS |
| 18 | `test_result_carries_primitive_name_and_timing` | result envelope | PASS |

All 18 cases pass under `uv run pytest tests/cli/eval/test_expect_file.py -v`
in 0.18 s on 2026-05-20.

## Downstream consumers

* T05.02 E1 sticky-lifecycle eval — uses `Expect.file` to assert the
  hook-managed lifecycle file content after the session terminates.
* T05.10 matcher-coverage eval — uses `Expect.file(exists=True)` against
  per-matcher artifact paths emitted by the coverage gate.

## Linked roadmap entries

* R-065 — COMP-010.1 / D-0065
* Depends on: T04.01 (Expect package skeleton)
* Used by: T05.02 (E1), T05.10 (E9)
