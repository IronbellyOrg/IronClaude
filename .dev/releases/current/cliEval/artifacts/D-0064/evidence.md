# D-0064 — Evidence

**Task:** T04.01
**Verification command:** `uv run pytest tests/cli/eval/test_expect_primitives.py -v`
**Result:** 27 passed in 0.14s (exit 0)

## Files

* `src/superclaude/cli/eval/expect.py` — new FR-EXP1 primitive package
  (Expect class with 7 static methods + `from_mapping` + module helpers).
* `src/superclaude/cli/eval/__init__.py` — re-exports `Expect`,
  `ExpectCallable`, `PRIMITIVE_NAMES`.
* `tests/cli/eval/test_expect_primitives.py` — 27 tests covering:
  - Surface (`PRIMITIVE_NAMES` enumeration + attribute presence).
  - Construction smoke (no `NotImplementedError`) for all 7 primitives.
  - Programmatic invocation pass + fail for every primitive.
  - Declarative invocation via `Expect.from_mapping` (equivalence,
    empty-kwargs, unknown primitive, multi-key, kwargs threading).
  - `exit_code` mutual-exclusion guard (`equals` + `in_set`).

## Acceptance criteria checks

| AC | Status |
|---|---|
| Module exports `Expect.file/jsonl/settings_json/exit_code/stderr/stdout/duration` | ✅ verified by `test_primitive_names_matches_attribute_surface` + parametrised construction test |
| None raise `NotImplementedError` | ✅ `test_primitive_construction_does_not_raise_notimplemented[*]` (7 cases) |
| ExpectCallable returns `ExpectResult` | ✅ programmatic pass tests assert isinstance + 6-field shape |
| Declarative + programmatic forms equivalent | ✅ `test_from_mapping_equivalent_to_programmatic_exit_code` |
| `exit_code` mutual-exclusion guard | ✅ `test_exit_code_rejects_equals_and_in_set_together` |

## Pytest transcript

See `.dev/releases/current/cliEval/evidence/T04.01/pytest-output.txt`.
