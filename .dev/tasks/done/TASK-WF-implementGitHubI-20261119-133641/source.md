# Source snapshot

## Inline prompt (verbatim)

Implement GitHub issue #669 (adapt Jay's merged-PR daily digest generator into one opt-in script plus tests, with an Orca automation definition that is not switched on), using @.dev/issues/669/issue-body.md and @.dev/issues/669/issue-summary.md

Flags given: `--depth quick`

## Update that supersedes the local copies

Clay edited issue #669 at 2026-11-19T13:36:41Z and the credit rule changed. The live body below (read with `gh issue view 669 --repo IronbellyOrg/IronClaude --json body`) replaces `.dev/issues/669/issue-body.md` and the sentence "It credits the PR author by name" in `.dev/issues/669/issue-summary.md` wherever they differ. New rule: credit goes to the person who made the branch and submitted the PR, not whoever merged it. A bot never gets credit for opening a PR from someone else's work or for merging one. A bot-opened PR (`github-actions[bot]` or any account ending in `[bot]`) credits the person who made its branch (the author of the branch commits). A PR made wholly by a bot with no person behind it goes on a separate "no person" line, credited to nobody. A login not in the table and not a bot is shown as the login. There is no open question about `github-actions[bot]` any more. The tests must also cover a bot opening a PR from a person's branch and a PR made wholly by a bot.

## Referenced file: .dev/issues/669/issue-summary.md (local copy; credit sentence superseded as above)

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/669
- Type: feature
- Complexity: medium
- Effort estimate: 12 hours

Relevant files and systems:

| Path or system | Why it matters |
|---|---|
| `scripts/` (repo root) | Home for the new script; no install step reads it, which keeps the log opt-in. |
| `tests/` | Home for the tests with recorded GitHub responses. |
| `src/superclaude/cli/install_skills.py:88-115`, `src/superclaude/cli/main.py:197-251` | The install code that decides what every user gets; the change must leave it untouched. |
| `/home/coder/workspaces/worktrees/IronFlow/issue-5/.dev/research/merged-pr-log-hosting-comparison-20261119.md` | Hosting research: ClickUp Doc page rewrite (`PUT /v3/workspaces/{workspace_id}/docs/{doc_id}/pages/{page_id}`). |
| `/home/coder/workspaces/worktrees/IronFlow/issue-5/.dev/research/merged-pr-log-scheduler-comparison-20261119.md` | Scheduler research: Orca triggers are UTC, name must not start with `coordinator-`, search rate-limit risk. |
| `/home/coder/workspaces/worktrees/IronFlow/issue-5/tools/merged_pr_log/` | First attempt in the wrong repo; reference only (`credit.py`, `aggregate.py`, tests, `orca-automation.md`). |
| Jay's generator `build-fleet-daily-digest.py` (Simple-With-Us/AI-Fleet-Coordinator) | The code to adapt; Apache-2.0. |

## Live issue body (verbatim, updatedAt 2026-11-19T13:36:41Z)

## Feature Summary

Stand up our own daily log of merged pull requests, per day and per person, across the GitHub orgs IronbellyOrg and IronbellyGroup, by ADAPTING Jay Wedgeworth's existing generator (Apache-2.0, standard library only, about 1,400 lines). Do not write a new one from scratch. Requested by Clay on 2026-11-19. This replaces IronFlow issue #5, which was filed in the wrong repo and wired to the wrong things.

