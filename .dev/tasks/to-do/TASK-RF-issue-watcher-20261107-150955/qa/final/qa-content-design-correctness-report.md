# QA Report - Final gate, design-correctness lens (content)

**Topic:** issue-watch implementation, whole change set
**Date:** 2026-11-08
**Phase:** task-qualitative (design-correctness lens)
**Fix cycle:** 1 (first Final-gate review)

---

## Overall Verdict: FAIL (3 blocking, 9 minor)

Fix authorization: false (report-only). Nothing outside this report was modified. The only experiment ran on a `/tmp` copy (config, state directory, approvers file and worktree all under `mktemp -d`; no `gh`, `git` or Orca call was reached) and the directory was removed afterwards.

Binding sources read: `docs/designs/issue-watcher.md` lines 95-166, 168-302, 304-533, 535-745; `spec-final.md` lines 60-102 and 109-397; `06-gap-fill-decisions.md` DF-01 to DF-60 and the phase plan; `deviation-register.md` (all); `final-change-set.md` (all). Deliverables read in full: `cycle.py`, `predicates.py`, `record.py`, `launch.py`, `cli.py`, `github.py`, `audit.py`, `runner.py`, `docs/designs/issue-watcher-setup.md`. Decision rows marked DEVIATION (including the Gate C [PROPOSAL] reasons `cycle_complete` and `cycle_crashed`) were treated as overrides and only checked for internal consistency.

Axis lens status: `drift-axis-inactive` (no BUILD_REQUEST.GOAL verbatim in the spawn prompt, and the quoted prompt does not reproduce it). The Axis column uses the closed set; AX-1 is not used.

## Items Reviewed

