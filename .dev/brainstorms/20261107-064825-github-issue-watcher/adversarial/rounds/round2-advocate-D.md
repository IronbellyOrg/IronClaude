# Round 2 rebuttal: advocate D (devops lens: deployment, observability, runbooks, SLO impact)

## 1. Responses to criticisms

This section covers the criticisms of variant D from round 1 (A, B, C, E) and from round 2 so far (A, B, C). Concessions come first, then defences.

**Conceded**

1. **FR-014 "any other non-zero exit gives `failed`" (A R2, C R1/R2).** Conceded in full. D counts `launches` on success, so an Orca call that started a session and then returned an error, or was killed by D's own 20 s subprocess timeout, comes back as a retryable `failed`. That is a duplicate-launch path. Adopt C: in the same atomic write as `pending`, increment `launches` durably before Orca is spawned. After the spawn, every outcome other than confirmed success is `unknown`. Only a failure *before* the spawn (no Orca found, prompt or worktree rejected) is a retryable `failed`, and it consumes nothing. D's own principle that a duplicate costs more than a missed launch (§7) requires this. My FR-014 broke that principle.
2. **Orca timeout of 20 s (A R1).** Conceded, as in round 1. Use 120 s for Orca and 20 s for `gh`. A timeout becomes `unknown`, per item 1.
3. **Pre-launch failure deletes the entry (A R1).** Conceded. Adopt the B/C order: refresh first, then commit `pending`, then invoke Orca. A failed refresh never writes an entry, so there is nothing to delete. The audit line keeps `revalidation_failed` as evidence (C-009 below).
4. **Approvers file shipped with the Coder template (A R1/R2, A-010).** Conceded. A template-shipped file turns approval authority into infrastructure-as-code that nobody reviews per workspace. The owner creates it, and `check-config` refuses one that is missing, empty, or group- or world-writable.
5. **`rate_remaining` has no source (E R1).** Conceded. `gh api` would need `--include` to expose `X-RateLimit-Remaining`, and no code in the repo does this (grep, §3 N4). Drop the field and keep `gh_calls` (E NFR-007). The rate-limit case is covered by exit 5 and a persisted next-permitted time.
6. **The 100-item `project item-list` cliff (E R1, B R1).** Conceded. D's own R3 admits the cliff, and raising the limit only moves it. Adopt E's per-issue `projectItems`.
7. **Exit 3 is overloaded and the fail-closed scope covers the whole cycle (B R1, A R1).** Conceded. Adopt A's X-007 table and A's C-015 split: shared inputs void the cycle, and per-issue reads skip only that issue.
8. **Repeated exit 75 counted as healthy (C R2, E R1).** Conceded. SLO (b), "≥99% of cycles exit 0 or 75", lets a hung cycle hold the lock forever while the SLO still reads green. Fix: `status` reports `last_completed_cycle_age_seconds`, a value that exit 75 never refreshes, and SLO (b) counts 75 as healthy only while that age stays under 900 s. Staleness (runbook step 6) then catches a wedged lock holder within three cycles.
9. **Removing an abandoned entry by hand needs a guarantee-reset warning (C R1/R2).** Conceded on the warning. My counter on deferral is in item 12.
10. **OD-7 "default interactive mode, never bypass" is not enforceable (B R1).** Conceded. No launch flag sets the mode (A-002). Replace it with A's C-014 gate: no cron is enabled until a live test records the mode, and bypass needs written owner acceptance.

**Defended**

