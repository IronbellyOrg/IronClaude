# A4 — Branch Trace (Rule 2.5)

**Scope**: For each branch in `expected-branches-extended.txt`, record whether `eval run --suite real` reaches that branch BEFORE the NameError fires at commands.py:1467 (`run_id = _new_run_id()`).

**Key finding**: The NameError at line 1467 is the **first line of executable body logic** after the flag-validation block (lines 1443–1461). Only the flag-validation branches (`HARD_FAIL_EXIT_CODE` lines 1453, 1461) can fire before the NameError, and only when the operator passes malformed `--timeout-mult` or `--max-disk-mb`. The canonical `eval run --suite real` invocation in design-spec §4 hits **none** of the flag-validation branches and crashes immediately on line 1467.

## Per-branch trace

| # | Line | Condition / branch | Reached before NameError@1467? | SUFFICIENCY-BLOCKER? |
|---|---|---|---|---|
| 1 | 1453 | `sys.exit(HARD_FAIL_EXIT_CODE)` — fires when `timeout_mult <= 0` | YES, but only with `--timeout-mult <= 0`. Default `1.0` → not reached on `eval run --suite real`. | NO — flag-validation branch; covered by canonical invocation. |
| 2 | 1461 | `sys.exit(HARD_FAIL_EXIT_CODE)` — fires when `max_disk_mb < 0` | YES, but only with `--max-disk-mb < 0`. Default `1024` → not reached. | NO — flag-validation branch; covered by canonical invocation. |
| 3 | 1479 | `click.echo(format_scratch_root_violation(exc), err=True)` — fires inside `except ScratchRootViolation` after the `resolve_scratch_root` call at 1473 | **NO** — `resolve_scratch_root` runs at 1473, but its `requested_output` argument is computed at 1468–1470 which references `_default_output_dir(run_id)` and `run_id = _new_run_id()` at 1467 → NameError fires FIRST. | **YES — BLOCKER**. This branch cannot be exercised by any `eval run` invocation while the NameError stands. |
| 4 | 1480 | `sys.exit(SCRATCH_ROOT_VIOLATION_EXIT_CODE)` — same `except` as #3 | NO — same reason. | **YES — BLOCKER**. |
| 5 | 1507 | `click.echo(f"eval run: {type(exc).__name__}: {exc}", err=True)` — inside `except SuiteNotFound` for `resolve_suite_manifest` at 1505 | NO — 1505 is BELOW the NameError site. | **YES — BLOCKER**. |
| 6 | 1508 | `sys.exit(SUITE_NOT_FOUND_EXIT_CODE)` — same | NO. | **YES — BLOCKER**. |
| 7 | 1514 | `click.echo(...)` inside `except SuiteLoaderError` at 1513 | NO — below NameError site. | **YES — BLOCKER**. |
| 8 | 1515 | `sys.exit(SUITE_LOADER_ERROR_EXIT_CODE)` | NO. | **YES — BLOCKER**. |
| 9 | 1529 | `sys.exit(EVAL_NOT_FOUND_EXIT_CODE)` — inside the `if missing:` block at 1523 (`--eval` resolution) | NO — line 1519+ is far below the NameError site. | **YES — BLOCKER**. |
| 10 | 1547 | `click.echo(_format_coverage_missing_roster(coverage), err=True)` — coverage-gate failure | NO — below. | **YES — BLOCKER**. |
| 11 | 1548 | `sys.exit(COVERAGE_GATE_FAILED_EXIT_CODE)` | NO. | **YES — BLOCKER**. |
| 12 | 1587 | `return EvalOutcome(...)` inside `run_one` closure — `--no-pty` short-circuit branch | NO — `run_one` is a *closure*, defined at 1579 but only invoked from inside `orchestrator.run(...)` at 1626. That call site is BELOW the NameError at 1467. The closure body is never reached. | **YES — BLOCKER**. |
| 13 | 1598 | `return _run_one_spec(spec, ...)` — main worker call inside `run_one` closure | NO — same reason as #12. Additionally, `_run_one_spec` is itself one of the 11 undefined names so even if reached it would NameError. | **YES — BLOCKER (compound)**. |
| 14 | 1633 | `click.echo(f"eval run: orchestrator rejected request: {exc}", err=True)` — `except ValueError` from `orchestrator.run(...)` at 1626 | NO. | **YES — BLOCKER**. |
| 15 | 1634 | `sys.exit(HARD_FAIL_EXIT_CODE)` — same `except` | NO. | **YES — BLOCKER**. |
| 16 | 1677 | `sys.exit(RUN_INTERRUPTED_EXIT_CODE)` — final exit-code block, cancel-token branch | NO — below NameError; also itself references undefined `RUN_INTERRUPTED_EXIT_CODE`. | **YES — BLOCKER (compound)**. |
| 17 | 1687 | `click.echo(DISK_BUDGET_RETENTION_ADVICE, err=True)` — disk-budget breach branch | NO. | **YES — BLOCKER**. |
| 18 | 1688 | `sys.exit(DISK_BUDGET_EXCEEDED_EXIT_CODE)` | NO. | **YES — BLOCKER**. |
| 19 | 1694 | `sys.exit(RUN_FAILURES_EXIT_CODE)` — failure-tally branch | NO — also references undefined `RUN_FAILURES_EXIT_CODE`. | **YES — BLOCKER (compound)**. |
| 20 | 1695 | `sys.exit(RUN_CLEAN_EXIT_CODE)` — clean-run fall-through | NO — also references undefined `RUN_CLEAN_EXIT_CODE`. | **YES — BLOCKER (compound)**. |

## Branch-trace summary

- **Total branches**: 20
- **Reachable before NameError@1467**: **2** (flag-validation branches at lines 1453, 1461), and only with malformed CLI flags. Default-flag `eval run --suite real` reaches NEITHER.
- **Unreachable / SUFFICIENCY-BLOCKER count**: **18 out of 20**.
- **Compound blockers** (branch site itself references an undefined name): **4** (lines 1598, 1677, 1694, 1695).

## Implication for Thesis 3

The branch-trace confirms that the F821 defect is **operationally fatal** to every meaningful eval_run code path. Any test that exercises *any* of the 18 SUFFICIENCY-BLOCKER branches must currently skip (and indeed the precondition probes in `test_single_command.py:134–161`, `test_no_mcp_skip.py:486–493`, `test_exit_codes.py`, `test_no_pty_exclusion.py`, and `test_retention_policy.py` all detect the missing names and skip). The fix — whether by Thesis 1 (author in-place), Thesis 2 (rename ghosts), or Thesis 3 (consolidate-to-siblings) — must restore reachability for **all 18 blocker branches** simultaneously, because they cluster downstream of a single point of failure (the assignment at line 1467).

This is consistent with the Thesis 3 reading that a single deferred-consolidation episode is the proximate cause: the author tried to wire to siblings, used placeholder names everywhere downstream, and never came back. The 18 unreachable branches are the *radius of the unfinished consolidation*, not 18 separate bugs.
