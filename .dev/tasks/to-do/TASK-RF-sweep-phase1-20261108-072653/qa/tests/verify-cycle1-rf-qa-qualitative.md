# Verify Cycle 1 - rf-qa-qualitative

**Date:** 2026-11-12
**Phase:** fix-cycle verification (cycle 1)
**fix_authorization:** false (report-only)

**Task:** TASK-RF-sweep-phase1-20261108-072653 (tests gate, fix cycle 1 of at most 2; item 10.18 verifier, prompt T234)
**Inputs read from disk now:** `consolidated-findings-cycle0.md` (TST-F1 to TST-F45), `fix-log-cycle1.md`, `cycle-ledger.md`, the seven `qa-*-report.md`, `tests/sweep/` (the changed passages in full, the rest by grep and by running it), the six result maps and `phase10-validation.md`, DESIGN sections 7.4, 7.5, 11, 12, and `src/superclaude/cli/sweep/` (`classify.py`, `report.py`, `probes.py`, `commands.py` ranges).
**Constraints kept:** no live Orca, ccsession or Claude command; no background loop; no repository file changed except this report (see "Private copy" below).

## Summary

- Verdict: PASS. Blocking count: 0.
- All six cycle-0 findings (TST-F1 to TST-F6, all MAJOR) are RESOLVED. For each I broke the guarded behaviour in a private copy under `/tmp` and the new test failed; every test the fix log names as the failing one failed in my runs too (RP2 and the banner mutations also failed one to three more tests than the log lists).
- All 102 check ids of the cycle-0 PASS set still pass (none regressed).
- No new BLOCKING or MAJOR finding. Seven new MINOR notes (TST-F46 to TST-F52): one over-broad comment in a test (TST-F46), three passages that do not say why a value is pinned or what a case proves (TST-F47 to TST-F49), one result-map placement (TST-F50), one widening of an existing temp-folder dependency (TST-F51), one stale-count note (TST-F52). They are notes and never fail the review.

## Gate commands run by me now

| Command | Result |
|---|---|
| `uv run pytest tests/sweep -v` | exit 0, `573 passed in 1.64s` (559 before; 161 + 94 + 3 + 243 + 24 + 48 = 573 by file) |
| `uv run pytest tests/sweep -m integration -v` | exit 0, `1 passed, 572 deselected`; the one test is `test_real_git_lock_free_status_and_gitignore` |
| `uv run ruff check src/superclaude/cli/sweep tests/sweep` | `All checks passed!` |
| `uv run ruff format --check src/superclaude/cli/sweep tests/sweep` | `15 files already formatted` |

## What the fix changed, and what it did not

