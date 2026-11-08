# Final change set (Step 9.F1)

Date: 2026-11-08. Branch `ironbelly/issue-331-github-issue-watcher`. Files discovered by Glob on 2026-11-08 under `src/superclaude/cli/issue_watch/`, `tests/issue_watch/` (which includes `tests/issue_watch/fixtures/_assumed_shape/`) and `docs/designs/issue-watcher-setup.md` (`__pycache__` entries excluded; they hold only bytecode, including stale bytecode for names that have no source file). Line counts come from one `wc -l` Bash call made in this step; the file counts were cross-checked with `find ... -not -path '*__pycache__*'` (9 source files, 40 files under `tests/issue_watch/` = 21 Python files + 19 JSON fixtures). The creating phase of each file is copied from `gate-a-change-set.md`, `gate-b-change-set.md`, `gate-c-change-set.md` and `gate-d-change-set.md` (which name the step). `docs/designs/issue-watcher.md` (the design) is also untracked but is not part of this change set (the deviation register records it as untouched by this task).

## 1. Every created or changed file

| Path | Lines | Creating phase (step) |
|---|---|---|
| `src/superclaude/cli/issue_watch/__init__.py` | 0 | 1 (1.6) |
| `src/superclaude/cli/issue_watch/runner.py` | 130 | 2 (2.1) |
| `src/superclaude/cli/issue_watch/predicates.py` | 312 | 2 (2.2) |
| `src/superclaude/cli/issue_watch/audit.py` | 404 | 2 (2.3) |
| `src/superclaude/cli/issue_watch/github.py` | 960 | 3 (3.1a-3.1c) |
| `src/superclaude/cli/issue_watch/record.py` | 865 | 4 (4.1a-4.1c) |
| `src/superclaude/cli/issue_watch/launch.py` | 355 | 5 (5.1) |
| `src/superclaude/cli/issue_watch/cycle.py` | 1369 | 6 (6.1-6.3) |
| `src/superclaude/cli/issue_watch/cli.py` | 348 | 7 (7.1, 7.2) |
| `src/superclaude/cli/main.py` (changed, not created; whole file is not counted here; diff in section 4) | n/a (diff adds 4 lines) | 7 (7.3) |
| `tests/issue_watch/__init__.py` | 0 | 1 (1.7) |
| `tests/issue_watch/conftest.py` (grown in Phases 2, 4/5, 6 and 8) | 1155 | 2 (2.4); parts appended in 4 (4.2), 5 (5.3), 6 (6.4), 8 (8.1) |
| `tests/issue_watch/test_runner.py` | 226 | 2 (2.5) |
| `tests/issue_watch/test_predicates.py` | 732 | 2 (2.6-2.7) |
| `tests/issue_watch/test_audit.py` | 849 | 2 (2.8) |
| `tests/issue_watch/test_github.py` | 2161 | 3 (3.6-3.7) |
| `tests/issue_watch/test_record.py` | 2369 | 4 (4.3-4.5) |
| `tests/issue_watch/test_launch.py` | 842 | 5 (5.4-5.5) |
| `tests/issue_watch/test_find_orca_parity.py` | 288 | 5 (5.6) |
| `tests/issue_watch/test_origin_parity.py` | 176 | 5 (5.7) |
| `tests/issue_watch/test_marker_contract.py` | 53 | 5 (5.8) |
| `tests/issue_watch/test_cycle.py` | 4671 | 6 (6.5-6.8) |
| `tests/issue_watch/test_slo_helper.py` | 421 | 6 (6.9) |
| `tests/issue_watch/test_cli.py` | 1593 | 7 (7.4, 7.5) |
| `tests/issue_watch/test_cli_e2e.py` | 443 | 8 (8.2) |
| `tests/issue_watch/test_security_invariants.py` | 968 | 8 (8.3) |
| `tests/issue_watch/test_crash_injection.py` | 373 | 8 (8.4) |
| `tests/issue_watch/test_concurrency.py` | 275 | 8 (8.5) |
| `tests/issue_watch/test_no_shell.py` | 266 | 8 (8.6) |
| `tests/issue_watch/test_no_text.py` | 969 | 8 (8.7) |
| `tests/issue_watch/test_module_boundaries.py` | 413 | 8 (8.8) |
| `tests/issue_watch/fixtures/_assumed_shape/gh_api_user_include.json` | 5 | 3 (3.2-3.5) |
| `tests/issue_watch/fixtures/_assumed_shape/gh_graphql_insufficient_scopes.json` | 14 | 3 (3.2-3.5) |
| `tests/issue_watch/fixtures/_assumed_shape/gh_graphql_rate_limited.json` | 14 | 3 (3.2-3.5) |
| `tests/issue_watch/fixtures/_assumed_shape/gh_issue_list.json` | 27 | 3 (3.2-3.5) |
| `tests/issue_watch/fixtures/_assumed_shape/gh_stderr_auth_401.json` | 7 | 3 (3.2-3.5) |
| `tests/issue_watch/fixtures/_assumed_shape/gh_stderr_rate_403.json` | 7 | 3 (3.2-3.5) |
| `tests/issue_watch/fixtures/_assumed_shape/gh_stderr_rate_429.json` | 7 | 3 (3.2-3.5) |
| `tests/issue_watch/fixtures/_assumed_shape/graphql_edits.json` | 37 | 3 (3.2-3.5) |
| `tests/issue_watch/fixtures/_assumed_shape/graphql_project_items.json` | 30 | 3 (3.2-3.5) |
| `tests/issue_watch/fixtures/_assumed_shape/rest_comments_marker.json` | 27 | 3 (3.2-3.5) |
| `tests/issue_watch/fixtures/_assumed_shape/rest_events_page.json` | 42 | 3 (3.2-3.5) |
| `tests/issue_watch/fixtures/_assumed_shape/orca_launch_success.json` | 14 | 5 (5.2) |
| `tests/issue_watch/fixtures/_assumed_shape/orca_launch_unknown.json` | 7 | 5 (5.2) |
| `tests/issue_watch/fixtures/_assumed_shape/gh_issue_reread.json` | 11 | 6 (6.4) |
| `tests/issue_watch/fixtures/_assumed_shape/gh_api_user_include_429.json` | 8 | Gate A fix (cycle 1; Phase 3 content) |
| `tests/issue_watch/fixtures/_assumed_shape/gh_stderr_http_502.json` | 7 | Gate A fix (cycle 1; Phase 3 content) |
| `tests/issue_watch/fixtures/_assumed_shape/gh_stderr_scope_read_project.json` | 7 | Gate A fix (cycle 1; Phase 3 content) |
| `tests/issue_watch/fixtures/_assumed_shape/orca_launch_no_operation_id.json` | 10 | Gate C fix (cycle 1, finding C-4; Phase 6/7 content) |
| `tests/issue_watch/fixtures/_assumed_shape/orca_launch_empty_operation_id.json` | 10 | Gate C fix (cycle 1, finding C-4; Phase 6/7 content) |
| `docs/designs/issue-watcher-setup.md` (owner runbook) | 651 | 9 (created in Phase 9, per the deviation register row DF-60) |

