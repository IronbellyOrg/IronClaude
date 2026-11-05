# Reviewer 1 brief (persona: analyzer)

Read-only reviewer. Audit the supplied hunks and matrix; you may Read/Grep/Glob the repo. Run nothing. Return findings only.

## T1 card excerpt

### Deviation / risk section (verbatim from t1-card.md)

How the revision addresses each round 1 finding:

- F-01 (blocking, ordering): the suite/lint/sync/staging task is now Task 14, depending on Task 13 only; the smoke checks are Tasks 15 and 16 after it, with truthful run/unavailable/pending outcomes instead of "reported as blocked"; Task 15 tells the executor to stop and resume in a new session; each smoke task stages its artifact; Task 16 re-runs tests, sync and lint after any fixture or script change.
- F-02 (blocking, security): Constraints add a secrets rule; Task 16 never asks for or inlines the token, needs the user to pre-export it, compares key paths only and never copies live values; Task 2's no-token check uses `env -u CLICKUP_API_TOKEN -u CLICKUP_WORKSPACE_ID` and every test clears both variables.
- F-03: new Task 17 records section 20 items 1-9 as run or pending; item 4 (stops before any write) is run.
- F-04: Task 7 adds the fork-safety scan (`--repo` on every `gh issue|pr|label` line; no `{owner}/{repo}`), Task 3's test adds it for worker bodies.
- F-05: Task 5 claim.md carries `git fetch origin` and `git log --since`; Task 3 body and test carry the fetch-only rule.
- F-06: Task 11 uses `git diff -U0 -- <guide>` with hunks inside 4.1-4.4.
- F-07: Task 10 states the ASCII and live-reference rules.
- F-09: all five refs carry the spawn rule; Task 7 checks every ref.
- F-10: Task 15 names external evidence sources and rejects self-report.
- F-11: Task 7 reads source command files only, noted as a deliberate narrowing.
- F-12: Task 13 compares against `origin/master` after `git fetch origin`.
- F-13: Constraints allow `./artifacts/`, `.dev/issues/smoke/` and the temporary worktree; Task 14 removes the worktree.
- F-15: claim.md adds `--limit 200` to the merged-PR query and records truncation.
- F-16: Task 2 documents the first page and invalid `CLICKUP_MAX_PAGES` behaviour and tests both.
- F-17: Task 7's scan skips `__pycache__` and non-UTF-8 files; Task 13 uses `grep -rIn`.
- F-18: one line-count rule (`len(text.splitlines())`) in Task 6 and Task 7.

Remaining risks:

- R-1: Task 17 item 4 runs `/sc:issue --claim` against a third-party URL (`octocat/Hello-World`); it depends on Wave 0 stopping before any `gh` call, which is what the spec orders (source.md:142-144) but is only as safe as the implemented SKILL.md.
- R-2: Task 15 and Task 16 may legitimately end pending; the plan's Goal now says so.


## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-04T07:10:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command projectPath=/home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/TASK-WF-scIssueCommand-20261104-064713.md:17-26

````markdown
## Constraints

- UV only: run Python and tests with `uv run ...` (`uv run pytest`, `uv run --no-project python ...`); never `python -m`, bare `python script.py` or `pip install`.
- Edit only under `src/superclaude/`, `tests/`, `docs/` and the one plugin guide copy `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (source section 15 and section 17 item 1). Also allowed: this package's `./artifacts/` folder, the unstaged scratch folder `.dev/issues/smoke/` (Task 15), and one temporary Orca worktree for the master comparison (Task 14), which that task removes. `.claude/` is produced by `make sync-dev`; never edit it by hand and never `git add` any `.claude/` path except `.claude/settings.json` (never `git add -f` on `.claude/`).
- Inside the new primitives (command, skill, refs, templates, agents) every reference to another primitive uses its installed path (`~/.claude/commands/sc/<name>.md`, `~/.claude/skills/<name>/...`, `~/.claude/agents/<name>.md`) plus, for existence checks, the project `.claude/` copy; no `src/superclaude/...` path appears in them (source section 15, "Path rule").
- Never interact with the upstream parent `SuperClaude-Org/SuperClaude_Framework`: every `gh` command passes `--repo IronbellyOrg/IronClaude` (or, inside the shipped skill, `--repo <R>` resolved from `origin`), every `gh api` path spells `repos/<owner>/<repo>/...`, and the only fetch is `git fetch origin` (source section 13).
- Secrets: the executor never asks for, prints, echoes or inlines `CLICKUP_API_TOKEN` (no `echo`, `env`, `printenv` or `set -x` on it). When a live ClickUp run is needed, the user exports the variables in their own shell before starting the session (source section 12, "Never printed, logged or written to disk").
- Do not commit or push unless the user asks. `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included; staging is not committing.
- Out of scope for this plan (source section 1 and section 17 item 5): running any next-step chain, creating GitHub labels, creating ClickUp tasks, editing rule 10 of `src/superclaude/core/CLAUDE.md`, changing the level table, adding `plugins/superclaude/` command, agent or skill mirrors, listing the workers in `docs/user-guide/agents.md`, any `src/superclaude/cli/` code, and opening the pull request (done afterwards with `/sc:pr-submit --monitor 3 --head ironbelly/feat-sc-issue-command --title "..." --body "..."`).
- Live `/sc:issue --claim` or `--create` runs post directly to GitHub (source decision B1). Live checks in this plan are the two the source schedules (Task 15 worker spawns, Task 16 ClickUp smoke claim) and the section 20 acceptance record of Task 17. A run that stops before any GitHub or ClickUp write (section 20 item 4) may run without asking; any run that would assign, comment on or create a real GitHub issue needs the user's explicit approval at that moment.
````

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/TASK-WF-scIssueCommand-20261104-064713.md:203-260