| # | Check (interaction no earlier gate saw together) | Axis | Result | Evidence |
|---|---|---|---|---|
| 1 | FR-001 / design 6.2 step order in `_Cycle.run`, `_steps`, `_load`, `_login_step`, `_sweep`, `_discover`, `_candidates`, `_commit`, `_conclude` | none | PASS | `cycle.py:663-790`; order is enabled, setup, lock, DISABLED, load+migrate, rate check, G1, origin, sweep, discovery, candidates, final write, audit. The worktree is checked before the approvers file (FR-001 lists the reverse): minor M-4 |
| 2 | Exit-code precedence 2, 6, 7, 5, 3, 4, 75 (`resolve_exit`, `_cond`, `_exit`, `_cycle_reason`) | none | PASS | `cycle.py:442-463, 568-577, 1127-1137`; first present of the precedence list, 75 only when sole condition. The 7-with-5 and 7-with-3 combinations cannot occur (B-2) |
| 3 | At-most-once across C1 to C5 (design 523-533) | none | PASS | `cycle.py:1060-1075`: `mark_pending`, then `_save()` (raises `_Stop` on `OSError`, so no launch), then `launcher.launch`; the outcome is held in memory and saved in `_commit_store`. Any exception after the save leaves `pending, launches 1`; `record.sweep` (`record.py:627-651`) abandons it as `pending_orphan`; `_examine` (`cycle.py:903-912`) then only looks for a marker. No code path lowers `launches` except `reset_entry` (`record.py:706-720`) |
| 4 | Dry-run isolation (FR-019) | none | PASS | `_load` saves a migrated store only when `not dry_run` (`cycle.py:727`); `_launch` returns before the probe (`cycle.py:1010-1016`); `_commit` routes to `_commit_shadow`, which writes only `dry-run.json` (`cycle.py:1109-1125`); rate limit and sweep changes stay in memory; every line carries `dry_run` |
| 5 | Reset audit lines (DF-03, DF-04, DF-57) | none | PASS | `cli.py:232-348`: one line per exit; success is a `decision` (issue) or `warning` (rate limit) line, refusals are `reset_refused` with the issue, lock and store faults are `warning` lines, `state_dir_unwritable` is stderr only, never a `cycle` line, rotation only under the lock |
| 6 | `status` read-only guarantee (FR-021) | none | PASS | `cycle.py:1194-1298` uses a plain `open(..., "rb")` and `os.stat` on `DISABLED`; no lock, no audit access; experiment: `status` after `init-state` printed the report, exited 1 and created no file |
| 7 | Section 3 predicates against `predicates.py` (approval, unchanged-since, project, intended owner, marker window, ordering) | none | PASS | `predicates.py:162-312` read against spec lines 84-107 and design 7.5; ties, equality and the `[bot]` rule match |
| 8 | G1 to G7 argv and reply classification against design 8.1 to 8.3 | AX-2 | PASS with note | `github.py:106-263, 345-431`: every argv matches the design table. A per-issue `auth_failed` is skipped, not exit 3 (design table 8.2 vs FR-022): minor M-1 |
| 9 | Rate limit persistence and clamp (FR-028, C22) | none | PASS | `cycle.py:644-649, 733-743, 775-783`; `github.rate_limit_wait` (`github.py:418-431`); dry-run keeps it in memory |
| 10 | Launch step order (FR-014) and 120 s cut-off (FR-029) | none | PASS | `cycle.py:1007-1075`: probe, prompt, re-read, day cap, DISABLED, cut-off, origin re-check, cut-off again, pending write, spawn |
| 11 | Lock protocol (FR-017, design 7.6) | none | PASS | `record.py:380-419`; descriptor released in `finally`; `cycle.py:675-683` maps `LockHeld` to 75 without rotation |
| 12 | Store schema, validation, migration, init (design 7.2) | none | PASS | `record.py:120-278, 753-802`; every writer (`fail`, `mark_*`, `set_considered`, `reset_*`) produces a document `validate` accepts |
| 13 | Config and approvers validation (design 4.2, FR-027) | none | PASS | `cycle.py:127-358`; label, project id, owner id, absolute path and network-FS rules match design and DF-13, DF-20, DF-23 |
| 14 | Audit schema, rotation, stderr fallback (design 10.1) | none | PASS | `audit.py:26-404`; 59 reason names; rotation `.3->.4 ... current->.1` under the lock only |
| 15 | SLO reducer (NFR-013) | none | PASS | `cycle.py:1301-1369`; nearest-rank p95, 7-day window, dry-run lines excluded |
| 16 | CLI verbs, exit codes, `cycle_crashed` handling | none | PASS | `cli.py:111-348`; five commands; an unexpected exception gives exit 1 and a fallback line with the class name only |
| 17 | Runbook against the behaviour of the code (sections 1 to 14) | AX-2 | FAIL | B-1 (`store_missing` vs `lock_missing`), B-2 (impossible exit combinations); the `/tmp` experiment confirms B-1 |
| 18 | Deviation register and `final-change-set.md` internal consistency | AX-2 | FAIL | B-3 (register says `final-gate-record.md` does not exist and the DF-05 sentence is pending; the file exists and holds it; the change set quotes a verdict the register does not contain) |
| 19 | Reason-count arithmetic 52 + 5 + 2 = 59 and the 29 DEVIATION ids | none | PASS | 29 register ids counted; runbook table counted by hand (59 rows including the `re-approved` note); `audit.REASON_TABLE` has 59 entries |
| 20 | Module interactions: cycle with the real github, record, launch and audit signatures (`Read.kind` handling, `LaunchOutcome` validity into `mark_launched`/`mark_unknown`, `Deps` fields) | none | PASS | `LaunchOutcome.__post_init__` (`launch.py:251-259`) guarantees a valid id, so `mark_launched(..., outcome.operation_id or "")` cannot raise after a spawn; `_val` and `_rv` cover every `Read.kind` that `github.py` produces |

## Summary
- Checks passed: 18 / 20 (item 8 passes with a minor note)
- Checks failed: 2 (items 17 and 18)
- Critical issues: 0
- Blocking findings: 3 (B-1, B-2, B-3)
- Minor findings: 9
- Issues fixed in-place: 0 (report-only)
- Axis lens status: drift-axis-inactive

## Issues Found

Blocking findings (the verdict is FAIL because of these):