Counts: 9 source files (the nine counted in section 2) + 1 changed registry file (`main.py`) + 21 Python test files (including the zero-byte `__init__.py`) + 19 JSON fixtures + 1 runbook. The fixture count is 19, not the "thirteen" written in the Step 9.F2 prompt text; `gate-d-change-set.md` also lists 19 (11 from Phase 3, 2 from Phase 5, 1 from Phase 6, 3 from the Gate A fix, 2 from the Gate C fix, as the table above shows). Files edited later by gate fixes keep the phase that created them; the files each gate fix changed are listed in `gate-d-change-set.md` ("Files changed by Gate A, Gate B and Gate C fixes") and the Gate D fix changed test files only (`qa/gate-d/qa-fix-report.md`). Step 9.17 edited only docstring lines of `test_predicates.py`, `test_cycle.py`, `test_cli.py`, `test_security_invariants.py`, `test_no_shell.py`, `test_slo_helper.py` and `test_module_boundaries.py` (`ac-trace.md`, last paragraph).

## 2. Total line counts

| Group | Files | Total lines | Source |
|---|---|---|---|
| Source files, `src/superclaude/cli/issue_watch/` | 9 | 4743 | `wc -l` total |
| Test Python files, `tests/issue_watch/*.py` (including `conftest.py` and the zero-byte `__init__.py`) | 21 | 19243 | `wc -l` total |
| Fixture JSON files, `tests/issue_watch/fixtures/_assumed_shape/` | 19 | 291 | `wc -l` total |
| Runbook, `docs/designs/issue-watcher-setup.md` | 1 | 651 | `wc -l` |

