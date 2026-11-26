# Iteration 3 work file: Ryan, epic E1

Generated Wed 25 Nov 2026 20:14 Central by `scripts/epic-files.sh` from the reviewed work map (`work-map.json`). Do not edit by hand: change the map's inputs and rebuild. Repository: `IronbellyOrg/IronClaude`, base branch `integration`. Iteration 3 ends Sunday 6 December.

## 1. Kickoff prompt

This file and the story files live in IronClaude at `.dev/iterations/iteration-3/`, on `integration`. Ryan starts the epic by opening a new Claude session in an IronClaude checkout of `integration` (after `git pull`) and pasting this:

```text
You lead epic E1 for Ryan in IronbellyOrg/IronClaude, iteration 3. Read .dev/iterations/iteration-3/epics/E1-ryan.md from top to bottom, then run it exactly as its section 4 says. Keep your progress in .dev/iterations/iteration-3/progress/E1.md, one line per story. Never merge a pull request. Ask Ryan only where this file says the owner decides.
```

## 2. What Ryan approves by starting this file

- Claiming each issue below on GitHub, one Orca worktree and one agent per story, in the order and lanes of section 5.
- For each story: committing on its own feature branch from `integration`, pushing that branch to `origin` (or, with the owner's go in step 1, the branch of the open pull request the story continues), and opening or attaching its pull request with `/sc:pr-submit --monitor 3`, which also pushes the fixes it makes for review findings and failing checks.
- For a story whose route says so: a comment with its evidence on its issue, closing that issue, filing the new issues the route names, and the writes the story's route or decisions name on other repositories (for example rulesets), each only after the checks they give.
- Not approved: merging (the owner merges, and never with a failing check), pushing to `integration` or `master`, closing an issue outside the story workflow, and any change outside the story's issue.

## 3. Epic goal

The watcher and the coordinator carry an approved issue to a merged pull request without a person passing it along, and their docs match what they do.

## 4. How to run this epic (for the lead session)

1. Check that the files are on `integration`: `git ls-tree origin/integration .dev/iterations/iteration-3/stories/` must list the story files. If it lists nothing, stop and tell Ryan: the pull request that adds this folder has not merged yet, and every story agent starts in a worktree made from `origin/integration`.
2. Read this whole file before starting anything.
3. Look at section 5. Every lane whose first story says **Start when: now** can start at once: start one agent for each, in parallel, except that only one shared-file story (section 5) runs at a time.
4. Before you start any story, run its **Start when** check and its **Shared files** check. Start it only when both pass. A story that fails a check waits; check again whenever a pull request merges.
5. To start a story, follow the story workflow in section 7, steps 1 and 2: you make its worktree and start its agent with its story file. The agent runs steps 3 to 10 itself.
6. How you and an agent talk: the agent writes `.dev/issues/<issue>/result.md` in its worktree and says in its terminal what it did and what is left, or that it is waiting (for a plan approval or an answer). Read its terminal and that file with the `orca-cli` skill. To give it an answer or the owner's go, type into its terminal with the `orca-cli` skill.
7. When a story's pull request has every check green and every review comment handled, tell Ryan it is ready to merge. After the merge, run step 12 (closeout), then start the next story in that lane.
8. A story marked **Plan approval: yes** stops after its plan. Show Ryan the plan path; type the owner's go into the agent's terminal only after the owner says go.
9. Where a story's decisions or scope say a part needs Ryan's answer at the start, ask Ryan when that story starts and type the answer into the agent's terminal; the agent writes it into the story's decisions (section 7, step 4) and its pull request. Nothing else waits on anyone.
10. Section 6 lists what this epic needs from other people and what they need from it. Check it before each start.
11. Write one line per story to your progress file whenever its state changes: waiting, started, plan ready, pull request open, merged, closed.

## 5. Lanes: what runs at the same time, and what runs in sequence

Stories in the same lane run one after another, in the order shown. Different lanes run at the same time, one agent each. The stories a lane row names as shared-file stories edit `WORKER-CONTRACT.md`: of those, only one is started and not yet merged at any time in this epic (each one's **Shared files** line gives the check); the other stories of such a lane are not held by it.

| Lane | Stories, in order (owner) | First story starts | Runs with |
|---|---|---|---|
| E1-L1 | #818 (Ryan) then #753 (Ryan) | now | every other lane at the same time |
| E1-L2 | #816 (Ryan) | now | every other lane at the same time |
| E1-L3 | #819 (Ryan) | now | every other lane at the same time |
| E1-L4 | #822 (Ryan) | now | every other lane at the same time |
| E1-L5 | #698 (Ryan) | now | every other lane at the same time |
| E1-L6 | #790 (Ryan) then #792 (Ryan) | now | every other lane at the same time; shared-file stories: #790 (one at a time) |
| E1-L7 | #771 (Ryan) | now | every other lane at the same time; shared-file stories: #771 (one at a time) |
| E1-L8 | #755 (Ryan) | now | every other lane at the same time; shared-file stories: #755 (one at a time) |
| E1-L9 | #725 (Ryan) | now | every other lane at the same time; shared-file stories: #725 (one at a time) |
| E1-L10 | #766 (Ryan) then #590 (Ryan) then #534 (Ryan) | now | every other lane at the same time |
| E1-L11 | #767 (Ryan) | now | every other lane at the same time |
| E1-L12 | #468 (Ryan) | now | every other lane at the same time |
| E1-L13 | #442 (Ryan) | now | every other lane at the same time |
| E1-L14 | #777 (Ryan) | now | every other lane at the same time |
| E1-L15 | #772 (Ryan) then #774 (Ryan) | now | every other lane at the same time; shared-file stories: #772, #774 (one at a time) |
| E1-L16 | #597 (Ryan) | now | every other lane at the same time |
| E1-L17 | #703 (Ryan) | now | every other lane at the same time |
| E1-L18 | #706 (Ryan) then #409 (Clay) | now | crosses owners: the second owner starts when the first story is closed |

## 6. Between people

- #837 (Clay) needs Ryan for the three repos only his login can change: IronHands-CLI, ironops-marketplace, irondots.
- #409 (Clay) needs #706 (Ryan), and both carry the same five acceptance criteria: Ryan builds #706 and settles those criteria with Clay at its start; Clay then finishes #409.
- #442 (Ryan) observes the launch-level guard that #825 (Leandro) changes: agree which guard version the observations run against before either starts (card 825; not verified in #442's steps).
- `WORKER-CONTRACT.md` is edited by #790, #771, #774, #755, #725 and #772 (Ryan) and by #446 and #699 (Leandro): each of those stories starts only when no open pull request changes that file and no other of them is already claimed in this iteration, in either epic (its **Shared files** line gives both checks).

## 7. The story workflow (every story, every step, in this order)

This is the workflow of the team's routing guide (`src/superclaude/core/HOW-WE-WORK.md`, sections 1, 3.2 to 3.4 and 3.11) and of the claim skill (`src/superclaude/skills/sc-issue-protocol/`). A story whose route starts with **Route (replaces steps 5 to 10)** has no code change: that paragraph replaces steps 5 to 10. Its agent may comment on and close its own issue as the route says; this is an exception to the claim launch prompt's rule that only the coordinator writes to an issue, and section 2 approves it.

Why the claim runs with `--pipeline none` for now: the claim skill forbids a launched claim (`--pipeline worktree` or `full`) on a real issue while its ship gate is closed (the rule in its `refs/claim.md`, Wave 8), and the issue watcher's matching gate is the constant `GOVERNED_LEVELS_ALLOWED = False` in `src/superclaude/cli/issue_watch/launch.py`. Both open only by a reviewed change, after four live observations of #442 have passed (OB-H1 item 1, OB-H1 item 5, OB-H2 and OB-H3, the gate items of `tests/hooks/test_launch_level_observations.py`). The claim also cannot yet carry this file's decisions into a launched agent. Until both are solved, the agent runs the claim and its next steps in its own session, which the claim skill allows for `--pipeline none`.

1. **Start check (lead).** Run the story's **Start when** command for each issue it names: each must print `CLOSED`. (Each of these is also a GitHub "blocked by" link, and since #848 the claim itself stops with `E-BLOCKED` while one is open, once your installed IronClaude has that change; this check stays the first line.) Run the story's **Shared files** command when it has one: it must print `[]`. If a check fails, the story waits. Then two more checks, for every story:
   - **Assignee.** `gh issue view <issue> --repo IronbellyOrg/IronClaude --json assignees --jq '[.assignees[].login]'` must list only your own login (`gh api user --jq .login`) or nothing. If it lists anyone else, the claim in step 3 would stop: ask the owner to have that person removed (they remove themselves, or the owner runs `gh issue edit <issue> --repo IronbellyOrg/IronClaude --remove-assignee <login>`), then start.
   - **Work already under way.** `orca-ide worktree list --json` (with the `orca-cli` skill) must show no worktree named `issue-<issue>`; if one exists, ask the owner before starting.
   - **Open pull request.** `gh pr list --repo IronbellyOrg/IronClaude --state open --limit 200 --json number,title,body --jq '[.[] | select((.title + " " + .body) | test("(^|[^0-9])#?<issue>([^0-9]|$)")) | .number]'` must print `[]`. If it prints a number, that pull request already carries work on this issue: tell the owner, and do not start a second one. With the owner's go, the story continues on that pull request: make the worktree as in step 2 and type the pull request number into the agent's terminal; the agent checks out its branch (step 3), does only what it leaves undone (step 5), pushes to it (step 9) and attaches with `--pr` (step 10).
2. **Worktree and agent (lead).** With the `orca-cli` skill, create an Orca worktree for the issue from `origin/integration` and start a Claude agent in it, on the model tier its story file's **Expected route** names, with this prompt: `Follow .dev/iterations/iteration-3/stories/<issue>.md from top to bottom.`
3. **Claim (agent).** If your Scope line names an open pull request that you continue, first run `gh pr checkout <number> --repo IronbellyOrg/IronClaude` in this worktree, so you work on that pull request's branch. Then `/sc:issue --claim <issue> --pipeline none`. It assigns the issue, checks the issue text against today's code, and writes `.dev/issues/<issue>/issue-summary.md` and `.dev/issues/<issue>/next-steps.md`.
4. **Decisions (agent).** Append the story's **Decided for this work** block, word for word, to the end of `.dev/issues/<issue>/issue-summary.md` under the heading `## Decided for this work (iteration 3)`, with any answer the lead typed in for it. Every later step reads that file, so the decisions reach the plan. Do this before step 5.
5. **Next steps (agent).** If you continue an open pull request, first read its diff against the issue (`gh pr diff <number> --repo IronbellyOrg/IronClaude`) and do only what it leaves undone. Open `next-steps.md`. Its first line names the model tier it was written for; if this session runs on a lower tier, say so and carry on. Run each step through the Skill tool, in order, in this session, up to and including the planning step; never run a step inside a subagent. `/sc:implement` is step 7: never run it from `next-steps.md` before step 6 is done. The story's **Expected route** says what the steps should look like; if `next-steps.md` differs, follow `next-steps.md` and note the difference in your report. For a bug: if the diagnosis report is inconclusive, failed or blocked, do not plan or apply a fix; stop and report it.
6. **Plan (agent).** For a simple bug there is no plan: the diagnosis report goes straight to step 7. Otherwise the planning step (`/sc:workflow`) prints a plan path, `.dev/tasks/to-do/<id>/<id>.md`, and an advisory check result. Read both. Fix every gap the check names before implementing. If the story says **Plan approval: yes**, stop here: say in the terminal that the plan at that path waits for approval, and wait for the owner's go.
7. **Implement (agent).** `/sc:implement <plan path>`. It implements each step, checks it against the plan's acceptance criteria and ends with an independent final review. If it stops with `E-RESUME-NEEDED`, run the same command again. If it stops with `E-HALT-QA` (a step still fails after its retries), stop and report the step and the progress file path: the owner either has the code fixed and the same command run again, or accepts the explained gap in this session, which `/sc:implement` records itself.
8. **Confirm (agent).** Read `progress.md` beside the plan and the final review. Every step must pass. Run the related tests yourself if nothing ran them.
9. **Commit and push (agent).** If you continue an open pull request: skip the next check, commit on its branch and push to that branch. Otherwise first check that no pull request exists for this branch: `gh pr list --repo IronbellyOrg/IronClaude --head <branch> --state all` must print nothing; if one exists, stop and report it. Commit on a feature branch made from `integration`, with a conventional-commit message (`type(scope): message`). Stage the changed files and `.dev/tasks`; never anything under `.claude/` or `.dev/issues/`. Push the feature branch to `origin`; never push `integration` or `master`.
10. **Pull request (agent).** If you continue an open pull request: `/sc:pr-submit --monitor 3 --pr <number>`. Otherwise `/sc:pr-submit --monitor 3 --head <branch> --base integration --title "<title>" --body "<body>"`. The body carries the story's **Decided for this work** block. Write `Fixes #<issue>` only when the pull request delivers the whole issue; otherwise `Refs #<issue>` and say what is left. Stay with it until every check is green and every review comment is handled, then report.
11. **Merge (owner).** The owner merges. Never merge with a failing check.
12. **Closeout (lead).** `/sc:closeout <pull request>`. It checks that the pull request merged and settles the issue, the work report entry and the Orca task.
13. **Next (lead).** Start the next story in this lane (section 5), from step 1.

## 8. Stories in order of completion

### 1. E1-F1-S1 [#818](https://github.com/IronbellyOrg/IronClaude/issues/818): [FEATURE] Issue watcher W10: Permissions of launched sessions (FU-6)

- **Issue:** [#818](https://github.com/IronbellyOrg/IronClaude/issues/818) [FEATURE] Issue watcher W10: Permissions of launched sessions (FU-6)
- **Feature:** E1-F1 Issue watcher: next-release items
- **Priority:** Medium; **complexity:** Simple; **kind:** gap-closer; **size:** S
- **Lane:** E1-L1, story 1 of 2 (#818 then #753)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): the next story in this lane is #753.
- **Decided for this work:**
  - **Question:** Refuse or only warn about approvers beyond the first until the watcher can check each approver's own GitHub permission? Where is the permission level of each started session recorded? **Decided:** Only warn (the 23 Nov rule in #753 makes every maintainer and admin an approver); record it in the watcher's audit log, which its status check already reads.
  - **One scope with #753** (same owner, Ryan): settle it at the start of whichever of the two starts first. Shared ground: The size of the approver list, with opposite aims. #753 makes every maintainer and admin an approver automatically. #818 (W10) says to block or flag a second approver until per-actor permission checks of the launched session exist. Built as written, #753 adds approvers that #818 would refuse.
- **Expected route:** Feature, simple: plan with `/sc:workflow --depth quick --handoff none`, then `/sc:implement` the printed plan. Model line: `claude-gw-tier2`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/818.md`

### 2. E1-F1-S2 [#816](https://github.com/IronbellyOrg/IronClaude/issues/816): [FEATURE] Issue watcher W8: Alert after three bad cycles (FU-4)

- **Issue:** [#816](https://github.com/IronbellyOrg/IronClaude/issues/816) [FEATURE] Issue watcher W8: Alert after three bad cycles (FU-4)
- **Feature:** E1-F1 Issue watcher: next-release items
- **Priority:** Medium; **complexity:** Medium; **kind:** enhancement; **size:** M
- **Lane:** E1-L2, story 1 of 1 (#816)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Question:** Where does the alert after three bad watcher runs go; does the check cover skipped issues and the stop at 100? **Decided:** A ClickUp message (outside the workspace, so it works when the workspace is stopped); yes to both.
- **Expected route:** Feature, medium: `/sc:brainstorm --blind` on the summary, `/sc:design` from its merged requirements, `/sc:workflow --depth standard --handoff none` on the design, then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/816.md`

### 3. E1-F1-S3 [#819](https://github.com/IronbellyOrg/IronClaude/issues/819): [FEATURE] Issue watcher W11: One retry of an unknown launch outcome through Orca's operation id (FU-8, owner question Q2)

- **Issue:** [#819](https://github.com/IronbellyOrg/IronClaude/issues/819) [FEATURE] Issue watcher W11: One retry of an unknown launch outcome through Orca's operation id (FU-8, owner question Q2)
- **Feature:** E1-F1 Issue watcher: next-release items
- **Priority:** Medium (GitHub: Low); **complexity:** Medium; **kind:** gap-closer; **size:** M
- **Lane:** E1-L3, story 1 of 1 (#819)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Question:** Which retry form for an unknown watcher launch outcome? **Decided:** The issue owner decides at the start of the work. This part needs Ryan's answer at the start of the story: ask, then record the answer here and in the pull request.
- **Expected route:** Feature, medium: `/sc:brainstorm --blind` on the summary, `/sc:design` from its merged requirements, `/sc:workflow --depth standard --handoff none` on the design, then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/819.md`

### 4. E1-F1-S4 [#822](https://github.com/IronbellyOrg/IronClaude/issues/822): [FEATURE] Issue watcher W14: check-config refuses a state folder that is not on a local disk (FU-12)

- **Issue:** [#822](https://github.com/IronbellyOrg/IronClaude/issues/822) [FEATURE] Issue watcher W14: check-config refuses a state folder that is not on a local disk (FU-12)
- **Feature:** E1-F1 Issue watcher: next-release items
- **Priority:** Low; **complexity:** Simple; **kind:** gap-closer; **size:** S
- **Lane:** E1-L4, story 1 of 1 (#822)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - Nothing to decide: build what the issue asks for, within its own scope.
- **Expected route:** Feature, simple: plan with `/sc:workflow --depth quick --handoff none`, then `/sc:implement` the printed plan. Model line: `claude-gw-tier2`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/822.md`

### 5. E1-F2-S1 [#753](https://github.com/IronbellyOrg/IronClaude/issues/753): issue-watch: always accept maintainers and admins as approvers

- **Issue:** [#753](https://github.com/IronbellyOrg/IronClaude/issues/753) issue-watch: always accept maintainers and admins as approvers
- **Feature:** E1-F2 Approvals and the shared GitHub login
- **Priority:** High; **complexity:** Medium; **kind:** gap-closer; **size:** M
- **Lane:** E1-L1, story 2 of 2 (#818 then #753)
- **Start when:** #818 is closed (same lane: the two share one scope): `gh issue view 818 --repo IronbellyOrg/IronClaude --json state --jq .state` prints `CLOSED`.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **One scope with #818** (same owner, Ryan): settle it at the start of whichever of the two starts first. Shared ground: The size of the approver list, with opposite aims. #753 makes every maintainer and admin an approver automatically. #818 (W10) says to block or flag a second approver until per-actor permission checks of the launched session exist. Built as written, #753 adds approvers that #818 would refuse.
- **Expected route:** Feature, medium: `/sc:brainstorm --blind` on the summary, `/sc:design` from its merged requirements, `/sc:workflow --depth standard --handoff none` on the design, then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/753.md`

### 6. E1-F2-S2 [#698](https://github.com/IronbellyOrg/IronClaude/issues/698): Release-worker and plan-approval checks rest on text matching and an assignee shortcut

- **Issue:** [#698](https://github.com/IronbellyOrg/IronClaude/issues/698) Release-worker and plan-approval checks rest on text matching and an assignee shortcut
- **Feature:** E1-F2 Approvals and the shared GitHub login
- **Priority:** Medium; **complexity:** Complex; **kind:** decision; **size:** M
- **Lane:** E1-L5, story 1 of 1 (#698)
- **Start when:** now.
- **Plan approval:** yes: complex, so the owner approves the plan before `/sc:implement` runs.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane. It also unblocks #773 (a later iteration), #775 (conditional) (a later iteration).
- **Decided for this work:**
  - **Question:** Which protection for release-worker: (a) the guard also catches the Python and Click routes, (b) release-worker refuses without an approval record, (c) the approval store is not writable by the worker's account, or (d) record that the guard is only a seatbelt? And the approver rule in done-when item 2? **Decided:** The issue owner (Ryan) chooses the protection at the start of the work; the approver rule follows #753 (every maintainer and admin), and Ryan also decides whether the assignee shortcut stays (done-when item 2) and records both choices in issue-pipeline-fu1.md. This part needs Ryan's answer at the start of the story: ask, then record the answer here and in the pull request.
- **Expected route:** Feature, complex: `/sc:brainstorm --depth deep --research deep --codebase --blind`, `/sc:design` from its merged requirements, `/sc:workflow --depth deep --handoff none` on the design, then, after the owner approves the plan, `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/698.md`

### 7. E1-F3-S1 [#790](https://github.com/IronbellyOrg/IronClaude/issues/790): [FEATURE] Coordinator C9: Handoff prompt template: fixed nine-section order, Fixes or Refs rule, no secrets, hand-back round block, regression gate

- **Issue:** [#790](https://github.com/IronbellyOrg/IronClaude/issues/790) [FEATURE] Coordinator C9: Handoff prompt template: fixed nine-section order, Fixes or Refs rule, no secrets, hand-back round block, regression gate
- **Feature:** E1-F3 Coordinator workers: start, track and finish
- **Priority:** Medium; **complexity:** Medium; **kind:** enhancement; **size:** M
- **Lane:** E1-L6, story 1 of 2 (#790 then #792)
- **Start when:** now.
- **Shared files:** this story edits `src/superclaude/core/WORKER-CONTRACT.md`, as do #771 (Ryan), #755 (Ryan), #725 (Ryan), #772 (Ryan), #774 (Ryan), #446 (Leandro), #699 (Leandro). Start only when `gh pr list --repo IronbellyOrg/IronClaude --state open --limit 200 --json number,files --jq '[.[] | select(any(.files[]; .path == "src/superclaude/core/WORKER-CONTRACT.md")) | .number]'` prints `[]`, and no other story of this list is already claimed and open: for each of them that is still open (`gh issue view <n> --repo IronbellyOrg/IronClaude --json state --jq .state` prints `OPEN`), `gh api repos/IronbellyOrg/IronClaude/issues/<n>/comments --paginate --jq '[.[] | select(.updated_at >= "2026-11-26" and (.body | contains("<!-- sc:issue:claim -->")))] | length'` prints only `0` (a claim comment posted or edited in this iteration means that story is under way, in either epic; a re-claim edits the earlier comment, which changes its `updated_at`), and no other story of this list in your own epic is started and not yet merged (your progress file). Before step 9, update your branch from `origin/integration` and keep every other story's change in that file.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): the next story in this lane is #792. It also unblocks #799 (a later iteration).
- **Decided for this work:**
  - **Question:** Decision 1: does the watcher only record a claim or result and wake the coordinator, or start the work itself? And may a pull request say "Fixes #N" only when it delivers the whole issue, or does Ruling 26 of docs/designs/sc-closeout.md apply? **Decided:** The watcher records and wakes the coordinator, which is an agent (decision 1's suggested answer; the scheduled wake itself is #757, not in this iteration, so build the template for that model); "Fixes" only for a full delivery, otherwise "Refs", and align Ruling 26 to that.
- **Expected route:** Feature, medium: `/sc:brainstorm --blind` on the summary, `/sc:design` from its merged requirements, `/sc:workflow --depth standard --handoff none` on the design, then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/790.md`

### 8. E1-F3-S2 [#792](https://github.com/IronbellyOrg/IronClaude/issues/792): [FEATURE] Coordinator C11: Define and validate a valid worker_done message

- **Issue:** [#792](https://github.com/IronbellyOrg/IronClaude/issues/792) [FEATURE] Coordinator C11: Define and validate a valid worker_done message
- **Feature:** E1-F3 Coordinator workers: start, track and finish
- **Priority:** Medium; **complexity:** Simple; **kind:** enhancement; **size:** S
- **Lane:** E1-L6, story 2 of 2 (#790 then #792)
- **Start when:** #790 is closed (this story needs it): `gh issue view 790 --repo IronbellyOrg/IronClaude --json state --jq .state` prints `CLOSED`.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Question:** Decision 1: same handoff model as #790. What fields make a valid worker_done message? **Decided:** Same model as #790; the fields are the ones the issue's "What to build" lists, defined and validated as part of this story.
  - **Scope:** #790 first; the field list of a valid worker_done message is part of this work (the issue's "What to build" lists the fields).
- **Expected route:** Feature, simple: plan with `/sc:workflow --depth quick --handoff none`, then `/sc:implement` the printed plan. Model line: `claude-gw-tier2`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/792.md`

### 9. E1-F3-S3 [#771](https://github.com/IronbellyOrg/IronClaude/issues/771): [FEATURE] Wire `/sc:closeout` and `/sc:worktrees` into the coordinator's finish, and give a "not done" result somewhere to go

- **Issue:** [#771](https://github.com/IronbellyOrg/IronClaude/issues/771) [FEATURE] Wire `/sc:closeout` and `/sc:worktrees` into the coordinator's finish, and give a "not done" result somewhere to go
- **Feature:** E1-F3 Coordinator workers: start, track and finish
- **Priority:** Medium; **complexity:** Medium; **kind:** gap-closer; **size:** M
- **Lane:** E1-L7, story 1 of 1 (#771)
- **Start when:** now.
- **Shared files:** this story edits `src/superclaude/core/WORKER-CONTRACT.md`, as do #790 (Ryan), #755 (Ryan), #725 (Ryan), #772 (Ryan), #774 (Ryan), #446 (Leandro), #699 (Leandro). Start only when `gh pr list --repo IronbellyOrg/IronClaude --state open --limit 200 --json number,files --jq '[.[] | select(any(.files[]; .path == "src/superclaude/core/WORKER-CONTRACT.md")) | .number]'` prints `[]`, and no other story of this list is already claimed and open: for each of them that is still open (`gh issue view <n> --repo IronbellyOrg/IronClaude --json state --jq .state` prints `OPEN`), `gh api repos/IronbellyOrg/IronClaude/issues/<n>/comments --paginate --jq '[.[] | select(.updated_at >= "2026-11-26" and (.body | contains("<!-- sc:issue:claim -->")))] | length'` prints only `0` (a claim comment posted or edited in this iteration means that story is under way, in either epic; a re-claim edits the earlier comment, which changes its `updated_at`), and no other story of this list in your own epic is started and not yet merged (your progress file). Before step 9, update your branch from `origin/integration` and keep every other story's change in that file.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Question:** Does the worktrees schedule stay off? Does "never closes" in ruling R38 also cover issues? **Decided:** Schedule stays off (the coordinator runs closeout and cleanup after each merge); R38 covers merging only, closeout may close a finished issue.
- **Expected route:** Feature, medium: `/sc:brainstorm --blind` on the summary, `/sc:design` from its merged requirements, `/sc:workflow --depth standard --handoff none` on the design, then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/771.md`

### 10. E1-F4-S1 [#755](https://github.com/IronbellyOrg/IronClaude/issues/755): Coordinator created multiple Orca Runs by default; find why, set a Run rule, compare one Run per project vs many

- **Issue:** [#755](https://github.com/IronbellyOrg/IronClaude/issues/755) Coordinator created multiple Orca Runs by default; find why, set a Run rule, compare one Run per project vs many
- **Feature:** E1-F4 Coordinator skill: layout, rules and safety
- **Priority:** High; **complexity:** Medium; **kind:** gap-closer; **size:** M
- **Lane:** E1-L8, story 1 of 1 (#755)
- **Start when:** now.
- **Shared files:** this story edits `src/superclaude/core/WORKER-CONTRACT.md`, as do #790 (Ryan), #771 (Ryan), #725 (Ryan), #772 (Ryan), #774 (Ryan), #446 (Leandro), #699 (Leandro). Start only when `gh pr list --repo IronbellyOrg/IronClaude --state open --limit 200 --json number,files --jq '[.[] | select(any(.files[]; .path == "src/superclaude/core/WORKER-CONTRACT.md")) | .number]'` prints `[]`, and no other story of this list is already claimed and open: for each of them that is still open (`gh issue view <n> --repo IronbellyOrg/IronClaude --json state --jq .state` prints `OPEN`), `gh api repos/IronbellyOrg/IronClaude/issues/<n>/comments --paginate --jq '[.[] | select(.updated_at >= "2026-11-26" and (.body | contains("<!-- sc:issue:claim -->")))] | length'` prints only `0` (a claim comment posted or edited in this iteration means that story is under way, in either epic; a re-claim edits the earlier comment, which changes its `updated_at`), and no other story of this list in your own epic is started and not yet merged (your progress file). Before step 9, update your branch from `origin/integration` and keep every other story's change in that file.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane. It also unblocks #786 (a later iteration).
- **Decided for this work:**
  - **Question:** One Orca Run per project or several; what happens to the three live Runs; run the switching test? **Decided:** One Run per project. Close an extra Run only when every pending message in its inbox has been read and handled and no worker still reports into it (check the Run's live workers in Orca first; a Run with a running worker stays open until that worker finishes). Record in the pull request which Runs were closed and why (done-when item 5). A question once sat unseen 10 hours in run_71871571be85. Run the switching test with disposable workers in a throwaway project, as done-when item 4 asks.
- **Expected route:** Feature, medium: `/sc:brainstorm --blind` on the summary, `/sc:design` from its merged requirements, `/sc:workflow --depth standard --handoff none` on the design, then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/755.md`

### 11. E1-F4-S2 [#725](https://github.com/IronbellyOrg/IronClaude/issues/725): [FEATURE] Coordinators MUST ask the peer project's coordinator (read-only) before asking a human

- **Issue:** [#725](https://github.com/IronbellyOrg/IronClaude/issues/725) [FEATURE] Coordinators MUST ask the peer project's coordinator (read-only) before asking a human
- **Feature:** E1-F4 Coordinator skill: layout, rules and safety
- **Priority:** Medium; **complexity:** Medium; **kind:** enhancement; **size:** M
- **Lane:** E1-L9, story 1 of 1 (#725)
- **Start when:** now.
- **Shared files:** this story edits `src/superclaude/core/WORKER-CONTRACT.md`, as do #790 (Ryan), #771 (Ryan), #755 (Ryan), #772 (Ryan), #774 (Ryan), #446 (Leandro), #699 (Leandro). Start only when `gh pr list --repo IronbellyOrg/IronClaude --state open --limit 200 --json number,files --jq '[.[] | select(any(.files[]; .path == "src/superclaude/core/WORKER-CONTRACT.md")) | .number]'` prints `[]`, and no other story of this list is already claimed and open: for each of them that is still open (`gh issue view <n> --repo IronbellyOrg/IronClaude --json state --jq .state` prints `OPEN`), `gh api repos/IronbellyOrg/IronClaude/issues/<n>/comments --paginate --jq '[.[] | select(.updated_at >= "2026-11-26" and (.body | contains("<!-- sc:issue:claim -->")))] | length'` prints only `0` (a claim comment posted or edited in this iteration means that story is under way, in either epic; a re-claim edits the earlier comment, which changes its `updated_at`), and no other story of this list in your own epic is started and not yet merged (your progress file). Before step 9, update your branch from `origin/integration` and keep every other story's change in that file.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - Nothing to decide: build what the issue asks for, within its own scope.
- **Expected route:** Feature, medium: `/sc:brainstorm --blind` on the summary, `/sc:design` from its merged requirements, `/sc:workflow --depth standard --handoff none` on the design, then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/725.md`

### 12. E1-F5-S1 [#766](https://github.com/IronbellyOrg/IronClaude/issues/766): [BUG] Read workers show as Could not Determine

- **Issue:** [#766](https://github.com/IronbellyOrg/IronClaude/issues/766) [BUG] Read workers show as Could not Determine
- **Feature:** E1-F5 Sweep, orchestrator and the cost of the coordinator loop
- **Priority:** High; **complexity:** Medium; **kind:** bug-fix; **size:** M
- **Lane:** E1-L10, story 1 of 3 (#766 then #590 then #534)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): the next story in this lane is #590. It also unblocks #757 (a later iteration).
- **Decided for this work:**
  - **Question:** Is turning every worker of a tail-only transcript into "could not determine" intended? **Decided:** No: keep the evidence and add a note to the row.
  - **One scope with #590** (same owner, Ryan): settle it at the start of whichever of the two starts first. Shared ground: Both fix the sweep's "could not determine" result for workers: the 50-read cap and unfollowed paging, and finished workers whose contract is not read.
- **Expected route:** Bug, medium: `/sc:troubleshoot --fix` with the summary as context; accept its offer to build the plan; then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/766.md`

### 13. E1-F5-S2 [#590](https://github.com/IronbellyOrg/IronClaude/issues/590): Sweep: first live run classified 1 of 264 sessions (show cap of 50, finished workers need an unread contract)

- **Issue:** [#590](https://github.com/IronbellyOrg/IronClaude/issues/590) Sweep: first live run classified 1 of 264 sessions (show cap of 50, finished workers need an unread contract)
- **Feature:** E1-F5 Sweep, orchestrator and the cost of the coordinator loop
- **Priority:** Medium; **complexity:** Medium; **kind:** gap-closer; **size:** M
- **Lane:** E1-L10, story 2 of 3 (#766 then #590 then #534)
- **Start when:** #766 is closed (planned order: start after it lands): `gh issue view 766 --repo IronbellyOrg/IronClaude --json state --jq .state` prints `CLOSED`.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): the next story in this lane is #534. It also unblocks #339 (a later iteration).
- **Decided for this work:**
  - **Question:** Page past the 50-session cap, or measure the cause split first? Change the "settled or asleep" wording, or read the contract? **Decided:** Measure first; read the contract.
  - **One scope with #766** (same owner, Ryan): settle it at the start of whichever of the two starts first. Shared ground: Both fix the sweep's "could not determine" result for workers: the 50-read cap and unfollowed paging, and finished workers whose contract is not read.
- **Expected route:** Feature, medium: `/sc:brainstorm --blind` on the summary, `/sc:design` from its merged requirements, `/sc:workflow --depth standard --handoff none` on the design, then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/590.md`

### 14. E1-F5-S3 [#534](https://github.com/IronbellyOrg/IronClaude/issues/534): Follow-ups from #339 Phase 1 (read-only sweep): open items, owner-ruled limitations and minor findings

- **Issue:** [#534](https://github.com/IronbellyOrg/IronClaude/issues/534) Follow-ups from #339 Phase 1 (read-only sweep): open items, owner-ruled limitations and minor findings
- **Feature:** E1-F5 Sweep, orchestrator and the cost of the coordinator loop
- **Priority:** Medium; **complexity:** Complex; **kind:** chore; **size:** L
- **Lane:** E1-L10, story 3 of 3 (#766 then #590 then #534)
- **Start when:** #590 is closed (this story needs it): `gh issue view 590 --repo IronbellyOrg/IronClaude --json state --jq .state` prints `CLOSED`.
- **Plan approval:** yes: complex, so the owner approves the plan before `/sc:implement` runs.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane. It also unblocks #339 (a later iteration).
- **Decided for this work:**
  - **Question:** The sweep follow-ups need the owner to approve policy edits to WC-16, the output style and the design: which edits? **Decided:** Measure first (decision 5); the issue owner (Ryan) chooses the policy edits to WC-16, the output style and the design and records them in the pull request; the pull request review is the normal merge review, nothing waits on it to start. This part needs Ryan's answer at the start of the story: ask, then record the answer here and in the pull request.
  - **Scope:** an L umbrella whose card says to split it before scheduling: in this iteration take only the slice that follows #590 (the measured cause split and the policy edits it leads to).
- **Expected route:** Feature, complex: `/sc:brainstorm --depth deep --research deep --codebase --blind`, `/sc:design` from its merged requirements, `/sc:workflow --depth deep --handoff none` on the design, then, after the owner approves the plan, `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/534.md`

### 15. E1-F5-S4 [#767](https://github.com/IronbellyOrg/IronClaude/issues/767): Coordinator is compacting convrsation too often

- **Issue:** [#767](https://github.com/IronbellyOrg/IronClaude/issues/767) Coordinator is compacting convrsation too often
- **Feature:** E1-F5 Sweep, orchestrator and the cost of the coordinator loop
- **Priority:** Medium; **complexity:** Medium; **kind:** bug-fix; **size:** M
- **Lane:** E1-L11, story 1 of 1 (#767)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - Nothing to decide: build what the issue asks for, within its own scope.
- **Expected route:** Bug, medium: `/sc:troubleshoot --fix` with the summary as context; accept its offer to build the plan; then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/767.md`

### 16. E1-F5-S5 [#468](https://github.com/IronbellyOrg/IronClaude/issues/468): orchestration check spam

- **Issue:** [#468](https://github.com/IronbellyOrg/IronClaude/issues/468) orchestration check spam
- **Feature:** E1-F5 Sweep, orchestrator and the cost of the coordinator loop
- **Priority:** Medium; **complexity:** Complex; **kind:** bug-fix; **size:** L
- **Lane:** E1-L12, story 1 of 1 (#468)
- **Start when:** now.
- **Plan approval:** no (see Route).
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Question:** Fix the "orchestration message" prompt spam here or where the prompt is produced? **Decided:** Find the producer and record a baseline here first, then move the fix to the producer if it is Orca.
  - **Scope:** only its first step is in this iteration: find the producer and record the baseline (Decision 36); the rest may move to Orca.
- **Expected route:** **Route (replaces steps 5 to 10):** First step only. After the claim, run `/sc:troubleshoot "<the orchestration check spam symptom from issue-summary.md>" --context .dev/issues/468/issue-summary.md` without `--fix` to find the producer of the prompt and record the baseline, post the report's summary and path as a comment on the issue, and stop. The fix moves to the producer (Orca) if that is where it is.
- **Story file:** `.dev/iterations/iteration-3/stories/468.md`

### 17. E1-F6-S1 [#442](https://github.com/IronbellyOrg/IronClaude/issues/442): [TEST GAP] Run the live observations OB-H1, OB-H2, OB-H3 and OB-CTX for the launch-level guard

- **Issue:** [#442](https://github.com/IronbellyOrg/IronClaude/issues/442) [TEST GAP] Run the live observations OB-H1, OB-H2, OB-H3 and OB-CTX for the launch-level guard
- **Feature:** E1-F6 Workers: contract, launch guard, recovery and unattended running
- **Priority:** High; **complexity:** Medium; **kind:** test; **size:** M
- **Lane:** E1-L13, story 1 of 1 (#442)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Question:** Also run the OB-H1, OB-H2 and OB-CTX live observations, as OB-H3 already runs? **Decided:** Yes, with the same coordinator and disposable test issues.
  - **Scope:** the OB-H3 runs are already under way, by the coordinator that works under the ironbelly login (test issues #841 and #842, opened and claimed 10:44 to 10:48 AM; that this is Ryan's coordinator is inferred from the login); the other observation sets (OB-H1, OB-H2, OB-CTX) follow on the same disposable test issues; the ship gate needs four items to pass: OB-H1 item 1, OB-H1 item 5, OB-H2 and OB-H3 (`_GATE_ITEMS` in `tests/hooks/test_launch_level_observations.py`); record each observation's result next to its test (un-skip it, or give a checked reason) and deliver that change through the normal pull request; never change `GOVERNED_LEVELS_ALLOWED` in `src/superclaude/cli/issue_watch/launch.py` and never say on the issue that the gate is lifted: turning it on is a separate reviewed change the owner decides on once all four pass.
  - **Between people:** #442 (Ryan) observes the launch-level guard that #825 (Leandro) changes: agree which guard version the observations run against before either starts (card 825; not verified in #442's steps).
- **Expected route:** Feature, medium: `/sc:brainstorm --blind` on the summary, `/sc:design` from its merged requirements, `/sc:workflow --depth standard --handoff none` on the design, then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/442.md`

### 18. E1-F7-S1 [#777](https://github.com/IronbellyOrg/IronClaude/issues/777): [FEATURE] Too many manual pieces to track per issue: map the whole watcher and coordinator chain and decide what to automate

- **Issue:** [#777](https://github.com/IronbellyOrg/IronClaude/issues/777) [FEATURE] Too many manual pieces to track per issue: map the whole watcher and coordinator chain and decide what to automate
- **Feature:** E1-F7 Watcher and coordinator chain: stage flow, gap list and docs
- **Priority:** High (GitHub: Medium); **complexity:** Simple; **kind:** docs; **size:** S
- **Lane:** E1-L14, story 1 of 1 (#777)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Question:** Who owns the map of manual steps per issue, and where does it live? **Decided:** Ryan owns it, under docs/designs/.
- **Expected route:** Feature, simple: plan with `/sc:workflow --depth quick --handoff none`, then `/sc:implement` the printed plan. Model line: `claude-gw-tier2`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/777.md`

### 19. E1-F7-S2 [#772](https://github.com/IronbellyOrg/IronClaude/issues/772): [FEATURE] Stage flow through the watcher: moving between Research, Spec, Plan and Debug, what Pipeline Full means, and a build step

- **Issue:** [#772](https://github.com/IronbellyOrg/IronClaude/issues/772) [FEATURE] Stage flow through the watcher: moving between Research, Spec, Plan and Debug, what Pipeline Full means, and a build step
- **Feature:** E1-F7 Watcher and coordinator chain: stage flow, gap list and docs
- **Priority:** High (GitHub: Medium); **complexity:** Medium; **kind:** bug-fix; **size:** M
- **Lane:** E1-L15, story 1 of 2 (#772 then #774)
- **Start when:** now.
- **Shared files:** this story edits `src/superclaude/core/WORKER-CONTRACT.md`, as do #790 (Ryan), #771 (Ryan), #755 (Ryan), #725 (Ryan), #774 (Ryan), #446 (Leandro), #699 (Leandro). Start only when `gh pr list --repo IronbellyOrg/IronClaude --state open --limit 200 --json number,files --jq '[.[] | select(any(.files[]; .path == "src/superclaude/core/WORKER-CONTRACT.md")) | .number]'` prints `[]`, and no other story of this list is already claimed and open: for each of them that is still open (`gh issue view <n> --repo IronbellyOrg/IronClaude --json state --jq .state` prints `OPEN`), `gh api repos/IronbellyOrg/IronClaude/issues/<n>/comments --paginate --jq '[.[] | select(.updated_at >= "2026-11-26" and (.body | contains("<!-- sc:issue:claim -->")))] | length'` prints only `0` (a claim comment posted or edited in this iteration means that story is under way, in either epic; a re-claim edits the earlier comment, which changes its `updated_at`), and no other story of this list in your own epic is started and not yet merged (your progress file). Before step 9, update your branch from `origin/integration` and keep every other story's change in that file.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): the next story in this lane is #774.
- **Decided for this work:**
  - **Question:** The four stage-flow questions (a) to (d) for the watcher? **Decided:** The issue owner decides at the start of the work. This part needs Ryan's answer at the start of the story: ask, then record the answer here and in the pull request.
  - **One scope with #774** (same owner, Ryan): settle it at the start of whichever of the two starts first. Shared ground: The wording of what Pipeline Full means (and the "one local commit" line) across `commands/issue.md`, `refs/claim.md`, `launch-prompt.md`, `docs/designs/issue-watcher-status-pipelines.md` and the test at `tests/skills/test_issue_protocol.py`; also `WORKER-CONTRACT.md` and the status-pipelines design are edited by both.
- **Expected route:** Feature, medium: `/sc:brainstorm --blind` on the summary, `/sc:design` from its merged requirements, `/sc:workflow --depth standard --handoff none` on the design, then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/772.md`

### 20. E1-F7-S3 [#774](https://github.com/IronbellyOrg/IronClaude/issues/774): [FEATURE] Docs refresh for the issue watcher and coordinator: stale statements and one contradiction in the worker contract

- **Issue:** [#774](https://github.com/IronbellyOrg/IronClaude/issues/774) [FEATURE] Docs refresh for the issue watcher and coordinator: stale statements and one contradiction in the worker contract
- **Feature:** E1-F7 Watcher and coordinator chain: stage flow, gap list and docs
- **Priority:** Low (GitHub: Medium); **complexity:** Medium; **kind:** docs; **size:** M
- **Lane:** E1-L15, story 2 of 2 (#772 then #774)
- **Start when:** #772 is closed (same lane: the two share one scope): `gh issue view 772 --repo IronbellyOrg/IronClaude --json state --jq .state` prints `CLOSED`.
- **Shared files:** this story edits `src/superclaude/core/WORKER-CONTRACT.md`, as do #790 (Ryan), #771 (Ryan), #755 (Ryan), #725 (Ryan), #772 (Ryan), #446 (Leandro), #699 (Leandro). Start only when `gh pr list --repo IronbellyOrg/IronClaude --state open --limit 200 --json number,files --jq '[.[] | select(any(.files[]; .path == "src/superclaude/core/WORKER-CONTRACT.md")) | .number]'` prints `[]`, and no other story of this list is already claimed and open: for each of them that is still open (`gh issue view <n> --repo IronbellyOrg/IronClaude --json state --jq .state` prints `OPEN`), `gh api repos/IronbellyOrg/IronClaude/issues/<n>/comments --paginate --jq '[.[] | select(.updated_at >= "2026-11-26" and (.body | contains("<!-- sc:issue:claim -->")))] | length'` prints only `0` (a claim comment posted or edited in this iteration means that story is under way, in either epic; a re-claim edits the earlier comment, which changes its `updated_at`), and no other story of this list in your own epic is started and not yet merged (your progress file). Before step 9, update your branch from `origin/integration` and keep every other story's change in that file.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Question:** May the coordinator restart a dead worker by itself (at most once an hour); which backlog-record choice? **Decided:** Yes, on Orca's proof that the worker exited; the issue owner picks the backlog record. This part needs Ryan's answer at the start of the story: ask, then record the answer here and in the pull request.
  - **One scope with #772** (same owner, Ryan): settle it at the start of whichever of the two starts first. Shared ground: The wording of what Pipeline Full means (and the "one local commit" line) across `commands/issue.md`, `refs/claim.md`, `launch-prompt.md`, `docs/designs/issue-watcher-status-pipelines.md` and the test at `tests/skills/test_issue_protocol.py`; also `WORKER-CONTRACT.md` and the status-pipelines design are edited by both.
- **Expected route:** Feature, medium: `/sc:brainstorm --blind` on the summary, `/sc:design` from its merged requirements, `/sc:workflow --depth standard --handoff none` on the design, then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/774.md`

### 21. E1-F8-S1 [#597](https://github.com/IronbellyOrg/IronClaude/issues/597): [BUG] Research routing bypasses available Context7 and Tavily MCP tools

- **Issue:** [#597](https://github.com/IronbellyOrg/IronClaude/issues/597) [BUG] Research routing bypasses available Context7 and Tavily MCP tools
- **Feature:** E1-F8 Troubleshoot, Jev preflight, research tools and confidence check
- **Priority:** Medium (GitHub: unset); **complexity:** Simple; **kind:** bug-fix; **size:** S
- **Lane:** E1-L16, story 1 of 1 (#597)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - Nothing to decide: build what the issue asks for, within its own scope.
- **Expected route:** Bug, simple: `/sc:troubleshoot --depth quick` with the summary as context (no `--fix`), then `/sc:implement` the report it prints. Model line: `claude-gw-tier2`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/597.md`

### 22. E1-F9-S1 [#703](https://github.com/IronbellyOrg/IronClaude/issues/703): Follow-ups from the issue 624 review: five small items in surgical remediation

- **Issue:** [#703](https://github.com/IronbellyOrg/IronClaude/issues/703) Follow-ups from the issue 624 review: five small items in surgical remediation
- **Feature:** E1-F9 Follow-ups on shipped commands, releases and installers
- **Priority:** Low (GitHub: Medium); **complexity:** Simple; **kind:** chore; **size:** S
- **Lane:** E1-L17, story 1 of 1 (#703)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - Nothing to decide: build what the issue asks for, within its own scope.
- **Expected route:** Feature, simple: plan with `/sc:workflow --depth quick --handoff none`, then `/sc:implement` the printed plan. Model line: `claude-gw-tier2`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/703.md`

### 23. E1-F10-S1 [#706](https://github.com/IronbellyOrg/IronClaude/issues/706): [FEATURE] Observer follow-up: session summaries, links, named steps, open session, sweep source and scale tests (sub-issue of #409)

- **Issue:** [#706](https://github.com/IronbellyOrg/IronClaude/issues/706) [FEATURE] Observer follow-up: session summaries, links, named steps, open session, sweep source and scale tests (sub-issue of #409)
- **Feature:** E1-F10 Observer dashboard and contact agents
- **Priority:** Medium; **complexity:** Complex; **kind:** enhancement; **size:** L
- **Lane:** E1-L18, story 1 of 2 (#706 then #409)
- **Start when:** now.
- **Plan approval:** yes: complex, so the owner approves the plan before `/sc:implement` runs.
- **When it is done** (merged and closed out, or closed by its Route): the next story in this lane is #409.
- **Decided for this work:**
  - **Question:** The observer gets its facts from the sweep JSON or its own collection? Session opening or disclosure (items 4 or 5)? Recommendation text and watcher state shown read-only (item 7)? **Decided:** Sweep JSON (one collection); the issue owner decides items 4, 5 and 7 at the start of the work, together with Clay, who owns #409 (the same five acceptance criteria); if Clay has not answered when the work starts, Ryan decides, records it in the pull request, and #409 follows it. This part needs Ryan's answer at the start of the story: ask, then record the answer here and in the pull request.
  - **One scope with #409** (owned by Clay): Ryan and Clay settle it together at the start. Shared ground: The five acceptance criteria added to #409 on 2026-11-13 (same sweep facts, plain-English summary, named steps with colours, open a session, scale tests) are written in both issues.
  - **Between people:** #409 (Clay) needs #706 (Ryan), and both carry the same five acceptance criteria: Ryan builds #706 and settles those criteria with Clay at its start; Clay then finishes #409.
- **Expected route:** Feature, complex: `/sc:brainstorm --depth deep --research deep --codebase --blind`, `/sc:design` from its merged requirements, `/sc:workflow --depth deep --handoff none` on the design, then, after the owner approves the plan, `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/706.md`

