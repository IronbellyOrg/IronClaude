# Section 10 analysis: Clay's rulings (2026-11-18 and 2026-11-19)
Counts: COVERED 29, CONFLICT 23, NOT-COVERED 10 (62 rows)

Sources read. Issue 655 body: /home/coder/workspaces/IronClaude/.dev/implement/reference-our-research-a-3463b8ef/inputs/issue-655-body.md (lines 1-30, section 10 at 142-157, acceptance criteria 213-230, plus lines 60-66, 104, 112, 121-138 for the text the rulings point at). Comments: .../inputs/issue-655-comments.md (comments 7, 8, 13, 14, 15). Current plan: SPEC = /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md, DEC = .../DECISIONS.md, D15 = .../debates/D15/VERDICT.md, QG2 = .../debates/QG2/VERDICT.md, TRIAGE = .../debates/OA-TRIAGE.md, TECHREF = .../techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md. All plan verdicts are recommendations until the owner rules in chat (SPEC line 7); "current plan wins" is applied as the owner asked. Nearly all of Clay's rulings are Clay's, not the owner's (DEC line 340, QG2 line 63).

Acceptance criteria of 655 that touch this section: line 215 (Orca automation, no cron), 216 (one orchestrator per repo, 3 in flight), 218 (claim once, worker once), 222 (hourly worker check, no session manager, one interrupt), 223 (worker pushes, only the orchestrator merges, review agents), 224 (what reaches Clay, release needs OK), 225 (limits, one interrupt), 226 (closeout and hand-back), 227 (audit, changes_requested, merge-safety hold), 229 (no trigger label, approval label, approver list, Project, plan-approval gate), 230 (live test, shadow run). They are cited inside the rows below.

## Rulings of 2026-11-18 (body lines 144-149)

### S10-F1 Assignment is the only trigger (no trigger label, approval label, approver list or plan-approval gate after the claim)
- 655 says: "The only trigger is assignment: no trigger label, no approval label, no approver list, no plan-approval gate after the claim" (body line 146; acceptance line 229 says none of these may remain).
- Status: CONFLICT
- Current plan: SPEC FR-01 (SPEC:191) "Assignment alone never starts work": a worker starts only if the issue is open, assigned only to the watcher login, approved (field `Approved`=Yes, label until the field is live) and unedited since, Status in Research, Spec, Plan or Debug, no `hold:backlog`, plan check passing. Decision D01 (DEC:149-157, SPEC:77), Clay element A12 "Assignment alone as the trigger: REJECT" (SPEC:447, D15:52). The post-claim plan-approval gate also stays: both gates stay, OA-1 SETTLED (TRIAGE:14), and PR 700 put the `issue_pipeline` package, WC-17 and guard rule 1 back on master (SPEC:758, 776). OA-8 keeps the trigger label for now (TRIAGE:21, SPEC:553). Clay's own "conditions to revisit" are kept as the four conditions under which assignment alone may be reconsidered (DEC:157): guard effective, workers cannot push or merge, skip when a claim record or worktree exists, owner records the reversal in chat.
- Evidence from our documents: DEC:152 "Assignment alone never starts work. A worker starts only when: ... an allowed approver's approval ... is present and unedited since". 655's version is REJECTED. D01 is partial, 78% (DEC:169).
- Concerns: the owner has not yet ruled in chat on OA-1 or OA-8 (they are verdict-settled, not owner-answered; SPEC:554 and Appendix B.3 item 4 say the answer is recorded after the fact). If the owner later reverses, the four conditions of DEC:157 are the entry test.

### S10-F2 Safety rationale: only users with triage or write access can assign an issue
- 655 says: assignment is a safe trigger because only users with triage or write access can assign an issue, "stated by the owner; UNVERIFIED here" (body line 146).
- Status: CONFLICT
- Current plan: not used as a basis. D01 lists "whether a read-only user can self-assign an issue" as UNVERIFIED (DEC:169), and the plan reads the matter the other way: "A hand claim assigns the issue, so 'assigned' cannot be shown as 'approved'" (DEC:164). The approval requirement (FR-01) replaces the rationale. Also, one login serves the person and every agent (DEC:251), so who assigned cannot prove that a person decided.
- Evidence from our documents: DEC:164 "A hand claim assigns the issue, so 'assigned' cannot be shown as 'approved'."; DEC:223 "a GitHub comment 'by ironbelly' cannot prove who acted because one login serves the person and the agents".
- Concerns: the claim is unverified in both documents; do not build anything on it.

### S10-F3 The plan hold is a precondition, not a trigger
- 655 says: the hold of section 1 is a precondition, not a trigger (body line 146; section 1 step 3, body line 25).
- Status: COVERED
- Current plan: FR-05 (SPEC:195) runs a read-only plan check on the body before the approval read, skipping as `held_incomplete`; `hold:backlog` skips as `held_backlog`; D09 items 1-2 (DEC:386-387), D15 rows A1 and A3 ADOPT+CHANGE (SPEC:441). So the hold is one more gate in front of the approval, never a trigger.
- Evidence: n/a (covered). The label write that 655 attaches to the hold is a separate row (S10-F35).
- Concerns: the plan check proves presence, not quality ("TBD" passes unless the placeholder rule is added; DEC:483, FR-54 SPEC:275).

### S10-F4 The Backlog column may stay, but nothing may depend on it
- 655 says: "The Backlog column may stay on the board, but nothing may depend on it" (body line 147; acceptance line 229 "no ... Project or Backlog read").
- Status: CONFLICT
- Current plan: FR-01 (SPEC:191) requires the Project Status to be in the allow-list Research, Spec, Plan or Debug (rule R22), so a Backlog issue is skipped; the plan also writes the board: FR-83 moves Status to `In review` after a succeeded `worker_done` (SPEC:243). D01 refuses the removal of the Project code (DEC:165 "14 predicate symbols, about 30 in `github.py`"). A3 note: "runbook says Status Backlog is already outside the allow-list" (D15:43).
- Evidence from our documents: DEC:152 "the Project Status is in the allow-list Research, Spec, Plan, Debug". 655's version is REJECTED.
- Concerns: none beyond S10-F1.

### S10-F5 An Orca automation runs the schedule, not cron
- 655 says: "An Orca automation runs the schedule, not cron" (body line 147; section 1 step 1, body line 23; acceptance line 215 "no cron entry exists"; line 230 shadow run).
- Status: CONFLICT
- Current plan: D02 (DEC:175-202, SPEC:78): cron stays the scheduler, one entry `*/5 * * * *` under `flock -n`; FR-10 (SPEC:200) "Run from one cron entry"; FR-11 (SPEC:201) cron calls `issue-watch run-all`; Clay element B2 "Orca automation as the scheduler: REJECT" (D15:59, SPEC:449). Clay's precheck automation survives only as a tested-first fallback: created `--disabled` by the owner, precheck always returns 1, enabled after a scheduled shadow run (DEC:185, SPEC:704).
- Evidence from our documents: DEC:196 "both advocates called it a toss-up (about 50 and 55 percent)"; D02 confidence 62%, partial (DEC:198); DEC:198 "UNVERIFIED: that an automation fires headless on this host; the 100-row cap, 720-minute catch-up". The owner's written reason "automations start an agent on each run" is wrong in one place and must be corrected (FR-69, SPEC:326), so the CONFLICT is about the choice, not about that reason.
- Concerns: the debate was a near toss-up and a firing test is required before the fallback is allowed (SPEC:704). Cron is not yet in the Coder image (Coder issue 515) and the `Coordinator` worktree is Coder 516 (SPEC:62), so scheduling needs those first. Clay's runbook steps that create `orchestrator-poll` are replaced.

### S10-F6 Unknown launch outcome: the system checks for the session itself
- 655 says: "If a launch outcome is unknown, the orchestrator checks for the session itself" (body line 148).
- Status: COVERED
- Current plan: an `unknown` store entry moves to `claimed` when the entry's own claim marker is seen (TECHREF:830, T-10 to T-12, "own claim marker seen"); FR-03 keeps `marker_in_window` (SPEC:193); FR-21 (SPEC:211) keeps claim evidence and replays the wake. The check is done by the poll plus the coordinator's wake pull (FR-28, SPEC:230), not by a person.
- Evidence: n/a (covered).
- Concerns: the check is made by the poll and by the claim marker, not by an "orchestrator" session looking for the session. The effect is equivalent.

