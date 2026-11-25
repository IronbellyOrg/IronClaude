# Section 11 analysis: Carried over and dropped
Counts: COVERED 20, CONFLICT 7, NOT-COVERED 12 (39 rows)

Sources read for this section: issue 655 body lines 1-30, 158-162, 213-230; saved comment 1 (history and carried-over detail, lines 74-126 of the comments file) and comments 15 and 16; the current plan files named in each row. Two documents outside the brainstorm folder were read read-only from `origin/master` with `git show` because they define the follow-up and owner-question labels that 655 cites: `docs/designs/issue-watcher.md` (call it DES) and `docs/designs/issue-watcher-setup.md` (call it SETUP). They are not in the checkout, only in git. Paths below that start with `.dev/brainstorms/20261120-pr686-unify/` are shortened to `<W>/`.

Short names: SPEC is `<W>/spec/SPEC.md`; DECISIONS is `<W>/DECISIONS.md`; TECHREF is `<W>/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md`; DES and SETUP are the two design documents above. A bare `SPEC.md:NN` means that line of SPEC.

<!-- ROWS-BEGIN -->
## Part A: carried over

### S11-F1 Reuse the built issue-watch code as the poll step
- 655 says: the poll step reuses `runner.py`, `record.py`, `audit.py`, `launch.py` and the budget and rate-limit code in `github.py`; `cycle.py` is reshaped, not reused as is (body line 160; comment 1 line 90).
- Status: COVERED
- Current plan: D14 "PR 686 adapted in place as one draft" (`SPEC.md:90`); SPEC section 1.3 treats the master poll as "complete code, `enabled` defaults to false, never ran live" and keeps it (`SPEC.md:59`); D07 keeps one cron-run dispatcher and per-repo config (`SPEC.md:83`, `<W>/debates/D07/VERDICT.md:49`). The plan keeps the same files and changes `cycle.py` to add the plan check, hold skips and wake transport (FR-05 to FR-08, FR-13).
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: 655 reshapes `cycle.py` for its own design (route to an orchestrator with a free place, `repos.yaml`). The plan rejected the registry repository and `repos.yaml` (FR-11 `SPEC.md:201`; Clay element C5, `SPEC.md:454`), so that reshaping is 655 section 3 and 5 territory, not this row.

### S11-F2 One claim and one worker start per issue (durable dispatch record written before the launch)
- 655 says: at most one launch per issue, a durable dispatch record is written before the launch (comment 1 line 91; body line 160).
- Status: COVERED
- Current plan: FR-03 (keep `marker_in_window`, so a hand claim and a watcher start never run two workers, `SPEC.md:193`); FR-21 (claim evidence and delivery intent saved in ONE store save, an unknown launch receipt never relaunches, `SPEC.md:211`); D01 MR-2 (`DECISIONS.md:155`); store states pending to abandoned (`SPEC.md:173`).
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: none

### S11-F3 Up to 3 delivery tries for a wake
- 655 says: an unacknowledged wake is tried up to 3 times (body line 24; line 160 lists "up to 3 delivery tries").
- Status: COVERED
- Current plan: FR-13 "three deliveries 10 minutes apart, then mark the Orca workspace unread and exit 7; the poll never writes the ack" (`SPEC.md:203`).
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: none

### S11-F4 Run lock against two runs at once
- 655 says: a lock keeps two poll runs from running at the same time (comment 1 line 91).
- Status: COVERED
- Current plan: FR-10 wraps the cron entry in `flock -n` (`SPEC.md:200`); NFR-02 one writer per file (`SPEC.md:215`); the in-code lock of the master poll is kept by D14 (adapt in place). The coordinator verbs get "one state lock" (FR-26, `SPEC.md:228`).
- Depends on: S11-F1
- Evidence from our documents: n/a (COVERED)
- Concerns: no plan requirement names the poll's in-code lock (`lock_held`, exit 75). It survives only because the master code is kept. UNVERIFIED that the adapted PR 686 keeps it; its test is S11-F12.

### S11-F5 GitHub call budget and rate-limit handling
- 655 says: the call budget, error classification and rate-limit code in `github.py` are kept (comment 1 line 90; body line 160).
- Status: COVERED
- Current plan: kept by D14 (adapt in place, `SPEC.md:90`). The dispatcher has a "270 s cap" (`SPEC.md:171`). The master code (call budget 32 plus 3 reserved, reason `budget_exhausted`) is described in `TECHREF:631` and `TECHREF:906`.
- Depends on: S11-F1
- Evidence from our documents: n/a (COVERED)
- Concerns: no FR or test pins the budget for the new `run-all` case that serves many repos in one 270 s window; it is covered only by keeping the existing code. UNVERIFIED how the budget is shared across repos.

