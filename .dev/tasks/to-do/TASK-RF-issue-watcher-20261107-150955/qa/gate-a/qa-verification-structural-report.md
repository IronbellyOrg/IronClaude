# QA Report - Gate A structural verification (fix cycle 1)

**Topic:** issue-watch implementation, Gate A (Phases 2 and 3)
**Date:** 2026-11-07
**Phase:** fix-cycle (structural verification, Step 3.G10)
**Fix cycle:** 1
**Inputs:** `qa/gate-a/qa-consolidated-findings.md` (A-1 to A-18 blocking), `qa/gate-a/qa-fix-report.md`

---

## Overall Verdict: PASS

All 18 blocking findings are FIXED in the repository files. No new blocking structural issue was found. Minor findings (A-19 to A-72) were not rechecked.

## Gate commands re-run by this agent

| Command | Result |
|---|---|
| `uv run pytest tests/issue_watch/ -q` | 684 passed in 1.38 s |
| `uvx --offline ruff@0.15.20 check src/superclaude/cli/issue_watch tests/issue_watch` | All checks passed! |
| `uvx --offline ruff@0.15.20 format --check src/superclaude/cli/issue_watch tests/issue_watch` | 11 files already formatted |

## Per-finding verification

| id | Result | Evidence |
|---|---|---|
| A-1 | FIXED | `tests/issue_watch/test_github.py:1379,1393,1438,1460,1478` build each reply from `load("gh_issue_list.json")`, `rest_events_page.json`, `rest_comments_marker.json`, `graphql_edits.json`, `graphql_project_items.json` and assert exact parsed values (events result also run through `approval_of`). `test_every_assumed_shape_fixture_is_read_by_a_test__df32` at line 585 added. |
| A-2 | FIXED | `src/superclaude/cli/issue_watch/github.py:768-769` now reads `[UNVERIFIED] reply shape (design 837, FU-1): treated as None when the value is null or has no name; any other non-object value is malformed.` The false claim is gone. |
| A-3 | FIXED | New fixtures exist: `gh_api_user_include_429.json`, `gh_stderr_http_502.json`, `gh_stderr_scope_read_project.json` (14 files in `_assumed_shape/`; count test at `test_github.py:578` expects 14). They are read at `test_github.py:421, 453, 1492, 1513, 1526, 2024`. `[UNVERIFIED, assumed shape]` tags with design rows at lines 94, 458, 618, 636, 941, 1241, 1572, 1601, 1636. |
| A-4 | FIXED | `predicates.py:24` `_UTC_SHAPE` (ASCII `[0-9]` fields, trailing `Z`), `predicates.py:37` `fullmatch` before `strptime`. Mutant that removes the shape guard is killed. |
| A-5 | FIXED | `runner.py:96-97` `encoding="utf-8", errors="replace"`; `runner.py:112` `except (OSError, ValueError)` gives `spawn_error` by class name; `runner.py:82-87` empty or non-list argv raises `TypeError`. Mutant dropping `errors="replace"` is killed. Docstrings (lines 25, 75-80) match the code. |
| A-6 | FIXED | `github.py:739-746` `_edited_at` does `_check("lastEditedAt" in d)`; used by `_edit_issue` (line 750) and `_comment_edit` (line 760); explicit null still means never edited. Mutant removing the key check is killed. |
| A-7 | FIXED | `audit.py:191-247` `_RULES` plus `_check_value`: `ts` and `approved_at` real UTC time, `cycle_id` 32 lower-case hex, `state` enum equal to design 422, `host`, `login`, `issue` 1..999999999, ids above 0, `exit` 0..255, counts at least 0. `stderr_fallback` (lines 389-390) checks `exit`, `ts`, `host`. Docstring (lines 4-6) now true. State-enum mutant is killed. |
| A-8 | FIXED | `github.py:3-6` docstring names the five caller values; `_CURSOR_RE` (127), `_cursor_args` (141-147), `_trigger_arg` (150-165, no comma, no control character, no leading dash, at most 50), `_login_arg` (168-172), and the hostile `endCursor` guard at `github.py:698-699`. `argv_discover` (191, 193) applies both checks. Cursor-guard mutant is killed. |
| A-9 | FIXED | `github.reread` tests at `test_github.py:1654-1846` (success, empty lists, reserved slots and 36th refusal, `timeout_for` None, other number, bool number, malformed fields, missing keys, non-object, transient versus failed split). Mutants "drop `number == n`" and "swap the two reasons" are killed. |
| A-10 | FIXED | `SHARED_FAILURES` table at `test_github.py:1510`, run against `user` and `discover`, with `retry_after_s` cases. |
| A-11 | FIXED | `test_rest_failed_first_page_is_unreadable__df02_fr005_fr009` (`test_github.py:1856`) and `test_rest_failed_page_2_discards_page_1__df02_fr005_fr009` (`test_github.py:1871`) run both REST reads (`events`, `marker_comments`) against the `REST_FAILURES` table and assert value None, the `*_unreadable` reason, the kind, and the call count. |
| A-12 | FIXED | `_errors_kind` (`github.py:631-638`) now covered for `RATE_LIMITED`, scope precedence and the odd item shapes. Mutant that disables the `rate_types` branch is killed. |
| A-13 | FIXED | `predicates.py:243` filter `e.event == "renamed"`. Mutant removing the filter is killed. |
| A-14 | FIXED | `predicates.py:204-208` `type(approval.actor_id) is not int` and the `actor_login is None` clause. Mutants "`is None` instead of `is not int`" and "`<=` becomes `<` at store creation" are both killed. |
| A-15 | FIXED | `audit.py:147` `_fsync_dir(self.state_dir)` after rotation. Mutant replacing it with `pass` is killed. |
| A-16 | FIXED | `test_github.py:49-76` writes `EDITS_QUERY` and `PROJECT_ITEMS_QUERY` out literally; `test_graphql_constants_equal_the_literal_drafts__df14` at line 273. Mutant `first: 100` to `first: 50` is killed. |
| A-17 | FIXED | `conftest.py:76,85` `FakeRunner.timeouts` records each timeout; tests at `test_github.py:1979` and nearby check the value reaches `runner.run`. Mutant `runner.run(argv, 30.0)` at `github.py:576` is killed. |
| A-18 | FIXED | `github.py:296` CRLF replace; tests at `test_github.py:2015, 2023, 2036` use CRLF copies of the G1 fixtures. Mutant removing the replace is killed. |