Test count, copied from `final-gate-record.md`: 2628 passed, 0 skipped for `uv run pytest tests/issue_watch/ -v`. `ac-trace.md` records 844 test functions in `tests/issue_watch/`.

## 3. git status

`git status --short`, lines outside `.dev/tasks/`:

```
 M src/superclaude/cli/main.py
?? .dev/brainstorms/20261107-064825-github-issue-watcher/
?? .dev/issues/331/
?? docs/designs/issue-watcher-setup.md
?? docs/designs/issue-watcher.md
?? src/superclaude/cli/issue_watch/
?? tests/issue_watch/
```

Lines under `.dev/tasks/`: 166 (161 staged; 5 untracked directories: `phase-outputs/`, `qa/gate-a/`, `qa/gate-b/`, `qa/gate-c/`, `qa/gate-d/` of this task package). `git diff --cached --name-only` printed 161 paths, 0 outside `.dev/tasks/`. Nothing in the change set above (source, tests, runbook, `main.py`) is staged yet: they are untracked or modified in the working tree; Phase 10 stages them by the allowlist. `.dev/issues/` and `.dev/brainstorms/` are untracked on purpose.

## 4. `git diff -- src/superclaude/cli/main.py` (verbatim)

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

`git diff --cached -- src/superclaude/cli/main.py` printed nothing (not staged).

## 5. Final gate record table (copied from `final-gate-record.md`, dated 2026-11-08)

All results were produced after the Step 9.17 docstring edits.

| Gate | Command | Exit | Verdict |
|---|---|---|---|
| G-1 | `uv run pytest tests/issue_watch/ -v` | 0 (2628 passed, 0 skipped) | PASS |
| G-2 | `uv run pytest tests/issue_watch/ tests/skills/test_model_alias_policy.py tests/docs/test_retired_docs_absent.py tests/cli/test_cli_registration.py tests/swarm/test_cli_registration.py tests/recommend/test_cli_registration.py -v -rs` | 0 (2658 passed, 1 pre-existing skip outside this change set) | PASS |
| G-3 | `uv run --offline --with "pytest-xdist>=3.5,<4" pytest -n auto tests/issue_watch/` | 0 (2628 passed, 0 skipped) | PASS |
| G-4 | `make lint` | 0 (5 pre-existing warnings, none in issue_watch) | PASS |
| G-5 | `uvx --offline ruff@0.15.20 check` and `format --check` on the package, main.py and tests, then `format --check src/ tests/` | 0, 0, 0 (31 and 1234 files already formatted) | PASS |
| G-6 | `make verify-deps`; `make sync-dev` (preparation); `make verify-sync` | 0, 0, 0 (all components in sync; nothing under src/superclaude/{skills,agents,commands,hooks,templates} changed) | PASS |
| G-7 | grep of Python 3.11+ APIs over the package and tests | 1 hit, a docstring (predicates.py:30), justified in p9-g7.txt | PASS |
| G-8 | `grep -rnE 'shell=True\|os\.system' src/superclaude/cli/issue_watch/` | 1 (NO_MATCH) | PASS |
| G-9 | `uv run superclaude issue-watch --help` | 0 (exactly check-config, init-state, once, reset, status) | PASS |
| G-10 | `git diff --exit-code pyproject.toml Makefile`; `git diff --exit-code -- .github/`; staged `.claude/` paths | 0, 0, 0 staged .claude/ paths | PASS |
| G-11 | trailing-space, CR and final-newline checks (48 files) | no hit, 0 problems | PASS |

