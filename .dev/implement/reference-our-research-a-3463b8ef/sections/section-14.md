# Section 14 analysis: Testing and design questions for the orchestrator skill
Counts: COVERED 18, CONFLICT 8, NOT-COVERED 7 (33 rows)

Sources read: 655 body lines 1-30, 191-230; SPEC.md sections 2, 4, 7, 8, 12, 13, Appendix B; DECISIONS.md (selected lines); debates D06, D07, D09, D12, D15 (VERDICT.md and merged-d15-position.md), QG1. Naming: "coordinator" in our plan = "orchestrator" in 655. Numbering note: our documents refer to Clay's tests T1 to T13 as they stood in the design doc `docs/designs/orchestrator.md` (PR 681, removed from master by PR 700, text on the archive branch; SPEC.md:758-759). The 655 body's T-list may differ in detail (for example T13: merge-gate in D15, audit in 655). The mapping is UNVERIFIED because I did not read the archived design doc.

### S14-F1 Local end-to-end gate before the skill PR is opened, results in the PR description
- 655 says: The skill is tested locally, end to end (T1 to T13), before its PR is opened, and the results go in the PR description (body line 193; acceptance line 217: "lands as one pull request after T1 to T13 pass, with their results in its description").
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md sections 8, 12.2, 13 and DECISIONS.md for "throwaway", "end-to-end", "local test", "PR description", "PR body". Our live tests (SPEC.md:698-713) run in S17, after S14 to S16 are merged and before the poll is switched on; the only pre-merge evidence rule is the S6 dry-run record "for the S7 PR body" (SPEC.md:490), now done by PR 700.
- Component (NOT-COVERED only): OTHER, a process and test rule for the skill's PR; it is not a watcher, coordinator or dashboard behavior.
- Feature statement (NOT-COVERED only): Before the PR that adds `/sc:coordinator` (S14, and each S15 PR) is opened, the author runs the local throwaway end-to-end tests that apply to that PR and pastes the pass or fail result of each into the PR description.
- Done when: the PR body of S14 lists each local test with pass or fail and the throwaway issue or PR it used.
- Depends on: S14-F3, S14-F4 to S14-F33 (the individual tests); 655 section 14 acceptance "one pull request".
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D07/VERDICT.md:29 quotes Clay's own design: "UNVERIFIED and ... the first local end-to-end check" (Clay's design already admitted its claims rested on an unrun local check). SPEC.md:698 "Nothing below has run."
- Concerns: Our plan has no pre-merge live run of the skill; the first live run is S17. Every real write to GitHub or typing into a session needs the owner's go (SPEC.md:698, SEC-14), so a local test run that writes to throwaway issues needs a recorded go per run. UNVERIFIED whether throwaway repos in both orgs exist.

### S14-F2 The skill lands as one pull request
- 655 says: "The skill is one pull request and deep work" (body line 193) and acceptance "The skill lands as one pull request" (line 217).
- Status: CONFLICT
- Current plan: SPEC.md:474 "Rules for every stage: one reviewable PR, one local action or one consented host operation; a stage never enables a later one". The coordinator is split: S13 substrate (SPEC.md:497), S14 merge path plus `/sc:coordinator` command and skill (SPEC.md:498), S15 four PRs S15a to S15d (SPEC.md:499), S16 observability (SPEC.md:500). Decision D14 (SPEC.md:90) fixed this order. 655's single-PR delivery is REJECTED.
- Evidence from our documents: SPEC.md:499 "S15 transport, cap, restart, audit, hand-back, `report-entry`, cleanup `list` (four PRs: S15a ... S15d)". SPEC.md:474 "a stage never enables a later one".
- Concerns: none beyond the conflict. The test content (T1 to T13) is still usable per stage; see S14-F1.

### S14-F3 Throwaway issues and pull requests in more than one repo across both GitHub orgs as the test bed
- 655 says: Tests use throwaway issues and PRs "in more than one repo across both GitHub orgs the work report covers (IronbellyOrg and IronbellyGroup)" (body line 193).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md and DECISIONS.md for "IronbellyGroup", "two orgs", "throwaway", "cross-org". Our throwaway use is a single repo: OA-19 "at most one throwaway repo after the shadow run, cap 1" (SPEC.md:582), the S17 "enable one throwaway repo" (SPEC.md:501) and the FR-77 ruleset test (SPEC.md:341). Both orgs appear only as the work report's search scope (techref OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md:1004) and the `allowed_owners` list key (D07 C-012, see S14-F4).
- Component (NOT-COVERED only): OTHER, test fixtures and process.
- Feature statement (NOT-COVERED only): Provide and document a set of throwaway repos, one in each org the work covers, with throwaway issues and PRs that the local tests T1 to T13 can use and that are closed afterwards.
- Done when: a written fixture list names at least two throwaway repos in two different orgs and each local test names the fixture it uses.
- Depends on: S14-F1.
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/adversarial/merged-d15-position.md:93 "T1 | Logic rewrite, plus setup step | Uses two orgs and a listed repo with `repos.yaml`, which D07 removes." (only the `repos.yaml` part is rewritten; the two-org idea is not rejected). SPEC.md:582 limits switching on to one throwaway repo.
- Concerns: Creating throwaway issues and PRs is a GitHub write and needs the owner's go (SPEC.md:698). OA-19 caps switch-on, not testing, but cap 1 and `claim_by: poll` apply to any live repo.

