# Verify cycle 1 - rf-qa (tests gate)

**Date:** 2026-11-12
**Role:** verifier, `fix_authorization: false`
**Inputs:** consolidated-findings-cycle0.md (F_0 = TST-F1 to TST-F6), fix-log-cycle1.md, cycle-ledger.md (102 cycle-0 PASS ids), tests/sweep/, six result maps, phase10-validation.md, DESIGN sections 7.4, 7.5, 11, 12, src/superclaude/cli/sweep/.

Sections are appended below as each part is finished.

## Method and evidence base

- Read from disk now: `consolidated-findings-cycle0.md`, `fix-log-cycle1.md`, `cycle-ledger.md`, the seven `qa-*-report.md` (all check descriptions), the new or changed tests (`test_cli_contract.py:508-531` and `:1018-1038`; `test_report.py:66`, `:571-613`, `:1162-1247`; `test_probes_allowlist.py:1362-1383`; `test_classify.py:550-579`, `:999-1048`), DESIGN 7.5 (header block) and `report.py:164-192`.
- Runs in the repository (read-only effect): `uv run pytest tests/sweep` gives `573 passed in 1.66s`; `uv run pytest tests/sweep -m integration` gives `1 passed, 572 deselected`; `uv run ruff check src/superclaude/cli/sweep tests/sweep` gives `All checks passed!`; `uv run ruff format --check ...` gives `15 files already formatted`.
- Change accounting, independent of the fix log: `sha256sum -c /tmp/t232-src-before.sha` (the executor's pre-fix record) prints OK for all 6 modules under `src/superclaude/cli/sweep/`; `sha256sum -c /tmp/t232-protected-before.sha` prints OK for all 20 files under `tests/sweep/fixtures/` (19 captured fixtures and `SOURCES.md`), `phase10-validation.md`, DESIGN and every QA report, and FAILED only for the plan file `TASK-RF-sweep-phase1-20261108-072653.md` (the executor's own progress file, not a gate input). File times: only `test_cli_contract.py` (05:43), `test_probes_allowlist.py` (05:45), `test_classify.py` (05:45), `test_report.py` (05:48) and the four result maps (05:47-05:48) are newer than the cycle-0 reports (05:24-05:38); `conftest.py` (04:04), `test_readonly.py` (04:44), `test_cli_registration.py` (04:59), every module under `src/` and `phase10-validation.md` (05:17) are older. Test counts per file went 159/90/3/242/24/41 (cycle-0 determinism report, E4) to 161/94/3/243/24/48; the deltas (+2, +4, 0, +1, 0, +7 = 14) equal the tests the fix log says it added, so no test was removed.
- Private experiments only under a `/tmp/ironclaude-batch.*` directory (a copy of `src/superclaude`, `tests/sweep`, `tests/conftest.py`, `pyproject.toml`, `.gitignore`, run through `PYTHONPATH`), removed at the end; no repository file was edited. Results are in the sections below.

## Findings F_0

### TST-F1 (MAJOR): RESOLVED

- Fix on disk: `tests/sweep/test_cli_contract.py:1018` `test_json_worktree_values_are_exact_and_removable_is_never_yes` asserts, for both worktrees of `_captured_world`, `status_read is True`, `uncommitted is False`, `unpushed is None`, `removable == "no"`, `removable_reason == "unpushed branch: no upstream"` (`:1026-1033`) and `all(w["removable"] in ("no", "could not determine") ...)` (`:1035-1037`), which is the smallest fix of the finding.
- Independent discrimination: mutation `report.py:653` `"removable": w.removable,` to `"removable": "yes",` in the private copy: 1 failed, 572 passed; failing test `test_json_worktree_values_are_exact_and_removable_is_never_yes`. Cycle-0 had 559 passed for the same mutation.

### TST-F2 (MAJOR): RESOLVED

