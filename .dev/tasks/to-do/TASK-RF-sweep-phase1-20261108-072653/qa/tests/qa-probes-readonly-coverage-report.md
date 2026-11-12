# QA Report - Probes and read-only coverage lens (T225)

**Date:** 2026-11-12
**Phase:** code gate, tests (probes + read-only coverage lens)
**fix_authorization:** false
**Scope:** DESIGN section 11 rows for test_probes_allowlist.py and test_readonly.py mapped to tests.

**Authority read:** `docs/designs/orchestrator-mode.md` (the revised DESIGN) section 11 rows at lines 758 (`test_readonly.py`) and 759 (`test_probes_allowlist.py`), section 7.1 (353-447), 7.2 line 511, 7.3 (519-559), section 12 rows 785-819. Later revision folders (`revisions/chat-output-exception-*`, `revisions/plan-defect-fixes-*`) do not touch these two rows (grep found no mention).
**Files read in chunks of at most 150 lines:** `tests/sweep/test_probes_allowlist.py` (1-1934), `tests/sweep/test_readonly.py` (1-528), `tests/sweep/conftest.py` (1-334), `src/superclaude/cli/sweep/probes.py` (100-340, 491-545, 560-630, 740-850, 1240-1300), `src/superclaude/cli/sweep/commands.py` (128-228), result maps `test-readonly.txt` (1-72) and `test-probes-allowlist.txt` (name and heading scan, lines 277-321), `phase10-validation.md` (1-80).

## Method

1. Listed every case in the two DESIGN rows and mapped each to a test (tables below).
2. Read each mapped test and compared its assertion with the assertion DESIGN states.
3. Ran `uv run pytest tests/sweep -v` (559 passed), the two files alone (266 passed, no warnings, so the real-git control was conclusive), `uv run ruff check` and `uv run ruff format --check` on `src/superclaude/cli/sweep tests/sweep` (both clean).
4. Mutation experiments on a private copy under `/tmp` (deleted afterwards; no repository file changed): 25 runs (1 pristine, 24 mutations), results in the Mutation table.
5. Re-ran the two files in reversed order in a private copy: 266 passed (no order dependence).

## Case-to-test map: `test_probes_allowlist.py` row (DESIGN line 759)