### S10-F7 Unknown launch outcome: retry once automatically
- 655 says: if the outcome is unknown, the orchestrator "retries once" (body line 148; comment 7 says this is the owner design's Q2 and FU-8 "automatic launch retry; now the orchestrator's own single retry").
- Status: CONFLICT
- Current plan: FR-21 (SPEC:211) "an unknown launch receipt never relaunches"; at-most-once rule in master: `unknown` leaves only by a person's `reset N --forfeit-guarantee` (TECHREF:1627, record.py:706-720). The brainstorm confirmed it is already built at store level (/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/brainstorm/run/nested/adversarial-1/adversarial/rounds/round2-advocate-1-opus-architect.md:57 "`record.py:447-448` ... `unknown` leave otherwise only by a person's `reset N`"). FU-8 auto-retry is NOT BUILT and deferred "after FU-1 confirms the C20 argv" (TECHREF:944, 1963).
- Evidence from our documents: TECHREF:1627 "`pending`, `launched`, `unknown`, `abandoned`, `claimed` are never relaunched; only `reset N --forfeit-guarantee` removes `abandoned` or `unknown`". 655's version is REJECTED.
- Concerns: a retry after an unknown launch can start a duplicate claim session. The plan's debate treated "unknown launch means no second claim" as a required safe result (.../brainstorm/run/nested/adversarial-1/adversarial/rounds/round1-advocate-3-haiku-backend.md:37).

### S10-F8 No command is printed for a person
- 655 says: "no command is printed for a person" when a launch outcome is unknown (body line 148).
- Status: CONFLICT
- Current plan: master `status` prints the retry command: `retry_argv` (launch.py:119-132) "is only printed" (TECHREF:944, 1963); the person's `reset N` is the exit from `unknown`. No SPEC requirement removes it.
- Evidence from our documents: TECHREF:1963 "`retry_argv` ... is only printed by `status_report` (`P/cycle.py:1308-1312`) ... Deferred 'after FU-1 confirms the C20 argv'".
- Concerns: depends on S10-F7 (with no automatic retry, a person is the only way out of `unknown`). Weaker conflict than F7: nothing in the plan forbids dropping the printed line once an automatic path exists.

### S10-F9 GitHub throttling uses exponential backoff
- 655 says: "GitHub throttling uses exponential backoff" (body line 148; comment 7: owner design Q3 "is answered by exponential backoff").
- Status: NOT-COVERED
- Current plan: none found; searched SPEC for "throttl|backoff|rate.limit|exponential" (no hit), DEC and all VERDICT files (only D07 mentions "rate-limit wait" of the existing dispatcher), TECHREF. Master already handles throttling a different way: `rate_limit_wait` takes `Retry-After` or `x-ratelimit-reset` within 1..3600 s, else clamps to now + 3600 s, stored in `next_permitted_at`, exit 5 (TECHREF:805, 1631); failed launches wait a fixed 10 minutes (TECHREF:826, 1677). D07's Clay position says the poll keeps the existing rate-limit code (/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D07/position-CLAY.md:31).
- Component: WATCHER (poll behaviour, call budget).
- Feature statement: When GitHub throttles a read or a launch, the poll waits with an exponentially growing delay (with a ceiling) instead of the fixed header wait or the 3600 s clamp.
- Done when: a test feeds three consecutive throttled replies and sees the stored `next_permitted_at` grow geometrically up to the ceiling, then reset after one success.
- Depends on: none.
- Evidence from our documents: TECHREF:805 "`rate_limit_wait` (418-431): `Retry-After` or `x-ratelimit-reset` within 1..3600 s gives `rate_limited`, else now + 3600 s `rate_limit_clamped`"; TECHREF:1887 "The reason a live failure produces (`gh_auth_failed`, `rate_limited`, `gh_non_json`, `launch_unknown`) is unverified".
- Concerns: the exact GitHub throttle replies are UNVERIFIED (all 19 reply fixtures are assumed shapes, TECHREF:807); backoff constants would be guesses until the cron shadow run captures real replies (SPEC:705). A header-driven wait is probably more accurate than a blind exponential one, so a builder should keep the header value as a floor.

### S10-F10 An unrecognized GitHub error is a login failure until the live test shows the real text
- 655 says: "an unrecognized GitHub error is a login failure until the live test shows the real text" (body line 148; also body line 302).
- Status: COVERED
- Current plan: built behaviour kept as the base: a `gh` read failure that is not recognized stops the cycle fail closed with exit 3 (`login_invalid`, `gh_auth_failed`, `gh_timeout`, `gh_non_json`, `project_read_failed`; TECHREF:862, 1505 "fail closed: skip or stop; no write happens"); the error strings (`GH_ERROR_SIGNS`) are marked `[UNVERIFIED]` in source (TECHREF:804). SPEC 13.2 "Cron shadow run" captures real replies "to replace assumed fixtures" (SPEC:705).
- Evidence: n/a (covered).
- Concerns: no SPEC requirement states the rule in words; it rests on the retained built code and the live capture. The reason name differs (`gh_auth_failed` rather than a "login" reason). Same effect.

### S10-F11 The poll sends data to an agent only when something new arrived
- 655 says: "The poll sends data to an agent only when something new arrived" (body line 149; acceptance line 215 "With nothing new a cycle starts no agent and spends no model tokens").
- Status: COVERED
- Current plan: the poll is a cron-run script with no model (FR-10, SPEC:200); it starts a claim session only for an issue passing FR-01 and writes a wake file only after a claim marker is seen (SPEC:125, FR-13 SPEC:203, FR-21 SPEC:211); the info streams that would pass on extra items are off by default (FR-09, SPEC:199; OD-9, DEC:893).
- Evidence: n/a (covered).
- Concerns: Clay's "new since the last poll" rule replaces the old "one launch per run" rule (comment 7, Q1); the plan keeps the built `considered` stamp and at-most-once store instead (TECHREF:748, 1627). Same effect.

### S10-F12 The live test uses throwaway issues
- 655 says: "The live test uses throwaway issues that are only assigned" (body line 149; acceptance line 230 live test, shadow run, lock test, restart test).
- Status: COVERED
- Current plan: S17 and OA-19 "at most one throwaway repo after the shadow run, cap 1" (SPEC:582, 585); guard probe on a "throwaway issue and repo" (SPEC:706); 13.2 shadow run, lock and restart checks (SPEC:704-713); D15 G1 "setup step approving the throwaway issue on rows that start a worker" (D15:129).
- Evidence: n/a (covered).
- Concerns: "only assigned" cannot hold under the plan: a throwaway issue also needs the approval, an allowed Status and filled plan sections (S10-F1, F4). Builders must write the live-test setup accordingly.

## Rulings of 2026-11-19: report and people (body line 153)

### S10-F13 The report is a living document (ruling 1)
- 655 says: "the living report (1)" (body line 153; section 1 step 7, body line 29; acceptance line 221: entry added at claim, updated at milestones only, removed at close; the daily run no longer touches issue entries).
- Status: COVERED
- Current plan: D11 item 4 "living report adopted with change (per-user state path, entries store only `session_id`)" (DEC:450); FR-45 (read transcripts for sweep session ids plus every not-done session of the previous report), FR-46 (remove `"person": "clayphi"`, per-user state path), FR-48 (`report-entry` the only writer of an entry file) (SPEC:256-259); D15 rows E1 and E2 (SPEC:464).
- Evidence: n/a (covered).
- Concerns: PR 700 removed the `agent-work-report` skill from master, so FR-45, FR-46 and FR-48 are "blocked until the skill is restored" (SPEC:778). Restoring it from `clayphi/archive-orchestrator-655-20261120` is an open owner decision: Yes means the D11 adoption proceeds, No means FR-45, FR-46, FR-48 are dropped or rewritten (SPEC:786, Appendix B.3 item 1). Treat this row as covered only if the owner says Yes.

### S10-F14 No session manager, ever: the coordinator does every check-in and typing itself (ruling 2)
- 655 says: "no session manager, ever (2)" (body line 153; acceptance line 222 "There is no session-manager skill: the orchestrator does every check-in itself, typing and approvals included").
- Status: COVERED
- Current plan: the coordinator itself types into worker terminals under four typing rules (FR-14 and FR-40, SPEC:204, 242; D15 row D14 ADOPT+CHANGE, D15:98); one supervised `worker-start` route with check-ins and restart (D15 row D12, D15:96). No separate session-manager component exists in the plan; D08 lists only coordinator kinds (DEC:357).
- Evidence: n/a (covered). The approving-permission-prompts part of the same ruling is a separate row (S10-F15).
- Concerns: issue 339's "close or resume an idle session" duty is NOT built and stays open under issue 339 as an "all-sessions coordinator" (/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D13/VERDICT.md:28). "Ever" is stronger than the plan, which leaves 339 open for a later idle-session manager.

### S10-F15 The coordinator approves a worker's permission prompts (detail of ruling 2, FR-24 of Clay's spec)
- 655 says: the orchestrator does "typing into a worker's terminal and approving its permission prompts under the FR-23 and FR-24 rules" (comment 13 item 2; body line 121 "approving a permission prompt under FR-24 when the action is not in rows 1 to 7"; acceptance line 222).
- Status: CONFLICT
- Current plan: D15 row D14 "Reject approving permission prompts (WC:122, WC:137); drop approval rules and test cases" (D15:98); FR-40 "Type into worker terminals only under the four typing rules (never approve a permission prompt)" (SPEC:242).
- Evidence from our documents: D15:98 "Typing rules 1, 2, 3, 5 add conditions at no cost (G-5) ... Reject approving permission prompts". 655's version is REJECTED.
- Concerns: this leaves a worker blocked on a permission prompt with only the escalation path; the plan has no replacement for the unstick-by-approval case (nothing in SPEC or DEC says what the coordinator does instead beyond escalating).

### S10-F16 Only the user's own GitHub login counts, no bot list (ruling 11)
- 655 says: "only the user's own GitHub login counts, no bot list (11)" (body line 153; section 1 step 2, body line 24; comment 13 item 10 "Bots dropped").
- Status: COVERED
- Current plan: FR-01 requires the issue to be "assigned only to the watcher login" (SPEC:191); master `is_intended_owner` carries it (/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/brainstorm/run/merged-requirements.md:165). No bot list exists in the plan.
- Evidence: n/a (covered).
- Concerns: the plan is stricter: "assigned ONLY to the watcher login" means an issue also assigned to another person is skipped (`assigned_other`, TECHREF:929). 655 only says assigned to the user. Also the plan separately tracks the approvers (an approver list and role check FU-9 not built, TECHREF:944), which is a different list from Clay's bot list.

### S10-F17 The agent is never named in anything user-facing; people by name (ruling 15)
- 655 says: "the agent is never named in anything user-facing, people by name (15)" (body line 153; also body line 62 `names.py` "no agent or model is named in anything user-facing"; comment 15 item 3).
- Status: CONFLICT
- Current plan: OD-3 scope B (DEC:797, SPEC:99, QG2:12): the rule scans only the coordinator's own two writers, `report-entry` and `escalate`; workers' PR bodies keep today's practice; U54 (false-refusal count over the last 50 titles) must be measured before the check is switched on; D15 row D19 "Naming rule 5.12: DEFER" (D15:103). OD-4 (SPEC:100): a refused mandatory escalation fails open, with a visible marker and the original in the log. FR-37 (SPEC:239) and FR-47 (SPEC:258, "the person" instead of Clay).
- Evidence from our documents: QG2:12 "no check can read a worker's PR body before it is written (D:847), 25 of the last 30 merged PR bodies carry 'Generated with' ... and ruling 15 is Clay's ruling, not shown to be an owner ruling"; QG2:63 "The owner has not ruled on the naming rule at all; rulings 15, 27, 28 and 39 are Clay's."
- Concerns: scope A would contradict current practice (25 of the last 30 merged PR bodies carry "Generated with", QG2:12), and 655 itself allows one commit trailer "this repository's practice puts on commits" (body line 66). The plan's default B is the one the owner has not yet confirmed in chat (QG2:49 lists it as a pending owner answer). "People by name" conflicts with FR-47's "the person" wording; the plan picked a neutral word on purpose.

### S10-F18 Plain English, no em or en dashes, no secrets in what the orchestrator writes (ruling 17)
- 655 says: "plain English, no em or en dashes, no secrets (17)" (body line 153; the handoff template says "never print secrets", body line 66; escalation row 2 "a secret", body line 128).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC for "dash|plain English|secret|credential" (only the SPEC's own "In plain English" heading at SPEC:123 and the spec-writing rule in /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC-BRIEF.md:32 "No em dashes or en dash ranges. Plain English", which governs the spec document, not the coordinator's output), DEC, all VERDICT files, FOLLOW-UPS. The nearest mechanism is the naming scan on `report-entry` and `escalate` (FR-37, SPEC:239), which checks agent names only.
- Component: COORDINATOR (the writers `report-entry`, `escalate` and the four templates).
- Feature statement: Every text the coordinator writes for a person (report entries, escalations, handoff prompts, PR and issue text) is checked for em dashes, en dashes and for secret-like strings, and a failing text is fixed or masked before it is sent.
- Done when: a test feeds `report-entry` and `escalate` a text with an em dash, an en dash and a token-shaped string and each is rejected or masked with a visible marker, while a normal sentence passes.
- Depends on: S10-F17 (same writers, same fail-open question OD-4); 655 section 4 templates.
- Evidence from our documents: DEC:198 "A debate subagent printed the local Orca auth token into its own transcript" (a real secret leak in this very work); QG2:18 "A style failure is logged, never a block" (OD-4 fail open for naming).
- Concerns: a secret scan must not itself print the secret into a log; per OD-4 a fail-open mask keeps "the original match ... in the action log", which would store the secret, so secrets need fail-closed with no logging of the match (opposite to the naming rule). False positives on dash scans are low, on secret scans high (the U54 measurement shows the same risk for names).

## Rulings of 2026-11-19: workers and merging (body line 154)

### S10-F19 Workers push their own branch and open pull requests (rulings 3 and 13)
- 655 says: "workers push and open PRs, never merge or force-push; only the orchestrator merges (3, 13)" (body line 154; comment 13 item 3; acceptance line 223 "The worker pushes its own branch and opens its pull request").
- Status: CONFLICT
- Current plan: E-1 (SPEC:626): a coordinator-started worker is bound at W and released to WA, never at FS; "WC:245 and D06 item 5 forbid a worker push without the go". FR-32 (SPEC:234): the coordinator commits the result after `worker_done` and pushes only on a person's typed go; "the coordinator never types" the run line. Q04 / SEC-22 (SPEC:311, DEC:741-743): a push needs a person's typed go, except the person's own typed `/sc:pr-submit --monitor 3` line (or the Full Submit field) for that one run; "a worker never runs `/sc:pr-submit` (Clay's ADD1 stays rejected)" (DEC:743, D06 item 5 DEC:297).
- Evidence from our documents: SPEC:626 "D06 and D04: a worker never pushes except on a person's go". 655's version is REJECTED.
- Concerns: SEC-13 (SPEC:302) says a worker's own script can still push a feature branch or open a PR and the guard only "narrows honest drift"; the push would not be stopped, only not authorized. The guard has never bound a `worker-start` worker (SPEC:57, RK-1 SPEC:645), so until the live probe passes the real state is unguarded.

