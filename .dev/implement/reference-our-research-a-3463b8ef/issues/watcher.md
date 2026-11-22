## What was tried
Issue 655 (Clay's design for an issue-polling orchestrator) was split into its 14 sections of the Proposed Solution, and one analyst per section classified every design feature against our current plan (the unification spec and its decision record). Result over all sections: 488 features, 248 already covered by the current plan, 124 in direct conflict (the current plan wins and that part of 655 is rejected), 116 not covered. The not-covered features were sorted into three groups: the coordinator, the watcher and the TUI dashboard. This issue holds the group for the poll that finds assigned issues (`superclaude issue-watch`, `run-all`): 26 classified rows, merged into 15 items below. Of the 116 not-covered rows, 115 appear in the three issues; one row (S10-F60, the ordering step 'wait for additions A to E', already done in Clay's own spec work) was left out because its analyst judged it not a product feature. Rows that said the same thing in several sections of 655 were merged into one item and keep their row ids. Wherever the current plan decided otherwise, the plan was kept and nothing from 655 is requested here. Dashes inside quotes were replaced with hyphens. The classification was done by agents; every `UNVERIFIED` mark in an item is theirs and still open.

## Relevant files and links
- Source design being mined: issue 655 `#655` (IronbellyOrg/IronClaude). Related existing issues: `#409` (TUI dashboard), `#706` (observer follow-up, sub-issue of 409), `#444` (coordinator or sub-orchestrator evaluation), `#450` (watcher rollout), `#665` (21 Medium findings in the 655 plan).
- Sister issues of this split: coordinator {{I_COORD}}, watcher {{I_WATCH}}, TUI dashboard {{I_DASH}}.
- Current plan (local files, not pushed): `.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md` (stages S0 to S17, Appendix B after PR 700), `.dev/brainstorms/20261120-pr686-unify/DECISIONS.md` (43 recorded decisions), `.dev/brainstorms/20261120-pr686-unify/debates/*/VERDICT.md`, `.dev/brainstorms/20261120-pr686-unify/spec/FOLLOW-UPS.md`.
- Per-section analysis with every row, status and evidence (local files, not pushed): `.dev/implement/reference-our-research-a-3463b8ef/sections/section-01.md` to `section-14.md`.
- Pull request 697 (closed unmerged revert of PR 682, replaced after PR 700 by PR 701) and the follow-up issues 698 and 699 come from the same review work.

## Done when
Every item below is built, tested and checked against its own line, or the owner records in chat that it is dropped. Item ids (W1 to W15) are used by the review at the end. The lines called related items are cross-references found in the analysis; they show what to read together, not a strict build order. The build order is in the review.

- [ ] **W1. Switch-on baseline: issues already assigned count as seen, with a hand-over command** (655 section 1; rows S01-F8)
  - What to build: On a repo's first enabled poll, the watcher records every issue that is already assigned and approved as seen so it is never woken or started, and a person can hand one over with `/sc:coordinator --take`.
  - Done when: A dry run on a repo with an already assigned approved issue shows `would_baseline` for it and the real first poll starts no claim for it; once the coordinator command exists (plan stage S14), `--take <owner/repo#N>` on that issue is accepted.
  - Research and debate results from our documents:
    - S01-F8: debates/D01/VERDICT.md:59 "Issues assigned before switch-on are baselined as 'seen' in PR 686 and never woken, so an approved one needs `--take` (INV-009)." - debates/D09/VERDICT.md:34 "a baseline that never touches the 17 already-assigned issues (`:492`)" - debates/D09/VERDICT.md:41 "`--dry-run` that shows the holds before any write, plus the switch-on baseline ... they become the gate in recommendation item 4." - ...
  - Watch out:
    - S01-F8: The baseline is code in PR 686 that the plan adapts; whether the adapted PR keeps it is not stated (UNVERIFIED, PR 686 code not read). The D09 reference to the baseline as the switch-on gate was tied to the label write that was rejected, so the baseline may be dropped by accident unless a requirement names it.

