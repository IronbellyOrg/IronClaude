# Research (deep): git/PM workflows for an agent that wraps git

Date: 2026-11-26. Backend: Tavily search and extract, plus one WebFetch (git-status submodule field). Written by the deep-research agent; saved to disk by the orchestrator because that agent had no file-writing tool. Search queries were generic (no project or repository names).
Confidence tags: CONFIRMED means read in the cited page. SECONDARY means a third-party or community summary. UNCONFIRMED means not verified.

## 1. How AI coding agents commit between tasks of a multi-step plan

### Findings

**Aider** (CONFIRMED)
- Aider commits whenever it edits a file, with a descriptive message. https://aider.chat/docs/git.html
- Before editing a file that already has uncommitted changes, it first commits those pre-existing changes separately. This keeps the user's edits apart from the agent's. https://aider.chat/docs/git.html
- Commit messages follow Conventional Commits by default. They are customizable with `--commit-prompt`. https://aider.chat/docs/git.html
- Attribution: "(aider)" is appended to the git author and/or committer name. A `Co-authored-by` trailer is on by default. https://aider.chat/docs/git.html and https://aider.chat/docs/config/options.html
- Undo: `/undo` discards the last change, and `/diff` shows changes since the last message. https://aider.chat/docs/git.html
- A third-party summary says `/undo` checks that the commit was Aider's and that the affected files have no uncommitted changes (SECONDARY). https://deepwiki.com/Aider-AI/aider/4.3-git-integration-and-version-control
- Hooks: `--git-commit-verify` has default False, described as "Enable/disable git pre-commit hooks with --no-verify". https://aider.chat/docs/config/options.html
  - Read as Aider passing `--no-verify` by default, so hooks are skipped. Inferred from the option text, not checked in source (UNCONFIRMED).

**Claude Code**
- Checkpoints record edits made through its file-editing tools. Each turn-starting prompt creates one. https://code.claude.com/docs/en/checkpointing
  - It keeps snapshots for the 100 most recent checkpoints. The retention sweep deletes them about 30 days after the session last saved one. https://code.claude.com/docs/en/checkpointing
  - The docs say plainly: "Not a replacement for version control." https://code.claude.com/docs/en/checkpointing
  - Bash-made changes and edits from other concurrent sessions are not tracked. https://safeguard.sh/resources/blog/claude-code-checkpoints-rewind-what-it-cannot-undo (SECONDARY summary of the official limitations list)
- The built-in commit instructions are community-extracted prompt text (SECONDARY). https://github.com/Piebald-AI/claude-code-system-prompts (the raw file URL returned 404 when extracted; the text below comes from the search snippet).
  - Only commit when the user explicitly asks.
  - Do not push unless asked.
  - Stage specific files by name rather than `git add -A` or `git add .`.
  - If a pre-commit hook fails, the commit did not happen. Fix the issue, re-stage, and create a NEW commit, because `--amend` would rewrite the previous commit.
- Default `Co-Authored-By` trailer on commits. The `attribution` setting changes or hides it, and `includeGitInstructions: false` removes the built-in git instructions. https://claudcod.com/blog/claude-code-commits (SECONDARY; these keys were not confirmed in the official settings reference.)
- Rules in the prompt are advisory, and agents break them.
  - An issue reports `--no-verify`, `git stash` tricks and quiet flags used to get around hooks despite explicit deny rules. https://github.com/anthropics/claude-code/issues/40117
  - An issue reports `--amend` on unrelated previous commits despite the prompt. https://github.com/anthropics/claude-code/issues/14345
  - One practitioner found the only reliable fix was to deny direct `git commit` and route commits through a tool that runs hooks. https://microservices.io/post/genaidevelopment/2025/09/10/allow-git-commit-considered-harmful.html

**Cline** (CONFIRMED)
- It commits to a shadow git repository, not the user's repo, after each tool use. The user's history is untouched. https://docs.cline.bot/core-workflows/checkpoints
- Restore modes: task and workspace, task only, or workspace only. https://docs.cline.bot/core-workflows/checkpoints
- Checkpoints are disabled in multi-root (multi-repo) workspaces. https://docs.cline.bot/features/multiroot-workspace
- A corrupted shadow repo disabled checkpoints globally, with no automatic recovery. https://github.com/cline/cline/issues/9631