| id | Severity | File | Evidence | Expected versus actual |
|---|---|---|---|---|
| B-1 | blocking (false claim, IMPORTANT) | `docs/designs/issue-watcher-setup.md` line 156 (section 5) and line 336 (section 10.1, item 6) | Experiment on a `/tmp` copy: `once --dry-run` against a config whose `state_dir` did not exist printed `cycle: lock_missing`, `exit: 6`; with an existing empty `state_dir` it also gave `lock_missing`. Code: `cycle.py:675-683` takes `store.lock()` before `_load`, and `record.py:392-397` raises `LockError("lock_missing")` for an absent `lock` file; `store_missing` is raised only when the lock exists and `dispatch.json` does not (`record.py:357-358`). Design step 2 comes before step 4 and FR-017 says "A missing lock exits 6". The tests that cover `store_missing` (`test_cycle.py:1159, 1513, 1576`) keep the lock file and delete only `dispatch.json`, so none covers the real new-setup case | Runbook line 156 says "A cycle run before `init-state` ends exit 6 with `store_missing`" and line 336 says "`store_missing`: run `init-state` on a new setup". The actual reason on a new setup is `lock_missing`. An operator who greps the audit log for `store_missing`, or who follows line 336 for the `lock_missing` they really see, is sent to section 11.5 ("move the whole state directory aside"), which is wrong for a setup that has no state yet. Expected: name `lock_missing` (and `store_missing` only for a lock that exists without a store) in both places, and send a new-setup `lock_missing` to `init-state` |
| B-2 | blocking (false claim) | `docs/designs/issue-watcher-setup.md` line 340 (section 10.1, "Precedence") | `cycle.py:1007-1075`: after `_fail`, `launch_unknown` or `spawn_error` the candidate has `c.launching = True`, `_candidates` sets `self.halt` (`cycle.py:814-815`) and no further `gh` call, rate-limit stop or shared read can follow; the final save makes no external call. A rate-limit (5) or `gh` timeout (3) stop raises `_Stop` and ends the cycle before any entry write. The design sentence it copies (design line 166) contradicts the design's own S1 resolution (design 386-388: after any launch-step outcome later candidates are neither read nor stamped) | Runbook says "The combinations that occur in practice are 7 with 5 ... and 7 with 3 ... Both conditions are audited, and the exit is 7." In the code these combinations cannot occur, and a second condition is never audited next to a 7. Expected: state only the precedence rule and say that 7 is normally the last condition of a cycle (only 6 can follow it, when the final save fails, and 6 wins) |
| B-3 | blocking (false claim in a delivered report) | `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/phase-outputs/reports/deviation-register.md` lines 13 and 60; `final-change-set.md` section 7 (DF-05 row) | `final-gate-record.md` exists (written 02:21; the register 02:15) and its line 20 holds "full suite: CI only". Register line 13 still says that file "does not exist yet" and ends its verdict "pending Step 9.19, Table 3"; line 60 repeats "Pending ... until then". `final-change-set.md` section 7 says it copies the register but prints the DF-05 verdict as "PASS (the literal sentence is now in `final-gate-record.md`, section 5 above)", text the register does not contain | The two report files disagree about the same row, and the register is stale. Expected: the register's DF-05 row and Table 3 note say the sentence is in `final-gate-record.md` line 20, and `final-change-set.md` quotes the register verbatim |

Minor findings (notes; never rechecked):

| id | Severity | File | Evidence | Expected versus actual |
|---|---|---|---|---|
| M-1 | minor (design vs spec tension; self-heals next cycle) | `cycle.py:817-827` (`_val`), design 8.2 line 584 | `_val` handles `rate_limited`, `scope_missing` and `budget_exhausted`, and turns every other failed kind, `auth_failed` included, into a per-issue skip. Design table 8.2 gives `auth_failed` the effect "exit 3 `gh_auth_failed`" for every observation; FR-022 (spec line 136) lists only shared inputs as cycle-voiding. No DF row decides it | A 401 after a good G1 would skip up to 8 candidates with `*_unreadable` reasons and end exit 0 with the health stamp refreshed; the next cycle's G1 reports exit 3. Owner decision: keep the FR-022 reading and record it, or map `auth_failed` to `_Stop("gh_auth_failed")` |
| M-2 | minor | `docs/designs/issue-watcher-setup.md` line 65 (section 1.4) and line 332 | `cli.py:77-81`: `_config_exit` writes a JSON fallback line and then `issue-watch: <reason>: <detail>`, two stderr lines | Runbook says "a one-line reason on stderr" and "its stderr line names the reason". Actual: two lines; the second one names the reason |
| M-3 | minor | `docs/designs/issue-watcher-setup.md` line 432 (section 10.4) | `cli.py:169`: `status` calls `_load_config`, which exits 2 for an invalid config | Runbook lists status exits 0, 1 and 6 only; 2 is missing |
| M-4 | minor | `cycle.py:352-358` | `validate_setup` checks the worktree before the approvers file; FR-001 (spec line 115) lists the approvers file first | Only the reason differs when both are invalid (`worktree_invalid` vs `approvers_invalid`, both exit 2) |
| M-5 | minor (unregistered narrowing) | `launch.py:174-185` | `find_orca` skips a `which` result that is not absolute; design 8.4 says only "resolved with the injected `which`"; no DF row records it | An Orca binary reachable only through a relative PATH entry gives `orca_not_found`. Protective and documented in the docstring; add it to the register |
| M-6 | minor | `cycle.py:1251, 1290` | `age = int((now - last).total_seconds())`; `healthy = age is not None and age <= 900` | A `last_completed_cycle_at` in the future (clock moved back) gives a negative age and `healthy: true`. Clamp it or treat it as unhealthy |
| M-7 | minor (UNVERIFIED; goes to the live test FU-1) | `runner.py:90-101`, `launch.py:343-355` | `OrcaLauncher.launch` uses `subprocess.run(capture_output=True, timeout=120)`. If `orca agent launch` leaves a long-lived child holding stdout, `communicate()` waits for the pipe and the call times out as `unknown` although the session started | Not demonstrable here (no live Orca call allowed). The sweep and the marker check recover it (`unknown` becomes `claimed` on the marker), so the guarantee holds; record the observed behaviour in the live-test record |
| M-8 | minor | `docs/designs/issue-watcher-setup.md` line 525 and `cycle.py:1225-1230` | The runbook says the retry command starts with "the bare name `orca-ide` or `orca`, whichever is first on your `PATH`"; `_retry_orca` returns the bare name, never a path, and falls back to `orca-ide` when none resolves | Consistent with register Table 2 row 5; noted so the owner knows the printed command depends on the `PATH` of the shell where it is pasted |
| M-9 | minor | `06-gap-fill-decisions.md` DF-02 and DF-22 text; task file OQ-2 and OQ-49 | The decisions and open questions still say "57 names"; the tree has 59 (register Table 2 row 1 says so itself) | Consistent once Table 2 row 1 is read; the stale counts are already listed in register Table 3 |

