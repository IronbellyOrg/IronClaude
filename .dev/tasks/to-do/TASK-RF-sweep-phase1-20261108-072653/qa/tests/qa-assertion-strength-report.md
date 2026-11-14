# QA Report - Assertion-Strength Lens (T228)

**Phase:** task-qualitative (assertion-strength lens)
**Date:** 2026-11-12
**fix_authorization:** false (report is the only file written)

Sections are appended below as each test file is reviewed.

## Method and evidence base

- Read from disk in chunks of at most 150 lines: `tests/sweep/conftest.py` (334 lines), `test_classify.py` (1851), `test_probes_allowlist.py` (1934), `test_readonly.py` (528), `test_report.py` (1175), `test_cli_contract.py` (1409), `test_cli_registration.py` (69); `src/superclaude/cli/sweep/models.py` (all), `classify.py` lines 155-504 and 774-996, `commands.py` lines 150-288, `report.py` lines 36-70, 160-210 and 575-673, `probes.py` selected ranges; the six result maps (`test-classify.txt`, `test-readonly.txt`, `test-cli-registration.txt` in full; the other three by their case maps only), `phase10-validation.md`, and DESIGN section 7.4/7.5 and sections 11 and 12 in `docs/designs/orchestrator-mode.md` (lines 596-626 and 745-814).
- Baseline run on the repository: `uv run pytest tests/sweep -q` gives 559 passed (matches `phase10-validation.md` line 62); `ruff check` clean; `ruff format --check` 15 files already formatted.
- Mutation experiments: every code change was made in a private copy under `/tmp/t228-mut/` (copy of `src/superclaude`, `tests/sweep`, `pyproject.toml`, `.gitignore`, imported through `PYTHONPATH`), one change at a time, restored from a pristine copy after each run. A sanity mutation (`C_IDLE` rule name changed) failed 4 tests, which proves the copy is the code that runs. No repository file was changed; the copies were deleted at the end. No live Orca, ccsession or Claude command was run.
- Labels: **[mutated, survived]** = I ran the change and all selected tests still passed; **[by inspection]** = I did not run it; the assertion is weak on its face but I have no run to show.
- Severity scale for this lens: BLOCKING or MAJOR = a one-line change to production code that breaks a DESIGN-specified output, a safety/honesty claim or a correctness path while the whole suite stays green. MINOR = the assertion is loose but a neighbouring test pins the behaviour, or the changed behaviour is not DESIGN-specified.

## Weak tests per file (the five most likely to pass on wrong code)

### tests/sweep/test_classify.py

