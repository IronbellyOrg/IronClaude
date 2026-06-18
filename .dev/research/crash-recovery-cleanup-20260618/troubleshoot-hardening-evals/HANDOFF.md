# troubleshoot-hardening-evals handoff

## Current state

- Worktree: `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals`.
- Local branch: `feat/troubleshoot-hardening-evals` at `f210cf16`.
- Git state is clean for tracked files, with exactly 165 untracked files under three artifact roots: `.dev/eval-workspaces/cli-eval/`, `.dev/reflect/post-cli-eval-20260612/`, and `.dev/troubleshoot-meta/`.
- Stash state: `stash@{0}` is lane-specific (`On feat/troubleshoot-hardening-evals: pre-merge-local-changes-before-pr162-master-ff-2026-06-12`). Do not apply or drop it during cleanup unless a human explicitly asks.
- Task file: `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/.dev/tasks/to-do/TASK-RF-troubleshoot-hardening-evals-20260611-160018/TASK-RF-troubleshoot-hardening-evals-20260611-160018.md` is marked `status: "🟢 Done"` with completion date `2026-06-12`.
- Task scope: executable differential backtest/eval harness under `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/tests/troubleshoot/backtest/` for E1-E5, with OLD=MISS real replay green now and NEW=CATCH proxies skip-guarded until sibling hardening refs land.
- Post-reflect for the troubleshoot backtest task is preserved at `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/.dev/reflect/post-troubleshoot-hardening-evals-20260612031044/REPORT.md`; verdict was `pass_with_findings`, status success, confidence 0.81, 0 Drift, 0 Regression.
- Post-reflect noted one authorized expansion (NEW=CATCH skip-guarding, partial-by-design) and one necessary deviation (E4 HEAD-heal recitation corrected to merged heal `acd5631f/#158`, replay base pinned to `1b0264f1`).
- The final backtest validation summary says `uv run pytest tests/troubleshoot/backtest/ -v` was green locally: 38 passed, 11 skipped, 0 failed, 0 errored, with `backtest_status` currently `not_run` because NEW impl refs are absent. The reflect header also records a later/full validation count of 42 passed, 11 skipped, 0 failed plus ruff exit 0.
- Ruff evidence at `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/.dev/tasks/to-do/TASK-RF-troubleshoot-hardening-evals-20260611-160018/phase-outputs/test-results/ruff-backtest-output.txt` reports `ruff check` PASS and `ruff format --check` PASS for `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/tests/troubleshoot/backtest/`.

## PR/branch state

- PR: `https://github.com/IronbellyOrg/IronClaude/pull/168`.
- PR #168 state from `gh pr view 168 --repo IronbellyOrg/IronClaude`: `MERGED`, base `master`, head `feat/troubleshoot-hardening-evals`, head owner `IronbellyOrg`, not draft.
- Remote branch is gone: local branch shows `[origin/feat/troubleshoot-hardening-evals: gone]`.
- PR #168 bundled three commits: `d70b6564` troubleshoot E1-E5 backtest harness, `09f7d487` `/sc:cli-eval` skill, and `f210cf16` reflect remediation for cli-eval.
- Historical PR check rollup displayed failures on initial CI jobs even though PR state is now merged. Treat those as historical PR metadata, not a reason to resurrect the remote branch without a fresh validation pass.
- Local `f210cf16` is not an ancestor of current `origin/master`, but the relevant source/test surfaces compare clean against `origin/master` for `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/tests/troubleshoot/backtest/`, `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/src/superclaude/skills/sc-cli-eval-protocol/`, `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/src/superclaude/commands/cli-eval.md`, the eval agents, eval suites, COMMANDS row, and suites guide. This looks like content landed via non-identical merge/squash history while the local branch stayed behind.
- Do not open a new PR for this branch by default. If cleanup work needs a PR, use a new cleanup branch from current `origin/master` and target the fork with `--repo IronbellyOrg/IronClaude`.

## Validation plan

Use only if a new session wants to re-validate before retiring the worktree or preserving artifacts:

1. Refresh remote state: `git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals fetch origin`.
2. Confirm tracked cleanliness and untracked artifact roots: `git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals status --short --branch`.
3. Confirm PR state read-only: `gh pr view 168 --repo IronbellyOrg/IronClaude --json number,state,url,headRefName,baseRefName,mergeStateStatus,statusCheckRollup`.
4. Confirm code/test surfaces are already in current master: `git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals diff --stat HEAD..origin/master -- tests/troubleshoot/backtest src/superclaude/skills/sc-cli-eval-protocol src/superclaude/commands/cli-eval.md src/superclaude/agents/eval-docs-loader.md src/superclaude/agents/eval-run-reporter.md src/superclaude/agents/eval-suite-author.md src/superclaude/cli/eval/suites docs/eval/suites-guide.md src/superclaude/core/COMMANDS.md`.
5. Re-run focused backtest suite from the worktree if needed: `cd /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals && uv run pytest tests/troubleshoot/backtest/ -v`.
6. Re-run focused lint/format check if needed: `cd /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals && uv run ruff check tests/troubleshoot/backtest/ && uv run ruff format --check tests/troubleshoot/backtest/`.
7. If validating current `origin/master` instead of the stale local branch, run the same pytest/ruff commands in a fresh worktree rooted at current `origin/master`, not by rebasing this retired lane in place.

## Artifact cleanup/preservation plan

- Preserve before deletion. The 165 untracked files are not disposable scratch until explicitly archived or intentionally discarded.
- Highest-value untracked roots:
  - `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/.dev/eval-workspaces/cli-eval/`: skill-creator/eval iteration evidence, benchmark JSON/MD, review HTML, grading outputs, worked example run outputs.
  - `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/.dev/reflect/post-cli-eval-20260612/`: cli-eval post-reflect report, reviewer findings, changed-files artifact.
  - `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/.dev/troubleshoot-meta/`: source research and adversarial/spec-panel artifacts for troubleshoot pipeline hardening, including E1-E5 root-cause/remediation notes and release/spec artifacts.
- Recommended preservation pattern: create a dedicated artifact-preservation branch from current `origin/master`, copy the three untracked roots into an explicit archive location under `.dev/` or the project’s chosen rescue-artifact convention, then commit only that preservation bundle. Do not use this stale feature branch as the base for new cleanup.
- Do not stage `.claude/` paths. This lane’s relevant source-of-truth files are under `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/src/superclaude/` and the backtest files under `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/tests/troubleshoot/backtest/`.
- Do not apply or clear `stash@{0}` during artifact preservation. If the stash is investigated, first inspect it read-only with `git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals stash show --stat stash@{0}`.
- After artifacts are preserved and a human confirms no stash recovery is needed, the worktree can be removed as a retired lane. Until then, keep it intact.

## Risks

- The local branch is stale/history-divergent even though PR #168 is merged and content appears present on `origin/master`; rebasing or pushing it now risks reintroducing obsolete commits or duplicating merged content.
- Untracked artifact roots contain the only local copy of cli-eval iteration evidence and troubleshoot-hardening meta-evidence in this worktree; deleting the worktree without preserving them loses audit context.
- The backtest suite is intentionally partial today: NEW=CATCH remains skip-guarded until sibling implementation refs land, and `backtest_status` remains `not_run`; this is documented as authorized, not a test failure.
- CI shallow clones may skip OLD=MISS real-git replay tests because pre-fix parent commits are absent; local full-history validation is stronger than CI for those specific replay witnesses.
- Historical PR #168 checks showed failures despite merged state. If anyone needs to make new claims about current health, re-run validation on current `origin/master` rather than relying on PR check history.
- There is a lane-specific stash. Applying it into a stale merged branch could create confusing drift; inspect only if a human asks.

## New-session prompt

Continue crash-recovery cleanup for `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals` on branch `feat/troubleshoot-hardening-evals`. First invoke Skill `sc:analyze` with args `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals --focus quality --depth deep --format report`. Then work read-only unless explicitly preserving artifacts: inspect `git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals status --short --branch`, `git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals stash list`, and `gh pr view 168 --repo IronbellyOrg/IronClaude --json number,state,url,headRefName,baseRefName,mergeStateStatus,statusCheckRollup`. Treat PR #168 as merged and the remote branch as gone. Do not apply or clear stashes. Preserve before deleting the 165 untracked files under `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/.dev/eval-workspaces/cli-eval/`, `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/.dev/reflect/post-cli-eval-20260612/`, and `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/.dev/troubleshoot-meta/`. If validating, run `cd /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals && uv run pytest tests/troubleshoot/backtest/ -v` and `cd /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals && uv run ruff check tests/troubleshoot/backtest/ && uv run ruff format --check tests/troubleshoot/backtest/`. If creating a preservation PR, branch from current `origin/master`, target `--repo IronbellyOrg/IronClaude`, and never stage `.claude/` generated files.