````markdown
## Phase 6: Sync, full-suite pass, scheduled smoke checks and acceptance record

## Task 13: Regenerate the dev copies and check sync and installed-path hygiene

Depends on: Task 7, Task 9, Task 10, Task 11, Task 12

Run `make sync-dev`, then `make verify-sync` (source section 17 item 2). Run `grep -rIn 'src/superclaude' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core src/superclaude/hooks` (source section 17 item 4; `-I` skips binary files such as `__pycache__` bytecode) and compare its hits with the fork's master: `git fetch origin`, then `git grep -n 'src/superclaude' origin/master -- src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core src/superclaude/hooks` (`git stash` is not used). Stage nothing under `.claude/`.

Acceptance criteria:
- `make verify-sync` exits 0; output saved to `./artifacts/t13-verify-sync.log`.
- The path grep shows no hit in `src/superclaude/commands/issue.md`, `src/superclaude/skills/sc-issue-protocol/` or `src/superclaude/agents/issue-worker-t*.md`; both grep outputs are saved to `./artifacts/t13-path-grep.txt` with any pre-existing hit marked as pre-existing.
- `git status --porcelain .claude` shows no staged `.claude/` path other than `.claude/settings.json`.

## Task 14: Make the full test suite, lint and sync check pass

Depends on: Task 13

Run the full suite and checks the source names (section 16 last line, section 20 item 9): `uv run pytest tests/commands tests/core tests/skills tests/recommend tests/cli/test_issue_body_templates.py`, then the full suite `uv run pytest` (`make test` runs the same command), then `make lint`, then `make verify-sync`. Fix every failure caused by this feature in the file that causes it (re-running `make sync-dev` after any `src/superclaude/` fix). A failure that also occurs on master without this feature's changes is not fixed here: show that by running the same failing test on master in a temporary Orca worktree (`orca worktree create --name issue302-master-check --base-branch origin/master`; never a raw `git worktree add`), record it as pre-existing with the test ID and error line, then remove the worktree with `orca worktree rm --worktree name:issue302-master-check`.

Acceptance criteria:
- `./artifacts/t14-targeted.log`, `./artifacts/t14-full-pytest.log`, `./artifacts/t14-lint.log` and `./artifacts/t14-verify-sync.log` exist and hold the command outputs with their exit codes.
- `uv run pytest` reports no failure caused by this feature; `make lint` and `make verify-sync` exit 0.
- Every remaining failure is listed in `./artifacts/t14-failures.md` with the test ID, the error line and the evidence that it also fails on master; if there are none, the file says so.
- `orca worktree list` shows no `issue302-master-check` worktree.
- `git add .dev/tasks` has been run so this package and its `artifacts/` are staged; nothing is committed or pushed.

## Task 15: Smoke-spawn each worker agent on its pinned tier

Depends on: Task 14

The source schedules one manual smoke spawn per worker to confirm that the pinned picker ID is served (source section 6, section 20 item 7, default D19). Agent definitions load when a Claude Code session starts, so this check needs a session started after Task 13. If the current session started before Task 13, stop here and ask the user to start a new session in this checkout and re-run the same `/sc:implement` command; it resumes at this task. In that session, spawn `issue-worker-t3`, `issue-worker-t2` and `issue-worker-t1` once each with the Agent tool using only `subagent_type` and never the `model` parameter, with a harmless prompt that writes one file under `.dev/issues/smoke/`. Served-model evidence must come from a source outside the worker: the gateway or proxy request log entry for the call, or the model field of the subagent's transcript; the worker's own statement of its model is recorded but is not accepted as evidence. A spawn that fails because the picker ID is not served is recorded as `E-TIER-UNAVAILABLE` with the agent file and picker ID, not worked around with an alias. `.dev/issues/smoke/` is never staged; delete it afterwards only with the user's approval.