| # | Test (file:line) | One-line change that still passes | Stronger assertion |
|---|---|---|---|
| W-CL1 | `test_rule6_partial_carries_its_note` (`test_classify.py:694-697`) uses `orca(outcome="partial")` and `contract("partial")` together | `classify.py:283` `partial = "partial" in (orca.outcome, contract.worker_status)` becomes `partial = orca.outcome == "partial"`; and, separately, becomes `partial = contract.worker_status == "partial"` **[mutated, survived, both; 559 passed]** | Parametrize the two asymmetric inputs (Orca `partial` with contract `succeeded`; Orca `succeeded` with contract `partial`); both give `(FINISHED, (N_PARTIAL,))` with the current code (probed), so assert `cls.notes == (N_PARTIAL,)` for each |
| W-CL2 | `test_fr010_exemptions_never_become_idle` (`test_classify.py:967-1008`, one assertion at 1008: `class_name != IDLE`) over five rows | `classify.py:314` `and last >= ctx.window_start` becomes `and True`: stale rows that rule 8 must refuse become `person session (active)` instead of `could not determine` **[mutated, survived; 559 passed]** | Assert the exact `(rule, class_name)` per case. Current code (probed): `unreadable-transcript`, `unknown-timestamp`, `open-task`, `unread-report-candidate` give `("fallback", UNKNOWN)`; `explicit-wait` gives `("waiting_signal", WAITING)` |
| W-CL3 | `test_fr012_terminal_values_and_worktree_is_never_yes` (`test_classify.py:1508-1516`; the worktree assertion at 1515 is `safe.worktree in ("no", "could not determine")`) | `classify.py:489` unobserved worktree gives `"no"` instead of `"could not determine"` **[mutated, survived]**; and `classify.py:495` `reason=...` becomes `reason=None` **[mutated, survived]**. `SafeToClose.reason` is asserted in no test (the reason mutation left the whole suite green) | Table of expected worktree value per variant: `None`, `wtree()`, `wtree(status_read=False)` all `"could not determine"`; `wtree(uncommitted=True)` is `"no"`; plus `safe.reason == "terminal: terminal retained (terminal_state=retained, next_action=release); worktree: worktree not observed"` for the `None` case (probed string) |
| W-CL4 | `test_future_timestamp_is_unknown_age_and_never_idle` (`test_classify.py:487-493`) and `test_future_transcript_gets_no_age` (`496-502`): both end in `class_name != IDLE` | `classify.py:373` `row.last_activity > ctx.now` becomes `>= ctx.now`: a row stamped exactly `now` would be called future; no fixture has `last_activity == now` **[mutated, survived]**. The same tests also hide that the current class for a future-dated session is `person session (active)` (probed: rule `person_active`, notes `("timestamp in the future",)`), which no test states | Add the equal-to-`now` boundary (no `N_FUTURE`) and assert `(cls.rule, cls.class_name) == ("person_active", PERSON_ACTIVE)` with `cls.notes == (N_FUTURE,)`, or whatever class the owner decides it should be |
| W-CL5 | Every rule-2 fixture uses `transcript_readable=True`: `_rule_cases` `test_classify.py:292-303`, `test_fr009_exited_row_without_proof_is_not_stalled` (`542-547`) | `classify.py:196` `row.transcript_readable is not False` becomes `row.transcript_readable is True`. An Orca row with no joined transcript has `transcript_readable=None` (`classify.py:887`), so under the mutation `stalled (proved)` can never be produced for it **[mutated, survived]**. Current code gives STALLED for `None` (probed) | Add `transcript_readable=None` with exit proof, asserting `(rule, class_name) == ("orca_exit_proof", STALLED)` |

Also weak in this file, not in the five: `test_rule_5_needs_all_four_conditions` (`431-447`), `test_rule1_ask_the_coordinator_declines_with_the_note` (`578-602`) and `test_sp07_guard_refused_on_a_later_line_is_not_finished` (`676-679`) assert only `!= WORKING`, `!= WAITING`, `!= FINISHED`; `test_rule6_finished_never_says_admitted_or_accepted` (`682-691`) guards its text check with `if cls.class_name == FINISHED:` at line 686, so it checks nothing when the class is wrong (the `guard` case at 689-691 is unconditional); `removable` `classify.py:464` `sorted(...)[0]` becomes `[-1]` **[mutated, survived]** because every fixture has one shared id.

### tests/sweep/test_probes_allowlist.py

