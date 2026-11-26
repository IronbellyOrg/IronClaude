# Iteration 3 work file: Leandro, epic E3

Generated Wed 25 Nov 2026 20:05 Central by `scripts/epic-files.sh` from the reviewed work map (`work-map.json`). Do not edit by hand: change the map's inputs and rebuild. Repository: `IronbellyOrg/IronClaude`, base branch `integration`. Iteration 3 ends Sunday 6 December.

## 1. Kickoff prompt

This file and the story files live in IronClaude at `.dev/iterations/iteration-3/`, on `integration`. Leandro starts the epic by opening a new Claude session in an IronClaude checkout of `integration` (after `git pull`) and pasting this:

```text
You lead epic E3 for Leandro in IronbellyOrg/IronClaude, iteration 3. Read .dev/iterations/iteration-3/epics/E3-leandro.md from top to bottom, then run it exactly as its section 4 says. Keep your progress in .dev/iterations/iteration-3/progress/E3.md, one line per story. Never merge a pull request. Ask Leandro only where this file says the owner decides.
```

## 2. What Leandro approves by starting this file

- Claiming each issue below on GitHub, one Orca worktree and one agent per story, in the order and lanes of section 5.
- For each story: committing on its own feature branch from `integration`, pushing that branch to `origin` (or, with the owner's go in step 1, the branch of the open pull request the story continues), and opening or attaching its pull request with `/sc:pr-submit --monitor 3`, which also pushes the fixes it makes for review findings and failing checks.
- For a story whose route says so: a comment with its evidence on its issue, closing that issue, filing the new issues the route names, and the writes the story's route or decisions name on other repositories (for example rulesets), each only after the checks they give.
- Not approved: merging (the owner merges, and never with a failing check), pushing to `integration` or `master`, closing an issue outside the story workflow, and any change outside the story's issue.

## 3. Epic goal

Workers can run unattended within safe limits, and the repo's tests and CI can be trusted.

## 4. How to run this epic (for the lead session)

1. Check that the files are on `integration`: `git ls-tree origin/integration .dev/iterations/iteration-3/stories/` must list the story files. If it lists nothing, stop and tell Leandro: the pull request that adds this folder has not merged yet, and every story agent starts in a worktree made from `origin/integration`.
2. Read this whole file before starting anything.
3. Look at section 5. Every lane whose first story says **Start when: now** can start at once: start one agent for each, in parallel, except that only one shared-file story (section 5) runs at a time.
4. Before you start any story, run its **Start when** check and its **Shared files** check. Start it only when both pass. A story that fails a check waits; check again whenever a pull request merges.
5. To start a story, follow the story workflow in section 7, steps 1 and 2: you make its worktree and start its agent with its story file. The agent runs steps 3 to 10 itself.
6. How you and an agent talk: the agent writes `.dev/issues/<issue>/result.md` in its worktree and says in its terminal what it did and what is left, or that it is waiting (for a plan approval or an answer). Read its terminal and that file with the `orca-cli` skill. To give it an answer or the owner's go, type into its terminal with the `orca-cli` skill.
7. When a story's pull request has every check green and every review comment handled, tell Leandro it is ready to merge. After the merge, run step 12 (closeout), then start the next story in that lane.
8. A story marked **Plan approval: yes** stops after its plan. Show Leandro the plan path; type the owner's go into the agent's terminal only after the owner says go.
9. Where a story's decisions or scope say a part needs Leandro's answer at the start, ask Leandro when that story starts and type the answer into the agent's terminal; the agent writes it into the story's decisions (section 7, step 4) and its pull request. Nothing else waits on anyone.
10. Section 6 lists what this epic needs from other people and what they need from it. Check it before each start.
11. Write one line per story to your progress file whenever its state changes: waiting, started, plan ready, pull request open, merged, closed.

## 5. Lanes: what runs at the same time, and what runs in sequence

Stories in the same lane run one after another, in the order shown. Different lanes run at the same time, one agent each. The stories a lane row names as shared-file stories edit `WORKER-CONTRACT.md`: of those, only one is started and not yet merged at any time in this epic (each one's **Shared files** line gives the check); the other stories of such a lane are not held by it.

| Lane | Stories, in order (owner) | First story starts | Runs with |
|---|---|---|---|
| E3-L1 | #733 (Leandro) | now | every other lane at the same time |
| E3-L2 | #446 (Leandro) | now | every other lane at the same time; shared-file stories: #446 (one at a time) |
| E3-L3 | #699 (Leandro) | now | every other lane at the same time; shared-file stories: #699 (one at a time) |
| E3-L4 | #825 (Leandro) | now | every other lane at the same time |
| E3-L5 | #465 (Leandro) | now | every other lane at the same time |
| E3-L6 | #618 (Leandro) | now | every other lane at the same time |
| E3-L7 | #702 (Leandro) | now | every other lane at the same time |
| E3-L8 | #333 (Leandro) | now | every other lane at the same time |
| E3-L9 | #313 (Leandro) | now | every other lane at the same time |
| E3-L10 | #603 (Leandro) | now | every other lane at the same time |
| E3-L11 | #376 (Leandro) | now | every other lane at the same time |
| E3-L12 | #552 (Leandro) | now | every other lane at the same time |

## 6. Between people

- #442 (Ryan) observes the launch-level guard that #825 (Leandro) changes: agree which guard version the observations run against before either starts (card 825; not verified in #442's steps).
- `WORKER-CONTRACT.md` is edited by #790, #771, #774, #755, #725 and #772 (Ryan) and by #446 and #699 (Leandro): each of those stories starts only when no open pull request changes that file (its **Shared files** line gives the check).
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

### 1. E3-F1-S1 [#733](https://github.com/IronbellyOrg/IronClaude/issues/733): [FEATURE] Unattended mode for /sc:implement

- **Issue:** [#733](https://github.com/IronbellyOrg/IronClaude/issues/733) [FEATURE] Unattended mode for /sc:implement
- **Feature:** E3-F1 Workers: contract, launch guard, recovery and unattended running
- **Priority:** High; **complexity:** Complex; **kind:** enhancement; **size:** L
- **Lane:** E3-L1, story 1 of 1 (#733)
- **Start when:** now.
- **Plan approval:** yes: complex, so the owner approves the plan before `/sc:implement` runs.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane. It also unblocks #731 (a later iteration).
- **Decided for this work:**
  - Nothing to decide: build what the issue asks for, within its own scope.
- **Expected route:** Feature, complex: `/sc:brainstorm --depth deep --research deep --codebase --blind`, `/sc:design` from its merged requirements, `/sc:workflow --depth deep --handoff none` on the design, then, after the owner approves the plan, `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/733.md`

### 2. E3-F1-S2 [#446](https://github.com/IronbellyOrg/IronClaude/issues/446): WC-9: retry index.lock for about 10 s before a worker reports blocked

- **Issue:** [#446](https://github.com/IronbellyOrg/IronClaude/issues/446) WC-9: retry index.lock for about 10 s before a worker reports blocked
- **Feature:** E3-F1 Workers: contract, launch guard, recovery and unattended running
- **Priority:** Medium; **complexity:** Simple; **kind:** gap-closer; **size:** S
- **Lane:** E3-L2, story 1 of 1 (#446)
- **Start when:** now.
- **Shared files:** this story edits `src/superclaude/core/WORKER-CONTRACT.md`, as do #790 (Ryan), #771 (Ryan), #755 (Ryan), #725 (Ryan), #772 (Ryan), #774 (Ryan), #699 (Leandro). Start only when `gh pr list --repo IronbellyOrg/IronClaude --state open --limit 200 --json number,files --jq '[.[] | select(any(.files[]; .path == "src/superclaude/core/WORKER-CONTRACT.md")) | .number]'` prints `[]`, and no other story of this list is already claimed and open: for each of them, `gh issue view <n> --repo IronbellyOrg/IronClaude --json state,comments --jq 'select(.state == "OPEN") | [.comments[] | select(.createdAt >= "2026-11-26" and (.body | contains("<!-- sc:issue:claim -->")))] | length'` prints `0` or nothing (a claim comment posted in this iteration means that story is under way, in either epic), and no other story of this list in your own epic is started and not yet merged (your progress file). Before step 9, update your branch from `origin/integration` and keep every other story's change in that file.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - Nothing to decide: build what the issue asks for, within its own scope.
- **Expected route:** Feature, simple: plan with `/sc:workflow --depth quick --handoff none`, then `/sc:implement` the printed plan. Model line: `claude-gw-tier2`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/446.md`

### 3. E3-F1-S3 [#699](https://github.com/IronbellyOrg/IronClaude/issues/699): The claim script creates the issue worktree without an agent, against the every-worktree-gets-an-agent rule

- **Issue:** [#699](https://github.com/IronbellyOrg/IronClaude/issues/699) The claim script creates the issue worktree without an agent, against the every-worktree-gets-an-agent rule
- **Feature:** E3-F1 Workers: contract, launch guard, recovery and unattended running
- **Priority:** Medium; **complexity:** Simple; **kind:** decision; **size:** S
- **Lane:** E3-L3, story 1 of 1 (#699)
- **Start when:** now.
- **Shared files:** this story edits `src/superclaude/core/WORKER-CONTRACT.md`, as do #790 (Ryan), #771 (Ryan), #755 (Ryan), #725 (Ryan), #772 (Ryan), #774 (Ryan), #446 (Leandro). Start only when `gh pr list --repo IronbellyOrg/IronClaude --state open --limit 200 --json number,files --jq '[.[] | select(any(.files[]; .path == "src/superclaude/core/WORKER-CONTRACT.md")) | .number]'` prints `[]`, and no other story of this list is already claimed and open: for each of them, `gh issue view <n> --repo IronbellyOrg/IronClaude --json state,comments --jq 'select(.state == "OPEN") | [.comments[] | select(.createdAt >= "2026-11-26" and (.body | contains("<!-- sc:issue:claim -->")))] | length'` prints `0` or nothing (a claim comment posted in this iteration means that story is under way, in either epic), and no other story of this list in your own epic is started and not yet merged (your progress file). Before step 9, update your branch from `origin/integration` and keep every other story's change in that file.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Question:** Keep the claim script's agent-less worktree as a written exception? **Decided:** Yes.
- **Expected route:** Feature, simple: plan with `/sc:workflow --depth quick --handoff none`, then `/sc:implement` the printed plan. Model line: `claude-gw-tier2`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/699.md`

### 4. E3-F1-S4 [#825](https://github.com/IronbellyOrg/IronClaude/issues/825): [BUG] L1 launch-level guard does not protect integration (the new default branch)

- **Issue:** [#825](https://github.com/IronbellyOrg/IronClaude/issues/825) [BUG] L1 launch-level guard does not protect integration (the new default branch)
- **Feature:** E3-F1 Workers: contract, launch guard, recovery and unattended running
- **Priority:** Medium; **complexity:** Simple; **kind:** gap-closer; **size:** S
- **Lane:** E3-L4, story 1 of 1 (#825)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Between people:** #442 (Ryan) observes the launch-level guard that #825 (Leandro) changes: agree which guard version the observations run against before either starts (card 825; not verified in #442's steps).
- **Expected route:** Bug, simple: `/sc:troubleshoot --depth quick` with the summary as context (no `--fix`), then `/sc:implement` the report it prints. Model line: `claude-gw-tier2`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/825.md`

### 5. E3-F1-S5 [#465](https://github.com/IronbellyOrg/IronClaude/issues/465): [BUG] Verifier report delivery failure leaves implementation blocked without bounded recovery

- **Issue:** [#465](https://github.com/IronbellyOrg/IronClaude/issues/465) [BUG] Verifier report delivery failure leaves implementation blocked without bounded recovery
- **Feature:** E3-F1 Workers: contract, launch guard, recovery and unattended running
- **Priority:** Medium; **complexity:** Complex; **kind:** bug-fix; **size:** L
- **Lane:** E3-L5, story 1 of 1 (#465)
- **Start when:** now.
- **Plan approval:** yes: complex, so the owner approves the plan before `/sc:implement` runs.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Question:** Keep rf-qa-qualitative? **Decided:** Keep it (Clay's recommendation of 18 Nov); fix its report-writing wording.
- **Expected route:** Bug, complex: `/sc:troubleshoot --depth deep --fix` with the summary as context; accept its offer to build the plan; then, after the owner approves the plan, `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/465.md`

### 6. E3-F2-S1 [#618](https://github.com/IronbellyOrg/IronClaude/issues/618): Make IronClaude's ruff version follow the Coder image pin instead of its own

- **Issue:** [#618](https://github.com/IronbellyOrg/IronClaude/issues/618) Make IronClaude's ruff version follow the Coder image pin instead of its own
- **Feature:** E3-F2 Repository protection, CI and tool health
- **Priority:** High; **complexity:** Medium; **kind:** bug-fix; **size:** M
- **Lane:** E3-L6, story 1 of 1 (#618)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - Nothing to decide: build what the issue asks for, within its own scope.
- **Expected route:** Bug, medium: `/sc:troubleshoot --fix` with the summary as context; accept its offer to build the plan; then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/618.md`

### 7. E3-F2-S2 [#702](https://github.com/IronbellyOrg/IronClaude/issues/702): [FEATURE] Protect the default branch of IronClaude: no direct push, no force push

- **Issue:** [#702](https://github.com/IronbellyOrg/IronClaude/issues/702) [FEATURE] Protect the default branch of IronClaude: no direct push, no force push
- **Feature:** E3-F2 Repository protection, CI and tool health
- **Priority:** Medium; **complexity:** Complex; **kind:** enhancement; **size:** S
- **Lane:** E3-L7, story 1 of 1 (#702)
- **Start when:** now.
- **Plan approval:** yes: complex, so the owner approves the plan before `/sc:implement` runs.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane. It also unblocks #722 (conditional) (a later iteration).
- **Decided for this work:**
  - **Scope:** direct pushes are refused (checked 25 Nov); still open: the 7-day zero-direct-commit window to Wed 2 Dec, the first real release through the rules, and an update rule for the release-tag ruleset (ironbelly comment, 10:49 AM); pull request 844 (ironbelly/702-tag-update-rule) already carries the release-tag update rule: continue on it or wait for it (step 1, open pull request check).
  - **Between people:** #702 (Leandro) still has an update rule for the release-tag ruleset open, and #837 and #838 (Clay) copy the rulesets in `.github/rulesets/` to other repos: settle the release-tag rule in #702 first, or copy only the branch rulesets until it is settled.
- **Expected route:** Feature, complex: `/sc:brainstorm --depth deep --research deep --codebase --blind`, `/sc:design` from its merged requirements, `/sc:workflow --depth deep --handoff none` on the design, then, after the owner approves the plan, `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/702.md`

### 8. E3-F2-S3 [#333](https://github.com/IronbellyOrg/IronClaude/issues/333): sc-crash-recovery bootstrap_scan.sh exits non-zero and prints no JSON

- **Issue:** [#333](https://github.com/IronbellyOrg/IronClaude/issues/333) sc-crash-recovery bootstrap_scan.sh exits non-zero and prints no JSON
- **Feature:** E3-F2 Repository protection, CI and tool health
- **Priority:** Medium; **complexity:** Simple; **kind:** bug-fix; **size:** XS
- **Lane:** E3-L8, story 1 of 1 (#333)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - Nothing to decide: build what the issue asks for, within its own scope.
- **Expected route:** Bug, simple: `/sc:troubleshoot --depth quick` with the summary as context (no `--fix`), then `/sc:implement` the report it prints. Model line: `claude-gw-tier2`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/333.md`

### 9. E3-F2-S4 [#313](https://github.com/IronbellyOrg/IronClaude/issues/313): Tests must not depend on old logs and planning documents under .dev/

- **Issue:** [#313](https://github.com/IronbellyOrg/IronClaude/issues/313) Tests must not depend on old logs and planning documents under .dev/
- **Feature:** E3-F2 Repository protection, CI and tool health
- **Priority:** Medium; **complexity:** Medium; **kind:** test; **size:** M
- **Lane:** E3-L9, story 1 of 1 (#313)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - Nothing to decide: build what the issue asks for, within its own scope.
- **Expected route:** Feature, medium: `/sc:brainstorm --blind` on the summary, `/sc:design` from its merged requirements, `/sc:workflow --depth standard --handoff none` on the design, then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/313.md`

### 10. E3-F3-S1 [#603](https://github.com/IronbellyOrg/IronClaude/issues/603): [FEATURE] Incorporate spec-panel to Add a review, QA and enrichment phase at the end of sc:design

- **Issue:** [#603](https://github.com/IronbellyOrg/IronClaude/issues/603) [FEATURE] Incorporate spec-panel to Add a review, QA and enrichment phase at the end of sc:design
- **Feature:** E3-F3 Review panel unification and grading
- **Priority:** Medium; **complexity:** Simple; **kind:** enhancement; **size:** M
- **Lane:** E3-L10, story 1 of 1 (#603)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Question:** Spec-panel in sc:design: the original integration only, or the later panel improvements too? Chat-only output, and where review inputs are kept? **Decided:** Original integration only; the issue owner (Leandro) settles the output and persistence points at the start of the work and records them in the pull request. This part needs Leandro's answer at the start of the story: ask, then record the answer here and in the pull request.
- **Expected route:** Feature, simple: plan with `/sc:workflow --depth quick --handoff none`, then `/sc:implement` the printed plan. Model line: `claude-gw-tier2`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/603.md`

### 11. E3-F3-S2 [#376](https://github.com/IronbellyOrg/IronClaude/issues/376): sc:adversarial scoring mixes 25- and 30-criterion rubrics and omits the invariant eligibility report

- **Issue:** [#376](https://github.com/IronbellyOrg/IronClaude/issues/376) sc:adversarial scoring mixes 25- and 30-criterion rubrics and omits the invariant eligibility report
- **Feature:** E3-F3 Review panel unification and grading
- **Priority:** Medium; **complexity:** Medium; **kind:** bug-fix; **size:** M
- **Lane:** E3-L11, story 1 of 1 (#376)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - Nothing to decide: build what the issue asks for, within its own scope.
- **Expected route:** Bug, medium: `/sc:troubleshoot --fix` with the summary as context; accept its offer to build the plan; then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/376.md`

### 12. E3-F3-S3 [#552](https://github.com/IronbellyOrg/IronClaude/issues/552): [FEATURE] Issues being classified as blockers too egregiously

- **Issue:** [#552](https://github.com/IronbellyOrg/IronClaude/issues/552) [FEATURE] Issues being classified as blockers too egregiously
- **Feature:** E3-F3 Review panel unification and grading
- **Priority:** Medium; **complexity:** Medium; **kind:** enhancement; **size:** M
- **Lane:** E3-L12, story 1 of 1 (#552)
- **Start when:** now.
- **Plan approval:** no: the agent runs through to the pull request.
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Question:** Go for stage four on an updated plan (the old plan names skills that pull request 650 removed)? Accept the recorded cuts (no classifier, registry or seeded recall), or reopen them as separate work? **Decided:** The issue owner (Leandro) rewrites the plan for the current skills and decides on the cuts at the start of the work. This part needs Leandro's answer at the start of the story: ask, then record the answer here and in the pull request.
- **Expected route:** Feature, medium: `/sc:brainstorm --blind` on the summary, `/sc:design` from its merged requirements, `/sc:workflow --depth standard --handoff none` on the design, then `/sc:implement` the printed plan. Model line: `claude-gw-tier1b`. (The claim writes the real steps into `next-steps.md` from its chains, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; `/sc:recommend` may adjust them.)
- **Story file:** `.dev/iterations/iteration-3/stories/552.md`

