# QA Report - Gate A, security-invariants lens (Phases 2 and 3)

**Topic:** issue-watch implementation (runner.py, predicates.py, audit.py, github.py and tests)
**Date:** 2026-11-07
**Phase:** task-qualitative (security-invariants lens, content QA of produced code)
**Fix cycle:** N/A (first review; fix_authorization: false, report only)

---

## Overall Verdict: FAIL

Four blocking findings (B-1 to B-4). Everything else is minor and listed as notes. The prompt asked me to assume at least 15 errors; I did not find 15 distinct real errors. I found 4 blocking and 14 minor, and I list only what I could show with a tool call.

## Items Reviewed

One row per invariant in the prompt. `drift-axis-inactive` applies (see Summary).

| # | Invariant | axis | Result | Evidence |
|---|-----------|------|--------|----------|
| 1 | Only a validated integer (`type(v) is int`, 1..999999999, bool fails) becomes an issue-number argv element | none | PASS | `predicates.py:45-47` `valid_issue_number`; `github.py:109-113` `_issue_arg` is the only place an issue number is rendered (`github.py:165, 194, 216`); `_page_arg` `github.py:116-120`. `test_github.py:276-285` covers 0, -1, True, "42", None, 1.0. `discover` re-checks at `github.py:768-769`; `reread` at `github.py:892`. Probe: `discover` with 1.0, "5", True, 10**10 all returned `gh_non_json`. (B-4 covers the non-number argv inputs.) |
| 2 | Every repo-scoped argv and both GraphQL constants name IronbellyOrg/IronClaude literally; none has SuperClaude-Org or `{owner}` | none | PASS | `github.py:35, 73, 87, 165, 216`; Grep of `src/superclaude/cli/issue_watch` for `SuperClaude-Org\|\{owner\}\|mutation` returned no match; `test_github.py:226-232, 268-273` assert it. |
| 3 | Poller only reads: REST calls carry `--method GET`, GraphQL has no mutation, no argv writes | none | PASS (with note M-2) | G3, G4, G7 carry `--method GET` (`github.py:160-164, 211-215`); G1 `gh api user --include` has no parameters, so gh uses GET. Both query constants start with `query(` and contain no `mutation`. The prompt's literal wording "every REST path call carries --method GET" is false for G1; the design exempts G1 (`docs/designs/issue-watcher.md:554`) and `test_github.py:204-213` skips it. See M-2. |
| 4 | No argv asks for title, body or comment body; marker is a jq boolean | none | PASS | `github.py:52-66, 72-101`: projections list no title or body field; `MARKER_JQ` is the only `body` use and wraps it in `contains(...)`; `_marker` requires `type(marker) is bool` (`github.py:682-683`). `test_github.py:254-265` checks every argv element. |
| 5 | `SubprocessRunner` rejects a str argv and always passes `shell=False` | none | PASS | `runner.py:78-79, 85`; `test_runner.py:57-80`. Grep `shell=True\|os.system` in src: no match. (Other raise paths are B-3.) |
| 6 | stderr capped at 500 bytes by bytes; exception message text never reaches a `CommandResult` | none | PASS (with B-3) | `runner.py:56-63` encodes then slices bytes, `errors="ignore"`; `test_runner.py:104-123`. `OSError` gives only `type(exc).__name__` (`runner.py:109`), `test_runner.py:149-160`. The exception text does not reach a result, but non-OSError exceptions escape instead (B-3). |
| 7 | Audit builders accept only typed scalar fields and the closed key set; no title, body, label name, rate_remaining or stderr text can become a key | AX-5 | FAIL (keys are closed; the "no issue text can reach a line" claim is false) | Key set is closed (`audit.py:146-162, 207-211`); probe: `line("cycle", kind=...)` raises `TypeError` (multiple values for `kind`), so `kind` cannot be overridden. But values are free text: B-2. |
| 8 | Unreadable, incomplete or null evidence never counts as positive (approval, marker, edits, project items) | AX-2 | FAIL | Approval, marker, project items, events: fail closed (probe: login-less marker dropped; non-bool marker malformed; wrong-number reread rejected). Edits: an ABSENT `lastEditedAt` key is read as "never edited" and `unchanged_since` returns None (B-1). |
| 9 | Approval rules reject bots, non-User actors, outsiders, stale and reversed approvals | none | PASS (with M-6) | `predicates.py:196-203` (type, `[bot]` suffix, None login/id, id not in approvers); `:192-195` later unlabel voids; `:208-211` before trigger / before init; `:185-189` same-second ties fail closed. `test_predicates.py:121-261` covers outsider, Bot, `[bot]`, relabel by outsider, unlabeled after approval, tie ordering. |
| 10 | Dependency leaf rule (runner, predicates, audit import nothing from the package) | none | PASS | Import blocks of `runner.py:8-13`, `predicates.py:7-11`, `audit.py:9-16` are standard library only; `github.py:20-33` imports only `.predicates` and `.runner`. |

