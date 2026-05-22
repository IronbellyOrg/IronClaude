# A2 Branch Trace — Reachability of `eval_run` exits before first `NameError`

**Subject:** `src/superclaude/cli/eval/commands.py::eval_run` (def @ line 1406)
**First NameError site:** **line 1467** (`run_id = _new_run_id()`).
**Invocation under test:** `superclaude eval run --suite real` (defaults for every other flag).
**Question for each branch:** Does the operator-facing happy-path invocation reach this branch BEFORE line 1467? If a branch fires, it short-circuits the run with a non-NameError exit, which would mask the defect for that path.

The expected-branches list (19 lines) at
`.dev/reviews/2026-05-21-cliEval-runner-symbols-investigation/artifacts/expected-branches-extended.txt`
is enumerated below; each row was verified against the verbatim source
shown in the Read of `commands.py:1406-1695`.

| Line | Condition (verbatim or paraphrased) | Pre-NameError? | Fires on `--suite real` default invocation? | SUFFICIENCY-BLOCKER? |
|------|-------------------------------------|----------------|---------------------------------------------|----------------------|
| 1453 | `if timeout_mult <= 0:` (then `sys.exit(HARD_FAIL_EXIT_CODE)`) | YES (before 1467) | NO — default `timeout_mult` is `> 0` (`@click.option(..., default=1.0)` per FR-CLI1) | NO — only fires on bad flag value the operator supplied |
| 1461 | `if max_disk_mb < 0:` (then `sys.exit(HARD_FAIL_EXIT_CODE)`) | YES (before 1467) | NO — default `max_disk_mb` is `>= 0` | NO — only fires on bad flag value the operator supplied |
| 1479 | `except ScratchRootViolation:` → `sys.exit(SCRATCH_ROOT_VIOLATION_EXIT_CODE)` | NO — body is at lines 1472-1477, which executes AFTER line 1467 already ran (`_new_run_id()` is called at 1467, then `_default_output_dir(run_id)` at 1469, then `resolve_scratch_root(...)` at 1473). The first NameError lands at 1467 long before this branch could fire. | NO | NO |
| 1480 | `sys.exit(SCRATCH_ROOT_VIOLATION_EXIT_CODE)` (the exit inside the same handler) | NO (see 1479) | NO | NO |
| 1507 | `except SuiteNotFound:` → `click.echo(...)` at suite resolution (line 1504-1505) | NO — `resolve_suite_manifest` is called at 1505, AFTER 1467/1469. Unreachable due to prior NameError. | NO | NO |
| 1508 | `sys.exit(SUITE_NOT_FOUND_EXIT_CODE)` | NO (same) | NO | NO |
| 1514 | `except SuiteLoaderError:` → `click.echo(...)` at loader.load (line 1512) | NO — same reason. Unreachable. | NO | NO |
| 1515 | `sys.exit(SUITE_LOADER_ERROR_EXIT_CODE)` | NO | NO | NO |
| 1529 | `sys.exit(EVAL_NOT_FOUND_EXIT_CODE)` inside the `if missing:` arm at line 1523 (only fires if `--eval` was passed AND id is missing) | NO — at line 1523, far past 1467. Unreachable. | NO (and default invocation passes no `--eval`) | NO |
| 1547 | `click.echo(_format_coverage_missing_roster(coverage), err=True)` (coverage-gate failure render) | NO — `coverage_gate(...)` is called at 1541, far past 1467 | NO | NO |
| 1548 | `sys.exit(COVERAGE_GATE_FAILED_EXIT_CODE)` | NO | NO | NO |
| 1587-1597 | `return EvalOutcome(...)` inside the inner `run_one` closure's `if no_pty and spec.no_pty == "skip":` branch | NO — `run_one` is defined at line 1579 but only INVOKED via the orchestrator (line 1626). The orchestrator call is at 1626, far past 1467. Even if the closure were callable, the NameErrors at 1467/1469/1577 (`_resolve_executor_factory()`) all fire first. | NO | NO |
| 1598 | `return _run_one_spec(...)` (second NameError site inside `run_one` closure) | NO — same: closure is only entered via the orchestrator at 1626, which is unreachable | NO (additional NameError, but downstream of the first) | NO |
| 1633 | `except ValueError as exc:` → `click.echo(...)` (orchestrator rejected request) at lines 1621-1634 wrapping the orchestrator.run call | NO — orchestrator.run is at 1626; the wrapping `try` starts at 1621, which is past 1467 / 1469 / 1577 / 1612 / 1624 | NO | NO |
| 1634 | `sys.exit(HARD_FAIL_EXIT_CODE)` (the exit inside that handler) | NO | NO | NO |
| 1677 | `sys.exit(RUN_INTERRUPTED_EXIT_CODE)` inside `if token.is_cancelled():` (line 1676) | NO — at 1676, past every helper invocation. **Also itself a NameError site** (`RUN_INTERRUPTED_EXIT_CODE` is one of the 11 undefined symbols). | NO | NO |
| 1687-1688 | `click.echo(DISK_BUDGET_RETENTION_ADVICE, err=True)` + `sys.exit(DISK_BUDGET_EXCEEDED_EXIT_CODE)` inside `if poller.is_breached():` (line 1678) | NO — at 1678, past every helper invocation | NO | NO |
| 1694 | `sys.exit(RUN_FAILURES_EXIT_CODE)` (one of the 11 undefined names) | NO | NO | NO |
| 1695 | `sys.exit(RUN_CLEAN_EXIT_CODE)` (one of the 11 undefined names) | NO | NO | NO |

## Coverage tally

- **19 of 19** expected branches traced.
- **2 of 19** are pre-NameError exits (lines 1453, 1461). Both are
  defensive flag-validation guards that fire only when the operator
  supplies a *bad* `--timeout-mult` or a *bad* `--max-disk-mb`. The
  default values of those flags do NOT trigger them.
- **17 of 19** are downstream of line 1467 and therefore unreachable
  on any invocation that raises the first `NameError`.

## SUFFICIENCY-BLOCKERS

**None.** No branch in the 19-row expected list short-circuits the
default `eval run --suite real` invocation before the
`_new_run_id` NameError at line 1467 fires. The two pre-NameError
guards (1453, 1461) only fire on operator-supplied flag-value errors,
not on the happy path. This confirms the canonical reproduction:

```
File "src/superclaude/cli/eval/commands.py", line 1467, in eval_run
    run_id = _new_run_id()
             ^^^^^^^^^^^
NameError: name '_new_run_id' is not defined
```

is the FIRST symptom an operator would see on any
default-flag invocation. CP-P05-END.md transcribes the live capture
(`evidence/T05.28/eval-run-parallel-8.log`) at line 33 with the same
NameError stack — independent confirmation against the on-disk source.

## Sub-finding for the adversaries

The `eval_run --help` surface PASSES (per CP-P04-END.md row T04.10:
"`uv run superclaude eval run --help` renders them
(`evidence/T04.22/eval-run-help.txt`)") because Click's decorator stack
(commands.py:1304-1404, twelve `@click.option(...)` decorators above
`def eval_run`) is parsed at module-import time, while the function
*body* is only executed on actual invocation. This is precisely why
the defect slipped past `eval --help` smoke tests: the decorator
stack's correctness creates a false sense of liveness that masks the
fact that none of the body's helper calls can resolve.