- Changed: `test_cli_contract.py` (1409 to 1456 lines), `test_report.py`, `test_probes_allowlist.py` (1934 to 1958, exactly the 24 lines of one new test block), `test_classify.py` (1851 to 1891: two new tests and the exemption test), and the four result maps. The collected node ids of each of the four maps equal the ids that pytest collects now (148, 94, 232 and 48 unique stems; 161, 94, 243 and 48 tests), and the pytest blocks end `161`, `94`, `243` and `48 passed`.
- Not changed (verified, not taken from the fix log): the six modules under `src/superclaude/cli/sweep/` (`sha256sum -c /tmp/t232-src-before.sha`, the executor's pre-fix hashes: 6 of 6 `OK`); `tests/sweep/conftest.py` (mtime 04:04), `test_readonly.py` (04:44), `test_cli_registration.py` (04:59) and every file under `tests/sweep/fixtures/` (22:36 the day before), all older than the cycle-0 reports (05:24 to 05:32). The executor's 68-file protected list (`/tmp/t232-protected-before.sha`): 67 of 68 match now. The one that differs is the plan file `TASK-RF-sweep-phase1-20261108-072653.md`, modified 05:53, after the fix log (05:52): the executor ticking its checklist, not a gate input.

## Private copy

Every experiment ran in `/tmp/v234x` (a copy of `src/`, `tests/sweep/`, `tests/conftest.py`, `pyproject.toml`, `.gitignore`, run with the repository's `.venv/bin/pytest` and `PYTHONPATH` set to the copy). A sanity mutation (`"failed result"` to `"XX failed result"`) failed the dimension test, which proves the copy is the code under test. The copy and its helper folders were deleted (`ls -d /tmp/v234*` finds nothing).

## Discrimination re-proof (25 mutations, one change at a time, restored after each)

| Id | Change in the copy | Tests that fail (all else passes) |
|---|---|---|
| RP5 | `report.py` `"removable": w.removable` to `"yes"` | `test_json_worktree_values_are_exact_and_removable_is_never_yes` |
| RP1 | `Messages coverage: partial` to `complete` | `test_header_has_the_seven_exact_lines_of_design_7_5` |
| RP2 | `Orca binary:` line made the literal `orca` | the seven-lines test and `test_header_sources_line_says_none_when_there_are_no_sources` |
| RP3 | the `(age Ns)` suffix of `Sources:` dropped | the seven-lines test |
| RP4 | `Untracked paths:` line text changed | the seven-lines test |
| RP6 | `Sources: none` text changed | the `says_none` test |
| B-never / B-always | banner `if False:` / `if True:` | `[ps-unscanned]`, `[orca-unavailable]` (and two binding tests) / `[complete]` and the seven-lines test |
| B-ps-branch / B-orca-branch | `_discovery_incomplete`: ps branch returns False / Orca-unavailable branch dead | `[ps-unscanned]` / `[orca-unavailable]` |
| M9 | `commands.py` window start fixed at 6 h | `test_window_reaches_the_classification[1h-is-idle]` |
| M12 / M13 / M14 | `_lifecycle` always `running` / `_health` no `failed result` / blocked prints `blocked` | `test_lifecycle_health_and_result_cells_come_from_the_classifier` (each) |
| M15 / M16 / X1 | freshness swapped / age 0 / `stale` never true | `test_freshness_cell_comes_from_the_classifier_for_a_fresh_and_a_stale_transcript` (each) |
| A1 / A2 / A3 / A4 | `_age` returns 0 / source row age None / contract mtime epoch 0 / source age from `now` | `test_contract_mtime_and_source_age_come_from_the_file_time` (each) |
| M3 | rule 2 `is not False` to `is True` | `test_rule_2_stalled_holds_when_no_transcript_was_joined`, `test_rule_2_stalled_through_classify_all_for_an_orca_row_with_no_transcript` |
| M5 | rule 8 `last >= window_start` to `True` | `test_fr010_exemptions_never_become_idle[open-task]` and `[unread-report-candidate]` only |
| X2 | rule 8 drops `transcript_readable is True` | none: an equivalent mutant, because `classify()` forces every row with `transcript_readable is False` to `could not determine` afterwards (`classify.py:376-377`) |

## Determinism and isolation of the 14 new tests (private copy)

Reverse file order: 573 passed. `TZ` = Pacific/Kiritimati, America/Adak, Asia/Kolkata, UTC: 573 each. `PYTHONHASHSEED` 0, 1, 2, 99: 573 each. `LC_ALL=C PYTHONUTF8=0`: 573. Wall clock seen by `probes._utcnow` shifted by -400 days, +3650 days, -8.6 s, +0.5 s: 573 each; control: with `_utcnow` made to raise, 90 tests fail, among them the three `test_window_reaches_the_classification` cases, so the seam is reached and the shift was effective. Each new test alone: all pass. Temp folder through a symlink: pass. Temp folder whose name holds a space: the new TST-F5 test fails (see TST-F51). My runs in the repository (the four gate commands, a second `uv run pytest tests/sweep -q` giving `573 passed`, and `--collect-only` runs) changed nothing under `tests/sweep/`, `src/superclaude/cli/sweep/`, `docs/designs/` or `.dev/sweeps/` (0 files newer than 05:49 in each; `.dev/sweeps/` still holds only the four 03:11 to 03:45 reports). Other files in the checkout changed during this review (`.codegraph/` index files, the executor's `progress.md` and plan file, a sibling verifier's report `verify-cycle1-rf-qa.md`); they are not from my commands.

## Findings of the cycle-0 list F_0

### TST-F1 (MAJOR): RESOLVED

Evidence: `tests/sweep/test_cli_contract.py:1018-1037` `test_json_worktree_values_are_exact_and_removable_is_never_yes` asserts the two worktree paths, `status_read is True`, `uncommitted is False`, `unpushed is None`, `removable == "no"`, `removable_reason == "unpushed branch: no upstream"` for each, and `all(w["removable"] in ("no", "could not determine") ...)` (FR-012, DESIGN 7.4 line 599). Mutation RP5 (`report.py:653` copies `"yes"`) fails exactly this test; before the fix it left 559 passed. The values `no` and `None` agree with DESIGN section 2.2 line 72 (a branch with no upstream is `removable: no` while `unpushed` stays None); the reason wording is the classifier's (`classify.py:454`), see TST-F47.

### TST-F2 (MAJOR): RESOLVED

Evidence: `tests/sweep/test_report.py:571-588` pins all seven DESIGN 7.5 header lines as literals (`Orca binary: orca-ide`, `Sources: orca worker-list R1 read (age 5s) . remote hosts unknown`, `Messages coverage: partial`, the UNVERIFIED lock-risk line, the `Untracked paths:` line); `:591` pins `Sources: none` and the binary line for an empty result; `:607` asserts the banner (`WORKTREES_BANNER`, `:66`, identical to DESIGN 7.5 line 614) is in `header_block(text)` and printed once for `full_result` (ps unscanned) and for an Orca-unavailable result, and absent for `empty_result`. Mutations RP1 to RP4, RP6, B-never, B-always, B-ps-branch and B-orca-branch each fail at least one of these tests (table above); cycle 0 left RP1, RP2, M3, M19, M20, M23 and M24 green. The file docstring claim at `test_report.py:13-14` ("a changed constant ... fails here instead of passing silently") is now true for these lines. The map entries 24 and 25 in `test-report.txt:99-101` state what the tests do and match `_discovery_incomplete` (`report.py:155-158`).

### TST-F3 (MAJOR): RESOLVED

Evidence: `tests/sweep/test_cli_contract.py:508-530` `test_window_reaches_the_classification[1h-is-idle|12h-is-active|2h-edge-is-active]` runs the command with an empty Run and one transcript 2 h old: `--window=1h` gives class `idle`, `historical == 1`, `visible == 0`, `counts.idle == 1`; `12h` and the edge `2h` (`last_activity == window_start`, rule 8 is `>=`) give `person session (active)` and `historical == 0`. Mutation M9 (`commands.py:267` window start fixed at 6 h) fails `[1h-is-idle]`; before the fix it left 559 passed. This is the case the consolidated file asked for (1h idle, 12h active).

### TST-F4 (MAJOR): RESOLVED

Evidence: `tests/sweep/test_report.py:1162-1247`. `dimension_cells` reads Lifecycle, Health, Result and Freshness from the printed Sessions table; both tests build the input, run `classify_all`, then `render` (no cell set by hand). `test_lifecycle_health_and_result_cells_come_from_the_classifier` pins four rows: settled with a succeeded contract `(settled, unknown, succeeded, unknown)`, settled with a failed contract `(settled, failed result, failed, unknown)`, running with no contract, and a no-outcome row with a blocked contract `(unknown, unknown, null, unknown)`. `test_freshness_cell_comes_from_the_classifier_for_a_fresh_and_a_stale_transcript` pins `fresh (300s)` and `stale (25200s)` (5 min and 7 h, arithmetic from the fixture, not from the printout) and the idle/Historical placement of a readable stale transcript. Mutations M12 to M16 and X1 each fail one of the two tests; before the fix five different changes left 559 passed.

### TST-F5 (MAJOR): RESOLVED

Evidence: `tests/sweep/test_probes_allowlist.py:1362-1383` writes a contract, sets its time with `os.utime` to `NOW - 1 h`, patches `probes._utcnow` to `NOW`, then asserts `read_contract(...).mtime == NOW - 1 h` (aware), the `contract <dispatch>` source row is `("read", 3600)` and the collected `ContractRecord.mtime` is the same. Mutations A1 to A4 each fail it; before the fix A1 to A3 left 559 passed. The time is a whole even second, so file systems with 1 s or 2 s mtime granularity give the same value.

### TST-F6 (MAJOR): RESOLVED

Evidence: `tests/sweep/test_classify.py:550-561` (`transcript_readable=None` with exit proof gives `("orca_exit_proof", STALLED)`; `False` gives `("fallback", UNKNOWN)`), `:564-579` (the same through `classify_all` for an Orca row with no joined transcript, asserting `row.transcript_readable is None`), and `:999-1048` (`test_fr010_exemptions_never_become_idle` now compares the exact `(rule, class_name)` per case: four `("fallback", UNKNOWN)` and `explicit-wait` `("waiting_signal", WAITING)`, equality instead of `!= IDLE`). Mutation M3 fails both rule-2 tests; M5 fails `[open-task]` and `[unread-report-candidate]`; before the fix both left 559 passed. This also closes qa-classify-coverage F4 (merged into TST-F6).

## New findings from re-reading the changed passages (all MINOR, notes only)

I read each new or changed test, the four updated result maps and the fix log as a maintainer who has not seen the cycle: what does the test prove, why is each fixed value pinned, what does a failure mean. Names, structure and the TST-id comments are clear; the discrimination proofs of the fix log are accurate. The following passages mislead a little. None makes an assertion wrong, and no test pins a value that the DESIGN or the fixture does not support; all seven are one-line fixes.

### TST-F46 (MINOR): the comment in the exemptions test says more than the five cases prove

- Where: `tests/sweep/test_classify.py:1045-1046`: "`last_activity` is at(1), 11 h before `now` and outside the 6 h window, so a missing window test in rule 8 would turn these rows into `person session (active)`."
- What is off: measured with mutation M5, only `[open-task]` and `[unread-report-candidate]` fail. `[unreadable-transcript]` is forced to `could not determine` after the rules (`classify.py:376-377`), `[unknown-timestamp]` has `last_activity=None` (not `at(1)`), and `[explicit-wait]` is taken by rule 4 first. A maintainer could think all five cases guard the window edge. The fix log's wording ("what makes the rule 8 window edge visible") is true for the two cases that need it.
- Why MINOR: the assertions (exact `(rule, class_name)` per case) are right and DESIGN-backed; only the comment's reach is too wide, and the strengthened test still kills M5. Smallest fix: "... so dropping the window test in rule 8 turns `open-task` and `unread-report-candidate` into `person session (active)`; the other three cases pin their own rule."

### TST-F47 (MINOR): `removable == "no"` and its reason text are pinned without saying why

- Where: `tests/sweep/test_cli_contract.py:1019-1033`.
- What is off: the comment explains `status_read`, `uncommitted` and `unpushed` ("a clean branch with no upstream line") but not that this is what makes `removable` equal `no` (DESIGN section 2.2 line 72: a branch with no upstream is `removable: no` although `unpushed` stays None). The exact string `unpushed branch: no upstream` is the classifier's wording (`classify.py:454`); DESIGN names only the condition `no upstream`, so a harmless reword of the reason would fail this CLI-level test. The fix log says the values were observed from the run; the test does not say so.
- Smallest fix: one comment line citing DESIGN 2.2 line 72 and saying the reason string is the classifier's wording.

### TST-F48 (MINOR): the `null`, `failed result` and `settled` cells have no source in the test

- Where: `tests/sweep/test_report.py:1183-1213`.
- What is off: the test prints `null` as the Result of a blocked contract and `unknown` for every Health that is not a failed contract. The source is the REPORT step row at `RESEARCH-REPORT-orchestrator-mode.md:1248`, cited only in comments of `classify.py:781, 789, 800`. A reader of the test alone sees the string `null` and may take it for a bug. The values are not "pinned because the code printed them": they match that row.
- Smallest fix: one comment line naming that REPORT row.

### TST-F49 (MINOR): two small imprecisions in the header and banner tests

- Where: `tests/sweep/test_report.py:572-574` and `:601`.
- What is off: the comment says "the four lines after the scope line were unpinned"; five lines follow the scope line and the lock-risk one was already pinned by `test_orca_lock_risk_line_by_observed_version`. The `ps-unscanned` case expects a banner whose DESIGN 7.5 literal says "Orca unavailable" while Orca is available; the test and the map do not say that the literal is DESIGN's and is shown for either cause.
- Smallest fix: reword "four" to "the first four of the five", add "(the banner text is DESIGN's for both causes)" to the param comment.

### TST-F50 (MINOR): result-map case 23a sits under the wrong heading

- Where: `phase-outputs/test-results/test-probes-allowlist.txt:298`, inside "E. FR-020: byte limits".
- What is off: the new case is the SP-15 contract age (mtime and source-row age), not a byte limit. It is labelled `(TST-F5 ...)`, so it can be found, but a reader looking for age coverage would not look under E.
- Smallest fix: move it to its own heading or to the block of section F.

### TST-F51 (MINOR): the new TST-F5 test adds a third test that depends on the shape of the temp folder

- Where: `tests/sweep/test_probes_allowlist.py:1362` through `_stock_contract_run` (defined at `:1462`); same cause as TST-F42 (`_CONTRACT_PATH_RE`, `probes.py:1014`, stops at whitespace, quotes and parentheses).
- Evidence: with `TMPDIR` set to a folder whose name holds a space, three tests fail: `test_a_contract_over_1_mib_is_unscanned_with_a_reason`, `test_a_contract_that_changes_on_every_read_is_an_inconsistent_observation` (both TST-F42) and now `test_contract_mtime_and_source_age_come_from_the_file_time`. A symlinked temp folder passes.
- Why MINOR: unusual host setup only; same smallest fix as TST-F42 (skip with a reason when the path holds a stop character).

### TST-F52 (MINOR): two result files still show the pre-fix counts

- Where: `phase10-validation.md:62, 80, 89` (`559 passed`, `558 deselected`) and `test-cli-registration.txt:26-27` (`469 passed`, already stale at cycle 0, TST-F45).
- What is off: both are dated run records and the fix did not touch them (the fix log says so). The post-fix gate numbers (573, 1 of 573) are only in `fix-log-cycle1.md`. A later reader who takes `phase10-validation.md` as the current gate state gets 559.
- Smallest fix: when the phase 10 gate is re-recorded, regenerate `phase10-validation.md`; until then the fix log is the record. Not needed for this gate.

## Checks

One row per check id of the cycle-0 PASS set (102). The first word of each result is PASS or FAIL. The letters in brackets say how the check was confirmed:

- **R**: re-checked now by me (command, grep or read); the detail is in the cell.
- **N**: every test the check names still exists (a grep of the 276 `def test_` names in `tests/sweep/` against every `test_*` name cited in the seven reports: no cited name is missing, only file names and cut-off stems) and passes in the 573-test run.
- **U**: the check is about a file the fix did not change (the six `src/` modules by sha256, `conftest.py`, `test_readonly.py`, `test_cli_registration.py` and `fixtures/` by mtime, all older than the cycle-0 reports).
- **A**: the check describes a saved artifact or a scratch run of a cycle-0 agent (it cannot be re-run); I confirmed from disk that nothing the check relied on was changed or weakened by the fix, and the cell says so.
- **D**: a count or line number moved because of the fix (559 to 573 tests, +24 lines after `test_probes_allowlist.py:1362`, +32/+40 lines in `test_classify.py`), and the claim itself still holds.

| Check id | Result |
|---|---|
| qa-classify-coverage-report:C1 | PASS (R, D) suite 573 passed, `test_classify.py` 161 passed, ruff check and format clean; counts moved from 559 and 159 |
| qa-classify-coverage-report:C2 | PASS (N) rule 1 to 9 case, `CLASSES` and rule-order tests exist and pass |
| qa-classify-coverage-report:C3 | PASS (N, D) window, `last_activity` source and future-timestamp tests exist; lines before `:550` did not move |
| qa-classify-coverage-report:C4 | PASS (N) the FR-008 four-input test and the late-heartbeat case exist and pass |
| qa-classify-coverage-report:C5 | PASS (N, R) `test_fr009_case_1` and `_case_2` still assert `notes == (N_EXITED,)` (read at `test_classify.py:582-597`) |
| qa-classify-coverage-report:C6 | PASS (N) rule 1 decline-note tests and the rule 5 four-condition test exist |
| qa-classify-coverage-report:C7 | PASS (N) the FR-010 control test exists and passes |
| qa-classify-coverage-report:C8 | PASS (N) the three SPEC incomplete-case fixtures exist; their note constants equal `classify.py` (C20) |
| qa-classify-coverage-report:C9 | PASS (N) the three non-SPEC fixtures and the note-order fixture exist |
| qa-classify-coverage-report:C10 | PASS (R) the exemptions test is now exact per case (`:999-1048`), SP-29 test unchanged (`:1063-1090`, read); the F4 note of this check is resolved by TST-F6 |
| qa-classify-coverage-report:C11 | PASS (N) the `person_started` None, D9 join, guard-case and SPEC line 236 tests exist |
| qa-classify-coverage-report:C12 | PASS (N) the R2-B1 pane-reuse tests exist |
| qa-classify-coverage-report:C13 | PASS (N) the five R3-B1 window tests exist in `test_classify.py` |
| qa-classify-coverage-report:C14 | PASS (N, D) the six time-field tests exist in `test_probes_allowlist.py` (now `:1856-1951`, moved by +24) |
| qa-classify-coverage-report:C15 | PASS (N) the ten R3-B2 several-rows tests exist |
| qa-classify-coverage-report:C16 | PASS (N) SP-07, `FINAL:`, unreadable-input, WC-13 and rule 6 wording tests exist |
| qa-classify-coverage-report:C17 | PASS (N) FR-012 to FR-015 and FR-005 tests exist |
| qa-classify-coverage-report:C18 | PASS (N) the AST import tests and the B5 test exist; the map's "16 forms" slip (TST-F10) is unchanged, as at cycle 0 |
| qa-classify-coverage-report:C19 | PASS (R) the three `collect` source-row tests are still at `test_probes_allowlist.py:1177`, `:1216`, `:1242` (the block the check cites, `:1177-1268`, lies above the one inserted test at `:1362`) |
| qa-classify-coverage-report:C20 | PASS (R) I compared the 25 note constants at `test_classify.py:67-93` one by one with `classify.py:54-85` and DESIGN 7.2: byte-equal |
| qa-classify-coverage-report:C21 | PASS (A) the cycle-0 mutations MU1 to MU11 probed tests the fix left as they were, apart from the exemptions test, which only got stronger |
| qa-classify-coverage-report:C22 | PASS (R) no DESIGN 11 case lacks a test; `test_classify.py` grew from 1851 to 1891 lines by exactly two new tests and the exemptions edit, nothing removed |
| qa-classify-coverage-report:C23 | PASS (R) `test-classify.txt` lists 161 ids, equal to the 161 that pytest collects; its case map lists the two new tests (entries 18 and 18a); the "16 forms" slip stays (TST-F10) |
| qa-classify-coverage-report:C24 | PASS (A) the cycle-0 private copy is gone (`/tmp/qa-t224*` absent) and no repository file other than the report was changed by that review; nothing on disk contradicts it |
| qa-probes-readonly-coverage-report:C1 | PASS (N) the exact-set pin tests of the ten templates, seven verbs and constants exist |
| qa-probes-readonly-coverage-report:C2 | PASS (N) the negative-argv tests (24 ids) exist |
| qa-probes-readonly-coverage-report:C3 | PASS (N) the two `worktree ps --agent-wait` acceptance tests exist |
| qa-probes-readonly-coverage-report:C4 | PASS (N) the FR-021 forbidden-verb tests exist; the F4 note (scans `probes.py` only) is unchanged |
| qa-probes-readonly-coverage-report:C5 | PASS (N) the git negative tests and the one allowed git call tests exist |
| qa-probes-readonly-coverage-report:C6 | PASS (N) the full-sweep recording tests exist |
| qa-probes-readonly-coverage-report:C7 | PASS (N) the result-class tests and the captured no-binding test exist |
| qa-probes-readonly-coverage-report:C8 | PASS (R) the `collect` source-row and `truncated` tests are at `:1177`, `:1216`, `:1242` |
| qa-probes-readonly-coverage-report:C9 | PASS (N) the budget tests exist; the F1 and F6 notes are unchanged |
| qa-probes-readonly-coverage-report:C10 | PASS (N) the byte-limit and nine-boundary tests exist |
| qa-probes-readonly-coverage-report:C11 | PASS (N) the six failure-mode tests (lines 440, 443, 446, 450, 451, 452) exist; the F5 note is unchanged |
| qa-probes-readonly-coverage-report:C12 | PASS (N) the `parse_status` tests exist |
| qa-probes-readonly-coverage-report:C13 | PASS (N, D) the six R3-B1 time-field tests exist, now at `:1856-1951` |
| qa-probes-readonly-coverage-report:C14 | PASS (U) `test_readonly.py` is unchanged (04:44) and passes (24 of 24) |
| qa-probes-readonly-coverage-report:C15 | PASS (U) snapshot-diff tests live in the unchanged `test_readonly.py` |
| qa-probes-readonly-coverage-report:C16 | PASS (U, R) the real-git test is in the unchanged file; `-m integration` selects it and it passes |
| qa-probes-readonly-coverage-report:C17 | PASS (R) exactly one `@pytest.mark.integration` (`test_readonly.py:471`); `-m integration` selects 1 of 573; `conftest.py` is unchanged and all 573 pass under its guard |
| qa-probes-readonly-coverage-report:C18 | PASS (A) the 25 cycle-0 mutation runs used tests in `test_readonly.py` (unchanged) and `test_probes_allowlist.py`, which grew by exactly one 24-line block at `:1362`; no test was weakened or removed |
| qa-probes-readonly-coverage-report:C19 | PASS (R, D) 573 passed, also in reverse file order; the two files now hold 243 + 24 = 267 tests instead of 266; ruff check and format clean |
| qa-probes-readonly-coverage-report:C20 | PASS (R) the ids in `test-probes-allowlist.txt` (232 unique stems, 243 passed) and `test-readonly.txt` (24) equal the collected ids; the F1 and F2 wording notes are unchanged |
| qa-report-cli-coverage-report:C1 | PASS (N, D) the `test_report.py` row cases map to tests that exist (48 tests now, 41 before); pointers moved |
| qa-report-cli-coverage-report:C2 | PASS (U) `test_cli_registration.py` is unchanged; 3 of 3 pass |
| qa-report-cli-coverage-report:C3 | PASS (N, D) the `test_cli_contract.py` row cases map to tests that exist (94 now, 90 before) |
| qa-report-cli-coverage-report:C4 | PASS (N) the `_publish` error-table tests exist; the file grew from 1409 to 1456 lines by exactly the two new blocks (24 + 23 lines), so the publication tests did not change |
| qa-report-cli-coverage-report:C5 | PASS (N, R) Run-id, binding, window-parser, exit-code and naming tests exist; the window parser tests are joined by `test_window_reaches_the_classification` |
| qa-report-cli-coverage-report:C6 | PASS (R) `GOLDEN_V1`, `test_golden_v1_keys_and_types_at_every_level` and the checker self-test are untouched and pass; the new JSON value test follows them (`:1018`) |
| qa-report-cli-coverage-report:C13 | PASS (A) the cycle-0 run of 11 mutants (1 killed, 10 survived) is a record of that run; the survivors tied to F-2 (M3, M19, M20, M23, M24) are now killed (RP1 to RP4, B-ps-branch), which is the intended change; nothing it relied on was weakened |
| qa-report-cli-coverage-report:C14 | PASS (R, D) `test-report.txt` 48 and `test-cli-contract.txt` 94 and `test-cli-registration.txt` 3 equal disk; ruff results reproduce; `phase10-validation.md` still shows 559 as a dated record (TST-F52) |
| qa-report-cli-coverage-report:C15 | PASS (R, D) gates reproduced now: 573 passed, ruff check clean, ruff format clean |
| qa-report-cli-coverage-report:C16 | PASS (A) the cycle-0 copy `/tmp/t226*` is absent; nothing contradicts that review's statement that it wrote only its report |
| qa-isolation-report:C1 | PASS (R, D) baseline: 573 passed, ruff check and format clean |
| qa-isolation-report:C2 | PASS (U, A) `conftest.py` is unchanged (04:04), its guard reads only the function's own `pytestmark`; the cycle-0 mutation proof is an artifact of an unchanged file; 573 tests pass under it |
| qa-isolation-report:C3 | PASS (R) one `@pytest.mark.integration` in `tests/sweep/` (`test_readonly.py:471`); `-m integration` selects 1 of 573 |
| qa-isolation-report:C4 | PASS (A, R) the cycle-0 audit-hook run is an artifact; the 14 new tests run under the live guard (it blocks `subprocess.run`, `Popen`, `os.system`), I read all of them and none starts a process; no new `integration` mark |
| qa-isolation-report:C5 | PASS (U) the static scan of `src/superclaude/cli/sweep/` is about modules whose sha256 equals the pre-fix value |
| qa-isolation-report:C6 | PASS (U) the guard's coverage limits (F1) are in the unchanged `conftest.py:40-42` |
| qa-isolation-report:C7 | PASS (R) the new tests that reach `Path.home()` (`env` and `sweep_root`) use the fixtures that move `HOME` and `XDG_STATE_HOME` into `tmp_path`; the new report and classify tests do not call it |
| qa-isolation-report:C8 | PASS (R) new tests write only under `tmp_path` (`os.utime` on a tmp contract, `env.sweeps`); after my two repository runs `tests/sweep/`, `src/superclaude/cli/sweep/` and `.dev/sweeps/` have 0 files newer than 05:49, and `.dev/sweeps/` still holds only the four 03:11 to 03:45 reports |
| qa-isolation-report:C9 | PASS (R) `read_orca_version` is stubbed where the new tests collect (`test_probes_allowlist.py` autouse fixture, `test_cli_contract.py` `env`); the new report and classify tests do not collect |
| qa-isolation-report:C10 | PASS (R) the one new patch (`probes._utcnow`) is a `monkeypatch`; reverse file order and a run with the file listed twice in one process both pass |
| qa-isolation-report:C11 | PASS (U) the one real-git test is in the unchanged `test_readonly.py` |
| qa-isolation-report:C12 | PASS (R) both new CLI tests read the result through `_payload` (exit 0, empty stderr), so a guard trip inside the command would fail them |
| qa-isolation-report:C13 | PASS (R, D) `-m integration` selecting exactly 1 reproduces (1 of 573); `phase10-validation.md:62` (559) is a dated record (TST-F52); `test-readonly.txt:66` unchanged; the `469` slip of `test-cli-registration.txt` is unchanged (TST-F45) |
| qa-assertion-strength-report:C1 | PASS (R, D) baseline now 573 passed (559 at cycle 0, which `phase10-validation.md:62` still records, TST-F52) |
| qa-assertion-strength-report:C2 | PASS (R) ruff check clean, ruff format check 15 files already formatted |
| qa-assertion-strength-report:C3 | PASS (A) the cycle-0 harness is an artifact; my own copy was proved live by a sanity mutation; no repository file changed |
| qa-assertion-strength-report:C4 | PASS (U) the `conftest.py` fakes and guard are unchanged |
| qa-assertion-strength-report:C7 | PASS (U) `test_readonly.py` is unchanged |
| qa-assertion-strength-report:C10 | PASS (U) `test_cli_registration.py` is unchanged |
| qa-assertion-strength-report:C11 | PASS (R, D) the maps agree with disk: 161 (`test-classify.txt`), 24, 3, and now 94, 48, 243 for the others; they sum to 573 |
| qa-assertion-strength-report:C12 | PASS (N) the DESIGN 11 files exist under `tests/sweep/`; the section 12 rows name tests that exist; no test was removed |
| qa-fixture-provenance-report:C1 | PASS (U, R) the folder holds 20 files: 19 `captured-*.json` and `SOURCES.md`, nothing else; no file is newer than 2026-11-11 22:37 |
| qa-fixture-provenance-report:C2 | PASS (U, R) no file was added or changed in `tests/sweep/fixtures/`; no test file mentions `synthetic` and no hand-made file exists |
| qa-fixture-provenance-report:C3 | PASS (U) `captured-worker-list.json` is unchanged |
| qa-fixture-provenance-report:C4 | PASS (U) `captured-worker-show-1..5.json` are unchanged |
| qa-fixture-provenance-report:C5 | PASS (U) the two task-list fixtures are unchanged |
| qa-fixture-provenance-report:C6 | PASS (U) the run-current and unknown-Run fixtures are unchanged |
| qa-fixture-provenance-report:C7 | PASS (U) `captured-worktree-current.json` is unchanged |
| qa-fixture-provenance-report:C8 | PASS (U) the ps and list fixtures are unchanged (the UNVERIFIABLE part, F6, is unchanged) |
| qa-fixture-provenance-report:C9 | PASS (U) the five tab-map fixtures are unchanged |
| qa-fixture-provenance-report:C10 | PASS (U) the fake-UUID numbering lives in unchanged files |
| qa-fixture-provenance-report:C11 | PASS (U, R) `grep -rn "coder\|/home/coder" tests/sweep/fixtures` finds nothing now |
| qa-fixture-provenance-report:C14 | PASS (U) `SOURCES.md` and the files it describes are unchanged |
| qa-fixture-provenance-report:C15 | PASS (R) hand-made data in the new tests is built inline (`obs`, `ttail`, `sweep_root`), not as a file under `fixtures/`; DESIGN 11 line 754 ties the `synthetic` marker to file names, so the rule is met as at cycle 0 (F7 note unchanged) |
| qa-determinism-report:C1 | PASS (R) the new tests use `ctx.now`, `env.now` or the fixed `NOW`; the TST-F5 test patches `probes._utcnow` to `NOW` |
| qa-determinism-report:C2 | PASS (R) grep of `tests/sweep/*.py` for `time.time(`, `datetime.now(`, `utcnow(`, `sleep(`, `threading`, `random.`, `uuid.`, `tempfile`, `time.monotonic`: 0 hits |
| qa-determinism-report:C5 | PASS (R, A) reverse file order 573 passed; each of the 14 new tests passes alone; the cycle-0 single-test runs concern tests that did not change |
| qa-determinism-report:C6 | PASS (R) the suite passed twice in a row in the repository (`573 passed` both times) and once with a file listed twice in one process; nothing under `tests/sweep/`, `src/superclaude/cli/sweep/` or `.dev/sweeps/` changed |
| qa-determinism-report:C7 | PASS (U, R) `test_cli_registration.py` is unchanged and passes in reverse file order |
| qa-determinism-report:C8 | PASS (R) `TZ` = Pacific/Kiritimati, America/Adak, Asia/Kolkata, UTC: 573 passed each |
| qa-determinism-report:C9 | PASS (R) `LC_ALL=C LANG=C PYTHONUTF8=0`: 573 passed |
| qa-determinism-report:C10 | PASS (R) `PYTHONHASHSEED` 0, 1, 2, 99: 573 passed each |
| qa-determinism-report:C11 | PASS (R) the new tests list no directory; the code that sorts its scans is unchanged (sha256) |
| qa-determinism-report:C12 | PASS (R) `read_orca_version` is stubbed where the new tests collect; wall clock shifted by -400 days, +3650 days, -8.6 s, +0.5 s: 573 each (control: 90 tests fail when `_utcnow` raises) |
| qa-determinism-report:C14 | PASS (R) the suite passes from a copy in `/tmp` (other folder, no `.git` above); the new tests call no `chdir` |
| qa-determinism-report:C15 | PASS (R) the new mtime test sets a whole even second; no new test depends on sub-second file time |
| qa-determinism-report:C19 | PASS (R) ruff check and ruff format check exit 0 now |
| qa-determinism-report:C20 | PASS (R) every new test runs under the live guard; none starts a process; `test_a_sweep_starts_no_process_and_records_only_allowlisted_argv` still passes |

Rows: 24 + 20 + 10 + 13 + 8 + 13 + 14 = 102. FAIL rows: 0.

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` section was in my prompt, so this ran standalone and nothing was skipped on rf-qa's word. The only things I did not re-run are the cycle-0 scratch artifacts (checks marked A) and checks about files the fix did not change (marked U); for both I confirmed by hash or mtime that nothing they relied on changed.

**(b) Independent semantic checks (at least one required, INV-019):**
- Discrimination of the six fixes: 25 mutations in a private copy, each failing the new test the fix log names (table above); one survivor, X2, shown to be an equivalent mutant by reading `classify.py:376-377`.
- Reach of the fixture comment in `test_fr010_exemptions_never_become_idle`: M5 fails 2 of the 5 cases, not all five, so the comment over-claims (TST-F46).
- Whether pinned values come from DESIGN or only from the code: `removable == "no"` and `unpushed is None` match DESIGN 2.2 line 72; the header lines and banner match DESIGN 7.5 lines 606-614 character for character; `null`, `failed result` and `settled` trace to the REPORT row at line 1248; the reason string `unpushed branch: no upstream` is code wording only (TST-F47).
- Determinism of the 14 new tests: reverse file order, 4 time zones, 4 hash seeds, a C locale, 4 wall-clock shifts with a control that proves the seam is reached, each test alone, odd temp folders (found TST-F51).
- Result maps against disk: ids of the four updated maps equal pytest's collected ids; counts 161, 94, 243, 48 equal the pytest blocks.
- Executor claims: `sha256sum -c` of the six modules (6 of 6) and of the protected list (67 of 68; the one difference is the plan file, changed after the log).

Answers to the four self-audit questions:

1. Claims independently verified: 6 findings (each by at least one mutation and a read of the test), 102 check ids (by the bases above), 25 mutations, about 30 perturbation runs, 4 gate commands, 4 map-versus-disk comparisons, and the pinned values of the new tests against DESIGN and the REPORT row.
2. Files read: the seven cycle-0 reports, the consolidated file, fix log and ledger; `test_cli_contract.py` (`:470-580`, `:990-1080`), `test_report.py` (`:1-70`, `:540-640`, `:1140-1270`), `test_probes_allowlist.py` (`:1335-1415`), `test_classify.py` (`:62-100`, `:520-600`, `:985-1095`); `classify.py` (`:52-88`, `:180-210`, `:296-396`, `:770-930`), `report.py` (`:150-200`), `probes.py` (`:755-760`, `:996-1001`, `:1344-1347`); DESIGN 7.4, 7.5, 11, 12; the four updated result maps, `phase10-validation.md`.
3. This is not a zero-issue result: seven MINOR notes, each with a location and a measured or read basis. The passes rest on mutations that fail and on counts that match, not on reading the fix log.
4. Web research: none, so no Tavily or fallback call was needed or made.

## Confidence and tool engagement

- **Confidence:** Verified: 108/108 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (108 = 102 check ids + 6 findings). Of the 108, 9 rest on the "nothing it relied on changed" evidence only (A) and 18 on unchanged-file evidence only (U); the rest were re-run or re-read now.
- **Tool engagement (approximate):** Read: 40 | Grep: 10 | Glob: 0 | Bash: 22 (gate commands, hash checks, id comparisons, three mutation and perturbation batch scripts that ran 25 mutations and about 30 runs, greps, cleanup) | Edit/Write: 12 on this report only.
- **Flag:** Read + Grep + Glob (about 50) is below the 108 items, which the protocol marks as suspect. The reason: most check ids are one kind of claim (a cited test still exists and passes, or a cited file is unchanged) and were settled by single batch calls (one grep script over all 276 test names and the seven reports; one script for 25 mutations; one for the perturbation runs), not one call per id. The mutation and perturbation outputs are in this report so the reader can judge them directly.
- **Not covered:** macOS, Python 3.10 or 3.12, pytest-xdist, click older than 8.2 (TST-F44, unchanged), git older than 2.28 (TST-F43, unchanged). I did not re-run the cycle-0 audit-hook run of the isolation lens against the 14 new tests; I read them and ran them under the live guard instead.

Verdict: PASS
Blocking count: 0