Acceptance criteria:
- `./artifacts/t15-tier-smoke.md` exists with one row per worker giving the spawn outcome and one of: served (with the external evidence source and the picker ID it shows), `E-TIER-UNAVAILABLE` (with the reason), or pending (with the reason the session could not run it). The row states the truth; a pending or unavailable row is a valid result of this task.
- `git add .dev/tasks` has been run after writing the artifact.

## Task 16: Run the manual ClickUp smoke claim against a test task

Depends on: Task 14

The source schedules one manual smoke claim against a ClickUp test task (source section 12, last paragraph; section 20 item 5). It needs a ClickUp test task whose description links a test GitHub issue URL on `IronbellyOrg/IronClaude`, and `CLICKUP_API_TOKEN` and `CLICKUP_WORKSPACE_ID` exported by the user in their own shell before the session started. Ask the user only for the test issue URL and task ID; never ask for, print, echo or inline the token or workspace values. If the variables are not exported, record the task as pending and stop. Otherwise run `uv run --no-project python src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py --issue-url <test issue url> --issue-number <N> --repo IronbellyOrg/IronClaude` twice (the second run should report `already_assigned`). Compare the live response shapes with the fixtures in `tests/skills/test_clickup_claim.py` by key paths only, without printing or copying live values; never copy live values into fixtures. If the shapes differ, update the fixtures with made-up values and the script, then re-run `uv run pytest tests/skills/test_clickup_claim.py -v`, `make sync-dev`, `make verify-sync` and `make lint`.

Acceptance criteria:
- `./artifacts/t16-clickup-smoke.md` records either both runs' status fields (first `assigned` with `rule: github_link`, second `already_assigned`), the test task ID and whether the live key paths matched the fixtures, or "pending" with the reason (variables not exported, or no test task). The token and workspace values appear nowhere in it.
- If the script or fixtures changed: `uv run pytest tests/skills/test_clickup_claim.py -v` passes and `make verify-sync` and `make lint` exit 0, with outputs saved under `./artifacts/t16-*.log`.
- `git add .dev/tasks` has been run after writing the artifact.

## Task 17: Record the section 20 acceptance criteria as run or pending

Depends on: Task 14

Write `./artifacts/t17-acceptance.md` with one row per source section 20 acceptance criterion (items 1 to 9). Each row says run (with the evidence: a test name, artifact path or command output) or pending live verification (with the exact command a user would run and what it needs). Items 7 and 9 point at the Task 3, Task 7, Task 14 and Task 15 evidence; item 5's ClickUp half points at Task 2 and Task 16. Item 4 (a claim URL for another repo stops with `E-FOREIGN-REPO`) stops in Wave 0 before any GitHub or ClickUp write, so run it once in a session that has the skill loaded (after Task 13) as `/sc:issue --claim https://github.com/octocat/Hello-World/issues/1` and record the output. Items 1, 2, 3, 6 and 8 assign, comment on or create real issues or need a worker spawn; leave them pending with their exact commands unless the user approves a run against a test issue at that moment (source decision B1; an incorrect Wave 2 guard would reach `gh issue edit --add-assignee`).

Acceptance criteria:
- `./artifacts/t17-acceptance.md` has nine rows, each run or pending, with evidence or the exact command.
- The item 4 row shows `E-FOREIGN-REPO` from a real run, or pending with the reason the session could not run it.
- No GitHub issue was assigned, commented on or created without the user's approval in this task.
- `git add .dev/tasks` has been run after writing the artifact.
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
| INF-020: the unit tests pin them with recorded fixtures, and the implementation plan includes one manual smoke claim against a test task. | source.md:314 | none | Task 2 | 0.5333 |
| INF-054: Open the PR only with `/sc:pr-submit --monitor 3 | source.md:408 | none | Task 3 | 0.5 |
| INF-058: Running the same claim again edits both comments; the comment count on the issue does not grow. | source.md:468 | none | Task 5 | 0.5 |
| INF-059: A closed issue, or one assigned to someone else, stops with the stated message and makes no GitHub or ClickUp write. | source.md:469 | none | Task 5 | 0.5833 |
| INF-061: With `CLICKUP_API_TOKEN` unset the claim completes and the comment says ClickUp was skipped | source.md:471 | none | Task 2 | 0.5 |
| INF-062: at `standard`/`deep` a disagreement produces one marked pushback comment; no ClickUp call is made. | source.md:472 | none | Task 5 | 0.4 |
