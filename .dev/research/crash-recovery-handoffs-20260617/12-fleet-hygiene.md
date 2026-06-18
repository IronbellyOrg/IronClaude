# Fleet hygiene handoff

## Inventory

Scope: repository-wide fleet hygiene after the crash-recovery lanes finish. This is a sequencing handoff only; no cleanup, deletion, staging, stash operation, or branch mutation was performed while writing it.

Current registered worktrees from `git -C /config/workspace/IronClaude worktree list --porcelain`:

| Worktree | Branch | Observed hygiene state |
|---|---|---|
| `/config/workspace/IronClaude` | `fix/pr-submit-defaults-monitor-timeout` | Root branch is clean except untracked registered worktree directories under `/config/workspace/IronClaude/.dev/worktrees/`. Treat those directories as live worktrees, not loose trash. |
| `/config/workspace/IronClaude/.claude/worktrees/SprintReRun` | `feat/sprint-auto-resume-v435` | Upstream is gone. Contains untracked `.dev/reflect`, `.dev/releases`, and `.dev/tasks/done` artifacts. |
| `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028` | `fix/swarm-normalize-perworker-status-fr028` | Clean. |
| `/config/workspace/IronClaude/.claude/worktrees/mastra-research` | `worktree-mastra-research` | Clean. |
| `/config/workspace/IronClaude/.claude/worktrees/mms-m8m9` | `feat/sc-bare-review-m8m9-migration` | Dirty: modified `.dev/eval-workspaces/prd-test-product` logs and `.dev/releases/current/cliEval/evidence/T02.15/perf.json`; multiple untracked reflect, release, task, and troubleshoot artifacts. |
| `/config/workspace/IronClaude/.claude/worktrees/sc-cli-eval` | `feat/sc-cli-eval` | Tracks `origin/master` and is behind. No local dirty files observed. |
| `/config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12` | `feat/troubleshoot-pipeline-hardening` | Upstream is gone. Contains untracked `.dev/pr-monitor/pr-173-augment-remediation-2026-06-12/monitor-run-173.jsonl`. |
| `/config/workspace/IronClaude/.dev/worktrees/SprintRun429` | `SprintRun429` | Active dirty implementation lane: modified sprint CLI/test files, new `src/superclaude/cli/sprint/recovery_policy.py`, new sprint exhaustion fixtures/tests, and untracked task/research artifacts. |
| `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2` | `fix/cli-eval-v2` | Tracks `origin/master` and is behind. Contains untracked brainstorm and cli-eval handoff artifacts. |
| `/config/workspace/IronClaude/.dev/worktrees/fix-sprint-rerun-pass-recovered` | `fix/sprint-rerun-pass-recovered` | Upstream is gone. No local dirty files observed. |
| `/config/workspace/IronClaude/.dev/worktrees/reflect-pass-recovered-artifacts` | `chore/reflect-pass-recovered-artifacts` | Upstream is gone. No local dirty files observed. |
| `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend` | `feat/tfep-troubleshoot-backend` | Contains untracked review artifacts under `.dev/reviews/pr-180-20260617-1250/`. |
| `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening` | `feat/troubleshoot-pipeline-hardening` | Same branch name as `/config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12`; upstream is gone. No local dirty files observed. |
| `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals` | `feat/troubleshoot-hardening-evals` | Upstream is gone. Large untracked `.dev/eval-workspaces/cli-eval`, `.dev/reflect`, and `.dev/troubleshoot-meta` artifact set. |

Additional fleet signals:

- No registered worktree reported an in-progress merge or rebase when checked via each worktree's `git rev-parse --git-dir` state directory.
- Branch registration check showed `refs/heads/feat/troubleshoot-pipeline-hardening` in two registered worktrees: `/config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12` and `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening`. Treat this as a duplicate-lane risk until a human confirms which copy is canonical.
- Repo-level stash list currently contains five stashes: `stash@{0}` on `feat/troubleshoot-hardening-evals`, `stash@{1}` on `docs/sc-reflect-surface-sync`, `stash@{2}` on detached/no-branch state, `stash@{3}` on `fix/prd-build-task-file-glob`, and `stash@{4}` on `fix/pr66-eval-run-nameerror-and-scratch-root-tautology`. One stash stat was very large; do not infer ownership from the current branch.
- `/config/workspace/IronClaude/.dev/tasks/to-do` contains many tasks whose own status fields say done/completed, including `TASK-MULTIMODELSWARM-AUDIT-REMEDIATION-20260531`, `TASK-PR111-HISTORY-SURGERY-20260602`, `TASK-RESEARCH-20260602-211124`, many `TASK-RF-20260602*` through `TASK-RF-20260608*` entries, `TASK-RF-troubleshoot-hardening-20260611-023739`, and `TASK-RF-troubleshoot-hardening-evals-20260611-160018`. This is a separate hygiene lane from worktree cleanup: move only after task owners confirm completion and artifact retention needs.
- `/config/workspace/IronClaude/.dev/README.md` says iteration artifacts belong under `/config/workspace/IronClaude/.dev/`, and `.claude/skills/<skill>-workspace/` style outputs should be redirected to `.dev/eval-workspaces/<skill-name>/`.
- `/config/workspace/IronClaude/docs/dev/sync-discipline.md` and `/config/workspace/IronClaude/CLAUDE.md` both make `src/superclaude/` the source of truth and `.claude/` a generated mirror except `/config/workspace/IronClaude/.claude/settings.json`.

## Cleanup sequencing

1. Freeze the fleet first: ask every lane owner to stop writing and record their lane disposition. Do not perform repo-wide cleanup while active agents still have dirty worktrees.
2. Re-run read-only inventory commands from the root and from every registered worktree. Capture worktree list, root status, per-worktree status, merge/rebase state, branch tracking, and stash list before changing anything.
3. Classify each worktree into one of four buckets: active lane to preserve, clean stale lane, dirty artifact-only lane, or dirty source-code lane.
4. For dirty source-code lanes, require the lane owner to either commit/PR from that worktree or produce an explicit abandon/discard instruction. Do not remove the worktree just because its upstream is gone.
5. For dirty artifact-only lanes, copy or move approved artifacts only to canonical `.dev/` destinations after the owner confirms they are needed. Keep `.dev/eval-workspaces/<skill-name>/`, `.dev/research/`, `.dev/tasks/`, `.dev/releases/`, and `.dev/reviews/` conventions from `/config/workspace/IronClaude/.dev/README.md`.
6. Resolve duplicate branch occupancy before deleting anything. The `feat/troubleshoot-pipeline-hardening` duplicate must be human-resolved by choosing the canonical path and comparing any untracked artifacts in both `/config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12` and `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening`.
7. Only after owner signoff and artifact preservation, remove stale clean worktrees with `git -C /config/workspace/IronClaude worktree remove <absolute-worktree-path>`. Use `git -C /config/workspace/IronClaude worktree prune` only after removals and after confirming no expected worktree is missing.
8. Clean stale local branches only after their worktrees are removed and after checking whether a PR, remote branch, or local-only recovery value remains. Branches with `[gone]` are candidates, not automatic deletions.
9. Triage `/config/workspace/IronClaude/.dev/tasks/to-do` separately. For each task whose own status says done/completed, move to `/config/workspace/IronClaude/.dev/tasks/done/` only when no active worktree or handoff still references it as in-flight.
10. Run source-of-truth sync validation last. For any skill/command/agent/hook/template changes, the only valid path is edit `src/superclaude/`, run `make sync-dev`, then `make verify-sync`, and stage only the `src/` side.

## Do-not-do rules

- Never stage `.claude/` mirrors. The only tracked exception under `.claude/` is `/config/workspace/IronClaude/.claude/settings.json`; never use `git add -f` on `.claude/skills`, `.claude/commands`, `.claude/agents`, `.claude/hooks`, or `.claude/templates`.
- Never apply, pop, drop, or clear stashes blindly. Repo stashes are shared across lanes and may belong to other recovery work; `git stash clear` is especially forbidden.
- Never run `git stash` during an in-progress merge. In worktrees, `.git` is a file and merge state lives under `$(git rev-parse --git-dir)`, not `.git/MERGE_HEAD`.
- Never delete a registered worktree directory with filesystem deletion. Use `git worktree remove` only after owner signoff and after preserving required artifacts.
- Never treat untracked `/config/workspace/IronClaude/.dev/worktrees/*` entries in the root status as ordinary untracked folders. They are registered worktrees.
- Never clean `.dev/` globally with broad deletion. `.dev/` is the canonical place for research, eval, review, release, and task artifacts.
- Never rebase/reset shared active worktrees to make cleanup easier. Parallel sessions can share index/HEAD within a worktree; isolate cleanup in its own worktree if commit operations are needed.
- Never create PRs without `--repo IronbellyOrg/IronClaude` if cleanup work later requires a PR.

