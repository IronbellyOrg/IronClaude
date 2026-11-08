# Gate C change set (Phases 6 and 7)

Files discovered by Glob on 2026-11-08 under `src/superclaude/cli/issue_watch/`, `tests/issue_watch/` and `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/phase-outputs/test-results/p[67]-*` (`__pycache__` entries excluded; they hold only stale bytecode and no source). Line counts from one `wc -l` call.

## Files created or changed in Phases 6 and 7

| Path | Lines | Step |
|---|---|---|
| `src/superclaude/cli/issue_watch/cycle.py` | 1350 | 6.1, 6.2, 6.3 |
| `tests/issue_watch/conftest.py` (part 4 appended: deps factory and scripted GitHub world) | 889 | 6.4 |
| `tests/issue_watch/test_cycle.py` | 4153 | 6.5, 6.6, 6.7, 6.8 |
| `tests/issue_watch/test_slo_helper.py` | 416 | 6.9 |
| `tests/issue_watch/fixtures/_assumed_shape/gh_issue_reread.json` (new fixture, fixture pin 16 to 17, per the Phase 6 task-log entry) | n/a | 6.4 |
| `src/superclaude/cli/issue_watch/cli.py` | 339 | 7.1, 7.2 |
| `src/superclaude/cli/main.py` (edit; whole-file count) | 569 | 7.3 |
| `tests/issue_watch/test_cli.py` | 1443 | 7.4, 7.5 |

## Every file found by Glob (for reference)

Source (9): `__init__.py`, `runner.py`, `github.py`, `audit.py`, `predicates.py`, `launch.py`, `record.py`, `cycle.py`, `cli.py`.

Tests (14 Python files): `__init__.py`, `conftest.py`, `test_runner.py`, `test_audit.py`, `test_predicates.py`, `test_github.py`, `test_record.py`, `test_launch.py`, `test_find_orca_parity.py`, `test_origin_parity.py`, `test_marker_contract.py`, `test_cycle.py`, `test_slo_helper.py`, `test_cli.py`.

Fixtures (17 JSON files under `tests/issue_watch/fixtures/_assumed_shape/`): `gh_issue_list`, `gh_stderr_auth_401`, `gh_api_user_include`, `gh_stderr_rate_403`, `gh_stderr_rate_429`, `rest_events_page`, `gh_graphql_insufficient_scopes`, `rest_comments_marker`, `gh_graphql_rate_limited`, `graphql_edits`, `graphql_project_items`, `gh_api_user_include_429`, `gh_stderr_http_502`, `gh_stderr_scope_read_project`, `orca_launch_success`, `orca_launch_unknown`, `gh_issue_reread`.

Result files (p6/p7): `p6-g1-raw.txt`, `p6-g1-summary.md`, `p6-ruff.txt`, `p7-g9.txt`, `p7-g2-raw.txt`, `p7-g2-summary.md`, `p7-g4-raw.txt`, `p7-g4-summary.md`, `p7-ruff.txt`.

## Files changed by Gate A and Gate B fixes

Read from `qa/gate-a/qa-fix-report.md`, `qa/gate-a/qa-fix-report-cycle2.md`, `qa/gate-b/qa-fix-report.md` and `qa/gate-b/qa-fix-report-cycle2.md`.

| Fix | Files changed |
|---|---|
| Gate A cycle 1 (18 blocking ids A-1 to A-18) | `src/superclaude/cli/issue_watch/{runner,predicates,audit,github}.py`; `tests/issue_watch/{conftest,test_runner,test_predicates,test_audit,test_github}.py`; new fixtures `gh_api_user_include_429.json`, `gh_stderr_http_502.json`, `gh_stderr_scope_read_project.json` under `tests/issue_watch/fixtures/_assumed_shape/` |
| Gate A cycle 2 (1 blocking id A-7) | `src/superclaude/cli/issue_watch/audit.py`; `tests/issue_watch/test_audit.py` |
| Gate B cycle 1 (13 blocking ids B-1 to B-13) | `src/superclaude/cli/issue_watch/{launch,record,predicates}.py`; `tests/issue_watch/{test_record,test_launch,test_predicates,test_find_orca_parity}.py` |
| Gate B cycle 2 | none: `qa/gate-b/qa-fix-report-cycle2.md` reads "skipped: cycle 2 not selected" |