## Summary
- Invariants passed: 8 / 10 (rows 7 and 8 fail)
- Blocking findings: 4 (B-1 to B-4)
- Minor notes: 14 (M-1 to M-14)
- Critical issues: 0 (no path found that launches on a forged approval; B-1 is the closest)
- Issues fixed in-place: 0 (fix_authorization: false)
- Axis lens status:
drift-axis-inactive

(The prompt carried no BUILD_REQUEST.GOAL verbatim, so AX-1 was disabled. AX-2 to AX-5 were applied.)

## Issues Found (blocking)

| # | Severity | axis | Location | Issue | Required Fix |
|---|----------|------|----------|-------|-------------|
| B-1 | IMPORTANT (blocking) | AX-2 | `github.py:694-706` (`_edit_issue`, `_comment_edit`) feeding `predicates.py:229-239` (`unchanged_since`) | The edit-evidence parsers use `d.get("lastEditedAt")` and `_opt_time`, so a reply where the key is MISSING gives the same result as an explicit null: "never edited". Probe: a G5 reply with no `lastEditedAt` on the issue or on another user's comment returned `Read(value=EditEvidence(... last_edited_at=None))` with `reason=None`, and `unchanged_since(...)` returned `None` (unchanged = positive). The invariant says null or incomplete evidence never counts as positive. The reply shape is marked UNVERIFIED in `github.py:69-70` (FU-1), so shape drift is the exact case this guards. `test_github.py` has no test for an absent key (Grep for `lastEditedAt` shows only explicit `None`, lines 853, 872, 911). | In `_edit_issue` and `_comment_edit` require the key to be present (`if "lastEditedAt" not in d: raise _Malformed`); keep explicit null as the only "never edited" value. Add tests: absent key on the issue, absent key on a comment, both give `edits_unreadable`. |
| B-2 | IMPORTANT (blocking) | AX-5 | `audit.py:4` docstring; `audit.py:165-184, 187-196, 260-289`; design `docs/designs/issue-watcher.md:223, 701-718` | The claim "The builders accept only typed scalar fields, so no issue text can reach a line" (design line 223: "Never: contain issue text") is false. `_TYPES` only checks `str`, so `host`, `login`, `cycle_id`, `ts`, `approved_at` and `state` take any string. Probe: `decision_line(host="stderr text HTTP 401", state="Title: secret", approved_at="not a time", ...)` was accepted and returned those values. The design table says `state` is an enum, `cycle_id` is `uuid4().hex`, `ts` and `approved_at` are UTC strings. `issue` is unbounded too: `decision_line(issue=-5)` was accepted. `test_audit.py:163` tests forbidden KEYS only, never forbidden values. A caller that passes a title, label name or stderr text as `state` or `host` writes it to the audit file. | Validate values, not just types: `state` against the closed entry-state set; `ts` and `approved_at` against `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$`; `cycle_id` against `^[0-9a-f]{32}$`; `host` and `login` against a short charset and length; `issue` against 1..999999999 (audit imports nothing, so repeat the range check). Add tests that a title-like string is rejected in each field. Or delete the false sentence from the docstring and design. |
| B-3 | IMPORTANT (blocking) | AX-2 | `runner.py:83-91` (`subprocess.run(..., text=True)`, no `encoding` or `errors`), `runner.py:78-80`; contract at `github.py:722-725` | `SubprocessRunner.run` can raise instead of returning a `CommandResult`. Probes: a child writing bytes `\xff\xfe` to stdout, or `\xff` to stderr, gives `UnicodeDecodeError` out of `run`; an argv element containing NUL gives `ValueError`; an empty list argv gives `IndexError`. The timeout path decodes with `errors="replace"` (`runner.py:52`), so the two paths disagree. `github.py:724` promises "Every read returns a Read and never raises for a malformed reply"; `_call` (`github.py:533`) has no guard, so every typed read inherits the raise. NUL and empty values are reachable because `trigger`, `login` and the cursor reach argv unvalidated (B-4). The decoding also follows the locale, which is not pinned. The failure is closed (no launch), but a crash replaces the designed `gh_non_json` or `*_unreadable` skip. `test_runner.py` mocks `subprocess.run` and never feeds undecodable bytes. | Pass `encoding="utf-8", errors="replace"` to `subprocess.run`; catch `ValueError` next to `OSError` and return `spawn_error="ValueError"`; reject an empty argv with `TypeError`. Add tests with a real child writing invalid UTF-8 and with a NUL argv element. |
| B-4 | IMPORTANT (blocking) | AX-2 | `github.py:1-8` docstring; `github.py:123-155` (`_cursor_args`, `argv_discover`); `github.py:739-741` (`user`) | The module says "Every argv is built here from module constants", but three values enter argv with no content check: `trigger` and `login` (`--label`, `--assignee`, `github.py:147-150`) and the GraphQL cursor (`-f after=<cursor>`, `github.py:129`). `login` comes straight from the G1 reply (`user()` accepts any string) and the cursor from a GitHub reply. The cursor guard is "non-empty str"; `trigger` and `login` have none. `test_github.py` uses only benign values (`"sc:issue"`, `"owner-login"`, `"Y3Vyc29yOjE="`). The login regex is "the cycle's" (`github.py:730`) and `cycle.py` is not in this change set, so Gate A cannot show the check exists. Practical risk is low (list argv, no shell, `-f` is a raw field so `@file` is not expanded), but a comma in `trigger` silently turns the filter into an AND of labels, and NUL or empty values feed B-3. | Validate inside github.py so the module keeps its own invariant: cursor `^[A-Za-z0-9+/=_-]{1,200}$`; `trigger` non-empty, no comma, no NUL, no leading `-`; `login` GitHub login charset, max 39. Add hostile-value tests (comma, NUL, leading dash, empty, `@me`). Or reword the docstring to say which inputs are validated elsewhere. |

