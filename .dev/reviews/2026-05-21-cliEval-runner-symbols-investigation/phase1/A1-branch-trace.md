# A1 — Rule 2.5 Branch Trace for `eval_run` (commands.py:1406–1695)

**Source-of-truth file:** `src/superclaude/cli/eval/commands.py` (current
on-disk state; 60 914 bytes; mtime 2026-05-20 23:08).
**Expected-branches reference:**
`.dev/reviews/2026-05-21-cliEval-runner-symbols-investigation/artifacts/expected-branches-extended.txt`.

**Runtime scenario being traced:** `superclaude eval run --suite real`
(no `--eval` filter, default flags, real fixtures present).

**First-NameError site:** line **1467** (`run_id = _new_run_id()`). Any
branch *strictly before* line 1467 is reachable before the NameError;
any branch at-or-after line 1467 is only reachable if the
NameError-throwing call is mocked or the helper is wired.

---

## Branch-by-branch trace

Each row cites the line, the verbatim triggering condition (from
`commands.py`), and whether a real-fixture `eval run --suite real`
invocation would hit the branch BEFORE the line-1467 NameError. Rows
flagged **SUFFICIENCY-BLOCKER** are branches whose existence as-an-exit-
path before the NameError means runtime cannot reach the NameError on
that input — they "filter out the failure path."

> **Note on line-number reconciliation.** The expected-branches file
> references the historical ruff log line numbers (e.g. 1453, 1467,
> 1479, 1480, 1507, 1508, 1514, 1515, 1529, 1547, 1548, 1577, 1587,
> 1598, 1612, 1624, 1633, 1634, 1636, 1677, 1687, 1688, 1694, 1695).
> The expected-branches file at `artifacts/expected-branches-extended.txt`
> mixes both numbering ranges. The trace below uses **current on-disk
> line numbers** and notes any reconciliation.