### S10-F20 Workers never merge and never force-push (rulings 3 and 13)
- 655 says: workers "never merge or force-push" (body line 154; acceptance line 223).
- Status: COVERED
- Current plan: guard level FS "never merge, never push to `master`" (DEC:266); SEC-22 fence "no force push, no push to the default or a protected branch" (SPEC:311); D01 condition "workers cannot push or merge" (DEC:157); worker never runs `/sc:pr-submit` or `/sc:closeout` (SEC-05, SPEC:294).
- Evidence: n/a (covered).
- Concerns: the plan states this "narrows" and does not "close" the risk: with admin bypass on the shared login a script can still run `gh pr merge --admin` and `master` is unprotected (SEC-13, SPEC:302; SPEC:48). Clay's rule is a contract line, the plan's is a contract plus guard plus a ruleset that does not exist yet (FR-75, OA-5).

### S10-F21 Only the orchestrator merges, with no person's go (rulings 3 and 13)
- 655 says: "only the orchestrator merges (3, 13)" and merges "when every merge condition holds" (body line 154 and line 121; acceptance line 223; "Merging and closing issues are not in the table (ruling 13)", body line 138).
- Status: CONFLICT
- Current plan: SEC-01 (SPEC:290) "Merge only on a person's typed go for that PR naming repo, PR, full 40-character head sha, method, the word 'merge' and the gate output ... A passing gate never triggers a merge." D06 item 1 (DEC:293), D07 element "standing `pr.merge` and `issue.close`; autonomous merge: REJECT" (D15:91, SPEC:458), SEC-06 (SPEC:295) no standing `pr.merge`. The coordinator "prepares, checks and waits"; Clay's wave 7 autonomous merge becomes "show the gate output and wait for the go" (DEC:306).
- Evidence from our documents: DEC:306 "Clay's throughput gain is given up (no measured figure exists)"; D15:91 "a person's go is the only brake on an unprotected `master`". 655's version is REJECTED.
- Concerns: 655 comment 15 itself says that for this build "no pull request is merged by the orchestrator session or any worker ... Clay does the QA and the merge", which matches the plan. Merge automation may only be built after the owner records a go age or "none" (OA-13a, SPEC:110).

### S10-F22 The poll starts an orchestrator when none is running (ruling 4)
- 655 says: "the poll starts an orchestrator when none runs (4)" (body line 154; section 1 step 1, body line 23; comment 17).
- Status: COVERED
- Current plan: D10 item 8 and D15 row B6 "Start a session when none is live: ADOPT+CHANGE" (DEC:421, D15:63); FR-17 (SPEC:207) an unreadable process table means unknown and starts nothing; FR-27 (SPEC:229) a script may start the coordinator at depth 0 only when the launch prompt cites an owner authorization recorded in chat, "`coordinator_autostart` absent means false". Resolved contradiction E-2 (SPEC:627): "autostart off by default, `coordinator_absent`, unreadable table starts nothing".
- Evidence: n/a (covered with a default of off).
- Concerns: the capability exists but is OFF until the owner gives a recorded authorization per repo (OA-18, SPEC:581); starting at depth 0 is unproven (U3, SPEC:710); the start is "self-attested". A builder must not turn autostart on by default.

### S10-F23 Merge method is the repo's normal practice, kept per repo (ruling 5)
- 655 says: "merge method per repo (5)" (body line 154; comment 13 item 5: squash, and a merge commit for a release pull request from `integration` to `master`, kept "in `repos.yaml`").
- Status: COVERED
- Current plan: D07 item 5 (DEC:328) optional per-repo `merge` settings block with `merge_method`, `release_head`, `release_merge_method`, `can_merge`, `reviewers`, `merge_safety_files`, overridden by the live GitHub role at merge time; D15 row C3 (D15:75); FR-12 (SPEC:202) per-repo JSON.
- Evidence: n/a (covered).
- Concerns: the carrier differs: per-repo JSON in `~/.config/superclaude/issue-watch.d/`, not `repos.yaml` (FR-11 says "no `repos.yaml`", SPEC:201). The method is read live at merge time; the merge still needs a person's go (S10-F21).

### S10-F24 Review agents that do not run or finish hold the pull request (ruling 6)
- 655 says: "review agents that do not run or finish hold the PR (6)" (body line 154; comment 13 item 6: held and escalated; acceptance line 223).
- Status: COVERED
- Current plan: SEC-04 (SPEC:293) and OA-13b (DEC:989): an owner-set per-repo `reviewers` list, re-request review on the final head, wait 60 minutes from when its checks finish (UNVERIFIED, owner-settable), then escalate to the person; `review_stalled`, `review_none_present` and `changes_requested` are not overridable by a go (SPEC:292).
- Evidence: n/a (covered).
- Concerns: the plan holds up to 60 minutes first and then escalates; 655 escalates when the agent "does not run". The 60 minutes has no source (DEC:993). A repo whose listed reviewer never reviews dead-waits 60 minutes at each merge (DEC:991).