| # | Test (file:line) | One-line change that still passes | Stronger assertion |
|---|---|---|---|
| W-PR1 | The contract-source tests (`test_probes_allowlist.py:1349-1360`, `1558-1574`, `1666-1687`) and the golden type check (`test_cli_contract.py:903`, `age_seconds` is `(int, NoneType)`). No test asserts a contract's source `age_seconds` or `ContractRecord.mtime` read from disk | `probes.py:999` `_age` returns `0`; or `probes.py:1346` passes `None` instead of `_age(now, record.mtime)`; or `probes.py:757-758` reads `mtime` as `datetime.fromtimestamp(0, ...)` **[mutated, survived, all three; 559 passed]** | Write a contract, `os.utime` it to `NOW - 1 h`, then assert `read_contract(path, root).mtime == NOW - 1h` and the `contract <dispatch>` source row has `age_seconds == 3600`. The Waiting (a) Age column (SP-15) is computed from this mtime |
| W-PR2 | `test_a_process_that_cannot_start_is_unavailable_with_the_binary_named` (`test_probes_allowlist.py:737-744`) ends in `reason.startswith("could not start orca-ide: ")` | `probes.py:260` `f"could not start {binary}: {exc}"` becomes `f"could not start {binary}: "` (the cause is dropped) **[mutated, survived]** | `assert result.reason == "could not start orca-ide: [Errno 13] Permission denied"` |
| W-PR3 | `test_every_call_timing_out_still_collects_and_publishes` (`test_probes_allowlist.py:1150-1169`); the last line, 1169, is `assert report.render(classify_all(inp, ctx), ctx)` (any non-empty string) | `report.render` returns `"x\n"`: this test still passes **[mutated, survived with `-k "every_call_timing_out"`; the sibling `test_full_timeout_fakes_finish_under_120_s_and_still_publish` fails because it checks a substring]** | `text = report.render(...)`; `assert text.endswith("Report complete\n")` and `assert "orca unavailable" in text` |
| W-PR4 | `test_a_show_of_the_wrong_shape_raises_nothing` (`test_probes_allowlist.py:1548-1555`) checks only `obs.dispatch` and `obs.status` out of about twenty `OrcaObservation` fields | **[by inspection]** a parser that keeps stray values (for example `outcome` or `terminal_state` from a malformed `show`) for the six wrong shapes | `assert obs == probes.parse_worker_show(RUN, {"dispatchId": DISPATCH}, None)` so every field equals the no-show baseline |
| W-PR5 | `test_probes_source_holds_no_write_verb_even_as_a_string` (`test_probes_allowlist.py:454-463`) collects only whole `ast.Constant` strings | Add `_X = "worker-" + "start"` to `probes.py` **[mutated, survived; 559 passed]** (the allowlist pins do not see it because it is not in `ALLOWED_ORCA`) | Scan the compiled module's `co_consts` recursively (CPython folds constant concatenation), or scan the source text for the verbs split across quotes |

Also loose: `test_full_timeout_fakes_finish_under_120_s_and_still_publish` ends in `"time budget reached" in text` (`1147`); `test_the_one_git_call_is_accepted` and the budget tests are strong (exact argv and exact timeouts).

### tests/sweep/test_readonly.py

| # | Test (file:line) | One-line change that still passes | Stronger assertion |
|---|---|---|---|
| W-RO1 | `test_real_git_lock_free_status_and_gitignore` (`test_readonly.py:471-528`). The lock-free call at 513-517 is built in the test (`[GIT, "--no-optional-locks", "-C", ...]`); `probes._git` is never called. When the control is inconclusive it only warns (523-528) | `probes.py` `"--no-optional-locks"` becomes `"--no-pager"` **[mutated: the real-git test still passed with `-k real_git`; only the two recorded-argv tests at `test_readonly.py:73-91` and `144-158` failed]** | Call `probes._git(repo, *STATUS_ARGS)` inside this integration-marked test and assert the index bytes are unchanged; turn the inconclusive-control `warnings.warn` into `pytest.skip` or a failure so a pass always means the control held (it is conclusive on this host: git 2.47.3, no warning under `-rw`) |
| W-RO2 | `test_sweep_run_adds_exactly_one_report_and_changes_nothing_else` (`test_readonly.py:367-389`); report content is checked only as `size > 0` (388-389) | `commands.py:165` `data = text.encode(...)` becomes `data = b"x\n"` **[mutated, survived with `tests/sweep/test_readonly.py`; 24 passed]** | Read the report and assert `text.endswith("Report complete\n")` and that `json.loads(result.stdout)["report_path"]` is the file read |
| W-RO3 | The snapshot scope `sweep_env.paths` (`test_readonly.py:340-346`) is root, `HOME`, state, three XDG dirs and the worktrees folder. The working folder is not in it | Add `open("stray.log", "w").close()` at the start of `commands.run` (writes into the current folder) **[mutated, survived; 24 passed; the file was created in the private copy]** | Add `Path.cwd()` (after `monkeypatch.chdir(tmp_path / "cwd")`) and the system temp folder to `paths` |
| W-RO4 | `test_a_sweep_starts_no_process_and_records_only_allowlisted_argv` (`test_readonly.py:440-458`) uses `set(orca_calls) == {...}` (line 446) | **[by inspection]** a second `worktree ps` or repeated `worker-list` call per Run would leave the set unchanged | Compare the recorded list in order: `orca_calls == [WORKER_LIST, TASKS_READY, TASKS_ALL, WORKTREE_PS]` |
| W-RO5 | The report file mode is never read (snapshot records kind, size, mtime, SHA-256 only, `test_readonly.py:164-184`) | `commands.py:170` mode `0o666` becomes `0o777`: the report is created executable **[mutated, survived the whole suite]** | `assert stat.S_IMODE(os.stat(report).st_mode) & 0o111 == 0` |