### S11-F6 Audit log with a closed reason table
- 655 says: `audit.py` (the audit log and its closed reason table) is reused; 62 poll reasons in the acceptance criteria (comment 1 line 90; body line 215).
- Status: COVERED
- Current plan: `audit.jsonl` is a store row (`SPEC.md:173`); FR-20 "a reasons table equal to the code: restore the 14 approval reasons; add `coordinator_full`, `name_collision`, `no_checkout`, `coordinator_absent`; remove `registry_invalid`, `repo_not_listed` and four label-write reasons" (`SPEC.md:210`); FR-05 test that the body is absent from `audit.jsonl` (`SPEC.md:195`); MC-10 (reasons pin rewritten, `SPEC.md:696`).
- Depends on: S11-F1
- Evidence from our documents: n/a (COVERED)
- Concerns: the reason set differs. The plan keeps the approval reasons; 655 counts 62 names without them. The count "62" belongs to 655 section 3 and is rejected where it removes approval reasons.

### S11-F7 Dry-run mode
- 655 says: a dry-run mode that decides but launches nothing is kept (body line 160).
- Status: COVERED
- Current plan: FR-23 test `test_dry_run_generates_nothing` (`SPEC.md:213`); `run-all --dry-run` (FR-11, `SPEC.md:201`); 13.2 "Cron shadow run" (`SPEC.md:705`); D09 keeps the `would_hold` dry-run listing (`DECISIONS.md:713`).
- Depends on: S11-F1
- Evidence from our documents: n/a (COVERED)
- Concerns: none

### S11-F8 Only a validated integer reaches the poll's launch prompt
- 655 says: only a validated integer reaches the launch prompt the poll script uses; the rule does not cover the orchestrator's handoff prompt to workers (comment 1 line 91).
- Status: COVERED
- Current plan: the D10 verdict lists "D3, the integer-only launch prompt, with its tests" as a strength that must be kept and widens it to "no free GitHub text in the wake file" (`<W>/debates/D10/VERDICT.md:46` and `:51`); FR-13 wake items are `repo`, `number`, `url` only (`SPEC.md:203`); Clay element B8 "no GitHub text in a typed line" is ADOPT (`SPEC.md:450`).
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: none

### S11-F9 Origin check before a launch
- 655 says: an origin check is kept (comment 1 line 91).
- Status: COVERED
- Current plan: D07 "Our strengths that must be kept: per-launch origin check" (`<W>/debates/D07/VERDICT.md:51`); `test_origin_parity.py` stays green (`SPEC.md:696`).
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: master compares the origin to `ironbellyorg/ironclaude` only (`TECHREF:817`), so the multi-repo case needs the check to follow the repo key. The plan does not say how; that is a 655 section 3 point, not this row.

### S11-F10 Live test against real `gh` and Orca on throwaway issues, replacing the `_assumed_shape` fixtures, with a written record
- 655 says: a live test replaces every guessed fixture under `tests/issue_watch/fixtures/_assumed_shape/` with captured real output, and a live-test record is written (comment 1 line 92; body lines 160 and 230).
- Status: COVERED
- Current plan: 13.2 "Cron shadow run ... real replies captured to replace assumed fixtures" (`SPEC.md:705`); the other 13.2 rows record their results (`SPEC.md:706-713`); S17 "Go/no-go record (code head, host, primitive hashes, fixture captures, failed and passed probes) kept by an agent" (`SPEC.md:501`); SPEC 1.3 states the fixtures are assumed shapes (`SPEC.md:59`); FR-23 keeps the watcher off until then (`SPEC.md:213`).
- Depends on: S11-F11
- Evidence from our documents: n/a (COVERED)
- Concerns: the old design has the owner write and commit `docs/designs/issue-watcher-live-test.md` (SETUP section 8.5). The plan has an agent keep the record, which fits the owner rule that approvals and records go through chat and an agent, never a file the owner writes. The stderr classifier (Q4) is settled by the same capture, see S11-F26.

### S11-F11 24-hour shadow run before switch-on
- 655 says: a 24-hour shadow run (a dry run that decides but launches nothing) is done before switching on (comment 1 line 93; body lines 160 and 230).
- Status: COVERED
- Current plan: 13.2 "Cron shadow run: the cron line runs `run-all --dry-run` for 24 hours under cron's environment" with pass criterion "no agent, no config generated, no GitHub write" (`SPEC.md:705`); the S17 pass list (`SPEC.md:501`); `DECISIONS.md:1119`.
- Depends on: S11-F7
- Evidence from our documents: n/a (COVERED)
- Concerns: the plan runs the shadow run under cron; 655 runs it under an Orca automation (conflict in S11-F32). The S17 pass list is "a proposal, not an owner rule (UNVERIFIED)" (`DECISIONS.md:1119`).