- Fix on disk: `test_report.py:571` `test_header_has_the_seven_exact_lines_of_design_7_5` compares `header_block(text)` with the seven lines, including `Orca binary: orca-ide`, `Sources: orca worker-list R1 read (age 5s) . remote hosts unknown`, `Messages coverage: partial`, `Orca lock risk: UNVERIFIED (checked for Orca 1.4.245; observed unknown)` and the `Untracked paths:` line; `:591` pins `Sources: none`; `:607` is the banner test (3 ids: `ps-unscanned` and `orca-unavailable` expect the banner in the header and printed once, `complete` expects none); `:66` `WORKTREES_BANNER` is a literal copy of the DESIGN 7.5 text, not an import from `report.py`. The seven lines agree with DESIGN 7.5 and `report.py:164-192`.
- Independent discrimination (private copy, `report.py`): `Messages coverage: complete` killed (1 test); `Orca binary: orca` literal killed (2); `Untracked paths:` text changed killed (1); `Sources:` line replaced by `none` killed (1); the `(age Ns)` suffix dropped killed (1); banner never printed killed (4, including `[ps-unscanned]` and `[orca-unavailable]`); banner always printed killed (2, including `[complete]`); cycle-0 survivors M3 (`_discovery_incomplete` ps-unscanned branch returns False), M19 (Messages line removed), M23 (Orca binary line removed) and M24 (Sources line removed) all killed now.

### TST-F3 (MAJOR): RESOLVED

- Fix on disk: `test_cli_contract.py:517` `test_window_reaches_the_classification[1h-is-idle|12h-is-active|2h-edge-is-active]` writes a transcript 2 h before `env.now` and runs `--window=<w>` through the command; it asserts class `idle` with `summary.historical == 1`, `visible == 0`, `counts.idle == 1` for `1h`, and `person session (active)` with `historical == 0` for `12h` and for the edge `2h` (`last_activity == window_start`).
- Independent discrimination: M9 (`commands.py:267` window_start fixed at 6 h) killed by `[1h-is-idle]`; an extra mutant, `window_start` one second later than `now - span`, killed by `[2h-edge-is-active]`; the rule-8 comparison `>=` changed to `>` (`classify.py:314`) killed by `[2h-edge-is-active]` and `test_5h_old_row_is_idle_only_when_window_is_under_5h[5-person_active]`.

### TST-F4 (MAJOR): RESOLVED

- Fix on disk: `test_report.py:1183` `test_lifecycle_health_and_result_cells_come_from_the_classifier` and `:1216` `test_freshness_cell_comes_from_the_classifier_for_a_fresh_and_a_stale_transcript`; both build a `sweep_input`, call `classify_all` and `report.render`, and read the printed Sessions cells with `dimension_cells` (`:1162`); no dimension value is set by hand. The first pins `(Lifecycle, Health, Result, Freshness)` for four rows: settled/succeeded, settled/failed, running/no contract, no-outcome/blocked (`null`); the second pins `fresh (300s)`, `stale (25200s)` and the `freshness`/`freshness_age_s` of a stale readable transcript.
- Independent discrimination (private copy, `classify.py`): M12 (`_lifecycle` always `running`), M13 (`failed result` to `unknown`), M14 (blocked `null` to `blocked`) each killed by the first test; M15 (fresh and stale swapped) and M16 (`freshness_age_s` set to 0) each killed by the second.

### TST-F5 (MAJOR): RESOLVED

- Fix on disk: `test_probes_allowlist.py:1362` `test_contract_mtime_and_source_age_come_from_the_file_time` writes a contract, `os.utime` to `NOW - 1 h` (whole seconds, so the float is exact), patches `probes._utcnow` to `NOW` with `monkeypatch`, then asserts `read_contract(path, root).mtime == NOW - 1h` (aware), the `contract <dispatch>` source row is `("read", 3600)` and the collected `ContractRecord.mtime` is the same value.
- Independent discrimination (private copy, `probes.py`): A1 (`_age` returns 0), A2 (source row age `None`), A3 (contract `mtime` read as epoch 0): each killed by this test only (1 failed, 572 passed).

### TST-F6 (MAJOR): RESOLVED

- Fix on disk: `test_classify.py:550` pins `("orca_exit_proof", STALLED)` for exit proof with `transcript_readable=None` and `("fallback", UNKNOWN)` for `False`; `:564` does the same through `classify_all` and asserts `row.transcript_readable is None`; `:999-1048` `test_fr010_exemptions_never_become_idle` is parametrized with the exact `(rule, class)` per case (`unreadable-transcript`, `unknown-timestamp`, `open-task`, `unread-report-candidate` give `("fallback", UNKNOWN)`; `explicit-wait` gives `("waiting_signal", WAITING)`) and its rows use `last_activity=at(1)`, outside the 6 h window.
- Independent discrimination (private copy, `classify.py`): M3 (`is not False` to `is True`) killed by both new rule-2 tests; M5 (rule 8 window test removed) killed by `[open-task]` and `[unread-report-candidate]`.

### Blocking count after the fix

All six `F_0` findings are RESOLVED, so the open count from `F_0` is 0.

