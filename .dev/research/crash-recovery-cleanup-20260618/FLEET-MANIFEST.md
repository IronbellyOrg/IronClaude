# Fleet Cleanup Manifest

Generated for crash-recovery cleanup coordination on 2026-06-18.

Scope constraints followed while preparing this manifest:

- No worktrees were removed.
- No source files were edited.
- No files were staged or committed.
- No stashes were touched.
- Only this manifest was written: `/config/workspace/IronClaude/.dev/research/crash-recovery-cleanup-20260618/FLEET-MANIFEST.md`.

## Inputs

- Handoff: `/config/workspace/IronClaude/.dev/research/crash-recovery-handoffs-20260617/12-fleet-hygiene.md`
- Repository root: `/config/workspace/IronClaude`

## Root inventory

### `git -C /config/workspace/IronClaude worktree list --porcelain`

```text
worktree /config/workspace/IronClaude
HEAD 300c06a6d53287893a446db8e859f5f1bc5434d8
branch refs/heads/master

worktree /config/workspace/IronClaude/.claude/worktrees/SprintReRun
HEAD aedd01040f8d80f225323103e201e8605d124840
branch refs/heads/feat/sprint-auto-resume-v435

worktree /config/workspace/IronClaude/.claude/worktrees/fr028-fr028
HEAD d2ad3cbd556f93f2ff9aeef208b9c6d6a9f496d6
branch refs/heads/fix/swarm-normalize-perworker-status-fr028

worktree /config/workspace/IronClaude/.claude/worktrees/mastra-research
HEAD 4e749f1ecff99ca818e53415ba967bcb0dc683b9
branch refs/heads/worktree-mastra-research

worktree /config/workspace/IronClaude/.claude/worktrees/mms-m8m9
HEAD adafd61dc0ad96fb34359227daca629c22f5e44a
branch refs/heads/feat/sc-bare-review-m8m9-migration

worktree /config/workspace/IronClaude/.claude/worktrees/sc-cli-eval
HEAD 8cefefdee026346b4d6dd804d142513096b05b5e
branch refs/heads/feat/sc-cli-eval

worktree /config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12
HEAD b9378c72e2d5acc12607316b10ef377110f7c5a3
branch refs/heads/feat/troubleshoot-pipeline-hardening

worktree /config/workspace/IronClaude/.dev/worktrees/SprintRun429
HEAD d33a52ea95a3aa58a0c160d7da46a9f6c8dceeb1
branch refs/heads/SprintRun429

worktree /config/workspace/IronClaude/.dev/worktrees/cli-eval-v2
HEAD 02582ca03ea5a974f4dbab35d9b9cd0033217aca
branch refs/heads/fix/cli-eval-v2

worktree /config/workspace/IronClaude/.dev/worktrees/fix-sprint-rerun-pass-recovered
HEAD 8e23880edabde89fc8311fd5fe06a2df67ca4bd8
branch refs/heads/fix/sprint-rerun-pass-recovered

worktree /config/workspace/IronClaude/.dev/worktrees/reflect-pass-recovered-artifacts
HEAD 0e813c33951920eae8e071810296182aed595d05
branch refs/heads/chore/reflect-pass-recovered-artifacts

worktree /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend
HEAD c8363739ce8f634ab3c65862a96428dd6b0d6d66
branch refs/heads/feat/tfep-troubleshoot-backend

worktree /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening
HEAD b9378c72e2d5acc12607316b10ef377110f7c5a3
branch refs/heads/feat/troubleshoot-pipeline-hardening

worktree /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals
HEAD f210cf16d2f2c09c42d1a399a364686ba7779e6f
branch refs/heads/feat/troubleshoot-hardening-evals
```

### `git -C /config/workspace/IronClaude status --short --branch`

```text
## master...origin/master [behind 3]
?? .dev/research/crash-recovery-handoffs-20260617/
?? .dev/worktrees/
```

Notes:

- The current root worktree is on `master`, behind `origin/master` by 3 commits.
- Root has untracked `.dev/research/crash-recovery-handoffs-20260617/` and `.dev/worktrees/` entries.
- The `.dev/worktrees/` entry contains registered worktrees and must not be treated as loose trash.

### `git -C /config/workspace/IronClaude stash list`