### S11-F12 Two-process lock test
- 655 says: a two-process lock test runs before switching on, as in SETUP section 8.2 (comment 1 line 93; body lines 160 and 230).
- Status: NOT-COVERED
- Current plan: none found; searched `SPEC.md`, `DECISIONS.md` and `FOLLOW-UPS.md` for "lock test", "two-process", "lock_held", "exit 75", "flock" and "state lock". Only FR-10 (`flock -n` on the cron line, `SPEC.md:200`) and FR-26's coordinator `test_state_lock.py` (`SPEC.md:228`) turn up. Neither tests the poll's own run lock. The 13.2 live-test list and the S17 pass list do not include it.
- Component (NOT-COVERED only): WATCHER (poll run lock)
- Feature statement (NOT-COVERED only): before the poll is enabled, hold the poll's lock from one process, start a dry-run cycle in a second, and require the second to exit 75 with reason `lock_held`, then require a normal run after release.
- Done when (NOT-COVERED only): the second cycle prints `lock_held` and exits 75, the audit log carries a `cycle` line with that reason, and a third run afterwards runs normally; the result is in the S17 go/no-go record.
- Depends on: S11-F4, S11-F11
- Evidence from our documents: SETUP section 8.2 (`origin/master`): "The second command must print `cycle: lock_held` and `exit: 75`"; the dry run is used because "while `enabled` is `false`, a run without it stops at `not_enabled` before it reaches the lock".
- Concerns: none

### S11-F13 Restart test: the state directory survives a workspace restart
- 655 says: a restart test before switching on, as in SETUP section 8.3 (comment 1 line 93; body lines 160 and 230).
- Status: NOT-COVERED
- Current plan: none found; searched `SPEC.md` for "persist", "survives a restart", "reboot", "state directory", "after two restarts". The nearest hits are 13.2 "after two restarts: one `crontab -l` line, one daemon" (`SPEC.md:713`), which tests cron and the daemon, not the store, and S15a "kill-and-restart tests at every persistence boundary" (`SPEC.md:499`), which tests wake and ack persistence. NFR-03 reads `state_dir` from config (`SPEC.md:216`) and FR-22 backs up the store before a migration (`SPEC.md:212`); neither checks that the store outlives a restart.
- Component (NOT-COVERED only): WATCHER (state files)
- Feature statement (NOT-COVERED only): before the poll is enabled, restart the workspace and show that `state_dir` and `dispatch.json` still exist with the same `created_at`, because the at-most-once guarantee lives in that directory.
- Done when (NOT-COVERED only): after a restart the directory and `dispatch.json` exist, `created_at` is unchanged and `issue-watch status` does not exit 6.
- Depends on: S11-F2, S11-F21
- Evidence from our documents: SETUP section 8.3 (`origin/master`): "The at-most-once guarantee lives in the state directory. A new, empty state directory has no memory of earlier launches (risk R5 of the design)."
- Concerns: this matters more under the plan than under 655, because the plan's store also holds waiting hand-backs and the in-flight count (FR-33, SEC-21).
### S11-F14 FU-3: narrower GitHub token scope
- 655 says: FU-3 (narrower GitHub token) is carried over (body line 160; comment 1 line 94).
- Status: NOT-COVERED
- Current plan: none found; searched `SPEC.md` for "token", "GH_TOKEN", "fine-grained", "scope", "least privilege", and `SPEC.md`, `DECISIONS.md`, `FOLLOW-UPS.md` for "FU-3". Only unrelated token mentions exist (`SPEC.md:539`, the organisation-ruleset check; `SPEC.md:545`, an Orca token left in a transcript).
- Component (NOT-COVERED only): WATCHER (GitHub reads)
- Feature statement (NOT-COVERED only): move the poll off the user's CLI login to a fine-grained token that holds only the read scopes the poll needs, and record those scopes.
- Done when (NOT-COVERED only): the poll runs a full cycle with a token that cannot write to any repo, and `check-config` or the runbook states the scopes.
- Depends on: S11-F1
- Evidence from our documents: DES line 862 (`origin/master`): "FU-3 | Fine-grained token scope | when the owner moves off the CLI login"; DES line 64: the fallback "if workspace Project access fails (FU-3)". Our risk row RK-11: "`Approved` field or Status allow-list missing in a Project skips every issue silently" (`SPEC.md:655`).
- Concerns: 655 drops the Project read, which removes the Project scope that FU-3 was about. The plan keeps the Project read (S11-F31), so FU-3 stays relevant to the plan. Its trigger ("when the owner moves off the CLI login") has not happened.

### S11-F15 FU-4: alert after three bad cycles
- 655 says: FU-4 (alert after three bad cycles) is carried over (body line 160).
- Status: NOT-COVERED
- Current plan: none found for the alert rule; searched `SPEC.md` for "alert", "alarm", "staleness", "bad cycles". Partial hits only: FR-11 "zero repos served is an alarm" (`SPEC.md:201`) and NFR-04 "unreadable-state alarm" in `status --json` (`SPEC.md:217`). Neither is the three-bad-cycles rule.
- Component (NOT-COVERED only): WATCHER (`status` exit rule; the alert sink could later be shown on the dashboard)
- Feature statement (NOT-COVERED only): make `issue-watch status` read the audit log and exit non-zero after three consecutive cycles that end with exit 3, 4, 5, 6 or 7, and choose where the alert goes.
- Done when (NOT-COVERED only): three scripted failing cycles in a row make `status` exit non-zero, and a good cycle clears it.
- Depends on: S11-F6
- Evidence from our documents: `TECHREF:1953` (D-02): `status` takes the audit log "accepted for the fixed signature and not read"; SETUP section 12 (`origin/master`): "`status` does not read the audit log, so that rule is not built".
- Concerns: the alert sink was never chosen (SETUP section 12). A check running inside the same workspace is silent when the workspace is stopped (same section).

