# Gate D change set (Phase 8)

Files discovered by Glob on 2026-11-08 under `tests/issue_watch/` and `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/phase-outputs/test-results/p8-*` (`__pycache__` entries excluded; they hold only stale bytecode and no source, including bytecode for four names that have no source file: `test_smoke_x`, `test_zz_scratch_world`, `test_tmp_orig`, `test_dbg_tmp`). Line counts from one `wc -l` call; executable files from one `find tests/issue_watch -type f -perm /111` call.

## Files created or changed in Phase 8

| Path | Lines | Step |
|---|---|---|
| `tests/issue_watch/conftest.py` (part 5 appended: `stub_path` fixture, `write_scenario`, `read_calls`; whole-file count) | 1155 | 8.1 |
| `tests/issue_watch/test_cli_e2e.py` | 443 | 8.2 |
| `tests/issue_watch/test_security_invariants.py` | 961 | 8.3 |
| `tests/issue_watch/test_crash_injection.py` | 373 | 8.4 |
| `tests/issue_watch/test_concurrency.py` | 275 | 8.5 |
| `tests/issue_watch/test_no_shell.py` | 191 | 8.6 |
| `tests/issue_watch/test_no_text.py` | 961 | 8.7 |
| `tests/issue_watch/test_module_boundaries.py` | 375 | 8.8 |

`test_security_invariants.py` and `test_no_text.py` both have 961 lines by coincidence (`cmp` reports them different; 32824 and 34121 bytes).

## Every file found by Glob (for reference)

Source (9, from the Gate C change set; not re-globbed): `__init__.py`, `runner.py`, `github.py`, `audit.py`, `predicates.py`, `launch.py`, `record.py`, `cycle.py`, `cli.py`. The Phase 8 steps create or append tests only, so no source file is listed as changed in Phase 8.

Tests (21 Python files): `__init__.py`, `conftest.py`, `test_runner.py`, `test_audit.py`, `test_predicates.py`, `test_github.py`, `test_record.py`, `test_launch.py`, `test_find_orca_parity.py`, `test_origin_parity.py`, `test_marker_contract.py`, `test_cycle.py`, `test_slo_helper.py`, `test_cli.py`, `test_cli_e2e.py`, `test_security_invariants.py`, `test_crash_injection.py`, `test_concurrency.py`, `test_no_shell.py`, `test_no_text.py`, `test_module_boundaries.py`.

Fixtures (19 JSON files under `tests/issue_watch/fixtures/_assumed_shape/`): `gh_issue_list`, `gh_stderr_auth_401`, `gh_api_user_include`, `gh_stderr_rate_403`, `gh_stderr_rate_429`, `rest_events_page`, `gh_graphql_insufficient_scopes`, `rest_comments_marker`, `gh_graphql_rate_limited`, `graphql_edits`, `graphql_project_items`, `gh_api_user_include_429`, `gh_stderr_http_502`, `gh_stderr_scope_read_project`, `orca_launch_success`, `orca_launch_unknown`, `gh_issue_reread`, `orca_launch_no_operation_id`, `orca_launch_empty_operation_id`. Phase 8 added none (the last two came from the Gate C fix, C-4).

Result files (p8): `p8-g1-raw.txt`, `p8-g1-summary.md`, `p8-g3-raw.txt`, `p8-g3-summary.md`, `p8-g8.txt`, `p8-ruff.txt`.

Nothing under `.claude/` appears in this change set.

## Files changed by Gate A, Gate B and Gate C fixes

Read from `qa/gate-a/qa-fix-report.md`, `qa/gate-a/qa-fix-report-cycle2.md`, `qa/gate-b/qa-fix-report.md`, `qa/gate-b/qa-fix-report-cycle2.md`, `qa/gate-c/qa-fix-report.md` and `qa/gate-c/qa-fix-report-cycle2.md`.

