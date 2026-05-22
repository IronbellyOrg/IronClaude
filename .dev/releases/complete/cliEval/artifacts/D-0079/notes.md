# D-0079 — Implementation notes

## Module-level decisions

* **Console-script over `python -m`.** The package has no
  `__main__.py`; the hatchling-generated `superclaude` console-script
  is the operator-visible surface. `_resolve_superclaude_bin()`
  resolves it off `sys.executable`'s parent, so any venv layout (CI,
  `make dev`, ephemeral worktrees) finds the binary. If neither the
  venv binary nor `shutil.which("superclaude")` resolves, the module
  skips at import time with a diagnostic — the tests are about the
  CLI shim's behaviour, so running them against a missing shim would
  prove nothing.

* **Forward-compat skip mirrors `test_no_pty_exclusion.py` (T04.16).**
  The exit-code-2 path is independent of T04.10; the 0 / 1 / 3 paths
  are not. Rather than block this deliverable on T04.10 we use the
  same skip-when-deps-missing pattern T04.16 established for the
  parallel forward dependency. `_skip_unless_t0410_landed()` checks
  for six T04.10 names and emits `pytest.skip(...)` with the missing
  set inline so the diagnostic is actionable on its own. The skip
  evaporates automatically once T04.10 adds the helpers, no edits
  needed here.

* **Two harness-error gates, not one.** Scenario 3 asserts the
  exit-code-2 contract through `--timeout-mult 0` *and*
  `--max-disk-mb -1`. Both gates land at `HARD_FAIL_EXIT_CODE` but
  through independent code paths (`commands.py:1398` vs `:1405`), so
  a future refactor that breaks one without the other is still
  caught. The test also pins `"--timeout-mult"` / `"--max-disk-mb"`
  in stderr so the operator-visible diagnostic stays present.

* **Library boundary constant + process boundary `returncode`
  asserted together.** Scenarios 3 and 4 each assert the
  module-level constant (`HARD_FAIL_EXIT_CODE`, `EXIT_INTERRUPTED`)
  equals the integer named by design-spec §4, *and* the subprocess
  `returncode` matches. The constant test guards against a rename;
  the `returncode` test guards against a wiring break. Holding both
  in the same test means a future change that loses either contract
  fails here loudly rather than appearing as a flake.

## Exit-code map at a glance

```
0 — RUN_CLEAN_EXIT_CODE                  (T04.10 closure → sys.exit)
1 — RUN_FAILURES_EXIT_CODE               (T04.10 closure → sys.exit)
2 — HARD_FAIL_EXIT_CODE                  (commands.py:1398, :1405 etc.)
    SUITE_NOT_FOUND_EXIT_CODE            (commands.py:1458)
    SUITE_LOADER_ERROR_EXIT_CODE         (commands.py:1465)
    EVAL_NOT_FOUND_EXIT_CODE             (commands.py:1479)
    COVERAGE_GATE_FAILED_EXIT_CODE       (commands.py:1498)
    SCRATCH_ROOT_VIOLATION_EXIT_CODE     (commands.py:1430)
    DISK_BUDGET_EXCEEDED_EXIT_CODE       (T04.10 closure)
    REPORTER_CONTRACT_VIOLATION_EXIT_CODE (run_report.py — T04.10 catches)
    RUN_BODY_DEFERRED_EXIT_CODE          (commands.py:1229 — transitional)
3 — RUN_INTERRUPTED_EXIT_CODE / EXIT_INTERRUPTED (T03.07 signal_handler)
```

## Hand-off to T04.10

Once T04.10 lands the missing run-loop helpers, the three currently
skipped tests un-skip automatically. T04.10's acceptance criteria
should include `uv run pytest tests/cli/eval/test_exit_codes.py -v`
showing **4 passed, 0 skipped** as a smoke gate for the run-loop
wiring. If any of the three skips fail to clear, T04.10 has missed a
forward dep.

## Why scenario 2 leans on a synthetic suite

Authoring the failing-run case against a real failing eval would
couple this test to one of the E1-E15 specs, which are in turn
authored against the production CLI surface. A future tweak that
makes the chosen real eval pass would silently make this test green
for the wrong reason. The synthetic suite is deliberately
self-contained: a one-spec YAML with an `expect: exit_code 9999` that
no plausible Claude subprocess will ever satisfy. The test pins the
*exit-code mapping*, not any particular eval's contents.
