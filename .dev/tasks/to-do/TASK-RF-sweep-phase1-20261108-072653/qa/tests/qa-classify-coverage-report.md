# QA Report - Classify coverage lens

**Task:** TASK-RF-sweep-phase1-20261108-072653
**Date:** 2026-11-12
**Phase:** tests gate, classify coverage lens (T224)
**fix_authorization:** false (report only)

**Scope read from disk now:** `tests/sweep/test_classify.py` (all 1851 lines, 13 chunks of at most 150), the `test_classify.py` row of DESIGN section 11 (`docs/designs/orchestrator-mode.md:760`) and section 12 (`:770-820`), the R3-B1 probes fixtures and the `collect` source-row tests in `tests/sweep/test_probes_allowlist.py` (`:1130-1268`, `:1790-1934`), `src/superclaude/cli/sweep/classify.py` (rules, joins, guard, `removable`, `classify_all` regions), `probes.py:740-870`, the SPEC rows FR-005 to FR-015 and SPEC lines 236, 254-259, 269, `test-classify.txt` (all 257 lines) and `phase10-validation.md` (all 89 lines).

**Method.** Each design case was matched to a test by name, then the test body was read for what it asserts (class, rule, exact note). Notes were compared byte for byte between the test constants (`test_classify.py:67-93`), `classify.py:54-85` and the DESIGN text. To test whether the assertions really pin the design, 11 mutations were applied to a private copy under `/tmp` (copy deleted afterwards; `ls /tmp | grep -c qa-t224` printed 0; `git status` shows no tracked file changed by this review). Test runs: `uv run pytest tests/sweep` gives 559 passed, `tests/sweep/test_classify.py` gives 159 passed, `ruff check` passes, `ruff format --check` reports 15 files already formatted.

## Case-to-test coverage (DESIGN 11 `test_classify.py` row, in the row's own order)