| Fix | Files changed |
|---|---|
| Gate A cycle 1 (18 blocking ids A-1 to A-18) | `src/superclaude/cli/issue_watch/{runner,predicates,audit,github}.py`; `tests/issue_watch/{conftest,test_runner,test_predicates,test_audit,test_github}.py`; new fixtures `gh_api_user_include_429.json`, `gh_stderr_http_502.json`, `gh_stderr_scope_read_project.json` under `tests/issue_watch/fixtures/_assumed_shape/` |
| Gate A cycle 2 (1 blocking id A-7) | `src/superclaude/cli/issue_watch/audit.py`; `tests/issue_watch/test_audit.py` |
| Gate B cycle 1 (13 blocking ids B-1 to B-13) | `src/superclaude/cli/issue_watch/{launch,record,predicates}.py`; `tests/issue_watch/{test_record,test_launch,test_predicates,test_find_orca_parity}.py` |
| Gate B cycle 2 | none: `qa/gate-b/qa-fix-report-cycle2.md` reads "skipped: cycle 2 not selected" |
| Gate C cycle 1 (13 blocking ids C-1 to C-13) | `src/superclaude/cli/issue_watch/{cycle,audit,cli}.py`; `tests/issue_watch/{test_cycle,test_audit,test_cli,test_launch,test_github,test_slo_helper,conftest}.py`; new fixtures `orca_launch_no_operation_id.json` and `orca_launch_empty_operation_id.json` under `tests/issue_watch/fixtures/_assumed_shape/` |
| Gate C cycle 2 (1 blocking id C2-1) | `src/superclaude/cli/issue_watch/cycle.py`; `tests/issue_watch/test_cycle.py` |

Gate C added two closed reasons to `audit.REASON_TABLE`: `cycle_complete` (kind cycle, exit 0) and `cycle_crashed` (kind cycle, exit 1, written only by `once` through `audit.stderr_fallback`); the name-count pin in `test_audit.py` is 59 names. Results recorded in the fix reports: Gate A cycle 1 684 passed, Gate A cycle 2 686 passed, Gate B cycle 1 1577 passed, Gate C cycle 1 2242 passed, Gate C cycle 2 2243 passed.

## Executable files under `tests/issue_watch/`

`find tests/issue_watch -type f -perm /111` printed nothing (exit 0). The list is empty, as expected.

## Gate commands of Phase 8

Verdicts and numbers are copied from the result files in `phase-outputs/test-results/`. The command text is the one in the task-file step; the result files for G-1 and G-3 hold the same command (the step also appends `2>&1; echo "EXIT=$?"`).

| Gate | Command | Exit | Verdict | Source |
|---|---|---|---|---|
| G-1 | `uv run pytest tests/issue_watch/ -v` | 0 | PASSED, 2616 passed, 0 failed, 0 errors, 0 skipped (`2616 passed in 16.86s`); failures table: none | `p8-g1-summary.md` (raw `p8-g1-raw.txt`) |
| G-3 | `uv run --offline --with "pytest-xdist>=3.5,<4" pytest -n auto tests/issue_watch/` | 0 | PASSED, 2616 passed, 0 failed, 0 errors, 0 skipped (`2616 passed in 6.40s`) | `p8-g3-summary.md` (raw `p8-g3-raw.txt`) |
| G-8 | `grep -rnE` with the single regex "shell=True", a pipe character, then "os", a backslash, a dot and "system" (the step text has the exact string; a pipe cannot sit inside a table cell), on `src/superclaude/cli/issue_watch/` | grep exit 1 (the file records `EXIT=1`) | NO_MATCH (no output) for the package as it now stands; this is the pass state | `p8-g8.txt` |
| G-5 | `uvx --offline ruff@0.15.20 check` then `uvx --offline ruff@0.15.20 format --check` on `conftest.py`, `test_cli_e2e.py`, `test_security_invariants.py`, `test_crash_injection.py`, `test_concurrency.py`, `test_no_shell.py`, `test_no_text.py`, `test_module_boundaries.py` (step text lists 8 files; the result file reports 31 files formatted and does not name them, consistent with the step's instruction to include earlier files touched by Gate C fixes) | check 0, format 0 | `All checks passed!`, `31 files already formatted` | `p8-ruff.txt` |

`p8-g1-summary.md` also records that the `git status --short` after the G-1 run showed no file created outside the paths this task owns.

## Decision rows applied

DF-10, DF-12, DF-15, DF-28, DF-29, DF-31, DF-34, DF-39, DF-55, DF-56.

## Design line ranges implemented

D 507-533, 653-672, 691-693, 765, 772-791.