### S11-F16 FU-5: cheaper GitHub reads (conditional requests, ETag)
- 655 says: FU-5 (cheaper GitHub reads, for example conditional requests) is carried over (comment 1 line 94).
- Status: NOT-COVERED
- Current plan: none found; searched `SPEC.md` and `DECISIONS.md` for "ETag", "conditional request", "FU-5", "rate limit". Only FR-09 (info streams off by default, `SPEC.md:199`) and the open check "per-repo `status --json` calls fit the observer's 15-second refresh" (`SPEC.md:678`) touch cost.
- Component (NOT-COVERED only): WATCHER (call budget)
- Feature statement (NOT-COVERED only): use conditional GitHub reads so an unchanged issue list costs no call budget, once call-budget pressure is measured.
- Done when (NOT-COVERED only): a repeat poll with no change spends no more than the minimum calls and the audit line shows `gh_calls` falling.
- Depends on: S11-F5, S11-F11
- Evidence from our documents: DES line 864 (`origin/master`): "FU-5 | ETag conditional reads | call budget pressure"; `TECHREF:1966` (D-15): "No code".
- Concerns: it is a deferred follow-up with a trigger (budget pressure); the plan's multi-repo `run-all` (FR-11) raises that pressure. Do not build before the live capture shows real numbers.

### S11-F17 FU-6: permissions of launched sessions
- 655 says: FU-6 (permissions of launched sessions) is carried over (comment 1 line 94).
- Status: NOT-COVERED
- Current plan: none found for FU-6 itself; searched `SPEC.md` and `DECISIONS.md` for "FU-6", "permission mode", "second approver". Related but different: D05 and FR-30 put every coordinator-started worker under the launch guard (`SPEC.md:81`, `:232`), and D04 passes `--pipeline none` for the claim (FR-51, `SPEC.md:272`). They do not say what permission mode the poll-launched session runs in, or what a second approver changes.
- Component (NOT-COVERED only): WATCHER (launch of the session)
- Feature statement (NOT-COVERED only): read the permission mode of the session the poll launches during the live test, state it in the go/no-go record, and block a second approver until per-actor permission checks exist.
- Done when (NOT-COVERED only): the S17 record names the observed permission mode of the launched session, and adding a second approver is refused or flagged until a check exists.
- Depends on: S11-F10, S11-F28
- Evidence from our documents: SETUP section 14.2 (`origin/master`): "Do not add a second approver before FU-6. Per-actor permission checks inside the launched session are not built."
- Concerns: the plan keeps the approver list (S11-F28), so a second approver stays possible; D01 text says "an allowed approver" (`DECISIONS.md:152`).

### S11-F18 FU-8: automatic launch retry (now the orchestrator's single retry)
- 655 says: FU-8 (automatic launch retry) is carried over, now as the orchestrator's own single retry (comment 1 lines 94 and 96).
- Status: NOT-COVERED
- Current plan: none found; searched for "FU-8", "retry-launch", "retry_argv", "single retry". FR-21 says "an unknown launch receipt never relaunches" (`SPEC.md:211`) and FR-34 restarts a dead coordinator at most 3 times (`SPEC.md:236`); neither is an automatic retry of an unknown launch.
- Component (NOT-COVERED only): WATCHER (launch outcome handling)
- Feature statement (NOT-COVERED only): when a launch outcome is `unknown`, retry once through Orca's operation-id retry (not a fresh launch) after the real argv is confirmed by the live test.
- Done when (NOT-COVERED only): in a live test with a lost reply, one retry with the same operation id produces exactly one session and the entry reaches `claimed` or `failed`.
- Depends on: S11-F10, S11-F2
- Evidence from our documents: `TECHREF:1963` (D-12): "`retry_argv` ... is only printed by `status_report`", "Deferred 'after FU-1 confirms the C20 argv'"; DES line 103 (`origin/master`): the retry flag and unknown-outcome reply shapes "are UNVERIFIED".
- Concerns: FR-21's "never relaunches" must stay true; a retry is allowed only if it cannot make a second session. UNVERIFIED that Orca's retry has that property.

### S11-F19 FU-10: service-level review after 7 days live
- 655 says: FU-10 (service-level review after 7 days live) is carried over (comment 1 line 94).
- Status: NOT-COVERED
- Current plan: none found; searched `SPEC.md` and `DECISIONS.md` for "SLO", "FU-10", "latency", "7 days", "after 7". No hits.
- Component (NOT-COVERED only): WATCHER (`slo_numbers` is a library function in the poll package)
- Feature statement (NOT-COVERED only): after 7 days live, run `slo_numbers` (p95 approval-to-launch, exit-0 share, claimed share, stale count) and review the result with the owner.
- Done when (NOT-COVERED only): a written review of the four numbers exists after the first 7 live days.
- Depends on: S11-F10
- Evidence from our documents: `TECHREF:1954` (D-03): "`slo_numbers` ... have no caller; only `test_slo_helper.py` and an owner-run snippet".
- Concerns: the p95 "approval-to-launch" number assumes the approval step that the plan keeps, not 655's assignment trigger.

