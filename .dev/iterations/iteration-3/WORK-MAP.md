# Iteration 3 work map: epics, features and stories in work order

Built Wed 25 Nov 19:56 Central from the reviewed iteration proposal (`plan/min50/EXPANDED-PROPOSAL.md`, independent review PASS) and the planning run's maps of dependencies (`plan/DEPENDENCIES.md`) and overlaps (`overlap/OVERLAP-REPORT.md`). Machine-readable copy: `work-map.json`. Epics and features exist only in this file; no GitHub issue is created for them.

## How an agent uses this map
1. Find your epic (one per person). Work its features in the order listed, and the stories inside a feature in the order listed.
2. **Starts** is either "start now" (first in its lane) or "after #N" (the story before it in its lane, because it needs that story or must agree a shared scope with it). Nothing waits on anyone's answer. **Needs first** names each issue that must be merged first ("partial" means only part of the story waits; "order" means start after that story lands).
3. Read **Overlaps**: another issue covers part of the same ground. "link-only" means mention it and do not duplicate it; "merge-scope" means one scope for both issues: when the other issue is in this iteration, see **Settle with**; when it is not, the owner of this story settles the shared part at the start of the work, records it in the pull request and links the other issue. Nothing waits on Clay or on the other issue.
4. **Settle with** names another story in this iteration that covers the same ground (or, for #753 and #818, aims the opposite way). The owner of the first story in the lane settles the shared part at its start; when the other story has a different owner (named in the line), the two owners settle it together.
5. **Open question** is answered as part of the work, never waited on: use the recommended answer, or, where it says the issue owner decides, the owner of that story decides it at the start and records the answer in the pull request. **Note** sets a limit or gives context (for example "only its first step", "confirm and close", "branch from integration"); follow it.
6. **Unblocks** lists the issues that wait on this story (in this iteration or later); finishing it early frees them.
7. **Runs** says what can run at the same time. Every story is in a lane. Stories in the same lane run one after another, in the order shown (one needs the other, or they must agree one scope). Different lanes run in parallel, one agent per lane. The lanes are built from dependencies and overlaps only: two parallel stories may still edit the same file, which this map does not check (known cases are listed under "Between people" below). Before starting any two lanes at once, in any feature or epic, compare the files each will change (for example with `/sc:impact`) and run them in sequence if they share one.

Priority is the proposed level from the planning cards; the level set on GitHub is shown when it differs. Order of features in an epic: the features that serve the epic goal first, in pipeline order (`feature-order.tsv` gives the reason for each). Order inside a feature: what another story needs first (dependency or conflict), then priority, then how many issues it unblocks, then complexity (simpler first; not set counts as Medium), then size (smaller first). Open questions never affect the order.

## Overview
| Epic | Owner | Goal | Features | Stories | Lanes (stories that can start now, in parallel) | Run in sequence (behind another story in its lane) |
|---|---|---|---|---|---|---|
| E1 | Ryan | The watcher and the coordinator carry an approved issue to a merged pull request without a person passing it along, and their docs match what they do | 10 | 23 | 18 | 5 |
| E2 | Clay | Claiming, releasing and session tooling work reliably on integration, and the team's rules for worktrees, branches and changes are written down | 7 | 21 | 19 | 2 |
| E3 | Leandro | Workers can run unattended within safe limits, and the repo's tests and CI can be trusted | 3 | 12 | 12 | 0 |
| E4 | swill-ib | Swarm runs always leave a reliable completion marker and their results, on integration | 1 | 2 | 2 | 0 |

**Overlaps and conflicts inside this iteration (settle before building the shared part):**
- #753 and #818: The size of the approver list, with opposite aims. #753 makes every maintainer and admin an approver automatically. #818 (W10) says to block or flag a second approver until per-actor permission checks of the launched session exist. Built as written, #753 adds approvers that #818 would refuse.
- #590 and #766: Both fix the sweep's "could not determine" result for workers: the 50-read cap and unfollowed paging, and finished workers whose contract is not read.
- #772 and #774: The wording of what Pipeline Full means (and the "one local commit" line) across `commands/issue.md`, `refs/claim.md`, `launch-prompt.md`, `docs/designs/issue-watcher-status-pipelines.md` and the test at `tests/skills/test_issue_protocol.py`; also `WORKER-CONTRACT.md` and the status-pipelines design are edited by both.
- #409 and #706: The five acceptance criteria added to #409 on 2026-11-13 (same sweep facts, plain-English summary, named steps with colours, open a session, scale tests) are written in both issues.

**Between people (dependencies, shared work and shared files):**
- #837 (Clay) needs Ryan for the three repos only his login can change: IronHands-CLI, ironops-marketplace, irondots
- #409 (Clay) needs #706 (Ryan), and both carry the same five acceptance criteria: Ryan builds #706 and settles those criteria with Clay at its start; Clay then finishes #409
- #442 (Ryan) observes the launch-level guard that #825 (Leandro) changes: agree which guard version the observations run against before either starts (card 825; not verified in #442's steps)
- `WORKER-CONTRACT.md` is edited by #790, #771, #774, #755, #725 and #772 (Ryan) and by #446 and #699 (Leandro): run those in sequence or agree who edits which section
- #702 (Leandro) still has an update rule for the release-tag ruleset open, and #837 and #838 (Clay) copy the rulesets in `.github/rulesets/` to other repos: settle the release-tag rule in #702 first, or copy only the branch rulesets until it is settled

## E1: Ryan

**Goal:** The watcher and the coordinator carry an approved issue to a merged pull request without a person passing it along, and their docs match what they do

### E1-F1: Issue watcher: next-release items (subject 4)

**E1-F1-S1** [#818](https://github.com/IronbellyOrg/IronClaude/issues/818): [FEATURE] Issue watcher W10: Permissions of launched sessions (FU-6)
- Priority Medium; size S; complexity Simple; kind gap-closer; architecture change none
- Starts: start now
- Runs: lane E1-L1, in sequence: #818 then #753; in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: #753 overlaps, merge-scope (in this iteration)
- **Settle with** #753 (#753 has the same owner): The size of the approver list, with opposite aims. #753 makes every maintainer and admin an approver automatically. #818 (W10) says to block or flag a second approver until per-actor permission checks of the launched session exist. Built as written, #753 adds approvers that #818 would refuse.
- Open question (answered in the work, not waited on): Refuse or only warn about approvers beyond the first until the watcher can check each approver's own GitHub permission? Where is the permission level of each started session recorded? Recommended: Only warn (the 23 Nov rule in #753 makes every maintainer and admin an approver); record it in the watcher's audit log, which its status check already reads

**E1-F1-S2** [#816](https://github.com/IronbellyOrg/IronClaude/issues/816): [FEATURE] Issue watcher W8: Alert after three bad cycles (FU-4)
- Priority Medium; size M; complexity Medium; kind enhancement; architecture change none
- Starts: start now
- Runs: lane E1-L2 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: #775 overlaps, merge-scope
- Open question (answered in the work, not waited on): Where does the alert after three bad watcher runs go; does the check cover skipped issues and the stop at 100? Recommended: A ClickUp message (outside the workspace, so it works when the workspace is stopped); yes to both

**E1-F1-S3** [#819](https://github.com/IronbellyOrg/IronClaude/issues/819): [FEATURE] Issue watcher W11: One retry of an unknown launch outcome through Orca's operation id (FU-8, owner question Q2)
- Priority Medium (GitHub: Low); size M; complexity Medium; kind gap-closer; architecture change moderate
- Starts: start now
- Runs: lane E1-L3 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: #788 overlaps, link-only
- Open question (answered in the work, not waited on): Which retry form for an unknown watcher launch outcome? Recommended: The issue owner decides at the start of the work

**E1-F1-S4** [#822](https://github.com/IronbellyOrg/IronClaude/issues/822): [FEATURE] Issue watcher W14: check-config refuses a state folder that is not on a local disk (FU-12)
- Priority Low; size S; complexity Simple; kind gap-closer; architecture change none
- Starts: start now
- Runs: lane E1-L4 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -

### E1-F2: Approvals and the shared GitHub login (subject 5)

**E1-F2-S1** [#753](https://github.com/IronbellyOrg/IronClaude/issues/753): issue-watch: always accept maintainers and admins as approvers
- Priority High; size M; complexity Medium; kind gap-closer; architecture change moderate
- Starts: after #818 (the story before it in its lane)
- Runs: lane E1-L1, in sequence: #818 then #753; in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: #698 overlaps, link-only (in this iteration); #818 overlaps, merge-scope (in this iteration)
- **Settle with** #818 (#818 has the same owner): The size of the approver list, with opposite aims. #753 makes every maintainer and admin an approver automatically. #818 (W10) says to block or flag a second approver until per-actor permission checks of the launched session exist. Built as written, #753 adds approvers that #818 would refuse.

**E1-F2-S2** [#698](https://github.com/IronbellyOrg/IronClaude/issues/698): Release-worker and plan-approval checks rest on text matching and an assignee shortcut
- Priority Medium; size M; complexity Complex; kind decision; architecture change moderate
- Starts: start now
- Runs: lane E1-L5 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: #773 #775(conditional)
- Overlaps: #722 overlaps, link-only; #753 overlaps, link-only (in this iteration)
- Open question (answered in the work, not waited on): Which protection for release-worker: (a) the guard also catches the Python and Click routes, (b) release-worker refuses without an approval record, (c) the approval store is not writable by the worker's account, or (d) record that the guard is only a seatbelt? And the approver rule in done-when item 2? Recommended: The issue owner (Ryan) chooses the protection at the start of the work; the approver rule follows #753 (every maintainer and admin), and Ryan also decides whether the assignee shortcut stays (done-when item 2) and records both choices in issue-pipeline-fu1.md

### E1-F3: Coordinator workers: start, track and finish (subject 2)

**E1-F3-S1** [#790](https://github.com/IronbellyOrg/IronClaude/issues/790): [FEATURE] Coordinator C9: Handoff prompt template: fixed nine-section order, Fixes or Refs rule, no secrets, hand-back round block, regression gate
- Priority Medium; size M; complexity Medium; kind enhancement; architecture change moderate
- Starts: start now
- Runs: lane E1-L6, in sequence: #790 then #792; in parallel with every other lane
- Needs first: -
- Unblocks: #792 #799
- Overlaps: -
- Open question (answered in the work, not waited on): Decision 1: does the watcher only record a claim or result and wake the coordinator, or start the work itself? And may a pull request say "Fixes #N" only when it delivers the whole issue, or does Ruling 26 of docs/designs/sc-closeout.md apply? Recommended: The watcher records and wakes the coordinator, which is an agent (decision 1's suggested answer; the scheduled wake itself is #757, not in this iteration, so build the template for that model); "Fixes" only for a full delivery, otherwise "Refs", and align Ruling 26 to that

**E1-F3-S2** [#792](https://github.com/IronbellyOrg/IronClaude/issues/792): [FEATURE] Coordinator C11: Define and validate a valid worker_done message
- Priority Medium; size S; complexity Simple; kind enhancement; architecture change moderate
- Starts: after #790 (the story before it in its lane)
- Runs: lane E1-L6, in sequence: #790 then #792; in parallel with every other lane
- Needs first: #790
- Unblocks: -
- Overlaps: -
- Open question (answered in the work, not waited on): Decision 1: same handoff model as #790. What fields make a valid worker_done message? Recommended: Same model as #790; the fields are the ones the issue's "What to build" lists, defined and validated as part of this story
- Note: #790 first; the field list of a valid worker_done message is part of this work (the issue's "What to build" lists the fields)

**E1-F3-S3** [#771](https://github.com/IronbellyOrg/IronClaude/issues/771): [FEATURE] Wire `/sc:closeout` and `/sc:worktrees` into the coordinator's finish, and give a "not done" result somewhere to go
- Priority Medium; size M; complexity Medium; kind gap-closer; architecture change moderate
- Starts: start now
- Runs: lane E1-L7 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: #339 overlaps, merge-scope; #716 overlaps, merge-scope; #761 overlaps, link-only; #799 overlaps, link-only
- Open question (answered in the work, not waited on): Does the worktrees schedule stay off? Does "never closes" in ruling R38 also cover issues? Recommended: Schedule stays off (the coordinator runs closeout and cleanup after each merge); R38 covers merging only, closeout may close a finished issue

### E1-F4: Coordinator skill: layout, rules and safety (subject 1)

**E1-F4-S1** [#755](https://github.com/IronbellyOrg/IronClaude/issues/755): Coordinator created multiple Orca Runs by default; find why, set a Run rule, compare one Run per project vs many
- Priority High; size M; complexity Medium; kind gap-closer; architecture change moderate
- Starts: start now
- Runs: lane E1-L8 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: #786
- Overlaps: #716 overlaps, link-only; #786 overlaps, merge-scope
- Open question (answered in the work, not waited on): One Orca Run per project or several; what happens to the three live Runs; run the switching test? Recommended: One Run per project. Close an extra Run only when every pending message in its inbox has been read and handled and no worker still reports into it (check the Run's live workers in Orca first; a Run with a running worker stays open until that worker finishes). Record in the pull request which Runs were closed and why (done-when item 5). A question once sat unseen 10 hours in run_71871571be85. Run the switching test with disposable workers in a throwaway project, as done-when item 4 asks

**E1-F4-S2** [#725](https://github.com/IronbellyOrg/IronClaude/issues/725): [FEATURE] Coordinators MUST ask the peer project's coordinator (read-only) before asking a human
- Priority Medium; size M; complexity Medium; kind enhancement; architecture change moderate
- Starts: start now
- Runs: lane E1-L9 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -

### E1-F5: Sweep, orchestrator and the cost of the coordinator loop (subject 3)

**E1-F5-S1** [#766](https://github.com/IronbellyOrg/IronClaude/issues/766): [BUG] Read workers show as Could not Determine
- Priority High; size M; complexity Medium; kind bug-fix; architecture change moderate
- Starts: start now
- Runs: lane E1-L10, in sequence: #766 then #590 then #534; in parallel with every other lane
- Needs first: -
- Unblocks: #757 #590(order)
- Overlaps: #534 overlaps, link-only (in this iteration); #590 overlaps, merge-scope (in this iteration)
- **Settle with** #590 (#590 has the same owner): Both fix the sweep's "could not determine" result for workers: the 50-read cap and unfollowed paging, and finished workers whose contract is not read.
- Open question (answered in the work, not waited on): Is turning every worker of a tail-only transcript into "could not determine" intended? Recommended: No: keep the evidence and add a note to the row

**E1-F5-S2** [#590](https://github.com/IronbellyOrg/IronClaude/issues/590): Sweep: first live run classified 1 of 264 sessions (show cap of 50, finished workers need an unread contract)
- Priority Medium; size M; complexity Medium; kind gap-closer; architecture change none
- Starts: after #766 (the story before it in its lane)
- Runs: lane E1-L10, in sequence: #766 then #590 then #534; in parallel with every other lane
- Needs first: #766(order)
- Unblocks: #339 #534
- Overlaps: #766 overlaps, merge-scope (in this iteration)
- **Settle with** #766 (#766 has the same owner): Both fix the sweep's "could not determine" result for workers: the 50-read cap and unfollowed paging, and finished workers whose contract is not read.
- Open question (answered in the work, not waited on): Page past the 50-session cap, or measure the cause split first? Change the "settled or asleep" wording, or read the contract? Recommended: Measure first; read the contract

**E1-F5-S3** [#534](https://github.com/IronbellyOrg/IronClaude/issues/534): Follow-ups from #339 Phase 1 (read-only sweep): open items, owner-ruled limitations and minor findings
- Priority Medium; size L; complexity Complex; kind chore; architecture change moderate
- Starts: after #590 (the story before it in its lane)
- Runs: lane E1-L10, in sequence: #766 then #590 then #534; in parallel with every other lane
- Needs first: #590
- Unblocks: #339
- Overlaps: #766 overlaps, link-only (in this iteration)
- Open question (answered in the work, not waited on): The sweep follow-ups need the owner to approve policy edits to WC-16, the output style and the design: which edits? Recommended: Measure first (decision 5); the issue owner (Ryan) chooses the policy edits to WC-16, the output style and the design and records them in the pull request; the pull request review is the normal merge review, nothing waits on it to start
- Note: an L umbrella whose card says to split it before scheduling: in this iteration take only the slice that follows #590 (the measured cause split and the policy edits it leads to)

**E1-F5-S4** [#767](https://github.com/IronbellyOrg/IronClaude/issues/767): Coordinator is compacting convrsation too often
- Priority Medium; size M; complexity Medium; kind bug-fix; architecture change moderate
- Starts: start now
- Runs: lane E1-L11 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -

**E1-F5-S5** [#468](https://github.com/IronbellyOrg/IronClaude/issues/468): orchestration check spam
- Priority Medium; size L; complexity Complex; kind bug-fix; architecture change moderate
- Starts: start now
- Runs: lane E1-L12 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -
- Open question (answered in the work, not waited on): Fix the "orchestration message" prompt spam here or where the prompt is produced? Recommended: Find the producer and record a baseline here first, then move the fix to the producer if it is Orca
- Note: only its first step is in this iteration: find the producer and record the baseline (Decision 36); the rest may move to Orca

### E1-F6: Workers: contract, launch guard, recovery and unattended running (subject 9)

**E1-F6-S1** [#442](https://github.com/IronbellyOrg/IronClaude/issues/442): [TEST GAP] Run the live observations OB-H1, OB-H2, OB-H3 and OB-CTX for the launch-level guard
- Priority High; size M; complexity Medium; kind test; architecture change none
- Starts: start now
- Runs: lane E1-L13 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -
- Open question (answered in the work, not waited on): Also run the OB-H1, OB-H2 and OB-CTX live observations, as OB-H3 already runs? Recommended: Yes, with the same coordinator and disposable test issues
- Note: the OB-H3 runs are already under way, by the coordinator that works under the ironbelly login (test issues #841 and #842, opened and claimed 10:44 to 10:48 AM; that this is Ryan's coordinator is inferred from the login); the other observation sets (OB-H1, OB-H2, OB-CTX) follow on the same disposable test issues; the ship gate needs four items to pass: OB-H1 item 1, OB-H1 item 5, OB-H2 and OB-H3 (`_GATE_ITEMS` in `tests/hooks/test_launch_level_observations.py`); record each observation's result next to its test (un-skip it, or give a checked reason) and deliver that change through the normal pull request; never change `GOVERNED_LEVELS_ALLOWED` in `src/superclaude/cli/issue_watch/launch.py` and never say on the issue that the gate is lifted: turning it on is a separate reviewed change the owner decides on once all four pass

### E1-F7: Watcher and coordinator chain: stage flow, gap list and docs (subject 6)

**E1-F7-S1** [#777](https://github.com/IronbellyOrg/IronClaude/issues/777): [FEATURE] Too many manual pieces to track per issue: map the whole watcher and coordinator chain and decide what to automate
- Priority High (GitHub: Medium); size S; complexity Simple; kind docs; architecture change none
- Starts: start now
- Runs: lane E1-L14 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: #761 overlaps, link-only; #773 overlaps, merge-scope
- Open question (answered in the work, not waited on): Who owns the map of manual steps per issue, and where does it live? Recommended: Ryan owns it, under docs/designs/

**E1-F7-S2** [#772](https://github.com/IronbellyOrg/IronClaude/issues/772): [FEATURE] Stage flow through the watcher: moving between Research, Spec, Plan and Debug, what Pipeline Full means, and a build step
- Priority High (GitHub: Medium); size M; complexity Medium; kind bug-fix; architecture change moderate
- Starts: start now
- Runs: lane E1-L15, in sequence: #772 then #774; in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: #761 overlaps, link-only; #774 overlaps, merge-scope (in this iteration)
- **Settle with** #774 (#774 has the same owner): The wording of what Pipeline Full means (and the "one local commit" line) across `commands/issue.md`, `refs/claim.md`, `launch-prompt.md`, `docs/designs/issue-watcher-status-pipelines.md` and the test at `tests/skills/test_issue_protocol.py`; also `WORKER-CONTRACT.md` and the status-pipelines design are edited by both.
- Open question (answered in the work, not waited on): The four stage-flow questions (a) to (d) for the watcher? Recommended: The issue owner decides at the start of the work

**E1-F7-S3** [#774](https://github.com/IronbellyOrg/IronClaude/issues/774): [FEATURE] Docs refresh for the issue watcher and coordinator: stale statements and one contradiction in the worker contract
- Priority Low (GitHub: Medium); size M; complexity Medium; kind docs; architecture change none
- Starts: after #772 (the story before it in its lane)
- Runs: lane E1-L15, in sequence: #772 then #774; in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: #717 overlaps, link-only; #761 overlaps, link-only; #772 overlaps, merge-scope (in this iteration); #793 overlaps, link-only; #823 overlaps, link-only
- **Settle with** #772 (#772 has the same owner): The wording of what Pipeline Full means (and the "one local commit" line) across `commands/issue.md`, `refs/claim.md`, `launch-prompt.md`, `docs/designs/issue-watcher-status-pipelines.md` and the test at `tests/skills/test_issue_protocol.py`; also `WORKER-CONTRACT.md` and the status-pipelines design are edited by both.
- Open question (answered in the work, not waited on): May the coordinator restart a dead worker by itself (at most once an hour); which backlog-record choice? Recommended: Yes, on Orca's proof that the worker exited; the issue owner picks the backlog record

### E1-F8: Troubleshoot, Jev preflight, research tools and confidence check (subject 15)

**E1-F8-S1** [#597](https://github.com/IronbellyOrg/IronClaude/issues/597): [BUG] Research routing bypasses available Context7 and Tavily MCP tools
- Priority Medium (GitHub: unset); size S; complexity Simple; kind bug-fix; architecture change moderate
- Starts: start now
- Runs: lane E1-L16 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -

### E1-F9: Follow-ups on shipped commands, releases and installers (subject 16)

**E1-F9-S1** [#703](https://github.com/IronbellyOrg/IronClaude/issues/703): Follow-ups from the issue 624 review: five small items in surgical remediation
- Priority Low (GitHub: Medium); size S; complexity Simple; kind chore; architecture change none
- Starts: start now
- Runs: lane E1-L17 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -

### E1-F10: Observer dashboard and contact agents (subject 7)

**E1-F10-S1** [#706](https://github.com/IronbellyOrg/IronClaude/issues/706): [FEATURE] Observer follow-up: session summaries, links, named steps, open session, sweep source and scale tests (sub-issue of #409)
- Priority Medium; size L; complexity Complex; kind enhancement; architecture change moderate
- Starts: start now
- Runs: lane E1-L18, in sequence: #706 then #409; in parallel with every other lane; this lane crosses owners, so the second owner starts when the first story is merged
- Needs first: -
- Unblocks: #409
- Overlaps: #409 overlaps, merge-scope (in this iteration); #727 overlaps, link-only
- **Settle with** #409 (#409 is owned by Clay: settle together): The five acceptance criteria added to #409 on 2026-11-13 (same sweep facts, plain-English summary, named steps with colours, open a session, scale tests) are written in both issues.
- Open question (answered in the work, not waited on): The observer gets its facts from the sweep JSON or its own collection? Session opening or disclosure (items 4 or 5)? Recommendation text and watcher state shown read-only (item 7)? Recommended: Sweep JSON (one collection); the issue owner decides items 4, 5 and 7 at the start of the work, together with Clay, who owns #409 (the same five acceptance criteria); if Clay has not answered when the work starts, Ryan decides, records it in the pull request, and #409 follows it

## E2: Clay

**Goal:** Claiming, releasing and session tooling work reliably on integration, and the team's rules for worktrees, branches and changes are written down

### E2-F1: Claim pipeline, worktrees, git workflows and team rules (subject 10)

**E2-F1-S1** [#289](https://github.com/IronbellyOrg/IronClaude/issues/289): docs(how-we-work): decide the worktree and branch protocol for parallel sessions
- Priority Medium; size M; complexity Medium; kind docs; architecture change none
- Starts: start now
- Runs: lane E2-L1 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: #687 overlaps, link-only
- Open question (answered in the work, not waited on): Exact branch and worktree name format; keep lesson extraction before cleanup? Recommended: The issue owner (Clay) sets the pattern within the limits in the issue (under 25 characters, no spaces, short description); keep lesson extraction

**E2-F1-S2** [#290](https://github.com/IronbellyOrg/IronClaude/issues/290): docs(how-we-work): decide how team members propose and change skills, commands and agents
- Priority Medium; size M; complexity Medium; kind docs; architecture change none
- Starts: start now
- Runs: lane E2-L2 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -

**E2-F1-S3** [#379](https://github.com/IronbellyOrg/IronClaude/issues/379): sc:issue --claim can assign a wrong-repository ClickUp task via #N fallback
- Priority Medium (GitHub: High); size M; complexity Medium; kind bug-fix; architecture change moderate
- Starts: start now
- Runs: lane E2-L3 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -

**E2-F1-S4** [#834](https://github.com/IronbellyOrg/IronClaude/issues/834): [FEATURE] /sc:issue --create asks the user a question only when the draft contradicts what the user said
- Priority Medium (GitHub: unset); size M; complexity Medium; kind enhancement; architecture change none
- Starts: start now
- Runs: lane E2-L4 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -
- Note: its Fix approach says base branch master, but the default branch is integration: branch from integration; pull request 849 (clayphi/issue-834, opened 25 Nov) already carries this work: continue on it (step 1, open pull request check) instead of starting a second one

**E2-F1-S5** [#326](https://github.com/IronbellyOrg/IronClaude/issues/326): [Feature]: Embed more Git and PM related workflows into skills
- Priority Medium; size L; complexity Complex; kind enhancement; architecture change moderate
- Starts: start now
- Runs: lane E2-L5 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: #687 overlaps, link-only
- Open question (answered in the work, not waited on): Confirm the narrowed scope of 2 Nov; is branch deletion wanted? Recommended: Confirm the 2 Nov scope; reuse the local branch cleanup that pull request 711 already delivered (do not rebuild it); no remote branch deletion
- Note: assigned on GitHub to ironbelly as well as clayphi: before the claim, Ryan removes himself or Clay removes him (step 1, assignee check)

### E2-F2: Follow-ups on shipped commands, releases and installers (subject 16)

**E2-F2-S1** [#393](https://github.com/IronbellyOrg/IronClaude/issues/393): sc:implement retry ladder now picks advisers it cannot start (from PR #385)
- Priority Medium; size S; complexity Medium; kind bug-fix; architecture change none
- Starts: start now
- Runs: lane E2-L6 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -

**E2-F2-S2** [#676](https://github.com/IronbellyOrg/IronClaude/issues/676): Core, agent and template installers overwrite edited files with no backup under --force and update
- Priority Medium; size S; complexity Medium; kind decision; architecture change none
- Starts: start now
- Runs: lane E2-L7 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -
- Open question (answered in the work, not waited on): Should the core, agent and template installers back up edited files like the other installers? Recommended: Yes, same .bak behaviour as install_commands.py and install_user_setup.py

**E2-F2-S3** [#826](https://github.com/IronbellyOrg/IronClaude/issues/826): [FEATURE] Define the release path from integration to master and update release tooling
- Priority Medium; size M; complexity Medium; kind gap-closer; architecture change moderate
- Starts: start now
- Runs: lane E2-L8 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -

**E2-F2-S4** [#599](https://github.com/IronbellyOrg/IronClaude/issues/599): [FEATURE] Refactor sc:reflect to remove task-builder and task with --remediate --depth deep
- Priority Low (GitHub: Medium); size S; complexity Medium; kind decision; architecture change none
- Starts: start now
- Runs: lane E2-L9 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: #647 overlaps, link-only
- Open question (answered in the work, not waited on): Pass depth through to the planner (the 17 Nov answer) or keep review-only (what shipped in pull request 653)? Recommended: The issue owner (Clay) decides at the start of the work; keep review-only until then

**E2-F2-S5** [#571](https://github.com/IronbellyOrg/IronClaude/issues/571): Release 6.0.0: remove headless CLI families, swarm and retired commands from IronClaude (plan for review)
- Priority Low; size S; complexity Complex; kind chore; architecture change none
- Starts: start now
- Runs: lane E2-L10 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -
- Open question (answered in the work, not waited on): Close the 6.0.0 umbrella and file its three leftovers as their own issues? Recommended: Yes

### E2-F3: Repository protection, CI and tool health (subject 11)

**E2-F3-S1** [#517](https://github.com/IronbellyOrg/IronClaude/issues/517): [BUG] ccsession proxy: a tier whose first model always thinks fails every request with the default effort medium and never falls through to the next model
- Priority Medium; size S; complexity Medium; kind bug-fix; architecture change none
- Starts: start now
- Runs: lane E2-L11 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -
- Note: assigned on GitHub to ironbelly, but ccsession work is Clay's (Clay's rule wins over the assignee); before the claim, Ryan removes himself or Clay removes him (step 1, assignee check)

**E2-F3-S2** [#837](https://github.com/IronbellyOrg/IronClaude/issues/837): [ruleset] Apply the branch protection rulesets to the other public IronbellyOrg repos (702 follow-up)
- Priority Medium (GitHub: unset); size S; complexity not set on GitHub (counted as Medium in the order); kind gap-closer; architecture change none
- Starts: start now
- Runs: lane E2-L12 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -
- Open question (answered in the work, not waited on): Which repos get the rulesets? Recommended: The six repos listed in the issue are the candidates; each one gets the rulesets only after the issue owner's go for that repo and its own 90-day check of direct pushes; Ryan applies the three only his login can change
- Note: first step: the issue owner (Clay) gives the go per repo, as its pick-up note asks; needs admin on each repo: Clay has it on three, Ryan applies the three only his login can change (IronHands-CLI, ironops-marketplace, irondots); run the 90-day check of direct pushes per repo first

**E2-F3-S3** [#838](https://github.com/IronbellyOrg/IronClaude/issues/838): [ruleset] Apply the branch protection rulesets to the IronbellyGroup repos (702 follow-up)
- Priority Medium (GitHub: unset); size S; complexity not set on GitHub (counted as Medium in the order); kind gap-closer; architecture change none
- Starts: start now
- Runs: lane E2-L13 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -
- Note: Clay has admin on all 18 repos; the repo names are in the author's local notes and go to the admin on request; this part needs Clay's answer at the start: the list of repos, which is the go for each of them

**E2-F3-S4** [#352](https://github.com/IronbellyOrg/IronClaude/issues/352): Flaky ccsession shim tests in tests/unit/test_ccsession_tiers.py under load
- Priority Medium; size M; complexity Medium; kind test; architecture change none
- Starts: start now
- Runs: lane E2-L14 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -

### E2-F4: Sweep, orchestrator and the cost of the coordinator loop (subject 3)

**E2-F4-S1** [#765](https://github.com/IronbellyOrg/IronClaude/issues/765): [FEATURE] Stop Claude Code from killing the coordinator's message watch under low memory, and research what to stop instead
- Priority High; size L; complexity Complex; kind gap-closer; architecture change moderate
- Starts: start now
- Runs: lane E2-L15 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -
- Note: the work moved to the Coder repository (Clay's decision on the issue, 25 Nov 2:55 PM Central): one line, export CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1, in the Coder template's aienv.d/defaults.sh; tracked as IronbellyOrg/Coder issue 536; pull request 847 (the ccsession change) is superseded

### E2-F5: Troubleshoot, Jev preflight, research tools and confidence check (subject 15)

**E2-F5-S1** [#610](https://github.com/IronbellyOrg/IronClaude/issues/610): Jev preflight step 1: add missing performance phrases to the troubleshoot keyword table (sub-issue of #609)
- Priority Medium; size XS; complexity Simple; kind gap-closer; architecture change none
- Starts: start now
- Runs: lane E2-L16, in sequence: #610 then #611; in parallel with every other lane
- Needs first: -
- Unblocks: #609 #611
- Overlaps: #609 overlaps, link-only

**E2-F5-S2** [#611](https://github.com/IronbellyOrg/IronClaude/issues/611): Jev preflight step 2: compare Jev against the keyword table on about 30 labelled prompts (sub-issue of #609)
- Priority Low (GitHub: Medium); size M; complexity Medium; kind test; architecture change none
- Starts: after #610 (the story before it in its lane)
- Runs: lane E2-L16, in sequence: #610 then #611; in parallel with every other lane
- Needs first: #610
- Unblocks: #609 #612
- Overlaps: #609 overlaps, link-only
- Open question (answered in the work, not waited on): Send about 30 public prompts to TypeSafe on the TYPESAFE_API_KEY key with a spend cap; what margin must Jev win by; what median latency is acceptable? Recommended: Yes, 1 dollar cap, public prompts only; the issue owner (Clay) sets margin and latency before the run

### E2-F6: Session startup cost, output style and Orca app issues (subject 17)

**E2-F6-S1** [#758](https://github.com/IronbellyOrg/IronClaude/issues/758): [FEATURE] Assume the user is coming in blind when asking a decision or question
- Priority Medium; size S; complexity Simple; kind enhancement; architecture change none
- Starts: start now
- Runs: lane E2-L17 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -

**E2-F6-S2** [#780](https://github.com/IronbellyOrg/IronClaude/issues/780): [BUG] Orca registers this repository under the upstream project id
- Priority Medium; size M; complexity Medium; kind bug-fix; architecture change none
- Starts: start now
- Runs: lane E2-L18 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -
- Open question (answered in the work, not waited on): Change Orca so origin wins, or override the stored upstream once? Recommended: Try the one-time override first; if it does not hold, change Orca

**E2-F6-S3** [#779](https://github.com/IronbellyOrg/IronClaude/issues/779): [BUG] Orca-ide uses CPU while idle: troubleshoot the 60 frames per second software compositing loop
- Priority Medium; size M; complexity Complex; kind bug-fix; architecture change none
- Starts: start now
- Runs: lane E2-L19 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -
- Open question (answered in the work, not waited on): Track Orca's idle CPU here or with the image maintainer? Recommended: Track it here for the read-only measuring; ask the image maintainer for the fix
- Note: only the read-only measuring and tracing steps (Decision 26); the restart steps stay on Clay's hold

### E2-F7: Observer dashboard and contact agents (subject 7)

**E2-F7-S1** [#409](https://github.com/IronbellyOrg/IronClaude/issues/409): [FEATURE] TUI Dashboard to Manage Orchestration at Scale
- Priority Medium; size XS; complexity Complex; kind enhancement; architecture change none
- Starts: after #706 (the story before it in its lane)
- Runs: lane E1-L18, in sequence: #706 then #409; in parallel with every other lane; this lane crosses owners, so the second owner starts when the first story is merged
- Needs first: #706
- Unblocks: -
- Overlaps: #706 overlaps, merge-scope (in this iteration)
- **Settle with** #706 (#706 is owned by Ryan: settle together): The five acceptance criteria added to #409 on 2026-11-13 (same sweep facts, plain-English summary, named steps with colours, open a session, scale tests) are written in both issues.
- Open question (answered in the work, not waited on): Replace the umbrella status that is out of date? Recommended: Yes; close it when #706 is done

## E3: Leandro

**Goal:** Workers can run unattended within safe limits, and the repo's tests and CI can be trusted

### E3-F1: Workers: contract, launch guard, recovery and unattended running (subject 9)

**E3-F1-S1** [#733](https://github.com/IronbellyOrg/IronClaude/issues/733): [FEATURE] Unattended mode for /sc:implement
- Priority High; size L; complexity Complex; kind enhancement; architecture change moderate
- Starts: start now
- Runs: lane E3-L1 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: #731
- Overlaps: -

**E3-F1-S2** [#446](https://github.com/IronbellyOrg/IronClaude/issues/446): WC-9: retry index.lock for about 10 s before a worker reports blocked
- Priority Medium; size S; complexity Simple; kind gap-closer; architecture change moderate
- Starts: start now
- Runs: lane E3-L2 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -

**E3-F1-S3** [#699](https://github.com/IronbellyOrg/IronClaude/issues/699): The claim script creates the issue worktree without an agent, against the every-worktree-gets-an-agent rule
- Priority Medium; size S; complexity Simple; kind decision; architecture change none
- Starts: start now
- Runs: lane E3-L3 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -
- Open question (answered in the work, not waited on): Keep the claim script's agent-less worktree as a written exception? Recommended: Yes

**E3-F1-S4** [#825](https://github.com/IronbellyOrg/IronClaude/issues/825): [BUG] L1 launch-level guard does not protect integration (the new default branch)
- Priority Medium; size S; complexity Simple; kind gap-closer; architecture change none
- Starts: start now
- Runs: lane E3-L4 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -

**E3-F1-S5** [#465](https://github.com/IronbellyOrg/IronClaude/issues/465): [BUG] Verifier report delivery failure leaves implementation blocked without bounded recovery
- Priority Medium; size L; complexity Complex; kind bug-fix; architecture change moderate
- Starts: start now
- Runs: lane E3-L5 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -
- Open question (answered in the work, not waited on): Keep rf-qa-qualitative? Recommended: Keep it (Clay's recommendation of 18 Nov); fix its report-writing wording

### E3-F2: Repository protection, CI and tool health (subject 11)

**E3-F2-S1** [#618](https://github.com/IronbellyOrg/IronClaude/issues/618): Make IronClaude's ruff version follow the Coder image pin instead of its own
- Priority High; size M; complexity Medium; kind bug-fix; architecture change moderate
- Starts: start now
- Runs: lane E3-L6 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -

**E3-F2-S2** [#702](https://github.com/IronbellyOrg/IronClaude/issues/702): [FEATURE] Protect the default branch of IronClaude: no direct push, no force push
- Priority Medium; size S; complexity Complex; kind enhancement; architecture change moderate
- Starts: start now
- Runs: lane E3-L7 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: #722(conditional)
- Overlaps: -
- Note: direct pushes are refused (checked 25 Nov); still open: the 7-day zero-direct-commit window to Wed 2 Dec, the first real release through the rules, and an update rule for the release-tag ruleset (ironbelly comment, 10:49 AM); pull request 844 (ironbelly/702-tag-update-rule) already carries the release-tag update rule: continue on it or wait for it (step 1, open pull request check)

**E3-F2-S3** [#333](https://github.com/IronbellyOrg/IronClaude/issues/333): sc-crash-recovery bootstrap_scan.sh exits non-zero and prints no JSON
- Priority Medium; size XS; complexity Simple; kind bug-fix; architecture change none
- Starts: start now
- Runs: lane E3-L8 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -

**E3-F2-S4** [#313](https://github.com/IronbellyOrg/IronClaude/issues/313): Tests must not depend on old logs and planning documents under .dev/
- Priority Medium; size M; complexity Medium; kind test; architecture change none
- Starts: start now
- Runs: lane E3-L9 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -

### E3-F3: Review panel unification and grading (subject 12)

**E3-F3-S1** [#603](https://github.com/IronbellyOrg/IronClaude/issues/603): [FEATURE] Incorporate spec-panel to Add a review, QA and enrichment phase at the end of sc:design
- Priority Medium; size M; complexity Simple; kind enhancement; architecture change moderate
- Starts: start now
- Runs: lane E3-L10 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -
- Open question (answered in the work, not waited on): Spec-panel in sc:design: the original integration only, or the later panel improvements too? Chat-only output, and where review inputs are kept? Recommended: Original integration only; the issue owner (Leandro) settles the output and persistence points at the start of the work and records them in the pull request

**E3-F3-S2** [#376](https://github.com/IronbellyOrg/IronClaude/issues/376): sc:adversarial scoring mixes 25- and 30-criterion rubrics and omits the invariant eligibility report
- Priority Medium; size M; complexity Medium; kind bug-fix; architecture change none
- Starts: start now
- Runs: lane E3-L11 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -

**E3-F3-S3** [#552](https://github.com/IronbellyOrg/IronClaude/issues/552): [FEATURE] Issues being classified as blockers too egregiously
- Priority Medium; size M; complexity Medium; kind enhancement; architecture change moderate
- Starts: start now
- Runs: lane E3-L12 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: #602 overlaps, merge-scope
- Open question (answered in the work, not waited on): Go for stage four on an updated plan (the old plan names skills that pull request 650 removed)? Accept the recorded cuts (no classifier, registry or seeded recall), or reopen them as separate work? Recommended: The issue owner (Leandro) rewrites the plan for the current skills and decides on the cuts at the start of the work

## E4: swill-ib

**Goal:** Swarm runs always leave a reliable completion marker and their results, on integration

### E4-F1: Eval framework and swarm tooling (subject 14)

**E4-F1-S1** [#540](https://github.com/IronbellyOrg/IronClaude/issues/540): [BUG] Successful foreground swarm run does not write done.json completion marker
- Priority High; size S; complexity Medium; kind bug-fix; architecture change none
- Starts: start now: confirm and close (the fix, pull request 762, is on integration since 11:42 AM Central on 25 Nov through pull request 846)
- Runs: lane E4-L1 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -
- Note: do not write a second patch; check the issue's done-when on integration, then close it; the done.json-on-resume finding from pull request 846 is a separate follow-up

**E4-F1-S2** [#555](https://github.com/IronbellyOrg/IronClaude/issues/555): [BUG] Detached swarm child drops output delivery and leaves no durable results
- Priority High; size S; complexity Medium; kind bug-fix; architecture change none
- Starts: start now: confirm and close (the fix, pull request 762, is on integration since 11:42 AM Central on 25 Nov through pull request 846)
- Runs: lane E4-L2 on its own; can run in parallel with every other lane
- Needs first: -
- Unblocks: -
- Overlaps: -
- Note: do not write a second patch; check the issue's done-when on integration, then close it

