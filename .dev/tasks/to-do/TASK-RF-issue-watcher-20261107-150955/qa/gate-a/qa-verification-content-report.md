# QA Report - Gate A fix verification, content (fix cycle 1)

**Topic:** issue-watch implementation, Phases 2 and 3 (`src/superclaude/cli/issue_watch/`, `tests/issue_watch/`)
**Date:** 2026-11-07
**Phase:** fix-cycle (content verification of `qa/gate-a/qa-fix-report.md` against `qa/gate-a/qa-consolidated-findings.md`)
**Fix cycle:** 1
**Agent:** rf-qa-qualitative, `fix_authorization: false` (no file other than this report was written)

---

## Overall Verdict: FAIL

17 of 18 blocking ids are FIXED. One, A-7, is NOT FIXED: its false docstring claim is only half removed. The code now validates every audit value, but `audit.py:4-7` still says "free text cannot be written into a line through any key". `host` and `login` still accept free text (probe below). The remedy is one sentence or one regex. No other new blocking issue was found.

## Evidence gathered

- Read in full: `runner.py`, `predicates.py`, `audit.py`, `github.py`, `conftest.py`. Read in part: `test_github.py` (lines 1-130, 255-324, 384-482, 555-700, 1360-1530, 1810-1950), `test_predicates.py` (150-280, 370-430), `test_audit.py` (340-470), the 5 new or changed fixtures.
- Design ranges read: `docs/designs/issue-watcher.md` 131, 215-226, 340-351, 415-426, 540-602, 695-726, 828-847; spec-final lines 87-88, 128.
- `uv run pytest tests/issue_watch/ -q`: **684 passed** (fix report says 684; the pre-fix run in `p3-g1-raw.txt` had 373).
- Deleted-test check: test ids passed before the fix (370 captured from `p3-g1-raw.txt`) compared with ids passed now (659 captured): **0 old ids missing**. No test was deleted or renamed. (3 and 25 ids are lost to line wrapping in the grep on both sides, so this is a check of the captured ids, not of all.)
- Behaviour probe (a temporary script, deleted afterwards): results quoted per row below.

## Per-finding verification