### S10-F25 Worker status check: hourly, Monday to Friday, 24 hours a day, stops at `worker_done` (ruling 7)
- 655 says: "worker check Monday to Friday, 24 hours a day (7)" (body line 154; table row at body line 112: hourly by default and configurable, for each running worker, stops at its `worker_done`; comment 13 item 7; acceptance line 222).
- Status: NOT-COVERED
- Current plan: none found for the schedule; searched SPEC and DEC for "hourly|Monday|weekday|24 hours a day|business hours". The only hits are the flag `--hourly` of `/sc:coordinator` (FR-24, SPEC:226; D08 item 2 "lift unchanged ... Source: D:133", DEC:356), the coordinator's wake pull at most every 5 minutes (FR-28, SPEC:230) and a sweep per wake (WC-16, SPEC:253). The plan does not define what `--hourly` does, who starts it or the Monday-to-Friday window.
- Component: COORDINATOR (check-in loop and its schedule; the clock that starts it may be a separate automation, see 655 section 8).
- Feature statement: For each running worker the coordinator runs one status check an hour (interval configurable), reading Orca state and the issue, Monday to Friday around the clock, and stops the check for a worker when that worker sends `worker_done`.
- Done when: a test with a fake clock shows one check per hour on a weekday, none on Saturday and Sunday, a configured interval honoured, and no further check after `worker_done`.
- Depends on: 655 section 8 (the clock) and section 6 (check-in and playbook); S10-F14.
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md:1251 "`waker.py` hourly mode ... Leftover, unreferenced: no hourly automation exists" and :811 "`hourly` is a recorded skip"; DEC:73 issue 339 counts an "hourly sweep" among its own unbuilt duties.
- Concerns: "Monday to Friday, 24 hours a day" is a long-running schedule with no weekend check, so a worker that stalls on Friday night waits until Monday; this is Clay's ruling, not the owner's. Cron versus an Orca automation for this clock is again S10-F5.

### S10-F26 One orchestrator per repo, at most 3 issues in flight (ruling 8)
- 655 says: "one orchestrator per repo, 3 in flight (8)" (body line 154; section 1 step 5, body line 27; acceptance line 216: `max_in_flight` default 3 in `repos.yaml`, an open plan request counts).
- Status: COVERED
- Current plan: D07 items 1 and 3 (DEC:324, 326): one coordinator per project, key `max_in_flight` (default 3) checked inside the child cycle, per coordinator id, a full repo records `coordinator_full`; FR-33 (SPEC:235); D15 row C1 (D15:73).
- Evidence: n/a (covered).
- Concerns: the first build enforces 1, not 3, "until claim agents have their own worktree" (FR-33 SPEC:235, D07 item 8 DEC:331, FR-70 SPEC:327, OA-23 SPEC:585); the cap counts differently (a waiting hand-back does not count, OD-13 DEC:957; a waiting merge go does count, SEC-21 SPEC:310). 655 says an open plan request also takes a place; the plan defers plan requests (S10-F38). The key lives in per-repo JSON, not `repos.yaml`. The plan marks "in flight needs a named closing writer and an expiry (not yet designed)" (DEC:326).

### S10-F27 The poll starts another orchestrator when a repo has more work (ruling 8)
- 655 says: "The poll alone routes each issue, starts another orchestrator when a repo has more" (comment 13 item 8; body line 27: "or starts another; an idle one ends, a dead one is restarted"; acceptance line 216).
- Status: CONFLICT
- Current plan: D07 item 2 (DEC:325) removes "the 30-minute idle end, extra poll-started orchestrators per repo, the `wrong_target` refusal"; D15 row C5 "Registry repo ... one orchestrator per repo with ids, 30-minute idle end, `wrong_target`, poll starting extra orchestrators: REJECT" (D15:77, SPEC:454). A full repo records the skip `coordinator_full` instead (FR-33).
- Evidence from our documents: D15:77 "D07: needs a hand-made clone per host, state is host-local, `cd <checkout> &&` before every claim". 655's version is REJECTED. The restart of a dead one is covered (S10-F48).
- Concerns: with one coordinator per repo and a cap that starts at 1, a second issue of a busy repo simply waits (`coordinator_full`); nothing is lost.

### S10-F28 Issues already assigned at switch-on are counted as seen (ruling 9)
- 655 says: "existing issues seen at switch-on" (body line 154; section 1 step 2: "an older one is handed over with `/sc:orchestrator --take <repo>#<N>`").
- Status: COVERED
- Current plan: master refuses an approval made at or before store creation (`approval_before_init`, predicates.py:230-231; TECHREF:929 lists the reason); FR-24 keeps the `--take <owner/repo#N>` flag (SPEC:226, FR-25 SPEC:225). D01 states the effect: "Issues assigned before switch-on are baselined as 'seen' in PR 686 and never woken, so an approved one needs `--take`" (/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D01/VERDICT.md:59).
- Evidence: n/a (covered).
- Concerns: the invariant probe left this as INV-009, MEDIUM, UNADDRESSED: the store-init floor and the "seen" baseline "behave the same for an approval-gated start" (/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D01/adversarial/adversarial/invariant-probe.md:15). The SPEC has no row that states the baseline rule in words.

### S10-F29 A wake is tried up to 3 times (ruling 9)
- 655 says: "3 delivery tries" (body line 154; section 1 step 2 "an unacknowledged wake is tried up to 3 times"; comment 13 item 9: "at most one claim and one worker start per issue, up to 3 delivery tries of a wake").
- Status: COVERED
- Current plan: FR-13 (SPEC:203) "three deliveries 10 minutes apart, then mark the Orca workspace unread and exit 7; the poll never writes the ack"; D10 item 1 (DEC:414). The "one claim, one worker start" part is FR-03 (SPEC:193), FR-21 (SPEC:211) and the exclusive-create adoption record FR-29 (SPEC:231).
- Evidence: n/a (covered).
- Concerns: D10 added two mandatory fixes Clay's code lacks: acknowledge only after the state file exists (M1) and recover an abandoned wake (M2) (DEC:423-424, FR-15, FR-16).

### S10-F30 Retire the old approval code first (ruling 9)
- 655 says: "retire the approval code first" (body line 154; comment 13 item 9 "PR D first, PR A merges after D, PR B after A"; acceptance line 229).
- Status: CONFLICT
- Current plan: Clay element A13 "Deletion of the plan-approval code (PR 682): REJECT (revert)" (D15:53, SPEC:448); D03 (DEC:211) and FR-72 (SPEC:336). PR 700 itself restored the package, WC-17 and guard rule 1 on master on 2026-11-20 (SPEC:758, 769, 776), and Clay's comment 16 states "Nothing more of this issue gets built or merged until you and Clay agree on one design" (/home/coder/workspaces/IronClaude/.dev/implement/reference-our-research-a-3463b8ef/inputs/issue-655-comments.md:293). OA-1 "both gates stay" (TRIAGE:14) now needs only a recorded owner answer (SPEC:789).
- Evidence from our documents: DEC:211 "Revert PR 682 ... The package, WC-17, 'Issue pipeline duties' and guard G2 rule 1 return." 655's version is REJECTED.
- Concerns: removal order was real: the package imports the `issue_watch` symbols PR 686 deletes, so retiring first breaks `superclaude --help` unless done together (DEC:213; /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D03/VERDICT.md:17). If the owner ever answers "only the start gate stays", a new removal PR is needed (SPEC:774, 8.3).

### S10-F31 The orchestrator repo is `IronbellyOrg/IronOrchestrator` (ruling 9)
- 655 says: "repo name IronOrchestrator (9)" (body line 154; section 1 step 6, body line 28: the repo list and repo-to-checkout map are read from the private orchestrator repo where the orchestrator sessions run).
- Status: CONFLICT
- Current plan: D07 item 2 (DEC:325) "Remove the separate registry repo `IronbellyOrg/IronOrchestrator`, `.orchestrator/orchestrators.json`, the hand-kept `repos.yaml` allow list ..."; FR-11 (SPEC:201) "no registry repository, no `repos.yaml`"; D15 row C5 REJECT (D15:77). The coordinator lives in each project: branch/worktree `Coordinator`, session `COORD-<RepoName>`, records on branch `coordinators` (FR-24, FR-62, FR-64; SPEC:226, 319, 321), with one config per project in `~/.config/superclaude/issue-watch.d/` (DEC:324).
- Evidence from our documents: DEC:342 "the debate agent made two read-only GitHub calls naming `IronbellyOrg/IronOrchestrator` (one returned `private: true`)", so the repo exists but the plan does not use it. 655's version is REJECTED.
- Concerns: the repo name is also where 655 puts the coordinator spec and report state (acceptance line 228). If the owner wants a central repo for records, the plan has the `coordinators` records branch per project instead.

### S10-F32 Tiers, never model ids, set per repo with a one-step fallback (ruling 12)
- 655 says: "tiers, never model ids (12)" (body line 154; body line 9: the plan call, worker and orchestrator session run on ccsession tiers named in `repos.yaml`, a per-repo override; a tier the user cannot use falls once to the next allowed tier and is recorded; a tier the gateway refuses is row 9).
- Status: COVERED
- Current plan: D15 row C6 "Tier settings (5.8): orchestrator, worker and plan tiers, efforts, validated against `ccsession --help`, one fallback step: ADOPT+CHANGE" (D15:78, SPEC:455); `coordinator_tier` and `worker_tier` "as requests until U28 passes, record `launch.effective`; efforts wait for U30; keys move to the per-repo JSON". FR-63 renames `orchestrator_tier` (SPEC:320). Live check U28/U30 in SPEC:710.
- Evidence: n/a (covered, for the worker and coordinator tiers).
- Concerns: the plan names the tier of the plan call differently (S10-F33) and states no default tier values (S10-F34). Until U28 passes a tier is only a request.

### S10-F33 The plan call is run by `plan_tier` (default `tier1b`), which sets the depth of `/sc:issue --plan`
- 655 says: `plan_tier` (default `tier1b`) "sets the depth of `/sc:issue --plan`" (body line 9; comment 14).
- Status: CONFLICT
- Current plan: OD-1 (SPEC:97, DEC:765) and FR-59 (SPEC:280): one plain key `plan_depth` (quick, standard, deep), unset means `quick`, run by the cheapest worker `issue-worker-t3`; "no `plan_tier` and no tier-to-depth table" (QG1 VERDICT line 20, /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG1/VERDICT.md:20).
- Evidence from our documents: QG1:21 "nobody has measured plan quality or cost per depth ... and the person's approval is the quality gate because the plan check proves only that three headings are filled in. Both advocates, Clay's included, sided with `quick`." 655's version is REJECTED. D15 row C6 explicitly turns `plan_tier` into `plan_depth` (DEC:579).
- Concerns: 66% confidence, a tie (DEC:769). With `deep` a hand-back can run the planner up to four times per issue (DEC:767). Clay's goal "stronger models plan, cheaper models build" stays available per repo by setting `plan_depth` higher.

