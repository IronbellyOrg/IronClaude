# QA Report - Source Fidelity Gate, Agent 2 of 3 (spec-fidelity)

**Topic:** issue-watch implementation vs `.dev/brainstorms/20261107-064825-github-issue-watcher/spec-final.md` (515 lines, read in full)
**Date:** 2026-11-08
**Phase:** report-validation (source-fidelity, report only, `fix_authorization: false`)
**Fix cycle:** 1 (first review of this gate)
**Lens:** spec-fidelity
**Output under review:** the change set of `phase-outputs/reports/final-change-set.md` (9 source files, `main.py` registration, 21 test files, 19 fixtures, `docs/designs/issue-watcher-setup.md`)

---

## Overall Verdict: FAIL (blocking: 1, minor: 8)

One blocking finding (M2-1: the cycle line omits the clock offset that the spec says it records every cycle). Everything else I could check against the spec is implemented as written or is a listed, evidenced departure (DF-nn, OQ-nn, Gate C `cycle_complete`/`cycle_crashed`). I did not find 15 errors. I report what I found; I did not pad the list.

## Findings (numbered; blocking first)

| id | severity | spec lines | implementation location | expected versus actual |
|---|---|---|---|---|
| M2-1 | BLOCKING | S 100 (Section 3 "Claimed"); design D 715 agrees (`clock_skew_s` is "yes" on the cycle line) | `src/superclaude/cli/issue_watch/cycle.py:751-756` (`_login_step` sets `self.clock_skew_s` only inside `if skew > SKEW_WARN_S`); `audit.py:164-165` (`clock_skew_s` optional on the cycle line); `tests/issue_watch/test_cycle.py:1710` (`assert "clock_skew_s" not in _the_cycle_line(lines)` for skew 0, 59, 60, -60) | Spec: "The cycle line records the offset between the local clock and the `Date` header of the `gh api user --include` reply, and an offset above 60 s [PROPOSAL] writes a `clock_skew` warning line." Two separate duties: (1) every cycle line records the offset, (2) above 60 s a warning line is added. Actual: only duty (2) exists; at 60 s or less the offset is dropped, so an operator cannot see a drifting clock before the warning threshold, and the test pins the omission. DF-22 (the only decision touching this) authorizes the 60/61 s boundary tests and the warning reason, not dropping the cycle-line field. Fix: set `clock_skew_s = int(round(skew))` whenever the `Date` header parses, keep the warning guarded by `> 60`, and change the test at 1710 to assert the value is present. |
| M2-2 | minor | S 157 (FR-014), S 289 (transition row 5) | `launch.py:36` and `:332` (`outcome_of`: id must fullmatch `^[A-Za-z0-9._:-]{1,128}$`, else `operation_id_invalid` gives `unknown`); `predicates.py:57` | Spec: confirmed success is "exit 0 and JSON whose operation ID is a non-empty string". Actual: a non-empty id outside that character set is recorded `unknown` (exit 7, no retry command in `status`). Direction is fail-closed (at-most-once holds, `unknown` can still move to `claimed`) and the pattern comes from design 9.2 to keep the printed retry command shell-safe, so no safety loss. Not in the 29 departures; the owner should confirm the pattern against a captured id in FU-1. |
| M2-3 | minor | S 102-105 (Eligible issue: "first failure is the skip reason", GitHub checks in the order open, tagged, owner, approved, not claimed, ...) | `cycle.py:922-928` (`_examine` reads comments (G4) before events (G3) and before the approval test) | A candidate whose comments cannot be read is skipped `marker_unreadable` even when it is also not approved, where the spec order gives `not_approved` first (approved precedes claimed). It also spends one call on every unapproved issue. Reason label only; no launch consequence. |
| M2-4 | minor | S 82 (Tagged: exact, case-sensitive name), S 102-105 (open) | `predicates.py` (no `is_tagged` or `is_open` predicate); `cycle.py:896-942` (`_examine` never tests `c.issue.labels` for the trigger or `c.issue.state`) | "Tagged" and "open" rely on the server-side filters of the discovery argv (`--state open --label`), and `gh issue list --label` matches case-insensitively. A label differing only in case therefore reaches `_examine`; it then fails closed, but under `events_incomplete` (no trigger event with the exact name, OQ-38) instead of "matches nothing". `_revalidate` does test the exact trigger name. Outcome (no launch) is right. |
| M2-5 | minor | S 231 (NFR-014: "every time read goes through the clock") | `audit.py:396` (`stderr_fallback` calls `datetime.datetime.now` when `ts` is None; used by `cli.py` `_config_exit`, `_refuse_reset`, the crash path); `runner.py:89,110,120,129` (`time.monotonic` for `duration_s`) | Wall-clock and monotonic reads outside the `Clock` Protocol. `audit.py` documents it as "a stamp, not a decision" and none feeds a decision, so behaviour is unaffected; the NFR sentence is not met literally. |
| M2-6 | minor | S 227 (NFR-012 "*Test:* dependency list unchanged") | `phase-outputs/reports/ac-trace.md` NFR-012 row: "Gate-only (no test)" | The only proof is the one-off `git diff --exit-code pyproject.toml Makefile` of gate G-10. There is no durable test. The register states this openly, so it is a coverage gap, not a false claim. |
| M2-7 | minor | S 361 (Tests; FR-009 contract test) | `tests/issue_watch/test_marker_contract.py:22-39` | The contract test also reads `~/.claude/skills/sc-issue-protocol/...` when that folder exists, so the result depends on the host's installed copy (an old install without the marker fails the test on that machine). The two `src/` copies the spec names are checked unconditionally. |
| M2-8 | minor | S 330-358, S 336 | `audit.py:261-285` (`line()` checks the reason for table membership only; the line kind is chosen by the caller) | The schema accepts a cycle-kind reason on a decision line and a skip reason on a cycle line. The spec says only that a value outside the table fails the schema, which holds. Noted because AC-14 is described as a schema check. |
| M2-9 | minor | S 185 (FR-020 GWT: "each examined issue adds exactly one decision line") | `cycle.py:758-773` (`_sweep` writes a `pending_orphan` or `claim_not_observed` decision line) plus `_candidates` (a second line for the same issue; `test_cycle.py:2567-2570` expects two lines for issue 9) | A swept issue that is also discovered gets two decision lines in one cycle. The spec ties "one line" to examined issues and lists `pending_orphan` as an entry reason, so I read this as consistent; flagged for the owner because the GWT wording is literal. |