| # | DESIGN case | Test (file `tests/sweep/test_probes_allowlist.py`) | Assertion matches DESIGN |
|---|---|---|---|
| P1 | each full-sweep argv equals one template token for token | `test_full_sweep_records_only_template_argv` (538-550); `_is_template_argv` (105-113) | yes; also pins 1+2+5+1 calls |
| P2 | argv[0] is `$ORCA_CLI_COMMAND` when set, else `orca-ide` | `test_argv0_is_orca_ide_by_default_then_orca_cli_command` (521-535), `test_full_sweep_argv0_follows_orca_cli_command` (570-581), `test_orca_binary_*` (511-518) | yes; also stdin DEVNULL, timeout, check=False |
| P3 | zero argv for the four "not called" templates | `test_full_sweep_issues_zero_argv_for_the_not_called_templates` (553-567, 4 params) | yes |
| P4 | exact-set pin of the ten templates | `test_allowed_orca_is_exactly_the_ten_templates` (340-342), `..._names_seven_verbs` (345-358), `test_other_allowlist_constants_are_pinned` (361-366) | yes (tuple equality, so order is pinned too) |
| P5 | negatives raise `ValueError` before a subprocess: `check`, `inbox`, `worker-read`, `gate-list`, extra flag, `--include-remote`, `run-list` | `NEGATIVE_ARGV` (388-418, 24 cases incl. all seven named) with `test_negative_argv_raises_value_error_before_a_subprocess` (421-427: raises from `check_orca_argv` and `_orca`, and `fake_run.calls == []`) | yes |
| P6 | positive: both `worktree ps --agent-wait` templates accepted | `test_worktree_ps_agent_wait_templates_are_accepted` (374-385), `test_every_template_is_accepted` (369-371) | yes |
| P7 | FR-021 forbidden list held in the test | `FORBIDDEN_VERBS` (76-89, the same 12 words as DESIGN line 553), `test_fr021_forbidden_verbs_are_in_no_template_and_are_refused` (439-451), `test_probes_source_holds_no_write_verb_even_as_a_string` (454-463) | yes (see F4) |
| P8 | git negatives: `rev-parse`, `log`, `branch`, `--version`, any `stash` form | `GIT_NEGATIVE` (466-485, 18 cases incl. 7 stash forms) with `test_git_negatives_raise_value_error_before_a_subprocess` (488-494) | yes |
| P9 | each unavailable cause on call one | `FIRST_CALL_CAUSES` (779-810) with `test_each_unavailable_cause_on_call_one_stops_the_binding` (813-828); `test_nonzero_exit_is_unavailable_on_call_one_and_call_failed_later` (831-839); `test_wrong_shape_list_reply_..._call_one_..._later` (867-884) | yes |
| P10 | quoted-marker negative fixture | `CLASS_CASES` ids `quoted-marker-in-stderr-line`, `marker-on-second-stderr-line`, `marker-inside-error-message`, `marker-in-plain-stdout`, `marker-inside-an-ok-result` (642-671) | yes |
| P11 | middle `worker-show` exit 1 | `test_a_middle_worker_show_failure_leaves_the_sweep_going` (920-953; exit 1 and malformed zero-exit) | yes |
| P12 | malformed zero-exit body | `CLASS_CASES` `zero-exit-*` (673-708) | yes |
| P13 | empty `run-current` body | `test_empty_run_current_body_is_call_failed_invalid_response` (747-756) | yes |
| P14 | captured no-binding fixture | `test_captured_no_binding_fixture_is_no_binding` (759-776); fixture `fixtures/captured-run-current.json` exists | yes |
| P15 | `collect` source rows and `truncated` (six sub-cases) | `test_collect_worker_list_source_rows_and_truncated` (1177-1213: names with `ORCA_CLI_COMMAND` set, R2 unscanned, R1 None, failed `task-list R2`, 100 rows True, 99 rows False); `..._budget_spent_before_r2` (1216-1238); `..._orca_tabs[missing/empty/unreadable]` (1241-1268) | yes |
| P16 | budget: 60 rows give 50 shows and `bound_reached` 10 | `test_60_rows_give_50_worker_show_and_bound_reached_10` (1065-1080) | yes |
| P17 | 50 rows give 50 and 0 | `test_50_rows_give_50_worker_show_and_bound_reached_0` (1083-1095) | yes |
| P18 | 2 Runs of 40 get 25 each | `test_two_runs_of_40_rows_get_25_shows_each` (1098-1113) | yes (also `bound_reached` 30) |
| P19 | with 20 s left the per-call timeout is at most 20 s | `test_with_20_s_left_the_per_call_timeout_is_at_most_20_s` (978-985), `test_with_20_s_left_every_orca_timeout_is_at_most_20_s` (1044-1062) | yes |
| P20 | full-timeout fakes finish under 120 s and still publish | `test_full_timeout_fakes_finish_under_120_s_and_still_publish` (1116-1147), `test_every_call_timing_out_still_collects_and_publishes` (1150-1169) | partly: elapsed 90 s and `report.render` are asserted; nothing is published (F1) |
| P21 | contract over 1 MiB unscanned with a reason | `test_a_contract_over_1_mib_is_unscanned_with_a_reason` (1349-1359) | yes (`over 1 MiB`) |
| P22 | ledger over 1 MiB read as head and tail (GQ-105) | `test_ledger_over_the_limit_is_read_as_head_and_tail` (1328-1333), `test_ledger_tail_drops_a_first_line_that_the_cut_split` (1336-1346), `test_ledger_size_boundary` (1319-1325) | yes (only the tail is searched, as DESIGN line 62 says) |
| P23 | nine boundary fixtures (limit -1, at, +1) for 1 MiB contract and ledger, 256 KiB transcript tail, 8 MiB output | `BOUNDARY` (1275-1279) used by `test_contract_size_boundary`, `test_ledger_size_boundary`, `test_transcript_tail_boundary`, `test_subprocess_output_boundary_for_orca`, `test_subprocess_output_boundary_for_git` = 15 fixtures; `test_byte_limits_are_pinned` (1282-1288) | yes; limit hit only when size is over it |
| P24 | worktree directory deleted between the seams | `test_worktree_removed_between_the_seams_is_unscanned_and_the_others_continue` (1449-1483, `stat-fails` and `git-fails`) | yes |
| P25 | list and show disagree, show value used (443) | `test_list_and_show_disagree_and_the_show_value_is_used` (1486-1512) | yes |
| P26 | one missing and one extra `worker-show` key (446) | `test_one_missing_and_one_extra_worker_show_key_raise_nothing` (1528-1545), `test_a_show_of_the_wrong_shape_raises_nothing` (1548-1555) | yes |
| P27 | symlink-out fixture `unscanned: outside root` (450) | contract (1558-1574), ledger (1577-1592), transcript (1595-1612), tab-map entry (1615-1630) | yes (four sources) |
| P28 | contract changed between two reads: one re-read; changes every read: `conflict: inconsistent observation` (451) | `test_a_contract_changed_between_two_reads_is_re_read_once` (1649-1663, exactly 2 reads), `test_a_contract_that_changes_on_every_read_is_an_inconsistent_observation` (1666-1687, 2 reads, row text) | yes (budget half unpinned, F5) |
| P29 | duplicate Dispatch with two states: one `orca:<dispatch>` row, `conflict: duplicate Dispatch rows disagree` (452) | `test_duplicate_dispatch_rows_with_two_states_give_one_conflict_row` (1690-1711) | yes |
| P30 | `parse_status`: `ahead 3`, upstream no ahead, no upstream, `[gone]`, detached HEAD, `No commits yet` | `STATUS_HEADERS` (1718-1741, 8 cases) with `test_parse_status_branch_header` (1744-1754) and `test_read_worktree_unpushed_follows_the_branch_header` (1769-1783) | yes |
| P31 | rename pair in `-z` form | `test_parse_status_rename_pair_in_z_form` (1786-1799; also a copy pair) | yes |
| P32 | `??` path under `.dev/tasks/` | `test_parse_status_untracked_path_under_dev_tasks` (1802-1807), `test_read_worktree_untracked_dev_tasks_path_is_unsaved_and_marks_the_package_active` (1810-1824) | yes |
| P33-P35 | R3-B1 transcript time fields (3 tests) | `test_read_transcript_tail_sets_first_and_last_record_ts` (1832-1848), `..._first_record_ts_is_minimum` (1851-1862), `..._over_256k` (1865-1880) | yes (values, aware UTC, `tail_complete` as DESIGN states) |
| P36-P38 | R3-B1 `worker-show` Dispatch times (3 tests) | `test_worker_show_dispatch_times_sqlite_form` (1883-1898), `..._iso_z_form` (1901-1916), `..._missing_or_bad` (1919-1934) | yes |