```text
stash@{0}: On feat/troubleshoot-hardening-evals: pre-merge-local-changes-before-pr162-master-ff-2026-06-12
stash@{1}: WIP on docs/sc-reflect-surface-sync: 1a00efb2 Roadmap pipeline brittleness-elimination (R0 bridge + R1 substrate rewrite) (#112)
stash@{2}: WIP on (no branch): 861047c2 fix(roadmap): honor M{n}-D{nn} milestone-prefixed IDs in tokenizer + canonicalizer
stash@{3}: On fix/prd-build-task-file-glob: in-progress drift before test_is_wrong follow-up
stash@{4}: On fix/pr66-eval-run-nameerror-and-scratch-root-tautology: pre-existing perf.json drift, restored after rebase
```

Stash rule: leave all stashes untouched unless the user gives a specific, stash-targeted instruction.

## Handoff-derived lane status summary

The prior handoff classified the fleet as follows. Treat these as cleanup inputs, not automatic deletion authorization.

| Worktree | Branch | Handoff status | Cleanup posture |
|---|---|---|---|
| `/config/workspace/IronClaude` | previously observed as `fix/pr-submit-defaults-monitor-timeout`; now inventoried as `master` | Root has untracked `.dev/worktrees/` and handoff artifacts | Preserve root; do not clean `.dev/worktrees/` as ordinary untracked files. |
| `/config/workspace/IronClaude/.claude/worktrees/SprintReRun` | `feat/sprint-auto-resume-v435` | Upstream gone; untracked `.dev/reflect`, `.dev/releases`, `.dev/tasks/done` artifacts | Closed/stale candidate only after artifact archive/manifest and owner signoff. |
| `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028` | `fix/swarm-normalize-perworker-status-fr028` | Clean | Closed clean candidate after owner signoff. |
| `/config/workspace/IronClaude/.claude/worktrees/mastra-research` | `worktree-mastra-research` | Clean | Closed clean candidate after owner signoff. |
| `/config/workspace/IronClaude/.claude/worktrees/mms-m8m9` | `feat/sc-bare-review-m8m9-migration` | Dirty: modified eval/release artifacts and many untracked artifacts | Block removal until dirty artifacts are archived or explicitly abandoned. |
| `/config/workspace/IronClaude/.claude/worktrees/sc-cli-eval` | `feat/sc-cli-eval` | Tracks `origin/master`, behind, no local dirty files observed | Likely superseded by v-next lane; confirm before removal. |
| `/config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12` | `feat/troubleshoot-pipeline-hardening` | Upstream gone; untracked PR monitor artifact | Duplicate branch occupancy risk; resolve against `.dev/worktrees/troubleshoot-hardening` before removal. |
| `/config/workspace/IronClaude/.dev/worktrees/SprintRun429` | `SprintRun429` | Active dirty implementation lane | Preserve. Do not remove. |
| `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2` | `fix/cli-eval-v2` | Tracks `origin/master`, behind; untracked brainstorm and cli-eval handoff artifacts | Active cliEval v-next lane should remain. Do not remove unless user explicitly closes it. |
| `/config/workspace/IronClaude/.dev/worktrees/fix-sprint-rerun-pass-recovered` | `fix/sprint-rerun-pass-recovered` | Upstream gone; no local dirty files observed | Closed clean candidate after owner signoff. |
| `/config/workspace/IronClaude/.dev/worktrees/reflect-pass-recovered-artifacts` | `chore/reflect-pass-recovered-artifacts` | Upstream gone; no local dirty files observed | Closed clean candidate after owner signoff. |
| `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend` | `feat/tfep-troubleshoot-backend` | Untracked review artifacts | Block removal until review artifacts are archived or explicitly abandoned. |
| `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening` | `feat/troubleshoot-pipeline-hardening` | Same branch as `.claude/worktrees/wf_3cd03e8d-30a-12`; upstream gone; no local dirty files observed | Duplicate branch occupancy risk; choose canonical copy before removal. |
| `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals` | `feat/troubleshoot-hardening-evals` | Upstream gone; large untracked eval/reflect/troubleshoot-meta artifacts | Block removal until artifacts are archived or explicitly abandoned. |

## Recommended cleanup sequence