## Minor notes (do not fail the review, not rechecked later)

| # | Location | Note |
|---|----------|------|
| M-1 | `github.py:345-350` `_header_int` | `Retry-After` or reset header of more than 4300 digits raises `ValueError` from `int()` (probe 5). Real GitHub never sends it; wrap in try or cap the regex at 10 digits. |
| M-2 | `github.py:105-106` comment | "Every REST path call carries --method GET" is not true for G1 (`gh api user --include`, no parameters). Behaviour is read-only and design-sanctioned (design line 554). Reword the comment: "every REST path call that sends parameters". |
| M-3 | `github.py:537-538` `_failed` | `Read.retry_after_s` carries the raw header value (unclamped); only `rate_limit_wait` clamps to 3600. A consumer that uses `retry_after_s` directly could build an overflowing `timedelta`. Clamp at the source. |
| M-4 | `predicates.py:25-32` `parse_utc` | Docstring says any other input raises `ValueError`, but `strptime` accepts unpadded fields: `parse_utc("2026-1-5T1:2:3Z")` returned a datetime (probe 6). GitHub always pads, so fail-closed value is small; use a regex before `strptime`. |
| M-5 | `predicates.py:210` `approval_of` | A naive `store_created_at` raises `TypeError` (probe 7). Closed failure, but `approval_of` is the security predicate; check `tzinfo` and return `events_incomplete` or raise a clear `ValueError`. |
| M-6 | `predicates.py:196-203` | `actor_id` of `True` with `approvers={1}` returns approved (probe 8). Not reachable through `github.py` (`_pos_int` rejects bool, `github.py:477-481`), but add `type(approval.actor_id) is int` for defence in depth. Tests have no case for `actor_login=None`, `actor_type=None` or `actor_id=None` (`test_predicates.py:121-149` covers outsider, Bot, `[bot]`, removed label only). |
| M-7 | `predicates.py:185-189` | A same-second pair of approval on/off or approval/trigger events anywhere in history gives `events_incomplete` forever, even after a later clean re-approval. Fail closed, but permanent. Document it or limit the check to events at or after the last approval. |
| M-8 | `audit.py:117-126` `append` | No `O_NOFOLLOW` (the design uses it for the lock only), no `fsync` of the data, and a short write raises after the partial bytes are already on disk, so the next append glues onto a truncated line. Low likelihood. |
| M-9 | `audit.py:199-223` `line` | `exit` is not tied to `REASON_TABLE`: `cycle_line(exit_code=0, reason="gh_auth_failed")` was accepted (probe 4b), and a `cycle` line may carry a skip reason. The design table says `clock_skew_s` is required on a cycle line; the implementation makes it optional (`audit.py:151-152`). |
| M-10 | `audit.py:319-342` `stderr_fallback` | `exit_code` is not checked against the reason; `sys.stderr` being None raises `AttributeError`. |
| M-11 | `runner.py:69-91` | `timeout` is not validated (`None` means no limit) and `gh` is looked up on `PATH` by bare name; `stdout` is not size-capped. All come from the caller or the operator's environment, so low risk. |
| M-12 | `runner.py:83-91` | The child inherits the full environment, so `GH_HOST` or `GH_TOKEN` set in the operator's shell steer every call; no argv carries `--hostname github.com`. The literal repo name does not pin the host. Operator-controlled, so hardening only. |
| M-13 | `github.py:413-415, 514-534` | `_call` with `budget=None` counts nothing; G1 and G2 are counted only if the cycle remembers `spend_shared`. Design line 537 says every call is counted by `CallBudget`. The cycle is not in this change set; re-check at Gate B. |
| M-14 | `github.py:747-783` `discover` | The server-side filter is trusted: returned issues are not checked for `state`, the trigger label or the assignee. The FR-011 re-read and `approval_of` cover it later; a cheap local check would be belt and braces. Also a missing `gh` binary is reported as `gh_auth_failed` (design-sanctioned, `github.py:541-542`). |