| # | Current line | Verbatim triggering condition | Branch type | Reached BEFORE line-1467 NameError? | SUFFICIENCY-BLOCKER? |
|---|---|---|---|---|---|
| 1 | **1453** | `sys.exit(HARD_FAIL_EXIT_CODE)` inside `if timeout_mult <= 0:` (line 1448) | Early-exit (HARD_FAIL=2) | **Yes** — runs at line 1448 BEFORE line 1467. Default CLI value of `--timeout-mult` is positive (defined upstream at decorator line ~1380), so default invocation does NOT trigger. | **Yes — SUFFICIENCY-BLOCKER** *only when the operator passes `--timeout-mult 0` or negative*. For default invocations the branch is reachable in theory but NOT taken in practice. |
| 2 | **1461** | `sys.exit(HARD_FAIL_EXIT_CODE)` inside `if max_disk_mb < 0:` (line 1455) | Early-exit (HARD_FAIL=2) | **Yes** — runs at line 1455 BEFORE line 1467. Default `--max-disk-mb` is `DEFAULT_DISK_BUDGET_MB` (positive), so default invocation does NOT trigger. | **Yes — SUFFICIENCY-BLOCKER** only when operator passes `--max-disk-mb -1`. Not taken on default invocations. |
| 3 | **1467** | `run_id = _new_run_id()` — **first NameError** | NameError (no branch) | **N/A** — this IS the failure site. | The pivot point: every entry below this row is **unreachable on real-fixture invocations** unless `_new_run_id` resolves. |
| 4 | **1469** | `output_dir if output_dir is not None else _default_output_dir(run_id)` — second NameError if `output_dir` is None | NameError (conditional) | **No** — line 1467 raises first. | n/a (post-pivot) |
| 5 | **1479** | `click.echo(format_scratch_root_violation(exc), err=True)` inside `except ScratchRootViolation` (line 1478) | Error-handling branch | **No** — line 1467 NameError fires before `resolve_scratch_root` call at 1473. | n/a (post-pivot) |
| 6 | **1480** | `sys.exit(SCRATCH_ROOT_VIOLATION_EXIT_CODE)` | Early-exit (=2) | **No** — same reason. | n/a (post-pivot) |
| 7 | **1507** | `click.echo(f"eval run: {type(exc).__name__}: {exc}", err=True)` inside `except SuiteNotFound` (line 1506) | Error-handling branch | **No** — post-pivot. | n/a (post-pivot) |
| 8 | **1508** | `sys.exit(SUITE_NOT_FOUND_EXIT_CODE)` | Early-exit (=2) | **No** — post-pivot. | n/a |
| 9 | **1514** | `click.echo(f"eval run: {type(exc).__name__}: {exc}", err=True)` inside `except SuiteLoaderError` (line 1513) | Error-handling branch | **No** — post-pivot. | n/a |
| 10 | **1515** | `sys.exit(SUITE_LOADER_ERROR_EXIT_CODE)` | Early-exit (=2) | **No** — post-pivot. | n/a |
| 11 | **1529** | `sys.exit(EVAL_NOT_FOUND_EXIT_CODE)` inside `if missing:` (line 1523) | Early-exit (=2) | **No** — post-pivot. Note: this branch fires only if `--eval` filter excludes all expanded specs, which requires the suite to be loaded first (line 1512), which requires `resolve_scratch_root` (line 1473), which requires `_default_output_dir` (line 1469), which requires `_new_run_id` (line 1467). | n/a |
| 12 | **1547** | `click.echo(_format_coverage_missing_roster(coverage), err=True)` inside `if not coverage.passed:` (line 1546) | Error-handling branch | **No** — post-pivot. | n/a |
| 13 | **1548** | `sys.exit(COVERAGE_GATE_FAILED_EXIT_CODE)` | Early-exit (=2) | **No** — post-pivot. | n/a |
| 14 | **1577** | `executor_factory = _resolve_executor_factory()` — **third NameError** if reached | NameError | **No** — line 1467 fires first, but this is also a NameError itself. | n/a (compound failure post-pivot) |
| 15 | **1587** | `return EvalOutcome(... status="SKIPPED", ...)` inside `if no_pty and spec.no_pty == "skip":` (line 1586) — closure body | Conditional skip-return | **No** — closure body executes only after `orchestrator.run` is called at 1626/1628, which is post-pivot. Also note: this `return` is inside the `run_one` closure; the closure is *defined* at line 1579 but not *executed* until orchestrator dispatch. | n/a (post-pivot AND post-closure-call) |
| 16 | **1598** | `return _run_one_spec(spec, ...)` — **fourth NameError** when closure executes | NameError | **No** — post-pivot AND post-closure-call. | n/a |
| 17 | **1612** | `started_iso = _utc_iso_now()` — **fifth NameError** | NameError | **No** — post-pivot. | n/a |
| 18 | **1624** | `if SignalHandlerInstaller is not None and _can_install_signal_handler():` — **sixth NameError** | NameError (conditional, short-circuit) | **No** — post-pivot. Note: short-circuit evaluation means `SignalHandlerInstaller is not None` (which is True — it was successfully imported at line 87) does NOT prevent the second clause from being evaluated. | n/a |
| 19 | **1633** | `click.echo(f"eval run: orchestrator rejected request: {exc}", err=True)` inside `except ValueError` (line 1629) | Error-handling branch | **No** — post-pivot AND post-orchestrator-call. | n/a |
| 20 | **1634** | `sys.exit(HARD_FAIL_EXIT_CODE)` | Early-exit (=2) | **No** — post-pivot. | n/a |
| 21 | **1636** | `finished_iso = _utc_iso_now()` — **seventh NameError** | NameError | **No** — post-pivot. | n/a |
| 22 | **1642** | `counts, totals = _compute_run_stats(outcomes, manifest_n=manifest_n)` — **eighth NameError** | NameError | **No** — post-pivot. | n/a |
| 23 | **1671** | `click.echo(_format_run_summary_line(summary, resolved_output))` — **ninth NameError** inside `elif verbose:` (line 1670) | NameError (conditional) | **No** — post-pivot. | n/a |
| 24 | **1677** | `sys.exit(RUN_INTERRUPTED_EXIT_CODE)` — **tenth NameError** inside `if token.is_cancelled():` (line 1676) | NameError replacing exit-3 | **No** — post-pivot. | n/a |
| 25 | **1687** | `click.echo(DISK_BUDGET_RETENTION_ADVICE, err=True)` inside `if poller.is_breached():` (line 1678) | Diagnostic-echo branch | **No** — post-pivot. | n/a |
| 26 | **1688** | `sys.exit(DISK_BUDGET_EXCEEDED_EXIT_CODE)` | Early-exit (=2) | **No** — post-pivot. | n/a |
| 27 | **1694** | `sys.exit(RUN_FAILURES_EXIT_CODE)` — **eleventh NameError** inside `if totals.failed > 0 or totals.errored > 0 or totals.timeout > 0:` (lines 1689-1693) | NameError replacing exit-1 | **No** — post-pivot. | n/a |
| 28 | **1695** | `sys.exit(RUN_CLEAN_EXIT_CODE)` — **twelfth NameError** (the fall-through "happy path") | NameError replacing exit-0 | **No** — post-pivot. | n/a |