| id | Result | Evidence |
|---|---|---|
| A-1 | FIXED | Five tests build the scripted reply from the five fixtures (`test_github.py:1379-1485`: gh_issue_list, rest_events_page, rest_comments_marker, graphql_edits, graphql_project_items) and assert the parsed values, so a changed capture changes a result. `...events_fixture` also runs `approval_of` on the result (expects `not_approved`, correct because the fixture unlabels the approval). `test_every_assumed_shape_fixture_is_read_by_a_test__df32` (585-593) fails for an unread file. Weakness: it is a substring search of the test source for `"<name>"`, so a name in a comment satisfies it (minor, M-3). The 14 fixtures all parse and carry `_assumed_shape: true`. |
| A-2 | FIXED | `github.py:768-770` now reads `[UNVERIFIED] reply shape (design 837, FU-1): treated as None when the value is null or has no name; any other non-object value is malformed`. This is exactly what lines 770-775 do (`None` -> `None`; `_obj(status)` raises on a non-object; `_opt_text(name)`). The false sentence is gone. |
| A-3 | FIXED | Three fixtures added (`gh_api_user_include_429.json`, `gh_stderr_http_502.json`, `gh_stderr_scope_read_project.json`), each tagged `_assumed_shape` with the design row. All three are read by tests (lines 421, 453, 1492, 1513, 1526). `g1_result`, `event_item`, `marker_item`, the `gql` block (941), the stderr table (458) and the G1/G7 helpers (1572, 1601, 1636) carry `[UNVERIFIED, assumed shape]` with the design row and twin fixture. Inline-to-fixture swaps keep the same assertions (`test_classify_auth_failed_from_the_401_fixture`, `..._transient_for_http_502`). |
| A-4 | FIXED | `predicates.py:24,37` add `fullmatch` on `[0-9]{4}-..Z` before `strptime`. Probe: `2026-1-5T1:2:3Z`, lower-case `z`, Arabic-Indic digits, trailing `\n`, `23:59:60Z`, `2026-02-30` all raise `ValueError`; `2026-11-07T12:00:00Z` parses. The docstring now matches the code. |
| A-5 | FIXED | `runner.py:91-101` add `encoding="utf-8", errors="replace"`; `112` catches `(OSError, ValueError)` as `spawn_error` by class name; `82-87` raise `TypeError` on empty, `str` or non-str-item argv. Probe: NUL in argv and NUL in `cwd` give `returncode=None, spawn_error='ValueError'`; a missing binary gives `FileNotFoundError`; a child writing `a\xff\xfeb` gives `'a��b'`, return code 0; `[]`, `()` and `"gh"` raise `TypeError`. Design 218 only names `str`; the extra `TypeError` for an empty list is stricter and harmless (every `github.py` argv is non-empty). |
| A-6 | FIXED | `github.py:739-746` `_edited_at` requires the key (`_check("lastEditedAt" in d)`), explicit null stays "never edited"; used by `_edit_issue` and `_comment_edit`. Probe: `{}` raises `_Malformed`, `{"lastEditedAt": None}` gives `None`. Tests at 1925-1960 cover issue key missing, comment key missing and the null control; the missing-key paths give `edits_unreadable`. |
| A-7 | **NOT FIXED** | Done: `_RULES` (audit.py:218-232) puts a closed shape on `state` (the design 422 enum, matches `_ENTRY_STATES`), `cycle_id` (32 lower-case hex), `ts`/`approved_at` (real UTC time), `issue` (1..999999999), ids above 0, `exit` 0..255, counts at least 0, with 36 rejected and 22 accepted test rows, an enum pin and a bound pin. Not done: the module docstring (audit.py:4-7) still says each value matches "a closed shape (an enum, a fixed pattern or a range), so free text cannot be written into a line through any key". `host` is only "printable, 1..255" and `login` only "printable, no whitespace, 1..100". Probe: `warning_line(host="Fix the login bug in prod title text", ...)` is accepted and the sentence is written; the tests themselves accept `host="hôst-☃"` and `login="bad_login!"`. The comment above `_RULES` ("it only keeps free text out") overclaims the same way. This is the same defect class as the original A-7 (a false statement about what can reach an audit line), now on two keys. Fix: reword the docstring to "except `host` and `login`, which take any printable token of bounded length", or restrict `host` to a hostname charset (for example `[A-Za-z0-9._-]{1,255}`) and `login` to the login charset, with rejected-value rows. |
| A-8 | FIXED | Docstring (github.py:1-10) now names the five caller values and says each is checked here. `_trigger_arg` (150-165): 1..50 chars, no control char, no comma, no leading dash. `_login_arg` (168-172): `[A-Za-z0-9][A-Za-z0-9-]{0,38}` via `fullmatch`; this equals the cycle's regex quoted in the task plan (TASK file line 462). `_cursor_args`/`_valid_cursor` (125-147): `[A-Za-z0-9+/=_.:-]{1,256}`, tagged `[UNVERIFIED]`. A hostile `endCursor` in a reply is checked before use (698-699) and gives `unreadable`/`non_json` with no further call. Probe: `a,b`, `-x`, `bad login`, `-x` login, 60-char trigger, NUL trigger rejected; `Y3Vyc29yOnYyOpHOAAAA` accepted; `abc def`, 257 chars, trailing `\n` rejected. A cursor of `-f` is accepted but always sent as `after=-f`, so it cannot act as an option. Tests at 2100-2150 cover hostile and benign values and the no-call rule. |
| A-9 | FIXED | 13 `reread` tests (1654-1830): success, empty lists, reserved-slot use and refusal beyond 35, `timeout_for` None makes no call, another number (and `True` for issue 1), malformed fields, missing keys, non-object body, and the 8-way transient/failed split with `len(runner.calls) == 1`. Swapping the two reasons or dropping `d.get("number") == n` (github.py:951) now fails a test. |
| A-10 | FIXED | `SHARED_FAILURES` (1510-1540) run against `user` and `discover` (1553, 1560) asserting reason, kind and `retry_after_s`; `Retry-After` 120/1/absent/unparseable on `user`; malformed G1 bodies including `id: true`. Mapping everything to `gh_auth_failed` or dropping the carry now fails. |
| A-11 | FIXED | `REST_FAILURES` (1837-1851: timeout, 401, rate limit, 5xx, failure, non-JSON, spawn error) run for both `events` and `marker_comments` on page 1 (1856) and page 2 (1871); assert value None, the `*_unreadable` reason, the kind, and for page 2 that two calls were made. An empty history on a failed page can no longer pass. |
| A-12 | FIXED | `test_graphql_exit_zero_errors_kind__df02_fr028` (1885-1919) for both G5 and G6: the `RATE_LIMITED` fixture and inline, scope beating rate, rate after another type, non-dict item, no type, int type, null type, string, dict. Deleting `_errors_kind` lines 636-637 would fail it. |
| A-13 | FIXED | `test_ac3_only_renamed_events_count_as_changes__fr005` (test_predicates.py:389-405): a `labeled` event exactly at `approved_at`, later `labeled`, `unlabeled`, `assigned`, `milestoned` leave the result `None`; adding a `renamed` event flips it. Dropping the `renamed` filter (predicates.py:243) fails the test. |
| A-14 | FIXED | `predicates.py:207` now `type(approval.actor_id) is not int`; tests cover `actor_login`, `actor_type`, `actor_id` None, wrong-case and organization type (184-202), `actor_id=True` with `approvers={1}` (205-216; would be approved without the guard because `True in {1}`), and equality at `store_created_at` (240-246: equal gives `approval_before_init`, one second earlier approves). Spec-final line 88 says "later than the store's `created_at`", so `<=` is right and now pinned. |
| A-15 | FIXED | `test_rotation_fsyncs_the_state_dir_once_after_the_last_replace__df30` (test_audit.py:608) records `os.replace` and `os.fsync` and expects exactly one state-dir fsync after the last replace; `test_no_rotation_means_no_fsync__df30` (625) covers the no-file and below-threshold cases. Deleting `_fsync_dir` (audit.py:147) fails. |
| A-16 | FIXED | `EDITS_QUERY` and `PROJECT_ITEMS_QUERY` are written out in the test (49-76) and the G5/G6 argv tests use them; `test_graphql_constants_equal_the_literal_drafts__df14` (273) pins `github.* == literal`; `test_graphql_query_asks_for_what_the_parsers_read__df14` (278-311) pins `first: 100` and each field the parsers read. Only the expected value changed in existing tests; the assertions are the same. |
| A-17 | FIXED | `FakeRunner.timeouts` (conftest.py:76,85) records every call's timeout; tests with distinct `timeout_for` values show `user`, `discover`, `reread`, REST paging and GraphQL paging pass the value to `runner.run` (for example 1979). `runner.run(argv, 30.0)` hard-coded now fails. |
| A-18 | FIXED | CRLF copies of the G1 fixtures (2015-2047): `classify` ok, `retry_after` 120, `date_header` parsed, `user()` reads it; a header block with a line lacking a colon, no status line and no blank line give `non_json`. Removing the `.replace("\r\n", "\n")` at github.py:296 fails a test. Note: `SubprocessRunner` uses `text=True` (universal newlines), so CRLF never reaches the parser in production; the branch is defensive and the test is correct for it. |

