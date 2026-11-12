# Fix Log - cycle 1 (tests gate, F_0 = TST-F1 to TST-F6)

**Date:** 2026-11-12
**fix_authorization:** true
**Scope:** six test-strength findings, fixed in `tests/sweep/` only (source changes are listed below if any were needed).

Sections are appended below as each finding is finished.

## Files edited

- `tests/sweep/test_cli_contract.py` (TST-F1, TST-F3)
- `tests/sweep/test_report.py` (TST-F2, TST-F4; `ruff format` was run on this file only, it joined one constant onto one line)
- `tests/sweep/test_probes_allowlist.py` (TST-F5)
- `tests/sweep/test_classify.py` (TST-F6)
- Result maps in `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/`: `test-classify.txt` (159 to 161 tests), `test-cli-contract.txt` (90 to 94), `test-probes-allowlist.txt` (242 to 243), `test-report.txt` (41 to 48). Each pytest stdout block is the real new `-v` output; each new test is added to the file's case-to-test map.
- `tests/sweep/conftest.py`: no helper was needed.
- Source modules under `src/superclaude/cli/sweep/`: no change. No strengthened test exposed a bug; every mutation below was applied only in the private copy.

## Discrimination method

A private copy of `src/`, `tests/sweep/`, `pyproject.toml` and `.gitignore` was made under `/tmp/t232/` and imported through `PYTHONPATH=/tmp/t232/src`; the pytest run printed paths under `/tmp/t232/`, and the unmutated copy gave 573 passed (the repository count after the fix). Each mutation was one exact-text change to one copied module, restored from a pristine copy before the next. The copy was deleted afterwards (`ls /tmp/t232` reports no such directory). No repository file was mutated.

## TST-F1 - FIXED

- Change: new test `test_json_worktree_values_are_exact_and_removable_is_never_yes` in `tests/sweep/test_cli_contract.py:1018`. For the two worktrees of `_captured_world` it asserts the paths and, per worktree, `status_read is True`, `uncommitted is False`, `unpushed is None`, `removable == "no"`, `removable_reason == "unpushed branch: no upstream"` (values observed from the real run, not guessed), and `all(w["removable"] in ("no", "could not determine") ...)` (FR-012).
- file:line after the change: `tests/sweep/test_cli_contract.py:1018`.
- Discrimination proof: mutation RP5, `report.py` `"removable": w.removable,` changed to `"removable": "yes",`. Failing test: `test_json_worktree_values_are_exact_and_removable_is_never_yes`.

## TST-F2 - FIXED

- Change: constant `WORKTREES_BANNER` (`tests/sweep/test_report.py:66`); `test_header_has_the_seven_exact_lines_of_design_7_5` (`:571`) pins all seven header lines (`Orca binary: orca-ide`, `Sources: orca worker-list R1 read (age 5s) . remote hosts unknown`, `Messages coverage: partial`, the UNVERIFIED lock-risk line, the `Untracked paths:` line, plus the two already pinned); `test_header_sources_line_says_none_when_there_are_no_sources` (`:591`); `test_discovery_incomplete_banner_is_in_the_header_only_when_discovery_is_incomplete[ps-unscanned|complete|orca-unavailable]` (`:607`) asserts the banner is in `header_block(text)` for `full_result` and for an Orca-unavailable result, absent for `empty_result`, and printed once.
- file:line after the change: `tests/sweep/test_report.py:66`, `:571`, `:591`, `:607`.
- Discrimination proof (all in `report.py`, private copy):
  - RP1 `"Messages coverage: partial"` to `"Messages coverage: complete"`: fails `test_header_has_the_seven_exact_lines_of_design_7_5`.
  - RP2 `f"Orca binary: {sanitize(result.orca_binary)}"` to the literal `"Orca binary: orca"`: fails `test_header_has_the_seven_exact_lines_of_design_7_5`.
  - `Untracked paths:` line text changed: fails `test_header_has_the_seven_exact_lines_of_design_7_5`.
  - `Sources:` age suffix dropped: fails `test_header_has_the_seven_exact_lines_of_design_7_5`.
  - Banner never printed (`if _discovery_incomplete(result):` to `if False:`): fails `test_discovery_incomplete_banner_is_in_the_header_only_when_discovery_is_incomplete[ps-unscanned]`.
  - Banner always printed (`if True:`): fails `test_discovery_incomplete_banner_is_in_the_header_only_when_discovery_is_incomplete[complete]`.