## Case-to-test map: `test_readonly.py` row (DESIGN line 758)

| # | DESIGN case | Test (file `tests/sweep/test_readonly.py`) | Assertion matches DESIGN |
|---|---|---|---|
| R1 | every recorded `_git` argv has `--no-optional-locks` at index 1 and `-C <path>` after it | `test_git_argv_and_env_are_lock_free` (73-91: argv[0..4], real `_git` over a recorder); `test_collect_reaches_git_with_a_lock_free_argv_for_each_worktree` (144-158) | yes. The same assertion at line 453 is vacuous (F2) |
| R2 | the child env holds `GIT_OPTIONAL_LOCKS=0` | same two tests (89, 158); a caller value `1` is set first (74-76) | yes |
| R3 | one git argv per discovered worktree | `test_collect_makes_one_git_call_per_worktree_that_ps_reports[0/1/2 extra]` (129-141) | yes |
| R4 | real-git test: control | `test_real_git_lock_free_status_and_gitignore` (471-528), lines 506-528 | partly: warns only when inconclusive (F3) |
| R5 | `check-ignore .dev/sweeps/x.md` succeeds | line 496 (`returncode == 0`) | yes |
| R6 | `check-ignore .dev/tasks/to-do/x.md` fails | line 498 (`returncode == 1`, not just non-zero) | yes |
| R7 | a file under `.dev/sweeps/` leaves `git status --porcelain` unchanged | lines 500-504 (`== before == ""`) | yes |
| R8 | snapshot diff (path, size, `st_mtime_ns`, SHA-256) over root, `HOME`, XDG dirs: exactly one added report plus the output directory when new | `test_sweep_run_adds_exactly_one_report_and_changes_nothing_else[nothing/dev/sweeps]` (367-389) over `sweep_env.paths` (340-346: root, HOME, state, three XDG dirs, sibling worktrees); helper `snapshot`/`diff`/`assert_only_added` (164-215) | yes (directories recorded by kind only, F7) |
| R9 | no temp file and no second name for the report after exit 0 | `test_no_temp_file_and_no_second_name_remain_after_exit_0[...]` (392-404: directory listing is exactly the report, `st_nlink == 1`, no `.tmp`; the real temp name is a dotfile `.{stem}.{pid}.tmp`, `commands.py:168`) | yes |
| R10 | the check cannot pass vacuously | `test_snapshot_diff_detects_each_kind_of_change` (264-289, 7 kinds), `..._overlapping_paths_once` (292-297), `test_the_snapshot_check_catches_a_stray_write_made_during_the_run` (407-428) | yes |
| R11 | (Covers) NFR-013, no process start | `test_the_subprocess_guard_is_live_in_this_module` (434-437), `test_a_sweep_starts_no_process_and_records_only_allowlisted_argv` (440-458); guard `conftest.py:22-42`; exactly one `integration`-marked test in `tests/sweep` (grep) | yes |

