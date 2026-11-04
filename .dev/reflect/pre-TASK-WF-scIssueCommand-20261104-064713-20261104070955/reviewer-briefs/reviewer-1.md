# Reviewer 1 brief (persona: analyzer)

Read-only reviewer. Audit the supplied hunks and matrix; you may Read/Grep/Glob the repo. Run nothing. Return findings only.

## T1 card excerpt

### Deviation / risk section (verbatim from t1-card.md)

- R-1 (important): Section 20 behavioural acceptance criteria 1 to 6 have no execution step (see C-4). A plan that ends with every task passing can still ship a skill whose claim/create waves never ran once. Source section 20 is titled "Acceptance criteria for the implementation" (source.md:465).
- R-2 (minor): Task 14 (plan lines 205-213) needs a Claude Code session started after `make sync-dev` so the new agents load; a single `/sc:implement` session cannot restart itself, so Task 14 is likely to end as "blocked" and needs a human step. The task already says to report blocked rather than passed.
- R-3 (minor): Task 15 (plan lines 215-224) needs the user's ClickUp token and a test task; same blocked-not-passed handling is already written.
- R-4 (minor): the git-fetch rule (C-2) is not assigned to a file.


## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-04T07:10:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command projectPath=/home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/TASK-WF-scIssueCommand-20261104-064713.md:17-25

````markdown
## Constraints

- UV only: run Python and tests with `uv run ...` (`uv run pytest`, `uv run --no-project python ...`); never `python -m`, bare `python script.py` or `pip install`.
- Edit only under `src/superclaude/`, `tests/`, `docs/` and the one plugin guide copy `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (source section 15 and section 17 item 1). `.claude/` is produced by `make sync-dev`; never edit it by hand and never `git add` any `.claude/` path except `.claude/settings.json` (never `git add -f` on `.claude/`).
- Inside the new primitives (command, skill, refs, templates, agents) every reference to another primitive uses its installed path (`~/.claude/commands/sc/<name>.md`, `~/.claude/skills/<name>/...`, `~/.claude/agents/<name>.md`) plus, for existence checks, the project `.claude/` copy; no `src/superclaude/...` path appears in them (source section 15, "Path rule").
- Never interact with the upstream parent `SuperClaude-Org/SuperClaude_Framework`: every `gh` command passes `--repo IronbellyOrg/IronClaude` (or, inside the shipped skill, `--repo <R>` resolved from `origin`), every `gh api` path spells `repos/<owner>/<repo>/...`, and the only fetch is `git fetch origin` (source section 13).
- Do not commit or push unless the user asks. `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included; staging is not committing.
- Out of scope for this plan (source section 1 and section 17 item 5): running any next-step chain, creating GitHub labels, creating ClickUp tasks, editing rule 10 of `src/superclaude/core/CLAUDE.md`, changing the level table, adding `plugins/superclaude/` command, agent or skill mirrors, listing the workers in `docs/user-guide/agents.md`, any `src/superclaude/cli/` code, and opening the pull request (done afterwards with `/sc:pr-submit --monitor 3 --head ironbelly/feat-sc-issue-command --title "..." --body "..."`).
- Live `/sc:issue --claim` or `--create` runs post directly to GitHub (source decision B1). The only live checks in this plan are the two the source schedules (one spawn per worker agent, Task 14; one ClickUp smoke claim against a test task, Task 15). Any run that would post to a real GitHub issue needs the user's explicit approval at that moment.
````

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/TASK-WF-scIssueCommand-20261104-064713.md:205-237

````markdown
## Task 14: Smoke-spawn each worker agent on its pinned tier

Depends on: Task 13

The source schedules one manual smoke spawn per worker to confirm that the pinned picker ID is served (source section 6, section 20 item 7, default D19). In a Claude Code session started in this checkout after Task 13 (so the project `.claude/agents/issue-worker-t*.md` copies are loaded), spawn `issue-worker-t3`, `issue-worker-t2` and `issue-worker-t1` once each with the Agent tool using only `subagent_type` and never the `model` parameter, with a harmless prompt that writes one file under `.dev/issues/smoke/` naming the model it reports running on. Record for each worker: the spawn result, the model it reports, the file it wrote, and whether the session's model log or status line confirms `claude-gw-tier3`, `claude-gw-tier2`, `claude-gw-tier1a`. A spawn that fails because the picker ID is not served is recorded as `E-TIER-UNAVAILABLE` with the agent file and picker ID, not worked around with an alias. Delete `.dev/issues/smoke/` afterwards only with the user's approval.

Acceptance criteria:
- `./artifacts/t14-tier-smoke.md` exists with one row per worker giving the spawn outcome and the served model evidence.
- Each worker either shows its pinned picker ID as served, or its row records `E-TIER-UNAVAILABLE` and the reason, and the task is then reported as blocked rather than passed.

## Task 15: Run the manual ClickUp smoke claim against a test task

Depends on: Task 13

