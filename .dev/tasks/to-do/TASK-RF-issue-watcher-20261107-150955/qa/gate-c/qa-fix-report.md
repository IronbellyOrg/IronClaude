# Gate C fix report (Step 7.G9)

**Fix agent:** one `rf-qa` agent with `fix_authorization: true`. **Scope:** `src/superclaude/cli/issue_watch/` and `tests/issue_watch/` only. No edit to the task file, design, spec, research, pyproject, Makefile, workflows or `.claude/`. Minor findings (C-14 to C-69) were not fixed.

**Result:** all 13 blocking findings (C-1 to C-13) fixed. `uv run pytest tests/issue_watch/ -q`: 2242 passed (2194 before). `make lint`: pass (0 errors, 5 existing warnings). Pinned `uvx --offline ruff@0.15.20 check` and `format --check` on the 10 changed files: all checks passed, 10 files already formatted.

## Executor decisions, recorded as [PROPOSAL]

| id | decision | where |
|---|---|---|
| C-2 | [PROPOSAL] one new cycle-kind reason `cycle_complete` (exit 0) in `audit.REASON_TABLE`; a clean cycle's cycle line uses it. A candidate that causes a cycle-level stop (`rate_limit_clamped`, `project_read_failed`, `orca_not_found`, `disabled_mid_cycle`, `origin_mismatch`) gets no decision line; the cycle line carries the stop reason. `considered` stamping is unchanged. | `audit.py` (comment above the entry), `cycle.py` `_cycle_reason` and `_candidates` |
| C-3 | [PROPOSAL] new closed reason `cycle_crashed` (kind cycle, exit 1), written only by `once` through `audit.stderr_fallback`. | `audit.py` (comment above the entry), `cli.py` `_EXIT_CRASH` and `once_command` |

The name-count pin in `test_audit.py` is now 59 names (57 + the two proposals), with both rows in `EXPECTED_NAMES` and `EXPECTED_TABLE`.

## Per blocking finding