Statements required by the plan (copied):
- full suite: CI only (the whole `make test` run is left to CI, decision DF-05).
- pre-commit hooks are not run as a whole locally. G-11 covers only trailing spaces, CR and the final newline. The secret scan (detect-secrets-hook, G-12) and markdownlint (G-13) were run by hand, offline, in the Final-gate fix pass and exit 0 (see `final-gate-record.md`, "Final-gate fix pass"); the fixture JSON parse test and the runbook reading cover the rest (decisions DF-32 and DF-58).

Additional fact in the record: a real Python 3.10.20 interpreter was found during Gate D and the whole `tests/issue_watch` suite passed on it (2628 passed); the plan text saying none exists is stale.

## 6. AC trace table (from `ac-trace.md`, Table 1; the "Test" column names the first test the trace lists for the row, and `ac-trace.md` holds the full list per row and the FR/NFR table)

| AC | Criterion | Ids | First-named test | Verdict |
|---|---|---|---|---|
| AC-1 | One `once` runs the FR-001 order; `FakeRunner` sees G1 first and no argv after an exit decision | FR-001, FR-002 | `test_cli_e2e.py::test_fr010_fr013_eligible_issue_launches_once_through_orca_ide` | PASS |
| AC-2 | Discovery argv equals the FR-003 literal; 100 results or a repeated number exits 4 | FR-003, FR-004 | `test_github.py::test_g2_argv_is_the_fr003_literal__fr003` | PASS |
| AC-3 | Approval table: outsider, bot, unlabel, relabel, incomplete history, edit after approval each skip with their reason | FR-005, FR-006 | `test_predicates.py::test_ac3_not_approved_rows__fr005` | PASS |
| AC-4 | Project and owner tables: wrong project, not Backlog, unassigned, other assignee skip | FR-007, FR-008 | `test_predicates.py::test_fr007_project_mismatch_rows` | PASS |
| AC-5 | An own-login marker comment yields `claimed` and no launch | FR-009 | `test_cycle.py::test_an_own_claim_marker_gives_claimed_and_no_launch__ac5_fr009` | PASS |
| AC-6 | `pending` with `launches` 1 is saved before the launcher is called; the re-read failure skips | FR-010, FR-011 | `test_cycle.py::test_the_launch_steps_run_in_the_fr014_order_and_pending_is_durable__fr010_fr014` | PASS |
| AC-7 | Every recorded prompt matches the D3 regex over the hostile corpus; non-int input raises | FR-012, NFR-001 | `test_launch.py::test_ac7_prompt_accepts_only_the_int_nine__fr012_nfr001` | PASS |
| AC-8 | Launch argv equals the 12-element list; outcome table maps to `launched`, `failed`, `unknown`, `abandoned` | FR-013, FR-014 | `test_launch.py::test_ac8_launch_argv_equals_the_literal_twelve_elements__fr013` | PASS |
| AC-9 | No automatic retry; `status` lists the full retry argv for an `unknown` entry | FR-015, FR-021 | `test_cycle.py::test_a_dispatched_entry_without_a_fresh_marker_skips_already_dispatched__fr009` | PASS |
| AC-10 | Budget, day cap and `consumed_log` hold through `reset`; acceptance property passes | FR-016, FR-023, FR-024, NFR-009 | `test_cycle.py::test_acceptance_property` | PASS |
| AC-11 | Second process exits 75; symlinked or foreign lock exits 6 | FR-017 | `test_concurrency.py::test_two_processes_one_store_one_launch__fr017_ac11` | PASS |
| AC-12 | `DISABLED` and `enabled: false` exit 0 before any external call | FR-018, FR-027 | `test_cycle.py::test_disabled_is_exit_0_with_zero_calls_and_no_health_stamp__fr018_fr021` | PASS |
| AC-13 | Dry-run writes only `dry-run.json` and audit; the real store is byte-identical | FR-019 | `test_cycle.py::test_a_dry_run_reports_would_launch_and_writes_nothing_but_the_shadow__fr019` | PASS |
| AC-14 | Every exit writes a schema-valid audit line or the stderr fallback; rotation keeps 4 files | FR-020, NFR-006 | `test_audit.py::test_reasons_pin_59_names__ac14_fr020_nfr006` | PASS |
| AC-15 | Shared-input failures map to exits 2, 3, 5, 6, 7 with the precedence 2, 6, 7, 5, 3, 4 | FR-022, NFR-007 | `test_cycle.py::test_shared_failure_voids_the_cycle_with_zero_launches__nfr007_fr022` | PASS |
| AC-16 | Origin mismatch exits 2; parity table agrees with `origin_repo.py` | FR-025, NFR-003 | `test_cycle.py::test_origin_mismatch_is_exit_2_before_discovery__fr025` | PASS |
| AC-17 | Each verb's exit codes match section 4; `check-config` and `status` write nothing | FR-026, FR-021 | `test_cli.py::test_once_exits_with_the_exit_code_of_the_cycle` | PASS |
| AC-18 | Rate limit persists `next_permitted_at`, clamps to 3600 s, and `reset --rate-limit` clears it | FR-028 | `test_cycle.py::test_retry_after_120_persists_next_permitted_at_and_blocks_the_next_cycle__fr028_df51` | PASS |
| AC-19 | A sleeping stub ends with `gh_timeout`; no launch starts after 120 s | FR-029, NFR-008 | `test_runner.py::test_real_child_timeout_returns_quickly__nfr008` (split by DF-55 with in-process `test_cycle.py` cases) | PASS |
| AC-20 | Argv prefix scan: only G1 to G7, `--method GET`, no upstream name | NFR-002, NFR-003 | `test_security_invariants.py::test_every_argv_of_the_cycle_is_an_allowed_form` | PASS |
| AC-21 | `test_no_shell.py` passes | NFR-004 | `test_no_shell.py::test_no_shell_forms_in_issue_watch_package` | PASS |
| AC-22 | Crash points C1 to C5 and 50 cycles never exceed one launch per issue | NFR-005, NFR-010, NFR-011 | `test_crash_injection.py::test_c1_crash_before_the_pending_save_leaves_the_store_untouched__nfr005` | PASS |
| AC-23 | No new dependency; gates in section 13 pass | NFR-012 | none (gate-only): gates G-4, G-6, G-10 | PASS (gate-proven) |
| AC-24 | `slo_numbers` returns the four values on a fixture log | NFR-013 | `test_slo_helper.py::test_the_four_numbers_from_one_rotated_fixture_log` | PASS |
| AC-25 | Module-boundary and parity tests pass | NFR-014 | `test_module_boundaries.py::test_package_has_exactly_the_designed_modules` | PASS |