## Regression experiments (private copy, deleted afterwards)

| Experiment | Result |
|---|---|
| Whole suite in the private copy, unchanged | 573 passed (the copy is the code under test: every mutation above changed the result) |
| Suite under an audit hook (`sys.addaudithook`) in file order, reversed order and rotated order | 573 passed each; 9 `subprocess.Popen` events per run, all `/usr/bin/git` with `-C <tmp>/repo`, all owned by `test_real_git_lock_free_status_and_gitignore`; 0 process events in a reversed run with `-m "not integration"`; 0 `WRITE_OUTSIDE` or `MUTATE_OUTSIDE` events owned by a test (the 10 outside events have no owning test: pytest start-up temp files); 0 `READ_HOST` events (`/opt/Orca`, `~/.claude`, `~/.local/state`, `~/.config`, `~/.aidev*`); 166 `Path.home()` calls, 0 outside the test temp folder; one relative `os.remove(".git")` inside `test_worktree_removed_between_the_seams_is_unscanned_and_the_others_continue[stat-fails]` (the same event the cycle-0 isolation report explains as a directory-fd `rmtree` of a folder under `tmp_path`) |
| Each of the 6 test files alone; the 6 files in reverse file order; the suite listed twice in one process (`--keep-duplicates`) | 161, 94, 243, 48, 24, 3 passed; 573 passed; 1146 passed |
| Every one of the 573 node ids alone in its own process (8 in parallel) | 0 failures |
| `TZ` = Pacific/Kiritimati, America/Adak, Asia/Kolkata, UTC | 573 passed each |
| `LC_ALL`/`LANG` = C and C.utf8 | 573 passed each |
| `PYTHONHASHSEED` = 0, 1, 2, 99 | 573 passed each |
| `probes._utcnow` and `commands.datetime` shifted to 1970-01-01, 2036-01-01 and 2026-11-08T12:00:00Z | 573 passed each |
| Scrubbed environment (`env -i`, `ORCA_CLI_COMMAND=/bin/false`, `COLUMNS=20 NO_COLOR=1 TERM=dumb`); run from cwd `/` | 573 passed each |
| Cycle-0 probes and read-only mutations re-run (default binary `orca`; `git` argv without `--no-optional-locks`; env without `GIT_OPTIONAL_LOCKS`; orca and git output limit `>=`; `_stable` single read; ledger and contract limit `>=`; show cap 51) | all killed (probes tests 1 to 9 failing each) |
| Cycle-0 classify note mutations re-run (MU6, MU7, MU9, plus the tab-map and truncated notes dropped) | all killed |
| Known MINOR survivors (not in `F_0`): `bound_reached >= 1` to `>= 2` (TST-F24), `call_timeout` `< 1.0` to `<= 1.0` (TST-F18) | still survive, as recorded in cycle 0; MINOR, not rechecked |
| Result maps: pytest `-v` lines of `test-classify.txt`, `test-cli-contract.txt`, `test-probes-allowlist.txt`, `test-report.txt`, `test-readonly.txt`, `test-cli-registration.txt` against `pytest --collect-only` | identical sets: 161, 94, 243, 48, 24, 3 (none only in one side); every `test_*` name in the case-to-test text of the six maps exists in `tests/sweep/*.py` |
| Test note constants (25 `N_*` in `test_classify.py`) against `classify.py` string constants; `NO_RECORDS`, `BOUND_LINE`, `PAGE_LINE`, `WORKTREES_BANNER`, `SP24`, `SP16`, `WC13`, `ORIGIN_NOT_PROVED` in `test_report.py` against `report.py`/`classify.py` | all equal (`SCOPE_LOWER_BOUND` is built inside an f-string in `report.py`; the rendered line is pinned by passing tests) |
| Grep of `tests/sweep/*.py` for sleep, wall clock, thread, random, uuid, tempfile; for `posix_spawn`, `os.spawn`, `os.exec`, `os.fork`, `ctypes`, `pty`, `socket`, `os.putenv`, `os.chdir`; for markers | no hit; the only `pytest.mark.integration` is `test_readonly.py:471`; the new tests add no listing call |
| Fixtures: 19 `captured-*.json` each have a row in `SOURCES.md` and no row lacks a file; the folder holds nothing else; 54 distinct UUIDs, all `00000000-0000-4000-8000-<12 digits>`, 1 to 54; grep for `coder` (lower case), `/home/coder`, e-mail, IPv4 and key-like words | no difference; 0 hits |

## Checks