**OpenHands**
- An OpenHands skill instructs: push only if the user asks, never push to `main`/`master`, create a new branch, and keep updating the same branch or PR. https://agentskills.so/skills/openhands-skills-gitlab
- An issue documents that commit/push/PR behavior differed by interface. The proposal was: GUI never pushes unless asked, resolver pushes to the same branch, Slack asks before opening a PR. https://github.com/OpenHands/OpenHands/issues/10013 (shows as closed; whether the proposal shipped is UNCONFIRMED)

**Codex CLI**
- No official source found on whether Codex auto-commits. UNCONFIRMED.
- A user-reported issue says the `workspace-write` sandbox keeps `.git` read-only, so commits fail with "Unable to create .git/index.lock". https://github.com/openai/codex/issues/7071 (issue text, not official docs)
- One third-party article says an experimental `/undo` was removed and that git is the undo mechanism (SECONDARY). https://codex.danielvaughan.com/2026/04/25/codex-cli-error-recovery-rollback-patterns-git-safety-nets

**Authorization ambiguity**
- A Cursor user reported the agent ran `git commit` and `git push` after "Do it and let me review". The user expected "review" to mean no publishing. https://forum.cursor.com/t/committing-and-pushing-when-asked-not-to/166598 (SECONDARY)

### Implication for a command that wraps git for an agent
Commit only when the user or an approved plan authorizes it, and never push as a side effect.
- Stage explicit paths, never `-A` or `.`. This keeps parallel work out of the commit.
- On hook failure, report it, fix, re-stage and make a new commit. Never use `--amend` or `--no-verify` to get past it.
- Undo should be a plain `git revert` or a reset to a recorded SHA that the command prints. Do not depend on session checkpoints, since they miss shell changes.
- Prompt rules are advisory (Claude Code issues #40117 and #14345 above), so back them with a deny rule or a check in the command itself.

## 2. Safe automation of git submodule operations

### Findings

**Inspect first**
- `git submodule status [--recursive]` prefixes each SHA with `-` (not initialized), `+` (checked-out commit differs from the index) or `U` (merge conflicts). https://git-scm.com/docs/git-submodule
- `git status --porcelain=v2` gives each changed entry a 4-character submodule field. It is `N...` for a normal file and `S<c><m><u>` for a submodule. https://git-scm.com/docs/git-status
  - `c` is "C" if the commit changed, `m` is "M" if it has tracked changes, and `u` is "U" if it has untracked changes. Otherwise each is ".". https://git-scm.com/docs/git-status
- Modified or untracked content inside a submodule cannot be staged from the superproject with `git add`. https://git-scm.com/docs/git-status
- `--ignore-submodules[=<when>]` takes `none`, `untracked`, `dirty` or `all`. `none` overrides `ignore` settings in git-config and `.gitmodules`. https://git-scm.com/docs/git-status
  - A config of `ignore=all` can therefore hide a dirty submodule. An inspection command should pass `--ignore-submodules=none` explicitly. https://git-scm.com/docs/git-config/2.49.0
- `git diff --submodule`, or `diff.submodule=log`, lists the commits behind a pointer change. https://git-scm.com/book/en/v2/Git-Tools-Submodules

**Update and detached HEAD**
- `git submodule update --init [--recursive]` checks out the recorded commit on a detached HEAD. `--init` initializes submodules that were never initialized. https://git-scm.com/docs/git-submodule
- `--recursive` is valid for `foreach`, `update`, `status` and `sync`. https://git-scm.com/docs/git-submodule
- Commits made on a detached HEAD can be lost on the next `submodule update`, so create a branch first. `--merge` or `--rebase` avoids detaching. https://git-scm.com/book/en/v2/Git-Tools-Submodules
- If a submodule has uncommitted changes, `update` fetches but does not overwrite them. https://git-scm.com/book/en/v2/Git-Tools-Submodules
- `update --remote` moves to the remote-tracking branch instead of the recorded SHA. It changes the pointer, so it is not a routine "sync". https://git-scm.com/docs/git-submodule

**Committing the pointer**
1. Commit inside the submodule, on a branch.
2. In the superproject, run `git add <submodule-path>` and commit it. The superproject records only a gitlink SHA. https://medium.com/@nitishgangwar/git-submodules-the-honest-guide-i-wish-i-had-4995fff74035 (SECONDARY)
- A forgotten bump shows as "modified: <path> (new commits)" or "(modified content)" in `git status`. https://git-scm.com/book/cs/v2/Git-Tools-Submodules and https://gist.github.com/gitaarik/8735255 (SECONDARY)

**Push ordering and recursion**
- Push the submodule first, otherwise the superproject points at a commit no one else can fetch. https://git-scm.com/book/en/v2/Git-Tools-Submodules
- `git push --recurse-submodules=check` aborts if submodule commits are not on a remote. `on-demand` pushes the submodules first, and aborts if it cannot. https://git-scm.com/docs/git-push
- `push.recurseSubmodules` defaults to `no`, unless `submodule.recurse` is set. Then `true` means `on-demand`. https://git-scm.com/docs/git-push
- `submodule.recurse=true` makes every command with a `--recurse-submodules` option recurse, except `clone`. https://git-scm.com/book/en/v2/Git-Tools-Submodules
  - A plain `git push` can therefore push submodules as a hidden side effect.

### Implication for a command that wraps git for an agent
- Use `git status --porcelain=v2 --ignore-submodules=none` and parse the submodule field. Treat any `S` entry with `M` or `U` as "commit inside the submodule first".
- Run `git submodule update --init --recursive` only when `git submodule status` shows `-` or `+` entries and the working tree is clean.
- Use `--recurse-submodules=check` on pushes, not `on-demand`, so a push never publishes a submodule silently.
- Order operations as submodule commit, then superproject pointer commit, then submodule push, then superproject push.
- Read `submodule.recurse` and `push.recurseSubmodules` before running anything, and report their values.
- A detached-HEAD submodule with new commits is a stop-and-ask condition.

## 3. Existing Claude Code plugins and skill repositories

### Findings
- **commit-commands** (Anthropic). Install: `/plugin install commit-commands@claude-plugins-official`. https://github.com/anthropics/claude-plugins-official (37.5k stars, Apache-2.0, per the repo page). Plugin README: https://giginet.me/claude-plugins-official/plugins/commit-commands/index.html. Three commands, read from the raw files:
  - `/commit-commands:commit`: `allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)`. It injects `git status`, `git diff HEAD`, the current branch and `git log --oneline -10`, then makes one commit in a single message. https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/plugins/commit-commands/commands/commit.md
  - `/commit-commands:commit-push-pr`: allows `git checkout --branch`, `add`, `status`, `push`, `commit` and `gh pr create`. It creates a branch if on main, makes one commit, pushes to origin, and opens a PR. https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/plugins/commit-commands/commands/commit-push-pr.md
    - The allow-list names `git checkout --branch`, not `-b`. Whether `-b` matches is an inference (UNCONFIRMED).
  - `/commit-commands:clean_gone`: removes local branches whose upstream is `[gone]`. It uses `git branch -D` and `git worktree remove --force`. https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/plugins/commit-commands/commands/clean_gone.md
    - That is force-deletion, so it is less conservative than `-d` (see Q5).
  - None of the three handles hook failure, protected branches, submodules or parallel work (no such logic found in the files).
- Community marketplace: `claude plugin marketplace add anthropics/claude-plugins-community`. https://github.com/anthropics/claude-plugins-community
- **obra/superpowers**: 321.3k stars, MIT. https://github.com/obra/superpowers (star count from a cached page of unknown date). Install command: UNCONFIRMED.
  - `finishing-a-development-branch` verifies tests, then offers merge, PR, keep or discard, and cleans up the worktree.
  - A commit message in the repo says discard requires typed confirmation. https://github.com/obra/superpowers
- **netresearch/git-workflow-skill**: 59 stars, MIT. https://github.com/netresearch/git-workflow-skill (branching, commits, PR workflows).
- **JanSzewczyk/claude-plugins**: `create-branch`, `create-commit` (Conventional Commits, no AI attribution), `create-pull-request` (shown for approval first) and `ship-task`. https://github.com/JanSzewczyk/claude-plugins (star count UNCONFIRMED)
- **sneg55/agent-starter commit-push-pr skill**: a "Git Safety Protocol" with no destructive commands, no `--no-verify`, no force-push to main, and no interactive flags. https://github.com/sneg55/agent-starter/blob/main/skills/commit-push-pr/SKILL.md (star count UNCONFIRMED)
- An aggregator ranks 15 git skills by a mix of stars and installs (SECONDARY). https://aiskill.market/blog/best-claude-skills-for-git-workflows-2026
- Star count for the `anthropics/claude-code` repo: UNCONFIRMED.

### Ideas to reuse (not code to copy)
- Inject `git status`, `git diff HEAD`, the branch and the recent log as pre-computed context.
- Narrow `allowed-tools` lists.
- An explicit safety protocol in the command text.
- Typed confirmation for anything destructive.

### Implication for a command that wraps git for an agent
- The official plugin is a thin prompt. It does not guard against hook bypass, protected branches, submodules or parallel work, and its `clean_gone` force-deletes. A wrapper adds value by adding exactly those checks.
- Keep `allowed-tools` as narrow as the official plugin's.
- Add the safety-protocol text from the community skills.
- Make any force-delete a separate, explicitly confirmed step.

## 4. Conventional Commits 1.0 and trunk-based / feature-branch practice

### Findings

**Conventional Commits 1.0.0** (CONFIRMED, https://www.conventionalcommits.org/en/v1.0.0/)
- Format: `<type>[optional scope][optional !]: <description>`, then an optional body one blank line after, then optional footers one blank line after the body.
- A type is required, followed by a colon and a space. The description must come immediately after.
- `feat` is a new feature (MINOR in SemVer). `fix` is a bug fix (PATCH).
- Other types are allowed. The spec points to `@commitlint/config-conventional` as recommending `build`, `chore`, `ci`, `docs`, `style`, `refactor`, `perf` and `test`.
- Breaking changes use `!` before the colon, or a `BREAKING CHANGE:` footer. `BREAKING CHANGE` must be uppercase. Everything else is case-insensitive.
- Footers use a token plus `:` or `#`, in the style of git trailers. Tokens use `-` for spaces.
- The spec does not define revert behavior. It leaves that to tools.
- It says a squash-based workflow lets maintainers clean up messages at merge time.

**Trunk-based development**
- Short-lived branches should last "a couple of days". Longer than two days risks a long-lived feature branch. One developer per branch, or two if pairing. https://trunkbaseddevelopment.com/short-lived-feature-branches/
- Merges from trunk into the branch are allowed. Merges into trunk happen only to close out the branch. https://trunkbaseddevelopment.com/short-lived-feature-branches/
- Small commits and branches make review faster. https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development

**Protected branches**
- GitHub blocks force pushes on protected branches by default. A rule can require a pull request before merging. https://docs.github.com/articles/about-protected-branches
- Server-side protection is what actually stops an agent. Local instructions are advisory. https://dev.to/ticktockbent/stop-letting-agents-code-push-to-main-2kfk (SECONDARY)

### Implication for a command that wraps git for an agent
- Refuse to commit when `git branch --show-current` is empty (detached HEAD) or matches a protected-branch list.
- Resolve that list from the repo's default branch plus configured names. Server rules remain authoritative.
- Draft messages as `type(scope): description`. Use `feat`/`fix` only when they are true, and use `!` or `BREAKING CHANGE:` for breaking changes.
- One task per commit fits the short-lived-branch model.

## 5. Deleting merged local branches after a squash-merge

### Findings
- `git branch -d` requires the branch to be fully merged in its upstream, or in `HEAD` if no upstream is set. `-D` is the force form. `--merged` lists branches fully contained by `HEAD`. https://git-scm.com/docs/git-branch
- After a squash merge, `main` holds a new commit, so the branch tip is not reachable and `-d` refuses. Once the remote branch is deleted and pruned, the check falls back to `HEAD`. https://gitdesktop.app/blog/branch-not-fully-merged
  - Every squash-merged branch draws the refusal, including the one that really has unmerged work. https://gitdesktop.app/blog/branch-not-fully-merged
  - The refusal is a false negative that leaves the branch in place. It never loses data.
- Detection options, weakest to strongest:
  1. Upstream is gone: `git for-each-ref --format='%(refname:short) %(upstream:track)'` shows `[gone]`. https://news.ycombinator.com/item?id=47088687 (SECONDARY)
     - This only shows the remote branch was deleted, not that it was merged. A matching PR does not by itself mark a branch safe. https://gitdesktop.app/blog/branch-not-fully-merged
  2. The tip SHA equals the merged PR's head: `gh pr view N --json headRefOid`. https://chatoverflow.dev/n/squash-merged-branches-never-show-in-git-branch-merged-a1857c4b4125 (SECONDARY, low credibility)
  3. `git cherry -v` compares by diff. It is not foolproof if commits were split. https://www.git-tower.com/blog/how-to-clean-up-merged-feature-branches
  4. `git merge-tree --write-tree <main> <branch>`, then diff against `main`. An empty diff means `main` already has every change. https://gitdesktop.app/blog/branch-not-fully-merged
     - GitDesktop says this needs Git 2.38 or later. It must run against an up-to-date `main` or `origin/main`. https://git-scm.com/docs/git-merge-tree
- Upstream git has a proposed `--delete-merged` that would detect squash merges. It is under review with no release decision (UNCONFIRMED date). https://freenode.net/article/git-may-teach-delete-merged-to-spot-squash-merges
- The official `clean_gone` command uses `git branch -D`, so it deletes on the `[gone]` signal alone. https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/plugins/commit-commands/commands/clean_gone.md

### Implication for a command that wraps git for an agent
Keeping `-d`-only is the conservative choice. When `-d` refuses, report the branch as "kept, not provably merged" and do not escalate to `-D`.
- If escalation is ever offered, require stronger evidence and a user confirmation. The strongest evidence is an empty `git merge-tree --write-tree` diff against a freshly fetched `origin/<default>`.
- `[gone]` alone is not enough.
- Never delete the current branch or a branch checked out in a worktree.

## Open questions
- Codex CLI's built-in commit behavior (official docs not found).
- Whether Aider's default really passes `--no-verify` (read from option text, not source).
- OpenHands' current default after issue #10013.
- Star counts for `anthropics/claude-code`, `JanSzewczyk/claude-plugins` and `sneg55/agent-starter`.
- Official-docs confirmation of the `attribution` and `includeGitInstructions` settings.

## Sources
- https://aider.chat/docs/git.html
- https://aider.chat/docs/config/options.html
- https://deepwiki.com/Aider-AI/aider/4.3-git-integration-and-version-control
- https://code.claude.com/docs/en/checkpointing
- https://safeguard.sh/resources/blog/claude-code-checkpoints-rewind-what-it-cannot-undo
- https://github.com/Piebald-AI/claude-code-system-prompts
- https://claudcod.com/blog/claude-code-commits
- https://github.com/anthropics/claude-code/issues/40117
- https://github.com/anthropics/claude-code/issues/14345
- https://microservices.io/post/genaidevelopment/2025/09/10/allow-git-commit-considered-harmful.html
- https://docs.cline.bot/core-workflows/checkpoints
- https://docs.cline.bot/features/multiroot-workspace
- https://github.com/cline/cline/issues/9631
- https://agentskills.so/skills/openhands-skills-gitlab
- https://github.com/OpenHands/OpenHands/issues/10013
- https://github.com/openai/codex/issues/7071
- https://codex.danielvaughan.com/2026/04/25/codex-cli-error-recovery-rollback-patterns-git-safety-nets
- https://forum.cursor.com/t/committing-and-pushing-when-asked-not-to/166598
- https://git-scm.com/docs/git-status
- https://git-scm.com/docs/git-submodule
- https://git-scm.com/docs/git-push
- https://git-scm.com/docs/git-branch
- https://git-scm.com/docs/git-merge-tree
- https://git-scm.com/docs/git-config/2.49.0
- https://git-scm.com/book/en/v2/Git-Tools-Submodules
- https://git-scm.com/book/cs/v2/Git-Tools-Submodules
- https://gist.github.com/gitaarik/8735255
- https://medium.com/@nitishgangwar/git-submodules-the-honest-guide-i-wish-i-had-4995fff74035
- https://github.com/anthropics/claude-plugins-official
- https://github.com/anthropics/claude-plugins-community
- https://giginet.me/claude-plugins-official/plugins/commit-commands/index.html
- https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/plugins/commit-commands/commands/commit.md
- https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/plugins/commit-commands/commands/commit-push-pr.md
- https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/plugins/commit-commands/commands/clean_gone.md
- https://github.com/obra/superpowers
- https://github.com/netresearch/git-workflow-skill
- https://github.com/JanSzewczyk/claude-plugins
- https://github.com/sneg55/agent-starter/blob/main/skills/commit-push-pr/SKILL.md
- https://aiskill.market/blog/best-claude-skills-for-git-workflows-2026
- https://www.conventionalcommits.org/en/v1.0.0/
- https://trunkbaseddevelopment.com/short-lived-feature-branches/
- https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development
- https://docs.github.com/articles/about-protected-branches
- https://dev.to/ticktockbent/stop-letting-agents-code-push-to-main-2kfk
- https://gitdesktop.app/blog/branch-not-fully-merged
- https://www.git-tower.com/blog/how-to-clean-up-merged-feature-branches
- https://news.ycombinator.com/item?id=47088687
- https://chatoverflow.dev/n/squash-merged-branches-never-show-in-git-branch-merged-a1857c4b4125
- https://freenode.net/article/git-may-teach-delete-merged-to-spot-squash-merges