### tests/sweep/test_report.py

| # | Test (file:line) | One-line change that still passes | Stronger assertion |
|---|---|---|---|
| W-RE1 | `test_header_first_line_and_scope_line_are_exact` (`test_report.py:556-565`) pins `lines[0]` and `lines[1]` only. No test mentions `Orca binary:`, `Sources:`, `Messages coverage:` or `Untracked paths:` (grep of `tests/sweep` finds none); DESIGN 7.5 lines 608-613 lay all four out | `report.py:181` `"Messages coverage: partial"` becomes `"Messages coverage: complete"` **[mutated, survived]**; `report.py:179` `Orca binary: {...}` becomes the literal `Orca binary: orca` (NFR-003 says never bare `orca`) **[mutated, survived]** | Assert the full seven header lines for a fixed result, including `Orca binary: orca-ide` and `Messages coverage: partial`, and a `Sources:` line with an `(age Ns)` suffix |
| W-RE2 | `test_next_inspection_map_has_an_entry_per_rule_and_only_names_a_read` (`test_report.py:962-968`) and `test_every_sessions_row_has_a_next_inspection_cell_from_the_map` (`971-984`): the second compares each cell with the production dict itself, the first checks only non-empty text and `BANNED_WORD` (`959`: stop, retry, release, merge, remov*) | `report.py:49` `"working"` text replaced with another rule's text **[mutated, survived]**; `report.py:53` `"fallback"` text gets `", then delete the stale worktree"` appended **[mutated, survived]** (`delete` is a removal word the regex lacks) | Pin the nine map values as literals, and widen `BANNED_WORD` to `delete|prune|clean|rm|remov\w*` |
| W-RE3 | `test_ten_dimensions_are_sessions_columns_and_not_json_keys` (`test_report.py:1091-1111`) and `dimension_result` (`1066-1088`) feed hand-built `lifecycle`, `health`, `result`, `freshness` strings to the printer | `classify.py:785` `return "settled" if _settled(orca) else "running"` becomes `return "running"`; `classify.py:792` `"failed result"` becomes `"unknown"`; `classify.py:800` blocked `"null"` becomes `"blocked"`; `classify.py:921` fresh and stale swapped; `classify.py:922` `freshness_age_s` set to `0` **[mutated, survived, all five; 559 passed]** | One `classify_all` fixture that goes through to `report.render` and asserts the Lifecycle, Health, Result and Freshness cells for a settled row, a failed-contract row, a blocked row, and a fresh and a stale transcript |
| W-RE4 | `test_report_gives_no_advice_to_delete_anything_under_dev_tasks` (`test_report.py:1169-1175`) scans only lines that contain `.dev/tasks/` | **[by inspection]** advice text placed on a line without that path. W-RE2's `delete` mutation is the same hole, reached through the Next-inspection cell | Scan every line of the rendered report for the widened banned words, not only the `.dev/tasks/` lines |
| W-RE5 | `test_report_holds_no_command_to_paste` (`test_report.py:1161-1166`) checks for fences and a leading `$ ` only | **[by inspection]** a bare command line such as `git worktree remove /wt/one` has neither | Also reject lines that start with `git `, `orca` or `rm ` |

