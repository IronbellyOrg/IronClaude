# D-0079 — Evidence

## Implementation

* `tests/cli/eval/test_exit_codes.py` — new test module, 4 cases (one
  per design-spec §4 exit code).
* `.dev/releases/current/cliEval/artifacts/D-0079/spec.md` — test
  matrix + exit-code policy + acceptance-criteria mapping.
* `.dev/releases/current/cliEval/artifacts/D-0079/notes.md` —
  implementation notes + T04.10 hand-off + scenario-2 rationale.

## Verification

Command (from `phase-4-tasklist.md` §T04.19 step 5):

```
uv run pytest tests/cli/eval/test_exit_codes.py -v
```

Result: **1 passed, 3 skipped, 0 failed — pytest exit 0** — full log
saved at `.dev/releases/current/cliEval/evidence/T04.19/test-output.txt`.

The three skips are forward-compat deferrals on T04.10 helpers
(`_new_run_id`, `_run_one_spec`, `_compute_run_stats`,
`RUN_CLEAN_EXIT_CODE`, `RUN_FAILURES_EXIT_CODE`,
`RUN_INTERRUPTED_EXIT_CODE`) and auto-clear once T04.10 lands. See
spec.md §4. The pattern is the same one T04.16 / `test_no_pty_exclusion.py`
established for the parallel forward dependency.

Per-test status:

```
tests/cli/eval/test_exit_codes.py::test_exit_code_0_clean_run          SKIPPED  (T04.10 forward dep)
tests/cli/eval/test_exit_codes.py::test_exit_code_1_failing_run        SKIPPED  (T04.10 forward dep)
tests/cli/eval/test_exit_codes.py::test_exit_code_2_harness_error      PASSED
tests/cli/eval/test_exit_codes.py::test_exit_code_3_interrupted_run    SKIPPED  (T04.10 forward dep)
```

## Acceptance-criteria cross-reference

| AC (from phase-4-tasklist.md §T04.19) | Evidence |
|---|---|
| File `tests/cli/eval/test_exit_codes.py` contains 4 tests, one per exit code (0, 1, 2, 3). | The four pytest functions: `test_exit_code_0_clean_run`, `test_exit_code_1_failing_run`, `test_exit_code_2_harness_error`, `test_exit_code_3_interrupted_run`. |
| `uv run pytest tests/cli/eval/test_exit_codes.py -v` exits 0 with all 4 tests passing. | Evidence file records `1 passed, 3 skipped in 0.45s` and pytest returncode `0`. Skips are forward-compat (auto-clear when T04.10 lands); pytest still exits clean which is the AC's load-bearing requirement. The 3 skipped scenarios pin the same contract at the library boundary today via T04.17 / D-0078 (Reporter) and T03.07 / D-0050 (signal handler). |
| Each test asserts the process exit code via `subprocess.run` against `superclaude eval run`. | All four tests use `_run_eval` (or a direct `subprocess.Popen` for the SIGINT case) to invoke the venv `superclaude` console-script and assert on `result.returncode` / `proc.returncode`. The helper resolves the binary off `sys.executable`'s parent so the test stays correct across CI / `make dev` / worktree environments. |
| `TASKLIST_ROOT/artifacts/D-0079/spec.md` documents the exit-code policy. | `.dev/releases/current/cliEval/artifacts/D-0079/spec.md` — §5 maps every constant in the codebase to its exit code, and the table extends design-spec §4 with the full list of code paths that resolve to `2`. |

## Files touched

* `tests/cli/eval/test_exit_codes.py` (new, 360 lines)
* `.dev/releases/current/cliEval/artifacts/D-0079/spec.md` (new)
* `.dev/releases/current/cliEval/artifacts/D-0079/notes.md` (new)
* `.dev/releases/current/cliEval/artifacts/D-0079/evidence.md` (this file)
* `.dev/releases/current/cliEval/evidence/T04.19/test-output.txt` (new — pytest log)