Gate B cycle 1 results recorded in its report: `uv run pytest tests/issue_watch/ -q` 1577 passed; pinned ruff check and format check clean on its 7 files; `make lint` exit clean with 0 architecture errors and 5 warnings. Gate A cycle 2 recorded 686 passed.

## main.py diff (`git diff -- src/superclaude/cli/main.py`, verbatim)

```diff
diff --git a/src/superclaude/cli/main.py b/src/superclaude/cli/main.py
index ffe4a34d..74ffc1a9 100644
--- a/src/superclaude/cli/main.py
+++ b/src/superclaude/cli/main.py
@@ -560,6 +560,10 @@ from superclaude.cli.reflect.commands import reflect_group  # noqa: E402,I001  #
 
 main.add_command(reflect_group, name="reflect")
 
+from superclaude.cli.issue_watch.cli import issue_watch_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports
+
+main.add_command(issue_watch_group, name="issue-watch")
+
 
 if __name__ == "__main__":
     main()
```

## Gate commands of Phases 6 and 7

Verdicts and numbers are copied from the result files in `phase-outputs/test-results/`. For the ruff rows the command text is the one in the task-file step; the result file holds only the tool output.

| Gate | Phase | Command | Exit | Verdict | Source |
|---|---|---|---|---|---|
| G-1 | 6 | `uv run pytest tests/issue_watch/ -v` | 0 | PASSED, 2098 passed, 0 failed, 0 errors (`2098 passed in 7.68s`) | `p6-g1-summary.md` |
| G-5 | 6 | `uvx --offline ruff@0.15.20 check` then `uvx --offline ruff@0.15.20 format --check` on `cycle.py`, `conftest.py`, `test_cycle.py`, `test_slo_helper.py` (step text lists 4 files; the result file reports "5 files already formatted" and does not name the fifth) | check 0, format 0 | `All checks passed!`, `5 files already formatted` | `p6-ruff.txt` |
| G-1 | 7 | same run as G-2 (the Phase 7 record of G-1) | 0 | see G-2 | `p7-g2-summary.md` |
| G-2 | 7 | `uv run pytest tests/issue_watch/ tests/skills/test_model_alias_policy.py tests/docs/test_retired_docs_absent.py tests/cli/test_cli_registration.py tests/swarm/test_cli_registration.py tests/recommend/test_cli_registration.py -v -rs` (`-rs` added to print the skip reason; it changes no selection) | 0 | PASSED, 2224 passed, 1 skipped, 0 failed, 0 errors (`2224 passed, 1 skipped in 10.37s`); the one skip is the pre-existing `tests/swarm/test_cli_registration.py:127` "got empty parameter set for (subcommand)", outside this change set; no skip in `tests/issue_watch/` | `p7-g2-summary.md` |
| G-4 | 7 | `make lint` | 0 | PASSED; architecture policy 0 errors, 5 warnings (pre-existing, none in issue_watch); `ruff check .` All checks passed | `p7-g4-summary.md` |
| G-5 | 7 | `uvx --offline ruff@0.15.20 check` then `uvx --offline ruff@0.15.20 format --check` on `cli.py`, `main.py`, `test_cli.py` | check 0, format 0 | `All checks passed!`, `3 files already formatted` | `p7-ruff.txt` |
| G-9 | 7 | `uv run superclaude issue-watch --help` | 0 | PASSED; the Commands block lists exactly `check-config`, `init-state`, `once`, `reset`, `status` | `p7-g9.txt` |

## Decision rows applied

DF-02, DF-03, DF-04, DF-06, DF-13, DF-17, DF-20, DF-22, DF-23, DF-25, DF-29, DF-41, DF-43, DF-44, DF-45, DF-47, DF-50, DF-51, DF-52, DF-53, DF-55, DF-57.

## Design line ranges implemented

D 108-121, 123-166, 224-225, 288-302, 304-388, 724-745, 759-760.