- [ ] **W2. One plan request from the poll after one quiet hour, with the quiet clock, a place in the in-flight count and the plan_stuck reason** (655 section 1, 3, 5, 10, 14; rows S01-F16, S03-F14, S05-F19, S05-F20, S05-F21, S05-F26, S14-F23, S10-F38)
  - What to build: The watcher sends one ids-only plan-request wake item to the repo's coordinator when an assigned issue has failed the plan check for one hour with no change, and counts that open request as in flight.
  - Also in this item:
    - S03-F14: When an assigned issue has stayed in `held_incomplete` for one hour, the poll adds one id-only plan request to the repo coordinator's wake file so the coordinator can run `/sc:issue --plan`.
    - S05-F19: The poll sends one id-only plan-request item to the project's coordinator for an issue that has stayed without a plan for one quiet hour, never twice for the same quiet period.
    - S05-F20: The poll keeps one quiet-since time per unplanned issue and resets it when the issue, a linked branch, a pull request or a session on it changes.
    - S05-F21: An open plan request counts as one in-flight place for its repo and is routed only to the repo's coordinator when a place is free.
    - S05-F26: The poll adds the reason `plan_stuck` to its closed reasons table and raises it when a plan request has had no finish for 60 minutes.
    - S14-F23: When an assigned issue has failed the plan check for one hour with no body change, the poll writes one ids-only plan-request item to the repo's coordinator wake, once per issue and without a GitHub write.
    - S10-F38: When an assigned issue has stayed held for plan reasons for one hour with no sign of plan work, the poll adds exactly one plan request (ids only, never the title) to the wake of the repo's coordinator, and never a second one for that hold.
  - Done when: With a fixture issue that fails the plan check for 60 minutes, the poll writes exactly one wake item of kind plan request (ids only, no title), writes nothing to GitHub, sends no second request on later polls, and the in-flight count includes it.
    - also: a fixture issue held for 61 minutes yields exactly one plan request in the next wake and none in later cycles, and the request carries repo, number and url only.
    - also: a test with a clock shows exactly one plan-request item after 60 quiet minutes, none at 59, none a second time, and the wake file holds only `repo`, `number`, `url`.
  - Related items (read together; the order is in the review at the end): C15
  - Research and debate results from our documents:
    - S01-F16: debates/D15/VERDICT.md:44 "A4 | Plan request after one hour, wake `plan_requests[]` with the issue title | Defer | A wake-file item, not a GitHub write (D09 item 5); a title is free GitHub text (D10 item 5)" - debates/Q03/VERDICT.md:71 "the one-hour plan request remains a wake-file item for D07. Because the wake-time re-check today needs the label ... leaving it unchanged would stop plan requests from ever firing in a ...
    - S03-F14: `.dev/brainstorms/20261120-pr686-unify/debates/D15/VERDICT.md:44` "A wake-file item, not a GitHub write (D09 item 5); a title is free GitHub text (D10 item 5) ... Not built now; if built, ids only and after D07 settles who plans".
    - S05-F19: VERD(D10):18 "The plan-request payload (`plan_requests[]`, with a title) belongs to the plan-hold decision (D09), not to this transport." VERD(D01):16 "the plan request is an agent edit of the issue body, and any body edit after the approval voids it".
  - Watch out:
    - S01-F16: Two traps for the builder. (1) Order: a plan written after approval voids the approval (D01 item 5, SPEC.md:194 FR-04), so a plan request must complete before the person approves. (2) 655's wake carries the issue title; the plan forbids titles in wakes (ids only, DECISIONS.md:418). The "who plans" question (D07) is settled for ...
    - S03-F14: wake items must hold ids only (FR-13, SPEC:203; SEC-16, SPEC:305), so 655's plan request may not carry the issue title.

