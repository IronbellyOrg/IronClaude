# QA Report - Gate C, lens "design-correctness" (Phases 6 and 7)

**Topic:** issue-watch `cycle.py` and `cli.py` against `docs/designs/issue-watcher.md`, `spec-final.md` and decisions DF-02..DF-57
**Date:** 2026-11-08
**Phase:** task-qualitative (content lens: design-correctness), fix_authorization false
**Fix cycle:** 1 (first review of this gate)

---

## Overall Verdict: FAIL

blocking: 1, minor: 13. The one blocking finding (DC-1) is a real wrong exit code in a deadline corner; everything else I probed behaved as the design, spec and decisions say.

## Method

Read `cycle.py` (all 1350 lines), `cli.py` (all 339 lines), the binding design ranges, spec FR rows 115-201 and reason table 326-358, and the listed DF rows (DF-02, 03, 04, 06, 13, 17, 20, 22, 23, 25, 29, 41, 43, 45, 47, 50, 51, 52, 53, 55, 57). Read the `github.py`, `record.py`, `audit.py`, `launch.py` and `predicates.py` functions that `cycle.py` calls, so cross-module behaviour is judged on the real code. Then ran 7 probe scripts from `/tmp/gatec-probe/` (outside the repo, no repo file written) that drive `run_cycle` through the repo's own `GhWorld`, `FakeClock`, `FakeLauncher` and drive the five CLI commands through `click.testing.CliRunner`. Expected values in the probes were taken from the design and spec text, not from the code.

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run (15 cycle steps, order, exit of each failure) | AX-2 | FAIL | Order matches D 342-358 and FR-001 (`cycle.py:690-711`: disabled, load, user, origin, sweep, discover, order, candidates). Every shared-input failure maps to the right exit (probes 2, 6; `audit.REASON_TABLE`). One wrong exit: DC-1 (probe5: exit 2 `origin_mismatch` when the deadline ran out). |
| 2 | Convention compliance (module boundaries, `main.py` registration) | none | PASS | `main.py` diff is the DF-29 eager import after `reflect`; `cycle.py` imports only `audit github launch predicates record runner` (lines 27-31); no `subprocess`, no `except BaseException` (grep of `except` in `cycle.py`: only `OSError`, `ValueError`, `LockHeld`, `LockError`, `StoreError`, `ConfigError`, `_Skip`, `_Stop`, `_Transient`). |
| 3 | Intra-phase order simulation (pending saved before launcher, re-read before pending) | none | PASS | `_launch` (`cycle.py:999-1056`): probe, prompt, re-read, day cap, DISABLED, origin, cutoff, `mark_pending`, `_save()`, then `launcher.launch`. The `launcher.launch` call at line 1043 is the first statement after `_save()` returns, and `_save()` turns an `OSError` into `_Stop("state_dir_unwritable")`, so no launch can follow a failed pending write. |
| 4 | Function signature verification (`github.*`, `record.*`, `launch.*` calls from the cycle) | none | PASS | `github.user/discover/events/marker_comments/edits/project_items/reread` return `Read(value, reason, kind)`; cycle uses `.reason`, `.kind`, `.value` only. `record.sweep(doc, now)` and `day_cap_count(doc, now)` take a `StoreDoc` (DF-44). `OrcaLauncher.launch(orca, worktree, prompt, timeout)` matches the call at `cycle.py:1043`. |
| 5 | Module context / cross-symbol input shape | none | PASS | `cycle.validate_approvers`, `approvers_summary`, `validate_setup` all take a path to a regular file / directory consistently; `_read_store_doc` and `FileStore.load` agree on `dispatch.json` (both migrate in memory, both raise `store_missing`/`store_invalid`). `github._trigger_arg` is weaker than `cycle._label` (control chars, quotes), so no config-valid label can make `discover` raise. |
| 6 | Downstream consumers (audit lines, status, SLO reducer) | none | PASS | Probe 2/6 lines parse through `audit.line`; `slo_numbers` consumes only `kind/ts/reason/exit/issue/approved_at/dry_run`. `status_report` field set equals D 730-739 (eight fields, probe4 `--json`). |
| 7 | Verification validity (adapted: my probes assert literal values from the sources) | none | PASS | Probe expectations: 8 candidates then `budget_exhausted` for 15 skipping issues (D 384, k = 8), gh_calls 34 (15 skipping issues) and 9 (one launch: 2 shared + 4 reads + 3 reserved), 3600 s clamp on a per-issue rate limit. Test-file adequacy itself belongs to the test-adequacy lens and was not assessed here. |
| 8 | Primary use case end to end (adapted: whole cycle through `run_cycle`) | none | PASS | Probe 2 c1/c2: launch, then second candidate on the next cycle; probe 7: 15 eligible launches exactly 1 and stamps only candidate 1 (S1). |
| 9 | Error path coverage (config, approvers, store, lock, reset, init-state) | AX-3 | PASS (minor notes DC-M1..M5) | Probe3 (28 config and approvers inputs) and probe4 (13 CLI invocations). Only wording and ordering nits. |
| 10 | Runtime failure path trace (deadline, rate limit, disabled mid-cycle, origin) | AX-2 | FAIL | DC-1. Probes 2 (P6, P7, P8) and 5. |
| 11 | Completion scope honesty (Open Questions vs implementation) | none | PASS | OQ-36, 39, 41a, 49, 50 are declared and the code does what they say. `re-approved` is unreachable by design (OQ-49); not reported as a defect. |
| 12 | Ambient dependency completeness (registration, exports, reason table) | none | PASS | `uv run superclaude issue-watch --help` evidence in `p7-g9.txt`; `REASON_TABLE` has the 57 names and every reason the cycle raises (`cycle.py` `_cond/_stopped` arguments all appear in the table). |
| 13 | Kwarg sequencing | none | PASS | `Runner.run(..., *, cwd=None)` exists before `_LastResult.run` and `OrcaLauncher.launch` pass `cwd`; `github.events(..., reserved=)` exists before `_revalidate` passes it. |
| 14 | Existence claims verified | none | PASS | Grepped: no `fcntl`/`/proc` use at `cycle.py` import time (`_read_mountinfo` is a function, `fcntl` imported inside `FileStore.lock`); the change-set line counts (1350, 339) match `wc -l`. |
| 15 | Cross-reference accuracy (design/spec/DF citations in docstrings) | none | PASS | DF-13/20/23/41/53 cited in `cycle.py` match the rows read. |