### S11-F20 FU-11: size bound for the dispatch store
- 655 says: FU-11 (size bound for the dispatch store) is carried over (comment 1 line 94).
- Status: NOT-COVERED
- Current plan: none found; searched `SPEC.md` for "prune", "tombstone", "1 MiB", "FU-11". FR-22 (backup before a schema migration) is the only store-lifecycle row (`SPEC.md:212`).
- Component (NOT-COVERED only): WATCHER (state files)
- Feature statement (NOT-COVERED only): bound finished tombstone entries in `dispatch.json` once the store passes 1 MiB.
- Done when (NOT-COVERED only): a store seeded above 1 MiB with finished entries is trimmed without losing any entry that blocks a second launch.
- Depends on: S11-F2
- Evidence from our documents: `TECHREF:1965` (D-14): "Only `reset_entry` removes `abandoned`/`unknown`", "Deferred 'when the store is above 1 MiB'".
- Concerns: the plan counts store entries for the in-flight cap and "an unreadable file counts" (FR-33, `SPEC.md:235`), so pruning must not drop an entry that still counts.

### S11-F21 FU-12: check that the state folder is on a local disk
- 655 says: FU-12 (check that the state folder is on a local disk) is carried over (comment 1 line 94).
- Status: NOT-COVERED
- Current plan: none found; searched `SPEC.md` for "local file", "filesystem", "FU-12", "state_dir". NFR-03 only reads the path from config (`SPEC.md:216`).
- Component (NOT-COVERED only): WATCHER (state files and locks)
- Feature statement (NOT-COVERED only): make `check-config` refuse or warn when `state_dir` is not on a local, persistent file system.
- Done when (NOT-COVERED only): `check-config` flags a `state_dir` on a network or non-persistent mount.
- Depends on: S11-F13
- Evidence from our documents: `TECHREF:1966` (D-15): "local-FS allow-list FU-12 ... No code"; DES line 871 (`origin/master`): "FU-12 | Local-filesystem allow-list for `state_dir` | per-host facts gathered".
- Concerns: DES says the allow-list waits on "per-host facts gathered"; no such facts were found in our documents.

### S11-F22 Issue 442's launch checks (OB-H1, OB-H2, OB-H3, OB-CTX) before any real worker
- 655 says: issue 442's launch checks must pass before any governed worker is launched for a real issue (comment 1 line 95; body line 230).
- Status: COVERED
- Current plan: 13.2 "Guard probe (issue 442's twelve observations ...)" (`SPEC.md:706`); FR-30 `WORKER_BINDING_PROVEN` stays false and "refuses a start for any issue outside per-repo `probe_issues`" (`SPEC.md:232`); RK-1 (`SPEC.md:645`); FR-52 (`SPEC.md:273`); D05 (`SPEC.md:81`). The twelve observations are "un-skipped only by the owner" (`SPEC.md:696`).
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: UNVERIFIED: none of the twelve observations has passed (`TECHREF:2001`, U-4).

### S11-F23 Owner question Q1: the one-launch-per-cycle reading
- 655 says: Q1 (one launch per run) is replaced by the new-since-last-poll rule (comment 1 line 96).
- Status: COVERED
- Current plan: D07 keeps "one launch per sweep" (`<W>/debates/D07/VERDICT.md:52`); the in-flight cap starts at 1 (FR-33, `SPEC.md:235`). The built behaviour (a cycle that launches stops after one launch, `TECHREF:910`) stays.
- Depends on: 655 section 1 step 2 (new-since-last-poll rule)
- Evidence from our documents: n/a (COVERED)
- Concerns: the replacement rule (find only what is new since the last poll) is a 655 section 1 feature, not this row. The plan's poll starts work only for approved issues (FR-01), so 655's rule cannot replace Q1 without touching D01.

### S11-F24 Owner question Q2: the full-argv retry form and the orchestrator's own check and single retry
- 655 says: Q2 is answered by the orchestrator's own check and single retry, confirmed by Clay (comment 1 line 96).
- Status: NOT-COVERED
- Current plan: none found; same searches as S11-F18. Nothing in the plan accepts or rejects the full-argv retry form (C20).
- Component (NOT-COVERED only): WATCHER (launch outcome handling)
- Feature statement (NOT-COVERED only): record the owner's answer on the retry form and implement it together with S11-F18.
- Done when (NOT-COVERED only): the retry form is chosen in chat and recorded, and the test of S11-F18 uses that form.
- Depends on: S11-F18
- Evidence from our documents: DES line 873 (`origin/master`): "Q2 accept the full-argv retry form (C20) in place of FR-015's short form."
- Concerns: I found no owner answer to Q2 in the brainstorm folder. UNVERIFIED whether it was answered elsewhere.