11. **Flags-only interface with no config file (A R1).** Partly conceded. D has `check-config`, but D also lists every option as a flag. A config file plus `check-config` is the better operator surface, because cron lines stay short and the values are reviewable. I accept A's C-020 verbs, with C's read-only `check-config` (item 12).
12. **Reset should be deferred (C R2).** Contested. Deferral does not remove the reset; it just moves it into "edit `record.json` by hand", which happens without the lock, without an audit line and without a schema check. That is the worst form a reset can take, and an operator *will* hit it: `claim_not_observed` and `pending_orphan` are terminal by design. So the reset must exist as a verb, with C's safeguards. It works only on `abandoned`, takes the cycle lock, requires an explicit `--forfeit-guarantee` flag, prints that issue N may now be launched twice, and writes an audit line. That satisfies C's acknowledgement requirement and keeps the recovery inside a mechanism the system controls.
13. **Exit 75 rather than 0 for a held lock (A R1, E R1: "benign overlaps alert").** Defended. A single 75 is not an alert. The alert rule is staleness (item 8), not "any non-zero exit". 75 is `EX_TEMPFAIL` from BSD `sysexits.h`, which cron wrappers recognise as "try later". B and C now agree with this (B R2 item 9; C C-018 AGREE).
14. **Runbook, `DISABLED` kill switch, 24 h shadow `--dry-run`, staleness rule.** No variant criticised these. A's X-007 ruling and A's C-023 adopt the action-per-exit-code idea. I add the shadow dry-run as an activation gate (C-023 below).
15. **SLO (c), "≥95% of `launched` reach `claimed` within the lease" (C R1: SLO success must not hide unknowns).** Defended with a fix. SLO (c) is the only production detector for R1 (the slash command does not run from `--prompt`). Add an SLO (d): no `unknown` or `pending_orphan` entry stays unacknowledged for more than 24 h. With (d) in place, success on (c) cannot hide them.

## 2. Changed views on other variants

- **C** is now my reference for the at-most-once core. "Consume before I/O, and expiry never releases a consumed slot" fixes the hole in D's FR-014 that I missed in round 1. I still reject SQLite: one JSON file, written with the existing helper plus a directory fsync, meets C's integrity properties (S-005). I also reject C's "bounded comment content" (X-008).
- **A** produced the most usable merged rulings. I take A's text on 18 of the 28 points. The one place I break from A is C-009: A writes `pending` first and then deletes the entry, and B and C show that ordering is unnecessary.
- **B** conceded every dangerous rule it had: a corrupt record reset to empty, a relaunch after the lease, and the label-only mode. B's page-counting rule (N1) reconciles complete event histories with E's 35-call cap, so I now vote B on C-006 and C-024.
- **E** fixed the scaling defect that every variant, mine included, shared: per-issue `projectItems`. E's daily cap of 6 is the right blast-radius limit for a selection bug, and an operator can read it straight off the audit.

## 3. New evidence (checked read-only this round)