## Coverage table by FR / NFR id

"Code" = I read the implementing code against the spec sentence. "Test" = what I verified about the proof: R = read the assertions, N = confirmed by grep that the traced test exists (name only; assertions not read, so this is not full verification). Departures cite the register id.

| id | Code | Test | Note |
|---|---|---|---|
| FR-001 | match | R | order in `cycle.py:663-718` equals S 115; two-call idle GWT pinned |
| FR-002 | match | N | login regex, `account_id_mismatch` before other calls (`_login_step`) |
| FR-003 | match | N | argv `github.py:180-198` equals the S 121 literal incl. `-L 100`; warning at `>= 80` |
| FR-004 | match | N | `github.discover` `>= 100` and repeated number |
| FR-005 | match | N | `predicates.approval_of`; OQ-38 and OQ-37 are listed |
| FR-006 | match | N | latest `labeled`, ties and repeated id give `events_incomplete` |
| FR-007 | match | N | `project_check`, `scope_missing` gives exit 3 `project_read_failed` |
| FR-008 | match | N | `is_intended_owner` exact set |
| FR-009 | match | R | marker window incl. 300 s tolerance; test seeds `pending_at - 301 s` |
| FR-010 | match | N | `_launch` saves `pending` before `launcher.launch` |
| FR-011 | match | N | G7, G3', G6' with 3 reserved calls; transient gives `failed` |
| FR-012 | match | R | `type(n) is int`, 1..999999999; edge list in `test_security_invariants.py:125` |
| FR-013 | match | N | 12-element argv; `find_orca` mirrors `_find_orca` (it adds an absolute-path guard and a stricter `topics` shape test, comments cite DF-36/DF-54; not on the 29 list but behaviour-neutral for a real Orca) |
| FR-014 | match | N | step order equals S 157; M2-2 on the id pattern |
| FR-015 | match (X2) | N | DF-50 X2: full-argv retry in `status` |
| FR-016 | match (X1) | R | S1 reading accepted (Q1, design 386) |
| FR-017 | match | N | `O_NOFOLLOW`, regular file and owner test, dev/inode and `st_nlink` test |
| FR-018 | match | N | checked after the lock and again before `pending` |
| FR-019 | match | N | shadow file, no Orca call, sweep reported not written; OQ-39 listed |
| FR-020 | match | N | M2-9 note; rotation 5 MiB, 4 files, only under the lock |
| FR-021 | match (X4, X5) | R (skew) | 900 s, stale 24 h, retry list |
| FR-022 | match | R | shared-failure table `test_cycle.py:1569-1598` |
| FR-023 | match | N | stamping, pruning, shadow map |
| FR-024 | match | N | half-open window, `consumed_log` kept through `reset` |
| FR-025 | match | N | start and pre-`pending` re-check; copied parser rules equal `origin_repo.py:65-99` (read) |
| FR-026 | match (DF-06, DF-57) | N | five commands; exit codes per register |
| FR-027 | match | N | validator reads as S 193; `enabled` false gives `not_enabled` |
| FR-028 | match (X3, DF-51) | N | clamp 3600; per-issue limits always clamp (design C22, OQ-32) |
| FR-029 | match | N | 240 s, 5 s floor, 120 s cut-off, 120 s launch timeout |
| NFR-001 | match | R | property test over `random.Random(331)` (DF-12) |
| NFR-002 | match | R | `classify_argv` allows exactly the S 207 forms |
| NFR-003 | match | R | no `SuperClaude-Org`, no `{owner}` asserted per argv |
| NFR-004 | match | N | `TypeError` on non-list argv; AST test exists |
| NFR-005 | match (DF-15) | R (50-cycle), N (rest) | `test_fifty_cycles` read; account-rename case = `...another_login...df47_nfr005` |
| NFR-006 | match | N | no text keys; 59-name pin (57 + `cycle_complete`, `cycle_crashed`) |
| NFR-007 | match | R | table at `test_cycle.py:1569`; a login reply that is not JSON is not a row of that table; I did not locate its test (not verified, see Unchecked) |
| NFR-008 | match (DF-55) | N | 20 s, 120 s, 240 s |
| NFR-009 | match | N | `CallBudget` 32 + 3 reserved, 2 shared |
| NFR-010 | match | R | `test_second_once_launches_nothing` |
| NFR-011 | match (DF-17) | N | mode 0600/0700, exit 6 cases, in-memory migration |
| NFR-012 | match | none | M2-6 |
| NFR-013 | match | N | four numbers; `disabled_mid_cycle` is not excluded from (b), the spec excludes only DISABLED and `not_enabled` |
| NFR-014 | match | N | M2-5; four Protocols; no `select` module |

