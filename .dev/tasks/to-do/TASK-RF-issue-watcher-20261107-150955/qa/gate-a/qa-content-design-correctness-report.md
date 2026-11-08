# QA Report — Gate A, design-correctness lens (task-qualitative)

**Topic:** issue-watch implementation, Phases 2 and 3 (runner.py, predicates.py, audit.py, github.py)
**Date:** 2026-11-08
**Phase:** task-qualitative (lens: design-correctness)
**Fix cycle:** N/A (first review, fix_authorization: false, report only)

---

## Overall Verdict: FAIL

One blocking finding (F-01) and 14 minor findings. Only F-01 makes the verdict FAIL.

The brief assumed at least 15 errors. I found 15 findings in total (1 blocking, 14 minor), every one reproduced or read in source. I did not pad the list: the runner, the reason table, the argv forms and the classifier table match the binding text on all the points I could test (see Items Reviewed).

## Items Reviewed

Axis column: AX-1 drift, AX-2 contradictions, AX-3 omissions, AX-4 weakened criteria, AX-5 invented content, none. `drift-axis-inactive` does not apply: the design text, spec lines and DF rows were read as the baseline.

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Runner signature and cwd handling (D 265, DF-01) | AX-2 | FAIL (F-01 only) | `runner.py:40-42,69-71,90` has `run(argv, timeout, *, cwd=None)` and passes `cwd=cwd` to `subprocess.run`. Probe: a bad cwd gives `spawn_error=FileNotFoundError`. The runner raises on non-UTF-8 output, empty argv and a NUL byte (F-01). |
| 2 | 57-name reason table, kind and exit (S 330-358, DF-02/03/22/41/57) | none | PASS | Probe: `len(REASON_TABLE) == 57`. I compared all 52 spec rows with `audit.py:19-89` one by one: kind and exit match. The five proposals match DF-41 (`marker_unreadable`, `edits_unreadable` skip 0; `operator_reset` skip/warning 0; `dry_run_shadow_reset` warning 0; `reset_refused` warning 2). A scan of design and spec for reason-like names missing from the table found none. |
| 3 | Audit line schema (D 697-722, DF-33) | AX-2 | PASS with notes | Key sets, nullability, `ensure_ascii`, sorted keys, `O_APPEND` single `os.write`, 5 MiB rotation order `.3→.4 … current→.1` plus directory fsync, `stderr_fallback` key set all match. Notes F-05, F-06, F-13, F-14. |
| 4 | Approval rule (a) to (e), tie rule, trigger order, init floor | none | PASS | 16 probe cases against `approval_of`: allow-list, `[bot]`, `Bot` type, re-label by outsider, unlabel after, before trigger, before init, equal to init, same-second ties, missing trigger event (OQ-38). All give the reason S 84-92 and FR-005/FR-006 GWT require. Note F-08 on the tie scope. |
| 5 | Owner rule (FR-008) | none | PASS | `{o}` true; `{}` unassigned; `{o,x}` and `{x}` assigned_other; `{o,o}` true. |
| 6 | Project rule (S 96, FR-007) | none | PASS | One live item in `project_id` with Status `Backlog` passes; archived, duplicate, wrong project and `backlog` (case) give `project_mismatch`. |
| 7 | Marker-window and `marker_time` (D 502, DF-16, S 100) | none | PASS | Exactly `pending_at − 300 s` counts; 301 s does not; an old comment edited after `pending_at` counts; with no `pending_at` an equal-to-approval marker does not count and a later one does; marker false, other login, different case do not. |
| 8 | Ordering rule (D 352, FR-023) | none | PASS | `[9, 7, 8]` for map `{7: T1, 8: T2}` and discovery `{7, 8, 9}`. |
| 9 | Unchanged-since rule (S 94, OQ-37) | none | PASS | Own-login comment after approval ignored; ghost author counted; equal timestamp counts as changed; renamed after approval fails, before passes. |
| 10 | Classifier table, every row in order (D 577-588, DF-37) | AX-2 | PASS with notes | 16 probe replies: timeout, exit 0 ok/non-JSON/empty, 401, `gh auth login`, GraphQL `INSUFFICIENT_SCOPES`/`RATE_LIMITED`, 403+rate limit, 429 alone (failed, as the table says), 500/502, spawn error. All match the table. Note F-11. |
| 11 | Rate-limit time rules (D 598-602, DF-35) | AX-2 | FAIL on a contrived input (F-02, minor) | Retry-After 120 gives now+120 `rate_limited`; 3601, HTTP-date, absent and non-G1 clamp to now+3600 `rate_limit_clamped`; reset +30 s used. Header of more than 4300 digits raises (F-02). |
| 12 | Paging, null-handling, budget rules (D 566-575, DF-18/19) | AX-2 | PASS with notes | 100 then 1 item completes; five full pages `events_incomplete`; page of 101 `events_unreadable`; repeated id `events_incomplete`; bool and float ids unreadable; G4 incomplete is `marker_unreadable`; null login dropped; GraphQL repeated or empty cursor incomplete; budget 32 plus 3 reserved. Notes F-03, F-07, F-09, F-12. |
| 13 | Argv forms G1 to G7 (D 541-550, 554) | none | PASS | All seven argv lists equal the design rows; `--method GET` on G3, G4, G7 only; none on G1 or GraphQL; `-F number=` typed; cursor sent with raw `-f`. `EDITS_QUERY` and `PROJECT_ITEMS_QUERY` are byte-equal to Table 1.5 (DF-14). |
| 14 | Module boundaries named in D 218-224 | none | PASS | `subprocess` imported only in `runner.py`; `predicates` and `audit` import nothing from the package; `github` imports `runner` and `predicates` only. |
| 15 | Cross-symbol input-shape agreement (check 5 of the lens) | AX-2 | FAIL (minor F-10) | `DiscoveredIssue.state` is `"OPEN"` (gh issue list), `IssueSnapshot.state` is `"open"` (REST); neither is normalised or documented. |