## Actions Taken
None. fix_authorization is false. One read-only experiment on `/tmp` (removed afterwards) and four read-only `grep`/`sed`/`wc` Bash calls. Two Grep tool calls failed with `EACCES` (`rg` not executable) and were redone with Bash `grep`.

## Inherited Structural Verdict - Reliance Audit (PR-04, INV-019)
The spawn prompt carried no `## Inherited Structural Verdict` section, so standalone behaviour applied. No structural PASS was relied on. The line counts, file inventory and gate table in `final-change-set.md` were used only as an index to the files and checked against the files themselves.

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- None. No inherited structural verdict was provided. `final-change-set.md` section 5 (gate results) was taken as the record of which commands ran, not as proof of behaviour; its pytest counts were not re-run (that belongs to the gate-reproduction lens).

**(b) Independent semantic checks (>=1 required, INV-019):**
- Runbook reason for a cycle before `init-state` -- verified by running `once --dry-run` against a `/tmp` config with a missing and then an empty `state_dir`; both printed `lock_missing`, exit 6 (Bash call 2). This contradicts runbook lines 156 and 336 and is the evidence for B-1.
- At-most-once ordering -- verified by reading `cycle.py:1060-1075` against `record.py:538-568, 627-651` and design 523-533; `_save()` precedes `launcher.launch`, and a failed `_save()` stops before the spawn.
- Exit-combination claim -- verified by tracing `_candidates` (`cycle.py:793-815`) and `_launch` to show nothing runs after an exit-7 condition (B-2).
- Launch outcome validity -- verified that `LaunchOutcome.__post_init__` (`launch.py:251-259`) prevents `mark_launched` and `mark_unknown` from raising after a spawn.
- Store round trip -- verified by reading every `record.py` writer against `_entry` and `validate` (`record.py:168-244`).
- Reason-table arithmetic -- counted the 59 runbook rows and the 29 register ids by hand.

**Confidence (Confidence Gate Protocol):** Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (items 17 and 18 are verified failures).
Limits: the 2628-test suite and the stub end-to-end runs were not re-executed (gate-reproduction lens); no live `gh` or Orca call was made (not allowed); behaviour that depends on real `gh` or Orca output (event shapes, `Retry-After` on rate-limited replies, Orca stdout handling) is UNVERIFIED by design and was not judged beyond the fixtures.

**Tool engagement:** Read: 28 (one rejected for size, then paged; one read of this report) | Grep: 1 successful, 2 failed with EACCES | Glob: 0 | Bash: 5 (wc, the /tmp experiment, test greps, register greps, `sed` of `atomic.py`). Read+Grep+Glob (29) is at least the 20 checklist items.

**Web research:** none performed; Tavily not needed.

## Recommendations
- Fix B-1 in `docs/designs/issue-watcher-setup.md` (lines 156 and 336) and add a test or a runbook note for the real new-setup case (`lock_missing` with no state directory).
- Fix B-2 (line 340) so the runbook states only what the code can do.
- Fix B-3: update `deviation-register.md` lines 13 and 60, and make `final-change-set.md` section 7 quote the register verbatim.
- Minor findings M-1 to M-9 stay as notes. M-1 and M-5 deserve a line in the deviation register if the owner agrees with the behaviour.

## QA Complete