Axis lens: AX-2 (contradiction between the plan text for step 12 and design section 8.5) fired once.

## Summary
- Checks passed: 13 / 15 (items 1 and 10 fail on the same finding, DC-1)
- Checks failed: 2
- Critical issues: 0 (1 blocking, graded IMPORTANT)
- Issues fixed in-place: 0 (report-only)
- Axis lens status:
drift-axis-inactive

## Issues Found

### Numbered findings table

| id | severity | file | evidence | expected versus actual |
|---|---|---|---|---|
| DC-1 | blocking (IMPORTANT) | `src/superclaude/cli/issue_watch/cycle.py:1027-1030` and `:651-657` | Probe `/tmp/gatec-probe/probe5.py`: one eligible issue, a scripted clock jump of 236 s during the reserved `items` re-read. Result: `EXIT 2 REASON origin_mismatch`, decision line `origin_mismatch` for issue 1, no entry. `git remote get-url` was never run; `_origin_ok()` returns False because `Deadline.timeout_for(10)` is None with under 5 s left. | Expected (D 647, FR-029, plan step 6.2 item 12 "launch cutoff"): once the budget is spent the launch step ends with no entry and a `budget_exhausted` decision line, exit 0. Actual: exit 2 with a false `origin_mismatch` reason, which tells the operator to fix the worktree origin when only time ran out. The cause is order: `_origin_ok()` runs before `deadline.launch_allowed()`. Fix: test `launch_allowed()` first, or map a None origin timeout inside `_launch` to `_Skip("budget_exhausted")`; keep the exit-2 mapping for the cycle-start check. Add a test with a 236 s jump before the origin re-check. |

### Minor notes (carried forward, never block)