`ac-trace.md` result line: AC rows: 25 (24 PASS by tests, AC-23 PASS by gates). FR rows: 29, NFR rows: 14 (NFR-012 gate-only). All 68 rows PASS. GAPs found and fixed: 14 (docstring-id gaps; no missing test).

## 7. Deviation register (from `deviation-register.md`; locations of each departure are in that file)

Table 1: the 29 authorized departures (R-003 DEVIATION rows). Count: 29 rows, 29 PASS, 0 GAP.

| Id (OQ) | Departs from | Verdict |
|---|---|---|
| DF-01 (OQ-1) | D 265 and S 309: `Runner.run(argv, timeout)`, `run_command` (keyword-only `cwd` added) | PASS |
| DF-02 (OQ-2) | S 330-358 closed reason list (`marker_unreadable`, `edits_unreadable`) | PASS (pin test now holds 59 names; OQ-2 still says 57) |
| DF-03 (OQ-3) | S 330-358; S 358 warning reasons (`operator_reset`) | PASS |
| DF-04 (OQ-4) | D 118 and S 297: no case for `reset N` without an entry (`reset_refused`) | PASS |
| DF-05 (OQ-5) | AC-23 (D 896), D 798, S 366: `make test` locally (full suite: CI only) | PASS (the literal sentence is in final-gate-record.md line 20) |
| DF-06 (OQ-6) | D 177 and D 759 "six verbs" (five commands) | PASS |
| DF-07 (OQ-7) | Build request "no commit step" (Phase 10 commit items) | PASS |
| DF-09 (OQ-8) | D 800 `uv run ruff format --check src/ tests/` (pinned `uvx --offline ruff@0.15.20`) | PASS |
| DF-10 (OQ-9) | D 765 and D 780 committed bash stubs (stubs written into `tmp_path`) | PASS |
| DF-12 (OQ-10) | D 693 row C12, the `property_based` marker (seeded `random.Random(331)`, no marker) | PASS |
| DF-13 (OQ-11) | D 137 (expand `~` only for the default and `--config`) | PASS |
| DF-15 (OQ-12) | D 296 (superseded by D 779), D 784 "rerun" (crash points C1 to C5, 5 reruns) | PASS |
| DF-17 (OQ-13) | D 441 migrated store saved before any other step | PASS |
| DF-18 (OQ-14) | D 572 "item missing a field" | PASS |
| DF-20 (OQ-15) | D 131-132 label rules | PASS |
| DF-22 (OQ-16) | S 330-358 and S 358 (warning reasons) | PASS |
| DF-24 (OQ-17) | D 297-298 names `RecordingLauncher`, `FakeClock(start, step)` | PASS |
| DF-25 (OQ-18) | D 224 `slo_numbers(lines, store, now)` | PASS |
| DF-27 (OQ-19) | D 95 row C14, premise of a collision | PASS |
| DF-28 (OQ-20) | D 102 row C21 "every G2 to G7 argv" (`--method GET` only on REST path calls) | PASS |
| DF-29 (OQ-21) | D 244 "imports the package lazily" (eager import in main.py) | PASS |
| DF-42 (OQ-22) | The design has `record` check `last_reason` membership (D 237-238 forbids the `audit` import) | PASS |
| DF-43 (OQ-23) | Transition table D 476-490 (`fail` allowed from `failed`) | PASS |
| DF-44 (OQ-24) | D 221 and D 350 `sweep(store, now)`, `day_cap_count(store, now)` | PASS |
| DF-48 (OQ-25) | D 776 `Reply` as the `FakeRunner` script value | PASS |
| DF-50 (OQ-26) | S 161, S 163-164, S 196, S 267 (X1 to X5) | PASS |
| DF-55 (OQ-27) | D 892 (AC-19 via a sleeping stub) | PASS |
| DF-57 (OQ-28) | D 399 meets a reason outside S 330-358; exit-6 reasons have spec kind `cycle` (S 336) | PASS |
| DF-60 (OQ-29) | S 384 (runbook inside the design document) | PASS |

