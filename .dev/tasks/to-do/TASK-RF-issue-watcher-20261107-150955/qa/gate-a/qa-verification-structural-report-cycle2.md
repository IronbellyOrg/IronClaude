# QA Report - Gate A structural verification (fix cycle 2)

**Topic:** issue-watch implementation, Gate A (Phases 2 and 3)
**Date:** 2026-11-07
**Phase:** fix-cycle (structural verification, Step 3.G15)
**Fix cycle:** 2
**Agent:** rf-qa, `fix_authorization: false` (no file other than this report was written)
**Inputs:** `qa/gate-a/qa-consolidated-findings-cycle2.md` (1 blocking: A-7), `qa/gate-a/qa-fix-report-cycle2.md`, cycle-1 reports `qa-verification-structural-report.md` (PASS) and `qa-verification-content-report.md` (FAIL, 17 of 18 fixed)

---

## Overall Verdict: PASS

The one cycle-2 blocking finding (A-7) is FIXED in the repository files. No cycle-1 FIXED or PASS item regressed. No new blocking structural issue was found. Minor findings were not rechecked.

## Gate commands re-run by this agent

| Command | Result |
|---|---|
| `uv run pytest tests/issue_watch/ -v` | 686 passed in 1.42 s (cycle 1: 684; +2 are the two new A-7 tests) |
| `uvx --offline ruff@0.15.20 check src/superclaude/cli/issue_watch tests/issue_watch` | All checks passed! |
| `uvx --offline ruff@0.15.20 format --check src/superclaude/cli/issue_watch tests/issue_watch` | 11 files already formatted |

## Per-finding verification

| id | Result | Evidence |
|---|---|---|
| A-7 | FIXED | `audit.py:4-10` module docstring now says each value must match a closed shape, "The one exception is ``host`` and ``login``: they take any printable token of bounded length (``login`` without whitespace)", and "No issue title, body, label or stderr text has a key or a typed slot on a line." The false sentence "free text cannot be written into a line through any key" is gone (Grep for `free text cannot` in `audit.py` matches only the comment text "they do not filter free text", not the claim). Comment above `_RULES` (`audit.py:218-222`) says the `host` and `login` rules "only bound length and printability (login also bars whitespace)... they do not filter free text" and "Every other key is closed". Checked the "every other key is closed" claim against code: `kind` and `reason` are checked in `line()` (`audit.py:261-278`), `note` must be a `REASON_TABLE` entry of kind `note` (`audit.py:276-278`), `state`, `cycle_id`, `ts`, `approved_at` have patterns or enums in `_RULES` (`audit.py:223-237`), the rest are int or bool. The comment's reference to the login regex at design line 348 matches the design table row 5 ("login regex"). `_RULES` unchanged in behaviour. |
| A-7 new test 1 | PASS | `test_audit.py:444-456` `test_host_and_login_take_any_printable_bounded_token__...` accepts a sentence, a 255-character host, a comma-bearing login, a 100-character login, and asserts the docstring wording. Mutants run in a private temp copy: restore the old docstring claim -> this test fails; host limit 255 -> 10 -> this test fails. |
| A-7 new test 2 | PASS | `test_audit.py:459-463` `test_no_free_text_key_exists_on_any_line_kind__...` takes the union of `_KEYS` and asserts none of `FORBIDDEN_KEYS` (`test_audit.py:164`: rate_remaining, title, body, label, label_name, stderr) is in it and that all keys are in `_TYPES`. Mutant adding a `title` key to the warning line kind and `_TYPES` -> the run stops at `test_line_rejects_forbidden_keys__...[title]` (the older forbidden-key test), so this new test is not the first to catch it, but the key set is pinned twice. |
| A-7 old rows | PASS | The 36 rejected-value rows and 22 accepted rows (`test_audit.py:371-441`) are intact; mutant `state` rule -> `True` fails `...outside_the_key_shape[state-Fix the login bug in prod]`. |