- **N1. `write_prepared_bytes` already gives 0600 files and fsyncs the file but not the directory.** `src/superclaude/cli/swarm/atomic.py:22-32` creates the temp file with `tempfile.mkstemp` in the target directory, fsyncs it at `:31` and calls `os.replace` at `:32`. `mkstemp` creates the file with mode 0600, and `os.replace` keeps that mode. So D's NFR-012 (atomic writes, mode 0600) needs no new code. No `fsync` of the parent directory exists (only line 31 matches `fsync`), which confirms C's E1. The fix is a small wrapper in `issue_watch/record.py` that fsyncs the directory after the replace. `swarm` itself stays unchanged.
- **N2. A Python `fcntl.flock` precedent exists in installed hooks, not in package code.** `src/superclaude/hooks/scripts/launch-job-identity.sh:146` uses `fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)` in embedded Python, and `:461-462` refuses any platform other than Linux, or a missing `fcntl`, with `unsupported platform`. `ccsession:415` uses the same call. This qualifies A's E6 ("no Python flock"): the non-blocking form is house practice, and so is refusing when it is unavailable. The watcher's lock should copy both and exit 2 on a platform without flock. That is a pre-flight check an operator can see, not a silent run with no lock.
- **N3. Nothing in `src/superclaude` uses exit 75 or `os.EX_*`** (grep for `EX_TEMPFAIL|exit(75)|return 75|os.EX_` finds nothing). 75 is therefore a new contract for this package, as C's §8 says of all its codes, not a reuse of an existing one. It must be written into the design-doc exit table.
- **N4. No code reads GitHub rate-limit headers.** A case-insensitive grep for `X-RateLimit|rate_limit|ratelimit` finds only unrelated hits: ClickUp's `rate_limited` reason in `sc-issue-protocol/scripts/clickup_claim.py:56,123` and the Anthropic gateway's `rate_limit_error`. This supports conceding `rate_remaining` (item 5). It also shows that `clickup_claim.py` returns `rate_limited` as a reason string, not a dedicated exit code (`:56-58`), so the watcher's exit 5 is a separate, new decision.
- **N5. `_find_orca` cannot be stubbed through an injected runner as written.** `install_user_setup.py:205` calls `shutil.which` and `:209-215` calls `subprocess.run([path, "skills", "list", "--json"], ..., timeout=10)` directly. This confirms C's E2. The C-010 ruling needs the probe to go through the injected runner, either by moving its logic into a runner-taking helper or by wrapping it. It also needs the 10 s probe counted in the cycle's time budget. Separately, I confirmed `poll-augment-review.sh:46-56` (B's N1): explicit `per_page=100` pages, `--method GET`, "fail incomplete at the cap".

## 4. Updated positions

"AGREE with X" means I accept advocate X's round-2 ruling exactly as written.

| Point | Superior variant | Confidence % | Merged ruling or AGREE with X |
|---|---|---|---|
| C-001 | HYBRID | 75 | AGREE with A. Matching by name fails closed on a rename, and creating labels needs write access. Label node IDs would add a resolve call and a config surface without closing a real gap, because the approval actor check carries the trust. |
| C-004 | HYBRID | 80 | AGREE with A. The claim assigns and checks by login (`@me`), and the login is re-read each cycle from the same token, so login routing stays consistent with the claim. |
| C-005 | HYBRID | 85 | AGREE with A |
| C-006 | HYBRID (E+B) | 85 | AGREE with B |
| C-007 | HYBRID (A+C) | 90 | A's fields and states. `launches` is incremented in the same durable write as `pending`, before Orca is spawned; a fresh launch requires `launches == 0`. Re-labelling, re-approval, lease expiry and login change never reset it; only `reset <N> --forfeit-guarantee` does. |
| C-008 | HYBRID | 80 | AGREE with A |
| C-009 | HYBRID (B/C order) | 85 | Under the lock, re-read state, labels, assignees, approval and Project Status. A failed or unreadable re-read skips `revalidation_failed`, writes no entry, launches nothing. Only then durably write `pending` with `launches` incremented, then call Orca. A `pending` at cycle start becomes `abandoned` `pending_orphan`. |
| C-010 | HYBRID (A+B+C) | 85 | AGREE with A, plus: `_find_orca`'s probe runs through the injected runner (today it calls `subprocess.run` directly) and its 10 s timeout counts toward the cycle time budget. |
| C-011 | C | 90 | Any outcome after Orca is spawned other than confirmed success (timeout, malformed output, `agent_session_operation_unknown`, non-zero exit) is `unknown`, with the slot consumed. With an `operationId`, only `--retry-launch <id>` from the stored cwd; without one, `abandoned`. Retryable `failed` covers only pre-spawn failures. |
| C-012 | HYBRID | 90 | AGREE with A |
| C-013 | HYBRID (C IDs) | 85 | AGREE with A |
| C-014 | HYBRID | 85 | AGREE with C |
| C-015 | HYBRID | 85 | AGREE with A |
| C-018 | D | 90 | A's text, plus: `status` also reports `last_completed_cycle_age_seconds`, which exit 75 never refreshes. An age above 900 s is unhealthy whatever the exit codes, so repeated overlaps raise an alert. |
| C-020 | HYBRID (A+C+E) | 75 | Verbs: `once [--dry-run]`, `status [--json]`, read-only `check-config`, `init-state` (creates the store and refuses if one exists), and `reset <N> --forfeit-guarantee` (only on `abandoned`, under the lock, audited, prints that N may launch twice). Exit codes as in X-007. |
| C-023 | HYBRID (A+D) | 80 | AGREE with A, adding three activation gates before cron is enabled: a 24 h shadow `--dry-run` whose audit is reviewed, a two-process lock test on the real state directory, and the staleness alert (`last_completed_cycle_age_seconds` > 900) wired up. |
| C-024 | HYBRID | 85 | AGREE with B |
| S-001 | HYBRID | 70 | AGREE with A |
| S-004 | HYBRID | 75 | AGREE with A |
| S-005 | HYBRID (D form, C init) | 85 | One versioned JSON record file per state directory, written with `write_prepared_bytes` (0600) plus a parent-directory fsync. Only `init-state` creates it. If it is missing after init, unparseable or of unknown version, `once` exits 6 with no launch and leaves the file untouched. No SQLite. |
| S-007 | B | 70 | AGREE with A |
| S-008 | HYBRID | 65 | AGREE with A |
| X-001 | D | 90 | AGREE with A, plus: a later own marker still moves the `abandoned` entry to `claimed`, and `claim_not_observed` never releases the consumed slot. |
| X-002 | D | 85 | AGREE with A. Under C-007 the slot is already consumed, so C's `unknown` and D's `abandoned` block equally; `pending_orphan` names the cause for the operator. |
| X-003 | D | 95 | AGREE with A |
| X-005 | D | 90 | AGREE with A |
| X-007 | HYBRID | 85 | AGREE with A. Exit 6 also covers a store that is missing after `init-state`. |
| X-008 | HYBRID | 85 | AGREE with A |

Reasons for the non-AGREE rows:

- **C-007 and C-011** carry C's consume-before-spawn rule. Without it, D's own FR-014 relaunches a session that Orca started but timed out on.
- **C-009** uses the B/C order. A's write-then-delete creates an extra `pending_orphan` source, a crash during a re-read that fails, and with it an operator ticket for an issue that was never launched.
- **C-018** separates "the lock was held" from "work completed". Otherwise the observability SLO is blind to a wedged holder.
- **C-020** keeps the reset as an audited verb. A deferred reset becomes an unlocked hand edit of the record.
- **S-005** is A's form plus C's directory durability and explicit init. N1 shows the directory fsync is missing from the helper we reuse.


## 5. Shared-assumption changes

Only the assumptions whose answer changed since my round 1 are listed here. A-002, A-004, A-005, A-008 and A-010's core answer are unchanged except where noted.

- **A-001 (state survives restarts):** QUALIFY, tightened. Only `init-state` creates the store; a missing store after init exits 6 and never starts empty, so losing `$HOME` stops dispatch instead of duplicating launches. A cleared state directory can only be recovered by a re-init followed by owner review of the open `launched` issues.
- **A-003 (logins and names stable):** changed from a partial REJECT to a split ACCEPT. Owner routing stays by login, because the claim works by login (`refs/claim.md:41-42`, B's N4) and the login is re-read each cycle. Approvers are keyed by account ID (C-013), so a rename cannot transfer approval trust. Label names stay names and fail closed (C-001).
- **A-006 (wall clock trustworthy):** QUALIFY, narrowed. Only the rolling 24 h cap, the backoff and the lease report depend on the clock. A jump can only delay launches, or let at most one extra launch through the daily cap. It can never relaunch an issue, because `launches == 0` and `abandoned` are terminal states that do not depend on the clock. The `status` view reports ages computed from the clock, so a skew shows up there first.
- **A-007 (`flock` effective):** QUALIFY, made checkable. The house lock helper already refuses a non-Linux platform or a missing `fcntl` (`launch-job-identity.sh:461-462`). The watcher does the same and exits 2. A local, single-host state directory is a documented precondition, and A's two-process lock test on the real directory is an activation gate (C-023).
- **A-009 (marker within lease):** changed from QUALIFY to REJECT-as-safety-input. Under X-001 and X-002 the lease is only a reporting threshold that moves the entry to `abandoned` `claim_not_observed`, and a later marker still moves it to `claimed`. No at-most-once property depends on it, so a slow Wave 4 costs a status line, not a duplicate session.
- **A-010 (allow-list file owner-only):** QUALIFY, unchanged on permissions (group- or world-writable gives `check-config` exit 2). Changed on provenance: the template does not ship the file, the owner creates it, it holds account IDs, and an empty file means no approvers rather than "anyone".

