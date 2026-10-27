# D-0073 — Evidence (T04.11)

## Test run

Executed `2026-05-21T21:03Z` against `master` (post-T04.10/T05.01/T05.02 landing):

```
$ uv run pytest tests/cli/eval/test_single_command.py -v
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0
collected 2 items

tests/cli/eval/test_single_command.py::test_single_command_local_runnability PASSED [ 50%]
tests/cli/eval/test_single_command.py::test_single_command_contract_is_documented PASSED [100%]

============================== 2 passed in 0.38s ===============================
```

Full pytest output: [`../../evidence/T04.11/pytest-output.txt`](../../evidence/T04.11/pytest-output.txt).

## Direct invocation evidence

The literal AC command also exits 0 on its own:

```
$ mkdir -p /tmp/eval-runs/t04_11_smoke
$ uv run superclaude eval run --suite real --eval E1 --output-dir /tmp/eval-runs/t04_11_smoke
$ echo $?
0
$ ls /tmp/eval-runs/t04_11_smoke
homes  per-eval  summary.json  summary.md  summary.yaml
```

`summary.md` records `1 passed, 0 failed, 0 skipped, 0 errored, 0 interrupted, 0 timeout`
for `E1 — auggie-first sticky lifecycle — set then clear`; `summary.json` parses
as a JSON object with the FR-RPT1 schema (run_id, counts, totals, evals[]).

## Acceptance criteria status

| AC | Status | Evidence |
|----|--------|----------|
| `tests/cli/eval/test_single_command.py` runs `uv run superclaude eval run --suite real --eval E1` and exits 0. | LANDED | `test_single_command_local_runnability` PASSED at `2026-05-21T21:03Z`; subprocess `returncode == 0` confirmed. |
| Test asserts presence of `summary.md` and `summary.json` under per-run directory. | LANDED | `SUMMARY_FILES` tuple in the test module enumerates both filenames; assertion loop verifies `.is_file()` + non-empty; both files observed on disk under `/tmp/eval-runs/t04_11_smoke/`. |
| No manual setup beyond `make dev` required (docstring records this). | LANDED | Module docstring §"Clean-host contract" + `test_single_command_contract_is_documented` guards. |
| `D-0073/spec.md` documents the clean-host contract. | LANDED | [`spec.md`](spec.md). |

## Notes

* The pre-E1 skip predicates from the initial authoring pass (T05.01 real.yaml
  missing, T05.02 E1 inputs missing, T04.10 helpers missing) have all resolved
  — `_resolve_skip_reason` now returns `None` and the literal-invocation test
  executes end-to-end.
* Wallclock is fast (~0.4s for the whole pytest module) because the current
  E1 body is the stub spec landed in T05.02 with `duration_sec=0.0`. The
  contract that FR-G6 pins (exit 0 + summary pair) is satisfied regardless
  of eval duration; once E1 gains a real Claude-driven body the smoke test
  will exercise the full subprocess path without modification.
* Schema fidelity of `summary.json` is owned by TEST-007 (T04.17); FR-G6
  only verifies the file is present, non-empty, and parses as a JSON object.