(Total entries traced: **28**. The expected-branches file lists ~19
canonical lines; the trace expands to 28 because several lines pair an
error-echo with an immediate exit, both of which are branches in the
control-flow sense.)

---

## SUFFICIENCY-BLOCKER summary

Two branches (`#1` at line 1453 and `#2` at line 1461) fire **before**
the line-1467 NameError. Both are flag-validation exits with `exit 2`.
They are reachable only when the operator passes:

- `--timeout-mult <= 0`, or
- `--max-disk-mb < 0`.

The TEST-008 process-boundary suite (`tests/cli/eval/test_exit_codes.py`)
exploits this by:

> *"The exit-code-2 paths (`--timeout-mult <=0`, `--max-disk-mb <0`) are
> guarded by flag validation that runs BEFORE the
> :mod:`superclaude.cli.eval.commands` run-id helper, so they exercise
> real `sys.exit(HARD_FAIL_EXIT_CODE)` calls today."*
> (`tests/cli/eval/test_exit_codes.py:31-34`)

This confirms the trace: lines 1453 and 1461 are the *only* runtime-
reachable exits in `eval_run` on the current codebase. **All other 26
branches are unreachable until T04.10 ships `_new_run_id`** (or the test
caller mocks it via `monkeypatch.setattr` — which the helper tests
explicitly do for `_run_one_spec`, see
`test_no_pty_exclusion.py:337` and `test_no_mcp_skip.py:528`).

---

## Filtering implication for the three theses

Because **only 2 of 28 branches are reachable on real-fixture
invocations**, no sibling agent can claim "the bug is masked by an
earlier guard." The real-fixture failure mode is **deterministic
NameError at line 1467, exit 1 (the Python interpreter's default
unhandled-exception exit code)** — NOT any of the design-spec §4 exit
codes (which would be 0/1/2/3 from `sys.exit`).

This is also confirmed by the CP-P05-END diagnostic at lines 217-220:

> *"The runner aborts with `NameError: name '_new_run_id'`… (`---EXIT:1`)
> at line 1467 of commands.py."*

(Note: `EXIT:1` here is the Python-interpreter exit code on unhandled
exception, **not** `RUN_FAILURES_EXIT_CODE = 1`. The two are the same
integer by coincidence, but the semantic provenance is different —
which is exactly the kind of subtle distinction the missing `RUN_*`
constants are supposed to disambiguate.)

---

## Conclusion (Rule 2.5)

Branch trace shows the line-1467 NameError is the **canonical failure
site for any operator-realistic invocation** of `eval run --suite real`.
The only two branches that bypass it (flag-validation early-exits at
lines 1453 and 1461) require operator-supplied invalid flag values and
are exercised today only by TEST-008's flag-validation pin. Every other
branch — including all conditional skip-returns, the orchestrator-error
recovery, and the four design-spec §4 terminal exits — is
post-NameError and therefore epistemically inert until T04.10 lands.
