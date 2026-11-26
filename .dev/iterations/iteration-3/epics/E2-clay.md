# Iteration 3 work file: Clay, epic E2

Generated Wed 25 Nov 2026 19:56 Central by `scripts/epic-files.sh` from the reviewed work map (`work-map.json`). Do not edit by hand: change the map's inputs and rebuild. Repository: `IronbellyOrg/IronClaude`, base branch `integration`. Iteration 3 ends Sunday 6 December.

## 1. Kickoff prompt

This file and the story files live in IronClaude at `.dev/iterations/iteration-3/`, on `integration`. Clay starts the epic by opening a new Claude session in an IronClaude checkout of `integration` (after `git pull`) and pasting this:

```text
You lead epic E2 for Clay in IronbellyOrg/IronClaude, iteration 3. Read .dev/iterations/iteration-3/epics/E2-clay.md from top to bottom, then run it exactly as its section 4 says. Keep your progress in .dev/iterations/iteration-3/progress/E2.md, one line per story. Never merge a pull request. Ask Clay only where this file says the owner decides.
```

## 2. What Clay approves by starting this file

- Claiming each issue below on GitHub, one Orca worktree and one agent per story, in the order and lanes of section 5.
- For each story: committing on its own feature branch from `integration`, pushing that branch to `origin` (or, with the owner's go in step 1, the branch of the open pull request the story continues), and opening or attaching its pull request with `/sc:pr-submit --monitor 3`, which also pushes the fixes it makes for review findings and failing checks.
- For a story whose route says so: a comment with its evidence on its issue, closing that issue, filing the new issues the route names, and the writes the story's route or decisions name on other repositories (for example rulesets), each only after the checks they give.
- Not approved: merging (the owner merges, and never with a failing check), pushing to `integration` or `master`, closing an issue outside the story workflow, and any change outside the story's issue.

## 3. Epic goal

Claiming, releasing and session tooling work reliably on integration, and the team's rules for worktrees, branches and changes are written down.

## 4. How to run this epic (for the lead session)

1. Check that the files are on `integration`: `git ls-tree origin/integration .dev/iterations/iteration-3/stories/` must list the story files. If it lists nothing, stop and tell Clay: the pull request that adds this folder has not merged yet, and every story agent starts in a worktree made from `origin/integration`.
2. Read this whole file before starting anything.
3. Look at section 5. Every lane whose first story says **Start when: now** can start at once: start one agent for each, in parallel, except that only one shared-file story (section 5) runs at a time.
4. Before you start any story, run its **Start when** check and its **Shared files** check. Start it only when both pass. A story that fails a check waits; check again whenever a pull request merges.
5. To start a story, follow the story workflow in section 7, steps 1 and 2: you make its worktree and start its agent with its story file. The agent runs steps 3 to 10 itself.
6. How you and an agent talk: the agent writes `.dev/issues/<issue>/result.md` in its worktree and says in its terminal what it did and what is left, or that it is waiting (for a plan approval or an answer). Read its terminal and that file with the `orca-cli` skill. To give it an answer or the owner's go, type into its terminal with the `orca-cli` skill.
7. When a story's pull request has every check green and every review comment handled, tell Clay it is ready to merge. After the merge, run step 12 (closeout), then start the next story in that lane.
8. A story marked **Plan approval: yes** stops after its plan. Show Clay the plan path; type the owner's go into the agent's terminal only after the owner says go.
9. Where a story's decisions or scope say a part needs Clay's answer at the start, ask Clay when that story starts and type the answer into the agent's terminal; the agent writes it into the story's decisions (section 7, step 4) and its pull request. Nothing else waits on anyone.
10. Section 6 lists what this epic needs from other people and what they need from it. Check it before each start.
11. Write one line per story to your progress file whenever its state changes: waiting, started, plan ready, pull request open, merged, closed.

## 5. Lanes: what runs at the same time, and what runs in sequence

Stories in the same lane run one after another, in the order shown. Different lanes run at the same time, one agent each. The stories a lane row names as shared-file stories edit `WORKER-CONTRACT.md`: of those, only one is started and not yet merged at any time in this epic (each one's **Shared files** line gives the check); the other stories of such a lane are not held by it.

| Lane | Stories, in order (owner) | First story starts | Runs with |
|---|---|---|---|
| E2-L1 | #289 (Clay) | now | every other lane at the same time |
| E2-L2 | #290 (Clay) | now | every other lane at the same time |
| E2-L3 | #379 (Clay) | now | every other lane at the same time |
| E2-L4 | #834 (Clay) | now | every other lane at the same time |
| E2-L5 | #326 (Clay) | now | every other lane at the same time |
| E2-L6 | #393 (Clay) | now | every other lane at the same time |
| E2-L7 | #676 (Clay) | now | every other lane at the same time |
| E2-L8 | #826 (Clay) | now | every other lane at the same time |
| E2-L9 | #599 (Clay) | now | every other lane at the same time |
| E2-L10 | #571 (Clay) | now | every other lane at the same time |
| E2-L11 | #517 (Clay) | now | every other lane at the same time |
| E2-L12 | #837 (Clay) | now | every other lane at the same time |
| E2-L13 | #838 (Clay) | now | every other lane at the same time |
| E2-L14 | #352 (Clay) | now | every other lane at the same time |
| E2-L15 | #765 (Clay) | now | every other lane at the same time |
| E2-L16 | #610 (Clay) then #611 (Clay) | now | every other lane at the same time |
| E2-L17 | #758 (Clay) | now | every other lane at the same time |
| E1-L18 | #706 (Ryan) then #409 (Clay) | now | crosses owners: the second owner starts when the first story is closed |
| E2-L18 | #780 (Clay) | now | every other lane at the same time |
| E2-L19 | #779 (Clay) | now | every other lane at the same time |

## 6. Between people

- #837 (Clay) needs Ryan for the three repos only his login can change: IronHands-CLI, ironops-marketplace, irondots.
- #409 (Clay) needs #706 (Ryan), and both carry the same five acceptance criteria: Ryan builds #706 and settles those criteria with Clay at its start; Clay then finishes #409.
- #702 (Leandro) still has an update rule for the release-tag ruleset open, and #837 and #838 (Clay) copy the rulesets in `.github/rulesets/` to other repos: settle the release-tag rule in #702 first, or copy only the branch rulesets until it is settled.

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
5. **Next steps (agent).** If you continue an open pull request, first read its diff against the issue (`gh pr diff <number> --repo IronbellyOrg/IronClaude`) and do only what it leaves undone. Open `next-steps.md`. Its first line names the model tier it was written for; if this session runs on a lower tier, say so and carry on. Run each step through the Skill tool, in order, in this session; never run a step inside a subagent. The story's **Expected route** says what the steps should look like; if `next-steps.md` differs, follow `next-steps.md` and note the difference in your report. For a bug: if the diagnosis report is inconclusive, failed or blocked, do not plan or apply a fix; stop and report it.
6. **Plan (agent).** For a simple bug there is no plan: the diagnosis report goes straight to step 7. Otherwise the planning step (`/sc:workflow`) prints a plan path, `.dev/tasks/to-do/<id>/<id>.md`, and an advisory check result. Read both. Fix every gap the check names before implementing. If the story says **Plan approval: yes**, stop here: say in the terminal that the plan at that path waits for approval, and wait for the owner's go.
7. **Implement (agent).** `/sc:implement <plan path>`. It implements each step, checks it against the plan's acceptance criteria and ends with an independent final review. If it stops with `E-RESUME-NEEDED`, run the same command again. If it stops with `E-HALT-QA` (a step still fails after its retries), stop and report the step and the progress file path: the owner either has the code fixed and the same command run again, or accepts the explained gap in this session, which `/sc:implement` records itself.
8. **Confirm (agent).** Read `progress.md` beside the plan and the final review. Every step must pass. Run the related tests yourself if nothing ran them.
9. **Commit and push (agent).** If you continue an open pull request: skip the next check, commit on its branch and push to that branch. Otherwise first check that no pull request exists for this branch: `gh pr list --repo IronbellyOrg/IronClaude --head <branch> --state all` must print nothing; if one exists, stop and report it. Commit on a feature branch made from `integration`, with a conventional-commit message (`type(scope): message`). Stage the changed files and `.dev/tasks`; never anything under `.claude/` or `.dev/issues/`. Push the feature branch to `origin`; never push `integration` or `master`.
10. **Pull request (agent).** If you continue an open pull request: `/sc:pr-submit --monitor 3 --pr <number>`. Otherwise `/sc:pr-submit --monitor 3 --head <branch> --base integration --title "<title>" --body "<body>"`. The body carries the story's **Decided for this work** block. Write `Fixes #<issue>` only when the pull request delivers the whole issue; otherwise `Refs #<issue>` and say what is left. Stay with it until every check is green and every review comment is handled, then report.
11. **Merge (owner).** The owner merges. Never merge with a failing check.
12. **Closeout (lead).** `/sc:closeout <pull request>`. It checks that the pull request merged and settles the issue, the work report entry and the Orca task.
13. **Next (lead).** Start the next story in this lane (section 5), from step 1.

## 8. Stories in order of completion

### 1. E2-F1-S1 [#289](https://github.com/IronbellyOrg/IronClaude/issues/289): docs(how-we-work): decide the worktree and branch protocol for parallel sessions

- **Issue:** [#289](https://github.com/IronbellyOrg/IronClaude/issues/289) docs(how-we-work): decide the worktree and branch protocol for parallel sessions
- **Feature:** E2-F1 Claim pipeline, worktrees, git workflows and team rules
- **Priority:** Medium; **complexity:** Medium; **kind:** docs; **size:** M
- **Lane:** E2-L1, story 1 of 1 (#289)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Question:** Exact branch and worktree name format; keep lesson extraction before cleanup? **Decided:** The issue owner (Clay) sets the pattern within the limits in the issue (under 25 characters, no spaces, short description); keep lesson extraction. This part needs Clay's answer at the start of the story: ask, then record the answer here and in the pull request.
- **Expected route:** Feature, medium: `/sc:brainstorm --blind` on the summary, `/sc:design` from its merged requirements, `/sc:workflow --depth standard --handoff none` on the design, then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/289.md`

### 2. E2-F1-S2 [#290](https://github.com/IronbellyOrg/IronClaude/issues/290): docs(how-we-work): decide how team members propose and change skills, commands and agents

- **Issue:** [#290](https://github.com/IronbellyOrg/IronClaude/issues/290) docs(how-we-work): decide how team members propose and change skills, commands and agents
- **Feature:** E2-F1 Claim pipeline, worktrees, git workflows and team rules
- **Priority:** Medium; **complexity:** Medium; **kind:** docs; **size:** M
- **Lane:** E2-L2, story 1 of 1 (#290)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - Nothing to decide: build what the issue asks for, within its own scope.
- **Expected route:** Feature, medium: `/sc:brainstorm --blind` on the summary, `/sc:design` from its merged requirements, `/sc:workflow --depth standard --handoff none` on the design, then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/290.md`

### 3. E2-F1-S3 [#379](https://github.com/IronbellyOrg/IronClaude/issues/379): sc:issue --claim can assign a wrong-repository ClickUp task via #N fallback

- **Issue:** [#379](https://github.com/IronbellyOrg/IronClaude/issues/379) sc:issue --claim can assign a wrong-repository ClickUp task via #N fallback
- **Feature:** E2-F1 Claim pipeline, worktrees, git workflows and team rules
- **Priority:** Medium (GitHub: High); **complexity:** Medium; **kind:** bug-fix; **size:** M
- **Lane:** E2-L3, story 1 of 1 (#379)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - Nothing to decide: build what the issue asks for, within its own scope.
- **Expected route:** Bug, medium: `/sc:troubleshoot --fix` with the summary as context; accept its offer to build the plan; then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/379.md`

### 4. E2-F1-S4 [#834](https://github.com/IronbellyOrg/IronClaude/issues/834): [FEATURE] /sc:issue --create asks the user a question only when the draft contradicts what the user said

- **Issue:** [#834](https://github.com/IronbellyOrg/IronClaude/issues/834) [FEATURE] /sc:issue --create asks the user a question only when the draft contradicts what the user said
- **Feature:** E2-F1 Claim pipeline, worktrees, git workflows and team rules
- **Priority:** Medium (GitHub: unset); **complexity:** Medium; **kind:** enhancement; **size:** M
- **Lane:** E2-L4, story 1 of 1 (#834)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Scope:** its Fix approach says base branch master, but the default branch is integration: branch from integration; pull request 849 (clayphi/issue-834, opened 25 Nov) already carries this work: continue on it (step 1, open pull request check) instead of starting a second one.
- **Expected route:** Feature, medium: `/sc:brainstorm --blind` on the summary, `/sc:design` from its merged requirements, `/sc:workflow --depth standard --handoff none` on the design, then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/834.md`

### 5. E2-F1-S5 [#326](https://github.com/IronbellyOrg/IronClaude/issues/326): [Feature]: Embed more Git and PM related workflows into skills

- **Issue:** [#326](https://github.com/IronbellyOrg/IronClaude/issues/326) [Feature]: Embed more Git and PM related workflows into skills
- **Feature:** E2-F1 Claim pipeline, worktrees, git workflows and team rules
- **Priority:** Medium; **complexity:** Complex; **kind:** enhancement; **size:** L
- **Lane:** E2-L5, story 1 of 1 (#326)
- **Start when:** now.
- **Plan approval:** yes: complex, so the owner approves the plan before `/sc:implement` runs.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Question:** Confirm the narrowed scope of 2 Nov; is branch deletion wanted? **Decided:** Confirm the 2 Nov scope; reuse the local branch cleanup that pull request 711 already delivered (do not rebuild it); no remote branch deletion.
  - **Scope:** assigned on GitHub to ironbelly as well as clayphi: before the claim, Ryan removes himself or Clay removes him (step 1, assignee check).
- **Expected route:** Feature, complex: `/sc:brainstorm --depth deep --research deep --codebase --blind`, `/sc:design` from its merged requirements, `/sc:workflow --depth deep --handoff none` on the design, then, after the owner approves the plan, `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/326.md`

### 6. E2-F2-S1 [#393](https://github.com/IronbellyOrg/IronClaude/issues/393): sc:implement retry ladder now picks advisers it cannot start (from PR #385)

- **Issue:** [#393](https://github.com/IronbellyOrg/IronClaude/issues/393) sc:implement retry ladder now picks advisers it cannot start (from PR #385)
- **Feature:** E2-F2 Follow-ups on shipped commands, releases and installers
- **Priority:** Medium; **complexity:** Medium; **kind:** bug-fix; **size:** S
- **Lane:** E2-L6, story 1 of 1 (#393)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - Nothing to decide: build what the issue asks for, within its own scope.
- **Expected route:** Bug, medium: `/sc:troubleshoot --fix` with the summary as context; accept its offer to build the plan; then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/393.md`

### 7. E2-F2-S2 [#676](https://github.com/IronbellyOrg/IronClaude/issues/676): Core, agent and template installers overwrite edited files with no backup under --force and update

- **Issue:** [#676](https://github.com/IronbellyOrg/IronClaude/issues/676) Core, agent and template installers overwrite edited files with no backup under --force and update
- **Feature:** E2-F2 Follow-ups on shipped commands, releases and installers
- **Priority:** Medium; **complexity:** Medium; **kind:** decision; **size:** S
- **Lane:** E2-L7, story 1 of 1 (#676)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Question:** Should the core, agent and template installers back up edited files like the other installers? **Decided:** Yes, same .bak behaviour as install_commands.py and install_user_setup.py.
- **Expected route:** Feature, medium: `/sc:brainstorm --blind` on the summary, `/sc:design` from its merged requirements, `/sc:workflow --depth standard --handoff none` on the design, then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/676.md`

### 8. E2-F2-S3 [#826](https://github.com/IronbellyOrg/IronClaude/issues/826): [FEATURE] Define the release path from integration to master and update release tooling

- **Issue:** [#826](https://github.com/IronbellyOrg/IronClaude/issues/826) [FEATURE] Define the release path from integration to master and update release tooling
- **Feature:** E2-F2 Follow-ups on shipped commands, releases and installers
- **Priority:** Medium; **complexity:** Medium; **kind:** gap-closer; **size:** M
- **Lane:** E2-L8, story 1 of 1 (#826)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - Nothing to decide: build what the issue asks for, within its own scope.
- **Expected route:** Feature, medium: `/sc:brainstorm --blind` on the summary, `/sc:design` from its merged requirements, `/sc:workflow --depth standard --handoff none` on the design, then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/826.md`

### 9. E2-F2-S4 [#599](https://github.com/IronbellyOrg/IronClaude/issues/599): [FEATURE] Refactor sc:reflect to remove task-builder and task with --remediate --depth deep

- **Issue:** [#599](https://github.com/IronbellyOrg/IronClaude/issues/599) [FEATURE] Refactor sc:reflect to remove task-builder and task with --remediate --depth deep
- **Feature:** E2-F2 Follow-ups on shipped commands, releases and installers
- **Priority:** Low (GitHub: Medium); **complexity:** Medium; **kind:** decision; **size:** S
- **Lane:** E2-L9, story 1 of 1 (#599)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Question:** Pass depth through to the planner (the 17 Nov answer) or keep review-only (what shipped in pull request 653)? **Decided:** The issue owner (Clay) decides at the start of the work; keep review-only until then. This part needs Clay's answer at the start of the story: ask, then record the answer here and in the pull request.
- **Expected route:** Feature, medium: `/sc:brainstorm --blind` on the summary, `/sc:design` from its merged requirements, `/sc:workflow --depth standard --handoff none` on the design, then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/599.md`

### 10. E2-F2-S5 [#571](https://github.com/IronbellyOrg/IronClaude/issues/571): Release 6.0.0: remove headless CLI families, swarm and retired commands from IronClaude (plan for review)

- **Issue:** [#571](https://github.com/IronbellyOrg/IronClaude/issues/571) Release 6.0.0: remove headless CLI families, swarm and retired commands from IronClaude (plan for review)
- **Feature:** E2-F2 Follow-ups on shipped commands, releases and installers
- **Priority:** Low; **complexity:** Complex; **kind:** chore; **size:** S
- **Lane:** E2-L10, story 1 of 1 (#571)
- **Start when:** now.
- **Plan approval:** no (see Route).
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Question:** Close the 6.0.0 umbrella and file its three leftovers as their own issues? **Decided:** Yes.
- **Expected route:** **Route (replaces steps 5 to 10):** No implementation. File each of the umbrella's three leftovers as its own issue with `/sc:issue --create "<leftover>"`, each linked to #571: (1) the Coder pin result, (2) the new-repository issue, filed with "repository to be named by Ryan" for Ryan to edit, so nothing waits on the name, (3) the request to ingest eight analysis documents. Then comment on #571 with the three new links and close it.
- **Story file:** `.dev/iterations/iteration-3/stories/571.md`

### 11. E2-F3-S1 [#517](https://github.com/IronbellyOrg/IronClaude/issues/517): [BUG] ccsession proxy: a tier whose first model always thinks fails every request with the default effort medium and never falls through to the next model

- **Issue:** [#517](https://github.com/IronbellyOrg/IronClaude/issues/517) [BUG] ccsession proxy: a tier whose first model always thinks fails every request with the default effort medium and never falls through to the next model
- **Feature:** E2-F3 Repository protection, CI and tool health
- **Priority:** Medium; **complexity:** Medium; **kind:** bug-fix; **size:** S
- **Lane:** E2-L11, story 1 of 1 (#517)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Scope:** assigned on GitHub to ironbelly, but ccsession work is Clay's (Clay's rule wins over the assignee); before the claim, Ryan removes himself or Clay removes him (step 1, assignee check).
- **Expected route:** Bug, medium: `/sc:troubleshoot --fix` with the summary as context; accept its offer to build the plan; then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/517.md`

### 12. E2-F3-S2 [#837](https://github.com/IronbellyOrg/IronClaude/issues/837): [ruleset] Apply the branch protection rulesets to the other public IronbellyOrg repos (702 follow-up)

- **Issue:** [#837](https://github.com/IronbellyOrg/IronClaude/issues/837) [ruleset] Apply the branch protection rulesets to the other public IronbellyOrg repos (702 follow-up)
- **Feature:** E2-F3 Repository protection, CI and tool health
- **Priority:** Medium (GitHub: unset); **complexity:** not set on GitHub (counted as Medium); **kind:** gap-closer; **size:** S
- **Lane:** E2-L12, story 1 of 1 (#837)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Question:** Which repos get the rulesets? **Decided:** The six repos listed in the issue are the candidates; each one gets the rulesets only after the issue owner's go for that repo and its own 90-day check of direct pushes; Ryan applies the three only his login can change. This part needs Clay's answer at the start of the story: ask, then record the answer here and in the pull request.
  - **Scope:** first step: the issue owner (Clay) gives the go per repo, as its pick-up note asks; needs admin on each repo: Clay has it on three, Ryan applies the three only his login can change (IronHands-CLI, ironops-marketplace, irondots); run the 90-day check of direct pushes per repo first.
  - **Between people:** #837 (Clay) needs Ryan for the three repos only his login can change: IronHands-CLI, ironops-marketplace, irondots.
  - **Between people:** #702 (Leandro) still has an update rule for the release-tag ruleset open, and #837 and #838 (Clay) copy the rulesets in `.github/rulesets/` to other repos: settle the release-tag rule in #702 first, or copy only the branch rulesets until it is settled.
- **Expected route:** Feature, medium: `/sc:brainstorm --blind` on the summary, `/sc:design` from its merged requirements, `/sc:workflow --depth standard --handoff none` on the design, then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/837.md`

### 13. E2-F3-S3 [#838](https://github.com/IronbellyOrg/IronClaude/issues/838): [ruleset] Apply the branch protection rulesets to the IronbellyGroup repos (702 follow-up)

- **Issue:** [#838](https://github.com/IronbellyOrg/IronClaude/issues/838) [ruleset] Apply the branch protection rulesets to the IronbellyGroup repos (702 follow-up)
- **Feature:** E2-F3 Repository protection, CI and tool health
- **Priority:** Medium (GitHub: unset); **complexity:** not set on GitHub (counted as Medium); **kind:** gap-closer; **size:** S
- **Lane:** E2-L13, story 1 of 1 (#838)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Scope:** Clay has admin on all 18 repos; the repo names are in the author's local notes and go to the admin on request; this part needs Clay's answer at the start: the list of repos, which is the go for each of them.
  - **Between people:** #702 (Leandro) still has an update rule for the release-tag ruleset open, and #837 and #838 (Clay) copy the rulesets in `.github/rulesets/` to other repos: settle the release-tag rule in #702 first, or copy only the branch rulesets until it is settled.
- **Expected route:** Feature, medium: `/sc:brainstorm --blind` on the summary, `/sc:design` from its merged requirements, `/sc:workflow --depth standard --handoff none` on the design, then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/838.md`

### 14. E2-F3-S4 [#352](https://github.com/IronbellyOrg/IronClaude/issues/352): Flaky ccsession shim tests in tests/unit/test_ccsession_tiers.py under load

- **Issue:** [#352](https://github.com/IronbellyOrg/IronClaude/issues/352) Flaky ccsession shim tests in tests/unit/test_ccsession_tiers.py under load
- **Feature:** E2-F3 Repository protection, CI and tool health
- **Priority:** Medium; **complexity:** Medium; **kind:** test; **size:** M
- **Lane:** E2-L14, story 1 of 1 (#352)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - Nothing to decide: build what the issue asks for, within its own scope.
- **Expected route:** Feature, medium: `/sc:brainstorm --blind` on the summary, `/sc:design` from its merged requirements, `/sc:workflow --depth standard --handoff none` on the design, then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/352.md`

### 15. E2-F4-S1 [#765](https://github.com/IronbellyOrg/IronClaude/issues/765): [FEATURE] Stop Claude Code from killing the coordinator's message watch under low memory, and research what to stop instead

- **Issue:** [#765](https://github.com/IronbellyOrg/IronClaude/issues/765) [FEATURE] Stop Claude Code from killing the coordinator's message watch under low memory, and research what to stop instead
- **Feature:** E2-F4 Sweep, orchestrator and the cost of the coordinator loop
- **Priority:** High; **complexity:** Complex; **kind:** gap-closer; **size:** L
- **Lane:** E2-L15, story 1 of 1 (#765)
- **Start when:** now.
- **Plan approval:** no (see Route).
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Scope:** the work moved to the Coder repository (Clay's decision on the issue, 25 Nov 2:55 PM Central): one line, export CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1, in the Coder template's aienv.d/defaults.sh; tracked as IronbellyOrg/Coder issue 536; pull request 847 (the ccsession change) is superseded.
- **Expected route:** **Route (replaces steps 5 to 10):** No IronClaude code change: the work moved to IronbellyOrg/Coder issue 536 (one line in the template's aienv.d/defaults.sh). Follow that issue; when its pull request has merged and the image is rebuilt, comment on #765 with the link and close it. Pull request 847 is superseded: close it with a comment pointing to Coder issue 536.
- **Story file:** `.dev/iterations/iteration-3/stories/765.md`

### 16. E2-F5-S1 [#610](https://github.com/IronbellyOrg/IronClaude/issues/610): Jev preflight step 1: add missing performance phrases to the troubleshoot keyword table (sub-issue of #609)

- **Issue:** [#610](https://github.com/IronbellyOrg/IronClaude/issues/610) Jev preflight step 1: add missing performance phrases to the troubleshoot keyword table (sub-issue of #609)
- **Feature:** E2-F5 Troubleshoot, Jev preflight, research tools and confidence check
- **Priority:** Medium; **complexity:** Simple; **kind:** gap-closer; **size:** XS
- **Lane:** E2-L16, story 1 of 2 (#610 then #611)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): the next story in this lane is #611. It also unblocks #609 (a later iteration).
- **Decided for this work:**
  - Nothing to decide: build what the issue asks for, within its own scope.
- **Expected route:** Feature, simple: plan with `/sc:workflow --depth quick --handoff none`, then `/sc:implement` the printed plan. Model line: `claude-gw-tier2`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/610.md`

### 17. E2-F5-S2 [#611](https://github.com/IronbellyOrg/IronClaude/issues/611): Jev preflight step 2: compare Jev against the keyword table on about 30 labelled prompts (sub-issue of #609)

- **Issue:** [#611](https://github.com/IronbellyOrg/IronClaude/issues/611) Jev preflight step 2: compare Jev against the keyword table on about 30 labelled prompts (sub-issue of #609)
- **Feature:** E2-F5 Troubleshoot, Jev preflight, research tools and confidence check
- **Priority:** Low (GitHub: Medium); **complexity:** Medium; **kind:** test; **size:** M
- **Lane:** E2-L16, story 2 of 2 (#610 then #611)
- **Start when:** #610 is closed (this story needs it): `gh issue view 610 --repo IronbellyOrg/IronClaude --json state --jq .state` prints `CLOSED`.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane. It also unblocks #609 (a later iteration), #612 (a later iteration).
- **Decided for this work:**
  - **Question:** Send about 30 public prompts to TypeSafe on the TYPESAFE_API_KEY key with a spend cap; what margin must Jev win by; what median latency is acceptable? **Decided:** Yes, 1 dollar cap, public prompts only; the issue owner (Clay) sets margin and latency before the run. This part needs Clay's answer at the start of the story: ask, then record the answer here and in the pull request.
- **Expected route:** Feature, medium: `/sc:brainstorm --blind` on the summary, `/sc:design` from its merged requirements, `/sc:workflow --depth standard --handoff none` on the design, then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/611.md`

### 18. E2-F6-S1 [#758](https://github.com/IronbellyOrg/IronClaude/issues/758): [FEATURE] Assume the user is coming in blind when asking a decision or question

- **Issue:** [#758](https://github.com/IronbellyOrg/IronClaude/issues/758) [FEATURE] Assume the user is coming in blind when asking a decision or question
- **Feature:** E2-F6 Session startup cost, output style and Orca app issues
- **Priority:** Medium; **complexity:** Simple; **kind:** enhancement; **size:** S
- **Lane:** E2-L17, story 1 of 1 (#758)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - Nothing to decide: build what the issue asks for, within its own scope.
- **Expected route:** Feature, simple: plan with `/sc:workflow --depth quick --handoff none`, then `/sc:implement` the printed plan. Model line: `claude-gw-tier2`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/758.md`

### 19. E2-F6-S2 [#780](https://github.com/IronbellyOrg/IronClaude/issues/780): [BUG] Orca registers this repository under the upstream project id

- **Issue:** [#780](https://github.com/IronbellyOrg/IronClaude/issues/780) [BUG] Orca registers this repository under the upstream project id
- **Feature:** E2-F6 Session startup cost, output style and Orca app issues
- **Priority:** Medium; **complexity:** Medium; **kind:** bug-fix; **size:** M
- **Lane:** E2-L18, story 1 of 1 (#780)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Question:** Change Orca so origin wins, or override the stored upstream once? **Decided:** Try the one-time override first; if it does not hold, change Orca.
- **Expected route:** Bug, medium: `/sc:troubleshoot --fix` with the summary as context; accept its offer to build the plan; then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/780.md`

### 20. E2-F6-S3 [#779](https://github.com/IronbellyOrg/IronClaude/issues/779): [BUG] Orca-ide uses CPU while idle: troubleshoot the 60 frames per second software compositing loop

- **Issue:** [#779](https://github.com/IronbellyOrg/IronClaude/issues/779) [BUG] Orca-ide uses CPU while idle: troubleshoot the 60 frames per second software compositing loop
- **Feature:** E2-F6 Session startup cost, output style and Orca app issues
- **Priority:** Medium; **complexity:** Complex; **kind:** bug-fix; **size:** M
- **Lane:** E2-L19, story 1 of 1 (#779)
- **Start when:** now.
- **Plan approval:** no (see Route).
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Question:** Track Orca's idle CPU here or with the image maintainer? **Decided:** Track it here for the read-only measuring; ask the image maintainer for the fix.
  - **Scope:** only the read-only measuring and tracing steps (Decision 26); the restart steps stay on Clay's hold.
- **Expected route:** **Route (replaces steps 5 to 10):** Measure only. After the claim, run `/sc:troubleshoot "<the idle CPU symptom from issue-summary.md>" --type performance --context .dev/issues/779/issue-summary.md` without `--fix`, post the report's summary and path as a comment on the issue, and stop. The restart steps stay on Clay's hold.
- **Story file:** `.dev/iterations/iteration-3/stories/779.md`

### 21. E2-F7-S1 [#409](https://github.com/IronbellyOrg/IronClaude/issues/409): [FEATURE] TUI Dashboard to Manage Orchestration at Scale

- **Issue:** [#409](https://github.com/IronbellyOrg/IronClaude/issues/409) [FEATURE] TUI Dashboard to Manage Orchestration at Scale
- **Feature:** E2-F7 Observer dashboard and contact agents
- **Priority:** Medium; **complexity:** Complex; **kind:** enhancement; **size:** XS
- **Lane:** E1-L18, story 2 of 2 (#706 then #409)
- **Start when:** #706 (Ryan) is closed (this story needs it): `gh issue view 706 --repo IronbellyOrg/IronClaude --json state --jq .state` prints `CLOSED`.
- **Plan approval:** yes: complex, so the owner approves the plan before `/sc:implement` runs.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Question:** Replace the umbrella status that is out of date? **Decided:** Yes; close it when #706 is done.
  - **One scope with #706** (owned by Ryan): Clay and Ryan settle it together at the start. Shared ground: The five acceptance criteria added to #409 on 2026-11-13 (same sweep facts, plain-English summary, named steps with colours, open a session, scale tests) are written in both issues.
  - **Between people:** #409 (Clay) needs #706 (Ryan), and both carry the same five acceptance criteria: Ryan builds #706 and settles those criteria with Clay at its start; Clay then finishes #409.
- **Expected route:** Feature, complex: `/sc:brainstorm --depth deep --research deep --codebase --blind`, `/sc:design` from its merged requirements, `/sc:workflow --depth deep --handoff none` on the design, then, after the owner approves the plan, `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/409.md`

