# QA Report - Gate C, design-correctness lens (report only)

**Topic:** issue-watch implementation, Phases 6 and 7 (`cycle.py`, `cli.py`, `main.py` registration)
**Date:** 2026-11-08
**Phase:** doc-qualitative adapted to code (design-correctness lens, Step 7.G5)
**Fix cycle:** 1 (first review of Gate C). `fix_authorization: false`; no file other than this report was modified.

---

## Overall Verdict: FAIL

3 blocking findings (C-1 to C-3), 9 minor notes. Everything else in the lens list matches its binding source.

## Items Reviewed

Binding sources read in full for the cited ranges: `docs/designs/issue-watcher.md` 100-166, 224-225, 288-302, 304-388, 400-519, 523-533, 585-602, 638-649, 690-745, 747-764; `spec-final.md` 110-232 and 326-361; decisions DF-02, 03, 04, 06, 13, 17, 20, 22, 23, 25, 29, 41, 43, 45, 47, 50, 51, 52, 53, 55, 57 in `research/06-gap-fill-decisions.md`. Code read in full: `cycle.py` (1-1350), `cli.py` (1-339); supporting reads: `github.py` (105-205, 370-465, 555-640, 780-960), `record.py` (334-440, 495-810), `audit.py` (255-399), `launch.py` (grep of signatures).

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Order of the 15 steps and the exit of every failure | FAIL (C-1) | `_steps` (cycle.py:690-711) and `run` (661-681) follow D 342-358: config/enabled/approvers/worktree, lock, DISABLED, load + `next_permitted_at`, G1, origin, sweep, discovery, order, candidates, final save, health stamp, audit. Exit per reason comes from `audit.REASON_TABLE`. Defect: the cycle line reason of a clean exit-0 cycle (see C-1). |
| 2 | Precedence function | PASS | `resolve_exit` (447-458): first of 2, 6, 7, 5, 3, 4, then 75 only when it is the sole non-zero condition, else 0. Matches D 166 and S 328. `_cycle_reason` picks the first condition with the winning code. |
| 3 | S1 reading | PASS | `_candidates` (786-807) sets `halt` after any candidate that reached `_launch` (`c.launching`), including a launch-step skip; the loop breaks before reading or stamping later candidates. Claimed-by-marker candidates do not halt. Matches D 386-388 and DF-50. |
| 4 | `pending` written and saved before the launcher call | PASS | `_launch` 1041-1043: `mark_pending`, `_save()`, then `d.launcher.launch`. A failed save raises `_Stop("state_dir_unwritable")` before the call; `_commit` then skips the final write. |
| 5 | Re-read with its reserved calls | PASS | `_revalidate` (952-989): G7, G3' and G6' all `reserved=True` (3 calls); transient/timeout gives `_Transient` -> `failed` (`_fail`), other failure `revalidation_failed`, closed/label loss `revalidation_failed`, `{own, other}` -> `assigned_other`, empty -> `unassigned`, budget refusal -> `budget_exhausted` skip with no entry. `CallBudget.spend` (github.py:448-454) gives cap 32 for normal and 35 for reserved calls. |
| 6 | Day cap | PASS | `_day_cap_reached` (840-849) uses `record.day_cap_count` (half-open `(now-24h, now]` over every `consumed_at` plus `consumed_log`, record.py:689-703) plus shadow launches in dry-run; checked at step 10 and again in `_launch` before the pending write; `reset_entry` keeps `consumed_at` in `consumed_log`. |
| 7 | DISABLED check at the start and before the pending write | PASS | `_steps` 691-692 (`disabled`, exit 0, no store write); `_launch` 1025-1026 (`disabled_mid_cycle`, stamp, exit 0, no health stamp because `stop_reason` is set, `_commit_store` 1082). |
| 8 | Origin check at start and re-check | FAIL (C-3) | Start check 695-696 and re-check 1027-1028 are present and uncached (`_origin_ok`, 651-657). Defect: a call that the deadline forbids is reported as `origin_mismatch` exit 2. |
| 9 | 120 s launch cutoff and 240 s deadline | PASS with C-3 | `Deadline` (383-412): `timeout_for` returns None below 5 s left, `launch_allowed` is `elapsed() <= 120`; `_launch` 1029-1030 skips with `budget_exhausted` (not stamped, 804) before the pending write; launch timeout 120 s is never shortened (1043). Probe floor handled at 1009-1011. |
| 10 | Rate-limit persistence and clamp | PASS | G1: `rate_limit_wait` (github.py:418-431) gives `Retry-After` 1..3600 -> `rate_limited`, reset header within 3600 s, else now+3600 s `rate_limit_clamped` (cycle.py:731-735). Every other call: `_rate_stop` (644-649) persists now+3600 s with `rate_limit_clamped`. `_load` (722-724) exits 5 with zero gh calls before `next_permitted_at`. Earlier entries stand and examined stamps are kept because `_commit_store` still runs. |
| 11 | Dry-run rules | PASS | No `dispatch.json` write: `_load` saves a migration only when not dry-run (720), `_launch` returns before the probe (1002-1008), `_commit` routes to `_commit_shadow` (1065-1066) which writes `dry-run.json` only; shadow `considered` and shadow launches (1090-1106); unparseable shadow gives `dry_run_shadow_reset` warning (704-705); `enabled` ignored (664); rate limit honoured but not persisted; no health stamp; decision lines tagged `dry_run`, `state` None (620). |
| 12 | Config and approvers validation tables | PASS with notes M-2, M-3 | `load_config` (195-283) and `validate_approvers` (298-342) implement every row of D 127-149 including DF-13, DF-20 (comma, quote, leading dash), unknown keys, `type(v) is int` for ids, 20-digit and leading-zero rules, symlink, owner, group/other-writable, empty file. |
| 13 | Filesystem check | PASS | `fs_type_of` (146-175) and `_read_mountinfo` (178-184): field 5 mount point with `\040 \011 \012 \134` decoded in one pass, type after the `-` separator, longest prefix wins, later line wins ties, deny set equals D 69, unreadable mountinfo skips the check; one shared check in `load_config` for `once`, `check-config`, `init-state`, `status`, `reset` (DF-52, DF-53). |
| 14 | Five commands and their exit codes | FAIL (C-2) | Smoke run in a temp dir: `check-config` 0, `status` 6 then 1 after `init-state`, second `init-state` 6, `reset` refused 2, `reset --rate-limit` 0, config missing 2. Exactly five names. Defect: no crash path (see C-2). |
| 15 | `status` read-only behaviour and field set | PASS | `status_report` (1214-1279) opens `dispatch.json` with a plain `open`, stats `DISABLED`, returns exactly the eight fields of D 728-739; `stale` is `unknown` or `abandoned`+`pending_orphan` older than 24 h; `retry` argv is `launch_argv` plus `--retry-launch <id>` before `--json` (launch.py:119-131). `status` never takes the lock (cli.py:155-173). Smoke output confirmed exit 1 for a fresh store. |
| 16 | `reset` behaviour, one audit line per exit, never a cycle line | PASS | cli.py:273-339: usage errors before `state_dir` use `stderr_fallback("reset_refused", 2)`; lock first, then load, then entry check (`_reset_locked`); exits 0/2/6/75 each write one `warning` or `decision` line (`_write_reset`, 246-270), `state_dir_unwritable` stderr only; rotation only with the lock held. Smoke run: the audit file held exactly one line per reset exit and no `cycle` line from reset. |

