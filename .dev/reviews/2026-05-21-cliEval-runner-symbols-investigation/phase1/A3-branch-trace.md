# A3 — Branch-trace (Rule 2.5)

**Agent**: A3
**Source**: `.dev/reviews/2026-05-21-cliEval-runner-symbols-investigation/artifacts/expected-branches-extended.txt`
**Subject file**: `src/superclaude/cli/eval/commands.py` (untracked)
**Subject function**: `eval_run` (declared at L1406, body terminates at L1695)
**First NameError site at runtime**: L1467 — `_new_run_id()`
**SUFFICIENCY-BLOCKER definition**: A branch is SUFFICIENCY-BLOCKER if a
real-world `superclaude eval run --suite real` invocation can plausibly
reach it BEFORE control flow hits L1467, because the defect surfaces
only after L1467 and any branch that exits earlier renders the eleven
NameErrors irrelevant for that invocation path.

The artifact's "expected branches" file lists 19 candidate lines pulled
by line-grep of `sys.exit(...)` and `return ...` sites in the
`eval_run` body (lines 1453-1695). Branch-trace below maps each one.

| # | Line | Condition / call | Reachable BEFORE L1467? | SUFFICIENCY-BLOCKER? | Notes |
|---|------|------------------|--------------------------|----------------------|-------|
| 1 | 1453 | `sys.exit(HARD_FAIL_EXIT_CODE)` — `timeout_mult <= 0` | **YES** | **YES** | Flag-validation branch: invocations supplying `--timeout-mult 0` or negative exit here before run_id is allocated. Default invocation skips it. |
| 2 | 1461 | `sys.exit(HARD_FAIL_EXIT_CODE)` — `max_disk_mb < 0` | **YES** | **YES** | Flag-validation branch: invocations supplying `--max-disk-mb -1` exit here before L1467. Default invocation skips it. |
| 3 | 1479 | `click.echo(format_scratch_root_violation(exc), err=True)` — caught from `resolve_scratch_root(...)` | NO | no | This runs at L1479, AFTER `_new_run_id()` at L1467 and AFTER `_default_output_dir(...)` at L1469. Cannot be reached without the L1467 NameError firing first. |
| 4 | 1480 | `sys.exit(SCRATCH_ROOT_VIOLATION_EXIT_CODE)` | NO | no | Pairs with #3. |
| 5 | 1507 | `click.echo(...)` — suite-not-found error path | NO | no | Post-L1467. |
| 6 | 1508 | `sys.exit(SUITE_NOT_FOUND_EXIT_CODE)` | NO | no | Post-L1467. |
| 7 | 1514 | `click.echo(...)` — suite-loader error path | NO | no | Post-L1467. |
| 8 | 1515 | `sys.exit(SUITE_LOADER_ERROR_EXIT_CODE)` | NO | no | Post-L1467. |
| 9 | 1529 | `sys.exit(EVAL_NOT_FOUND_EXIT_CODE)` — `--eval E?` mismatch | NO | no | Post-L1467. |
| 10 | 1547 | `click.echo(_format_coverage_missing_roster(coverage), err=True)` | NO | no | Post-L1467. |
| 11 | 1548 | `sys.exit(COVERAGE_GATE_FAILED_EXIT_CODE)` | NO | no | Post-L1467. |
| 12 | 1587 | `return EvalOutcome(...)` — `--no-pty` skip branch inside `run_one` closure | NO | no | Closure body; only invoked from inside orchestrator.run(...) at L1626/L1628, which is post-L1467 + post-L1612 (`_utc_iso_now()`). |
| 13 | 1598 | `return _run_one_spec(...)` — closure return path | NO | no | Closure body; same reasoning as #12. Also a second NameError site (`_run_one_spec`) but only triggered if the orchestrator dispatch reaches it, which it can't because L1467 fires first. |
| 14 | 1633 | `click.echo(f"eval run: orchestrator rejected request: {exc}", err=True)` | NO | no | Post-L1467. |
| 15 | 1634 | `sys.exit(HARD_FAIL_EXIT_CODE)` | NO | no | Post-L1467. |
| 16 | 1677 | `sys.exit(RUN_INTERRUPTED_EXIT_CODE)` | NO | no | Post-L1467; also itself a NameError site. |
| 17 | 1687 | `click.echo(DISK_BUDGET_RETENTION_ADVICE, err=True)` | NO | no | Post-L1467. |
| 18 | 1688 | `sys.exit(DISK_BUDGET_EXCEEDED_EXIT_CODE)` | NO | no | Post-L1467. |
| 19 | 1694 | `sys.exit(RUN_FAILURES_EXIT_CODE)` | NO | no | Post-L1467; also itself a NameError site. |
| (20) | 1695 | `sys.exit(RUN_CLEAN_EXIT_CODE)` | NO | no | Fall-through at end; post-L1467; also itself a NameError site. *Not in the source file but materially the 20th terminal branch.* |

## Reachability summary

* **19 candidate branches enumerated.**
* **2 SUFFICIENCY-BLOCKERs** (lines 1453, 1461) — both pre-L1467
  flag-validation paths. A bad `--timeout-mult` or `--max-disk-mb`
  invocation aborts before the defect surfaces; tests using only those
  inputs would miss the eleven NameErrors entirely. A real
  `--suite real` invocation (no bad flags) never hits 1453 or 1461 and
  therefore goes straight to L1467 and NameErrors out.
* **17 branches unreachable before the defect** — every other terminal
  branch sits downstream of the L1467 `_new_run_id()` NameError
  (against the un-patched `commands.py`).

## Implications for Thesis 2

The branch-trace is consistent with — and silent on — every thesis,
because all three theses agree the eleven symbols are missing from the
module. The trace contributes one substantive observation specific to
my seat: **even the post-L1467 NameError sites (`_utc_iso_now` ×2 at
L1612/L1636, `_can_install_signal_handler` at L1624, `_compute_run_stats`
at L1642, `_format_run_summary_line` at L1671, `RUN_INTERRUPTED_EXIT_CODE`
at L1677, `RUN_FAILURES_EXIT_CODE` at L1694, `RUN_CLEAN_EXIT_CODE` at
L1695, `_run_one_spec` at L1598) are arranged in a perfectly *linear,
unauthored* order — they appear at exactly the points an implementer
would have *next* extracted helper calls during top-down decomposition.
This pattern fits "wrote the call sites first, never wrote the helpers"
(Thesis 1) far better than "wrote then deleted" (Thesis 2), where one
would expect orphaned references in some branches to have been
mechanically rewritten and others not. The uniformity of all eleven
remaining as `_<verb>_<object>` placeholders is the signature of an
unfinished pass, not a partial-rename refactor.

## Branch-trace count for return summary

**19** candidate branches; **2** SUFFICIENCY-BLOCKERs.