Mutation method: a private copy of `src/superclaude/cli/issue_watch` and `tests/issue_watch` under a temporary directory (removed afterwards), baseline 684 passed in the copy, then 15 single-line mutants run with `pytest -x`. Result: 15 killed, 0 survived, 0 pattern-missing. The repository files were not touched.

## New blocking structural issues

None.

| Check | Result | Evidence |
|---|---|---|
| Imports against design 233-242 | OK | `runner.py` imports `subprocess, time, dataclasses, typing`; `predicates.py` adds `re` (stdlib); `audit.py` imports stdlib only; `github.py` imports `.predicates` and `.runner` only (Grep of `^(import\|from)` over the package). No `superclaude.*` import and no third-party import in any module. |
| Python 3.10 compatibility | OK on reading and AST | All 11 `.py` files parse with `ast.parse(..., feature_version=(3, 10))`. Grep for `datetime.UTC`, `tomllib`, `StrEnum`, `Self`, `except*`, `ExceptionGroup`, `fromisoformat` code use, `itertools.batched` found no use (only docstring words). `from __future__ import annotations` present in all four modules. A real 3.10 run is not possible here (`uv python find 3.10` found none), already noted as A-34. |
| File hygiene | OK | No trailing whitespace, no tabs, final newline on every `.py` and `.json`; `__pycache__` is gitignored (`.gitignore:2`); tests write only under `tmp_path`; only the two package trees plus task artifacts changed. |
| Test and lint gates | OK | Commands in the table above. |

## Notes (not blocking)

- `test_every_assumed_shape_fixture_is_read_by_a_test__df32` checks that the quoted file name appears in the test source; a name in a docstring would also satisfy it. The five new read tests are what actually pin the shapes.
- `argv_discover` and `discover` now raise `ValueError` for an unsafe trigger or login. This is documented in the docstring and in the fix report, and the cycle (Phase 6) must validate both first.

## Summary

- Checks passed: 24 / 24 (18 finding checks, 6 structural checks)
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)

**Confidence:** Verified: 24/24 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
(The real Python 3.10 interpreter run is outside the 24 checks; it is carried as minor note A-34.)

**Tool engagement:** Read: 14 | Grep: 11 | Glob: 0 | Bash: 5

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| none | - | - | No blocking issue open | - |

## QA Complete
