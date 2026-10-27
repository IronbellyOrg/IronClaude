# D-0067 — `Expect.settings_json` primitive spec (COMP-010.3)

**Task:** T04.04 (Phase 4, Roadmap R-067 / COMP-010.3)
**Module:** `src/superclaude/cli/eval/expect.py` — `Expect.settings_json`
**Tests:** `tests/cli/eval/test_expect_settings_json.py` (21 cases)
**Status:** Implemented 2026-05-20

## Signature

```python
Expect.settings_json(
    *,
    path: str | Path,
    key_path: str,
    equals: Any = _SENTINEL,
    exists: Optional[bool] = None,
) -> ExpectCallable
```

All four named arguments are keyword-only. Returns an
`ExpectCallable = Callable[[EvalContext], ExpectResult]` (DM-009).

The default for `equals` is the module-level sentinel `_SENTINEL` (not
`None`), so manifests can legitimately assert `equals=None` against a
JSON null value without colliding with the "no equals argument" default.

## Argument semantics

| Arg | Type | When set | Pass condition |
|---|---|---|---|
| `path` | `str | Path` | Always required | Resolves relative paths against `ctx.home_path` (DM-006 / NFR-ISO1); absolute paths are used verbatim. |
| `key_path` | `str` | Always required | Dot-separated traversal expression (e.g. `"hooks.PreToolUse.matchers"`). Each segment indexes a dict; non-dict intermediates short-circuit traversal. |
| `equals` | `Any` (sentinel default) | Strict equality | Resolved value `== equals` (Python equality semantics, applied to the JSON-decoded payload — so list/dict comparisons are deep). |
| `exists` | `Optional[bool]` | Presence check | `True` requires the key_path resolve successfully; `False` requires it to be absent. |

## Path resolution (NFR-ISO1 contract)

The path argument *always* resolves through the helper
`_resolve_path(ctx, path)`:

* Absolute paths are returned unmodified.
* Relative paths are joined to `ctx.home_path` (the per-eval scratch
  HOME created by `HomeIsolation`, T02.11).

This means a manifest written as
`{settings_json: {path: "settings.json", key_path: "hooks.matchers", equals: [...]}}`
asserts against the per-eval scratch `settings.json`, *not* the real
`~/.claude/settings.json` on the host. The
`test_resolution_isolated_from_real_home` test pins this invariant by
asserting only against a scratch-only marker key and confirming
`result.details["path"]` starts with the scratch HOME prefix.

## `key_path` traversal rules

The traversal walks each dot-separated segment via `value[segment]` when
the current value is a `collections.abc.Mapping`. If any of:

1. `value` is not a Mapping (e.g. a string, list, scalar), OR
2. `segment` is not a key of the current mapping,

then traversal short-circuits with `found=False` and `value=None`. This
mirrors the "absent key" semantics from `Path.get(...)` style helpers and
prevents traversal from raising `TypeError` on schema drift.

Edge cases pinned by tests:

* `test_key_path_short_circuits_on_missing_intermediate` — traversing
  `hooks.PreToolUse.matchers` against `{"hooks": {}}` yields `found=False`.
* `test_key_path_into_non_mapping_value` — traversing `hooks.PreToolUse`
  against `{"hooks": "not-a-dict"}` yields `found=False` (no exception).

## Evaluation order

Inside the callable:

1. Resolve `path`; if the file is missing → FAIL with
   `expected={"settings_json_present": True}` / `actual={"settings_json_present": False}`.
2. Parse JSON; on parse error → FAIL with `expected="valid JSON"` and the
   raw body in `actual`, plus the `JSONDecodeError` traceback.
3. Walk `key_path` to compute `(found, value)`.
4. If `exists is not None` and `found != bool(exists)` → FAIL with
   `expected={"key_path": <kp>, "exists": <bool>}` and corresponding
   `actual`.
