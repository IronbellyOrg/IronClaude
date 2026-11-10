# Brief: spec the launch-level enforcement hook (issue #394)

You are a Claude Code session started in a fresh Orca worktree of IronbellyOrg/IronClaude. No human is watching. Work through the steps below in order, decide for yourself instead of waiting, and finish with the committed, pushed and reported result. If a step cannot be done, write why in the result file and stop.

## Fixed rules (from the project CLAUDE.md, do not break)

- The only GitHub repo you touch is `IronbellyOrg/IronClaude` (`origin`). Every `gh` command passes `--repo IronbellyOrg/IronClaude`. Never touch SuperClaude-Org/SuperClaude_Framework (no push, fetch, PR, issue, comment). No Orca link flags (`--issue`, `--pr`, `--reference`, and so on).
- You are on a feature branch made by Orca. Never commit or push to `master` or `main`. Never merge. Do NOT open a PR and do NOT run `/sc:pr-submit`: the owner did not ask for one.
- Edit only inside this worktree. Primitives are edited under `src/superclaude/` and synced with `make sync-dev`; you are writing documents, so you should not need that. Never stage anything under `.claude/` (except `.claude/settings.json`, which you will not touch) and never stage `.dev/issues/`. `.dev/tasks/` is always staged if anything exists there (`git add .dev/tasks`).
- Use UV for Python (`uv run ...`), never bare `python` or `pip`.
- This is requirements and design work only. Do not implement the hook.

## Read first (absolute paths in the main checkout, read-only)

- Issue text: `/home/coder/workspaces/IronClaude/.dev/issues/394/issue-body.md` (issue #394, "Hook that enforces the launch level of claim-launched agents").
- The feature the hook protects: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/launch-levels-addendum.md` (read FR-21 to FR-31 and section 6) and `.../merged-requirements.md` in the same folder.
- Worker rules the hook must not contradict: `~/.claude/WORKER-CONTRACT.md` (outward actions, never-as-worker list).
- Related: issues #322 (worktree write boundary design review), #357 (PreToolUse hook that blocks bare python; its source is `src/superclaude/hooks/scripts/block-bare-python.sh` and `src/superclaude/hooks/hooks.json` in this worktree), #315 (ccsession name prompt in agent-spawned sessions).

## Step 1: brainstorm

Invoke the Skill tool with skill `sc:brainstorm` and these arguments (one line):

`"Design the hook that mechanically enforces the launch level of agents started by /sc:issue --claim --pipeline (issue #394). Cover: what it blocks at each level (worktree, full, full with --submit), how it knows it is in a claim-launched session and which level applies, where the level is stored so the agent cannot edit it, how a human approves and how the hook tells a human command from an agent command, subagents and nested subagents, the Skill, Task and Bash tools, shell wrappers around git, fail-closed behaviour, plain-words block messages, performance, and how it is tested. Goal: maximum effect with the fewest edge cases and unwanted behaviour. @/home/coder/workspaces/IronClaude/.dev/issues/394/issue-body.md @/home/coder/workspaces/IronClaude/.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/launch-levels-addendum.md" --depth standard --proposals 3 --strategy systematic --codebase --research light`

There is no human to answer the Socratic questions: answer them yourself from the issue, the addendum and the code, and write the assumptions into the seed brief. Verify every Claude Code hook behaviour you rely on (PreToolUse matchers and decisions, behaviour with permission prompts off, whether hooks fire inside subagents, the Skill and Task tool names, how to tell a human-typed slash command from an agent tool call, UserPromptSubmit) against the official hooks documentation (https://code.claude.com/docs/en/hooks, or Context7) and mark anything you could not verify as UNVERIFIED. Use the default output folder under `.dev/brainstorms/` in this worktree.

## Step 2: design

When the brainstorm has produced `merged-requirements.md`, invoke the Skill tool with skill `sc:design` and arguments `@<the brainstorm folder>/merged-requirements.md --type architecture --format spec`. If `/sc:design` would ask a question, answer it yourself from the requirements, record the choice as a decision in the spec, and continue. Save the final design as `docs/designs/sc-issue-launch-level-hook.md` in this worktree. It must be a spec a later sprint can implement from: components and files, the state file or other state and why the agent cannot edit it, the exact decision table (tool call x level -> allow or block), the human-approval mechanism, fail-closed rules, edge-case table, test plan with named cases, acceptance criteria, the order of work, and an Open decisions list for anything the owner must decide.

## Step 3: save, commit, push

1. `git remote get-url origin` must print the IronbellyOrg/IronClaude URL and `git branch --show-current` must not be `master` or `main`; otherwise stop and report.
2. Stage the design doc, the new `.dev/brainstorms/<your folder>/`, and `.dev/tasks` if it exists: `git add docs/designs/sc-issue-launch-level-hook.md .dev/brainstorms/<your folder> .dev/tasks`. Run `git status --short` and make sure nothing under `.claude/` or `.dev/issues/` is staged.
3. Commit with a conventional message, for example `docs(hook): spec for the launch-level enforcement hook (#394)`, ending with the line `Co-Authored-By: Claude Code <noreply@anthropic.com>`. Never use `--no-verify`; if a pre-commit hook fails, fix the cause and commit again.
4. `git push -u origin HEAD` (the current feature branch only).

## Step 4: update the issue

Post one comment on issue #394 with `gh issue comment 394 --repo IronbellyOrg/IronClaude --body-file <file>`. The comment starts with `<!-- sc:hook-spec -->`, then: a five-line summary of the design, the open decisions, a link to the spec on the pushed branch (`https://github.com/IronbellyOrg/IronClaude/blob/<branch>/docs/designs/sc-issue-launch-level-hook.md`), and the full spec inside a `<details><summary>Full spec</summary>` block when the comment stays under 60,000 characters (otherwise the summary and link only). Do not edit the issue body, close the issue, or change labels.

## Finish

Write `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/hook-session-result.md` with: status (done / partial / failed), the branch name, the commit hash, the comment URL, the paths of the design doc and the brainstorm folder, convergence score from the brainstorm contract, every UNVERIFIED item, every open decision, and anything you could not do and why. Then print the same summary in the terminal and stop.
