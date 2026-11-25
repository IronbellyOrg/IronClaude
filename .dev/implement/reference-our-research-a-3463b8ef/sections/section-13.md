# Section 13 analysis: What runs in parallel
Counts: COVERED 11, CONFLICT 12, NOT-COVERED 2 (25 features)

Source: issue 655 body lines 175-189 (table), acceptance criteria lines 217, 228-230. Current plan: SPEC.md section 8 (stages S0 to S17), section 6 (PR dispositions), Appendix B (update after PR 700), D03, D07, D11, D14 verdicts, DECISIONS.md.

Paths used below (short names): SPEC = /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md ; DEC = .../20261120-pr686-unify/DECISIONS.md ; Dnn = .../20261120-pr686-unify/debates/Dnn/VERDICT.md.

### S13-F1 The spec is done and approved; every other row starts after it
- 655 says: The spec (`docs/designs/orchestrator.md`) is "done, approved (ruling 37)" and the rows below start after it (body line 179).
- Status: CONFLICT
- Current plan: The design doc is gone from master (PR 700) and was only "approved by the owner (Clay)", which is not the owner's approval. The plan's own spec is SPEC.md, and no builder starts PR B or PR E until an owner-reviewed amendment merges: FR-68 (SPEC.md:325), SPEC.md:389, SPEC.md:569 (10.5), Appendix B.3 item 2 (SPEC.md:787). 655's "approved, so start" is REJECTED.
- Depends on: none
- Evidence from our documents: SPEC.md:389 "PR 681 ... 'approved by the owner (Clay)' | SUPERSEDED BY PR 700 ... no builder starts PR B or PR E before it merges". D07 VERDICT.md:31 "the design's own header says 'approved by the owner (Clay)' and defines 'the user' as Clay ... so its rulings ... are not the repository owner's decisions on topology."
- Concerns: The owner has not yet decided whether to restore the 681 design text (B.3 item 2). Until then the gate "no builder starts PR B or PR E" stays on.

### S13-F2 Issue #651 (plan sections in the issue templates) runs now, waits for nothing
- 655 says: #651 starts now and waits for nothing (body line 180).
- Status: COVERED
- Current plan: Already done. PR 661 (merged, closes issue 651) is KEEP: SPEC.md:394 and SPEC.md:69. D03 item 6 keeps the creation-time plan sections as an extra layer (D03 VERDICT.md:20).
- Depends on: none
- Evidence from our documents: SPEC.md:394 "PR 661 (merged plan sections in the four issue templates; closes issue 651) | KEEP".
- Concerns: none

### S13-F3 A separate private "orchestrator repo" (IronOrchestrator) exists and runs in parallel with everything
- 655 says: The orchestrator repo is created and moved into in parallel with everything; B's local tests and PR C need it (body line 181; also body lines 28 and 154, acceptance line 228).
- Status: CONFLICT
- Current plan: D07 item 2 "No registry repo": the plan removes the separate `IronbellyOrg/IronOrchestrator` repo, `orchestrators.json`, `repos.yaml`, the 30-minute idle end. FR-11 says "no registry repository, no `repos.yaml`". Topology is project-local coordinators (`COORD-<RepoName>`, `Coordinator` worktree, `coordinators` records branch): FR-11 (SPEC.md:201), FR-64 (SPEC.md:321), D07. 655's repo is REJECTED as a prerequisite.
- Depends on: none
- Evidence from our documents: D07 VERDICT.md:16 "No registry repo. The spec removes the separate `IronbellyOrg/IronOrchestrator` repo ... Test: a grep of the unified spec for `orchestrators.json` and `repos.yaml` finds only the 'rejected' table." D07 VERDICT.md:30 "CLAY needs a hand-made clone ... REQ R17 says 'Nothing in the setup is manual.'"
- Concerns: The private repo already exists on GitHub (D07 read `private: true`). D07 VERDICT.md:70 leaves "whether to keep it for the report session" as an open, non-blocking owner decision.