## Mutation experiments (private copy under /tmp, deleted afterwards)

Each run applied one source edit to a copy of `src/superclaude` and `tests/sweep`, then ran the two files. "Killed" means at least one test failed.

| Mutation | Result | Killed by |
|---|---|---|
| default binary `orca-ide` to `orca` | killed (6+ tests) | `test_orca_binary_default_...`, `test_argv0_...`, `test_full_sweep_records_only_template_argv` |
| `_git` argv drops `--no-optional-locks` | killed (4) | `test_the_one_git_call_is_accepted`, `test_full_sweep_runs_one_lock_free_git_status_per_worktree`, `test_git_argv_and_env_are_lock_free`, `test_collect_reaches_git_with_a_lock_free_argv_for_each_worktree`; NOT `test_a_sweep_starts_no_process_...` (confirms F2) |
| `_git` env drops `GIT_OPTIONAL_LOCKS=0` | killed (2) | `test_git_argv_and_env_are_lock_free`, `test_collect_reaches_git_...` |
| output limit `>` to `>=` (orca) / (git) | killed (1 each) | `..._boundary_for_orca[at-the-limit]`, `..._for_git[at-the-limit]` |
| output limit counts stdout only | killed (2) | `[limit-plus-1]` cases |
| ledger / transcript / contract limit `>` to `>=` | killed (1 each) | the `[at-the-limit]` cases |
| template match becomes prefix match | killed | `extra-flag`, `run-current-with-json` negatives |
| `_orca` stops calling `check_orca_argv` | killed | `check`, `inbox`, `worker-read`, ... negatives |
| `_stable` single read / three reads | killed (2 / 1) | the two changed-contract tests |
| show cap 50 to 51 | killed (6+) | budget and cap tests |
| `worker-list` truncation `>=` to `>` | killed | `test_collect_worker_list_source_rows_and_truncated` |
| `parse_status` drops the rename old path | killed | `test_parse_status_rename_pair_in_z_form` |
| `collect` also calls `worktree list --json` / `worktree ps --agent-wait` | killed (6 each) | the four zero-argv tests, `test_full_sweep_records_only_template_argv`, `test_a_sweep_starts_no_process_...` |
| `_publish` leaves its temp file | killed (6) | R8 and R9 tests |
| `_publish` writes a stray file in `HOME` / in `XDG_DATA_HOME` | killed (3 each) | R8 tests |
| real-git test: drop `--no-optional-locks` and the env var from its own argv | killed | `test_real_git_lock_free_status_and_gitignore` (the control discriminates) |
| remove the `FORBIDDEN_TOKENS` check | SURVIVED | equivalent: no template can match an argv holding `--include-remote`, so exact template matching already rejects it (probes.py:208-215) |
| `Budget.call_timeout` `< 1.0` to `<= 1.0` | SURVIVED | no test at exactly 1 s left (F6) |