Result cell rule: PASS or FAIL is the first word. "Drift" means a count or a line pointer the fix moved (559 to 573 tests, 159 to 161, 242 to 243, 41 to 48, 90 to 94; line numbers after the inserted tests) while the claim still holds. Check text is the text of the cycle-0 report; the "saved scratch" checks describe cycle-0 scratch runs that cannot be re-run, and the table says what on disk shows the fix changed nothing they relied on.

| Check | Result |
|---|---|
| qa-classify-coverage-report:C1 | PASS. Suite green now: 573 passed, `test_classify.py` 161 passed, ruff check and format clean (drift only: 559 and 159 became 573 and 161 by the 14 added tests). |
| qa-classify-coverage-report:C2 | PASS. `test_rule_case_per_rule_1_to_9`, `test_every_class_name_is_reached`, `test_rules_order_pin` exist and pass; `test_classify.py` gained only the two rule-2 tests and the exemption parametrization (+40 lines). |
| qa-classify-coverage-report:C3 | PASS. The window tests are unchanged; mutation `>=` to `>` at `classify.py:314` is killed by `test_5h_old_row_is_idle_only_when_window_is_under_5h[5-person_active]`. |
| qa-classify-coverage-report:C4 | PASS. `test_fr008_four_inputs_are_could_not_determine_never_stalled` at `test_classify.py:536` still has its 4 params. |
| qa-classify-coverage-report:C5 | PASS. `test_fr009_case_1_...` (`:582`) and `test_fr009_case_2_...` (`:593`) still assert `notes == (N_EXITED,)`; mutation MU7 killed by both. |
| qa-classify-coverage-report:C6 | PASS. Rule 1 decline tests and `test_rule_5_needs_all_four_conditions` exist and pass (names found in `test_classify.py`). |
| qa-classify-coverage-report:C7 | PASS. `test_fr010_control_complete_list_older_transcript_is_true_and_historical` exists and passes. |
| qa-classify-coverage-report:C8 | PASS. The three SPEC incomplete-list tests exist and assert exact notes; MU9 (outage also counted as `call_failed`) killed by 4 tests. |
| qa-classify-coverage-report:C9 | PASS. The three non-SPEC fixtures and `test_fr010_incomplete_notes_order` exist; MU12 and MU13 (tab-map and truncated notes dropped) killed. |
| qa-classify-coverage-report:C10 | PASS. The exemption test is now exact (`test_classify.py:999-1048`); `test_fr010_exemption_orca_rows_never_go_to_historical` (`:1051`) and `test_sp29_other_run_transcripts_...` (`:1063`) are unchanged. |
| qa-classify-coverage-report:C11 | PASS. The D9 join tests, the guard-case test and the SPEC line 236 test exist and pass (names found by grep). |
| qa-classify-coverage-report:C12 | PASS. `test_r2_b1_pane_reuse_outside_window_does_not_join[...]` and the two sibling tests exist and pass. |
| qa-classify-coverage-report:C13 | PASS. The five `test_path_b_window_*`/`..._terminal_row_...`/`..._incomplete_tail_...` tests exist and pass. |
| qa-classify-coverage-report:C14 | PASS. The six R3-B1 reader and parser tests exist in `test_probes_allowlist.py` (they sit before line 1362, which is where the file changed) and pass. |
| qa-classify-coverage-report:C15 | PASS. The ten R3-B2 `test_path_b_*` tests exist and pass. |
| qa-classify-coverage-report:C16 | PASS. `test_sp07_...` (MU6 killed), `test_truncated_jsonl_...`, the unreadable-input tests and `test_wc13_...` exist and pass. |
| qa-classify-coverage-report:C17 | PASS. The FR-012 to FR-015 and FR-005 tests exist (map text of `test-classify.txt` names all of them and each name exists). |
| qa-classify-coverage-report:C18 | PASS. `test_nfr004_module_imports_nothing_it_must_not`, `test_import_scanner_catches_every_import_form` and `test_b5_...` exist and pass; the "16 forms" wording (TST-F10) is MINOR and unchanged. |
| qa-classify-coverage-report:C19 | PASS. The `collect` source-row and `truncated` tests of DESIGN 12 sit before `test_probes_allowlist.py:1362`, so their line numbers did not move; they pass. |
| qa-classify-coverage-report:C20 | PASS. 25 `N_*` constants of `test_classify.py` all equal a string constant of `classify.py`; `src/` hashes equal the pre-fix record. |
| qa-classify-coverage-report:C21 | PASS. Exact-note assertions unchanged; MU6, MU7, MU9, MU12 and MU13 re-run and killed; the fix only made the exemption assertions exact. |
| qa-classify-coverage-report:C22 | PASS. No DESIGN 11 case lost its test: per-file test counts only went up, and the names of the map exist. |
| qa-classify-coverage-report:C23 | PASS. `test-classify.txt` was regenerated: its 161 `-v` lines equal `pytest --collect-only` for `test_classify.py`; the new tests 18a are in its case map; only TST-F10's "16 forms" wording remains (MINOR). |
| qa-classify-coverage-report:C24 | PASS. Saved scratch run: a `/tmp` listing shows no `qa-t224` directory and no tracked file of the gate changed by that review; nothing the check relied on was changed by the fix (hash and file-time evidence above). |
| qa-probes-readonly-coverage-report:C1 | PASS. `test_allowlist_is_exactly_the_ten_templates`-family tests (names in the case map) exist and pass; probes tests before `:1362` are unmoved. |
| qa-probes-readonly-coverage-report:C2 | PASS. `NEGATIVE_ARGV` and `test_negative_argv_raises_value_error_before_a_subprocess` exist; mutation "`_orca` stops calling `check_orca_argv`" family not re-run, but `default binary orca` and the `git` argv mutations are killed. |
| qa-probes-readonly-coverage-report:C3 | PASS. `test_worktree_ps_agent_wait_templates_are_accepted[no-json\|json]` pass and are among the tests that kill the `orca` binary mutation. |
| qa-probes-readonly-coverage-report:C4 | PASS. FR-021 forbidden-verb tests exist and pass (the TST-F16 note is MINOR and unchanged). |
| qa-probes-readonly-coverage-report:C5 | PASS. `GIT_NEGATIVE` tests and `test_the_one_git_call_is_accepted` exist; the `git` argv mutation is killed by the latter. |
| qa-probes-readonly-coverage-report:C6 | PASS. Full-sweep recording tests exist and kill the default-binary and `git` argv mutations. |
| qa-probes-readonly-coverage-report:C7 | PASS. The unavailable-cause, quoted-marker, middle `worker-show`, malformed body, empty `run-current` and captured no-binding tests exist and pass. |
| qa-probes-readonly-coverage-report:C8 | PASS. `test_collect_worker_list_source_rows_and_truncated` and its siblings exist and pass. |
| qa-probes-readonly-coverage-report:C9 | PASS. The budget tests exist; show cap 51 killed by 6 tests; the `call_timeout` `<=` survivor is the MINOR TST-F18, unchanged. |
| qa-probes-readonly-coverage-report:C10 | PASS. The boundary fixtures kill the orca, git, ledger and contract limit mutations (`[at-the-limit]` cases). |
| qa-probes-readonly-coverage-report:C11 | PASS. The six failure-mode tests exist; `_stable` single read killed by the two changed-contract tests. |
| qa-probes-readonly-coverage-report:C12 | PASS. `STATUS_HEADERS`, the `-z` rename test and the untracked `.dev/tasks/` tests exist and pass. |
| qa-probes-readonly-coverage-report:C13 | PASS. The six R3-B1 time-field tests exist and pass. |
| qa-probes-readonly-coverage-report:C14 | PASS. `test_readonly.py` is older than the cycle-0 reports; its lock-free argv tests kill the `git` argv and env mutations. |
| qa-probes-readonly-coverage-report:C15 | PASS. The snapshot-diff tests are unchanged and pass in file order, reversed and rotated order and alone. |
| qa-probes-readonly-coverage-report:C16 | PASS. The real-git test passes under `-m integration` (1 passed, 572 deselected); unchanged file. |
| qa-probes-readonly-coverage-report:C17 | PASS. The guard-liveness test and the one-integration test pass; grep finds the one `@pytest.mark.integration` at `test_readonly.py:471`. |
| qa-probes-readonly-coverage-report:C18 | PASS. Saved scratch: nothing it relied on changed in `src/` (hashes) or `test_readonly.py`; 10 of its mutations were re-run now and all were killed, and the two cycle-0 survivors (TST-F18 and the equivalent `FORBIDDEN_TOKENS` mutant) are the same. |
| qa-probes-readonly-coverage-report:C19 | PASS. Drift only: the two files now give 267 passed (243 and 24) in file, reversed and per-file order; ruff check and format clean. |
| qa-probes-readonly-coverage-report:C20 | PASS. `test-probes-allowlist.txt` (243 lines) and `test-readonly.txt` (24) equal the collected sets and every test name they cite exists; the F1 and F2 notes (MINOR) are unchanged. |
| qa-report-cli-coverage-report:C1 | PASS. The `test_report.py` row still maps to tests with real assertions; 7 tests were added (header lines, banner, two classifier-cell tests) and none removed (41 to 48). |
| qa-report-cli-coverage-report:C2 | PASS. `test_cli_registration.py` unchanged (3 tests, file time 04:59). |
| qa-report-cli-coverage-report:C3 | PASS. The `test_cli_contract.py` row still maps to tests; 4 tests were added (window x3, JSON worktree values), none removed (90 to 94). |
| qa-report-cli-coverage-report:C4 | PASS. The `_publish` publication tests are untouched (the file changed only at `:508-531` and `:1018-1038`); they pass. |
| qa-report-cli-coverage-report:C5 | PASS. Run id, binding, window parser, exit-code and naming tests unchanged and green; the new window test uses `_payload`, which asserts exit 0 and empty stderr. |
| qa-report-cli-coverage-report:C6 | PASS. `test_golden_v1_keys_and_types_at_every_level` and `GOLDEN_V1` are unchanged (`test_cli_contract.py` around `:971-1015`, drift only) and pass; the added value test sits after it. |
| qa-report-cli-coverage-report:C13 | PASS. Saved scratch (11 mutants, 1 killed, 10 survived, survivors mapped to F-2 to F-5): the record is of the cycle-0 run; the fix improved the tests, so M3, M19, M20, M23, M24 and M25 now die (re-run: killed); no survivor is unaccounted for, M1 and the `_publish` mutants remain MINOR findings. |
| qa-report-cli-coverage-report:C14 | PASS. `test-report.txt` (48), `test-cli-contract.txt` (94) and `test-cli-registration.txt` (3) equal the collected sets; `phase10-validation.md` is unchanged and still records the Phase 10 run at 559 passed (note N-1 below); its claims about ruff hold now. |
| qa-report-cli-coverage-report:C15 | PASS. Gates reproduced now: 573 passed (drift from 559), ruff check clean, ruff format clean. |
| qa-report-cli-coverage-report:C16 | PASS. Saved conduct claim (only the report written, mutation copy deleted, no live Orca command): `ls -d /tmp/t226*` now finds nothing and no gate file other than the changes listed above is newer than the cycle-0 reports; nothing the claim relied on was changed by the fix. |
| qa-isolation-report:C1 | PASS. Baseline now 573 passed, ruff clean (drift from 559). |
| qa-isolation-report:C2 | PASS. `conftest.py` (334 lines, file time 04:04) is unchanged; I read `:22-42` now: line 30 `marks = getattr(request.function, "pytestmark", [])`, line 31 the `integration` test, lines 40-42 the three patches. |
| qa-isolation-report:C3 | PASS. Grep finds the only decorator at `test_readonly.py:471`; `-m integration` selects 1 of 573 (drift from 559). |
| qa-isolation-report:C4 | PASS. Audit hook, full run in three orders: 9 `Popen` events, all git and all owned by the integration test; none at collection; a reversed run with `-m "not integration"` logged 0. |
| qa-isolation-report:C5 | PASS. Grep of `src/superclaude/cli/sweep/` finds subprocess starts only at `probes.py:248` and `:299` (both `subprocess.run`); `src/` hashes equal the pre-fix record; none of the 9 events names `orca`, `claude` or `ccsession`. |
| qa-isolation-report:C6 | PASS. The guard still patches only `run`, `Popen` and `os.system` (gap F1 stays MINOR); the new tests use none of `posix_spawn`, `os.spawn*`, `os.exec*`, `os.fork`, `pty`, `ctypes` (grep) and the audit saw none. |
| qa-isolation-report:C7 | PASS. 166 `Path.home()` calls in the audit run, 0 outside the test temp folder (the new tests build on `sweep_root` and `env`, which set `HOME` and `XDG_STATE_HOME` inside `tmp_path`). |
| qa-isolation-report:C8 | PASS. 0 writes or mutations outside the test's own temp folder; the one relative `os.remove(".git")` is the one the cycle-0 report explains; the new `os.utime` call is on a file under `tmp_path`. |
| qa-isolation-report:C9 | PASS. 0 `READ_HOST` events; `read_orca_version` is still patched in the three modules that collect (the new probes test uses the autouse stub at `test_probes_allowlist.py:208-211`). |
| qa-isolation-report:C10 | PASS. The new patches use `monkeypatch` (`probes._utcnow` at `test_probes_allowlist.py:1371`); reversed, rotated, per-file and one-test-per-process runs all pass. |
| qa-isolation-report:C11 | PASS. `test_readonly.py` unchanged (file time 04:44) and passes under `-m integration` and in the full run. |
| qa-isolation-report:C12 | PASS. `_payload` still asserts exit 0 and empty stderr and the new CLI tests use it; the new tests that read the result fail on any guard trip. |
| qa-isolation-report:C13 | PASS. Producer evidence reproduced: one integration test selected, `test-readonly.txt:66` text holds; `phase10-validation.md:62` records 559 and the suite now has 573 (drift, note N-1); `test-cli-registration.txt:26-27` "469" is the existing MINOR F3. |
| qa-assertion-strength-report:C1 | PASS. Baseline `uv run pytest tests/sweep -q` passes (573 now against 559 in `phase10-validation.md:62`, drift only). |
| qa-assertion-strength-report:C2 | PASS. `ruff check` and `ruff format --check` both clean on `src/superclaude/cli/sweep` and `tests/sweep` (15 files). |
| qa-assertion-strength-report:C3 | PASS. Saved scratch (harness proved by a sanity mutation); nothing it relied on changed in `src/`; my own harness proved the same way (every mutation changed the result). |
| qa-assertion-strength-report:C4 | PASS. `conftest.py` unchanged; `GitFake` calls `check_git_args` unconditionally (`conftest.py:62-78` region) and the guard is live (`test_the_subprocess_guard_is_live_in_this_module`). |
| qa-assertion-strength-report:C7 | PASS. `test_readonly.py` unchanged; MINOR only. |
| qa-assertion-strength-report:C10 | PASS. `test_cli_registration.py` unchanged; MINOR only. |
| qa-assertion-strength-report:C11 | PASS. The maps agree with the disk: 573 passed, 24 in `test-readonly.txt`, 3 in `test-cli-registration.txt`; `test-classify.txt` now 161 (was 159) and equals the collected set (drift, same claim). |
| qa-assertion-strength-report:C12 | PASS. The DESIGN 12 rows spot-checked (FR-005, FR-012, FR-013, FR-017, FR-025, NFR-002, NFR-003, NFR-010) still name files that exist and hold the tests (`test_cli_contract.py`, `test_classify.py`, `test_probes_allowlist.py`, `test_readonly.py`). |
| qa-fixture-provenance-report:C1 | PASS. 19 `captured-*.json`, each with a `SOURCES.md` row, no row without a file. |
| qa-fixture-provenance-report:C2 | PASS. The folder holds only `captured-*.json` and `SOURCES.md`; no hand-made file exists, so none lacks `synthetic`. |
| qa-fixture-provenance-report:C3 | PASS. `captured-worker-list.json` hash equals the pre-fix record (nothing changed since cycle 0). |
| qa-fixture-provenance-report:C4 | PASS. `captured-worker-show-1..5.json` hashes equal the pre-fix record. |
| qa-fixture-provenance-report:C5 | PASS. `captured-task-list.json` and `captured-task-list-ready.json` hashes equal the pre-fix record. |
| qa-fixture-provenance-report:C6 | PASS. `captured-run-current.json` and the two unknown-Run fixtures hashes equal the pre-fix record. |
| qa-fixture-provenance-report:C7 | PASS. `captured-worktree-current.json` hash equals the pre-fix record. |
| qa-fixture-provenance-report:C8 | PASS. `captured-worktree-ps.json` and `captured-worktree-list.json` hashes equal the pre-fix record (the UNVERIFIABLE part, F6, is unchanged). |
| qa-fixture-provenance-report:C9 | PASS. `captured-tab-map-1..5.json` hashes equal the pre-fix record. |
| qa-fixture-provenance-report:C10 | PASS. 54 distinct UUIDs, all `00000000-0000-4000-8000-<12 digits>`, first 1, last 54, none non-fake. |
| qa-fixture-provenance-report:C11 | PASS. Zero hits for lower-case `coder`, `/home/coder`, e-mail, IPv4 and key-like words in the fixture folder. |
| qa-fixture-provenance-report:C14 | PASS. `SOURCES.md` hash equals the pre-fix record and all fixtures are unchanged, so its per-file facts hold as before. |
| qa-fixture-provenance-report:C15 | PASS. No test file contains `synthetic`; the folder holds no hand-made file; the new tests build their data inline from existing builders. |
| qa-determinism-report:C1 | PASS. The new tests use a fixed `now` (`env.now`, `ctx.now`, the `NOW` constant); runs with `_utcnow` and `commands.datetime` shifted to 1970, 2036 and 2026-11-08 all pass. |
| qa-determinism-report:C2 | PASS. Grep of `tests/sweep/*.py` for sleep, wall clock, thread, random, uuid and tempfile finds nothing. |
| qa-determinism-report:C5 | PASS. Reversed, rotated, per-file, reversed file order, and each of the 573 tests alone: all pass. |
| qa-determinism-report:C6 | PASS. Two full runs plus 1146 passed with the suite listed twice in one process; no file under `tests/sweep` or `src/superclaude/cli/sweep` is newer than the report stub. |
| qa-determinism-report:C7 | PASS. `test_import_is_lazy_and_runs_no_seam` passes in reversed, rotated and alone runs. |
| qa-determinism-report:C8 | PASS. `TZ` = Pacific/Kiritimati, America/Adak, Asia/Kolkata, UTC: 573 passed each; the new tests use aware datetimes. |
| qa-determinism-report:C9 | PASS. `LC_ALL`/`LANG` = C and C.utf8: 573 passed each. |
| qa-determinism-report:C10 | PASS. `PYTHONHASHSEED` = 0, 1, 2, 99: 573 passed each. |
| qa-determinism-report:C11 | PASS. The new tests add no directory listing; the existing listings are sorted or have one entry (grep of `iterdir`, `listdir`, `rglob`, `os.walk`). |
| qa-determinism-report:C12 | PASS. Scrubbed environment (`env -i`, `ORCA_CLI_COMMAND=/bin/false`) gives 573 passed. |
| qa-determinism-report:C14 | PASS. Run from cwd `/` gives 573 passed; the new tests do not call `chdir`. |
| qa-determinism-report:C15 | PASS. The new mtime test sets whole-second times with `os.utime` and passes under shifted clocks; no new test depends on mtime granularity or ordering. |
| qa-determinism-report:C19 | PASS. `ruff check` and `ruff format --check` exit 0 now. |
| qa-determinism-report:C20 | PASS. Audit run: only the integration test starts a process and only `git`; no `orca`, `claude` or `ccsession` argv; the guard test passes. |