### S13-F4 Moving the spec and the work report state into the orchestrator repo
- 655 says: Part of the repo row: "moving the spec and work report state into it" (body line 181; acceptance line 228 "coordinator spec and work report state live in the orchestrator repo").
- Status: CONFLICT
- Current plan: Records live on the project's `coordinators` branch (FR-64, SPEC.md:321; SEC-14 import at S13, SPEC.md:303 and 497). The coordinator design text lives in this spec or in `docs/designs/` files the owner writes (Appendix B.3 item 2, SPEC.md:787). The report's state path becomes per-user and stores only `session_id` (FR-46, SPEC.md:257). None of these points to the orchestrator repo.
- Depends on: S13-F3
- Evidence from our documents: SPEC.md:787 "No: the coordinator design lives only in this spec and `docs/designs/` files the owner writes." DEC.md:17 "any recommendation to edit that design file is moot until the owner decides to restore it".
- Concerns: Same open owner decision as S13-F3 about using the private repo for the report session.

### S13-F5 PR D first: retire the old approval gate, waits for nothing
- 655 says: PR D (retire the approval code in `issue_pipeline`, WC-17, guard G2 rule 1) starts first and waits for nothing (body line 182; section 12 step 3; acceptance line 229).
- Status: CONFLICT
- Current plan: The plan keeps BOTH gates until the owner rules (D03 and D14; OA-1, SPEC.md:554). PR 682 (Clay's deletion) was rolled back by PR 700, so the pre-682 tree is on master (Appendix B.1, SPEC.md:758). Only a new removal PR could ever happen, and only if the owner answers "only the start gate stays" (8.3, SPEC.md:507). The plan's first step is S0 hold then S1 merge PR 693 (SPEC.md:484-485), not a gate removal. 655's PR D is REJECTED.
- Depends on: none
- Evidence from our documents: D14 VERDICT.md:25 "PR 682 ... REVERT ... Owner says in chat that BOTH gates stay". SPEC.md:507 "After PR 700 the plan-approval code is on master, so this branch now means a new removal PR".
- Concerns: Owner answer to OA-1 is still to be recorded after the fact (Appendix B.3 item 4, SPEC.md:789).

### S13-F6 PR A is the poll core, built in parallel with D
- 655 says: PR A (assignment-only discovery, repo list, routing, hold, 62 reasons, tier validation) runs in parallel with D (body line 183; section 12 step 3).
- Status: COVERED
- Current plan: The poll core is PR 686 (Clay's draft), kept and adapted in place as ONE draft: S11 (SPEC.md:495), FR-73 (SPEC.md:337), SPEC.md:384, L-10 (SPEC.md:363). The content differs (D01 keeps the approval gates; no label writer, no registry), but the deliverable "poll core as PR A" exists. Content-level differences belong to other sections.
- Depends on: 655 section 1 and section 12 step 3 (poll content)
- Evidence from our documents: SPEC.md:384 "DRAFT now ... then KEEP-ADAPT in place as ONE draft; not merge, not split, not close".
- Concerns: none

### S13-F7 PR A merges after PR D
- 655 says: PR A merges after D (body line 183).
- Status: CONFLICT
- Current plan: PR 686 merges after S2, S9 and S10 and only after MC-1 to MC-11: S11 (SPEC.md:495), SPEC.md:384 ("revert merged ... planb landed; names settled; PR 690's check merged"). PR D does not exist in the plan; the equivalent precondition (the gate code present) is already met by PR 700, and S9 (planb) must land first, which 655 does not have.
- Depends on: S13-F5
- Evidence from our documents: D14 VERDICT.md:20 "REBASE-AND-ADAPT in place, as a draft ... Revert merged; planb landed first; D08 names settled; PR 690's `plan_body.py check` merged". D03 VERDICT.md:17 "PR 686 must not merge ahead of this decision (mandatory precondition)".
- Concerns: 655's A has no planb step; the owner's local branch (planb) must be re-checked first (SPEC.md:372).

### S13-F8 The spec fixes the wake format that A and B build against
- 655 says: The wake format is fixed in the spec before A and B are built (body line 183).
- Status: COVERED
- Current plan: The wake envelope and acknowledgment are specified and renamed before PR 686 merges: FR-13 to FR-19 (SPEC.md:203-209), FR-63 (SPEC.md:320), D10 (HYBRID, DEC.md summary line 107), D08 names (full debate).
- Depends on: none
- Evidence from our documents: SPEC.md:320 "Rename before PR 686 merges: `orchestrator-wake/1` and `-ack/1`, mailbox kind ...".
- Concerns: The format is Clay's envelope with changes (id-only nudges, M1, M2); a builder must follow FR-13 to FR-19, not 655's text.

### S13-F9 PR P (`/sc:issue --plan`) is built in parallel with A
- 655 says: PR P, the `/sc:issue` plan mode, runs in parallel with A (body line 184).
- Status: COVERED
- Current plan: PR 690 is KEEP-ADAPT and merges early in lane 1: S2 (SPEC.md:486), FR-53, FR-54 (SPEC.md:274-275), SPEC.md:385. S1 to S5 "can run beside" lane 2 (SPEC.md:503).
- Depends on: none
- Evidence from our documents: SPEC.md:503 "S1 to S5 do not depend on lane 2 and can run beside it."
- Concerns: PR 690 needs PR 693 merged first (four shared files) and D12's four fixes (SPEC.md:385).

### S13-F10 PR P waits for PR D to be merged
- 655 says: PR P waits for PR D merged (body line 184).
- Status: CONFLICT
- Current plan: PR 690 waits for PR 693 (owner's PR) and OA-2, not for any gate removal: S2 preconditions "S1; OA-2" (SPEC.md:486). D14's lane 1 does not queue behind the revert: PR 690 and PR 693 "share no code with the revert or PR 686". 655's dependency is REJECTED (and PR D itself is rejected, S13-F5).
- Depends on: S13-F5
- Evidence from our documents: D14 VERDICT.md:49 "Independent work should not queue behind the hardest item: PR 690 and PR 693 share no code with the revert or PR 686."
- Concerns: none

### S13-F11 PR B, the orchestrator skill, is ONE pull request
- 655 says: The skill (all ten waves, refs, four templates, playbook, verbs) lands as one PR (body line 185; section 12 step 3; acceptance line 217).
- Status: CONFLICT
- Current plan: The coordinator is built in stages: S13 substrate, S14 merge path plus `/sc:coordinator` command and skill, S15 split into four PRs (S15a wake-check and ack, S15b cap, S15c audit and hand-back and `report-entry` and `escalate`, S15d cleanup list), S16 glue (SPEC.md:497-500). The rule for every stage is "one reviewable PR" (SPEC.md:474). 655's single big PR is REJECTED.
- Depends on: none
- Evidence from our documents: SPEC.md:499 "S15 ... (four PRs: S15a ... S15b ... S15c ... S15d ...)".
- Concerns: Naming: plan says command `/sc:coordinator`, skill `sc-coordinator-protocol` (FR-24, SPEC.md:226), not `orchestrator`.

### S13-F12 PR B is opened only after PR A and PR P are merged
- 655 says: PR B waits for A and P merged before its PR is opened (its tests fake the plan call) (body line 185).
- Status: CONFLICT
- Current plan: S13 preconditions are "S10 merged; OA-26"; S14 needs "S13; OA-6, OA-11, OA-12, OA-13, OA-27" (SPEC.md:497-498). Neither lists S11 (PR 686) or S2 (PR 690). Preconditions are owner decisions (OA-6, OA-11, OA-12, OA-13, OA-27) that 655 does not have. S12, S16 and S17 do wait for S11 (SPEC.md:496, 500-501).
- Depends on: S13-F6, S13-F9
- Evidence from our documents: SPEC.md:364 "L-11 New code after S10 merges: substrate, merge path with the bound worker route, transport, cap ..." (no wait for PR 686).
- Concerns: S10 is itself SUPERSEDED BY PR 700 (design doc gone; amendment needs owner-reviewed restoration first, SPEC.md:494), so S13 effectively waits for the owner's decision in Appendix B.3 item 2. A builder must not start S13 on 655's rule.

### S13-F13 T1 to T13 local end-to-end tests pass before PR B is opened
- 655 says: PR B is opened only after the local end-to-end tests T1 to T13 pass (body line 185; section 14; acceptance line 217).
- Status: COVERED
- Current plan: The T1 to T13 tests are carried as G1 "ADOPT+CHANGE" with T1, T3, T4, T8, T10, T11 logic rewritten and T12 for hand-back (SPEC.md:467). T13 is `tests/coordinator/test_merge_path.py` (S14, SPEC.md:498). Live tests run before the poll is enabled (13.2, SPEC.md:698-711).
- Depends on: 655 section 14 (the test list itself)
- Evidence from our documents: SPEC.md:467 "G1 tests T1-T13 ... ADOPT+CHANGE ... T1, T3, T4, T8, T10, T11 logic rewritten, T12 for hand-back".
- Concerns: The plan does not say the tests must pass "before the PR is opened" nor "results in the PR description" (655 spec 9.2); it gates on per-stage tests plus live tests before enabling. Test details belong to the section 14 analyst.

### S13-F14 #651 is needed by PR B at run time only
- 655 says: PR B needs #651 "at run time only" (body line 185).
- Status: COVERED
- Current plan: The plan check runs at run time through `plan_body.py check`: FR-05 (SPEC.md:195), FR-54 (SPEC.md:275). #651 itself is already merged (S13-F2).
- Depends on: S13-F2
- Evidence from our documents: SPEC.md:275 "Keep one plan check: `plan_body.py check` is the reference".
- Concerns: none

### S13-F15 Issue #668 (the closeout skill) is built in parallel; merged before the live test
- 655 says: #668 is not a 655 piece, is built in parallel with A and B, merged before the live test; PR B's tests use a fake closeout (body line 186; acceptance line 226).
- Status: COVERED
- Current plan: `/sc:closeout` (PR 683) is already merged and kept: SPEC.md:392, D13 (HYBRID). The coordinator calls it per merged PR under a go naming the close: FR-38 (SPEC.md:240). Appendix B.1 says PR 683 survived PR 700 (SPEC.md:758).
- Depends on: none
- Evidence from our documents: SPEC.md:392 "PR 683 (merged `/sc:closeout`; issue 668 is its request) | KEEP | ... wire as coordinator step (FR-38)".
- Concerns: Plan's close authority is a per-PR typed go (OA-12, SPEC.md:558), not an automatic close; that is a section 8 matter.

### S13-F16 PR C: move `agent-work-report` into IronClaude, in parallel with A and B
- 655 says: PR C moves the work-report skill into IronClaude, in parallel with A and B, waiting for the orchestrator repo so the daily run keeps working (body line 187; acceptance line 228).
- Status: CONFLICT
- Current plan: The move was PR 684, and PR 700 removed the skill from master. Restoring it needs a later owner-approved PR (Appendix B.3 item 1, SPEC.md:786; SPEC.md:393). It does not wait for an orchestrator repo; D11 makes state per-user (FR-46) and the report reads sweep rows (FR-45). FR-45, FR-46, FR-48 are blocked until the skill is restored (SPEC.md:778). 655's unconditional "in parallel" is REJECTED until the owner decides.
- Depends on: S13-F3
- Evidence from our documents: SPEC.md:786 "Decide whether to restore the PR 684 skill ... Yes: the D11 adoption of the living report proceeds ... No: FR-45, FR-46 and FR-48 are dropped or rewritten". DEC.md:24 "D11 ... SUPERSEDED BY PR 700 for every action that builds on the skill."
- Concerns: Open owner decision; the report skill is currently absent from master.

### S13-F17 The daily report run keeps working while the skill moves (IronFlow copy kept updated)
- 655 says: PR C waits for the orchestrator repo "so the daily run keeps working"; the IronFlow copy is kept updated (body line 187; acceptance line 228).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md and FOLLOW-UPS.md for "IronFlow", "daily run", "daily report" (no hits); D11 VERDICT.md only says the IronFlow coordinator spec was not read (line 108); DEC.md lines 10, 17, 24 note the skill was removed. Nothing says who keeps the existing daily report running or the IronFlow copy synced during the gap.
- Component (NOT-COVERED only): OTHER, because it is a transition and repo-sync duty for a skill that the plan has not decided to restore, not a watcher, coordinator or dashboard deliverable.
- Feature statement (NOT-COVERED only): Say how the existing daily work report keeps running, and how the IronFlow copy of the report skill is kept in step, between PR 700 and any later restore of the skill.
- Done when (NOT-COVERED only): A written owner answer in chat names which copy of the report skill runs the daily report and who updates the IronFlow copy until the restore PR merges.
- Depends on: S13-F16
- Evidence from our documents: DEC.md:24 "SUPERSEDED BY PR 700 for every action that builds on the skill." D11 VERDICT.md:108 "The IronFlow coordinator spec was not read."
- Concerns: UNVERIFIED whether the IronFlow copy still runs (not read here).

### S13-F18 Live test (owner-run) after A, B, P, the repo and #668 are merged
- 655 says: The owner runs the live test (real `gh` and Orca, throwaway issues) after A, B, P, the repo and #668 (body line 188; section 12 step 7).
- Status: COVERED
- Current plan: S17 "live tests, then enable one throwaway repo" after S14 to S16 and Coder 515 and 516, with section 13.2 listing the live firing tests (SPEC.md:501, 698-713). The orchestrator repo is not a prerequisite (S13-F3); PR 690 and PR 683 are already ahead of it in the stage order.
- Depends on: S13-F6, S13-F9, S13-F11, S13-F15
- Evidence from our documents: SPEC.md:700 "Nothing below has run. Each needs the owner's go if it writes to GitHub or types into a session."
- Concerns: Plan also requires all HIGH rows of 12.1 proven or accepted in chat and OA-19, OA-20, OA-23 (SPEC.md:501); 655 has none of these.

### S13-F19 #442's launch checks pass before any governed worker on a real issue
- 655 says: #442's launch checks run before any governed worker starts on a real issue (body line 188; acceptance line 230).
- Status: COVERED
- Current plan: Issue 442's twelve observations are the guard probe in 13.2 (SPEC.md:706). Workers start bound to the guard (FR-30, SPEC.md:232); `WORKER_BINDING_PROVEN` stays false until the owner flips it (OA-20, SPEC.md:583); governed levels stay closed (FR-52, SPEC.md:273); S9 "no governed level launches while R33 is false" (SPEC.md:493).
- Depends on: none
- Evidence from our documents: SPEC.md:583 "OA-20 | flip `WORKER_BINDING_PROVEN` after the probe ... not flipped: no worker on a real issue, probe issues only".
- Concerns: none

### S13-F20 PR E part one: real fixtures and the live-test record
- 655 says: After the live test comes PR E with real fixtures and the live-test record (body line 188; section 12 step 3 and step 7).
- Status: COVERED
- Current plan: The cron shadow run captures real replies to replace the assumed fixtures (SPEC.md:705); S17 keeps a go/no-go record (code head, host, primitive hashes, fixture captures, probes) (SPEC.md:501); NFR-05 asks for a 13.2 record (SPEC.md:343).
- Depends on: S13-F18
- Evidence from our documents: SPEC.md:705 "real replies captured to replace assumed fixtures".
- Concerns: Plan has no separate "PR E" stage; the record is kept by an agent and the fixtures replaced in S17 work. No builder starts PR E before the amendment merges (SPEC.md:569).

### S13-F21 PR E part two: the owner runbook rewritten as 655 describes it
- 655 says: PR E rewrites the owner runbook: labels, approvers and cron removed, Orca automation and a pointer to the orchestrator repo added (body lines 187-188 and 276).
- Status: CONFLICT
- Current plan: Labels and approvers stay (OA-8 "trigger label stays", D01 gate stays: SPEC.md:553). Cron stays the scheduler and Orca automation is REJECTED as scheduler (B2, SPEC.md:449; D02, SPEC.md:78). No orchestrator repo (S13-F3). The runbook text change the plan wants is narrower: correct the cron rationale and the six-field cron line (FR-69, SPEC.md:326). The content of 655's rewrite is REJECTED.
- Depends on: S13-F3
- Evidence from our documents: SPEC.md:449 "B1 precheck pattern; B2 Orca automation as scheduler | B1 ADOPT+CHANGE (fallback); B2 REJECT | ... cron stays".
- Concerns: none

### S13-F22 A runbook update after the live test, matching the unified design
- 655 says: Implied by PR E: after the live test the owner's runbook is brought up to date (body line 188).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md and FOLLOW-UPS.md for "runbook", "issue-watcher-setup", "PR E". Only hits: SPEC.md:69 says "PR E (runbook rewrite) ... unbuilt", SPEC.md:387 merges PR 685 (issue 442 runbook), SPEC.md:326 (FR-69) fixes cron lines. No stage updates the runbook after the live test.
- Component (NOT-COVERED only): OTHER, because it is documentation, not a watcher, coordinator or dashboard feature.
- Feature statement (NOT-COVERED only): After the S17 live tests, update the owner runbook (`docs/designs/issue-watcher-setup.md` and the issue 442 runbook) to the unified design as run, with the real captured steps.
- Done when (NOT-COVERED only): A merged PR changes the runbook text and the S17 record names the PR; a person can follow it to switch a repo on and off.
- Depends on: S13-F18
- Evidence from our documents: SPEC.md:69 "PR B (coordinator skill) and PR E (runbook rewrite) are unbuilt."
- Concerns: SPEC.md:569 gates PR E on the design amendment; it is not stated whether the plan keeps the name "PR E".

### S13-F23 Shadow run first, then switch-on, last and in that order
- 655 says: Shadow run (24 hours dry run, lock test, restart test) then switch-on, last, after the live test and PR E (body line 189; section 12 steps 8 and 9).
- Status: COVERED
- Current plan: S17 runs the live tests, then a 24-hour `run-all --dry-run` shadow run that wrote nothing, then enables ONE throwaway repo; the owner turns `auto_enable` on once afterwards (FR-23; OA-19, OA-28a): SPEC.md:501, 582, 565. No stage installs cron before S17 (FR-10, SPEC.md:200). Restart safety is tested earlier by kill-and-restart tests (S15a, SPEC.md:499).
- Depends on: S13-F18
- Evidence from our documents: SPEC.md:582 "OA-19 | switch a repo on | every repo off ... at most one throwaway repo after the shadow run, cap 1, `claim_by: poll`".
- Concerns: 655's two-process lock test and exit 75 are not named in S17 (the plan names `flock -n`, FR-10); the "Orca automation" in 655 step 9 is rejected (S13-F21).

### S13-F24 Switch-on also waits for PR C, PR D and #651
- 655 says: For the switch-on, also PR C, PR D and #651 must be done (body line 189).
- Status: CONFLICT
- Current plan: S17 waits for S14 to S16, Coder 515 and 516, the HIGH rows of 12.1, OA-19, OA-20, OA-23 (SPEC.md:501). PR D (gate removal) is rejected (S13-F5). PR C is an open owner decision (S13-F16). #651 is already done (S13-F2). Only the "PR D" and "PR C" parts conflict.
- Depends on: S13-F5, S13-F16
- Evidence from our documents: SPEC.md:501 (S17 preconditions) lists no report-skill PR and no gate removal.
- Concerns: S16 (observability glue) needs the report skill for FR-45, FR-46, FR-48 (SPEC.md:778), so PR C does bear on S16 once restored.

### S13-F25 Close #450 as replaced when switching on
- 655 says: At switch-on, "Close #450 as replaced by this issue" (body line 173, acceptance line 230); this follows the switch-on row.
- Status: CONFLICT
- Current plan: Issue 450 is KEEP open; Clay's 2026-11-18 comment awaits the owner's answer (OA-22): SPEC.md:427, 553. Issue 655 is KEPT and RESCOPED so the assignee drops "replaces #450" (SPEC.md:426; D14 VERDICT.md:28-29). 655's closing of #450 is REJECTED.
- Depends on: S13-F23
- Evidence from our documents: D14 VERDICT.md:29 "Issue 450 ... KEEP open, and answer Clay's 2026-11-18 comment | Its live test, shadow run and cron stay required under every verdict".
- Concerns: none

## Section summary
Section 13 is mostly a build-order table, and the plan overrides most of it. Rejected: the orchestrator repo and moving state there (D07), PR D first and every wait on it (gates stay, PR 700 already restored them), PR B as one pull request, the "approved spec" start rule, the PR C move as written, the 655 runbook rewrite and closing #450. Covered: #651 (done), #668 (done), PR P, the wake format, the T1 to T13 tests, #442 checks, fixtures and record, and shadow run then switch-on (S17). Not covered: keeping the daily report and IronFlow copy running while the skill is absent, and a runbook update after the live test.