5. If `equals is not _SENTINEL`:
   * If `not found` → FAIL with `expected=<equals>`, `actual=None`,
     message `"key_path <kp> missing; cannot compare"`.
   * Else if `value != equals` → FAIL with `expected=<equals>`,
     `actual=<value>`.
6. Otherwise PASS with `details={"path": ..., "key_path": <kp>, "found": <bool>}`.

The first failing check produces the `ExpectResult.failure` (DM-005);
remaining checks are not evaluated.

## Failure payload

| Branch | `expected` | `actual` | Notes |
|---|---|---|---|
| settings.json missing | `{"settings_json_present": True}` | `{"settings_json_present": False}` | |
| JSON parse error | `"valid JSON"` | raw body (UTF-8, `errors="replace"`) | `failure.traceback` populated with the `JSONDecodeError`. |
| `exists` mismatch | `{"key_path": <kp>, "exists": <bool>}` | `{"key_path": <kp>, "exists": <bool>}` | |
| `equals` missing key | `<equals>` | `None` | Distinguishes "absent" from "present but None" via the sentinel. |
| `equals` value mismatch | `<equals>` | resolved value | |

## Test matrix (`tests/cli/eval/test_expect_settings_json.py`)

| # | Test | Argument under test | Direction |
|---|---|---|---|
| 1 | `test_relative_path_resolves_against_home_path` | `path` (relative) | PASS |
| 2 | `test_absolute_path_is_used_verbatim` | `path` (absolute) | PASS |
| 3 | `test_resolution_isolated_from_real_home` | NFR-ISO1 invariant | PASS |
| 4 | `test_missing_settings_file_fails` | `path` (absent file) | FAIL |
| 5 | `test_key_path_navigates_nested_dicts` | `key_path` (nested) | PASS |
| 6 | `test_key_path_top_level_key` | `key_path` (single) | PASS |
| 7 | `test_key_path_short_circuits_on_missing_intermediate` | `key_path` (missing intermediate) | FAIL |
| 8 | `test_key_path_into_non_mapping_value` | `key_path` (into non-mapping) | PASS (`exists=False`) |
| 9 | `test_exists_true_passes_when_key_present` | `exists=True` | PASS |
| 10 | `test_exists_true_fails_when_key_absent` | `exists=True` | FAIL |
| 11 | `test_exists_false_passes_when_key_absent` | `exists=False` | PASS |
| 12 | `test_exists_false_fails_when_key_present` | `exists=False` | FAIL |
| 13 | `test_equals_passes_on_scalar_value` | `equals` (int) | PASS |
| 14 | `test_equals_fails_on_scalar_mismatch` | `equals` (int) | FAIL |
| 15 | `test_equals_supports_list_values` | `equals` (list, ordered) | PASS |
| 16 | `test_equals_supports_dict_values` | `equals` (dict, deep) | PASS |
| 17 | `test_equals_distinguishes_null_from_unset` | `equals=None` (sentinel) | PASS |
| 18 | `test_equals_fails_when_key_path_missing` | `equals=None` + missing kp | FAIL |
| 19 | `test_exists_true_and_equals_both_evaluated` | combined | PASS + FAIL |
| 20 | `test_invalid_json_payload_fails` | malformed JSON | FAIL |
| 21 | `test_result_carries_primitive_name_and_timing` | result envelope | PASS |

All 21 cases pass under
`uv run pytest tests/cli/eval/test_expect_settings_json.py -v` in 0.15 s
on 2026-05-20.

## Downstream consumers

* T05.10 / E9 matcher-coverage eval — asserts every hook matcher in
  `~/.claude/settings.json` resolves to a covering eval.
* T04.14 FR-G5 coverage gate — re-uses the same `settings.json` shape
  contract; `Expect.settings_json` is the manifest-level companion.

## Linked roadmap entries

* R-067 — COMP-010.3 / D-0067
* Depends on: T04.01 (Expect package skeleton), T02.11 (HomeIsolation.home_path)
* Used by: T04.14 (coverage gate), T05.10 (E9)