## Actions Taken
None. fix_authorization was false and no file other than this report was written. The two probe scripts ran with `uv run python -I` from stdin and created no files.

## Inherited Structural Verdict - Reliance Audit (PR-04, INV-019)

No `## Inherited Structural Verdict` section was in my spawn prompt, so I ran standalone and relied on no rf-qa PASS item.

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- None. The change-set file `gate-a-change-set.md` lists gate results (183 and 373 tests passed, ruff, `make lint`, G-8 grep NO_MATCH). I did not re-run them and I treat them only as context, not as verification of any invariant here.

**(b) Independent semantic checks (>=1 required, INV-019):**
- Absent-versus-null evidence in edits: verified by a probe feeding `github.edits` a reply with no `lastEditedAt` key and then `unchanged_since` (result `None`); source `github.py:694-706`. The 373 passing tests did not catch it (Grep `lastEditedAt` in `test_github.py`).
- Free-text values in audit lines: verified by a probe calling `decision_line` with title-like `state` and `host` (accepted); source `audit.py:165-196`.
- Runner raise paths: verified by a probe with a real child writing invalid UTF-8, a NUL argv and an empty argv; source `runner.py:83-91`.
- `kind` override on `audit.line`: I suspected it from reading the code and the probe disproved it (`TypeError: multiple values for argument 'kind'`), so it is not a finding.
- Repo literals, `--method GET`, no mutation, no title or body field: verified by Grep over `src/superclaude/cli/issue_watch` (no `SuperClaude-Org`, `{owner}`, `mutation`, `shell=True`, `os.system`) and by Read of `github.py:35-101, 132-219`.
- Approval rules: read `predicates.py:165-214` line by line against `test_predicates.py:107-261`, and ran probes for a bool actor id, naive `store_created_at` and an approval label equal to the trigger label (gave `events_incomplete`, closed).

Claims independently checked: 31 (10 invariants, 7 design-table rows against `docs/designs/issue-watcher.md:218-223, 537-602, 697-722`, 14 probe outcomes). Files read: `runner.py`, `predicates.py`, `audit.py`, `github.py` (all), `test_github.py:55-295`, `test_runner.py` (all), `test_predicates.py:120-150` plus a test-name grep, `test_audit.py:160-220`, the design sections above, `gate-a-change-set.md`. I did not read all of `test_github.py` (1250 lines), `test_predicates.py` (629) or `test_audit.py` (640); I searched them with Grep for the security cases. If I had to report 0 findings the user should not believe it; I found 4 blocking ones by running probes rather than reading summaries.

Web research: none performed (no external lookup was needed); Tavily not used, nothing fell back.

## Recommendations
- Fix B-1 to B-4 (small, local edits in github.py, runner.py, audit.py plus tests), then re-review only B-1 to B-4.
- Take M-2, M-3, M-6 with the same pass since they are one-line changes. Carry M-13 to Gate B.

## Confidence
Verified: 10/10 invariants | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (of the 10 invariants in the prompt; this is not a claim that no other defect exists). The review is not PASS-eligible because blocking findings are open.
**Tool engagement:** Read: 15 | Grep: 8 | Glob: 1 | Bash: 2 (probes). Read plus Grep plus Glob is 24, above the 10 invariants.

## QA Complete