## No assertion weakened or deleted

- Test ids: every one of the 370 captured pre-fix ids is still passing in the current run (see Evidence).
- The three edits to existing tests named in the fix report were read: constant to literal (A-16, same `==` assertions), inline string to fixture read (A-3, same `kind` assertions), fixture count 11 to 14 (test_github.py:578). None loosens an assertion.
- The pre-fix test file is not kept (the tree is untracked), so a line-by-line diff of every old assertion was not possible. The conclusion rests on the id comparison, the three edits read, and 684 passing tests; this limit is stated here, not hidden.
- Source files carry mtimes later than the test files (21:33:06-21:33:17 against 21:32:41); this matches the fix report's restore after mutation runs. I re-ran the full suite on the current tree: 684 passed.

## New blocking findings

None beyond the open A-7 item.

## New minor notes (not rechecked later)

| # | Location | Note |
|---|---|---|
| M-1 | `audit.py:389-390` (`stderr_fallback`) | The crash fallback now calls `_check_value("host", ...)`. Probe: `host=""` raises `ValueError`. A host name that is empty or non-printable would make the last-resort writer itself fail. `socket.gethostname()` is not expected to return one; consider falling back to `"unknown"`. |
| M-2 | `github.py:150-165` vs design 131 | Design 131 allows any non-empty 50-character trigger without control characters; `_trigger_arg` also rejects a comma and a leading dash, and `discover` raises `ValueError` for them. Phase 6 `load_config` must reject the same values as `config_invalid`, or `discover` will raise inside a cycle. The fix report lists this for login and trigger; add it to the Phase 6 plan items. |
| M-3 | `test_github.py:585-593` | The "fixture is read by a test" guard is a substring search of the test source. A file name in a comment or docstring satisfies it. Parse with `ast`, or match `load("<name>")`. |
| M-4 | `audit.py:215-217` comment | "it only keeps free text out" overstates; see A-7. |