### S10-F34 Default tiers (worker `tier2`, orchestrator `tier1b`) and the recorded fallback
- 655 says: defaults `worker_tier` `tier2` and `orchestrator_tier` `tier1b`; a tier the user cannot use "falls once to the next allowed tier and is recorded"; "a tier the gateway refuses is row 9" (body line 9, spec 5.8).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC, DEC, D15, QG1 and D14 verdicts for "tier1b|tier2|worker_tier|coordinator_tier|plan_tier" (only the plan-tier replacement of S10-F33 and the C6 summary line DEC:579 appeared, with no default values). D15 C6 only says keys are requests until U28 and one fallback step exists in PR 686 `repos.py:41-43` (D15:78).
- Component: COORDINATOR (the per-repo config it reads and the launch of workers and of its own session); the claim-launch tier belongs to the WATCHER only if the poll starts the session (S10-F22).
- Feature statement: The per-repo config sets the ccsession tier for the coordinator session and for each worker (defaults named by the owner), validates it against the installed ccsession, falls once to the next allowed tier and records the fallback, and treats a tier the gateway refuses as an escalation.
- Done when: a test with a fake `ccsession --help` shows an unusable tier replaced once by the next allowed tier with a recorded line, and a refused tier produces an escalation entry.
- Depends on: S10-F32, S10-F33; 655 section 9 (escalation table).
- Evidence from our documents: D15:78 "`coordinator_tier` and `worker_tier` as requests until U28 passes, record `launch.effective`"; SPEC:710 "U28 model and U30 effort in `launch.effective`" is a pending live check. The ccsession model list is itself template-controlled: "ccsession-models.json, fetched live from master at launch" (owner memory entry "IronClaude updates via Coder"), so tier names can change under the config.
- Concerns: the default values come only from Clay (ruling 12); the owner has not set them. The gateway refusal case needs the escalation table (a section 9 item).

## Rulings of 2026-11-19: addition A, the hold and plan creation (body line 155, rulings 23, 30, 31, 33, 39)

### S10-F35 The poll labels an incomplete issue `hold:plan` (label only, never a comment)
- 655 says: an issue that fails the plan check "gets the label `hold:plan` (a label only, never a comment)" and the poll removes it when the check passes (body line 25; acceptance line 219; "There is no `hold` verb: the poll alone writes the hold label", body line 62).
- Status: CONFLICT
- Current plan: FR-06 (SPEC:196) "Write nothing to GitHub in a poll cycle (NG-2): strip the label writer of PR 686 (`LabelWriter` ... `_label_write` ... label rows 3-5 of `_hold_step`, `hand_removed`)"; FR-07 (SPEC:197) create the local `holds` entry with no write and ignore a leftover `hold:plan`; D09 (DEC:383-391, SPEC:85), Q03 (SPEC:95), D15 row A5 "`hold:plan` label write by the poll: REJECT now ... label write deferred to its own later PR" (D15:45, SPEC:443); FR-82 (SPEC:218) names the only two code paths that may write to GitHub, neither a poll hold.
- Evidence from our documents: D15:45 "Q03: 'dormant' is not off by default because the design's own config example lists `issue.hold` ... and the no-grant state has defects (no entry, stuck label, warning every cycle ...). No reader of the label shown (D09)". D09 item 4 (DEC:389) gives the switch-on conditions for a later label write: "a 24-hour `--dry-run` shadow run showed the holds, and a test showed `gh` can add and remove a label under cron's minimal environment". 655's version is REJECTED for now.
- Concerns: the deferral is not a permanent rejection: D09 item 3 (DEC:388) allows a later narrow write of the existing `hold:plan` label in a repo holding the `issue.hold` grant, with NG-2 amended to name exactly those calls. Without a label a held issue is visible only in `issue-watch status` and the audit log (DEC:396), so the observer must show held issues (FR-44, SPEC:255). Q03's confidence is 70%, partial (SPEC:95).

### S10-F36 A person's `hold:backlog` label makes the system do nothing with the issue
- 655 says: "A person's label `hold:backlog` makes the system do nothing with the issue until it is removed" (body line 25; comment 15 item 1; acceptance line 219).
- Status: COVERED
- Current plan: FR-01 (SPEC:191) "no `hold:backlog`", FR-05 (SPEC:195) "skip `hold:backlog` as `held_backlog`", FR-08 (SPEC:198) re-check it at wake time; D09 item 2 (DEC:387) "Only a person places `hold:backlog` (the poll only reads it)"; D15 row A3 (D15:43).
- Evidence: n/a (covered).
- Concerns: the plan has the poll only read the label; who creates the label in a repo is OA-28b (the trigger label only; `hold:backlog` creation stays out of that decision, STATE.md line 53) so a repo may lack the label until the per-repo init creates it.

### S10-F37 A hold removed by hand stays removed
- 655 says: "A hold removed by hand stays removed" (body line 25; comment 15 item 1; acceptance line 219 "a hold removed by hand is not put back"; test T11).
- Status: CONFLICT
- Current plan: FR-06 strips `hand_removed` state (SPEC:196, D15:45 "the `hand_removed` state and the label tests of the wake-time re-check"), FR-07 ignores a leftover `hold:plan` "with no warning" (SPEC:197, D15:45); reasons `hold_removed_by_hand` and `hold_applied` leave the table (FR-20, SPEC:210; D15:114). With no label the poll re-evaluates the plan check every cycle, so a person cannot override it by removing a label; the only person-set stop is `hold:backlog` (S10-F36).
- Evidence from our documents: D15:45 "Strip `LabelWriter` ..., the `hand_removed` state ...; a leftover `hold:plan` is ignored with no warning". 655's version is REJECTED while the label write is off.
- Concerns: if the label write is later restored (S10-F35), the "stays removed" rule comes back with it, and D09 item 6 requires "one poll per repo" because two workspaces polling one repo would re-add a hand-removed label (DEC:398).

