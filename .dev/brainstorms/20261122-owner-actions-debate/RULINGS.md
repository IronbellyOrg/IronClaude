# Owner rulings recorded in chat (recorded by the IronClaude coordinator; the owner writes no file)

Source of every proposal: SUMMARY.md and <id>/FINAL.md in this folder. A ruling counts only as the owner's words typed in this session.

## 2026-11-22 (owner message, quoted)
- "d) All approved". Scope: section D of the coordinator's list: X08 (no typed wake line; coordinator_autostart off everywhere until the owner says otherwise), X09 (watcher rehearsal on IronbellyOrg/orchestrator-sandbox; every repository stays off; no cron line and no real run-all before the gate pull request merges), X10 (probe on disposable issues 712 to 715; WORKER_BINDING_PROVEN stays False until a reviewed pull request), X12 (X-001 check on a throwaway repo, three runs, cap 1, fixed rule), X17 (correction comment on Coder issue 516 and a three-case Orca test on a scratch repository; the hold stays). Approved as proposed in each item's FINAL.md. NOT yet done: the Coder 516 comment text is shown to the owner before posting.
- "X15 - Approved". OA-1: both approval gates stay; PR 700 stands; no removal pull request; review on 2026-12-22, or at the first live watcher run, or before any launch level above Pipeline None, whichever is first; silence at the review means both stay.
- "X05 - Shelve / backlog this for now for further human debate. File and issue / proposal around the issue we are trying to solve with this being one of the proposed solutions". Filed as issue 722 (IronbellyOrg/IronClaude). OA-6 stays unnamed (plan default) until the owner decides.

## Asked for more context (no ruling yet)
X01, X02, X14 (section A), X03, X04, X13 (section B), X06, X07 (section C).

## Not addressed in the message
X11 (Clay's eight removal PRs), X16 (other hosts from the 2026-11-20 window).

## 2026-11-22 (second owner message, quoted)
- "X07 - assigning is allowed, all else approved". OA-11 standing grants for the coordinator: issue.comment, issue.status.move (to In review only) and issue.assign; one repository at a time; adopted issues only; 90 days at most; the owner revokes in chat. The plan-body grant (issue.body.append_plan_sections) waits for stage S15c. Merge and issue close are never standing (one per-pull-request go). Nothing is active until the checking code exists (stage S14). Note: assign can change who owns work; recorded as a known risk.
- "X01 - Approved". Done the lighter way: one status note on issue 716 (comment 7078226063) and one on issue 718 (comment 7078226256), no body edits, nothing closed.
- "X02 - Skip and archive this". Closed, not pursued. Issue 718 items D3 and D4 are marked not pursued in the 718 note. No question to Clay.
- "X04 - no test needed". Closed, accepted risk. No fingerprint test, no rule, no hook, no further work.
- "X13 - I merged this, we don't need to spend any more time here". Closed, nothing required. No note to Clay, no ledger paperwork.
- "X14 - do not restore, do not make notes". Closed. The design text is not restored; no hold comments, no notes.
- "X06 - Line 71 - more context". Open: line 71 context requested. Lines 57 and 246 not explicitly answered yet.
- "X03 - is this allowed with our current plan?". Answered: yes (see chat); awaiting the owner's decision.

## 2026-11-22 (third owner message, quoted)
- "X06 - Approved". Lines 57 and 246 as proposed; line 71 held. Agent running in worktree x06-contract-wording (result file X06/pr-result.md). The owner merges the pull request.
- "X03 - Shelve this, file an issue for later". Filed as issue 723. Nothing set on GitHub. Answers recorded: allowed by the plan (FR-75, OA-5); no paid plan needed for IronClaude (org on GitHub Free, repository public; Coder is private and would need a paid plan).
- "Rollout - I have cloned this project locally, make use of it for live rehearsals". Sandbox clone: /home/coder/workspaces/orchestrator-sandbox (registered in Orca). Started: stand-in Coordinator worktree and the R0 to R3 setup agent (rehearsal-r1; brief /home/coder/.cache/orch-decisions/x09-r1-brief.txt; result file X09/r1-result.md). R4 (a claim by hand) and S2 (switching on) each need a separate owner go naming the issue.
- "Rename - Skip this for now". No rename. The sandbox keeps the name orchestrator-sandbox.

## 2026-11-22 (fourth owner message, quoted)
- "Approver - Clayphi". The approver of the sandbox rehearsal is clayphi (never the ironbelly login). Clay must set the Approved field on the test issue; the coordinator asks Clay with a neutral comment on that sandbox issue once the issues exist.
- "For for R4" (read as "Go for R4"). Go 2 of X09: one claim launched by hand (one orca agent launch of /sc:issue --claim N at Pipeline None, into the sandbox stand-in Coordinator worktree) on ONE sandbox test issue N; the launch-level guard is not enforced for that one run; the same run is the X-001 check. The owner did not name N; the coordinator picks the first of the three new test issues and tells the owner N before launching. Preconditions: R1 to R3 finished, clayphi has set Approved on issue N, a fresh read of docs/designs/issue-pipeline-fu1.md section 6. Switching the watcher on (S2) is NOT covered; it needs its own go.

## 2026-11-22 (fifth owner message, quoted)
- "X11 - All approved, none are used, no backup required." Clay's eight removal pull requests (620, 622, 627, 629, 631, 632, 650, 656) are confirmed as merged. The owner states none of the removed tools are used. No backup folder, no per-host list, no per-host go for these removals. Pull requests 617 and 621 stay as covered by the plan the owner approved. Not changed by this ruling: stale text that still mentions /task (launch-level-guard.sh, commands/issue.md, core/WORKER-CONTRACT.md); nobody was asked to fix it.
- "X16 - We dont' care about other machines ... Stop persuing this, move on and abandon this effort". Abandoned. No note on issue 717, no per-host check, no Coder sentence, no host rows in STATE.md. The earlier proposal in X16/FINAL.md is not pursued.

## Status of the 17 items
All 17 now have an owner answer or are closed or parked. Still running: X06 agent (pull request for the owner to merge), X09 rehearsal setup agent (R0 to R3). Awaiting the owner: ORCH-Coder's relayed request for a peer-coordinator rules issue.

## 2026-11-22 (sixth owner message, quoted)
- "442 - run probe". Go for the X10 early probe on disposable issue 712 only. Done 12:20 UTC: one worker, bound by the guard, stopped. Result: X10/early-probe/RESULT.md. WORKER_BINDING_PROVEN untouched.
- "409 - continue from 718 if you can confirm everything from 409 is complete and nothing needs copying to 718". Condition NOT met: issue 409 is open; its remaining work is tracked in #706 (and remote fleet in #604), not in #718 (which holds four report-entry items from 655). Nothing needs copying to 718. Nothing retired or deleted. Findings: .dev/brainstorms/20261122-worktree-review/.
- "This checkout - push". The branch docs/409-orca-dashboard-designs is already on origin at the same commit (495eb96d1); nothing to push for that commit. Asked the owner whether to commit and push the staged and untracked files.
