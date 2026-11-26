---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-makeTheRepoAgree-20261124-221427
version: "1"
priority: High
created_date: "2026-11-24"
---

# Make integration the base branch everywhere master was assumed

Source: ./source.md
Goal: The repo agrees that `integration` is the default and PR base branch (master stays the production branch); a governed launch session can no longer push to `refs/heads/integration`; one small test keeps the four base-branch statements from drifting apart.

## Constraints

- One pull request, base `integration`, branch `fix/default-branch-integration`, opened only through `/sc:pr-submit --monitor 3` against `IronbellyOrg/IronClaude`. Never merge, never touch SuperClaude-Org, no Orca link flags, no model flag, never Opus.
- Edit only `src/superclaude/**`, `tests/**`, `plugins/superclaude/hooks/scripts/launch-level-pre-push.sh` (a committed byte-identical mirror with no generator: `scripts/build_superclaude_plugin.py` writes `dist/` only) and the two root files `CLAUDE.md` and `.github/PULL_REQUEST_TEMPLATE.md`.
- Do not touch `docs/generated`, `docs/testing`, the `/sc:impact` and `/sc:auggie-review` diff examples, release tooling (`/sc:post-release`, `release-procedure.md`), or any text that says master is the production branch. Change no ABSOLUTE RULE wording in `CLAUDE.md` other than branch names.
- Never stage `.claude/` mirrors (only `.claude/settings.json` is tracked); `.dev/tasks` is staged. Commit only on the feature branch with `Co-Authored-By: Claude Code <noreply@anthropic.com>`.
- Follow-ups to list in the PR body, not fix here: the L1 command guard `src/superclaude/hooks/scripts/launch-level-guard.sh` (line 59 text, line 736 `master | main`) still classifies only master and main as PROTECTED (the L2 hook is the backstop); release tooling that assumes master.

## Phase 1: Close the safety gap

## Task 1: Protect refs/heads/integration in the L2 pre-push hook and its mirror

Edit `src/superclaude/hooks/scripts/launch-level-pre-push.sh`: line 17 becomes `L2_PROTECTED=(refs/heads/main refs/heads/master refs/heads/integration)`, the header comment at lines 8-9 names all three refs, and line 2 is bumped to `# launch-level-pre-push-version: 2` (the hook is byte-pinned and the installer replaces an installed hook only when the version line differs, so existing worktrees pick the fix up). Copy the finished file byte-for-byte over `plugins/superclaude/hooks/scripts/launch-level-pre-push.sh` (keep the executable bit). Update the version string `L2_VERSION_LINE` in `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` (line 877) and the pins `L2_VERSION_LINE` and `L2_HOOK_SHA256` in `tests/cli/test_install_hooks.py` (lines 1100-1101, new sha256 of the hook file). In `orca_worktree.py` `_l2_selftest` (loop at line 1363) add `refs/heads/integration` to the refs that must be refused with `L2-UNKNOWN` when the data file is gone.

Acceptance criteria:
- `grep -n L2_PROTECTED src/superclaude/hooks/scripts/launch-level-pre-push.sh plugins/superclaude/hooks/scripts/launch-level-pre-push.sh` shows `refs/heads/integration` in both, and the two files are byte-identical.
- `tests/cli/test_install_hooks.py` (mirror, executable, version-line and sha256-pin tests), `tests/hooks/test_launch_level_pre_push.py::test_t23_hook_sha256_pinned_with_version_line`, `tests/skills/test_issue_l2_install.py` and `tests/skills/test_issue_orca_worktree.py` pass; `tests/hooks/test_launch_job_identity.py` (own protected-ref list, unchanged) still passes.
- After `make sync-dev`, `make verify-sync` passes and no `.claude/` path other than `.claude/settings.json` is staged.

## Task 2: Prove a governed push to integration is refused and a feature-branch push is allowed

Depends on: Task 1

In `tests/hooks/test_launch_level_pre_push.py` (the real L2 hook tests; `tests/hooks/test_launch_level_guard.py` covers the separate L1 command guard and is not edited) change `BRANCHES = ["main", "master"]` (line 49) to include `"integration"` so every parametrized actor and malformed-stream test also covers it, and make sure a governed push to `refs/heads/integration` asserts `protected(...)` while a governed push to a feature branch such as `refs/heads/feature/x` asserts `allowed(...)` (add one small test only if no existing test already pushes a non-protected ref for a governed actor).

