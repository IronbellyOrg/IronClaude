d729e5d2cd050384298ecc6b4cf02eb3e376f05f
Review one task for spec compliance.

Task brief: ## Task 4: Update CLAUDE.md and the PR template to integration

Edit the repo-root `CLAUDE.md`: the fallback `gh pr create` at line 67 uses `--base integration`; pre-PR check 2 at line 73 becomes `git fetch origin && git log integration..origin/integration`, "rebase the branch onto `origin/integration`", and "No commits between integration and <branch>" (reword "the fork's master is ahead of the local master" to integration); the worktree example at lines 318-319 uses `--base-branch origin/integration`; the Git Workflow section (lines 290-297) keeps `master` (production) ← `integration` (testing) ← feature branches and gains no new claim, but step 1 and the PR rule must both say feature branches are cut from and PR'd to `integration`. The `/sc:pr-submit --monitor 3` example is left as it is: `~/.claude/commands/sc/pr-submit.md` resolves `--base` from the repo's default branch (`gh repo view ... defaultBranchRef`), which is now `integration`. In `.github/PULL_REQUEST_TEMPLATE.md` line 23 becomes "Branch rebased onto `origin/integration` (no conflicts)." No other ABSOLUTE RULE wording changes.

Acceptance criteria (ids):
T4.AC1: `grep -n "master" CLAUDE.md` leaves only lines that describe master as the production branch or the upstream-fork incident history (the 2026-05-25 PR rationale), none that name master as a PR base or rebase target.
T4.AC2: `uv run pytest tests/core tests/pr_submit -q` passes, including `tests/core/test_claude_md_worktree_rule.py`.
Global constraints: - One pull request, base `integration`, branch `fix/default-branch-integration`, opened only through `/sc:pr-submit --monitor 3` against `IronbellyOrg/IronClaude`. Never merge, never touch SuperClaude-Org, no Orca link flags, no model flag, never Opus.
- Edit only `src/superclaude/**`, `tests/**`, `plugins/superclaude/hooks/scripts/launch-level-pre-push.sh` (a committed byte-identical mirror with no generator: `scripts/build_superclaude_plugin.py` writes `dist/` only) and the two root files `CLAUDE.md` and `.github/PULL_REQUEST_TEMPLATE.md`.
- Do not touch `docs/generated`, `docs/testing`, the `/sc:impact` and `/sc:auggie-review` diff examples, release tooling (`/sc:post-release`, `release-procedure.md`), or any text that says master is the production branch. Change no ABSOLUTE RULE wording in `CLAUDE.md` other than branch names.
- Never stage `.claude/` mirrors (only `.claude/settings.json` is tracked); `.dev/tasks` is staged. Commit only on the feature branch with `Co-Authored-By: Claude Code <noreply@anthropic.com>`.
- Follow-ups to list in the PR body, not fix here: the L1 command guard `src/superclaude/hooks/scripts/launch-level-guard.sh` (line 59 text, line 736 `master | main`) still classifies only master and main as PROTECTED (the L2 hook is the backstop); release tooling that assumes master.
Start sha: d729e5d2cd050384298ecc6b4cf02eb3e376f05f
Diff against the start snapshot: diff --git a/.github/PULL_REQUEST_TEMPLATE.md b/.github/PULL_REQUEST_TEMPLATE.md
index f865337b7..877abde53 100644
--- a/.github/PULL_REQUEST_TEMPLATE.md
+++ b/.github/PULL_REQUEST_TEMPLATE.md
@@ -20,7 +20,7 @@ Closes #
 
 - [ ] Opened with `/sc:pr-submit --monitor 3` on `IronbellyOrg/IronClaude` (fallback: `gh pr create --repo IronbellyOrg/IronClaude`).
 - [ ] For collaborators: Used a topic branch (not directly committed to main).
-- [ ] Branch rebased onto `origin/master` (no conflicts).
+- [ ] Branch rebased onto `origin/integration` (no conflicts).
 - [ ] Commit messages conform to Conventional Commits (`feat:`, `fix:`, `docs:`, etc.).
 
 ### Code Quality
diff --git a/CLAUDE.md b/CLAUDE.md
index ffb28a9b8..4c3a233e0 100644
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -64,13 +64,13 @@ This repository is a **fork**. This clone has only one remote, `origin` = `Ironb
 **Fallback only, when `/sc:pr-submit` cannot run:**
 
 ```bash
-gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch> --title "..." --body "..."
+gh pr create --repo IronbellyOrg/IronClaude --base integration --head <branch> --title "..." --body "..."
 ```
 
 **Pre-PR checks (mandatory):**
 
 1. `git remote get-url origin` must print the `IronbellyOrg/IronClaude` URL, and `gh repo view IronbellyOrg/IronClaude --json nameWithOwner -q .nameWithOwner` must print `IronbellyOrg/IronClaude`. If gh's default repo is wrong, run `gh repo set-default IronbellyOrg/IronClaude`.
-2. `git fetch origin && git log master..origin/master` — if the fork's master is ahead of the local master, **rebase the branch onto `origin/master`** before pushing. The fork has additional commits (e.g., `.claude/` untrack, lint cleanup) that the local clone may not have. Without rebasing, the PR creation will fail with "No commits between master and <branch>".
+2. `git fetch origin && git log integration..origin/integration` — if the fork's integration is ahead of the local integration, **rebase the branch onto `origin/integration`** before pushing. The fork has additional commits (e.g., `.claude/` untrack, lint cleanup) that the local clone may not have. Without rebasing, the PR creation will fail with "No commits between integration and <branch>".
 3. After PR creation, **verify the returned URL points at `https://github.com/IronbellyOrg/IronClaude/pull/N`**. If it points at `SuperClaude-Org`, stop, report the URL to the user, and take no action on that PR; the user closes it. This matches `/sc:pr-submit`, which already halts on a misrouted URL.
 
 **There are no exceptions.**
@@ -291,7 +291,7 @@ def test_with_budget(token_budget):
 
 **Standard workflow**:
 
-1. Create branch from `integration`: `git checkout -b feature/your-feature`
+1. Create branch from `integration` (pull requests are opened against it): `git checkout -b feature/your-feature`
 2. Develop with tests: `uv run pytest`
 3. Commit: `git commit -m "feat: description"` (conventional commits)
 4. Merge to `integration` → validate → merge to `master`
@@ -315,8 +315,8 @@ worktree location, outside the main checkout; `orca worktree current --json` (fr
 - **Existing checkouts under the retired `.dev/worktrees/` location** may stay until their branch is merged, then are removed with `git worktree remove <path>`; no new checkout may be created there.
 
 ```bash
-# Create a worktree named pm-agent, based on origin/master, with an agent in it
-orca worktree create --name pm-agent --base-branch origin/master --agent claude --prompt "<task>"
+# Create a worktree named pm-agent, based on origin/integration, with an agent in it
+orca worktree create --name pm-agent --base-branch origin/integration --agent claude --prompt "<task>"
 
 # Show where Orca put it
 orca worktree list

Codegraph context
index_state: absent
checked_at: n/a
worktree_root: /home/coder/workspaces/worktrees/IronClaude/fix-default-branch-integration
projectPath: n/a
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep/Read floor.

Delta diff from the previous reviewed tree (empty on the first review): diff --git a/CLAUDE.md b/CLAUDE.md
index 2a4fe01f8..4c3a233e0 100644
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -289,11 +289,9 @@ def test_with_budget(token_budget):
 
 **Branch structure**: `master` (production) ← `integration` (testing) ← `feature/*`, `fix/*`, `docs/*`
 
-`integration` is the repository default branch (since 2026-11-24): feature branches are cut from it and pull requests are opened against it. `master` stays the production branch.
-
 **Standard workflow**:
 
-1. Create branch from `integration`: `git checkout -b feature/your-feature`
+1. Create branch from `integration` (pull requests are opened against it): `git checkout -b feature/your-feature`
 2. Develop with tests: `uv run pytest`
 3. Commit: `git commit -m "feat: description"` (conventional commits)
 4. Merge to `integration` → validate → merge to `master`

Earlier blocking findings of this start (empty on the first review): F1.1 ac=scope at=CLAUDE.md:292 anchor="keeps `master` (production) ← `integration` (testing) ← feature branches and gains no new claim" chk=amiss:n,false:n,harm:n,constraint:y family=new-claim fix=remove the added paragraph; say it in step 1: added dated default-branch paragraph is a new claim the task forbids

Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