Strong in this file (no weak pick): the sort, injection, cell cut, version-line, empty-section, SP-16, WC-13 and set-union tests all assert exact values.

### tests/sweep/test_cli_contract.py

| # | Test (file:line) | One-line change that still passes | Stronger assertion |
|---|---|---|---|
| W-CC1 | `test_golden_v1_keys_and_types_at_every_level` (`test_cli_contract.py:971-990`) with `GOLDEN_V1` (`880-891`): worktree values are checked by type only; the FR-012 line at 988-990 reads `rows[].safe_to_close.worktree`, not `worktrees[].removable` | `report.py:653` `"removable": w.removable` becomes `"removable": "yes"` **[mutated, survived; 559 passed]**. `removable` is the source of `safe_to_close.worktree` (`classify.py:491`) and `run()` in `test_classify.py:246-247` asserts `w.removable != "yes"`, but the JSON copy is not checked | Assert `all(w["removable"] in ("no", "could not determine") for w in payload["worktrees"])` and exact `status_read`, `uncommitted`, `unpushed` values for the two worktrees of `_captured_world` |
| W-CC2 | `test_valid_windows_parse_and_reach_the_json` (`test_cli_contract.py:480-499`) and `test_default_window_is_6h` (`502-505`) check `commands._parse_window` and the printed `window` text only. No CLI test runs a non-default window against a classification | `commands.py:267` `SweepContext(now, span, now - span, ...)` becomes `SweepContext(now, span, now - span.__class__(hours=6), ...)`: `window_start` is always 6 h whatever `--window` says **[mutated, survived; 559 passed]** | Run `--window=1h` with a transcript 2 h old and assert its class is `idle` and `summary.historical == 1`; run `--window=12h` and assert the same transcript is `person session (active)` |
| W-CC3 | `test_fr005_summary_reconciles` (`test_cli_contract.py:822-832`) checks `0 <= summary["bound_reached"] <= summary["visible"]` (line 831) | `classify.py:966` `bound_reached = sum(...)` becomes `bound_reached = 0` **[mutated, survived with the three CLI-level files `test_cli_contract.py`, `test_readonly.py`, `test_cli_registration.py`: 117 passed; I did not run the whole suite for this one, but `test_probes_allowlist.py:1065-1080` asserts `bound_reached == 10` and would fail, so the full suite catches it only there]** | `assert summary["bound_reached"] == 0` (three workers, three shows, nothing cut) |
| W-CC4 | `test_fr005_three_workers_two_worktrees_one_person_session` (`test_cli_contract.py:802-819`) checks row ids, counts and paths for the three captured workers, not their classes or rules | **[by inspection]** any class change that keeps the ids (the classes come from the captured fixtures) | Assert `(class, rule)` per captured row id, taken from the current output |

No fifth weak pick: the exit-code, publication-failure, `--run`, `--output` and `--root` tests assert exact stderr text, empty stdout and the files left behind, and the mutation set did not reach them.

### tests/sweep/test_cli_registration.py (3 tests, so fewer than five)

| # | Test (file:line) | One-line change that still passes | Stronger assertion |
|---|---|---|---|
| W-RG1 | `test_sweep_run_help_exits_zero` (`test_cli_registration.py:40-45`): `"--window" in result.output` | `commands.py:228` `default=DEFAULT_WINDOW` becomes `default="1h"` **[mutated, survived with `test_cli_registration.py`: 3 passed; `test_default_window_is_6h` (`test_cli_contract.py:502-505`) would catch it, not run]**; removing `--root`, `--output` or `--run` also leaves it green **[by inspection]** | Assert every option name (`--run`, `--window`, `--root`, `--output`) and the default `6h` in the help text |
| W-RG2 | `test_sweep_help_exits_zero` (`test_cli_registration.py:32-37`): `"run" in result.output` is a substring test | **[by inspection]** a help screen that lists a command named `runner` or `run-all` | Assert the command list: `list(sweep_group.commands) == ["run"]` and `"run  " in output` |
| W-RG3 | `test_import_is_lazy_and_runs_no_seam` (`test_cli_registration.py:48-69`) is strong: the result map records that an eager `from .commands import sweep_group` fails it (`test-cli-registration.txt` line 28) | none found | none |