Table 2: deviations introduced during execution (no R-003 row authorizes them).

| # | Deviation | Verdict |
|---|---|---|
| 1 | [PROPOSAL] closed reasons `cycle_complete` (kind cycle, exit 0) and `cycle_crashed` (exit 1, stderr only) added to `audit.REASON_TABLE`; the table now has 59 names (R-003 says 57; OQ-2 and OQ-49 still say 57) | PASS |
| 2 | The candidate that stops a cycle gets no decision line (the cycle line carries the stop reason) | PASS |
| 3 | The cycle-start origin check with no time left ends exit 3 `gh_timeout`; the per-issue origin re-check with no time left skips with `budget_exhausted` | PASS |
| 4 | Gate C cycle 2 added a `launch_allowed()` re-check after the origin re-check | PASS |
| 5 | `status` prints the bare orca name `orca-ide` for the retry argv when `which` resolves none (OQ-50), not a resolved path | PASS |
| 6 | `status_report`'s `audit` parameter is accepted and unused | PASS |
| 7 | Sub-agents executed the gate and fix items with pointer prompts instead of pasted prompts | PASS (process deviation) |
| 8 | One design-correctness Gate C report was overwritten by a mis-targeted agent and restored from its transcript; the second run is kept as `-run2` | PASS |
| 9 | Python 3.10.20 was found and used by Gate D although the task text says none exists | PASS (the task text is stale; the code is unaffected) |

