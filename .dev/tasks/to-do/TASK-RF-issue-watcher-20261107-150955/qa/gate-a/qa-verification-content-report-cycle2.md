# QA Report - Gate A fix verification, content (fix cycle 2)

**Topic:** issue-watch implementation, Phases 2 and 3 (`src/superclaude/cli/issue_watch/`, `tests/issue_watch/`)
**Date:** 2026-11-07
**Phase:** fix-cycle (content verification of `qa/gate-a/qa-fix-report-cycle2.md` against `qa/gate-a/qa-consolidated-findings-cycle2.md`)
**Fix cycle:** 2
**Agent:** rf-qa-qualitative, `fix_authorization: false` (no file other than this report was written)

---

## Overall Verdict: PASS

The one blocking cycle-2 finding, A-7, is FIXED. The false claim in `audit.py` is gone from both places and the new text matches what the code does. No cycle-1 fix was broken again. No new blocking content issue was found. Three minor notes are recorded below.

## Per-finding verification

| id | Result | Evidence |
|---|---|---|
| A-7 | FIXED | Cycle-2 remedy (consolidation row): reword both statements to say `host` and `login` take any printable bounded token. Done. (1) `audit.py:4-10` module docstring now reads: each value must match a closed shape "(an enum, a fixed pattern or a range, see ``_RULES``). The one exception is ``host`` and ``login``: they take any printable token of bounded length (``login`` without whitespace), so a caller can still put arbitrary text there. No issue title, body, label or stderr text has a key or a typed slot on a line." The sentence "free text cannot be written into a line through any key" is gone. (2) The comment above `_RULES` (`audit.py:218-222`) now says the `host` and `login` rules "only bound length and printability (login also bars whitespace)... they do not filter free text", and that the login rule is looser than the cycle's regex (design line 348, which is step 5 of the cycle table and names the login regex: checked). "Every other key is closed." The old "it only keeps free text out" is gone. (3) Behaviour matches the text. `_RULES` (`audit.py:223-237`): `host` is `_is_token(v, 255)` (printable, 1..255); `login` is `_is_token(v, 100)` and no whitespace. Probe (temporary script, deleted): `warning_line(host="Fix the login bug in prod, urgent")` is accepted and written; `login="a,b"` is accepted; `title=`, `body=`, `label=`, `stderr=` each raise `TypeError` (no such parameter), so no line kind has a typed slot for them. The code was not changed: the rule values equal those the cycle-1 content report recorded (host 1..255 printable; login 1..100 printable, no whitespace). |

## What the two new tests pin (and whether they would catch a relapse)

| Test | Verified | Evidence |
|---|---|---|
| `test_host_and_login_take_any_printable_bounded_token__ac14_fr020_nfr006` (`test_audit.py:444-456`) | Real behaviour, not a stub | Builds real warning lines: a sentence and a 255-character `host` are accepted and read back; a comma-bearing token and a 100-character `login` are accepted and read back. Then it reads `audit.__doc__`, collapses whitespace, and asserts it contains "``host`` and ``login``" and "any printable token" and does not contain "free text cannot be written". Putting the old sentence back in the docstring, or tightening `host` without updating the docstring (the sentence is then rejected), fails this test. The boundaries 255 and 100 are also covered on the reject side by the cycle-1 rows `("host", "h" * 256)` and `("login", "x" * 101)` (`test_audit.py:393,398`). |
| `test_no_free_text_key_exists_on_any_line_kind__ac14_fr020_nfr006` (`test_audit.py:459-463`) | Real invariant | Takes the union of required and optional keys of every kind in `audit._KEYS` and asserts it is disjoint from `FORBIDDEN_KEYS` (`test_audit.py:164`: rate_remaining, title, body, label, label_name, stderr) and a subset of `audit._TYPES` (so no key has an unchecked type). Adding a `title` key to any line kind fails it. |

## Regression check against cycle 1