## Summary
- Checks passed: 13 / 16 (checks 1, 8, 14 contain a blocking finding)
- Checks failed: 3
- Critical issues: 0
- Blocking issues: 3 (C-1, C-2, C-3)
- Issues fixed in-place: 0 (report only)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| C-1 | IMPORTANT (blocking: wrong audit behaviour, contradicts the task's own DF-41 rule) | `cycle.py:1108-1118` (`_cycle_reason`), `cycle.py:798-802` (`_issue_line(c, stop.reason)`); `tests/issue_watch/test_cycle.py:2022-2060` (`check_line_kinds`) | A clean exit-0 cycle writes a skip or entry reason on its `cycle` line: the last decision's reason (`launched`, `already_dispatched`, ...) or, when nothing was examined, `not_approved` (an idle queue is recorded as "not approved"). The candidate that stopped a cycle gets a `decision` line carrying a cycle-kind reason (`rate_limit_clamped`, `project_read_failed`, `orca_not_found`, `disabled_mid_cycle`, `origin_mismatch`). Step 6.6 of the task and DF-41 say the opposite: "a skip reason is never written on a cycle line and a cycle reason never on a decision line"; spec S 330 says a cycle reason sets the exit and a skip reason is per issue. The test helper `check_line_kinds` was rewritten to accept both uses (its docstring says so), so the DF-41 kind check no longer detects the behaviour. The Phase 6 task-log entry admits the departure. | Pick one and apply it in code and test: (a) add a [PROPOSAL] cycle-kind reason for a completed cycle (and, if wanted, per-issue stop lines) to `audit.REASON_TABLE`, update the name-count pin test, and write it on the cycle line; or (b) keep the closed table and restore the DF-41 check to its stated form, writing the stop reason only on the cycle line and a skip-kind line for the issue. In both cases restore `check_line_kinds` to the stated invariant. An owner decision on the new name is needed if (a) is chosen. |
| C-2 | IMPORTANT (blocking: missing required deliverable, FR-020) | `cli.py:117-128` (`once_command`), `cycle.py:1158-1166` (`run_cycle`); no `except Exception` anywhere in `cycle.py`, `cli.py` or `audit.py` (grep) | FR-020 and D 722 say a crash writes one JSON line to stderr (`audit.stderr_fallback`). Nothing catches an unexpected `Exception` from `run_cycle`, so a bug (for example a `ValueError` from a `record.mark_*` guard after Orca was started) ends the process with a Python traceback and exit 1, which is not in the exit table (S 316-326) and leaves no JSON line. The lock is released by the context manager, so no data is lost, but the operator contract is broken and `status` is the only signal. `stderr_fallback` is currently used only for config exits and `state_dir_unwritable`. | In `once_command` wrap `cycle.run_cycle(...)` in `except Exception`, call `audit.stderr_fallback(<closed reason>, <exit>)` and exit with a code from the table (the spec names no crash reason; choose and record one as a [PROPOSAL], for example exit 7 is wrong because no entry state is known, so owner confirmation is needed). Never catch `SystemExit` or `BaseException` (keeps the crash-injection tests valid). Add a test with a store whose `save` raises `RuntimeError`. |
| C-3 | IMPORTANT (blocking: wrong exit code and reason under a specified condition, FR-029 and D 647-649) | `cycle.py:651-657` (`_origin_ok`), `cycle.py:1027-1030` | `_origin_ok` returns False when `deadline.timeout_for` is None (fewer than 5 s left, so the call is not started) and when `check_origin` fails for any reason, and both become `_Stop("origin_mismatch", stamp=True)`, exit 2. The re-check sits before the `launch_allowed()` test. When the 3 reserved re-read calls run into the 240 s deadline (each up to 20 s, possible on a slow `gh`), the cycle ends with exit 2 `origin_mismatch` and a decision line of that name, although no git call was made and the origin was never compared. FR-029 and D 647 require the step to end with no entry and a `budget_exhausted` decision line, exit 0. An operator paged with exit 2 will check the remote, not the network. | In `_launch`, test `deadline.timeout_for(GIT_TIMEOUT_S) is None` (and `launch_allowed()`) before the origin re-check and raise `_Skip("budget_exhausted")`; keep `origin_mismatch` for a completed comparison that failed. Same split in step 6 (`_steps` 695-696). Add a test with a `FakeClock` advanced past 235 s between the re-read and the origin check. |

### Minor notes (carried forward, never rechecked)

| # | Location | Note |
|---|----------|------|
| M-1 | `cycle.py:352-358` (`validate_setup`) | Checks the worktree before the approvers file; FR-001 (S 115) orders approvers file first, then worktree. When both are invalid the audit reason is `worktree_invalid` instead of `approvers_invalid`. Same exit 2. |
| M-2 | `cycle.py:257-259` | A relative `worktree` or `approvers_file` gives `config_invalid`; the D 135-136 rows name `worktree_invalid` and `approvers_invalid`, and D 344 lists "worktree absolute and a directory" under the worktree reason. Same exit 2; the test `worktree_relative` pins the current reason. |
| M-3 | `cycle.py:320-325` | `validate_approvers` compares `lstat` and then opens with `O_NOFOLLOW` but does not `fstat` the opened descriptor, so owner and mode are not rechecked on the file actually read (narrow race). `check-config` also validates the file twice (`validate_setup`, then `approvers_summary`). |
| M-4 | `cycle.py:751-766`, `cycle.py:803` | An entry swept to `pending_orphan` and then examined in the same cycle gets two decision lines; FR-020 says each examined issue adds exactly one. |
| M-5 | `cycle.py:1206-1211` | `status` prints the bare Orca name in the retry argv (documented as OQ-50); D 741 says the first `_ORCA_CLIS` name "resolved with `shutil.which`". |
| M-6 | `cli.py:300-304` | `reset --rate-limit --forfeit-guarantee` (no ISSUE) is accepted and the flag ignored; the design is silent and the task log lists it as untested. |
| M-7 | `cli.py:155-173`, `record.py:425-431` | `disabled_since` catches only `FileNotFoundError`; a `PermissionError` on `DISABLED` would escape `status` as a traceback. |
| M-8 | `cycle.py:854-867`, `cycle.py:911-913` | The owner check (`assigned_other`/`unassigned`) runs after the day-cap check, so at the cap a non-owned issue is reported `day_cap`. Harmless; no launch either way. |
| M-9 | `docs/designs/issue-watcher.md:177, 759` | The design still says "six verbs"; DF-06 corrected this to five commands in code and tests. Design text only, outside this change set. |

## Actions Taken
None (report only). The only file written is this report. One smoke run executed the real CLI in a private `/tmp` directory (removed afterwards); its `once --dry-run` step reached the machine's real `gh api user`, a read-only call, and stopped at `origin_mismatch` because the temp worktree is not a git checkout.

## Inherited Structural Verdict - Reliance Audit (PR-04, INV-019)

No `## Inherited Structural Verdict` section was supplied in the spawn prompt, so there was no rf-qa PASS list to rely on; standalone behaviour applied and every check above was verified from source.

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- None. No inherited structural verdict was passed; nothing was skipped on reliance.

**(b) Independent semantic checks (>=1 required, INV-019):**
- Step order and exit mapping verified by reading `cycle.py:661-711` against D 342-358 and S 315-358.
- Cycle-line reason semantics verified by reading `_cycle_reason` (1108-1118) and `check_line_kinds` (test_cycle.py:2022-2060) against Step 6.6/DF-41 wording; found the departure (C-1).
- Crash path verified by grep for `except (Exception|BaseException)|crash` in `cycle.py`, `cli.py`, `audit.py` (no hits) and by reading D 722 / S 184 (C-2).
- Deadline/origin interaction verified by reading `Deadline.timeout_for` (399-408), `_origin_ok` (651-657) and `_launch` (1009-1030) against D 638-649 (C-3).
- CLI behaviour verified by running `check-config`, `status`, `status --json`, `init-state` (twice), `reset` in five forms and `once --dry-run`/missing-config against a temp state directory and reading the resulting `audit.jsonl`.
- Config and filesystem tables verified row by row against `load_config`, `validate_approvers`, `fs_type_of`.

## Recommendations
- Fix C-1 (decision needed on a completed-cycle reason), C-2 and C-3, then re-run `uv run pytest tests/issue_watch/ -v` and the pinned ruff checks. Do not weaken any assertion.
- Minor notes M-1 to M-9 are not rechecked in later rounds.

## Confidence

**Confidence:** Verified: 16/16 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (verification, not defect-free: 3 of the 16 verified checks failed)
**Tool engagement:** Read: 22 | Grep: 8 | Glob: 0 | Bash: 7 (one batch of CLI smoke runs; read-only listings and greps)
Web research: none; Tavily not used.

## QA Complete