Canary: the pristine copy gave 266 passed, and the first mutation proved the copy under `/tmp` was the code under test.

## Findings

No BLOCKING and no MAJOR finding. Every DESIGN case in the two rows has a test, and 22 of 24 mutations were caught. The eight findings below are MINOR (recorded as notes; they never fail the gate).

| Id | Severity | Evidence | What is wrong | Smallest fix |
|---|---|---|---|---|
| F1 | MINOR | `tests/sweep/test_probes_allowlist.py:1116-1147` (render at 1144-1147), `1150-1169` (render at 1168-1169); DESIGN line 759 "full-timeout fakes finish under 120 s and still publish"; result map `test-probes-allowlist.txt:292` says "the report renders" | Both tests are named "..._publishes" but assert only the fake-clock elapsed time (90 s) and that `report.render` returns text. `commands._publish` is not run under a cut budget. Publication and the every-call-times-out path are each covered elsewhere (R8 tests; the FR-019 disk-only continuation in `test_cli_contract.py`), so no defect was found, but the combined case DESIGN names is not asserted. | Add one `CliRunner` case that patches `probes.Budget`'s clock so the budget is cut mid-run, and assert exit 0 and one report file; or reword the DESIGN case and the test names to "still render". |
| F2 | MINOR | `tests/sweep/test_readonly.py:453`; `tests/sweep/conftest.py:71` | `all(c["argv"][:3] == ["git", "--no-optional-locks", "-C"] ...)` reads the `argv` that `GitFake` builds itself (conftest.py:71), so it can never fail. The result map `test-readonly.txt:70-72` presents it as evidence of "the lock-free prefix". The mutation that removes `--no-optional-locks` from `_git` did not fail this test (it failed four others, which carry the real coverage). | Delete line 453, or point it at the `recorder` fixture. |
| F3 | MINOR | `tests/sweep/test_readonly.py:513-519` and `523-528` | The real-git test runs its own literal argv and env, not `probes._git`, so it does not exercise the seam end to end. The control (a plain `git status` must rewrite the stat-dirty index) only calls `warnings.warn` when it is inconclusive, so on a git or filesystem where it is inconclusive the lock-free assertion passes vacuously. Today the control is conclusive: mutation X (dropping the flag and env in the test) failed the test, and `-rw` showed no warning. | Call `probes._git(repo, *STATUS_ARGS, timeout=30.0)` for the lock-free run, and turn the inconclusive-control warning into `pytest.skip`. |
| F4 | MINOR | `tests/sweep/test_probes_allowlist.py:454-463` | The "no write verb even as a string" check scans `probes.py` only and exempts `dispatch`. DESIGN line 553 says "the package". Today it holds: a grep of every `src/superclaude/cli/sweep/*.py` for the 12 quoted verbs finds only the `show["dispatch"]` JSON key (probes.py:422-433). The claim is not pinned for the other modules. | Scan all `src/superclaude/cli/sweep/*.py` and exempt only the `dispatch` key by context. |
| F5 | MINOR | DESIGN line 511 and line 808 (NFR-007: "one re-read of a changed input only while the budget allows"); `src/superclaude/cli/sweep/probes.py:563-570` (`_stable` takes no budget); tests at `test_probes_allowlist.py:1649-1687` | DESIGN says that with no budget left the changed input is `conflict: inconsistent observation` without a re-read. `_stable` always re-reads, and no test has a spent budget. The row text for the test file does not name this half, so this is a section 7.2 / section 12 gap, not a section 11 gap. Already recorded as CORE-F40 / edge-case M4 (minor) in `qa/impl-core/`. | Pass the `Budget` to `_stable` and add one test with a spent budget; or narrow the DESIGN sentence. |
| F6 | MINOR | `tests/sweep/test_probes_allowlist.py:961-975`; probes.py:172 | `call_timeout` returns None "below 1 s left" (DESIGN line 371); the test checks 0.5 s only. Mutation `< 1.0` to `<= 1.0` survived. | Add a case with exactly 1.0 s left expecting `1.0`. |
| F7 | MINOR | `tests/sweep/test_readonly.py:171-175` | DESIGN line 758 says the snapshot records path, size, `st_mtime_ns` and SHA-256. Directories are recorded by kind only, so a mode change or a directory-only change that adds and removes nothing is invisible. A new or removed child is still reported. | Record `st_mode` for directories. |
| F8 | MINOR | `tests/sweep/test_readonly.py:129-158`, `440-458` | `ps` listing the root itself is not tested (no dedupe case for "one git argv per discovered worktree"); DESIGN line 758 does not require it, so this is a note only. | None required. |