### Reason table (S 330-358)

Counted the spec rows: 52 names. `audit.REASON_TABLE` (`audit.py:26-102`) holds 59: the 52 with the kind and exit of the spec (checked row by row: exit 2 x7, exit 6 x5, exit 3 x5, exit 4 x2, exit 5 x2, exit 75 x1, exit 0 cycle x3, skips x15 with `marker_unreadable` and `edits_unreadable` added, entries `prompt_invalid` and `revalidation_transient` 7, `attempts_exhausted` 0, `spawn_error` 7, `launch_unknown` 7, `pending_orphan` and `claim_not_observed` 0, `launched` and `claimed` 0, `re-approved` note, `discovery_count` and `clock_skew` warnings) plus `marker_unreadable`, `edits_unreadable` (DF-02), `operator_reset` (DF-03), `dry_run_shadow_reset` (DF-22), `reset_refused` (DF-57), `cycle_complete`, `cycle_crashed` (accepted Gate C proposals). No spec name is missing and no kind or exit differs.

### Security model T1 to T13, T16, T17

T1 (prompt boundary), T2/T3 (allow-list, `User`, `[bot]`), T4 (`unchanged_since`), T5 (`REPO` literal), T6 (`shell=False`), T7 (`host`, `login` on every line), T8 (`created_at` floor, exit 6), T9 (GET only), T10 (no permission flag in the 12-element argv; gate in the runbook section 14), T11 (500-byte stderr cap, restricted audit keys), T12 (caps), T13 (approvers validator), T16 and T17 (runbook section 13; probe accepts only the `orca-cli` topic) are each present in code or runbook as written.

### Runbook steps 1 to 10 (S 384-395)

Step 1 = runbook 1.1 to 1.4; 2 = section 4; 3 = section 7; 4 = section 9; 5 = sections 10, 11; 6 = section 12 (900 s); 7 = section 5; 8 = section 6; 9 = sections 8.1 to 8.6 (shadow review, two-process lock test, persistence check, alert, live-test record, then `enabled`); 10 = section 13. Kill switch, exit-code table (all of S 317-326 plus code 1), reason table (59 names), recovery (`reset`, move-aside), follow-ups FU-1 to FU-12 and risks R10 to R18 are present. I found no runbook statement that contradicts the code (checked: exit 6 on `init-state` refusal, `lock_missing` before `init-state`, `not_enabled` before the lock, `status` exit 1, `cycle_complete` wording).