| id | file | note |
|---|---|---|
| DC-M1 | `cycle.py:352-358` | `validate_setup` checks the worktree before the approvers file. FR-001 and D 344 list approvers first. With both bad the reason is `worktree_invalid`, not `approvers_invalid`; the exit is 2 either way. The plan item 6.1 wording matches the code. |
| DC-M2 | `cycle.py:257-259` | A relative `worktree` or `approvers_file` gives `config_invalid`; D 135 and D 136 name `worktree_invalid` and `approvers_invalid` for those rows. Exit 2 either way (probe3). |
| DC-M3 | `cycle.py:135` | `_label` also rejects a leading dash on the approval label. DF-20 lists only `,` and `"`. The approval label never reaches an argv, so the extra rule refuses a valid GitHub label for no safety gain (it is justified for the trigger label, which `github._trigger_arg` also guards). |
| DC-M4 | `cli.py:300-304` | `reset --rate-limit --forfeit-guarantee` (no issue) is accepted and the flag is ignored (probe4: exit 0 "rate limit cleared"). D 121 lists only the two forms; an unneeded flag is silently dropped. |
| DC-M5 | `cycle.py:84-88`, `:218-220`, `:237-239`, `cli.py:79` | The `ConfigError` docstring says `detail` never holds a value read from the file, but unknown-key errors put the file's key names in `detail`, and `_config_exit` prints them raw to stderr (control characters would reach the terminal). Operator-owned file, so low risk; the claim is false as written. |
| DC-M6 | `cycle.py:796-803` | A stopping candidate gets a decision line carrying the cycle-level reason (probe P6: issue 2 decision `rate_limit_clamped`). Plan item 6.6 and DF-41 say a cycle reason never appears on a decision line; the test helper `check_line_kinds` documents the exception. FR-020 needs one decision line per examined issue, so a table decision is needed. A sweep line plus an examined line for the same issue (probe 6) is per plan, not a defect. |
| DC-M7 | `cycle.py:1108-1118` | An exit-0 cycle with no stop gets as cycle reason the last decision's reason, or `not_approved` when nothing was examined (an idle cycle). Declared as an open point in the code comment; the SLO reducer excludes only `disabled` and `not_enabled`. |
| DC-M8 | `cycle.py:1172` | `disabled_mid_cycle` cycle lines count in SLO number (b); NFR-013(b) says non-DISABLED cycles. |
| DC-M9 | `cycle.py:1236`, `record.py:421-431` | `disabled()` uses `lexists` (a dangling symlink disables the cycle) but `disabled_since()` uses `os.stat`, which fails on it; `status` then prints "disabled since: no" while every cycle exits `disabled`. |
| DC-M10 | `cycle.py:1232`, `:1271` | A `last_completed_cycle_at` in the future (clock moved back) gives a negative age and `healthy: true`. Spec says only "above 900 s is unhealthy". |
| DC-M11 | `cycle.py:307-324` | The approvers file is checked with `lstat` on the path and read through a second `open`; owner and mode are not re-checked on the opened descriptor. Only an attacker who can already write the parent directory can race it. |
| DC-M12 | `cli.py:117-128` | FR-020 and D 722 say a crash writes one JSON line to stderr. `once` has no handler for an uncaught exception (it prints a traceback, exit 1), and the closed reason table has no crash reason, so this needs a design decision first. `re-approved` is also never emitted (declared OQ-49, not counted). |
| DC-M13 | `cycle.py:1153` | A dry-run with no eligible issue reports no `probe:` line; FR-019 says a dry-run "reports the probe as skipped". With no candidate there is no probe step, so this is an editorial gap. |

## Actions Taken
None. fix_authorization is false. Only this report and the scratch probes under `/tmp/gatec-probe/` were written. `git status` outside `.dev/` was not changed by this review.

## Inherited Structural Verdict - Reliance Audit (PR-04, INV-019)
No `## Inherited Structural Verdict` section was in the spawn prompt, so the review fell back to standalone behaviour (independent checking). Nothing was skipped on the strength of another report.

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- None. No inherited structural verdict was supplied. I did not rely on the sibling `qa-structural-citation-evidence-report.md`.

**(b) Independent semantic checks (>=1 required, INV-019):**
- Exit-code and order check of the 15 steps - verified by reading `cycle.py:661-1056` against D 342-358 and running probes 1, 2, 5, 6, 7 through `run_cycle`.
- S1 halting and `k = 8` arithmetic - verified by probe7 (15 skipping issues: 8 stamped, 2 `budget_exhausted` unstamped, 34 gh calls; 15 eligible: 1 launch, 1 stamp).
- Config and approvers tables - verified by probe3 (28 inputs, including `True` as an id, 10**20, CRLF, BOM, 0620 mode).
- Reset audit lines - verified by probe4: one line per exit, no `cycle` line in `audit.jsonl`, `consumed_log` keeps the evidence and the day-cap count stays 2.
- Dry-run - verified by probe2: `dispatch.json` byte-identical after two dry-runs, zero launcher calls, shadow file written, would-launch on issue 1 then 2.
- Deadline corner - verified by probe5 and it produced DC-1.

Answers to the mandatory questions: (1) about 70 factual claims checked against code or by running it; (2) files read: `cycle.py`, `cli.py`, `record.py`, `audit.py`, `launch.py`, `predicates.py`, parts of `github.py` and `tests/issue_watch/conftest.py`, design lines 100-760, spec lines 84-110, 112-203, 205-232, 296-362, `06-gap-fill-decisions.md` DF rows, task file steps 6.1-6.9, 7.1-7.5 and Open Questions; (3) not applicable, issues were found, and the probes above are the evidence; (4) no web research was done, so no Tavily or fallback call was made.

## Recommendations
- Fix DC-1 (one reorder in `_launch`, one test) and re-run this lens in cycle 2. Minor notes need no action for the gate.
- Owner decisions worth taking after the task: DC-M6 (decision-line reasons), DC-M7 (cycle reason of a clean cycle), DC-M12 (crash line).
- Not assessed in this lens: test-file adequacy, secrets and printing rules (other Gate C lenses).

## Confidence
Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (checks 7 and 8 were adapted to behaviour probes; the test files were not read, by lens assignment).
Tool engagement: Read: 24 | Grep: 8 | Glob: 0 | Bash: 14 (7 of them probe runs)
Padding check: Read + Grep + Glob (32) is above the 15 checks.

## QA Complete