The source schedules one manual smoke claim against a ClickUp test task (source section 12, last paragraph; section 20 item 5). This needs the user's own `CLICKUP_API_TOKEN`, `CLICKUP_WORKSPACE_ID` and a ClickUp test task whose description links a test GitHub issue URL on `IronbellyOrg/IronClaude`; ask the user for them (never write the token to disk or to any artifact). Run `uv run --no-project python src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py --issue-url <test issue url> --issue-number <N> --repo IronbellyOrg/IronClaude` with those variables set in the environment, and run it a second time to confirm `already_assigned`. Compare the live response shapes with the fixtures used in `tests/skills/test_clickup_claim.py` and update the fixtures and script if they differ.

Acceptance criteria:
- `./artifacts/t15-clickup-smoke.md` records both runs' JSON outputs (first `assigned` with `rule: github_link`, second `already_assigned`), the test task ID, and whether the live shapes matched the fixtures; the token appears nowhere in it.
- If the user cannot provide a token or a test task, the artifact says "not run" with that reason and the task is reported as blocked, not passed.
- `uv run pytest tests/skills/test_clickup_claim.py -v` still passes after any fixture update.

## Task 16: Make the full test suite, lint and sync check pass

Depends on: Task 13, Task 14, Task 15

Run the full suite and checks the source names (section 16 last line, section 20 item 9): `uv run pytest tests/commands tests/core tests/skills tests/recommend tests/cli/test_issue_body_templates.py`, then the full suite `uv run pytest`, then `make lint`, then `make verify-sync`. Fix every failure caused by this feature in the file that causes it (re-running `make sync-dev` after any `src/superclaude/` fix). A failure that also occurs on `master` without this feature's changes is not fixed here: show that by running the same failing test on `master` in an Orca worktree (`orca worktree create --name <name> --base-branch origin/master`; never a raw `git worktree add`) and record it as pre-existing with the test ID and error line.

Acceptance criteria:
- `./artifacts/t16-targeted.log`, `./artifacts/t16-full-pytest.log`, `./artifacts/t16-lint.log` and `./artifacts/t16-verify-sync.log` exist and hold the command outputs with their exit codes.
- `uv run pytest` reports no failure caused by this feature; `make lint` and `make verify-sync` exit 0.
- Every remaining failure is listed in `./artifacts/t16-failures.md` with the test ID, the error line and the evidence that it also fails on `master`; if there are none, the file says so.
- `git add .dev/tasks` has been run so this package and its `artifacts/` are staged; nothing is committed or pushed.
````

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md:465-476

````markdown
## 20. Acceptance criteria for the implementation

1. `/sc:issue --claim <N>` on an open, unassigned issue of the origin repo: the T3 worker runs first; the issue is assigned to the current user; `.dev/issues/<N>/` holds `scout.md`, `clickup.json`, `accuracy-check.md`, `summary.md` (with an hours estimate), `recommend.md`, `next-steps.md`, `claim-comment.md`; two marked comments are posted; the command stops without running any next-step command.
2. Running the same claim again edits both comments; the comment count on the issue does not grow.
3. A closed issue, or one assigned to someone else, stops with the stated message and makes no GitHub or ClickUp write.
4. A claim URL for any repo other than origin stops with `E-FOREIGN-REPO`; no `gh` call is made without `--repo <origin repo>`.
5. With `CLICKUP_API_TOKEN` unset the claim completes and the comment says ClickUp was skipped; with a token and a task that links the issue URL, that task gains the user as assignee.
6. `/sc:issue --create "<text>" --mode bug --type cli` at each depth posts an issue whose body follows the selected template's headings, with only labels from section 11 that exist in the repo; at `standard`/`deep` a disagreement produces one marked pushback comment; no ClickUp call is made.
7. Each worker agent file pins its picker ID, and the skill never passes `model` on an Agent call (static test); one manual smoke run per worker shows it was served by the pinned tier.
8. `next-steps.md` contains only commands and flags listed in section 19, starts with the `/model` tier line of section 9, and never contains `--handoff tasklist` or `--handoff design` on a brainstorm step.
9. `make verify-sync` passes; the tests of section 16 pass; `uv run pytest tests/core tests/commands` passes; the `src/superclaude` path grep shows no new hit in the new primitives.
````

## Coverage slice

| Requirement | Citation | Method | Best task | Ratio |
|---|---|---|---|---|
| INF-013: Missing ones are listed in the final output, never created (B7). | source.md:215 | none | Task 2 | 0.5 |
| INF-023: `git fetch origin` is the only fetch; no other remote is added or fetched. | source.md:321 | none | Task 1 | 0.5714 |
| INF-054: Open the PR only with `/sc:pr-submit --monitor 3 | source.md:408 | none | Task 3 | 0.3333 |
| INF-058: Running the same claim again edits both comments; the comment count on the issue does not grow. | source.md:468 | none | Task 5 | 0.5 |
| INF-059: A closed issue, or one assigned to someone else, stops with the stated message and makes no GitHub or ClickUp write. | source.md:469 | none | Task 5 | 0.5833 |
| INF-062: at `standard`/`deep` a disagreement produces one marked pushback comment; no ClickUp call is made. | source.md:472 | none | Task 5 | 0.4 |
