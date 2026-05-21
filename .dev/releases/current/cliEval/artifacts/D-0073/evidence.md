# D-0073 — Evidence (T04.11)

## Test run

Executed `2026-05-20T15:50Z` against `fix/prd-path-resolution-and-templates`:

```
$ uv run pytest tests/cli/eval/test_single_command.py -v
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0
collected 2 items

tests/cli/eval/test_single_command.py::test_single_command_local_runnability SKIPPED
    (T05.02 deliverable eval E1 not yet present in suites/real.yaml;
     pre-E1 phase smoke uses a stub eval ...)
tests/cli/eval/test_single_command.py::test_single_command_contract_is_documented PASSED

========================= 1 passed, 1 skipped in 0.13s =========================
```

Full pytest output: [`../../evidence/T04.11/pytest-output.txt`](../../evidence/T04.11/pytest-output.txt).

## Acceptance criteria status

| AC | Status | Evidence |
|----|--------|----------|
| `tests/cli/eval/test_single_command.py` runs `uv run superclaude eval run --suite real --eval E1` and exits 0. | DEFERRED-TO-T05.02 | Test asserts exit 0 + summary files; skipped pre-E1 with precise reason. |
| Test asserts presence of `summary.md` and `summary.json` under per-run directory. | LANDED | `SUMMARY_FILES` tuple in the test module enumerates both filenames; assertion loop verifies `.is_file()` + non-empty. |
| No manual setup beyond `make dev` required (docstring records this). | LANDED | Module docstring §"Clean-host contract" + `test_single_command_contract_is_documented` guards. |
| `D-0073/spec.md` documents the clean-host contract. | LANDED | [`spec.md`](spec.md). |

## Notes

* Test SKIPPED is the correct pre-E1 posture per phase-4-tasklist.md §T04.11
  Notes ("pre-E1 phase smoke uses a stub eval"). The skip predicate
  re-activates the literal-invocation test the moment T04.10 helpers +
  T05.01 (real.yaml) + T05.02 (E1) land.
* T04.10's missing helpers are flagged in [`notes.md`](notes.md) §"Outstanding
  work surfaced" so the sprint runner can re-sequence; that scope is
  outside T04.11.