## Self-audit

- Zero BLOCKING findings is not a skipped check: 24 mutations plus a pristine run, two full-file reads (1934 and 528 lines, in chunks of at most 150), a full-suite run, and a reversed-order run back it. The two survivors were examined: one is an equivalent mutant, one is F6.
- Everything cited was read from disk in this session; line numbers are from those reads.
- Not verified here: whether `git` on the CI host rewrites a stat-dirty index (F3); no CI run was made.
- No live Orca, ccsession or Claude command was run. No repository file was changed except this report; `.pytest_cache` was not created (`-p no:cacheprovider`).

**Tool engagement:** Read: 32 | Grep: 9 | Glob: 1 | Bash: 12 (one batch script for the 25 mutation runs, one for the suite and reversed-order runs; the rest are listings and line reads). No web research (no Tavily or fallback calls).

## Checks

| Check | What was checked | Result |
|---|---|---|
| C1 | Exact-set pin of the ten templates, seven verbs, constants (P4) | PASS |
| C2 | Orca negatives raise `ValueError` before any subprocess, including the seven named (P5) | PASS |
| C3 | Positive acceptance of both `worktree ps --agent-wait` templates (P6) | PASS |
| C4 | FR-021 forbidden list held in the test, refused, absent from `probes.py` (P7) | PASS (F4 note) |
| C5 | Git negatives and the one allowed git call (P8) | PASS |
| C6 | Full-sweep recording: template match, argv[0], zero argv for the four "not called" templates (P1-P3) | PASS |
| C7 | Result classes: unavailable causes on call one, quoted-marker negatives, middle `worker-show`, malformed body, empty `run-current`, captured no-binding (P9-P14) | PASS |
| C8 | `collect` source rows and `truncated` (P15) | PASS |
| C9 | Budget cases (P16-P20) | PASS (F1, F6 notes) |
| C10 | Byte limits and the nine boundary fixtures, mutation-checked (P21-P23) | PASS |
| C11 | Six failure modes: lines 440, 443, 446, 450, 451, 452 (P24-P29) | PASS (F5 note) |
| C12 | `parse_status` cases (P30-P32) | PASS |
| C13 | R3-B1 time fields, six tests (P33-P38) | PASS |
| C14 | `test_readonly.py` recorded argv, env, one git argv per worktree (R1-R3) | PASS (F2 note) |
| C15 | Snapshot diff: one added report, output dir when new, no temp, no second name, non-vacuous (R8-R10) | PASS (F7 note) |
| C16 | Real-git test: control, two `check-ignore` results, status unchanged (R4-R7) | PASS (F3 note) |
| C17 | NFR-013 guard live, exactly one `integration`-marked test (R11) | PASS |
| C18 | Mutation sensitivity of the assertions (25 runs, 2 survivors explained) | PASS |
| C19 | `uv run pytest tests/sweep -v` 559 passed; two files 266 passed in both orders; ruff check and format clean | PASS |
| C20 | Result maps `test-probes-allowlist.txt` and `test-readonly.txt`: every test name they cite exists; claims match the tests except the two noted in F1 and F2 | PASS (F1, F2 notes) |

Verdict: PASS
Blocking count: 0