## TST-F3 - FIXED

- Change: new parametrized test `test_window_reaches_the_classification[1h-is-idle|12h-is-active|2h-edge-is-active]` in `tests/sweep/test_cli_contract.py:517`. An empty Run (join guard holds) plus one transcript 2 h old; `--window=1h` gives class `idle`, `summary.historical == 1`, `visible == 0`, `counts.idle == 1`; `--window=12h` and the edge `--window=2h` (`last_activity == window_start`) give `person session (active)` with `historical == 0`.
- file:line after the change: `tests/sweep/test_cli_contract.py:517`.
- Discrimination proof: mutation M9, `commands.py` `SweepContext(now, span, now - span, checkout, runs)` changed to `SweepContext(now, span, now - span.__class__(hours=6), checkout, runs)` (window_start fixed at 6 h). Failing test: `test_window_reaches_the_classification[1h-is-idle]`.

## TST-F4 - FIXED

- Change: helpers `dimension_cells` and `ttail` and two tests in `tests/sweep/test_report.py`. Both go through `classify_all` and `report.render`; no dimension value is set by hand.
  - `test_lifecycle_health_and_result_cells_come_from_the_classifier` (`:1183`): a settled row with a succeeded contract gives `(settled, unknown, succeeded, unknown)`; a settled row with a failed contract `(settled, failed result, failed, unknown)`; a running row with no contract `(running, unknown, unknown, unknown)`; a no-outcome row with a blocked contract `(unknown, unknown, null, unknown)` (Lifecycle, Health, Result, Freshness).
  - `test_freshness_cell_comes_from_the_classifier_for_a_fresh_and_a_stale_transcript` (`:1216`): a 5 min old transcript prints `fresh (300s)`; an unreadable 7 h old transcript prints `stale (25200s)` in the Sessions table; a readable 7 h old transcript is classed idle, has `row.freshness == "stale"` and `freshness_age_s == 25200`, and is listed under Historical sessions. The transcripts run in their own `classify_all` call because an in-scope Orca row would stop them joining (join guard), which would make the freshness `unknown`.
- file:line after the change: `tests/sweep/test_report.py:1162` (`dimension_cells`), `:1170` (`ttail`), `:1183`, `:1216`; imports `replace` (line 22) and `TranscriptTail`.
- Discrimination proof (all in `classify.py`, private copy):
  - M12 `_lifecycle` returns `"running"` always: fails `test_lifecycle_health_and_result_cells_come_from_the_classifier`.
  - M13 `_health` `"failed result"` to `"unknown"`: fails the same test.
  - M14 `_result` blocked `"null"` to `"blocked"`: fails the same test.
  - M15 fresh and stale swapped (line 921): fails `test_freshness_cell_comes_from_the_classifier_for_a_fresh_and_a_stale_transcript`.
  - M16 `freshness_age_s` set to `0` (line 922): fails the same freshness test.

## TST-F5 - FIXED

- Change: new test `test_contract_mtime_and_source_age_come_from_the_file_time` in `tests/sweep/test_probes_allowlist.py:1362`. It writes a contract with `sweep_root.contract()`, sets its time with `os.utime` to `NOW - 1 h`, patches `probes._utcnow` to `NOW` (`collect` reads the real clock through that function, so without the patch the age could not be asserted), then asserts `read_contract(path, root).mtime == NOW - 1 h` (timezone-aware), that the `contract <dispatch>` source row is `("read", 3600)` for `(coverage, age_seconds)`, and that the collected `ContractRecord.mtime` equals the same value.
- file:line after the change: `tests/sweep/test_probes_allowlist.py:1362`.
- Discrimination proof (all in `probes.py`, private copy); failing test in each case: `test_contract_mtime_and_source_age_come_from_the_file_time`:
  - A1 `_age` returns `0`.
  - A2 the source row built with age `None` instead of `_age(now, record.mtime)`.
  - A3 `_contract` reads the file time as `datetime.fromtimestamp(0, timezone.utc)`.