### S14-F4 T1: poll finds issues across orgs, origin check per repo, each worker starts in its own repo's worktree
- 655 says: T1 uses throwaway issues in two repos, one per org, and proves "The poll finds issues across orgs, the origin check runs per repo, each worker starts in its own repo's worktree" (body line 197).
- Status: COVERED
- Current plan: Per-repo config and one dispatcher: FR-11 (SPEC.md:201; `run-all` runs `once --config <repo>.json` per project of `orca repo list`), FR-67 (SPEC.md:324; keys on `owner/name`, duplicate short name is `name_collision`), D07 C-012 (debates/D07/adversarial/merged-output.md:150: `allowed_owners` is already a list key, default `("IronbellyOrg",)`, so a second org is one setting), D15 C7 row keeps `check_origin` (D15 VERDICT.md:79), FR-30 worker started by the coordinator for the repo's own worktree (SPEC.md:232), RK-5 proving check "`run-all --dry-run` lists every repo" (SPEC.md:649). D15 G1 adopts T1 with a logic rewrite (SPEC.md:467).
- Evidence from our documents: n/a (covered).
- Concerns: The test itself is only adopted as a skeleton; no rewritten T1 text is in SPEC.md section 13. UNVERIFIED that `allowed_owners` currently includes IronbellyGroup (the default is IronbellyOrg only, per D07 round-2 rebuttal line 35).

### S14-F5 T2: only the user's own login counts; someone else, or co-assigned, is not picked up
- 655 says: An issue assigned to the user's own login is picked up; one assigned to someone else, or co-assigned, is not (body line 198).
- Status: COVERED
- Current plan: FR-01 (SPEC.md:191) "assigned only to the watcher login" with a NEW per-predicate case in `issue_watch/test_cycle.py`; D01 item 1 (DECISIONS.md:152). "Only to" excludes co-assigned issues. The plan adds the approval gate on top: assignment alone never starts work.
- Evidence from our documents: n/a (covered).
- Concerns: The 655 test expects pickup on assignment alone; in our plan that is only the first predicate (see S14-F21).

### S14-F6 T3: an issue for a repo with no local checkout is never started in the wrong repo
- 655 says: Never started in the wrong repo: the checkout is set up (FR-8, `orca project setup-clone`) or the case is escalated (body line 199).
- Status: COVERED
- Current plan: for the "never started in the wrong repo" effect: D15 C7 (D15 VERDICT.md:79) "`no_checkout` skip reason; keep `check_origin`", FR-20 (SPEC.md:210) adds reason `no_checkout`, SPEC.md:454 "`no_checkout` skip instead". D15 merged position line 95: first case dropped, skip reason becomes `no_checkout`.
- Evidence from our documents: n/a (covered).
- Concerns: SPEC.md has no acceptance test that names `no_checkout` beyond the reasons-table pin MC-10 (SPEC.md:210, 478). A builder must add a behavior test. The "escalate" alternative of 655 has no plan row (a skip is shown on the sweep and observer, DECISIONS.md:604).

### S14-F7 T3: set the checkout up with `orca project setup-clone`
- 655 says: For a repo without a checkout, the checkout is set up (FR-8, `orca project setup-clone`) (body line 199).
- Status: CONFLICT
- Current plan: D15 element C7 REJECTED (D15 VERDICT.md:79: "Needs `repos.yaml`; changes the machine; no recorded authorization"); SPEC.md:454 "C5 registry repository ... C7 `setup-clone` | REJECT ... remove; `no_checkout` skip instead". 655's setup step is REJECTED.
- Evidence from our documents: D15 VERDICT.md:79 "Reject | Needs `repos.yaml`; changes the machine; no recorded authorization".
- Concerns: none beyond the conflict.

### S14-F8 T4: two orchestrators or users see the same issue, only one claims (routing, assignee check, "Claimed by" marker, dispatch record)
- 655 says: Only one claims, through one routing, the assignee check, the "Claimed by" marker, the lease and the dispatch record (body line 200).
- Status: COVERED
- Current plan: FR-01 assignee check (SPEC.md:191); FR-03 `marker_in_window` so a hand claim and a watcher start never run two workers (SPEC.md:193; marker `<!-- sc:issue:claim -->`, SPEC.md:174); FR-21 claim evidence and delivery intent in one store save (SPEC.md:211); FR-29 adoption record by exclusive create (SPEC.md:231); FR-33 cap counts each issue once (SPEC.md:235); D07 one dispatcher and one coordinator per project (SPEC.md:83).
- Evidence from our documents: n/a (covered).
- Concerns: none. The lease part is S14-F9.