### S10-F38 After one hour with no plan work, the poll sends ONE plan request to the repo's orchestrator
- 655 says: "After one hour with no plan work elsewhere the poll sends ONE plan request to the repo's orchestrator, which makes the plan through `/sc:issue --plan`" (body line 25; comment 15 item 1; acceptance line 219; test T11).
- Status: NOT-COVERED
- Current plan: explicitly deferred, not decided: D15 row A4 "Plan request after one hour, wake `plan_requests[]` with the issue title: DEFER ... Not built now; if built, ids only and after D07 settles who plans" (D15:44, SPEC:442); D09 item 5 (DEC:390) "the one-hour plan request (a wake-file item) ... are not poll writes and wait for D07". Meanwhile "A held issue is never sent to a coordinator, so plans come from a person or from `/sc:issue --plan`" (DEC:397). Searched SPEC, DEC and FOLLOW-UPS for "plan request|plan_requests|one hour".
- Component: WATCHER (the one-hour timer, the once-only rule and the wake item are poll behaviour; the plan call itself is the coordinator's, S10-F39).
- Feature statement: When an assigned issue has stayed held for plan reasons for one hour with no sign of plan work, the poll adds exactly one plan request (ids only, never the title) to the wake of the repo's coordinator, and never a second one for that hold.
- Done when: a test with a fake clock shows no request at 59 minutes, exactly one at 60, none again at later cycles, none for a full coordinator, and no GitHub text in the wake file.
- Depends on: S10-F26 (an open plan request takes an in-flight place in 655), S10-F39, 655 section 5 plan mode, FR-13 wake format.
- Evidence from our documents: D15:44 "a title is free GitHub text (D10 item 5)"; DEC:418 (D10 item 5) "The wake file carries ids only (`repo`, `number`, `url`); no title, label or comment text."
- Concerns: 655 wake items carry titles for the plan request (D15:44), which breaks the plan's no-GitHub-text rule (SEC-16, SPEC:305); a builder must send ids only. "No sign of plan work elsewhere" is undefined in both documents (UNVERIFIED which signal counts). The wake transport is itself unbuilt on master (SPEC:61).

### S10-F39 A plan is created only through `/sc:issue --plan`
- 655 says: plan creation "only through `/sc:issue`" (body line 155; section 1 step 3; acceptance line 219 "a plan is created only through `/sc:issue --plan` (PR P, with `--remaining`), the plan record written before the acknowledgment").
- Status: COVERED
- Current plan: D12 (DEC:464-491, SPEC:88): PR 690 KEEP-ADAPT merges `--plan <N>`, `plan_body.py` and `--remaining` after four fixes (FR-53, SPEC:274); a manual claim of a plan-less issue warns and prints `/sc:issue --plan <N>` (FR-56, SPEC:277); the coordinator hands a worker a chain that names the filed plan and `plan-check` is the same function as `plan_body.py check` (FR-61, FR-54; SPEC:282, 275); D15 rows A7, A8 (D15:47-48).
- Evidence: n/a (covered).
- Concerns: PR 690 is still a draft with its four fixes open (SPEC:772). The plan write needs the grant `issue.body.append_plan_sections`, which a fresh install does not hold (SEC-07 SPEC:296, OD-11 DEC:927). The plan-record-before-acknowledgment ordering is the same shape as M1 (FR-15) but is not stated for plan requests.

## Rulings of 2026-11-19: addition B, what reaches the person (body line 155, rulings 16, 24, 39)

### S10-F40 The nine-row table decides what reaches the person (the hard bar)
- 655 says: "the hard bar (releases, pricing, other people's access and data, deleting shared branches, breaking changes)" as one nine-row table; `escalate` refuses an entry that names no row (body line 155; body lines 123-137; acceptance line 224).
- Status: COVERED
- Current plan: D15 row D16 "Nine-row 'what reaches the person' table ... ADOPT+CHANGE: notice step only; 'the person' instead of Clay; sweep and observer never pick a row; keep the 'exactly nine rows' test; owner decision" (D15:100, SPEC:463); FR-47 (SPEC:258); FR-37 (SPEC:239) refusal of an entry naming no row stays; D06 item 10 (DEC:302) "adopted only as an inventory, as an owner decision".
- Evidence: n/a (covered).
- Concerns: the nine-row list is still an open owner decision (D06 item 11); the plan uses it "in the notice step only", while 655 uses it to decide every escalation. Wording "Clay" must be "the person".

### S10-F41 The rules are on from the start: no warn phase, no ladder
- 655 says: "The rules are on from the start: no warn phase, no ladder" (body line 137; ruling 16 in body line 155).
- Status: COVERED
- Current plan: the escalation refusal of an entry with no row stays hard (FR-37, SPEC:239; QG2:13 "Fail closed stays only for a structurally bad call such as an entry naming no row"); every control starts enforced and the whole system starts OFF (`enabled: false`, FR-23 SPEC:213).
- Evidence: n/a (covered).
- Concerns: the naming rule (S10-F17) is the exception: it is measured first (U54) and fails open (OD-4), i.e. a warn-like phase. Not a conflict with this row because the naming rule is a separate ruling (15).

### S10-F42 An unanswered question waits; nothing is decided for the person
- 655 says: "An unanswered question waits and nothing is decided for Clay: the entry says what stays blocked and what continues (`If you do not answer:`)" (body line 137; ruling 24).
- Status: COVERED
- Current plan: D15 row D20 "An answer is always typed; unanswered waits with no default (ruling 24): Adopt as is" (D15:104); SEC-21 and OA-25b (SPEC:310, 114): "Silence is never a yes"; a waiting merge go never expires; QG2:13 "an unanswered item waits for the person, not for nobody".
- Evidence: n/a (covered).
- Concerns: 655 also lets "his ClickUp reply" count as an answer (body line 137). The plan's `answer-check` accepts only input "typed in the coordinator's own terminal by a person, never relayed" (D15:88, SEC-08, SEC-09; SPEC:297-298), so a ClickUp reply is not an accepted answer channel; that part is REJECTED.

### S10-F43 Tagging or publishing a release always needs a recorded human OK
- 655 says: "Tagging or publishing a release always needs a recorded human OK" (body line 137; body line 140 "tag or publish a release only with a recorded OK"; acceptance line 224).
- Status: CONFLICT
- Current plan: OD-6 (DEC:845, SPEC:102, SEC-11 SPEC:300): the coordinator never tags or publishes a release; Clay's rule N6 "becomes an unconditional refusal with no `--answer-ref` pass path"; one denylist test per command (`git tag`, `gh release create`, `uv publish`, `npm publish` and the others); merging a release PR stays allowed on the per-PR go. Confidence 89%.
- Evidence from our documents: DEC:845 "Reason: Clay's own table calls release 'something that cannot be undone', and the pass path rests on `answer-check`, which cannot tell a person from a script (open in Clay's register as U57)." 655's version (a recorded OK as a pass path) is REJECTED.
- Concerns: `refuse(argv)` sees only commands the verbs run, so a tag typed in the coordinator's own shell stays unseen (DEC:847, UNVERIFIED how to cover); three denylist entries are UNVERIFIED against design line 763 (DEC:849).

### S10-F44 At most 5 notices per repo per 24 hours (`reach_daily_max`), default 5
- 655 says: "Notices ... are capped at `reach_daily_max` (5 per repo per 24 hours, ruling 39); an entry is never dropped" (body line 137; ruling 39 in body line 155).
- Status: CONFLICT
- Current plan: D15 row D17 "Cap of 5 notices a day: DEFER ... Key default stays 0 (no cap); no generator writes 5 until the owner rules" (D15:101); FR-12 (SPEC:202) "`reach_daily_max` absent or 0 means no notice cap"; FR-47 (SPEC:258) "keep the 5-a-day cap a proposal (default 0; no generator writes 5)"; D11 item 4 (DEC:450).
- Evidence from our documents: OA-25a (DEC:1021) "the cap of 5 notices a day is Clay's ruling 39 and the owner has no record of ruling on it"; QG2:63 "The same Clay-ruling status applies to the cap of 5." The "never dropped" rule is kept (QG2:14 rules of the channel).
- Concerns: a bad `reach_daily_max` must not silently read as "no cap" (C-INV-3, D15:142); the design text itself says both "open" (D:1177) and "settled" (D:686) (D15:101).

### S10-F45 The notice itself: a ClickUp message, else the Orca unread mark
- 655 says: "Notices (a ClickUp DM, else the Orca unread mark)" reach the person away from the report (body line 137; the three ways to reach him: entry lines, an Orca decision gate, the notice).
- Status: NOT-COVERED
- Current plan: reserved, not built, and not decided: OD-5 (SPEC:101, DEC:829) "Entry lines only in the first build, with a reserved notice"; the push notice is built only when all three triggers hold: the owner says in chat that a push is wanted and gives the cap number, a notice sender is built and tested, and the verb accepts row 8 alone (FR-49, SPEC:260; OA-25a SPEC:113). Searched SPEC, DEC, QG2 and OAG1 for "notice sender|ClickUp|unread".
- Component: COORDINATOR (sender behind the `escalate` verb); the TUI-DASHBOARD only shows "waiting on a person" with its age (SEC-21, SPEC:310).
- Feature statement: After an escalation entry is written, `escalate` may send one capped notice (an Orca unread mark, optionally a ClickUp message) to the person for the rows the owner allows, and never instead of writing the entry.
- Done when: with a recorded cap number and an enabled sender, an AU4a finding writes the entry and sends one notice, the sixth in 24 hours writes the entry and sends none, and with no cap number recorded no notice is sent.
- Depends on: S10-F44, S10-F40; 655 section 9; observer "waiting on a person" state.
- Evidence from our documents: QG2:70 "Whether any notice sender (ClickUp message, Orca unread mark) exists or works; none seen in master, pr-a or pr-p."; DEC:1021 "no escalation notice sender exists in master, PR 686's head or branch `issue-655-pr-p`". The Orca unread mark already exists as the poll's last-resort wake step (FR-13, SPEC:203), so that helper is reusable.
- Concerns: a ClickUp DM needs a ClickUp credential and path; none is described in the plan and the ruling-17 secret rule (S10-F18) applies. The owner must say a push is wanted (DEC:829).

## Rulings of 2026-11-19: addition C, what the orchestrator may do (body line 155, rulings 25, 29)

### S10-F46 The orchestrator may interrupt a worker once, after writing the escalation
- 655 says: "interrupt allowed" in ONE case, `escalate --interrupt`, "only after the escalation is written; this one send is exempt from the 60-second typing hold" (body lines 140 and 155; acceptance lines 222, 225).
- Status: CONFLICT
- Current plan: OD-7 (DEC:861, SPEC:103): "No. `escalate --interrupt` (Clay's rule N7) is not built"; FR-26 (SPEC:228) "no lease, no interrupt"; FR-40 (SPEC:242) "never interrupt a worker"; D15 row D9 REJECT (D15:93), SPEC:458. Only "write the escalation first and send nothing if refused" is kept.
- Evidence from our documents: DEC:861 "no incident is cited; Orca gives no receipt that the interrupt landed (U40); and the contract's next liveness nudge ('If your turn ended before worker_done, continue ...', WC:164) would undo the stop, with no rule in the design that suppresses it." 655's version is REJECTED. Re-opening needs "a contract exception ... the five coordinator-spec changes C25 to C29, a nudge-suppression rule and a check of whether `--interrupt` has its own receipt" (DEC:861).
- Concerns: the brake for an irreversible worker action is only the guard and the person's go (DEC:863). Confidence 85%.

### S10-F47 The orchestrator may delete the ordinary files its work needs
- 655 says: "delete the ordinary files its work needs (ruling 25; removal of that line was rejected)"; deleting a skill or an agent needs the issue to name it (body line 140; comment 8 item 2; acceptance line 224).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC, DEC, VERDICT files, FOLLOW-UPS for "ordinary file|any removal|delete(s|d)? (a )?(skill|agent|file)". The nearby decisions cover other deletions only: the cleanup script removes worktrees only by nine rules and "never uses `--force`, `git branch -D` or `rm`" (D13 item 3, DEC:504; FR-39, SPEC:241); Q02 allows local `git branch -d` only; `refuse(argv)` is the closed list adopted with change (D15 row D8, D15:92) but its contents are not given in the plan.
- Component: COORDINATOR (the closed "may do" and "may never do" lists in `limits.py` and the refusal of `rm` forms).
- Feature statement: The coordinator's `refuse(argv)` allows deleting ordinary files inside the worktree of its own work, refuses deleting a skill or an agent file unless the issue names it, and refuses any deletion of a shared branch, another person's data, or a worktree or session it did not start.
- Done when: refusal tests show `rm` of a plain file in the coordinator's own worktree allowed, `rm` of a skill or agent file not named by the issue refused, and `rm -r` of a worktree or a branch deletion refused.
- Depends on: 655 section 9 (the "may never" list), S10-F46.
- Evidence from our documents: DEC:504 "Nobody removes by judgment. A removal is decided only by the nine rules of issue 687"; DEC:512 "issue 687's incident: git knew 53 worktrees, Orca 26, sixteen removed by hand, two for open issues"; DEC:847 "`refuse(argv)` sees only commands the verbs run, so a tag typed in the coordinator's own shell stays unseen".
- Concerns: this row can collide with D13 item 3 ("no session decides a removal by its own judgment") unless "ordinary files of its own work" is defined narrowly; the incident shows the cost of loose deletion rules. A raw shell `rm` is invisible to the verb-level refusal.

### S10-F48 Restarting a dead agent stays (rulings 14 and 29)
- 655 says: "Restarting a dead agent stays as FR-23 says (ruling 29)"; "the restart of a dead agent kept (14 is superseded)" (body lines 140 and 155; acceptance line 216 "a dead one is restarted").
- Status: COVERED
- Current plan: FR-34 (SPEC:236) "Restart a dead coordinator with a resume wake, at most 3 times (stored counter); an unreadable terminal list restarts nothing"; D07 item 4 (DEC:327); D15 row C2 "Guarded restart with a resume wake: ADOPT+CHANGE" (D15:74).
- Evidence: n/a (covered).
- Concerns: until Coder 516 creates `COORD-<RepoName>` the duty holder is `ORCH-IronClaude` and "nothing restarts" (FR-34); the panel noted the restart skips the autostart consent FR-27 requires (FOLLOW-UPS.md finding F5, /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/FOLLOW-UPS.md:16, still open). The plan has no 30-minute idle end (D07 item 2).

## Rulings of 2026-11-19: addition D, closeout and hand-back (body line 155, rulings 19 to 22, 26, 32, 36, 38)

### S10-F49 Closeout is its own issue (#668, `/sc:closeout`) and adopts Jay's skill
- 655 says: "closeout is issue #668 and adopts Jay's skill" (body line 155; body line 7 addition D; acceptance line 226 "#668 is merged before the live test").
- Status: COVERED
- Current plan: D13 (DEC:493-519, SPEC:89): `/sc:closeout` (PR 683, merged 2026-11-20) is the built path to the first half of `sc:close` and "adopt as is" (D15 row F1, D15:120; SPEC:465); PR 700 kept it on master (DEC:519, SPEC:758); the design drops Jay Wedgeworth's "Retire the lane" step (/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D13/VERDICT.md:34). FR-38 (SPEC:240) makes it a coordinator step.
- Evidence: n/a (covered).
- Concerns: its step that settles a work-report entry depended on the PR 684 skill that PR 700 removed (effect UNVERIFIED, DEC:519). `/sc:closeout` stays on the never-as-worker list (SEC-05, SPEC:294).

### S10-F50 Closeout decides by whether the issue is done, not by the words Fixes, Closes or Refs
- 655 says: "it decides by whether the issue is done" (body line 155; comment 15 item 4: reading the issue's own criteria against what the pull request and its linked pull requests delivered, "it does not decide by the words Fixes, Closes or Refs").
- Status: COVERED
- Current plan: the built skill states it: "The words `Fixes`, `Closes` and `Refs` are read as data and decide nothing" and "Decide whether an issue is done by matching the words ..." is a Will Not Do (/home/coder/.claude/skills/sc-closeout-protocol/SKILL.md:24 and :112); SEC-12 (SPEC:301) "close issue M if closeout's verdict is done".
- Evidence: n/a (covered).
- Concerns: none for the decision rule itself. The authority to close is a separate row (S10-F51).

### S10-F51 Wave 8 runs the closeout after a merge with no person's go (the orchestrator closes a done issue)
- 655 says: after a merge, wave 8 calls `/sc:closeout <PR>`, which closes only a done issue; the orchestrator runs no `gh issue close` itself (body line 155; comment 15 item 4; acceptance line 226; comment 8 item 1 "Agents may close issues").
- Status: CONFLICT
- Current plan: FR-38 (SPEC:240) "call `/sc:closeout <PR>` per merged PR under a go naming the close"; SEC-12 and OD-10 (SPEC:301, 106; DEC:909) "One per-PR go, bound to the head sha, covers both the merge and the close ... there is no standing `issue.close`"; SEC-06 (SPEC:295) refuses `issue.close` as a grant. "Every merge go must name the close, or the close has no go. A restart between merge and closeout must read the recorded go" (DEC:911).
- Evidence from our documents: DEC:909 "`WORKER-CONTRACT.md:241` allows an outward action only when the user's instruction names that action." 655's version (no go for the close) is REJECTED.
- Concerns: a `Fixes` line in the PR body still closes the issue at merge with no coordinator write (DEC:909, SPEC:301, RK-10 SPEC:654), so the go only controls the coordinator's own close.

### S10-F52 A not-done issue goes back to the orchestrator (hand-back)
- 655 says: "a not-done issue goes back to the orchestrator" (body line 155; comment 15 item 5: re-plan with `/sc:issue --plan <N> --remaining <file>`, a new worker on a new branch after the old worker is final, at most 3 hand-backs, stop when nothing progressed, every stop is an escalation; acceptance line 226).
- Status: COVERED
- Current plan: FR-35 (SPEC:237) "Run the hand-back loop (`handback`: stop on empty list, `HANDBACK_MAX` 3 'not measured', `no_progress`; old worker final first; idempotent re-plan marker)"; D15 row D18 (D15:102); OD-2 (DEC:781); OD-13 (DEC:957).
- Evidence: n/a (covered).
- Concerns: the plan changes what round 2 does: re-plan, then the person re-applies the approval, then the whole start gate repeats; the issue waits in `waiting_reapproval` outside the in-flight cap (FR-35, OD-2, OD-13). 655 restarts a worker through the same waves with no new approval. That difference is a CONFLICT that belongs to 655's wave 8 section, not to this ruling. 655's "Round n of at most 4" block and the plan's cap of 3 are both "not measured".

### S10-F53 A worker PR says `Fixes` only when it fully addresses the issue, else `Refs` (rulings 26 and 38)
- 655 says: "`Fixes` only when fully addressed, else `Refs`" (body line 155; body line 66 handoff section 6; comment 15 item 4, ruling 38).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC, DEC and VERDICT files for "Refs", "`Fixes`", "Fixes line". The plan only states the limit: "A `Fixes` line in a PR body still closes the issue at merge" (SEC-12 SPEC:301; D15:143-144; DEC:909) and the risk RK-10 "Closeout or a `Fixes` line closes unfinished work" (SPEC:654). No requirement tells workers which word to use.
- Component: COORDINATOR (handoff prompt template section 6 and the worker contract text it quotes).
- Feature statement: The handoff prompt tells every worker to write `Fixes <repo>#<n>` in the PR body only when the PR fully addresses the issue and `Refs <repo>#<n>` otherwise, and the audit after the merge flags a `Fixes` line on a PR whose issue still has remaining items.
- Done when: a template test finds the rule in section 6 of the handoff prompt, and an audit test marks a PR with `Fixes` and a non-empty remaining list as a warning.
- Depends on: S10-F50, S10-F52; 655 section 4 (handoff template), section 9 audit.
- Evidence from our documents: SPEC:654 "RK-10 | Closeout or a `Fixes` line closes unfinished work ... | Medium | close only under the go"; DEC:909 "A `Fixes` line in the PR body still closes the issue at merge with no coordinator write."
- Concerns: the PR body is written by the worker, so the rule cannot be checked before it is written (same limit as the naming rule, QG2:12); the check can only run at the audit. The instruction narrows risk RK-10 and does not remove it.

## Rulings of 2026-11-19: addition E, audit and merge safety (body line 155, rulings 27, 34, 35)

### S10-F54 Audit findings reach the person as recommended (ruling 27)
- 655 says: "audit findings reach Clay as recommended" (body line 155; body line 104: eight checks, no model, no GitHub write; only AU4a, AU4c and AU5 reach him as row 8; warnings never; acceptance line 227).
- Status: COVERED
- Current plan: FR-36 (SPEC:238) audit AU1-AU8 with AU5 narrowed, and it states it cannot see a push with no PR; D15 row D15 (D15:99); OD-5 (SPEC:101, DEC:829) AU4a, AU4c, AU5 are lines of the issue's own entry marked "waiting on a person"; FR-49 (SPEC:260).
- Evidence: n/a (covered).
- Concerns: the channel is narrower: entry lines only in the first build, the push notice is reserved (S10-F45). Ruling 27 is Clay's (QG2:63). A post-merge finding can sit until the report is read (QG2:60), and the report skill that holds the entries is not on master (SPEC:778).

### S10-F55 A pull request with an open `changes_requested` review is never merged (ruling 34)
- 655 says: "`changes_requested` never merged" (body line 155; comment 15 item 6; acceptance lines 223 and 227).
- Status: COVERED
- Current plan: OA-13c (DEC:999-1005, SPEC:112) "`changes_requested` stays a hard refusal ... No go overrides"; SEC-03 (SPEC:292); D15 row D2 "Adopt as is" (D15:86). Confidence 95%.
- Evidence: n/a (covered).
- Concerns: still listed as an owner confirmation (DEC:1007).

### S10-F56 A bot-fix warning (AU8)
- 655 says: "a bot-fix warning" (body line 155; body line 104: AU8 "a bot fix after a '@codex fix this' style request (a warning only)").
- Status: COVERED
- Current plan: FR-36 (SPEC:238) adopts AU1-AU8 as a set; D15 row D15 ADOPT+CHANGE with only AU5 narrowed (D15:99); QG2:14 "warnings never reach the person".
- Evidence: n/a (covered).
- Concerns: none; the plan keeps the checks and the warning rule.

### S10-F57 The merge-safety hold: a CI or merge-safety file change waits for the person's OK for that head
- 655 says: "the merge-safety hold" (body line 155; comment 15 item 6: a pull request that changes CI or another merge-safety file waits for Clay's explicit OK for that head, "an unreadable file list is a hold"; acceptance lines 223 and 227).
- Status: COVERED
- Current plan: D15 rows D1 (fail-closed file list) and D2 (`merge_safety` hold, adopt as is) (D15:85-86); SEC-03 (SPEC:292) a go may override `merge_safety` only with its own key; SEC-08 (SPEC:297) the question key `merge_safety:<PR>:<head sha>`; SEC-10 (SPEC:299) the `merge_safety_files` list is write-protected and fails closed on `[]`; OD-12 (DEC:941).
- Evidence: n/a (covered).
- Concerns: the config is tamperable by the coordinator's own shell, so the hold only narrows the gap (DEC:943). The file list lives in per-repo JSON, not `repos.yaml`.

## Rulings of 2026-11-19: naming, removals, order and approval (body lines 155-156)

### S10-F58 Naming (ruling 28)
- 655 says: "Naming (28)" with no further text (body line 155). The body names the skill `orchestrator` and the command `/sc:orchestrator` (body line 3, line 62).
- Status: CONFLICT
- Current plan: D08 (DEC:348-377, SPEC:84): the role is "coordinator", the command `/sc:coordinator`, the skill `sc-coordinator-protocol`, session `COORD-<RepoName>`; "No `commands/orchestrator.md` or `sc-orchestrator-protocol`" (FR-24 SPEC:226, FR-62 SPEC:319); persisted names are renamed before PR 686 merges (FR-63, SPEC:320). If ruling 28 instead concerns the naming rule on agent names, OD-3 scope B applies (S10-F17).
- Evidence from our documents: DEC:371 "the name `/sc:orchestrator` was never an owner decision (OQ5 has Owner column 'no'; none of OD1 to OD15 covers it)"; QG2:63 "rulings 15, 27, 28 and 39 are Clay's". 655's version is REJECTED either way.
- Concerns: what ruling 28 says is UNVERIFIED: the RULINGS.md of Clay's session and the design text are not available locally (the design doc is only on the archive branch). The owner's wording "coordinator (aka orchestrator)" was found only in TOPICS.md (DEC:373).

### S10-F59 Removals 1, 3, 4 and 5a yes; 2 and 5 rejected (ruling 29)
- 655 says: "Removals 1, 3, 4, 5a yes; 2 and 5 rejected (29)" (body line 155; the dropped list is in comment 7: trigger label, approval label and approver list, Project and Backlog, plan-approval gate, cron).
- Status: CONFLICT
- Current plan: the removals of the trigger label, approval, Project and plan-approval gate are rejected: D01 (DEC:149-157), D03 and A13 (DEC:211, D15:53), OA-8 keeps the trigger label for now (TRIAGE:21), the plan-approval gate is back on master after PR 700 (SPEC:758, 776), cron stays (S10-F5). The numbering "1, 3, 4, 5a, 2, 5" refers to Clay's removal plan in design section 7.2, which D15 row G5 adopts only "as sequencing input and the bar for any replacement protection" (D15:133; /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D03/VERDICT.md:39).
- Evidence from our documents: DEC:211 "Revert PR 682 ... The package, WC-17, 'Issue pipeline duties' and guard G2 rule 1 return"; SPEC:774 "OA-1 'only the start gate' now means a new removal PR, not 'PR 682 stands'". 655's "yes" removals are REJECTED.
- Concerns: which removal each number stands for is UNVERIFIED (the design text is not local). Whichever two Clay rejected may match the plan, but the plan decided them on other grounds.

### S10-F60 Order: wait for additions A to E before building (ruling 20)
- 655 says: "wait for A to E (20)" (body line 156).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC, DEC, STATE for "ruling 20" and "wait for". The plan has its own order (H0 hold, then lanes; S0 to S17, SPEC:484-503, D14 order DEC:540) and the owner's goes in chat.
- Component: OTHER (a document-ordering step inside Clay's spec work, already done; it is not a product feature).
- Feature statement: none to build; do not carry this into the backlog. If the issue text is reused, replace it with the plan's own order (D14, section 8).
- Done when: not applicable.
- Depends on: none.
- Evidence from our documents: SPEC:484 stage S0 "owner decides in chat and holds the open PRs"; Clay's comment 16 "Nothing more of this issue gets built or merged until you and Clay agree on one design" (/home/coder/workspaces/IronClaude/.dev/implement/reference-our-research-a-3463b8ef/inputs/issue-655-comments.md:293).
- Concerns: none.

### S10-F61 Clay approved the draft and the spec (ruling 37), so the spec is the design of record
- 655 says: "Clay approved the draft and the spec (37)" and "where this body and the spec differ, the spec wins" (body lines 7, 156, 165, 179).
- Status: CONFLICT
- Current plan: SPEC header (SPEC:7-8): the owner `ironbelly` "is the repository admin and the only person who gives rulings. Every verdict here is a recommendation until the owner says so in chat"; D06 "Clay's design was approved by Clay only and no owner approval of PR 681 is on GitHub" (DEC:309); D07 "Clay's rulings 8 and 9 are Clay's, not the repository owner's" (DEC:340); FR-68 and PR 700 (design doc gone from master, SPEC:325, 775); the design amendment needs an owner review before any PR B or PR E (SPEC:569).
- Evidence from our documents: DEC:309, DEC:340, QG2:63. The design the spec approval refers to is not on master (SPEC:758) and Clay's own comment 16 puts the build on hold until one design is agreed (inputs/issue-655-comments.md:293).
- Concerns: the owner's rule applies: where 655 conflicts with the current plan, the current plan wins; Clay's approval is not an owner approval.

### S10-F62 The owner decisions OD1 to OD15 of Clay's spec, section 10
- 655 says: "The owner decisions OD1 to OD15 are in spec section 10" (body line 156).
- Status: NOT-COVERED
- Current plan: no complete mapping found. Our plan has its own owner questions: OA-1 to OA-34 (TRIAGE) and decisions OD-1 to OD-13 (SPEC:97-109, DEC:92-140), which share the "OD" prefix but are different questions. Clay's list lives in `docs/designs/orchestrator.md` section 10 on the archive branch `clayphi/archive-orchestrator-655-20261120` (SPEC:759, 787), not on master and not available locally. Searched DEC, SPEC, STATE and all VERDICT files for "OD1" through "OD15" written without a hyphen: only five of Clay's items are touched, as design text to rewrite: OD1 (the guard-less worker clause; D05 item 1 requires the guard, /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D05/VERDICT.md:19 and STATE.md:30 "guard level FS ... equals Clay's OD1"), OD3 and OD4 (merge authority, rewritten by D06, DEC:308), OD6 (report session names, D08 item 6, /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D08/VERDICT.md:22) and OD8 (topology ruling, /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D07/VERDICT.md:31). OD2, OD5, OD7 and OD9 to OD15 are not mentioned anywhere.
- Component: OTHER (process: a mapping of Clay's open owner questions onto ours).
- Feature statement: Each of Clay's OD1 to OD15 is mapped to the matching OA or OD answer of the plan (OD1, OD3, OD4, OD6, OD8 have a verdict), or listed as a remaining owner question (the other ten).
- Done when: a table lists OD1 to OD15 with a matching plan id or "open", checked against the design text on the archive branch.
- Depends on: all other rows of this section; the archive branch read.
- Evidence from our documents: DEC:371 "none of OD1 to OD15 covers it" (the command name); D06 caveat (DEC:309) shows the design text was only read through "D:nnn" line citations by the debates.
- Concerns: UNVERIFIED which of Clay's questions are already answered. Do not mix the two numbering schemes: Clay's OD1 is not our OD-1 (plan_depth).

## Section summary

- 62 rows: COVERED 29, CONFLICT 23, NOT-COVERED 10. Section 10 is mostly a list of policy rulings by Clay; the current plan already decided most of them, and where it decided differently 655 is rejected: assignment-only trigger and the Backlog independence (D01, FR-01), the Orca automation as scheduler (D02, FR-10), workers pushing without a go and merging without a go (E-1, Q04, SEC-01), the label write and the hand-removed hold (FR-06, FR-07), release OK pass path (OD-6), the 5 a day default (D17), the interrupt (OD-7), closeout without a go (SEC-12), the `plan_tier` (OD-1), the IronOrchestrator repo and extra poll-started orchestrators (D07), the unknown-launch retry (FR-21), approving permission prompts (FR-40), retiring the approval code (D03, PR 700) and Clay's approval as authority (SPEC:7-8).
- The ten NOT-COVERED rows to turn into backlog items: exponential backoff (F9, WATCHER), the plain English, dash and secret check on written text (F18, COORDINATOR), the Monday to Friday hourly worker check (F25, COORDINATOR), default tiers and the recorded fallback (F34, COORDINATOR), the one-hour plan request (F38, WATCHER, deferred by A4), the notice sender (F45, COORDINATOR), deleting ordinary files in the "may do" list (F47, COORDINATOR), the `Fixes` versus `Refs` rule (F53, COORDINATOR), and two process rows (F60 history, F62 mapping of Clay's OD1 to OD15, OTHER). Nothing in this section is owned by TUI-DASHBOARD alone; the dashboard only shows the waiting states that the notice and audit rows depend on.
- Three covered rows are conditional and a builder must not treat them as done: the living report (F13, the skill was removed by PR 700 and restoring it is an open owner decision), the poll starting a coordinator (F22, off until the owner records an authorization per repo) and the cap of 3 in flight (F26, the first build enforces 1).
- Almost every Clay ruling in this section is Clay's, not the owner's (QG2:63, DEC:340), and the plan itself is still a set of recommendations until the owner rules in chat (SPEC:7). Several items in "covered" depend on unbuilt or unproven parts (the guard has never bound a `worker-start` worker, the merge gate and `answer-check` exist nowhere: SPEC:57, 62), so "covered" means decided, not built.
- Acceptance-criteria lines of 655 that become obsolete or must be rewritten to match the plan: 215 (cron, not an automation), 216 (poll starts no extra orchestrators; cap 1 first), 222 (no permission-prompt approval, no interrupt), 223 (worker pushes and the orchestrator merges: both need a person's go), 224 (release pass path, ClickUp answers), 225 (the one interrupt), 226 (closeout under a go; round 2 needs re-approval), 229 (the removed gate and Project read stay) and the "62 reason names" of line 215 (the plan restores 14 approval reasons and drops 6, FR-20 SPEC:210).