### tests/sweep/conftest.py (fixtures, no tests)

- `OrcaFake.__call__` (`conftest.py:118-120`) runs `probes.check_orca_argv` only when `getattr` finds it; a rename in `probes.py` would turn the check off silently. `test_recorded_argv_fake_refuses_the_same_negatives` (`test_probes_allowlist.py:430-436`) would then fail, so it is covered, but the fake itself should import the name directly. MINOR.
- `GitFake.__call__` (`conftest.py:62-78`) calls `probes.check_git_args` unconditionally and records the argv and env; strong.
- The autouse `no_subprocess` guard reads only the test function's own marks (`conftest.py:30`); `test_the_subprocess_guard_is_live_in_this_module` (`test_readonly.py:434-437`) proves it fires.

## Findings

Mutation tally: 32 production changes were run (one at a time, in the private copy). 25 left the whole suite green (559 passed): M1-M16, A1-A3, RP1, RP2, RP5, RP8, RE1 and RO1 below. Seven were run on a subset only (C1, R2, R1, R1b, RP6, RP7, RP9); of those R1b and RP9 (partly) were caught. The sanity mutation failed 4 tests, so the harness does exercise the copy.

### AS-1 (MAJOR) JSON `worktrees[].removable` is never checked by value

- Evidence: `src/superclaude/cli/sweep/report.py:653` copies `w.removable`; `tests/sweep/test_cli_contract.py:880-891` (`_WORKTREE`) checks type `str`; `test_cli_contract.py:988-990` checks only `rows[].safe_to_close.worktree != "yes"`. Mutation RP5 (`"removable": "yes"`) left 559 passed.
- Wrong: the one machine-readable place that carries the worktree verdict can say `yes` while the suite stays green. DESIGN 7.4 (`orchestrator-mode.md:599`) pins `safe_to_close.worktree` as never `yes` (FR-012) and lists `removable` as a JSON string; the classifier is checked (`test_classify.py:246-247`), the JSON copy is not.
- Smallest fix: W-CC1 assertion.

### AS-2 (MAJOR) Four DESIGN 7.5 header lines have no test, and the file docstring says they do

- Evidence: `test_report.py:556-565` pins `lines[0]` and `lines[1]` only; no test file contains `Orca binary:`, `Sources:`, `Messages coverage:` or `Untracked paths:`; `report.py:179-183` prints them; DESIGN `orchestrator-mode.md:608-613` specifies them; `test_report.py:13-14` says a changed constant "fails here instead of passing silently". Mutations RP1 (`Messages coverage: complete`) and RP2 (`Orca binary: orca`, which NFR-003 forbids) both left 559 passed.
- Wrong: a read-only tool's coverage statement and its binary name can change to a false value unnoticed; the docstring claim is false for these lines.
- Smallest fix: W-RE1 assertion.

### AS-3 (MAJOR) `--window` never reaches a classification in any CLI-level test

- Evidence: `commands.py:267` builds `SweepContext(now, span, now - span, ...)`; `test_cli_contract.py:480-505` checks the parser and the printed `window` text only. Mutation M9 (`window_start` fixed at 6 h) left 559 passed.
- Wrong: FR-003 and FR-007 (activity window) are untested through the command; `classify` tests set the window by hand (`test_classify.py:130-139`).
- Smallest fix: W-CC2 assertion.

### AS-4 (MAJOR) The classifier-derived Sessions-table columns are not pinned

