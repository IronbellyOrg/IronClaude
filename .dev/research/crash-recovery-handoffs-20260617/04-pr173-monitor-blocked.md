# PR173 monitor handoff

## Current state

- Target lane inspected: `/config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12` on branch `feat/troubleshoot-pipeline-hardening` at `b9378c72e2d5acc12607316b10ef377110f7c5a3`.
- Git status in the target lane is not clean: `?? .dev/pr-monitor/` is untracked. No source-file modifications were observed.
- The branch tracks `origin/feat/troubleshoot-pipeline-hardening`, but that remote ref is gone.
- Divergence from `origin/master`: `15 1` via `git rev-list --left-right --count origin/master...HEAD` — target is 15 commits behind and has 1 local commit not on current `origin/master`.
- Divergence from local `master`: `13 1`; local `master` itself is behind `origin/master` by 2 commits.
- PR #173 on GitHub is already `MERGED`: `https://github.com/IronbellyOrg/IronClaude/pull/173`, head `feat/troubleshoot-pipeline-hardening`, recorded head SHA `b9378c72e2d5acc12607316b10ef377110f7c5a3`, base `master`.
- `origin/master` contains a squashed/merged equivalent of the PR as `71f16e13 feat(troubleshoot): Pipeline Hardening Closure mode (H0-H5 + waiver latch) (#173)`, plus later PRs #174, #175, #176, and #177.
- The monitor artifact at `/config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12/.dev/pr-monitor/pr-173-augment-remediation-2026-06-12/monitor-run-173.jsonl` has only two relevant events: initial polling for PR #173 and a terminal blocked event.
- The terminal blocked event says the PR head is behind `origin/master` and the approved `pr-submit` monitor scripts/core from `origin/master` are absent on the checked-out PR head, so the monitor cannot be confirmed/executed on that branch until it is rebased.
- Task state for the underlying troubleshoot hardening task is `🟢 Done` in `/config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12/.dev/tasks/to-do/TASK-RF-troubleshoot-hardening-20260611-023739/TASK-RF-troubleshoot-hardening-20260611-023739.md`.
- Validation artifacts in that task report prior local success: `make sync-dev` PASS, `make verify-sync` PASS, markdownlint PASS, and `uv run pytest tests/troubleshoot/ -v` PASS with 18/18 tests.
- Post-reflect report exists at `/config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12/.dev/tasks/to-do/TASK-RF-troubleshoot-hardening-20260611-023739/qa/reflect-post-report.md` and reports `VERDICT: PASS`.
- GitHub check rollup for the PR head still shows old failed checks from 2026-06-12: Quick Test, Python 3.10/3.11/3.12 tests, Lint and Format, Dependency Allow-list, and Test Summary failed; several other checks passed. Because the PR is merged, treat those as stale historical PR-head signals unless resurrecting the branch.
- Targeted `.dev` search found no additional PR #173-specific workflow/session log beyond the monitor artifact and task QA artifacts.

## Blocker root cause

The blocker was operational, not a code-change blocker in the troubleshoot hardening implementation:

1. The checked-out target branch predates the PR-submit monitor protocol. `git diff HEAD..origin/master` shows `origin/master` adds `src/superclaude/commands/pr-submit.md`, `src/superclaude/skills/sc-pr-submit-protocol/**`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/*.sh`, and `tests/pr_submit/**`.
2. The monitor was asked to run against PR #173 from the stale PR head `b9378c72e2d5acc12607316b10ef377110f7c5a3`, but the monitor machinery it needed only exists later on `origin/master` from the PR-submit work (#174/#176/#177).
3. The branch’s remote tracking ref is gone, and PR #173 is now merged. The local branch commit is a stale pre-merge/squash head, while `origin/master` contains the accepted PR content at merge commit/squash `71f16e13` plus later additions.
4. A rebase of this stale branch onto `origin/master` would likely be semantically unnecessary for PR #173 itself and may produce duplicate or confusing history unless the user explicitly wants to resurrect the branch for new follow-up work.

Duplicate-worktree relation:

- `/config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12` and `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening` are both registered worktrees for `feat/troubleshoot-pipeline-hardening` at the same SHA `b9378c72e2d5acc12607316b10ef377110f7c5a3`.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening` is the repo root cited by the post-reflect report, so it appears to be the canonical execution worktree for the original implementation.
- The target lane under `.claude/worktrees` contains the untracked PR monitor artifact. The `.dev/worktrees/troubleshoot-hardening` lane did not show the untracked monitor artifact in the status check.
- Because both worktrees point at the same local branch, rebasing or resetting the branch in either path changes the branch reference seen by both. Do not mutate either lane until a new session chooses one canonical path.

## Safe rebase/validation sequence

Recommended default: do not rebase for PR #173 recovery, because PR #173 is already merged. If the goal is only crash recovery and cleanup, skip to the cleanup plan.

If the user explicitly wants to continue the stale branch for new follow-up work, use one canonical worktree only, preferably `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening`, and first preserve the untracked monitor artifact from the `.claude/worktrees` copy.

Safe read-only preflight commands:

```bash
git -C /config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12 status --short --branch
```

```bash
git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening status --short --branch
```

```bash
git -C /config/workspace/IronClaude worktree list --porcelain
```

```bash
git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening remote -v
```

```bash
git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening fetch origin
```

```bash
git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening rev-list --left-right --count origin/master...HEAD
```

```bash
gh pr view 173 --repo IronbellyOrg/IronClaude --json number,state,isDraft,title,headRefName,headRefOid,baseRefName,url,mergeStateStatus,statusCheckRollup
```

Only if continuing the branch, after confirming the PR is not the desired terminal state:

```bash
git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening rebase origin/master
```

After any rebase, validate from the same canonical worktree:

```bash
make -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening sync-dev
```

```bash
make -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening verify-sync
```

```bash
uv run --directory /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening pytest tests/troubleshoot/ -v
```

```bash
uv run --directory /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening pytest tests/troubleshoot/backtest/ -v
```

```bash
uv run --directory /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening ruff format --check src/ tests/
```

```bash
make -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening lint
```

If a PR action is needed for a new follow-up branch, always target the fork explicitly:

```bash
gh pr view 173 --repo IronbellyOrg/IronClaude
```

```bash
gh pr create --repo IronbellyOrg/IronClaude --base master --head feat/troubleshoot-pipeline-hardening --title "feat(troubleshoot): follow-up pipeline hardening" --body "Follow-up from PR #173 crash-recovery handoff."
```

Do not run a bare `gh pr create`; this repo is a fork and PR commands must use `--repo IronbellyOrg/IronClaude`.

## Cleanup plan

1. Treat PR #173 as landed unless the user states otherwise. Confirm with `gh pr view 173 --repo IronbellyOrg/IronClaude --json state,url,headRefOid,baseRefName`.
2. Preserve the monitor artifact before deleting any worktree: `/config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12/.dev/pr-monitor/pr-173-augment-remediation-2026-06-12/monitor-run-173.jsonl`.
3. Choose one canonical retained worktree if follow-up work is needed. Prefer `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening` because the task’s post-reflect report references it as the implementation root.
4. If no follow-up work is needed, remove the duplicate/stale worktrees only after user approval. Do not clean automatically in this handoff lane.
5. If cleanup proceeds, remove the `.claude/worktrees/wf_3cd03e8d-30a-12` lane first after preserving the monitor artifact, because its only unique observed content is the untracked `.dev/pr-monitor/` directory.
6. Do not stage `.claude/` mirrors. Source-of-truth changes belong under `src/superclaude/`; `.claude/{skills,commands,agents,hooks,templates}` is sync-dev output.
7. If retaining branch history for audit, consider tagging or archiving the SHA before cleanup rather than rebasing the stale local branch.

## Risks/ambiguities

- PR #173 is merged, but the local branch still has one unique pre-merge/squash commit not on `origin/master`. Rebasing may create duplicate semantic changes rather than a useful branch.
- `origin/master` now includes later troubleshoot backtest files under `tests/troubleshoot/backtest/**`. The stale local branch lacks them; `git diff HEAD..origin/master` shows these as additions from the target branch’s perspective.
- The monitor artifact is untracked. A worktree removal or clean operation would delete it unless it is copied or otherwise preserved first.
- Two registered worktrees point to the same branch and SHA. Mutating the branch reference from one path affects both; avoid parallel branch operations.
- Historical GitHub checks on PR #173 failed even though the PR later merged. A new session should not infer current failure from old PR-head checks without rerunning validation on current `origin/master` or a rebased branch.
- The PR-submit monitor protocol was missing on the stale PR head by design; it exists on `origin/master`. Do not attempt to run the approved monitor from the stale head before rebasing or switching to a branch that contains `src/superclaude/skills/sc-pr-submit-protocol/**`.
- Local `master` is behind `origin/master`; use `origin/master` for comparisons and rebase targets, not local `master`.

## New-session prompt

Paste this into a fresh session if follow-up is needed:

```text
Continue PR #173 crash-recovery from /config/workspace/IronClaude/.dev/research/crash-recovery-handoffs-20260617/04-pr173-monitor-blocked.md. Use safe read-only inspection first. Target lane is /config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12; duplicate canonical implementation lane is /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening. PR #173 is merged on IronbellyOrg/IronClaude, but the local feat/troubleshoot-pipeline-hardening branch is stale: origin/feat/troubleshoot-pipeline-hardening is gone, HEAD is b9378c72e2d5acc12607316b10ef377110f7c5a3, and origin/master is 15 commits ahead with the pr-submit monitor protocol. Do not rebase, push, clean, or remove worktrees without explicit approval. First run: git -C /config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12 status --short --branch; git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening status --short --branch; git -C /config/workspace/IronClaude worktree list --porcelain; gh pr view 173 --repo IronbellyOrg/IronClaude --json number,state,url,headRefName,headRefOid,baseRefName,statusCheckRollup. Preserve /config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12/.dev/pr-monitor/pr-173-augment-remediation-2026-06-12/monitor-run-173.jsonl before any cleanup. If the user asks to resurrect the branch, use /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening as the canonical worktree, fetch origin, rebase only after approval, then validate with make -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening sync-dev; make -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening verify-sync; uv run --directory /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening pytest tests/troubleshoot/ -v; uv run --directory /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening pytest tests/troubleshoot/backtest/ -v; uv run --directory /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening ruff format --check src/ tests/; make -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening lint. Any PR command must use --repo IronbellyOrg/IronClaude.
```
