# Iteration 3 work file: swill-ib, epic E4

Generated Thu 26 Nov 2026 07:10 Central by `scripts/epic-files.sh` from the reviewed work map (`work-map.json`). Do not edit by hand: change the map's inputs and rebuild. Repository: `IronbellyOrg/IronClaude`, base branch `integration`. Iteration 3 ends Sunday 6 December.

## 1. Kickoff prompt

This file and the story files live in IronClaude at `.dev/iterations/iteration-3/`, on `integration`. swill-ib starts the epic by opening a new Claude session in an IronClaude checkout of `integration` (after `git pull`) and pasting this:

```text
You lead epic E4 for swill-ib in IronbellyOrg/IronClaude, iteration 3. Read .dev/iterations/iteration-3/epics/E4-swill-ib.md from top to bottom, then run it exactly as its section 4 says. Keep your progress in .dev/iterations/iteration-3/progress/E4.md, one line per story. Never merge a pull request. Ask swill-ib only where this file says the owner decides.
```

## 2. What swill-ib approves by starting this file

- Claiming each issue below on GitHub, one Orca worktree and one agent per story, in the order and lanes of section 5.
- For each story: committing on its own feature branch from `integration`, pushing that branch to `origin` (or, with the owner's go in step 1, the branch of the open pull request the story continues), and opening or attaching its pull request with `/sc:pr-submit --monitor 3`, which also pushes the fixes it makes for review findings and failing checks.
- For a story whose route says so: a comment with its evidence on its issue, closing that issue, filing the new issues the route names, and the writes the story's route or decisions name on other repositories (for example rulesets), each only after the checks they give.
- After a story is closed out: removing its worktree with `/sc:worktrees retire issue-<issue> --apply` (section 7, step 13), only when the dry run says its work is safe.
- Not approved: merging (the owner merges, and never with a failing check), pushing to `integration` or `master`, closing an issue outside the story workflow, and any change outside the story's issue.

## 3. Epic goal

Swarm runs always leave a reliable completion marker and their results, on integration.

## 4. How to run this epic (for the lead session)

1. Check that the files are on `integration`: `git ls-tree origin/integration .dev/iterations/iteration-3/stories/` must list the story files. If it lists nothing, stop and tell swill-ib: the pull request that adds this folder has not merged yet, and every story agent starts in a worktree made from `origin/integration`.
2. Read this whole file before starting anything.
3. Look at section 5. Every lane whose first story says **Start when: now** can start at once: start one agent for each, in parallel, except that only one shared-file story (section 5) runs at a time.
4. Before you start any story, run its **Start when** check and its **Shared files** check. Start it only when both pass. A story that fails a check waits; check again whenever a pull request merges.
5. To start a story, follow the story workflow in section 7, steps 1 and 2: you make its worktree and start its agent with its story file. The agent runs steps 3 to 10 itself.
6. How you and an agent talk: the agent writes `.dev/issues/<issue>/result.md` in its worktree and says in its terminal what it did and what is left, or that it is waiting (for a plan approval or an answer). Read its terminal and that file with the `orca-cli` skill. To give it an answer or the owner's go, type into its terminal with the `orca-cli` skill.
7. When a story's pull request has every check green and every review comment handled, tell swill-ib it is ready to merge. After the merge, run step 12 (closeout) and step 13 (worktree cleanup), then start the next story in that lane.
8. A story marked **Plan approval: yes** stops after its plan. Show swill-ib the plan path; type the owner's go into the agent's terminal only after the owner says go.
9. Where a story's decisions or scope say a part needs swill-ib's answer at the start, ask swill-ib when that story starts and type the answer into the agent's terminal; the agent writes it into the story's decisions (section 7, step 4) and its pull request. Nothing else waits on anyone.
10. Section 6 lists what this epic needs from other people and what they need from it. Check it before each start.
11. Write one line per story to your progress file whenever its state changes: waiting, started, plan ready, pull request open, merged, closed.

## 5. Lanes: what runs at the same time, and what runs in sequence

Stories in the same lane run one after another, in the order shown. Different lanes run at the same time, one agent each. The stories a lane row names as shared-file stories edit `WORKER-CONTRACT.md`: of those, only one is started and not yet merged at any time in this epic (each one's **Shared files** line gives the check); the other stories of such a lane are not held by it.

| Lane | Stories, in order (owner) | First story starts | Runs with |
|---|---|---|---|
| E4-L1 | #540 (swill-ib) | now | every other lane at the same time |
| E4-L2 | #555 (swill-ib) | now | every other lane at the same time |

## 6. Between people

- Nothing: no story of this epic waits on another person's story or shares a file or a scope with one.

## 7. The story workflow (every story, every step, in this order)

This is the workflow of the team's routing guide (`src/superclaude/core/HOW-WE-WORK.md`, sections 1, 3.2 to 3.4 and 3.11) and of the claim skill (`src/superclaude/skills/sc-issue-protocol/`). A story whose route starts with **Route (replaces steps 5 to 10)** has no code change: that paragraph replaces steps 5 to 10. Its agent may comment on and close its own issue as the route says; this is an exception to the claim launch prompt's rule that only the coordinator writes to an issue, and section 2 approves it.

Why the claim runs with `--pipeline none`: the launch gate is open since 25 Nov (pull request 851 set `GOVERNED_LEVELS_ALLOWED = True` after #442's live observations passed), but a launched claim cannot carry this file's decisions into the agent it starts. So the story's agent runs the claim and its next steps in its own session, which the claim skill allows for `--pipeline none`, and adds the decisions itself in step 4.

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
12. **Closeout (lead).** `/sc:closeout <pull request>`. It checks that the pull request merged and settles the issue, the work report entry and the Orca task. A story whose route closes its issue with no pull request skips this step.
13. **Worktree cleanup (lead).** From outside the story's worktree, run `/sc:worktrees retire issue-<issue>`. That dry run says whether the work is safe to remove. When it is, run `/sc:worktrees retire issue-<issue> --apply`: it saves the worktree's `.dev` files to the evidence repo and removes the worktree. When it says the work is not safe, keep the worktree and tell the owner why.
14. **Next (lead).** Start the next story in this lane (section 5), from step 1.

## 8. Stories in order of completion

### 1. E4-F1-S1 [#540](https://github.com/IronbellyOrg/IronClaude/issues/540): [BUG] Successful foreground swarm run does not write done.json completion marker

- **Issue:** [#540](https://github.com/IronbellyOrg/IronClaude/issues/540) [BUG] Successful foreground swarm run does not write done.json completion marker
- **Feature:** E4-F1 Eval framework and swarm tooling
- **Priority:** High; **complexity:** Medium; **kind:** bug-fix; **size:** S
- **Lane:** E4-L1, story 1 of 1 (#540)
- **Start when:** now.
- **Plan approval:** no (see Route).
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Scope:** do not write a second patch; check the issue's done-when on integration, then close it; the done.json-on-resume finding from pull request 846 is a separate follow-up.
- **Expected route:** **Route (replaces steps 5 to 10):** Confirm and close, no new code. In the worktree, check each done-when item of the issue against `integration` (the fix is pull request 762, on `integration` through pull request 846). If every item holds, comment on the issue with the evidence (command and output for each item) and close it; if one fails, stop and report which. File the done.json-on-resume finding from pull request 846 as its own issue with `/sc:issue --create` only if the owner says so.
- **Story file:** `.dev/iterations/iteration-3/stories/540.md`

### 2. E4-F1-S2 [#555](https://github.com/IronbellyOrg/IronClaude/issues/555): [BUG] Detached swarm child drops output delivery and leaves no durable results

- **Issue:** [#555](https://github.com/IronbellyOrg/IronClaude/issues/555) [BUG] Detached swarm child drops output delivery and leaves no durable results
- **Feature:** E4-F1 Eval framework and swarm tooling
- **Priority:** High; **complexity:** Medium; **kind:** bug-fix; **size:** S
- **Lane:** E4-L2, story 1 of 1 (#555)
- **Start when:** now.
- **Plan approval:** no (see Route).
- **When it is done** (merged and closed out, or closed by its Route): it is the last story in its lane.
- **Decided for this work:**
  - **Scope:** do not write a second patch; check the issue's done-when on integration, then close it.
- **Expected route:** **Route (replaces steps 5 to 10):** Confirm and close, no new code. In the worktree, check each done-when item of the issue against `integration` (the fix is pull request 762, on `integration` through pull request 846). If every item holds, comment on the issue with the evidence and close it; if one fails, stop and report which.
- **Story file:** `.dev/iterations/iteration-3/stories/555.md`