- [ ] **W3. Configurable poll interval** (655 section 8; rows S08-F3)
  - What to build: Let the owner change the poll interval in one named setting instead of hand-editing the cron line.
  - Done when: after changing the setting to a new value, `crontab -l` (or the dispatcher's own status) shows the new interval and `issue-watch status --json` reports it.
  - Research and debate results from our documents:
    - S08-F3: debates/D02/VERDICT.md:67 "A sweep can last up to about 525 seconds ... against a 300-second tick, so lost ticks can be routine; not measured." A shorter interval makes overlap worse.
  - Watch out:
    - S08-F3: low value. The 270 s cap (SPEC.md line 171) and `flock -n` (FR-10) assume a 5-minute tick; any interval below the sweep time causes skipped ticks, so a floor is needed.

- [ ] **W4. Exponential backoff with a ceiling for GitHub throttling** (655 section 10, 11; rows S10-F9, S11-F25)
  - What to build: When GitHub throttles a read or a launch, the poll waits with an exponentially growing delay (with a ceiling) instead of the fixed header wait or the 3600 s clamp.
  - Also in this item:
    - S11-F25: replace the fixed per-issue rate-limit wait with exponential backoff and a stated ceiling.
  - Done when: a test feeds three consecutive throttled replies and sees the stored `next_permitted_at` grow geometrically up to the ceiling, then reset after one success.
    - also: a test shows the wait doubling per rate-limit reply up to the ceiling and resetting after a good read.
  - Research and debate results from our documents:
    - S10-F9: TECHREF:805 "`rate_limit_wait` (418-431): `Retry-After` or `x-ratelimit-reset` within 1..3600 s gives `rate_limited`, else now + 3600 s `rate_limit_clamped`"; TECHREF:1887 "The reason a live failure produces (`gh_auth_failed`, `rate_limited`, `gh_non_json`, `launch_unknown`) is unverified".
    - S11-F25: DES line 873 (`origin/master`): "Q3 accept the 3600 s clamp for per-issue rate limits (C22)".
  - Watch out:
    - S10-F9: the exact GitHub throttle replies are UNVERIFIED (all 19 reply fixtures are assumed shapes, TECHREF:807); backoff constants would be guesses until the cron shadow run captures real replies (SPEC:705). A header-driven wait is probably more accurate than a blind exponential one, so a builder should keep the header value as a ...
    - S11-F25: 655 does not state the ceiling. UNVERIFIED.

- [ ] **W5. Live firing tests before enabling: two-process lock test and restart test** (655 section 11; rows S11-F12, S11-F13)
  - What to build: before the poll is enabled, hold the poll's lock from one process, start a dry-run cycle in a second, and require the second to exit 75 with reason `lock_held`, then require a normal run after release.
  - Also in this item:
    - S11-F13: before the poll is enabled, restart the workspace and show that `state_dir` and `dispatch.json` still exist with the same `created_at`, because the at-most-once guarantee lives in that directory.
  - Done when: the second cycle prints `lock_held` and exits 75, the audit log carries a `cycle` line with that reason, and a third run afterwards runs normally; the result is in the S17 go/no-go record.
    - also: after a restart the directory and `dispatch.json` exist, `created_at` is unchanged and `issue-watch status` does not exit 6.
  - Related items (read together; the order is in the review at the end): W14
  - Research and debate results from our documents:
    - S11-F12: SETUP section 8.2 (`origin/master`): "The second command must print `cycle: lock_held` and `exit: 75`"; the dry run is used because "while `enabled` is `false`, a run without it stops at `not_enabled` before it reaches the lock".
    - S11-F13: SETUP section 8.3 (`origin/master`): "The at-most-once guarantee lives in the state directory. A new, empty state directory has no memory of earlier launches (risk R5 of the design)."
  - Watch out:
    - S11-F13: this matters more under the plan than under 655, because the plan's store also holds waiting hand-backs and the in-flight count (FR-33, SEC-21).

- [ ] **W6. Shadow-run acceptance check: every cycle ends with exit 0 or a named reason** (655 section 12; rows S12-F25)
  - What to build: After the 24-hour shadow run, every recorded cycle exited 0 or has a named reason from the reasons table (FR-20), and any other exit blocks switch-on.
  - Done when: a script run over the shadow run's `audit.jsonl` and cron log lists zero cycles with an unexplained nonzero exit.
  - Research and debate results from our documents:
    - S12-F25: techref ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md:2215 "`once` exit code = cycle code, crash gives exit 1 with class name only, `status` JSON fields and exit follows age".
  - Watch out:
    - S12-F25: Small gap; easy to fold into the S17 pass list. Cron hides exit 75 under the detach (D02 position, position-CLAY.md:19), so exit codes must be read from `status` and the audit log, not from cron.

- [ ] **W7. Narrower GitHub token scope for the poll (FU-3)** (655 section 11; rows S11-F14)
  - What to build: move the poll off the user's CLI login to a fine-grained token that holds only the read scopes the poll needs, and record those scopes.
  - Done when: the poll runs a full cycle with a token that cannot write to any repo, and `check-config` or the runbook states the scopes.
  - Research and debate results from our documents:
    - S11-F14: DES line 862 (`origin/master`): "FU-3 | Fine-grained token scope | when the owner moves off the CLI login"; DES line 64: the fallback "if workspace Project access fails (FU-3)". Our risk row RK-11: "`Approved` field or Status allow-list missing in a Project skips every issue silently" (`SPEC.md:655`).
  - Watch out:
    - S11-F14: 655 drops the Project read, which removes the Project scope that FU-3 was about. The plan keeps the Project read (S11-F31), so FU-3 stays relevant to the plan. Its trigger ("when the owner moves off the CLI login") has not happened.

- [ ] **W8. Alert after three bad cycles (FU-4)** (655 section 11; rows S11-F15)
  - What to build: make `issue-watch status` read the audit log and exit non-zero after three consecutive cycles that end with exit 3, 4, 5, 6 or 7, and choose where the alert goes.
  - Done when: three scripted failing cycles in a row make `status` exit non-zero, and a good cycle clears it.
  - Research and debate results from our documents:
    - S11-F15: `TECHREF:1953` (D-02): `status` takes the audit log "accepted for the fixed signature and not read"; SETUP section 12 (`origin/master`): "`status` does not read the audit log, so that rule is not built".
  - Watch out:
    - S11-F15: the alert sink was never chosen (SETUP section 12). A check running inside the same workspace is silent when the workspace is stopped (same section).

- [ ] **W9. Cheaper GitHub reads with conditional requests (FU-5)** (655 section 11; rows S11-F16)
  - What to build: use conditional GitHub reads so an unchanged issue list costs no call budget, once call-budget pressure is measured.
  - Done when: a repeat poll with no change spends no more than the minimum calls and the audit line shows `gh_calls` falling.
  - Research and debate results from our documents:
    - S11-F16: DES line 864 (`origin/master`): "FU-5 | ETag conditional reads | call budget pressure"; `TECHREF:1966` (D-15): "No code".
  - Watch out:
    - S11-F16: it is a deferred follow-up with a trigger (budget pressure); the plan's multi-repo `run-all` (FR-11) raises that pressure. Do not build before the live capture shows real numbers.

- [ ] **W10. Permissions of launched sessions (FU-6)** (655 section 11; rows S11-F17)
  - What to build: read the permission mode of the session the poll launches during the live test, state it in the go/no-go record, and block a second approver until per-actor permission checks exist.
  - Done when: the S17 record names the observed permission mode of the launched session, and adding a second approver is refused or flagged until a check exists.
  - Research and debate results from our documents:
    - S11-F17: SETUP section 14.2 (`origin/master`): "Do not add a second approver before FU-6. Per-actor permission checks inside the launched session are not built."
  - Watch out:
    - S11-F17: the plan keeps the approver list (S11-F28), so a second approver stays possible; D01 text says "an allowed approver" (`DECISIONS.md:152`).

- [ ] **W11. One retry of an unknown launch outcome through Orca's operation id (FU-8, owner question Q2)** (655 section 11; rows S11-F18, S11-F24)
  - What to build: when a launch outcome is `unknown`, retry once through Orca's operation-id retry (not a fresh launch) after the real argv is confirmed by the live test.
  - Also in this item:
    - S11-F24: record the owner's answer on the retry form and implement it together with S11-F18.
  - Done when: in a live test with a lost reply, one retry with the same operation id produces exactly one session and the entry reaches `claimed` or `failed`.
    - also: the retry form is chosen in chat and recorded, and the test of S11-F18 uses that form.
  - Research and debate results from our documents:
    - S11-F18: `TECHREF:1963` (D-12): "`retry_argv` ... is only printed by `status_report`", "Deferred 'after FU-1 confirms the C20 argv'"; DES line 103 (`origin/master`): the retry flag and unknown-outcome reply shapes "are UNVERIFIED".
    - S11-F24: DES line 873 (`origin/master`): "Q2 accept the full-argv retry form (C20) in place of FR-015's short form."
  - Watch out:
    - S11-F18: FR-21's "never relaunches" must stay true; a retry is allowed only if it cannot make a second session. UNVERIFIED that Orca's retry has that property.
    - S11-F24: I found no owner answer to Q2 in the brainstorm folder. UNVERIFIED whether it was answered elsewhere.

- [ ] **W12. Seven-day service-level review after the first live enable (FU-10)** (655 section 11, 12; rows S11-F19, S12-F33)
  - What to build: after 7 days live, run `slo_numbers` (p95 approval-to-launch, exit-0 share, claimed share, stale count) and review the result with the owner.
  - Also in this item:
    - S12-F33: Seven days after the first live enable, the owner (or a scheduled agent) reads the watcher's SLO numbers and decides whether to keep it on.
  - Done when: a written review of the four numbers exists after the first 7 live days.
    - also: a dated review entry exists in the ledger or a task, created at switch-on, that cites the four SLO numbers from `slo_numbers`.
  - Research and debate results from our documents:
    - S11-F19: `TECHREF:1954` (D-03): "`slo_numbers` ... have no caller; only `test_slo_helper.py` and an owner-run snippet".
    - S12-F33: techref ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md:1954 "D-03 SLO numbers ... `slo_numbers` (`P/cycle.py:1359`) and `SloNumbers` (`:1339`) have no caller; ... NOT BUILT"; :1990 "FU-10 SLO review ... 'None of these is built by this work' ... FU-10 'after 7 days live'".
  - Watch out:
    - S11-F19: the p95 "approval-to-launch" number assumes the approval step that the plan keeps, not 655's assignment trigger.
    - S12-F33: `slo_numbers` has no caller today, so the review needs a reader first (maybe a status field); the review itself would need the owner's decision. FU-10 was in Clay's "carried over" list (line 160).

- [ ] **W13. Size bound for the dispatch store (FU-11)** (655 section 11; rows S11-F20)
  - What to build: bound finished tombstone entries in `dispatch.json` once the store passes 1 MiB.
  - Done when: a store seeded above 1 MiB with finished entries is trimmed without losing any entry that blocks a second launch.
  - Research and debate results from our documents:
    - S11-F20: `TECHREF:1965` (D-14): "Only `reset_entry` removes `abandoned`/`unknown`", "Deferred 'when the store is above 1 MiB'".
  - Watch out:
    - S11-F20: the plan counts store entries for the in-flight cap and "an unreadable file counts" (FR-33, `SPEC.md:235`), so pruning must not drop an entry that still counts.

- [ ] **W14. check-config refuses a state folder that is not on a local disk (FU-12)** (655 section 11; rows S11-F21)
  - What to build: make `check-config` refuse or warn when `state_dir` is not on a local, persistent file system.
  - Done when: `check-config` flags a `state_dir` on a network or non-persistent mount.
  - Related items (read together; the order is in the review at the end): W5
  - Research and debate results from our documents:
    - S11-F21: `TECHREF:1966` (D-15): "local-FS allow-list FU-12 ... No code"; DES line 871 (`origin/master`): "FU-12 | Local-filesystem allow-list for `state_dir` | per-host facts gathered".
  - Watch out:
    - S11-F21: DES says the allow-list waits on "per-host facts gathered"; no such facts were found in our documents.

- [ ] **W15. Update the owner runbook to the unified design after the live test** (655 section 13; rows S13-F22)
  - What to build: After the S17 live tests, update the owner runbook (`docs/designs/issue-watcher-setup.md` and the issue 442 runbook) to the unified design as run, with the real captured steps.
  - Done when: A merged PR changes the runbook text and the S17 record names the PR; a person can follow it to switch a repo on and off.
  - Research and debate results from our documents:
    - S13-F22: SPEC.md:69 "PR B (coordinator skill) and PR E (runbook rewrite) are unbuilt."
  - Watch out:
    - S13-F22: SPEC.md:569 gates PR E on the design amendment; it is not stated whether the plan keeps the name "PR E".

## Pick-up note
Nothing here is built. Do not start an item before the stage of the current plan that it extends has landed (see the review below). Every GitHub call for this work passes `--repo IronbellyOrg/IronClaude`. Where an item says UNVERIFIED, check it first. The plan and analysis files named above are local and not pushed to GitHub; the quotes in each item are what a reader of this issue has.

### Review of the three issues together

The split gives three issues: coordinator {{I_COORD}} (items C1 to C27), watcher {{I_WATCH}} (items W1 to W15) and TUI dashboard {{I_DASH}} (items D1 to D4). The dashboard group is small on purpose: issue 655 is mostly about the poll and the coordinator, and only the work-report entries reach what the owner sees. Assumption: "the observer" in the request was read as the watcher, because the request listed dashboard, watcher and coordinator as the three groups. If the third issue was meant to be the observer screen, retitle {{I_WATCH}} and move its items into the dashboard group; issues #409 and #706 already hold the observer work. One more reading: "with all features from our list" was taken as all not-covered features of that group.

**How the items relate**

1. The plan request crosses two issues. W2 (the poll sends one id-only plan request after one quiet hour) writes a wake item, and C15 (the coordinator saves its own record, acknowledges, then runs `/sc:issue --plan`) reads it. They share the wake item format and the closed table of reasons, and the hold-lifecycle test (T11) needs both. Fix the item format in the watcher change first, then build the consumer.
2. The coordinator issue has three phases. Phase 1 is the skeleton: C1, C2, C4 and C6 (skill layout, STOP codes, loading Orca's own skill, verb list). Phase 2 is one cluster that must be built together, because its items refer to each other: C5 (Run binding, whose check needs the coordinator's own worker start), C7 to C15 (worker start, issue-body hash, handoff template, check-ins, worker_done, playbook, decision gates, report entry, plan request), C19 (settling a worker), C3 (the return contract that reports what C19 settles), C25 (template tests) and C27 (the capped notice after an escalation entry). Phase 3 is C16 to C18 and C20 to C24 (merge gate and safety files, hand-back, limits, text hygiene, tiers, repo overview, spec home). C26 (build process) applies to every pull request. The lines called related items in each item are cross-references, not a strict order; the order is this one.
3. D2 (entry shows links and "no live session") repeats part of C14 (report entry content). Build the entry content once in C14; D2 then only adds the display.
4. One owner decision gates the report items: restore the report skill from the archive branch or not (SPEC Appendix B.3, action 1). D1 and D2 cannot be built until the skill is restored. C14 and the entry line of C8 write into the same report entry, so they need the same decision before they are built. D3 starts with an owner decision (where the report session and its state live), and its config change and test wait for the restore like D1 and D2. D4 has two parts: the owner's answer on which copy runs the daily report can be given now, and its diff check waits for the restore.
5. In the watcher issue, W14 (refuse a state folder that is not on a local disk) lands before W5 (lock and restart tests), because the restart test relies on a local, persistent state folder. W5 and W6 (shadow-run check) are gates before the first live enable. W3 and W8 are independent early items. W1 is independent for its baseline part; its hand-over check with `--take` waits for the coordinator command (plan stage S14). W4 (backoff) and W9 (conditional reads) wait for real GitHub replies captured in the live test and the shadow run, because their constants and savings are guesses until then. W7 (narrower token) waits for its trigger, the owner moving the poll off the CLI login, and W13 (store size bound) waits for its trigger, the store passing 1 MiB. W10 and W11 need output captured in the live test. W12 starts seven days after the first live enable. W15 comes after the live test.
6. Every item extends a stage of the current plan: watcher items extend S11 and S12 (PR 686 adapted), coordinator items extend S13 to S15 (substrate, merge path, transport, hand-back, report entry), dashboard items extend S16 (observability), and the gates W5 and W6 belong to S17 (live tests). No item starts before its stage has landed.

**Order to complete the issues**

1. Watcher, first part: W1 (baseline part), W2, W3, W8 and W14, with W2 defining the plan-request wake item.
2. Coordinator phase 1, then phase 2, then phase 3, as in point 2.
3. TUI dashboard: the owner decisions of D3 and the first part of D4 any time; D1, D2, the config change and test of D3 and the diff part of D4 after C14 and the report-skill restore.
4. Watcher, second part: W5 and W6 as the gates before enabling, then W4, W9, W10, W11 and W15 after the live test and shadow run, then W12 seven days after the first enable; W7 and W13 only when their triggers occur.

So the watcher issue is opened first and closed last, the coordinator issue sits in the middle, and the dashboard issue is finished after the coordinator's report entry exists.

**Decisions and risks that block items**

- The owner decides whether to restore the report skill (blocks D1, D2, the config change of D3, the diff part of D4 and the report-entry items C14 and C8) and where the report session and its state live (D3).
- The home of the coordinator spec (C24) needs one owner-named place.
- The classification was made by agents. A separate reviewer agent spot-checked about 30 not-covered rows against the plan in two passes and found none already covered (one, the quiet clock inside W2, is partly covered by the plan's hold decision); treat any item whose evidence says UNVERIFIED as open until read against the code.