1. Freeze cleanup-sensitive lanes and ask lane owners for final disposition: preserve, archive then remove, or abandon then remove.
2. Preserve active lanes:
   - `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2` remains as the active cliEval v-next lane.
   - `/config/workspace/IronClaude/.dev/worktrees/SprintRun429` remains because it is an active dirty implementation lane.
3. Re-run a full read-only inventory immediately before any removal:
   - worktree list
   - root status
   - per-worktree status
   - merge/rebase state via each worktree's `git rev-parse --git-dir`
   - branch tracking
   - stash list
4. Archive or manifest dirty artifact-only lanes before removal:
   - `/config/workspace/IronClaude/.claude/worktrees/SprintReRun`
   - `/config/workspace/IronClaude/.claude/worktrees/mms-m8m9`
   - `/config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12`
   - `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend`
   - `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals`
5. Resolve duplicate branch occupancy for `feat/troubleshoot-pipeline-hardening` before deleting either path:
   - `/config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12`
   - `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening`
6. Remove only owner-approved stale worktrees using `git -C /config/workspace/IronClaude worktree remove <absolute-worktree-path>`.
7. Run `git -C /config/workspace/IronClaude worktree prune` only after removals and after confirming every expected worktree is still registered or intentionally removed.
8. Leave all stashes untouched unless the user gives a separate, specific stash instruction.
9. Do not stage or commit cleanup artifacts unless separately instructed. If staging later becomes necessary, never stage `.claude/` mirrors; only `/config/workspace/IronClaude/.claude/settings.json` is an allowed tracked `.claude/` exception.

## Removal blockers and risks

### Hard blockers before removal

- Active cliEval v-next lane: `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2` should remain.
- Active dirty implementation lane: `/config/workspace/IronClaude/.dev/worktrees/SprintRun429` should remain.
- Duplicate branch occupancy: `feat/troubleshoot-pipeline-hardening` is registered in two worktrees and needs human adjudication before either path is removed.
- Dirty or untracked artifact lanes need archive/manifest or explicit abandonment before worktree removal.
- Repo stashes are shared and must remain untouched.

### Specific risks

- Root status shows `.dev/worktrees/` as untracked, but these are registered worktrees. Filesystem deletion would bypass git worktree metadata and can strand registrations.
- `.claude/` worktrees may contain generated mirror paths or artifacts; do not stage `.claude/` mirror content during cleanup.
- `[gone]` upstream status from the handoff is not deletion authorization. A gone upstream can still coexist with local-only commits or untracked recovery artifacts.
- Large eval/reflect/troubleshoot artifacts can be expensive to preserve but may be required evidence for recovery, review, or eval lanes.
- Root branch state changed relative to the handoff: the handoff observed root on `fix/pr-submit-defaults-monitor-timeout`, while the current inventory shows root on `master` behind `origin/master` by 3 commits. Treat this as a freshness warning and re-inventory again before executing removal.

## Final removal checklist for the main agent

Use this checklist only after receiving explicit cleanup approval.

- [ ] Re-run `git -C /config/workspace/IronClaude worktree list --porcelain`.
- [ ] Re-run `git -C /config/workspace/IronClaude status --short --branch --untracked-files=all`.
- [ ] Re-run `git -C /config/workspace/IronClaude stash list` and confirm stashes will not be touched.
- [ ] For every registered worktree, run `git -C <absolute-worktree-path> status --short --branch --untracked-files=all`.
- [ ] For every registered worktree, inspect merge/rebase state under `$(git -C <absolute-worktree-path> rev-parse --git-dir)`.
- [ ] Confirm `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2` remains unless user explicitly closes active cliEval v-next.
- [ ] Confirm `/config/workspace/IronClaude/.dev/worktrees/SprintRun429` remains unless user explicitly closes or abandons active dirty implementation work.
- [ ] Resolve which `feat/troubleshoot-pipeline-hardening` worktree is canonical.
- [ ] Archive or explicitly abandon artifacts in dirty artifact lanes.
- [ ] Get owner/user signoff for each absolute worktree path to remove.
- [ ] Remove approved stale worktrees only with `git -C /config/workspace/IronClaude worktree remove <absolute-worktree-path>`.
- [ ] Prune only after removals and after confirming no expected worktree is missing.
- [ ] Do not stage, commit, reset, rebase, stash, pop, drop, or clear anything as part of removal unless a separate explicit instruction says to.