## Summary
- Checks passed: 12 / 15 (3 rows carry a finding: 1, 11, 15)
- Checks failed: 3 (one blocking row, two minor)
- Critical issues: 0
- Blocking issues: 1 (F-01)
- Issues fixed in-place: 0 (report only)

## Issues Found

Severity: blocking (B) or minor (m), by the review severity rule. File paths are relative to the repository root.

| id | severity | file | evidence | expected versus actual |
|---|---|---|---|---|
| F-01 | B | `src/superclaude/cli/issue_watch/runner.py:69-111` | Probe on `SubprocessRunner.run`: a child writing `b"\xff\xfe"` to stdout or to stderr raised `UnicodeDecodeError`; `run([], 5)` raised `IndexError`; `run(["echo", "a\0b"], 5)` raised `ValueError`. The same module decodes partial output with `errors="replace"` on the timeout path (`_as_text`, line 52). | Expected (D 218, module docstring "report what happened"): every child outcome becomes a `CommandResult`, and only `TypeError` for a `str`/non-`list[str]` argv escapes. Actual: `text=True` uses strict decoding, so invalid bytes from `gh`, `git` or `orca` raise out of the one trust-boundary adapter. After the `pending` save, an Orca launch whose output has a bad byte would crash the cycle with the slot consumed and no `operation_id` stored (the entry is later swept to `abandoned`/`pending_orphan`, not `unknown`). Fix: pass `encoding="utf-8", errors="replace"` to `subprocess.run`; map `ValueError` and `IndexError` from the call to `spawn_error`; add a test for each. |
| F-02 | m | `src/superclaude/cli/issue_watch/github.py:345-350` | Probe: a `Retry-After` of 5,000 digits made `rate_limit_wait` raise `ValueError` ("Exceeds the limit (4300 digits)", Python 3.11 and later). `re.fullmatch("[0-9]+")` passes, then `int()` raises. | Expected (D 600, DF-35): an unparseable value clamps to now + 3600 s with `rate_limit_clamped`. Actual: an exception. Only G1 headers are read, so the input is contrived. Fix: cap the digit count (for example `[0-9]{1,10}`). |
| F-03 | m | `github.py:413-415,727-760` | `user()` and `discover()` call `_call(..., budget=None, ...)` and never count; counting is left to the cycle (`spend_shared`). | Expected (D 219, D 537 "every one counted by `CallBudget`"): `github.py` counts every call. Actual: G1 and G2 are counted only if the P6 cycle remembers; otherwise `gh_calls` under-reports by 2 and the 37-call worst-case arithmetic (D 381) is wrong. Fix: give `user` and `discover` the budget and call `spend_shared()` inside `_call`. |
| F-04 | m | `audit.py:149-153` | `clock_skew_s` is in the optional set of a `cycle` line. | Expected (D 715 table, `clock_skew_s`, Cycle line: "yes"; S 100 "The cycle line records the offset"): required on a cycle line. Actual: optional. The table's type is `int` with no null, so the design is itself unclear for a cycle that never reached G1; decide and pin it. |
| F-05 | m | `audit.py:164-184,265-289` | `state` accepts any `str`; `ts` and `approved_at` accept any `str`. | Expected (D 712 type "enum"; D 704 "UTC str"): enum-checked `state`, UTC-format `ts`. Actual: unchecked, so a caller mistake could put free text on an audit line (NFR-006). Fix: check `state` against the Section 7 states and `ts` with the `parse_utc` format. |
| F-06 | m | `audit.py:117-126` | `AuditLog.append(line: dict)` writes any dict. | Expected (D 223: builders are the only way to build a line, "Never: contain issue text"): `append` accepts only built lines. Actual: a caller can bypass the key and reason checks. Fix: have the builders return a small `Line` type, or re-run `line()` checks in `append`. |
| F-07 | m | `github.py:663-677` | Probe: an `assigned` event with `actor_id = 0`, and one with an integer `actor_login`, made the whole history `events_unreadable`. | Expected (DF-18): "`renamed` and every other kind need only `id`, `event`, `created_at`"; only fields a predicate reads for that kind may fail the read. Actual: non-null actor and label fields of every kind are type-checked. Fail-closed side and unlikely on real data; but it departs from the decision. |
| F-08 | m | `predicates.py:179-189` | Probe: trigger and approval `labeled` in the same second on 2026-11-03, then an unlabel, then a proper approval on 2026-11-05 gives `events_incomplete`; the old tie never leaves the history. | Matches S 92 literally ("an opposing tie is ... with equal `created_at` seconds") and S 94 says re-applying the label re-arms. A tie among superseded events cannot change checks (c) or (e), yet it blocks the issue for good. Owner question, not an implementation error: restrict the scan to the latest approval, latest trigger and later unlabels, or accept it and say so in the runbook. |
| F-09 | m | `github.py:633,649-650` | Probe: `"errors": []` on an otherwise valid reply gives `edits_unreadable`; a repeated `endCursor` on a final page with `hasNextPage` false gives `incomplete`. | Reference script `poll-augment-review.sh:107` accepts `.errors == []`; D 575 flags a repeated cursor as incomplete. Both are fail-closed and probably rare; the reply shapes are UNVERIFIED (FU-1, FU-3). Pin them with `_assumed_shape` cases or relax. |
| F-10 | m | `github.py:778,895` with `predicates.py:60-66,82-89` | Probe and fixtures: G2 `state` is `"OPEN"` (fixture `gh_issue_list.json`), G7 `state` is `"open"` (REST). | Two siblings that feed the same "is open" decision disagree on case and neither is normalised or documented (lens check 5, input-shape invariant). Fix: lower-case both at parse time or document the two forms. |
| F-11 | m | `github.py:302-328,588-595` | `classify` returns `ok` for an exit-0 reply whose body carries GraphQL `errors` of type `INSUFFICIENT_SCOPES` or `RATE_LIMITED`; only `_graphql_read` handles them. | D 577 says `classify` "maps every runner result before any field is read", and D 585-586 list the two GraphQL types as table rows. Real `gh` exits 1 on GraphQL errors, so the exit-0 path is hypothetical; the rows are met in two places instead of one table. |
| F-12 | m | `predicates.py:25-32` | Probe: `parse_utc("2026-1-1T1:2:3Z")` parses. | Expected (DF-35): the exact `%Y-%m-%dT%H:%M:%SZ` shape. `strptime` accepts unpadded fields. Fix: add a `re.fullmatch` on `\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z` before `strptime`. |
| F-13 | m | `audit.py:218,331-332` | `line()` rejects `re-approved` as a reason; `stderr_fallback` accepts it. | The two reason checks disagree. Fix: share one `_check_reason`. |
| F-14 | m | `audit.py:120-126` | A short `os.write` leaves a truncated JSON line on disk and then raises `OSError`. | A partial line breaks the NFR-013 reducer for every later read. Unlikely on a local file; at least name it in the docstring or write a repairing newline. |
| F-15 | m | `github.py:337-342` with `tests/issue_watch/conftest.py:76-88` | `_g1_header` decides whether headers apply from `result.argv`; `FakeRunner.run` returns a scripted `CommandResult` unchanged, and `conftest.result()` defaults `argv=()`. | A P6 cycle test for DF-51 (`Retry-After: 120` on G1) that builds its reply with the default `argv` silently gets no header and the clamp. `test_github.py` always passes `argv`, so it is covered today. Fix: stamp `argv=key` in `FakeRunner.run`, or pass `include_headers` to the header helpers. |