Reference material (Jay's work):
- Generator to adapt: https://github.com/Simple-With-Us/AI-Fleet-Coordinator/blob/main/scripts/build-fleet-daily-digest.py
- How he runs it every 6 hours: https://github.com/Simple-With-Us/AI-Fleet-Coordinator/blob/main/.github/workflows/fleet-activity-site.yml
- His repo allowlist: https://github.com/Simple-With-Us/AI-Fleet-Coordinator/blob/main/scripts/public_activity_repos.py
- His live page, for what it should look like: https://simple-with-us.github.io/AI-Fleet-Coordinator/

## Problem Statement

The team (Clay, Ryan, William, Leandro) has no single place that shows who merged what, per day, across both orgs. Jay's generator already does this for one owner; it needs to be adapted to two orgs, to credit the right person, and to run in exactly one place.

## User Story

As a team member, I want one daily log of merged pull requests per person across IronbellyOrg and IronbellyGroup, so that I can see what each person shipped each day without opening 60 repos.

## Proposed Solution

Keep from Jay's generator: merged PRs per day, day buckets in a fixed time zone (default America/Chicago, its own setting), a 21-day lookback, a web page and a markdown digest, and a link to every PR.

Change or drop:
- Two orgs instead of one owner: IronbellyOrg and IronbellyGroup. List every repo, public and private, fresh on each run so a new repo is included with no edit. Skip archived repos.
- Credit goes to the PERSON WHO MADE THE BRANCH AND SUBMITTED THE PR (Clay's ruling, 2026-11-19), not whoever merged it. A bot never gets credit for opening a PR from someone else's work, and never for merging one. For a PR opened by a bot (`github-actions[bot]` and any account whose name ends in `[bot]`), credit the person who made its branch (the author of the branch's commits). A PR made wholly by a bot with no person behind it (such as a dependency bump) is counted on its own "no person" line, never credited to anyone. Show people by name, NEVER an agent or "Claude Code" (the gateway hides which agent it was).
- Login to person table: `clayphi` is Clay, `ironbelly` is Ryan, `IBC-ChrisG` is Chris, `IB-Lea` is Leandro, `swill-ib` is William. A login that is not in the table and is not a bot is shown as the login. Never guess a person. (There is no question about who owns `github-actions[bot]`: a bot gets no credit.)
- Drop: issues, the calendar feed, the public allowlist, reading the agent from PR titles.

Hard rules from Clay:
1. This log has NOTHING to do with the daily work report or the orchestrator. It must not import from, read the config of, or be installed through either, and it must not live in IronFlow.
2. It belongs in IronClaude but must be OPT-IN. Not everyone who installs IronClaude gets it installed or scheduled, or many people would run the same job. How an install decides its contents, and how this stays opt-in, is under "Opt-in" below.
3. It runs on a schedule in exactly one place: an Orca automation in Clay's Coder workspace, at 5 minutes past 0, 6, 12 and 18 UTC (cron `5 0,6,12,18 * * *`; Orca triggers are UTC). Write the definition for Clay to switch on; do not switch it on. The automation name must NOT start with `coordinator-`, because Orca run history under that prefix is copied into the daily work report (rule 1).
4. Credentials come only from the environment, never from a file. Proposal (names only): `GH_TOKEN` (one token that can read both orgs; the script refuses to run without it instead of falling back to `gh`'s stored login) and `CLICKUP_API_TOKEN`; the ClickUp workspace id and Doc page id also come from the environment (variable names not decided).
5. Keep it small and finish it. A single script plus tests is the target. Do not plan more than the work needs.

### Opt-in

`superclaude install` copies every valid directory under `src/superclaude/skills/`, plus all commands, agents, hooks and templates, to every user, with no opt-in switch (`src/superclaude/cli/install_skills.py:88-115`, `src/superclaude/cli/main.py:197-251`). No `install_*.py` module reads the repo-root `scripts/` folder. So the log ships as one script under repo-root `scripts/` with tests under `tests/`, and with no skill, command, agent or hook. Only a person with a checkout runs it, and the schedule exists only as the Orca automation definition that Clay switches on. The issue was filed with the type `skill`; see the comment below the issue for why that does not fit.

### Hosting

The team must be able to open it. Earlier research found GitHub Pages cannot be team-only on these orgs' plans (IronbellyOrg is on `free`, where Pages needs a public repo; IronbellyGroup is on `team`, where Pages is public on the internet without Enterprise Cloud). It recommends a ClickUp Doc whose page is rewritten in place by the script (`PUT /v3/workspaces/{workspace_id}/docs/{doc_id}/pages/{page_id}`, replace mode). That holds only while the Doc is shared with the team and no public link is switched on; the ClickUp plan of the workspace is not confirmed. Read both files before deciding and reuse them as reference only:
- `/home/coder/workspaces/worktrees/IronFlow/issue-5/.dev/research/merged-pr-log-hosting-comparison-20261119.md`
- `/home/coder/workspaces/worktrees/IronFlow/issue-5/.dev/research/merged-pr-log-scheduler-comparison-20261119.md`

Also reusable as reference, not as code to import: `tools/merged_pr_log/credit.py`, `aggregate.py` and the tests in that worktree (a first attempt in the wrong repo).

Open risk from the research: `gh pr list --search` may count against GitHub's 30 per minute search limit and a run makes about 62 such calls (62 live repos on 2026-11-18). Settle it with a dry run that prints `gh api rate_limit` before and after.

## Acceptance Criteria

- A single script (plus tests) adapted from Jay's generator builds the log from both orgs, with every non-archived repo listed fresh on each run, and a new repo appears with no edit.
- Merged PRs are bucketed per day in a fixed, separately set time zone (default America/Chicago) over a 21-day lookback, and each PR links to GitHub.
- Credit goes to the person who made the branch and submitted the PR, using the login to person table. A bot-opened PR credits the person who made its branch. A PR with no person behind it is counted on a "no person" line. A login that is not in the table and is not a bot is shown as the login. No agent name or "Claude Code" appears anywhere.
- Output is a web page and a markdown digest; issues, the calendar feed, the public allowlist and agent-from-title are gone.
- Nothing imports from, reads the config of, or is installed through the daily work report or the orchestrator, and nothing lives in IronFlow.
- It is opt-in: no skill, command, agent or hook is added, and `superclaude install` output is unchanged.
- Credentials are read only from the environment, no secret value appears in any file, and the script fails clearly when a variable is missing.
- The Orca automation definition (5 minutes past 0, 6, 12 and 18 UTC, name without the `coordinator-` prefix) is written and NOT switched on.
- Tests use recorded GitHub responses and cover: a human author, a bot opening a PR from a person's branch, a PR made wholly by a bot, a PR merged by someone other than its author, a repo with no merges, and a repo added after the first run.
- Human steps are listed, including creating the ClickUp Doc (a human step) and switching on the Orca automation.
- Finished with `/sc:pr-submit --monitor 3`.

## Out of Scope

Issues, the calendar feed, the public allowlist and reading the agent from PR titles. Creating the ClickUp Doc (a human step, listed only). Switching the schedule on. GitHub Actions scheduling. Any link to the daily work report or the orchestrator. Anything that does not fit a single script plus tests.

## Components Affected (from `/sc:analyze`)

- New: a script under repo-root `scripts/` and tests under `tests/` (exact names Not known yet).
- New: the Orca automation definition (location Not known yet; no automation definitions exist in this repo today).
- Read, not changed: `src/superclaude/cli/install_skills.py`, `src/superclaude/cli/main.py` (install contents), to confirm install output does not change.

## Related Issues/PRs

- IronFlow issue #5 (wrong repo; replaced by this issue).
- No duplicate found in this repo. #655 (issue-polling orchestrator) was the closest search hit and is a different piece of work.