Mutation method: a private copy of the package and `test_audit.py` under a mktemp directory, removed on exit, run with `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, baseline 178 passed in `test_audit.py`, 4 single-line mutants, 4 killed, 0 survived. The repository files were not touched (checked: no file in the two trees has an mtime after 21:40).

## Regression check (cycle-1 FIXED and PASS items)

Only two files changed after the cycle-1 verification reports were written (21:37): `src/superclaude/cli/issue_watch/audit.py` and `tests/issue_watch/test_audit.py` (`find -newermt '2026-11-07 21:37:30'`). `github.py`, `predicates.py`, `runner.py`, `conftest.py`, `test_github.py`, `test_predicates.py`, `test_runner.py` and the fixtures have mtimes 21:22 to 21:33, before the cycle-1 reports, so the cycle-1 verdicts for A-1 to A-6 and A-8 to A-18 hold for those files. The full suite passing (686) re-runs every test that pins them. Markers re-checked in the current files:

| Cycle-1 item | Still fixed | Evidence |
|---|---|---|
| A-4 | yes | `predicates.py:24` `_UTC_SHAPE`, `predicates.py:37` `fullmatch` |
| A-5 | yes | `runner.py:97` `errors="replace"`, `runner.py:112` `except (OSError, ValueError)` |
| A-6 | yes | `github.py:745` `_check("lastEditedAt" in d)` |
| A-8 | yes | `github.py:137` `_valid_cursor`, `150` `_trigger_arg`, `168` `_login_arg`, `698` cursor guard |
| A-13 | yes | `predicates.py:243` `e.event == "renamed"` |
| A-14 | yes | `predicates.py:207` `type(approval.actor_id) is not int` |
| A-15 | yes | `audit.py:150` `_fsync_dir(self.state_dir)` (the A-15 test passes in the 686) |
| A-1, A-2, A-3, A-9 to A-12, A-16 to A-18 | yes | Files unchanged since the cycle-1 PASS; their tests are part of the 686 passing |
| No assertion weakened by the cycle-2 fix | yes | 684 -> 686 passed; the fix report names two added tests and no deletion; the A-7 accepted and rejected row lists are intact (see above). The tree is untracked, so no line-by-line diff was possible (stated limit). |

No regression found.

## New blocking structural issues

None.

| Check | Result | Evidence |
|---|---|---|
| Imports against design 233-242 | OK | Grep of `^(import\|from)` over the package: `audit.py` stdlib only (collections.abc, pathlib, typing, datetime, json, os, re, socket, sys); `github.py` imports `.predicates` and `.runner` only plus stdlib; `predicates.py` and `runner.py` stdlib only. No `superclaude.*` import and no third-party import. Matches the design table rows `runner`, `predicates`, `audit`, `github`. |
| Python 3.10 compatibility | OK on AST and grep | All `.py` files in both trees parse with `ast.parse(..., feature_version=(3, 10))`; Grep for `datetime.UTC`, `tomllib`, `StrEnum`, `Self`, `except*`, `ExceptionGroup`, `batched` found no use. `audit.py` uses `datetime.timezone.utc`. A real 3.10 interpreter run is not possible here (carried as minor note A-34). |
| File hygiene | OK | No trailing whitespace, no tabs, final newline on every `.py`; only `audit.py` and `test_audit.py` changed in cycle 2; the temp mutation copy was removed (trap) and nothing was written to the repository. |
| Test and lint gates | OK | Commands in the table above. |

## Notes (not blocking, not rechecked later)

- The new test `test_no_free_text_key_exists_on_any_line_kind__...` duplicates the coverage of the older forbidden-key test; harmless.
- The carried-forward minor notes (discover raising `ValueError` for unsafe trigger or login that Phase 6 must validate first; fixture-coverage test as substring search; real 3.10 run) are unchanged.

## Summary

- Checks passed: 10 / 10 (A-7 fix, 2 new tests, old rows intact, regression section, imports, Python 3.10, hygiene, tests, ruff check, ruff format)
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 9 | Grep: 1 | Glob: 0 | Bash: 4 (tests, ruff, one inspection batch, one mutation batch). Read + Grep + Glob = 10 against 10 checklist items; the Bash batches carry the other grep and run evidence.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| none | - | - | No blocking issue open | - |

## QA Complete