### S11-F25 Owner question Q3: the per-issue rate-limit clamp, answered by exponential backoff
- 655 says: Q3 is answered by exponential backoff (comment 1 line 96).
- Status: NOT-COVERED
- Current plan: none found; searched `SPEC.md`, `DECISIONS.md` and the two tech references for "backoff", "exponential", "clamp", "3600". The plan keeps the master code as is (S11-F5). Master has a fixed 10-minute backoff for a failed entry (`TECHREF:826`).
- Component (NOT-COVERED only): WATCHER (rate-limit handling)
- Feature statement (NOT-COVERED only): replace the fixed per-issue rate-limit wait with exponential backoff and a stated ceiling.
- Done when (NOT-COVERED only): a test shows the wait doubling per rate-limit reply up to the ceiling and resetting after a good read.
- Depends on: S11-F5
- Evidence from our documents: DES line 873 (`origin/master`): "Q3 accept the 3600 s clamp for per-issue rate limits (C22)".
- Concerns: 655 does not state the ceiling. UNVERIFIED.

### S11-F26 Owner question Q4: the stderr classifier stays UNVERIFIED until the live test
- 655 says: Q4 is accepted as written (comment 1 line 96).
- Status: COVERED
- Current plan: 13.2 captures real `gh` and Orca replies to replace assumed fixtures (`SPEC.md:705`); SPEC 1.3 and U-2 (`TECHREF:1999`) record the shapes as assumed.
- Depends on: S11-F10
- Evidence from our documents: n/a (COVERED)
- Concerns: UNVERIFIED whether real stderr text matches the classifier; settled only by the live capture.
## Part B: dropped on purpose

### S11-F27 Drop the trigger label (`issue-watch:trigger`)
- 655 says: assignment is the only trigger, so the trigger label goes (comment 1 line 100; body line 161).
- Status: CONFLICT
- Current plan: D01 winning item 7 "Keep the separate `issue-watch:trigger` label for now; dropping it is the owner's decision" (`DECISIONS.md:158`); owner question OA-8 "Keep the trigger label? ... keep `issue-watch:trigger` for now" (`DECISIONS.md:1241`); `SPEC.md:553` "trigger label (OA-8) ... label stays"; OA-28b and FR-82 let `repo_init.py` create the trigger label once per repo on the owner's chat OK (`SPEC.md:119`, `:218`); S17 makes the label on the throwaway repo first (`SPEC.md:501`). 655's version is REJECTED.
- Depends on: S11-F28
- Evidence from our documents: `DECISIONS.md:169`: "UNVERIFIED: ... whether the trigger label can be dropped without changing `approval_of`". `DECISIONS.md:161`: PR 686 "removes the approval, trigger, Project and approver code, so it cannot merge as it stands".
- Concerns: the plan calls the label's removal a later owner decision, so it is not closed for ever. The label is the one GitHub write the plan allows in init (FR-82), which touches the NG-2 rule (poll writes nothing to GitHub).

### S11-F28 Drop the approval label and the approver list
- 655 says: there is no approval step, so no approval label and no approver list (comment 1 line 101; body line 161).
- Status: CONFLICT
- Current plan: D01 winning item 1: work starts only when "an allowed approver's approval (the `Approved` = `Yes` issue field, or the `issue-watch:approved` label until that field is live) is present and unedited since" (`DECISIONS.md:152`); FR-01 "Assignment alone never starts work" (`SPEC.md:191`); FR-02 repeats every start gate at the moment of start (`SPEC.md:192`); `SPEC.md:553` "Approval, not assignment, stays the start gate". Clay's element A12 "assignment alone as trigger" is REJECT (`SPEC.md:447`). 655's version is REJECTED.
- Depends on: none
- Evidence from our documents: `DECISIONS.md:165`: "Dropping approval would remove the only code that ties a person's yes to the issue content (14 predicate symbols, about 30 in `github.py`)." `DECISIONS.md:157` lists four conditions under which assignment alone may be reconsidered: the launch guard refuses when not effective, workers cannot push or merge, the watcher skips an issue that has a claim record or worktree, and the owner records the reversal in chat.
- Concerns: `SPEC.md:553` is the controlling decision; the four conditions of D01 item 6 are the only route back to 655's trigger, and none is met today (RK-2, `SPEC.md:646`).

### S11-F29 Drop FU-9 (approver role check)
- 655 says: FU-9 goes with the approver list because there is no approver to check (comment 1 line 101).
- Status: CONFLICT
- Current plan: the plan keeps the approver (S11-F28), so the reason for dropping FU-9 does not hold. FU-9 itself is not scheduled anywhere (no hit for "FU-9" in `SPEC.md`, `DECISIONS.md` or `FOLLOW-UPS.md`). 655's version is REJECTED; FU-9 stays a deferred follow-up with its own trigger.
- Depends on: S11-F28
- Evidence from our documents: `TECHREF:1966` (D-15): "approver role check FU-9 ... No code"; DES line 868 (`origin/master`): "FU-9 | Approver role check (T14) | approver set grows".
- Concerns: with the approver list kept, a second approver needs FU-6 and FU-9 first (SETUP section 14.2). Neither is in the plan.