## Self-Audit

**(a) Reliance list**
- No Inherited Structural Verdict section was in the spawn prompt, so this ran standalone. No rf-qa PASS item was relied on.

**(b) Independent semantic checks (at least 1 required, INV-019)**
- A-7 docstring claim against code: read `audit.py:1-8,168-232`, ran a probe that built a warning line with a 35-character English sentence as `host`; it was accepted. The fix report's "every key now has a value shape" is true in form and false in effect for `host` and `login`.
- A-5 against the real runner: probe with NUL bytes in argv and `cwd`, a missing binary, non-UTF-8 child output and three bad argv shapes; each outcome quoted above.
- A-4 against `strptime`: probe with six malformed times.
- A-14 mutation reasoning: `True in {1}` is True, so the bool test fails without the new `type(...) is int` guard.
- Test deletion: compared pre-fix and post-fix passed ids with `comm -23`; empty result.
- Full suite re-run: 684 passed on the current tree.
- Design alignment: state enum (design 422), login regex (task plan 462), `store_created_at` "later than" (spec-final 88), `--method GET` and G1 exemption (design 554), 5-call and 35-call caps.

**Confidence:** Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (checklist = 18 finding ids + no-weakening + no-new-blocking). The verdict is FAIL because of one verified defect, not because of low confidence.
**Tool engagement:** Read: 17 | Grep: 11 | Glob: 0 | Bash: 7 (suite runs, id comparison, probe run, listings). Read + Grep + Glob = 28 against 20 checklist items.
**Web research:** none; Tavily not used.

## Recommendations

1. Close A-7: either reword `audit.py:4-7` and the `_RULES` comment to say `host` and `login` take any printable bounded token, or tighten both to a charset with rejected-value rows. One edit plus 4 test rows. Then re-verify only A-7 in cycle 2.
2. Add M-2 to the Phase 6 `load_config` plan: reject a comma, leading dash or NUL in `labels.trigger` as `config_invalid`.
3. Keep M-1, M-3 and M-4 as notes; they never fail a review.

## QA Complete