### S14-F9 T4: the lease for a second user or second orchestrator
- 655 says: The lease is one of the layers that keeps a second orchestrator or user from claiming the same issue (body line 200).
- Status: CONFLICT
- Current plan: OD-8 "No lease comment now; reserved with a trigger" (SPEC.md:104, QG4 verdict, 75%); FR-40 "reserve the lease comment (trigger: a second host or user polls; stale-lease rule first; marker `sc:coordinator:lease`)" (SPEC.md:242); D15 C8 DEFER (SPEC.md:456). 655's lease is REJECTED for the first build. The lease would also be a poll write, forbidden by NG-2 (FR-06, SPEC.md:196).
- Evidence from our documents: SPEC.md:104 "OD-8 | No lease comment now; reserved with a trigger. | OURS | QG4 | 75%".
- Concerns: A second host or user polling the same repo is the stated trigger; until then the only guard is the marker and the one dispatcher. The multi-user clause of 655 T4 cannot pass its lease part.

### S14-F10 T10: four issues of one repo, three go to orchestrator 1 and the fourth starts orchestrator 2
- 655 says: With at most 3 in flight each, "Three go to orchestrator 1, the fourth starts 2" (body line 201); the poll starts another orchestrator when the repo's others are full (body line 27).
- Status: CONFLICT
- Current plan: D07 removed "extra poll-started orchestrators per repo" (DECISIONS.md:325) and chose project-local coordinators with one coordinator per project (SPEC.md:83). FR-33 (SPEC.md:235): the cap is checked per coordinator id, the first build enforces 1 (not 3) "until claim agents have their own worktree", a full repo records `coordinator_full` (the poll skips; it never starts a second coordinator). FR-70 (SPEC.md:327) and RK-7 (SPEC.md:651) keep cap 1. 655's second-orchestrator start is REJECTED. D15 names T10 as a logic rewrite (merged-d15-position.md:99).
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/adversarial/merged-d15-position.md:99 "T10 | Logic rewrite, plus setup step | The poll starts coordinator 2; D07 has one coordinator."
- Concerns: The cap default (3) and the first-build value (1) differ from 655's 3; see FR-33.

### S14-F11 T10: none claimed twice; a killed orchestrator is restarted
- 655 says: Under the four-issue test none is claimed twice and a killed one is restarted (body line 201).
- Status: COVERED
- Current plan: FR-33 counts every pending, launched, claimed, woken, acked, unknown entry once per issue (SPEC.md:235, test "one issue counted once"); FR-21 and FR-29 (SPEC.md:211, 231) prevent a second claim or adoption; FR-34 (SPEC.md:236) restarts a dead coordinator with a resume wake, at most 3 times, an unreadable terminal list restarts nothing; S15a/S15b kill-and-restart tests (SPEC.md:499).
- Evidence from our documents: n/a (covered).
- Concerns: FR-34 says "until Coder 516 the duty holder is `ORCH-IronClaude` and nothing restarts"; Coder issue 516 (Coordinator worktree and session) is not landed (RK-5, SPEC.md:649), so restart cannot be proved before then.

### S14-F12 T5: restart in the middle of each wave, Run resumes with no second claim and no second `worker-start`
- 655 says: The Run resumes (`run-use`) with no second claim and no second `worker-start` (body line 202).
- Status: COVERED
- Current plan: FR-21 replay keeps the wake id, "an unknown launch receipt never relaunches" (SPEC.md:211); FR-29 adoption record by exclusive create before `worker-start`, with kill-and-restart tests (SPEC.md:231, FR-84 item 1 at SPEC.md:244); FR-24 `--resume` flag (SPEC.md:226); FR-34 restart (SPEC.md:236); M1 and M2 (FR-15, FR-16; SPEC.md:205-206); MC-6 (SPEC.md:478); S15a "kill-and-restart tests at every persistence boundary" (SPEC.md:499). "At-least-once, handling a round twice must have no second effect" (SPEC.md:125).
- Evidence from our documents: n/a (covered).
- Concerns: The Orca `run-use` verb is the Orca orchestration run binding; our plan names the `--resume` flag and per-issue state files instead (see memory note on Orca coordinator rebind). UNVERIFIED whether the coordinator uses Orca Runs at all; this is a design difference, the effect is covered.

### S14-F13 T6: worker asks, check-in and typing, `ask` then `reply`
- 655 says: "A worker that dies, stalls or asks": the check-in and playbook, `ask` then `reply` behave as written (body line 203).
- Status: COVERED
- Current plan: for the asks and check-in part: D15 D12 "one supervised `worker-start` route: mailbox, one message handled once per id, check-ins, restart" adopted with change (D15 VERDICT.md:96); FR-40 typing rules for worker terminals, never approve a permission prompt (SPEC.md:242); FR-14 and FR-28 mailbox nudge and pulling at each `check --wait` (SPEC.md:204, 230); SEC-20 / G2 rule 2 keeps a bound worker's `send` and `ask` as one plain call with no `--to` (SPEC.md:309; DECISIONS.md:271); FR-24 `--hourly` flag (SPEC.md:226).
- Evidence from our documents: n/a (covered).
- Concerns: Unproven live: U5 mailbox from outside a Run and `tui-idle` (SPEC.md:668, 708). The dying and stalling part is S14-F14.