### S11-F30 Drop the Backlog requirement
- 655 says: the Project and Backlog requirement goes (comment 1 line 102; body line 161). This row covers the Backlog column only; the Project read is S11-F31.
- Status: COVERED
- Current plan: FR-01 requires Status in "Research, Spec, Plan or Debug"; Backlog never acts (`SPEC.md:191`). DES line 15 (`origin/master`) says the built watcher already "reverses the original issue 331 rule 'Issues must be in Backlog status', by owner decision of 2026-11-18".
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: none

### S11-F31 Drop the Project read (`project_id`, the project-items read) and the Status allow-list
- 655 says: nothing may depend on the board, so `project_id` and the project-items read go (comment 1 line 102).
- Status: CONFLICT
- Current plan: FR-01 requires the Project Status in the allow-list Research, Spec, Plan or Debug (`SPEC.md:191`); D01 winning item 1 (`DECISIONS.md:152`); RK-11 records the risk that a missing Status allow-list "skips every issue silently" and answers it with `status --json` showing the reason per repo (`SPEC.md:655`). 655's version is REJECTED.
- Depends on: S11-F28
- Evidence from our documents: `DECISIONS.md:169`: "UNVERIFIED: ... the shape of `Approved` field timeline events on live GitHub (fixtures were assumed)". `DECISIONS.md:188` (D02 item 7): the setup still needs "the owner-created `Approved` field".
- Concerns: the `Approved` field lives in the Project, so the approval gate (S11-F28) cannot work without a Project read. Dropping the board would remove the approval.

### S11-F32 Drop cron (FU-2); an Orca automation replaces it
- 655 says: cron and its six-field entry (FU-2) are dropped; an Orca automation replaces it (comment 1 line 104; body lines 23 and 161).
- Status: CONFLICT
- Current plan: D02 "Cron stays the scheduler" with one entry every 5 minutes under `flock -n` (`DECISIONS.md:179-182`; `SPEC.md:78`); FR-10 and FR-11 (`SPEC.md:200-201`); Clay element "B2 Orca automation as scheduler" is REJECT and "B1 precheck pattern" is kept only as a fallback (`SPEC.md:449`); the fallback automation is created `--disabled` and enabled only after a scheduled shadow run (`SPEC.md:704`). 655's version is REJECTED. FR-69 corrects the owner's old reason and the six-field cron line (`SPEC.md:326`).
- Depends on: S11-F11
- Evidence from our documents: `DECISIONS.md:184` (D02 item 3): an automation "needs one creation step per Orca host and no boot script exists; one cron entry plus one dispatcher covers all repos with no per-project step". RK-5: "No cron in the image, no `Coordinator` worktree" (`SPEC.md:649`).
- Concerns: D02 confidence is 62 percent and partial (`DECISIONS.md:99`). Cron is not yet in the image (Coder issue 515; UNVERIFIED as built).

### S11-F33 Drop the plan-approval gate (WC-17, the `issue-pipeline` approval rows and `stage-status`, the approval part of guard G2)
- 655 says: the plan is reviewed at creation, so the worker no longer waits for a label or an `approved` comment (comment 1 line 103; body line 161).
- Status: CONFLICT
- Current plan: D03 "Revert PR 682" (`SPEC.md:79`; `<W>/debates/D03/VERDICT.md:9`); D14 (`SPEC.md:90`); FR-31 "When both gates stay (OA-1): record the plan approval, run `check-approval` (WC-17), write the worker's `sessions/<id>.ok` through restored `release-worker`" (`SPEC.md:233`). Appendix B.1: PR 700 restored the package, WC-17 and G2 rule 1 on master (`SPEC.md:758`). 655's version is REJECTED.
- Depends on: S11-F28
- Evidence from our documents: `SPEC.md:554` and `SPEC.md:789`: the owner has not answered OA-1 ("both gates stay or only the start gate"); the revert happened by PR 700 without that answer. `SPEC.md:163`: if only the start gate stays, "the plan-approval package is not restored (section 8.3)".
- Concerns: the plan assumes "both gates stay" but waits for the owner's chat answer to OA-1; until then this row is a recommendation, and an owner answer of "only the start gate" (SPEC section 8.3, `SPEC.md:505`) would remove the plan gate, so 655 could win this one point by that answer.

### S11-F34 Drop FU-7 (revisit D1 and D2)
- 655 says: FU-7 becomes this redesign (comment 1 line 105).
- Status: COVERED
- Current plan: the unification itself revisits the old D1 (where the watcher runs) and D2 (claim only): D01, D02, D04, D07 and D14 (`SPEC.md:77-90`). Clay's "conditions to revisit" are kept (`SPEC.md:447`; `DECISIONS.md:157`).
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: DES line 66 (`origin/master`) lists nine revisit conditions that FU-7 tracked (stopped workspaces, latency, central approval, duplicate claims, account binding, token cannot read Projects, event-time Project changes, shared ledger, recurring execution impossible). The plan does not carry that list. UNVERIFIED whether any of the nine is still wanted.