## TST-F6 - FIXED

- Change in `tests/sweep/test_classify.py`:
  - `test_rule_2_stalled_holds_when_no_transcript_was_joined` (`:550`): exit proof with `transcript_readable=None` gives `("orca_exit_proof", STALLED)`; the same row with `transcript_readable=False` still gives `("fallback", UNKNOWN)`.
  - `test_rule_2_stalled_through_classify_all_for_an_orca_row_with_no_transcript` (`:564`): the realistic path; an exited Orca row with no joined transcript has `row.transcript_readable is None` and is `("orca_exit_proof", STALLED)`.
  - `test_fr010_exemptions_never_become_idle` (`:1044`) is now parametrized with the exact `(rule, class_name)` per case and asserts equality instead of `!= IDLE`: `unreadable-transcript`, `unknown-timestamp`, `open-task`, `unread-report-candidate` give `("fallback", "could not determine")`; `explicit-wait` gives `("waiting_signal", "waiting on a person")`. The case fixtures use `last_activity=at(1)`, 11 h before `now` and outside the 6 h window, which is what makes the rule 8 window edge visible (comment added at the test).
- file:line after the change: `tests/sweep/test_classify.py:550`, `:564`, `:1044`.
- Discrimination proof (private copy, `classify.py`):
  - M3 rule 2 condition `row.transcript_readable is not False` changed to `is True`: fails `test_rule_2_stalled_holds_when_no_transcript_was_joined` and `test_rule_2_stalled_through_classify_all_for_an_orca_row_with_no_transcript`.
  - M5 rule 8 `and last >= ctx.window_start` changed to `and True`: fails `test_fr010_exemptions_never_become_idle[open-task]` and `test_fr010_exemptions_never_become_idle[unread-report-candidate]`.

## Re-check commands (run in this order after the last edit)

1. `uv run ruff check src/superclaude/cli/sweep tests/sweep`
   - exit code 0; last line: `All checks passed!`
   - PASS
2. `uv run ruff format --check src/superclaude/cli/sweep tests/sweep`
   - First run exited 1 (`tests/sweep/test_report.py` would be reformatted: the `WORKTREES_BANNER` constant fits on one line). I ran `uv run ruff format tests/sweep/test_report.py` (that file only, exit 0, `1 file reformatted`) and re-ran the check.
   - exit code 0; last line: `15 files already formatted`
   - PASS
3. `uv run pytest tests/sweep -v`
   - exit code 0; last line: `============================= 573 passed in 2.00s ==============================` (559 before, 14 added: TST-F1 1, TST-F2 5, TST-F3 3, TST-F4 2, TST-F5 1, TST-F6 2)
   - PASS
4. `uv run pytest tests/sweep -m integration -v`
   - exit code 0; last lines: `tests/sweep/test_readonly.py::test_real_git_lock_free_status_and_gitignore PASSED [100%]` and `====================== 1 passed, 572 deselected in 0.40s =======================` (exactly 1 selected)
   - PASS

All four exit 0.

## Executor check after the fix agent returned

Written by the executor, not the fix agent. No live re-run was needed: no module under `src/superclaude/cli/sweep/` changed (the sha256 of all six modules is identical to before the agent ran). The protected-file hash check (68 files: QA reports, consolidated file, ledger, prompts, artifacts, discovery and plans, captured fixtures, DESIGN, SPEC, plan file, `phase10-validation.md`, `main.py`) showed no change.

## Not touched

DESIGN (`docs/designs/orchestrator-mode.md`), the SPEC, the plan file, every QA report and `consolidated-findings-cycle0.md`, `cycle-ledger.md`, `phase10-validation.md`, everything under `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/`, the captured fixtures `tests/sweep/fixtures/captured-*.json`, `tests/sweep/conftest.py`, `tests/sweep/test_readonly.py`, `tests/sweep/test_cli_registration.py`, every module under `src/superclaude/cli/sweep/`, the result maps `test-readonly.txt` and `test-cli-registration.txt`, and every `.claude/` path. Nothing was staged or committed; no live Orca, ccsession or Claude command was run; no background process was started. The MINOR findings TST-F7 to TST-F45 were left alone.