## Minor notes (not findings)

- `rate_limit_wait` clamps an `x-ratelimit-reset` that is already in the past to a full hour (D 599 says "within 3600 s" and is silent on the past). Conservative; say so in the runbook.
- `Retry-After: 0` with no reset header clamps to 3600 s (`test_github.py:428` pins it); D 598 range is `0 < s`. Conservative.
- `AuditLog.append` follows a symlink at `audit.jsonl` (no `O_NOFOLLOW`), unlike the lock (D 515). D 699 does not require it and the state directory is mode 0700.
- The change set (`gate-a-change-set.md`) lists DF-48 among the rows applied; it is a test-seam row, not in the design-correctness list I was given. Harmless.

## Actions Taken

None. fix_authorization was false; I modified no file other than this report. The probe scripts I ran lived in `/tmp` and were deleted.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)

No `## Inherited Structural Verdict` section was in my spawn prompt, so I fell back to standalone behaviour and did not skip any structural check on the strength of another report.

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- None. No inherited verdict was supplied. I did not read or rely on the other Gate A lens reports.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Reason table is exactly 57 and every kind and exit equals the spec table: Bash probe `len(REASON_TABLE)` printed 57; Read of `audit.py:19-89` against `spec-final.md:332-358` row by row.
- Classifier table: 16 scripted replies through `github.classify`, results compared with `issue-watcher.md:577-588` (Bash probe, stdout kept in my notes).
- Approval, marker-window, owner, project, unchanged and ordering rules: 40 probe cases against `predicates.py` using the FR-005, FR-006, FR-008, FR-009 and FR-023 GWT values.
- Paging and null rules: 30 scripted runs of `events`, `marker_comments`, `edits`, `project_items`, `user`, `discover`, `reread` and `CallBudget` through a scripted runner.
- Runner contract: 8 live `SubprocessRunner` runs (invalid UTF-8 on both streams, empty argv, NUL byte, bad cwd, cwd that is a file, missing binary, timeout with partial output, 400 two-byte characters for the 500-byte cap). This found F-01.

**Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
(The 15 are the Items Reviewed rows. Behaviour was run, not only read. The reply shapes of `gh` itself stay UNVERIFIED, as the design says; no live `gh` call was made.)

**Tool engagement:** Read: 19 | Grep: 12 | Glob: 0 | Bash: 7 (5 probe runs, 1 `wc -l` and listing, 1 listing, status and cleanup of `/tmp` probes). Read plus Grep plus Glob is 31, above the 15 checklist rows. Web research: none performed, so no Tavily call and no fallback to record.

**Why trust this review:** I read all four source files end to end, the three binding design ranges and spec ranges named in the brief, the 17 DF rows' text, and the reference script `poll-augment-review.sh:46-145`. A 0-finding report would have been wrong: F-01 reproduces on this host.

## Recommendations

- Fix F-01 before Gate A can pass (one `subprocess.run` argument and two `except` clauses, plus two tests). Then re-run G-1 for `tests/issue_watch/test_runner.py`.
- Fold F-03 and F-15 into the P6 work (they are cheap now and expensive after the cycle is written).
- Put F-04, F-08 and F-10 to the owner or the Open Questions list; they are design ambiguities, not coding slips.
- F-02, F-05, F-06, F-07, F-09, F-11, F-12, F-13 and F-14 are minor: record them, do not block on them. They are not re-checked in a later round.

## QA Complete