### S11-F35 Replacement: the plan agent of wave 2 becomes `/sc:issue --plan`
- 655 says: the plan agent of wave 2 is replaced by `/sc:issue --plan` (body line 161).
- Status: COVERED
- Current plan: D12 "Keep PR 661; adapt and merge PR 690" (`SPEC.md:88`); FR-53 to FR-55 (`SPEC.md:274-276`); Clay elements A7 to A10 ADOPT+CHANGE (`SPEC.md:445`); OD-1 gives a `plan_depth` key with default `quick` and no `plan_tier` (`SPEC.md:97`).
- Depends on: 655 section 5 (plan mode)
- Evidence from our documents: n/a (COVERED)
- Concerns: 655 keeps `plan_tier` (default `tier1b`, body line 9); OD-1 rejected it. That difference belongs to 655 section 5.

### S11-F36 Replacement: the orchestrator's own `gh issue close` becomes the closeout
- 655 says: the orchestrator runs no `gh issue close`; the closeout closes (body lines 161 and 226).
- Status: COVERED
- Current plan: FR-38 "call `/sc:closeout <PR>` per merged PR under a go naming the close" (`SPEC.md:240`); OD-10 "One per-PR go bound to the head sha covers merge and close; no standing `issue.close`" (`SPEC.md:106`); FR-07 refuses `issue.close` in fixtures (`SPEC.md:197`); Clay element F1 `/sc:closeout` is ADOPT (`SPEC.md:465`).
- Depends on: 655 section 8 (closeout)
- Evidence from our documents: n/a (COVERED)
- Concerns: the plan needs a typed go for the close; 655 does not. That is a section 8 conflict, not this row.

### S11-F37 Replacement: the eight escalation rules become the nine-row table
- 655 says: the eight numbered escalation rules are replaced by the nine-row table (body line 161).
- Status: COVERED
- Current plan: Clay element D16 "nine-row table" is ADOPT+CHANGE (`SPEC.md:463`); FR-35 to FR-37 (`SPEC.md:237-239`); OD-3 to OD-5 set scope, fail-open and channel (`SPEC.md:99-101`).
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: SPEC resolved contradiction X-5 says entry lines are used "until the whole nine-row list is ruled" (`SPEC.md:606`), so the content of the nine rows is still open and belongs to 655 section 9.

### S11-F38 Safety features of this section keep their tests (acceptance criterion at body line 229)
- 655 says: the safety features of section 11 "still hold and have tests" (body line 229).
- Status: COVERED
- Current plan: 13.1 "Existing tests that must stay green" names `test_security_invariants.py`, `test_launch.py:75`, `test_marker_contract.py`, `test_origin_parity.py`, `test_audit.py` and `test_cycle.py` (`SPEC.md:696`); MC-1 to MC-12 are the common gate (`SPEC.md:692`).
- Depends on: S11-F2, S11-F4, S11-F6, S11-F8, S11-F9
- Evidence from our documents: n/a (COVERED)
- Concerns: no test is named for the call budget or the run lock (see S11-F4, S11-F5, S11-F12).

### S11-F39 Close issue 450 as replaced (acceptance criterion at body line 230)
- 655 says: "#450 is closed as replaced" once the live test, shadow run, lock test and restart test pass (body line 230).
- Status: CONFLICT
- Current plan: L-12 "issue 450 stays open with Clay's 2026-11-18 comment answered" (`SPEC.md:365`); `SPEC.md:553` lists "answer Clay on issue 450 (OA-22)" as an owner action. 655's version is REJECTED.
- Depends on: S11-F10, S11-F11, S11-F12, S11-F13
- Evidence from our documents: `DECISIONS.md:166`: "Clay's comment on the owner's issue 450 (roll-out of the watcher) has no recorded owner answer yet."
- Concerns: the rollout tracking (live test, shadow run, cron) is the content of issue 450, and the plan keeps all of it (S11-F10, S11-F11, S11-F32), so closing 450 would lose the owner's tracker for work that is still open.
<!-- ROWS-END -->

## Section summary
- Most of what 655 carries over is already in the current plan, because the plan also adapts the built issue-watch code: one claim and one start per issue, three wake tries, run lock, call budget, audit log, dry run, integer-only prompt, origin check, live capture of real replies, the 24-hour shadow run and issue 442's guard checks (20 rows COVERED).
- All seven CONFLICT rows are drops that the plan reverses: the trigger label (D01 item 7, OA-8), the approval label and approver list (D01 item 1, FR-01), FU-9, the Project read (FR-01 status allow-list), cron (D02, FR-10), the plan-approval gate (D03, FR-31; the owner's OA-1 answer is still missing) and closing issue 450 (L-12). 655's version of each is rejected.
- Twelve features are not in the plan and go to the backlog. Two are tests (two-process lock test, state-directory restart test); the rest are the deferred follow-ups FU-3, FU-4, FU-5, FU-6, FU-8, FU-10, FU-11, FU-12 and owner questions Q2 and Q3. All twelve belong to the WATCHER.
- Builder cautions: the Backlog drop and FU-7 are COVERED only because the built code and the unification already did them; FU-8 must not break FR-21 ("an unknown launch receipt never relaunches"); the S17 pass list is itself UNVERIFIED (`DECISIONS.md:1119`).