## New findings

None at BLOCKING or MAJOR level. I looked for defects the fix could have introduced: a test that passes on wrong code (every added test was mutation-checked above), a weakened existing test (per-file test counts only rose, the exemption test changed from `!=` to equality), a changed source file (hashes equal), a result map that disagrees with the disk (sets equal), and a new dependence on the clock, the order, the temp folder or the host (all perturbations pass).

Notes, MINOR, not graded:

- N-1: `phase10-validation.md:62` still records 559 passed, and `test-cli-registration.txt:26-27` still says 469 (the latter is the cycle-0 MINOR TST-F45). The first is a record of the Phase 10 run and was protected from the fix; refresh it when Phase 10 validation is next run.
- N-2: the MINOR findings TST-F7 to TST-F45 were left alone by the fix, as ordered; I did not recheck them. The two survivors I re-ran (TST-F18, TST-F24) are unchanged.

## Self-audit

- Verified by tool evidence: 102 of 102 check ids and 6 of 6 findings. Unverifiable: 0. Unchecked: 0. Checks that describe cycle-0 scratch runs (qa-classify-coverage-report:C24, qa-probes-readonly-coverage-report:C18, qa-report-cli-coverage-report:C13, qa-report-cli-coverage-report:C16, qa-assertion-strength-report:C3) are graded from what on disk shows was unchanged plus my own re-runs, as the prompt allows.
- Evidence I can point to: the `573 passed` run, the 1-test integration run, ruff output, `sha256sum -c` on both pre-fix records, about 45 mutation runs (all `F_0` mutations killed, 11 cycle-0 probes mutations and 5 classify note mutations re-killed), the audit-hook runs in three orders, 573 one-test processes, the TZ, locale, hash-seed, clock-shift and scrubbed-environment runs, and the result-map set comparisons.
- Tool engagement: Read 22 | Grep 2 | Glob 0 | Bash 27 (the Bash calls are the runs, listings, batch scripts and greps named above). No web research; no Tavily or fallback call.
- Cleanup: the private `/tmp/ironclaude-batch.*` directory and `/tmp/v1-workdir.txt` are removed after this report; this report is the only file written. No live Orca command was run and no background loop was started.

Verdict: PASS
Blocking count: 0