## Validation commands

All commands below are read-only except where the command name itself is explicitly a later cleanup action; run validation first and require human approval before any cleanup action.

- `git -C /config/workspace/IronClaude worktree list --porcelain`
- `git -C /config/workspace/IronClaude status --short --branch --untracked-files=all`
- `git -C /config/workspace/IronClaude stash list`
- `for wt in $(git -C /config/workspace/IronClaude worktree list --porcelain | grep '^worktree ' | cut -d' ' -f2-); do printf '\n### %s\n' "$wt"; git -C "$wt" status --short --branch --untracked-files=all; done`
- `for wt in $(git -C /config/workspace/IronClaude worktree list --porcelain | grep '^worktree ' | cut -d' ' -f2-); do gd=$(git -C "$wt" rev-parse --git-dir); printf '%s ' "$wt"; if [ -f "$gd/MERGE_HEAD" ]; then printf 'MERGE_HEAD '; fi; if [ -d "$gd/rebase-merge" ] || [ -d "$gd/rebase-apply" ]; then printf 'REBASE '; fi; printf '\n'; done`
- `git -C /config/workspace/IronClaude worktree list --porcelain | grep '^branch ' | cut -d' ' -f2- | sort | uniq -c | sort -nr`
- `git -C /config/workspace/IronClaude branch --format='%(refname:short) %(upstream:short) %(upstream:track)' | sort`
- `for d in /config/workspace/IronClaude/.dev/tasks/to-do/*; do [ -d "$d" ] || continue; f="$d/$(basename "$d").md"; [ -f "$f" ] || f=$(find "$d" -maxdepth 1 -type f -name '*.md' | sort | head -n 1); status=$(grep -im1 '^status:' "$f" 2>/dev/null | cut -d: -f2- | xargs); printf '%s | %s\n' "$(basename "$d")" "${status:-no-status-found}"; done | sort`
- `make -C /config/workspace/IronClaude verify-sync`
- `uv run --directory /config/workspace/IronClaude ruff format --check src/ tests/`
- `make -C /config/workspace/IronClaude lint`

## Risks

- Stash risk is the highest destructive-risk item: stashes are repo-level, not lane-local in practical cleanup workflows. Applying the wrong stash can mix unrelated historical work into the current lane; clearing stashes can destroy other owners' recovery points.
- Duplicate branch/worktree occupancy can cause a cleanup agent to preserve the wrong copy or delete the only copy with an untracked artifact. The `feat/troubleshoot-pipeline-hardening` duplicate must be adjudicated before removal.
- `.claude/` mirror drift can look like useful work but is generated output. Committing it creates source-of-truth drift and violates repository rules.
- Root status makes registered `.dev/worktrees/*` paths look like ordinary untracked directories because the worktrees live inside the repository tree. Filesystem deletion would bypass git worktree metadata and can strand registrations.
- Many completed tasks remain in `/config/workspace/IronClaude/.dev/tasks/to-do`; bulk moves can break recovery handoffs if a lane still references those paths.
- Worktrees with upstream `[gone]` may still contain local-only commits or untracked artifacts. `[gone]` is cleanup evidence, not deletion authorization.
- Large untracked `.dev/eval-workspaces` and `.dev/troubleshoot-meta` trees may be expensive but can be evidence for eval or reflection lanes; preserve or archive only with owner confirmation.

## New-session prompt for a cleanup-only agent

Use this prompt only after all crash-recovery lane owners have declared their lanes done or abandoned:

`You are a cleanup-only agent in /config/workspace/IronClaude. Read /config/workspace/IronClaude/.dev/research/crash-recovery-handoffs-20260617/12-fleet-hygiene.md, then perform a read-only re-inventory of worktrees, per-worktree statuses, merge/rebase state, branch tracking, stashes, and /config/workspace/IronClaude/.dev/tasks/to-do statuses. Do not delete, move, stash, stage, reset, rebase, or commit. Produce a proposed cleanup plan with owner-confirmation checkpoints. Explicitly preserve source-of-truth rules: never stage .claude mirrors, never git add -f .claude paths, never apply/pop/drop/clear stashes blindly, and treat /config/workspace/IronClaude/.dev/worktrees/* as registered worktrees until git worktree list proves otherwise.`