Acceptance criteria:
- A governed actor pushing `HEAD:integration` exits non-zero with the `L2-PROTECTED ... refs/heads/integration` line, and a governed actor pushing a feature branch exits 0.
- `uv run pytest tests/hooks -q` passes; reverting line 17 of the hook makes the new integration cases fail.

## Phase 2: Move the defaults

## Task 3: Default the reflect base branch to integration

Edit `src/superclaude/cli/reflect/config.py`: `_DEFAULT_BASE_BRANCH = "integration"` (line 44), rewrite the OQ1 comment above it (lines 40-43, which says the trunk is master and integration must not be hardcoded) to say the default branch is now integration, and fix the docstring mentions of `master` at line 13 of the module and line 281 (`base_branch` argument). No helper that resolves the repository default branch exists (`_resolve_base` only runs `git merge-base HEAD <base_branch>`), so the constant is the single source. The only reader is `resolve_config(... base_branch=_DEFAULT_BASE_BRANCH)` at line 259 feeding `_resolve_base` (line 312); `tests/cli/reflect/test_cli_smoke.py` and `test_base_precedence.py` mock `_git` and do not depend on the value.

Acceptance criteria:
- `grep -n "master" src/superclaude/cli/reflect/config.py` finds no statement that master is the default base.
- `uv run pytest tests/cli/reflect -q` passes.

## Task 4: Update CLAUDE.md and the PR template to integration

Edit the repo-root `CLAUDE.md`: the fallback `gh pr create` at line 67 uses `--base integration`; pre-PR check 2 at line 73 becomes `git fetch origin && git log integration..origin/integration`, "rebase the branch onto `origin/integration`", and "No commits between integration and <branch>" (reword "the fork's master is ahead of the local master" to integration); the worktree example at lines 318-319 uses `--base-branch origin/integration`; the Git Workflow section (lines 290-297) keeps `master` (production) ← `integration` (testing) ← feature branches and gains no new claim, but step 1 and the PR rule must both say feature branches are cut from and PR'd to `integration`. The `/sc:pr-submit --monitor 3` example is left as it is: `~/.claude/commands/sc/pr-submit.md` resolves `--base` from the repo's default branch (`gh repo view ... defaultBranchRef`), which is now `integration`. In `.github/PULL_REQUEST_TEMPLATE.md` line 23 becomes "Branch rebased onto `origin/integration` (no conflicts)." No other ABSOLUTE RULE wording changes.

Acceptance criteria:
- `grep -n "master" CLAUDE.md` leaves only lines that describe master as the production branch or the upstream-fork incident history (the 2026-05-25 PR rationale), none that name master as a PR base or rebase target.
- `uv run pytest tests/core tests/pr_submit -q` passes, including `tests/core/test_claude_md_worktree_rule.py`.

## Phase 3: Keep them agreeing

## Task 5: Add one test that the four base-branch statements agree

Depends on: Task 1, Task 3, Task 4

Add `tests/core/test_default_branch_agreement.py` with one test. It reads the base branch once per source: the fallback `--base <name>` token of the `gh pr create` line in `CLAUDE.md`, the `origin/<name>` in the "Branch rebased onto" line of `.github/PULL_REQUEST_TEMPLATE.md`, `config._DEFAULT_BASE_BRANCH` from `superclaude.cli.reflect.config`, and that `refs/heads/<name>` is in the `L2_PROTECTED=(...)` array of `src/superclaude/hooks/scripts/launch-level-pre-push.sh`. It asserts the first three are equal and the fourth is present, with a message naming the disagreeing file.

Acceptance criteria:
- The test passes on the finished tree and fails (checked by temporarily changing any one of the four sources) when one of them names a different branch.
- Full `uv run pytest` and `make lint` pass (any failure is reported honestly in `.dev/issues/769/default-branch-result.md`), and `git status` shows no staged `.claude/` mirror.