| id | files changed | what changed |
|---|---|---|
| C-1 | `cycle.py`; `test_cycle.py`; `conftest.py` | `_origin_ok(timeout)` no longer reads the deadline. In `_launch` the order is now: day cap, `DISABLED`, then `launch_allowed()` (skip `budget_exhausted`), then `timeout_for(GIT_TIMEOUT_S)` None (skip `budget_exhausted`), then the git call; `origin_mismatch` (exit 2, stamp) is only for a git call that ran and failed. At the cycle-start check (`_steps`) no time left is `gh_timeout` (exit 3, no git call). New tests: 236 s jump at cycle start (exit 3, only the `user` call ran); 236 s jump during the reserved `items` re-read (exit 0, `cycle_complete`, decision `budget_exhausted`, one `origin` call, no entry, not stamped); same jump with `LAUNCH_CUTOFF_S` patched to 1000 so only the 5 s floor can refuse the call; git `failed`, `timeout` and `spawn_error` on the re-check are still exit 2 `origin_mismatch`. |
| C-2 | `audit.py`; `cycle.py`; `test_audit.py`; `test_cycle.py` | See the table above. `_cycle_reason` returns `cycle_complete` for a clean cycle; `_candidates` no longer writes a decision line for the `_Stop` candidate. `check_line_kinds` is restored to the strict invariant: a cycle line names a cycle-kind reason whose table exit equals the line exit (the one other kind allowed is an entry reason with table exit 7, which design 4.3 and the reason table give to the failed entry); a decision line never carries a cycle-kind reason; warning lines carry warning kinds. About 30 test expectations changed from the old behaviour to the strict rule (cycle reason `cycle_complete`, the skip reason asserted on the decision line; `EXIT_TABLE` row 5 now lists only issue 8). New tests: the checker rejects a skip or entry reason on an exit-0 cycle line, rejects a cycle reason on a decision line, accepts `cycle_complete` and an exit-7 entry reason; `mixed_decisions_and_launch` ends `cycle_complete` with its three decisions; `project_read_failed` has no decision line. |
| C-3 | `cli.py`; `test_cli.py`; `conftest.py` | `once_command` wraps `build_deps` and `run_cycle` in `except Exception` (never `SystemExit`, `KeyboardInterrupt` or `BaseException`), calls `audit.stderr_fallback("cycle_crashed", 1)`, prints `issue-watch: cycle_crashed: <ExceptionClassName>` (class name only, never the message) and exits 1. New tests: store whose `save` raises `RuntimeError` (exit 1, one fallback line with the five keys, no traceback, the exception text absent from the output, store unchanged, lock free, no audit line); `build_deps` raising; `SystemExit(42)` and `KeyboardInterrupt` propagate out of `once_command.callback` and print no `cycle_crashed`; `SystemExit(42)` through Click exits 42. |
| C-4 | `fixtures/_assumed_shape/orca_launch_no_operation_id.json` and `orca_launch_empty_operation_id.json` (new); `test_cycle.py`; `test_launch.py`; `test_github.py` | The two inline Orca reply bodies in `_UNKNOWN_OUTCOMES` now come from `load_fixture(...)["payload"]`. `test_launch.py` pins that the first fixture has no id at any `OPERATION_ID_PATHS` path and that the second holds `""` at path 0, so a changed path fails there. Fixture-count pin in `test_github.py` 17 to 19; the every-fixture-is-read test still passes (both names are read by `test_cycle.py`). |
| C-5 | `test_slo_helper.py` | Comment "13 / 20" changed to "13 / 18". |
| C-6 | `conftest.py` (new `FailingStore`); `test_cycle.py` | Pending save raises `OSError`: exit 6 `state_dir_unwritable`, `launcher.calls == []`, one save attempted, `dispatch.json` and the lock file byte-identical, no audit line, one stderr fallback line with the exact values. Outcome save (save 2) raises after the launch: one launch, the entry on disk is `pending` with `launches` 1, and two later cycles launch nothing (entry ends `abandoned` `pending_orphan`). |
| C-7 | `test_cycle.py`; `test_cli.py` | Final save raises `OSError` (idle cycle and one-skipped-issue cycle): exit 6, no cycle line in `audit.jsonl`, no health stamp, store unchanged, one fallback line. `once` prints `cycle: state_dir_unwritable` and `exit: 6`. |
| C-8 | `test_cycle.py` | `audit.jsonl` is a directory: a clean cycle and a login failure keep their exit code and reason, write exactly one stderr line with the keys `kind, ts, host, exit, reason` and literal values, and the store is still saved (health stamp on the clean cycle). |
| C-9 | `test_cycle.py` | Version-0 store with a future `next_permitted_at` (so the load is the only possible write): a real cycle rewrites it at version 1 without `legacy_note`; a dry-run leaves the bytes identical. |
| C-10 | `test_cycle.py` | With issues 9 and 10: `revalidation_failed`, `prompt_invalid`, the 121 s cut-off `budget_exhausted`, re-read `assigned_other` and re-read `unassigned` (parametrized), and `spawn_error`, each assert `_touched(world) == {9}`, no entry for 10, and `considered` equal to `[9]` (`[]` for the cut-off, which is never stamped). |
| C-11 | `conftest.py`; `test_cycle.py` | `FakeRunner.run` fails on a `None` timeout (after recording it); the `gh_world` teardown asserts every recorded timeout of every scripted cycle is not None and between 5 s and 20 s; a launch cycle's 12 timeouts are pinned as a literal list (20, 10, 20, 20, 20, 20, 20, 10, 20, 20, 20, 10). The C-1 tests cover the clock past 235 s before the cycle-start check, the probe and the second origin check. |
| C-12 | `test_cli.py` | `_REAL_BUILD_DEPS` is captured before the autouse fixture replaces `cli.build_deps`; one test calls it and asserts the config object, `SubprocessRunner`, `FileStore` and `AuditLog` over `config.state_dir`, `SystemClock`, `shutil.which`, `socket.gethostname()`, and that the `OrcaLauncher` runs the launch argv through `SubprocessRunner` with `cwd` set to the worktree. |
| C-13 | `test_cycle.py` | `_REAL_READ_MOUNTINFO` is captured before the autouse fixture. Tests: `_MOUNTINFO == "/proc/self/mountinfo"`; the real reader returns text from which `fs_type_of("/", ...)` finds a type (skips off Linux); the reader returns the file text for a tmp file and `None` for a missing one; `load_config` refuses an `nfs4` state directory through the real reader and accepts a local one. |