Legend: class = the test asserts the class (or the rule that fixes it); note = the test asserts the exact note string from DESIGN (`==` on the notes tuple, or `in` where DESIGN says the note is attached; F1 and F2 mark where `in` is weaker than DESIGN's wording). All tests are in `tests/sweep/test_classify.py`.

| # | Design case | Test | Class | Note | Gap |
|---|---|---|---|---|---|
| 1 | One case per rule 1 to 9, reaching every name in `CLASSES` | `test_rule_case_per_rule_1_to_9` (`:360-364`, 9 params), `test_every_class_name_is_reached` (`:367`) | yes (rule, class, waiting kind) | n/a | none |
| 2 | Rule-name order pin | `test_rules_order_pin` (`:374`) | n/a | n/a | none |
| 3 | 5 h old row, windows under and at 6 h | `test_5h_old_row_is_idle_only_when_window_is_under_5h` (`:455-464`; windows 4, 5, 6) | rule | n/a | none (the 5 h window pins the `<` boundary) |
| 4 | Record timestamp older than mtime | `:467-477`, `:480` | IDLE | evidence text named | none |
| 5 | Four FR-008 inputs; late-heartbeat live row never `stalled (proved)` | `:510-539` (4 params incl. `late-heartbeat`) | UNKNOWN, rule `fallback`, `!= STALLED` | DESIGN requires none | none |
| 6 | Two FR-009 cases with the exact note | `:550-558`, `:561-565` | FINISHED; UNKNOWN+fallback | `cls.notes == (N_EXITED,)` in both; MU7 (drop the note) fails case 1 | none |
| 7 | Rule 1 decline notes (M6) | `:578`, `:589-602`, `:605-616` | not WAITING; UNKNOWN | `N_ASK in` (two tests), `notes == (N_NOT_OBSERVED,)` | none |
| 8 | Rule 5 four-condition case | `:431-447` | WORKING and four negatives | n/a | none |
| 9 | Future timestamp: unknown age, never idle | `:487`, `:496`, `:378-385` (`notes == (N_FUTURE,)`) | yes | yes | none |
| 10 | FR-010 control (8 h old unmapped T: True, Historical) | `:848-859` | IDLE, `person_started` True | `notes == (N_ORIGIN_NOT_PROVED,)`, `summary["historical"] == 1` | none |
| 11 | SPEC case 1, outage | `:862-868` via `assert_origin_unknown` (`:836-845`) | UNKNOWN, None, visible, not Historical | `notes == (N_O_UNAVAILABLE,)` exactly (MU9, which also counts the outage as `call_failed`, fails it) | none |
| 12 | SPEC case 2, full page | `:871-880` (100 rows, `truncated` True, `total_is_lower_bound` True) | same | `notes == (N_O_TRUNCATED,)` | none |
| 13 | SPEC case 3, `call_failed` | `:883-890` | same | `notes == (N_O_CALL_FAILED,)` | none |
| 14 | Not-SPEC: Run not confirmed | `:893-903` | same | `notes == (N_O_RUN,)`; the control-result variant asserts only True and IDLE | F2 |
| 15 | Not-SPEC: Run never reached (budget) | `:906-913` | same | `notes == (N_O_CALL_FAILED,)` | none |
| 16 | Not-SPEC: tab map unreadable | `:916-925` | same | `notes == (N_O_TABS,)`; the control-result variant asserts only True and IDLE | F2, F6 |
| 17 | Note-order fixture, parts (a) and (b) | `:928-959` | UNKNOWN, None | (a) `== (N_O_UNAVAILABLE, N_SP16, N_JOIN_NOT_OBSERVABLE)`; (b) four `origin unknown:` notes in order, no join-guard note | none |
| 18 | Five exemptions | `:967-1008` (5 params), `:1011-1020` | `!= IDLE`; `historical == 0` for the open-Task case | n/a | F4 |
| 19 | SP-29 two-Run fixture | `:1023-1050` | UNKNOWN, None, `historical == 0` | `N_NOT_SCOPED in` | none |
| 20 | `person_started` None while `session_join` is None | `:1053-1066` | None, `historical == 0` | `N_JOIN_NOT_OBSERVABLE in` | none |
| 21 | D9: path-B join is False, shown as `orca:<dispatch>` | `:1069-1080` | False, only row `orca:D1` | `N_JOINED in` | none |
| 22 | D9: entry joining no scoped row is None even when the guard holds | `:1083-1092` | UNKNOWN, None, `historical == 0` | `notes == (N_NOT_SCOPED,)` | none |
| 23 | D9: path A no-entry True carries `origin not proved`; unscoped-Run worker never True without it | `:1095-1110` | True rows are exactly T and W | note on each True row | F7 |
| 24 | D9: path-B unmatched `session_join` makes every unjoined transcript None with the SP-16 literal | `:1113-1132` | None | `N_SP16 in` both, `N_EARLIER in` T, `N_NOT_SCOPED in` V | none |
| 25 | R2-B1: `/clear`, resume, person rerun | `:1192-1210` (3 params) | D1 UNKNOWN+fallback, early None/UNKNOWN, late None, no True row, `historical == 0` | `N_MOVED in` D1 and late, `N_EARLIER in` early | none |
| 26 | R2-B1: later session inside the window; no observable start | `:1213-1221`, `:1224-1228` | False; UNKNOWN | `N_JOINED in`, `notes == (N_EARLIER,)`; `N_WINDOW in` | none |
| 27 | Guard cases 1 and 2 together: SP-16 first, then join not observable | `:1135-1144` | n/a | `notes == (N_SP16, N_JOIN_NOT_OBSERVABLE)` | none |
| 28 | SPEC line 236 fixture | `:1147-1156` | UNKNOWN, None | `notes == (N_SP16,)` (the row has a `session_join`, so guard case 1 does not hold; consistent with DESIGN line 1029, m5) | none |
| 29 | SP-07 `guard refused:` on a later line; `FINAL:` inside text | `:676-679`, `:1666-1676` | `!= FINISHED`; `unfinished` | n/a | none (MU6 fails `:676`) |
| 30 | Truncated JSONL; unreadable contract; cut last line only; transcript open raises `OSError` | `:725-733`, `:775-792`, `:736-750`, `:753-772` | UNKNOWN+fallback (PERSON_ACTIVE for the cut-last-line case) | `N_TRANSCRIPT in`, `N_CONTRACT in` | none |
| 31 | Non-null `parent`: WC-13 note, class kept | `:700-707` | class equal to the no-parent row | `N_WC13 in`, absent without parent | none |
| 32 | FR-012 over all fixtures | `run()` (`:237-248`), `:1496-1516` | n/a | n/a | none |
| 33 | FR-013 one fixture per condition, condition named | `:1519-1565` (10 params), `:1568-1604` | `value == "no"` | reason substring per condition | none |
| 34 | FR-014 one fixture per state incl. `conflict` | `:1642-1690` (`set(PACKAGE_FIXTURES) == set(PACKAGE_STATES)`) | state | n/a | none |
| 35 | FR-015 three fixtures | `:1706-1744` (one printed line `- Active package pkg-07 is in several worktrees: /w1, /w2, /w3`) | n/a | exact line | F3(e) |
| 36 | FR-005 person-session fixture, active session (M9) | `:1607-1629` | PERSON_ACTIVE, 4 rows, 2 worktrees | n/a | none |
| 37 | AST import test | `:1790-1836` | n/a | n/a | F5 (result map miscount only) |

### R3-B1 fixtures (DESIGN 11 and 12)

| Design fixture | Test | Asserts |
|---|---|---|
| `test_path_b_window_open_row_joins` | `test_classify.py:1236-1244` | only row `orca:D1`, `person_started` False, `transcript_path == s.path`, `N_JOINED in` |
| `test_path_b_window_inclusive_bounds` | `:1247-1265` (3 params 10:00:00.700, 11:00:00.400, 11:00:01) | first two False and no `transcript:S` row; third D1 UNKNOWN+fallback with `N_MOVED`, S None with `N_MOVED` |
| `test_path_b_terminal_row_without_end_has_no_window` | `:1268-1274` | D1 UNKNOWN with `N_WINDOW`, S None with `N_WINDOW` |
| `test_path_b_row_without_start_has_no_window` | `:1277-1285` | same, S never True |
| `test_path_b_incomplete_tail_has_no_session_start` | `:1288-1295` | D1 UNKNOWN with `N_TAIL`, S None with `N_TAIL` |
| `test_read_transcript_tail_sets_first_and_last_record_ts` | `test_probes_allowlist.py:1832-1848` | first 07:00:01 UTC, last 07:00:09 UTC, both aware, `tail_complete` True |
| `test_read_transcript_tail_first_record_ts_is_minimum` | `:1851-1862` | first is 07:00:01 for out-of-order records (helper `conftest.py:271-300` keeps file order) |
| `test_read_transcript_tail_first_record_ts_over_256k` | `:1865-1880` | first 08:00:00, not 07:00:00; `tail_complete` False |
| `test_worker_show_dispatch_times_sqlite_form` | `:1883-1898` | started 07:00:00 UTC aware, ended None, status `dispatched` |
| `test_worker_show_dispatch_times_iso_z_form` | `:1901-1916` | both aware UTC, fractional seconds kept |
| `test_worker_show_dispatch_times_missing_or_bad` | `:1919-1934` (2 params) | both None, nothing raised |

### R3-B2 fixtures (all 10 present, all under `path_b`)

| Design fixture | Test (`test_classify.py`) | Class / rule | Note |
|---|---|---|---|
| `test_path_b_pane_reused_joins_later_row_only` | `:1347-1348` via `_assert_reused_pane` (`:1333-1344`) | D2 False and no `transcript:S` row; D1 UNKNOWN+fallback, `rule != "finished"`, rule-6 evidence `Orca outcome succeeded` kept | `N_JOINED in` D2, `N_MOVED not in` D2, `N_MOVED` on D1 |
| `test_path_b_two_windows_hold_session_is_conflict` | `:1363-1372` | D1 and D2 UNKNOWN+fallback, S None, no `orca:` row carries S | `N_SEVERAL` on all three; `assert_no_sp16` |
| `test_path_b_shared_boundary_second_is_conflict` | `:1375-1381` | both rows UNKNOWN, S None | `N_SEVERAL` on both rows |
| `test_path_b_no_matching_window_holds` | `:1384-1393` | both rows UNKNOWN, S None | `N_MOVED` on all; `assert_no_sp16` |
| `test_path_b_multi_row_result_ignores_row_order` | `:1403-1411` (reused-pane, two-windows) | snapshot (row id, class, notes) equal in both orders | equal notes |
| `test_path_b_entry_failing_window_note_order` | `:1414-1420` | n/a | `N_MOVED in`, `N_NOT_SCOPED not in`, `assert_no_sp16` (F1) |
| `test_path_b_rows_share_terminal_handle` | `:1351-1353` | same helper with `join=HANDLE` | as the first fixture |
| `test_path_b_two_rows_incomplete_tail` | `:1423-1440` (both orders, plus the `dispatch_started` None variant) | D1 and D2 UNKNOWN, S None | `N_TAIL`; variant: D1 `N_TAIL`, D2 `N_WINDOW`, S `N_TAIL` |
| `test_path_b_live_session_spans_two_dispatches` | `:1443-1452` | D1 False and no `transcript:S` row; D2 UNKNOWN | `N_JOINED` on D1, `N_BEFORE` on D2, `N_MOVED not in` D2 |
| `test_path_b_duplicate_dispatch_rows_count_once` | `:1455-1468` | exactly one `orca:` row, UNKNOWN, no join, S None | `N_DUPLICATE` and `N_WINDOW` on the row, `N_WINDOW` on S, `N_SEVERAL` absent, `assert_no_sp16` |

I printed the actual notes of seven of these fixtures from a private copy: each row and S carries exactly one note (two on the duplicate row), so the `in` assertions hold today with the exact set. The standalone SP-16 line in the report is derived from row notes (`report.py:328-329`), so `assert_no_sp16` is a sound stand-in for the design clause "Could not determine does not print the SP-16 line".

### Cases with no test

None. Every case in the DESIGN 11 `test_classify.py` row, every R3-B1 fixture (5 classify, 6 probes), every R3-B2 fixture (10) and every R3-B3 fixture (3 SPEC fixtures, 3 non-SPEC fixtures, the note-order fixture, plus the control) has a test that reaches the class and the note named by DESIGN.

## Mutation experiments (private copy under /tmp, deleted afterwards)

Each mutation changes `classify.py` in the copy only and runs `tests/sweep/test_classify.py` from the copy with `PYTHONPATH` pointing at it (the sanity mutation proves the copy is the code under test).

| Id | Mutation | Result | Reading |
|---|---|---|---|
| sanity | `pane moved to a later session` text changed | killed (`test_r2_b1_pane_reuse_outside_window_does_not_join[clear]`) | copy is in use |
| MU1 | append `NOTE_EARLIER_PANE` to every transcript left unjoined by the tail, window or several-rows rule (`classify.py:752-754`) | survived, 159 passed | F1 |
| MU2 | open window upper bound `collected_start` replaced by an unbounded value (`classify.py:548-549`) | survived | F3(a) |
| MU3 | rule 6 evidence says `accepted` | killed (`test_rule6_finished_never_says_admitted_or_accepted`) | pinned |
| MU4 | `mark_shared_packages` threshold 2 changed to 3 (`classify.py:433`) | survived | F3(e) |
| MU5 | append the SP-16 note to a transcript left unjoined by the window rules | killed (`test_path_b_two_windows_hold_session_is_conflict`) | pinned |
| MU6 | `guard refused:` accepted on any line | killed (`:676`) | pinned |
| MU7 | rule 2 decline no longer attaches `Orca: exited; fenced evidence not readable` | killed (`:550`) | pinned |
| MU8 | `Run not confirmed` ignores whether a row has that Run (`classify.py:699-704`) | survived | F3(d) |
| MU9 | outage also counted as `call_failed` (`classify.py:690`) | killed (`test_fr010_outage...`) | pinned |
| MU10 | incomplete tail with no observable window gets the tail note instead of the window note (`classify.py:619`) | survived | F3(c) |
| MU11 | status None accepted as an open window (`classify.py:548`) | survived | F3(b) |

## Findings

All findings are MINOR: none is a missing case, and none of the surviving mutations is on a case DESIGN 11 or 12 lists. MINOR findings never fail the gate.

| id | severity | evidence | what is wrong | smallest fix |
|---|---|---|---|---|
| F1 | MINOR | `test_classify.py:1414-1420`; `classify.py:752-754`; MU1 | DESIGN 11 says S's note is `pane moved to a later session`, not the `Orca pane session` note. The test asserts `N_MOVED in notes` and `N_NOT_SCOPED not in notes` only, and its name says "note_order" while no order is asserted. MU1 (a transcript that has a tab-map entry also receives `earlier pane session not joinable`, which DESIGN 7.2 reserves for transcripts with no entry) passes 159/159. The same `in` form is used for S in the inclusive-bounds, no-matching-window, terminal-row, row-without-start, incomplete-tail and duplicate fixtures. | Replace with `assert notes == (N_MOVED,)` (the observed value) and do the same for S in the other R3-B1 and R3-B2 fixtures that name a single note. |
| F2 | MINOR | `test_classify.py:899-903`, `:923-925` | DESIGN 11 says the same input with `task-list BAD` not unscanned, or an empty readable tab-map folder, "gives the control result" (True, `origin not proved` note, Historical). The two sub-assertions check only `person_started is True` and `class_name == IDLE`, not the note or `summary["historical"] == 1`. | Call one `assert_control(result)` helper (the assertions of `:852-856`) in all three places. |
| F3 | MINOR | `classify.py:548-549`, `:619`, `:699-704`, `:433`; MU2, MU4, MU8, MU10, MU11 | DESIGN 7.2 and SPEC FR-015 rules with no listed fixture survive a mutation: (a) an open Dispatch window ends at `collected_start` (every fixture has `collected_start == now` and S inside the window); (b) a row with a start, no end and status None has no window; (c) an incomplete tail with no observable window gives S the `Dispatch time window not observable` note; (d) `Run not confirmed` needs that no row has the Run; (e) a package is shared from 2 worktrees, not 3 (fixtures use 1 and 3). These are not in DESIGN 11's list, so nothing required is missing. | Optional: one fixture each (S first record after `collected_start`; status None; incomplete tail with no start; a Run with rows and a failed `task-list`; 2 worktrees). |
| F4 | MINOR | `test_classify.py:1007-1008`; `classify.py:964` | The five exemption cases assert `class_name != IDLE` through `classify()` and not `summary["historical"] == 0` through `classify_all`; only the open-Task case runs `classify_all` (`:1011-1020`). `historical` is the count of the IDLE class, so the check is equivalent today. | Optional: assert the exact class per exemption (UNKNOWN, UNKNOWN, WAITING-or-fallback as observed). |
| F5 | MINOR | `test-classify.txt:254` and `:151-165`; `test_classify.py:1793-1807` | The result map says the import scanner is shown to catch "16 forms"; the parametrization and the map's own pytest list hold 15 (`banned0` to `banned14`). | Correct the count to 15. |
| F6 | MINOR | `test_classify.py:919` (also DESIGN 11, the `tab map not readable` fixture text); `probes.py:862`; `test_probes_allowlist.py:1265` | The classify fixture builds the source row with `tab map not readable`; the real collector emits `tab map folder not readable`. `classify.py:710` reads only `unscanned is not None`, so behaviour is the same. | Optional: use `tab map folder not readable` in the fixture and in the DESIGN text. |
| F7 | MINOR | `test_classify.py:1095-1110` | DESIGN 11 says the unscoped-Run worker is "placed in the same worktree"; the fixture has no worktree link (`SessionRow` carries none), so only the no-entry, no-join shape is tested. | Optional: add a comment that the same-worktree clause is not modelled. |

## Checks

| Check | Subject | Result |
|---|---|---|
| C1 | Suite green: `uv run pytest tests/sweep` 559 passed, `test_classify.py` 159 passed, `ruff check`, `ruff format --check` | PASS |
| C2 | Rules 1 to 9, `CLASSES`, rule-name order pin (rows 1 and 2) | PASS |
| C3 | Window, `last_activity` source, future timestamp (rows 3, 4, 9) | PASS |
| C4 | FR-008 four inputs and the late-heartbeat case (row 5) | PASS |
| C5 | FR-009 two cases with the exact note (row 6) | PASS |
| C6 | Rule 1 decline notes (M6) and rule 5 (rows 7, 8) | PASS |
| C7 | FR-010 control (row 10) | PASS |
| C8 | R3-B3: the three SPEC fixtures assert class and exact note (rows 11 to 13) | PASS |
| C9 | R3-B3: the three non-SPEC fixtures and the note-order fixture (rows 14 to 17) | PASS (F2, F6 minor) |
| C10 | Exemptions and SP-29 (rows 18, 19) | PASS (F4 minor) |
| C11 | `person_started` None, D9 join fixtures, guard cases, SPEC line 236 (rows 20 to 24, 27, 28) | PASS (F7 minor) |
| C12 | R2-B1 pane-reuse fixtures (rows 25, 26) | PASS |
| C13 | R3-B1 window fixtures in `test_classify.py` (5 of 5 present) | PASS |
| C14 | R3-B1 reader and parser fixtures in `test_probes_allowlist.py` (6 of 6 present) | PASS |
| C15 | R3-B2 several-rows fixtures (10 of 10 present) | PASS |
| C16 | SP-07, `FINAL:`, unreadable inputs, WC-13, rule 6 wording (rows 29 to 31) | PASS |
| C17 | FR-012 to FR-015 and FR-005 (rows 32 to 36) | PASS (F3(e) minor) |
| C18 | AST import tests and B5 (row 37) | PASS (F5 minor) |
| C19 | `collect` source-row and `truncated` tests named in DESIGN 12 (`test_probes_allowlist.py:1177-1268`) | PASS |
| C20 | Note literals in the tests equal `classify.py:54-85` and DESIGN text (checked one by one) | PASS |
| C21 | Notes are asserted exactly where DESIGN says "exactly" (mutation evidence, MU1 to MU11) | PASS (F1, F3 minor) |
| C22 | Cases with no test (none found) | PASS |
| C23 | Result map `test-classify.txt` matches the tests | PASS (F5 minor) |
| C24 | Read-only method: only the report written; private copies deleted | PASS |

Self-audit: 24 checks, 11 mutation runs, 7 minor findings and 0 blocking. A review that finds nothing blocking after 11 mutations is plausible here because every listed case is covered by a named test; the survivors are all outside the DESIGN 11 list or are `in`-versus-`==` strength points.

Verdict: PASS
Blocking count: 0