- Evidence: `classify.py:780-801` (`_lifecycle`, `_health`, `_result`) and `classify.py:921-922` (freshness and its age) fill the Lifecycle, Health, Result and Freshness columns; `test_report.py:1066-1111` prints hand-built values; `test_classify.py:499-500` checks freshness only for the future case. Mutations M12-M16 (five different changes) all left 559 passed.
- Wrong: four of the ten printed dimensions can be wrong in every real report with no failing test.
- Smallest fix: W-RE3 assertion.

### AS-5 (MAJOR) Contract file age and mtime (SP-15) are never asserted from a real read

- Evidence: `probes.py:757-758` (mtime), `probes.py:998-999` (`_age`) and `probes.py:1346` (source-row age); the Waiting (a) Age uses `ContractRecord.mtime` (`models.py:102-103`); `test_report.py:573-637` tests the sort with hand-made `ContractRecord(mtime=...)`. Mutations A1, A2 and A3 left 559 passed.
- Wrong: the age shown for a waiting contract can be zero or 1970-based with all tests green.
- Smallest fix: W-PR1 assertion.

### AS-6 (MAJOR) The realistic path of rule 2 and the window edge of rule 8 are not pinned

- Evidence: every rule-2 fixture has `transcript_readable=True` (`test_classify.py:292-303`, `542-547`) while `classify_all` gives an Orca row with no joined transcript `transcript_readable=None` (`classify.py:887`); mutation M3 (`classify.py:196` `is not False` to `is True`) left 559 passed. `test_fr010_exemptions_never_become_idle` asserts only `!= IDLE` (`test_classify.py:1008`); mutation M5 (`classify.py:314` window test removed) left 559 passed.
- Wrong: `stalled (proved)` is the strongest claim the tool makes, and `person session (active)` can be given to stale rows, each unnoticed.
- Smallest fix: W-CL5 and W-CL2 assertions.

### Minor notes (never fail the gate)

- AS-7 (MINOR) `test_rule6_partial_carries_its_note` cannot tell which side carries `partial` (M1, M2 survived): W-CL1.
- AS-8 (MINOR) `safe_to_close` for an unobserved worktree: `"no"` instead of `"could not determine"` (M6) and the `reason` text (M7) are unasserted; `test_classify.py:1515` accepts either value: W-CL3. The wrong value errs on the safe side, so MINOR.
- AS-9 (MINOR) No `last_activity == now` boundary for the future note (M4); `sorted(shared_package_ids)[0]` vs `[-1]` untested with two ids (M8): W-CL4.
- AS-10 (MINOR) Loose assertions with a stronger form in the tables above: W-PR2 (M11), W-PR3 (RP9), W-PR4, W-PR5 (RP8), W-RO1 to W-RO5 (including RO1 report mode `0o777`, RP6, RP7), W-RE2 (RE1: `delete` missing from `BANNED_WORD`), W-RE4, W-RE5, W-CC3, W-CC4, W-RG1, W-RG2, the `!=` negatives and the conditional assert at `test_classify.py:686`, and the `getattr` guard at `conftest.py:118-120`.
- AS-11 (MINOR) `test_real_git_lock_free_status_and_gitignore` does not call `probes._git` (R1: dropping `--no-optional-locks` left it green; `test_readonly.py:73-91` and `144-158` catch it); the inconclusive control only warns (`test_readonly.py:523-528`). Conclusive on this host (git 2.47.3, no warning).
- Strong, nothing to add: the allowlist and negative-argv tests, the result-class table (`test_probes_allowlist.py:605-722`), the byte-limit boundary fixtures, the budget tests, the join and window fixtures in `test_classify.py` (exact notes and classes), the sort, injection and cell tests in `test_report.py`, and the exit-code and publication-failure tests in `test_cli_contract.py` (exact stderr, empty stdout, files left behind).

## Checks