Register notes: GAPs found: none. Stale counts live in the task text, not in the code (OQ-2 and OQ-49 say 57 reason names; the tree has 59; DF-09 and OQ-43 say no 3.10 interpreter exists).

## 8. Gates A to D: verdict and fix-cycle count (copied from `phase-outputs/plans/gate-[abcd]-verdict.md`)

| Gate | Phases | Verdict | Fix cycles used | Blocking findings fixed (per cycle) | Post-fix record |
|---|---|---|---|---|---|
| A | 2 and 3 | PASS | 2 | cycle 1: 18 (A-1 to A-18); cycle 2: 1 (A-7) | `gate-a-postfix-cycle2.txt`: pytest 686 passed, `make lint` exit 0, pinned ruff clean |
| B | 4 and 5 | PASS | 1 | cycle 1: 13 (B-1 to B-13); cycle 2 not run | `gate-b-postfix.txt`: 1577 passed, `make lint` exit 0, pinned ruff clean |
| C | 6 and 7 | PASS | 2 | cycle 1: 13 (C-1 to C-13); cycle 2: 1 (C2-1, from the new finding N-1) | `gate-c-postfix-cycle2.txt`: 2243 passed, `make lint` exit 0, pinned ruff clean |
| D | 8 | PASS | 1 | cycle 1: 3 (D-1 to D-3); cycle 2 not run | `gate-d-postfix.txt`: pytest 2628 passed, `make lint` 0 errors and 5 warnings (ruff check all passed), pinned ruff check clean, 31 files already formatted |

Minor notes are carried forward and never rechecked: A-19 to A-72 plus cycle-2 notes M-5 to M-7 (Gate A), B-14 to B-67 (Gate B), C-14 and following (56 notes) plus M-1 to M-3 (Gate C), D-4 and following (34 notes, including CE-1: wrong requirement id AC-17 in `test_crash_injection.py`) (Gate D).

## 9. Staging statement

No path under `.claude/`, `.dev/issues/` or `.dev/brainstorms/` is staged. Evidence from this step: `git diff --cached --name-only` printed 161 paths, all under `.dev/tasks/` (0 outside); `grep -c '^\.claude/'`, `grep -c '^\.dev/issues/'` and `grep -c '^\.dev/brainstorms/'` over that list each printed 0. `.dev/issues/331/` and `.dev/brainstorms/20261107-064825-github-issue-watcher/` are untracked on purpose (the `??` lines in section 3). No path under `.claude/` appears in the change set or in `git status --short`. The deliverables (source, tests, runbook and the `main.py` edit) are not yet staged; Phase 10 stages them through its allowlist.