## Items reviewed (the four checks of the prompt)

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Semantic coverage: every FR, NFR and GWT is satisfied by code and proven by a real test | FAIL (1 blocking) | Code read for all 29 FR and 14 NFR; M2-1 is the one unmet sentence. Test assertions read for 12 ids only (table above, column "Test"); the other 30 rest on test names plus `ac-trace.md` |
| 2 | Detail preservation: reason names, kinds, exits, precedence, windows, caps, timeouts | PASS | Row-by-row compare of S 332-358 against `audit.py:26-102`; constants compared in `cycle.py:34-47`, `github.py:40-49,376`, `record.py:31-35,434-444`, `audit.py:106-107`, `launch.py:36,56` |
| 3 | Phantom coverage: no FR or NFR claimed only by id | PASS with notes | 14 test names from `ac-trace.md` located by grep, all exist; NFR-012 is gate-only (M2-6) |
| 4 | Compliance and operational completeness: T1-T13, T16, T17, kill switch, audit schema and rotation, runbook steps 1 to 10 | PASS | Section above; runbook read in full (651 lines) |

## Summary

- Blocking findings: 1 (M2-1). Minor findings: 8 (M2-2 to M2-9). No finding asks to undo one of the 29 authorized departures; the S1 reading (Q1), 3600 s clamp (Q3), OQ-36 to OQ-51 and the Gate C reasons were treated as accepted.
- Why not 15: the code follows the spec closely and the one place it does not (M2-1) is also what the design says. I looked for more in the event/approval logic, the transition table, the budget arithmetic, the time windows, the exit precedence, the lock protocol, the dry-run rules, the rate-limit path and the runbook, and found only the minor items above. This is a statement about what I checked, not a proof of absence: see Unchecked.
- Fix needed for PASS: M2-1 only (about 6 lines in `cycle.py` plus the test at `test_cycle.py:1700-1710`, and the 60 s/-60 s cases then assert the offset is present).

## Confidence (Confidence Gate Protocol)

- **Confidence:** Verified: 13/43 | Unverifiable: 0 | Unchecked: 30 | Confidence: 30.2%. Unit = one FR or NFR id. "Verified" = I read the implementing code AND the test assertions (the 12 ids marked R in the coverage table, plus NFR-012, which has no test by design, M2-6). "Unchecked" = the 30 ids marked N: the code was read and matches the spec, but the proving test was only located by name or taken from `ac-trace.md`, which is reliance, not verification. This is below the 95% bar, so a PASS verdict would not have been allowed; the verdict is FAIL on the blocking finding in any case, and the low figure measures test-assertion depth, not code conformance (all 43 ids were read at code level).
- **Tool engagement:** Read: 28 | Grep: 28 | Glob: 0 | Bash: 1 (one `sed -n` to print a long decision row). Every call targeted a specific spec item, source file, test or decision row cited above.
- **Unchecked ids (assertions not read):** FR-002 to FR-008, FR-010, FR-011, FR-013 to FR-015, FR-017 to FR-020, FR-023 to FR-029, NFR-004, NFR-006, NFR-008, NFR-009, NFR-011, NFR-013, NFR-014. In a second round I would read the assertions first for FR-007 (scope), FR-011 (re-read), FR-014 (outcome table), FR-028 (rate limit) and NFR-011 (store faults).
- **Not run:** `uv run pytest tests/issue_watch/` was not re-run by me (it writes caches into the worktree; experiments are limited to `/tmp`). The 2628-pass result is the Final-gate record, which I did not independently reproduce.
- **Could hide undetected issues:** the unverified GitHub/Orca reply shapes (all `_assumed_shape`, accepted as OQ-42); per-test assertion strength for the Unchecked ids; behaviour of `write_prepared_bytes` beyond `mkstemp` (0600 by construction).

## Self-audit

Question asked before the verdict: "If I told the owner I found 0 issues, would they believe me?" I am not saying that: M2-1 is a concrete, line-cited miss, and the 8 notes are real but small. Evidence of checking is the file:line columns above and the row-by-row reason-table compare.

## QA Complete