- Files changed since the cycle-1 content report was written: `find -newer` over `src/superclaude/cli/issue_watch` and `tests/issue_watch` lists only `audit.py` and `test_audit.py`. `github.py`, `predicates.py`, `runner.py`, `conftest.py`, `test_github.py`, `test_predicates.py` and `test_runner.py` carry mtimes of 21:22-21:33, before cycle 1 was verified (21:37). So the 17 cycle-1 FIXED items A-1 to A-6 and A-8 to A-18 sit in files that were not touched in cycle 2.
- Test count: cycle-1 content report recorded 684 passed; now `uv run pytest tests/issue_watch/ -q` gives **686 passed in 1.33s** (684 plus the 2 new tests). No test was lost; no count dropped.
- `test_audit.py` parametrized A-7 rows are intact: 36 rejected rows (`test_audit.py:371-411`: state 4, cycle_id 5, ts 5, approved_at 3, host 3, login 5, issue 3, approver_id 2, approval_event_id 1, exit 2, gh_calls 1, duration_ms 1, discovery_count 1) and 22 accepted rows (`test_audit.py:418-438`), the same 36 and 22 the cycle-1 content report counted. The enum pin (`test_audit.py:466`) and the issue-bound pin (`test_audit.py:478`) are present.
- No assertion weakened or deleted: the only edits recorded are one docstring, one comment and two added tests; the rule table and every existing row match the cycle-1 report. The pre-cycle-2 file is not kept (the tree is untracked), so this rests on the unchanged row counts, the unchanged 686 minus 2 count, and reading the file; that limit is stated here.
- Gate commands re-run: `uvx --offline ruff@0.15.20 check src/superclaude/cli/issue_watch tests/issue_watch`: All checks passed. `format --check`: 11 files already formatted.

## New blocking findings

None.

## New minor notes (not rechecked later)

| # | Location | Note |
|---|---|---|
| M-5 | `audit.py:4-6` | "each value must also match a closed shape (an enum, a fixed pattern or a range)" is slightly wide: `clock_skew_s` (any int) and `dry_run` (bool) have no `_RULES` entry (probe: keys without a rule are `clock_skew_s`, `dry_run`, `kind`, `note`, `reason`; the last three are closed by `_KEYS` and `REASONS`). Neither can carry text, so this is wording only. Consider "except `host`, `login` and `clock_skew_s`". |
| M-6 | `audit.py:8-9` | "No issue title, body, label or stderr text has a key or a typed slot" reads as stronger than the next-to-last sentence allows, since `host` and `login` can still carry any text a caller passes. The two sentences are consistent if "key" means a dedicated key; wording only. |
| M-7 | `test_audit.py:453-456` | The docstring assertions search for exact phrases ("any printable token", the double-backtick form), so a harmless rewording of the docstring fails the test. Brittle, not wrong. |

Carried forward from earlier cycles and still open as notes: Phase 6 `load_config` and the cycle must validate `labels.trigger` and the login before `discover` and reject a comma or leading dash as `config_invalid` (else `discover` raises `ValueError` inside a cycle); the fixture-coverage test only checks fixture names in the test source. Neither is blocking.

## Self-Audit

**(a) Reliance list**
- No `## Inherited Structural Verdict` section was in the spawn prompt, so this ran standalone. No rf-qa PASS item was relied on. The cycle-1 structural report (PASS) was read only for the regression check and for the 684-test baseline.

**(b) Independent semantic checks (at least 1 required, INV-019)**
- Docstring claim against code: read `audit.py` in full (lines 1-399) and ran a probe that built a warning line with an English sentence as `host` and a comma token as `login` (both accepted), and tried the keys `title`, `body`, `label`, `stderr` (all rejected). The new text says exactly this.
- Comment reference: read `docs/designs/issue-watcher.md:340-351`; line 348 is cycle step 5 and names the login regex, so the comment's "design line 348" is correct.
- Test validity: read `test_audit.py:340-480`; the first new test builds real lines and reads the real docstring, the second inspects the real `_KEYS` and `_TYPES`; neither is a placeholder.
- Regression: `find -newer` against the cycle-1 report (only `audit.py`, `test_audit.py`), full suite 686 passed, ruff check and format clean, row counts 36 and 22 recounted from the file.
- Remaining-keys probe: listed the keys without a `_RULES` entry and judged each (source of M-5).

**Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (checklist = 1 blocking id, the 2 new tests, the regression check, the no-new-blocking check, the no-weakening check, counted as 5 groups: A-7, new tests, regression, no weakening, no new blocking).
**Tool engagement:** Read: 7 | Grep: 2 | Glob: 0 | Bash: 5 (suite run, ruff check and format, find -newer and mtimes, probe). Read + Grep + Glob = 9 against 5 checklist groups.
**Web research:** none; Tavily not used.

## Recommendations

1. Proceed. Gate A content verification is PASS for cycle 2; no further fix cycle is needed.
2. Keep M-5 to M-7 and the carried-forward Phase 6 note (`labels.trigger` and login validation before `discover`) as notes. They never fail a review.

## QA Complete