### S14-F14 T6: a worker that dies or stalls
- 655 says: The FR-9 states and the playbook handle a worker that dies or stalls (body line 203; the FR-9 state list is defined in 655's own section on the work report, outside this section).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md, DECISIONS.md, FOLLOW-UPS.md, D08, D10, D15 for "stall", "stalled", "dies", "dead worker", "worker crash", "stuck", "playbook", "check-in". The only hits are: FR-34 (restart of a dead COORDINATOR, not a worker), FR-30 (a worker that fails to bind stops the start), FR-40 (typing rules) and the `--hourly` flag name (FR-24) with no rule saying what the hourly run checks or does when a worker is silent. The sweep reports what each session is doing (FR-41, SPEC.md:252) but no requirement tells the coordinator what to do with a dead or stalled worker.
- Component (NOT-COVERED only): COORDINATOR, it is the per-project session that watches workers.
- Feature statement (NOT-COVERED only): The coordinator detects a worker that has exited, gone silent or stopped without `worker_done`, records a named state for it in the issue's entry, and applies a written playbook (nudge, restart under the cap, or escalate to the person).
- Done when: a test with a killed worker and a stalled worker shows each state recorded in the report entry and the playbook action taken once.
- Depends on: 655 section 4 (worker states, FR-9) and the hourly worker check; S14-F13; FR-33 cap; FR-47 nine-row table.
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md:236 "FR-34 ... Restart a dead coordinator with a resume wake" (the restart rule names the coordinator only); SPEC.md:242 FR-40 covers typing only. No document states a stall rule.
- Concerns: UNVERIFIED how a stalled worker is told from a working one (655's rule typed-output freshness belongs to another section). Never approve permission prompts (FR-40) and no interrupt (OD-7, SPEC.md:103) limit what the playbook may do.

### S14-F15 T6: nine-row escalation rows 7 and 9 behave as written
- 655 says: "rows 7 and 9 behave as written" (body line 203); these are rows of 655's nine-row escalation table.
- Status: COVERED
- Current plan: FR-47 "nine-row table in the notice step only ... exactly nine rows" (SPEC.md:258; D15 D16 adopted, SPEC.md:463); FR-37 write an escalation or entry first, name-check fail-open (SPEC.md:239); FR-49 and OD-5 (SPEC.md:101, 260). Which row is 7 and which is 9 in the owner's table is UNVERIFIED (the table is in the archived design doc).
- Evidence from our documents: n/a (covered).
- Concerns: The push notice is not in the first build (OA-25a, SPEC.md:113); a test of row 8 or any push behavior would not pass. Rows 7 and 9 of 655 may refer to a binding and a hand-back stop; UNVERIFIED.

### S14-F16 T7: an issue with no plan, the plan call appends the three sections with the plan marker
- 655 says: "The plan call appends the three sections with the plan marker" (body line 204).
- Status: COVERED
- Current plan: PR 690 `/sc:issue --plan` adopted with change: D12 A7 (SPEC.md:445), FR-53 (SPEC.md:274), FR-54 one plan check with a shared case table (SPEC.md:275), FR-59 `plan_depth` (SPEC.md:280). Write boundary: "one body edit, no comment, label, assignment or launch" (D12 VERDICT.md:34). The write grant `issue.body.append_plan_sections` (SEC-07, SPEC.md:296).
- Evidence from our documents: n/a (covered).
- Concerns: The "plan marker" is a 655 detail; UNVERIFIED whether PR 690 writes one. Under our plan the call is made by a person or at hand-back (FR-35, FR-56); no unattended first plan call (see S14-F23).

### S14-F17 T7: a plan it cannot fill escalates and leaves the body unchanged
- 655 says: "one it cannot fill escalates, body unchanged" (body line 204).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md FR-53 to FR-59, D12 VERDICT.md and the clay-prs inventory for "cannot fill", "unchanged", "escalat", "fail". FR-35 mentions a failed re-plan only as a hand-back stop condition in the test list, not as a rule for the first plan.
- Component (NOT-COVERED only): COORDINATOR, the plan call is run from the coordinator wave and escalation is the coordinator's.
- Feature statement (NOT-COVERED only): When the plan call cannot write all three sections, the issue body is left unchanged and the coordinator records an escalation naming the issue.
- Done when: a test with an issue the plan call cannot fill shows the body byte-identical before and after and one escalation line in the issue's entry.
- Depends on: S14-F16; the unattended plan call (S14-F23); FR-37 escalation write.
- Evidence from our documents: no evidence found in our documents.
- Concerns: Depends on an unattended plan call that our plan defers (D15 A4).

### S14-F18 T8: PR watch and merge on a real throwaway PR, each merge condition holds back the merge
- 655 says: Each condition holds the merge back when it fails: failing check, unfinished review, open thread, no `worker_done`, moved head (body line 205).
- Status: COVERED
- Current plan: SEC-02 `merge-gate` with 13 closed reasons run twice around the head-pinned `gh pr merge --match-head-commit` (SPEC.md:291); SEC-03 reasons a go may not override: `head_moved`, `draft`, `review_stalled`, `changes_requested` and others, only `checks_failing` and `merge_safety` overridable with their own key (SPEC.md:292; D06 VERDICT.md:16 lists `checks_pending`, `review_pending`, `threads_open`, `worker_not_done`); SEC-04 reviewer hold (SPEC.md:293); T13 `tests/coordinator/test_merge_path.py` (SPEC.md:290-292); live "Merge-path rehearsal" on a throwaway repo (SPEC.md:711).
- Evidence from our documents: n/a (covered).
- Concerns: Under our plan `checks_failing` can be overridden with the owner's own go key; 655 says "never over a failing check without the human's explicit OK", which matches. The `merge-gate` verb exists nowhere yet (SPEC.md:674, UNVERIFIED).

### S14-F19 T8: a clean PR merges
- 655 says: "a clean PR merges" in the T8 test (body line 205); the orchestrator merges when every condition holds (acceptance line 223).
- Status: CONFLICT
- Current plan: D06 / SEC-01 (SPEC.md:290): merge only on a person's typed go naming repo, PR, 40-character head sha, method and the gate output; "A passing gate never triggers a merge." D15 T8 row: "Expects an autonomous merge of a clean PR; D06 item 1 needs a person's go" (merged-d15-position.md:98). 655's autonomous merge is REJECTED; merge automation needs an owner-recorded go age or "none" (SEC-01).
- Evidence from our documents: merged-d15-position.md:98 "T8 | Logic rewrite | Expects an autonomous merge of a clean PR; D06 item 1 needs a person's go."
- Concerns: This also makes 655 closeout cases "merge by the orchestrator" (S14-F26) a person's merge in our plan. Security: the shared GitHub login cannot tell a person from a script (RK-3, SPEC.md:647).

### S14-F20 T9: report entry from claim to close
- 655 says: The report entry is added at claim, updated at milestones only, shows the assignee and session link, and leaves the report at close (body line 206).
- Status: COVERED
- Current plan: E2 living report, E5 item template, E7 `report-entry` adopted with change (SPEC.md:464); FR-48 `report-entry` is the only writer of an entry file (SPEC.md:259); FR-45, FR-46 (SPEC.md:256-257); FR-49 (SPEC.md:260). FR-80 limits fields shown (SPEC.md:263).
- Evidence from our documents: n/a (covered).
- Concerns: Appendix B: the work-report skill was removed by PR 700, so FR-45, FR-46 and FR-48 are "blocked until the skill is restored" and the owner must decide whether to restore it (SPEC.md:778, 786). Until then T9 cannot run.

### S14-F21 T11: a complete issue is woken at once with no label
- 655 says: In the ten-issue hold test, "a complete one is woken at once with no label" (body line 207).
- Status: CONFLICT
- Current plan: FR-01 (SPEC.md:191) and D01 (SPEC.md:77): "Assignment alone never starts work"; a person's approval (`Approved` field, unedited since) and a Status in the allow-list are also required, and the start gate repeats at start time (FR-02, SPEC.md:192). A complete plan alone does not wake the coordinator. 655's "woken at once on assignment plus a passing plan check" is REJECTED. The "no label" half agrees with our plan (FR-06 forbids poll writes).
- Evidence from our documents: SPEC.md:447 "A12 assignment alone as trigger | REJECT". SPEC.md:191 "Assignment alone never starts work."
- Concerns: Two open owner decisions bear on this: OA-1 (both gates or only the start gate) and OD-2 (SPEC.md:98); if the owner later rules only the start gate stays, the approval step could shrink, but assignment alone is still not a start (D01, 78%).

### S14-F22 T11: an incomplete issue gets `hold:plan` and no comment
- 655 says: "an incomplete one gets `hold:plan` and no comment" (body line 207).
- Status: CONFLICT
- Current plan: D09 and Q03 (SPEC.md:85, 95): the poll writes nothing to GitHub (NG-2); FR-05 read-only plan check, skip as `held_incomplete` (SPEC.md:195); FR-06 strips the label writer (SPEC.md:196); FR-07 creates a local `holds` entry with no write and ignores a leftover `hold:plan` (SPEC.md:197); D15 A5 `hold:plan` label write REJECT now, deferred PR with conditions (SPEC.md:443). 655's label write is REJECTED. D15 names T11 a logic rewrite "The poll writes `hold:plan` labels; D09 and the NG-2 rule forbid it" (merged-d15-position.md:100).
- Evidence from our documents: SPEC.md:443 "A5 `hold:plan` label write | REJECT now; deferred PR | 686a; O3 | strip (FR-06); return only with a shown reader, NG-2 amendment, 24-hour shadow run, cron write test". DECISIONS.md:712 "PR 686 ships no GitHub write by the poll."
- Concerns: SPEC.md:678 UNVERIFIED: "anyone reads `hold:plan`" (a reader of the label must be shown first). A visible reason on the sweep and observer (`held_incomplete`) replaces the label.

### S14-F23 T11: ONE plan request after one hour with no change, from the poll to the repo's coordinator
- 655 says: "a plan request only after one hour with no change", sent once to the repo's orchestrator that makes the plan through `/sc:issue --plan` (body line 207; section 1 point 3, line 25).
- Status: NOT-COVERED
- Current plan: deferred, not built: D15 A4 "Plan request after one hour, wake `plan_requests[]` with the issue title | Defer | A wake-file item, not a GitHub write (D09 item 5); a title is free GitHub text (D10 item 5) | Not built now; if built, ids only and after D07 settles who plans" (D15 VERDICT.md:44; SPEC.md:442). Searched SPEC.md and DECISIONS.md for "plan request", "plan_requests", "one hour": only A4 rows. FR-13 limits wake items to `repo`, `number`, `url` (SPEC.md:203), so no plan-request item exists. FR-56 prints a warning for a person's claim only (SPEC.md:277).
- Component (NOT-COVERED only): WATCHER, the poll owns the one-hour timer and the wake item; the coordinator's plan call is S14-F16.
- Feature statement (NOT-COVERED only): When an assigned issue has failed the plan check for one hour with no body change, the poll writes one ids-only plan-request item to the repo's coordinator wake, once per issue and without a GitHub write.
- Done when: a fixture issue held for 59 minutes produces no plan request, at 60 minutes exactly one, and a second cycle produces none; the wake file holds no title or free text.
- Depends on: 655 section 3 hold (A); S14-F16; S14-F22 (replacement of the label by a local hold); FR-13 wake format; who plans (open per D15 A4).
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/VERDICT.md:44 "Not built now; if built, ids only and after D07 settles who plans".
- Concerns: Titles must not enter the wake (SEC-16, SPEC.md:305; D10 item 5). The 60-minute figure is Clay's; our 60-minute values are UNVERIFIED and owner-settable (SPEC.md:676).

### S14-F24 T11: plan record before acknowledgment, three kill windows lose nothing, `plan_stuck` after 60 minutes, a full coordinator gets no plan request
- 655 says: The plan record is written first and the acknowledgment second; three kill windows lose nothing; `plan_stuck` after 60 minutes; a full orchestrator gets no plan request (body line 207).
- Status: NOT-COVERED
- Current plan: none found for these as plan rows; searched SPEC.md, DECISIONS.md, D09 and D15 for "plan_stuck", "plan record", "plan_requests". The general ordering rule exists for claims (M1 FR-15: ack only after the per-issue state file exists, SPEC.md:205; FR-29) and the cap reason `coordinator_full` exists (FR-33). `plan_stuck` appears nowhere in our documents.
- Component (NOT-COVERED only): COORDINATOR, the plan record, ack ordering and `plan_stuck` stop are coordinator state; the "full coordinator" check is the watcher's cap (S14-F23).
- Feature statement (NOT-COVERED only): The coordinator writes the plan record before the acknowledgment of a plan request, survives a kill at each of three windows without losing or repeating it, and stops with a named `plan_stuck` reason after 60 minutes without a plan.
- Done when: kill-and-restart tests at each of three points leave one plan record and one ack; a request left 60 minutes shows `plan_stuck` in the issue's entry.
- Depends on: S14-F23; FR-15 and FR-21 (generalized from claims to plan requests).
- Evidence from our documents: no evidence found in our documents for `plan_stuck`. Related risk RK-9 (SPEC.md:653) "A crash between ack and state loses the issue" shows why record-before-ack matters.
- Concerns: Exists only if S14-F23 is built (deferred); it adds a reason to the reasons-table pin (FR-20 / MC-10).

### S14-F25 T11: `hold:backlog` does nothing; a hold removed by hand is not put back
- 655 says: "`hold:backlog` does nothing, a hold removed by hand is not put back" (body line 207; section 1 point 3).
- Status: COVERED
- Current plan: FR-01 (`no hold:backlog`) and FR-05 (skip as `held_backlog`) (SPEC.md:191, 195), FR-08 re-check at wake time (SPEC.md:198); `hold:backlog` stays set by hand (FR-82, SPEC.md:218). A hand-removed `hold:plan` cannot be put back because the poll never writes it (FR-06, FR-07: leftover `hold:plan` ignored).
- Evidence from our documents: n/a (covered).
- Concerns: none.

### S14-F26 T12: closeout (wave 8) after a merge, by a person, squash-merged, or closed unmerged
- 655 says: Wave 8 closeout after a merge by the orchestrator, by a person while the worker still runs (the hand-back waits for `worker_done`), squash-merged, closed unmerged (body line 208).
- Status: COVERED
- Current plan: FR-38 each cycle run `/sc:closeout <PR>` per merged PR under a go naming the close; `--apply` only on a recorded go (SPEC.md:240; D13); SEC-12 one per-PR go covers merge and close, no standing close (SPEC.md:301); FR-35 hand-back: old worker final first (SPEC.md:237); `/sc:closeout` (PR 683) is merged and kept (SPEC.md:758) and its skill checks that the PR really merged (installed skill description). The "merge by the orchestrator" case is S14-F19 (our merges are typed by a person).
- Evidence from our documents: n/a (covered).
- Concerns: UNVERIFIED that `/sc:closeout`'s own tests already cover squash and unmerged cases; they belong to the closeout PRs, not this plan.

### S14-F27 T12: `Fixes` versus `Refs` in the handoff (`already_closed`)
- 655 says: Closeout tests `Fixes` (reported as `already_closed`) and `Refs`; the handoff carries a `Fixes` or `Refs` rule (body line 208; acceptance line 220).
- Status: NOT-COVERED
- Current plan: none found as a requirement; searched SPEC.md, DECISIONS.md and D13/D15/QG3 for "already_closed", "Refs", "Fixes". Only the risk is stated: SEC-12 "state that a `Fixes` line still closes at merge" (SPEC.md:301); RK-10 "Closeout or a `Fixes` line closes unfinished work" (SPEC.md:654); FR-61 says the coordinator hands the worker a chain from its own template that names the filed plan (SPEC.md:282) with no `Fixes` or `Refs` rule.
- Component (NOT-COVERED only): COORDINATOR, the handoff template belongs to the coordinator.
- Feature statement (NOT-COVERED only): The coordinator's handoff template tells the worker to write `Refs #N` in the PR when the issue may not be finished and `Fixes #N` only when the plan says the PR completes it, and closeout reports `already_closed` when GitHub closed the issue at merge.
- Done when: a template test finds the rule in the handoff; a closeout test on a throwaway PR with `Fixes` reports `already_closed` and with `Refs` leaves the issue open.
- Depends on: 655 section 2 handoff nine sections; FR-61; FR-38.
- Evidence from our documents: SPEC.md:654 "RK-10 | Closeout or a `Fixes` line closes unfinished work".
- Concerns: A `Fixes` line closes the issue with no go, against OD-10 (no standing close; SPEC.md:106) and SEC-12, so the rule must default to `Refs`.

### S14-F28 T12: a not-done issue handed back and finished in a second round; cap, no-progress stop, failed re-plan, tracked change in the worktree, kills inside a hand-back
- 655 says: "a not-done issue handed back and finished in a second round; the cap, the no-progress stop, a failed re-plan, a tracked change in the worktree; kills inside a hand-back" (body line 208).
- Status: COVERED
- Current plan: FR-35 hand-back loop: stop on empty list, `HANDBACK_MAX` 3, `no_progress`, old worker final first, idempotent re-plan marker, re-plan with `/sc:issue --plan <N> --remaining <file> --depth <d>` (SPEC.md:237); kill-and-restart tests (SPEC.md:499); FR-39 cleanup refusals keep a whole worktree (SPEC.md:241). D15 D18 adopted (SPEC.md:463).
- Evidence from our documents: n/a (covered).
- Concerns: `HANDBACK_MAX` 3 is "not measured" (SPEC.md:237, 676). The "tracked change in the worktree" case maps to FR-39 only by inference; UNVERIFIED.

### S14-F29 T12: the second round starts with no person step
- 655 says: The hand-back is finished in a second round by the orchestrator itself (body line 208; acceptance line 226: re-plan through `--remaining`, new worker on a new branch).
- Status: CONFLICT
- Current plan: OD-2 (QG1, SPEC.md:98) "Hand-back round 2: re-plan, person re-approves, whole start gate repeats"; FR-35 state `waiting_reapproval`, then the poll gives a NEW wake id and the whole start gate repeats (SPEC.md:237); OD-13 a waiting hand-back does not count toward `max_in_flight` (SPEC.md:109). 655's automatic second round is REJECTED. D15 rewrote T12 for this (merged-d15-position.md:101: "start a round with no person step ... G-3 adds the re-approval step").
- Evidence from our documents: merged-d15-position.md:101 "T12 | Rewrite for hand-back, plus setup step | Sub-cases (e), (h), (i), (j), (k) and (l) start a round with no person step".
- Concerns: The `waiting_reapproval` expiry limit has no default (SPEC.md:237, SEC-21).

### S14-F30 T13: the audit's eight checks on throwaway pull requests
- 655 says: The eight checks run on throwaway PRs (body line 209); acceptance line 227: the audit runs eight checks with no model and no GitHub write, AU4a, AU4c and AU5 reach Clay.
- Status: COVERED
- Current plan: FR-36 audit AU1 to AU8, AU5 narrowed to `<<<<<<< ` or `>>>>>>> `, states it cannot see a push with no PR (SPEC.md:238; D15 D15 adopted, D15 VERDICT.md:99); `audit` is one of the `superclaude coordinator` verbs (FR-26, SPEC.md:228); FR-49 AU4a, AU4c, AU5 shown as entry lines marked waiting on a person, push notice reserved (SPEC.md:260); OD-5 (SPEC.md:101); S15c builds AU1-AU8 (SPEC.md:499). Test gap: the T13 conflict-marker banner case is added by D15 (merged-d15-position.md:102).
- Evidence from our documents: n/a (covered).
- Concerns: "Reach Clay" is by report-entry lines only in the first build (OA-25a, SPEC.md:113), not a push notice. Whether the audit uses no model is UNVERIFIED in our documents (the verbs are scripts, FR-26). Our own plan numbers its merge-path test T13 (SPEC.md:290); do not confuse it with 655's T13.

### S14-F31 T13: merge-safety hold (workflow file, rename out of a protected path, unreadable file list)
- 655 says: A workflow file change is held until Clay's OK for that head; a rename out of a protected path is held; an unreadable file list is a hold, never "no match" (body line 209).
- Status: COVERED
- Current plan: D06 adopts the `merge_safety` hold and fail-closed file list (D06 VERDICT.md:34, 45: "a rename out of `.github/workflows/` is invisible in `gh pr diff --name-only` but visible to the gate"); D15 D1 "fail-closed file list" (D15 VERDICT.md:85); SEC-03 `merge_safety` overridable only with its own key (SPEC.md:292); SEC-08 key `merge_safety:<PR>:<head sha>`, go ends when the head moves (SPEC.md:297); SEC-10 fail closed on `merge_safety_files: []` (SPEC.md:299); gate reason `snapshot_incomplete` never overridable (D06 VERDICT.md:16).
- Evidence from our documents: n/a (covered).
- Concerns: "Clay's OK" is the owner's typed go in our plan (SEC-08; shared login cannot tell a person from a script, RK-3, SPEC.md:647). The gate verb exists nowhere yet (SPEC.md:674).

### S14-F32 The 13 design questions, answered in 655's spec 2.1 and the rest left to UNVERIFIED items
- 655 says: The 13 questions (which login, routing, no double claim, a repo with no checkout, restart state, the plan write grant, the #442 gate, the merge method, the cadence, the wake format, how the report is served, information items, several orchestrators) are answered in spec 2.1; what remains open are the spec's UNVERIFIED items (body line 211).
- Status: COVERED
- Current plan: our plan answers the same questions in its binding decisions and requirements: login FR-01 (SPEC.md:191); routing and one dispatcher D07 / FR-11 (SPEC.md:83, 201); no double claim FR-03, FR-21 (SPEC.md:193, 211); no checkout `no_checkout` (SPEC.md:454); restart state FR-15, FR-16, FR-21, FR-34 (SPEC.md:205-206, 211, 236); plan write grant SEC-07 `issue.body.append_plan_sections` (SPEC.md:296); the #442 gate FR-52 and the guard probe (SPEC.md:273, 706); merge method per-repo `merge` block (DECISIONS.md:328); cadence FR-10 cron `*/5` (SPEC.md:200); wake format FR-13 (SPEC.md:203); how the report is served FR-42, FR-79 (SPEC.md:253, 262; D11); information items FR-09 and OD-9 off by default (SPEC.md:199, 105); several orchestrators D07 and FR-33 (see S14-F10, a CONFLICT). The "remaining open items are UNVERIFIED" rule matches NFR-05 and the table of SPEC.md section 12.2 (SPEC.md:343, 662).
- Evidence from our documents: n/a (covered).
- Concerns: Several answers differ from 655's (assignment alone, labels, cron versus automation, merge go, one coordinator). 655 spec 2.1 itself is not in our documents (the design doc is gone from master, SPEC.md:758); the mapping is from the 655 question list in this section only.

### S14-F33 Acceptance items touching this section: live test, shadow run, lock test and restart test pass before `enabled: true`; #442's checks pass before the first worker on a real issue
- 655 says: "The live test, shadow run, lock test and restart test pass before `enabled: true`; #442's checks pass before the first worker on a real issue. #450 is closed as replaced." (acceptance line 230).
- Status: COVERED
- Current plan: S17 live tests then enable one throwaway repo (SPEC.md:501); section 13.2 live firing tests: cron shadow run 24 hours (SPEC.md:705), guard probe with issue 442's twelve observations (SPEC.md:706), worker binding (SPEC.md:707), cron and worktree after two restarts (SPEC.md:713); FR-23 `auto_enable` ships false and the owner turns it on once after S17 (SPEC.md:213); OA-28a (SPEC.md:118); FR-52 gate (SPEC.md:273); state lock test `tests/coordinator/test_state_lock.py` (SPEC.md:228) and `flock -n` (SPEC.md:200) for the lock. "#450 closed as replaced" belongs to another section.
- Evidence from our documents: n/a (covered).
- Concerns: Which of our tests corresponds to 655's "lock test" is UNVERIFIED (state lock versus cron `flock`). Nothing in 13.2 has run (SPEC.md:698).

## Section summary
- 33 feature rows. 655's test list T1 to T13 is largely adopted by the current plan as a skeleton (D15 G1, SPEC.md:467), with the logic of T1, T3, T4, T8, T10, T11 and T12 rewritten; no rewritten T-text exists in SPEC.md section 13, which has its own live-test table (SPEC.md:698-713).
- CONFLICT rows reject: one-PR delivery, `setup-clone`, the lease, a second poll-started coordinator, autonomous merge of a clean PR, wake on assignment alone, `hold:plan` label writes, and a second hand-back round with no person step.
- NOT-COVERED rows are: the pre-PR local end-to-end gate with results in the PR body, the two-org throwaway test bed, worker death and stall handling, the unfillable-plan escalation, the one-hour plan request, plan-record, kill-window and `plan_stuck` handling, and the `Fixes` versus `Refs` handoff rule. All but the first two depend on features of other 655 sections (hold, hand-back, worker watch).
- A builder must know: our plan numbers its own merge-path test T13, which differs from 655's T13; the work report tests (T9) are blocked by the removal of the report skill in PR 700 (SPEC.md:778); and every live write to a throwaway issue or PR needs the owner's go.