## Mutant re-run (copy under `/tmp`, repo never mutated, copy deleted afterwards)

Each mutant is a one-line change to a copy of `src/` run against the full `tests/issue_watch` suite. All 23 were killed (first failure with `-x`).

| mutant | result |
|---|---|
| M1 `_save` swallows `OSError` (C-6) | killed |
| M1b `_commit` swallows `OSError` (C-7) | killed |
| M1c audit fallback body replaced by `raise` (C-8) | killed |
| M2a migrated save never (`if False:`) (C-9) | killed |
| M2b dry-run also saves the migrated store (C-9) | killed |
| M3a no halt after `revalidation_failed` (C-10) | killed |
| M3b no halt after `prompt_invalid` (C-10) | killed |
| M3c no halt after the cut-off `budget_exhausted` (C-10) | killed |
| M3d no halt after re-read `assigned_other` or `unassigned` (C-10) | killed |
| M3e no halt after `spawn_error` (C-10) | killed |
| M4a origin `None` guard removed in `_launch` (C-11) | killed |
| M4a2 origin `None` guard removed at cycle start (C-11) | killed |
| M4b probe `None` guard removed (C-11) | killed |
| M5a `which` replaced by a lambda returning None (C-12) | killed |
| M5b audit log in another directory (C-12) | killed |
| M5c store in another directory (C-12) | killed |
| M7 `_MOUNTINFO` set to `/proc/self/mountstats` (C-13) | killed |
| C1a cut-off skip turned into `origin_mismatch` (C-1) | killed |
| C1b cycle-start no-time turned into `origin_mismatch` (C-1) | killed |
| C2a clean cycle reason back to `not_approved` (C-2) | killed |
| C2b stopping candidate gets a decision line again (C-2) | killed |
| C3a `once` catches `BaseException` (C-3) | killed |
| C3b `once` no longer catches `RuntimeError` (C-3) | killed |

## Points for the next reviewer

- C-1 at the cycle-start check: the fix prompt said "budget_exhausted (skip, exit 0)" for both places. A skip reason cannot sit on a cycle line under the strict DF-41 rule C-2 restores, and design 8.5 (line 644) says a shared call that cannot start is exit 3 `gh_timeout`, so the cycle-start origin check ends exit 3 `gh_timeout`; the per-issue re-check is `budget_exhausted`, exit 0, as specified. Change `cycle.py` `_steps` if the owner wants another reason.
- C-2: `check_line_kinds` keeps allowing the entry reasons with table exit 7 (`prompt_invalid`, `revalidation_transient`, `spawn_error`, `launch_unknown`) on an exit-7 cycle line, because the closed table gives exit 7 only to those reasons. Every other skip or entry reason on a cycle line is now rejected.
- With the 120 s cut-off checked first, the `timeout_for(GIT_TIMEOUT_S)` None guard in `_launch` is only reachable in a test that patches `cycle.LAUNCH_CUTOFF_S` (240 s total, 5 s floor, 120 s cut-off). It stays as a guard so a `None` can never reach a runner if the constants change; the C-11 test patches the cut-off to exercise it.
- The pending-save failure writes no audit line at all (not even decision lines of earlier candidates), as before; it is pinned by the new test.
- Tests that need root-free `chmod` still run as uid 1000 here; no new test depends on `chmod`.