| Check | Description | Result |
|---|---|---|
| C1 | Baseline `uv run pytest tests/sweep -q`: 559 passed; matches `phase10-validation.md:62` | PASS |
| C2 | `ruff check` clean and `ruff format --check` 15 files formatted on `src/superclaude/cli/sweep` and `tests/sweep` | PASS |
| C3 | Mutation harness exercises the private copy (sanity mutation failed 4 tests); repository files unchanged | PASS |
| C4 | `conftest.py` fakes enforce the allowlists, the subprocess guard is live and proven live | PASS (minor note on `getattr` guard) |
| C5 | `test_classify.py`: five weakest tests named with a surviving one-line change and a stronger assertion | FAIL (AS-6; AS-7 to AS-9) |
| C6 | `test_probes_allowlist.py`: same | FAIL (AS-5; AS-10) |
| C7 | `test_readonly.py`: same | PASS (MINOR only: W-RO1 to W-RO5) |
| C8 | `test_report.py`: same, and DESIGN 7.5 lines have a pinning test | FAIL (AS-2, AS-4) |
| C9 | `test_cli_contract.py`: same | FAIL (AS-1, AS-3) |
| C10 | `test_cli_registration.py`: same | PASS (MINOR only: W-RG1, W-RG2) |
| C11 | Result maps agree with the disk: 559 passed, 24 in `test-readonly.txt`, 3 in `test-cli-registration.txt`, 159 in `test-classify.txt` (counts read from the maps) | PASS |
| C12 | DESIGN section 11 files exist under `tests/sweep/` and the section 12 rows spot-checked (FR-005, FR-012, FR-013, FR-017, FR-025, NFR-001 to NFR-003, NFR-010) name a test that exists; not every row was re-derived | PASS |
| C13 | Docstring claims about pinned literals hold (`test_report.py:13-14`, `test_classify.py:9-10`, `test_probes_allowlist.py:16-18`) | FAIL (AS-2 for `test_report.py`) |

Not run: a second run in a different test order and a changed clock (nothing in this lens needed them); the maps record a reverse-file-order run in `test-cli-registration.txt` lines 26-27, which I did not repeat.

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check.** No `## Inherited Structural Verdict` section was in my prompt; this is standalone behaviour. I relied on the producer's maps only for the case-to-test names, never for pass or strength.

**(b) Independent semantic checks:**
- Whole suite re-run: 559 passed, read from my own command output, not from `phase10-validation.md`.
- 32 mutations, each by a perl substitution on an exact one-match anchor in a private copy; the harness refuses an anchor that matches zero or several times (A3 was refused once and re-anchored).
- The current class for the weak fixtures was probed with `/tmp/t228-mut/probe.py` (exemption rows, future-dated session, rule 2 with `transcript_readable=None`, `safe_to_close` variants, `partial` variants), so each "stronger assertion" above names a value the current code gives.
- Tool engagement (approximate counts): Read about 75 calls (all test files and cited source ranges in chunks of at most 150 lines), Grep 9, Bash 13 (baseline, ruff, four harness runs, probe, git status, line anchors), Write 6 (report stub, four harness scripts, probe), Edit about 12 (harness and report sections). No web research was done, so no Tavily call was needed.
- Confidence: Verified 11 of 13 checks by direct tool evidence; Unverifiable 0; Unchecked 0 (C12 is scoped as stated). Items marked **[by inspection]** (W-PR4, W-RO4, W-RE4, W-RE5, W-CC4, W-RG2) are weak on their face and I did not mutate them.

## Recommendations

1. Add the six assertions in AS-1 to AS-6 (each is one test or one extra case, using fixtures that already exist in `conftest.py` and the test files) and re-run the 25 surviving mutations; each should then fail at least one test.
2. Widen `BANNED_WORD` and pin the nine `NEXT_INSPECTION` values (W-RE2); change the real-git test to call `probes._git` (W-RO1).
3. No code change in `src/superclaude/cli/sweep/` is needed for these findings; every mutation above was a test-strength probe, not a defect found in the shipped code.

## QA Complete

Verdict: FAIL
Blocking count: 6

