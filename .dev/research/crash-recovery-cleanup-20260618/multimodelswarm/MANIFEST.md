# MultiModelSwarm stale artifact cleanup manifest

Cleanup root: `/config/workspace/IronClaude/.dev/research/crash-recovery-cleanup-20260618/multimodelswarm/`

Source handoff: `/config/workspace/IronClaude/.dev/research/crash-recovery-handoffs-20260617/11-multimodelswarm-artifacts.md`

## Cleanup criteria used

Moved only lowercase `current/MultiModelSwarm` bundles whose `.roadmap-state.json` matched all of:

- SHA-256 prefix `8df1f5f74613`
- `anti-instinct` status `FAIL`
- `spec_file` pointed under missing `/config/workspace/IronClaude/.claude/worktrees/BareReview/`
- Not the active/ambiguous `mms-m8m9` current bundle
- Not the root complete archive
- Not uppercase `Current` recovered-artifact bundles

The `mms-m8m9` complete 4-file copy was copied into this archive and the original was preserved in place.

## Moved stale lowercase current bundles

Each source below was moved into the archive with a source-identifying directory name.

| Original source | Archive destination | Files |
|---|---|---:|
| `/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm` | `/config/workspace/IronClaude/.dev/research/crash-recovery-cleanup-20260618/multimodelswarm/main-current__lowercase-current__moved` | 29 |
| `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/.dev/releases/current/MultiModelSwarm` | `/config/workspace/IronClaude/.dev/research/crash-recovery-cleanup-20260618/multimodelswarm/claude-worktree-fr028-fr028__lowercase-current__moved` | 29 |
| `/config/workspace/IronClaude/.claude/worktrees/sc-cli-eval/.dev/releases/current/MultiModelSwarm` | `/config/workspace/IronClaude/.dev/research/crash-recovery-cleanup-20260618/multimodelswarm/claude-worktree-sc-cli-eval__lowercase-current__moved` | 29 |
| `/config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12/.dev/releases/current/MultiModelSwarm` | `/config/workspace/IronClaude/.dev/research/crash-recovery-cleanup-20260618/multimodelswarm/claude-worktree-wf_3cd03e8d-30a-12__lowercase-current__moved` | 29 |
| `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/releases/current/MultiModelSwarm` | `/config/workspace/IronClaude/.dev/research/crash-recovery-cleanup-20260618/multimodelswarm/dev-worktree-SprintRun429__lowercase-current__moved` | 29 |
| `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/.dev/releases/current/MultiModelSwarm` | `/config/workspace/IronClaude/.dev/research/crash-recovery-cleanup-20260618/multimodelswarm/dev-worktree-cli-eval-v2__lowercase-current__moved` | 29 |
| `/config/workspace/IronClaude/.dev/worktrees/fix-sprint-rerun-pass-recovered/.dev/releases/current/MultiModelSwarm` | `/config/workspace/IronClaude/.dev/research/crash-recovery-cleanup-20260618/multimodelswarm/dev-worktree-fix-sprint-rerun-pass-recovered__lowercase-current__moved` | 21 |
| `/config/workspace/IronClaude/.dev/worktrees/reflect-pass-recovered-artifacts/.dev/releases/current/MultiModelSwarm` | `/config/workspace/IronClaude/.dev/research/crash-recovery-cleanup-20260618/multimodelswarm/dev-worktree-reflect-pass-recovered-artifacts__lowercase-current__moved` | 21 |
| `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/releases/current/MultiModelSwarm` | `/config/workspace/IronClaude/.dev/research/crash-recovery-cleanup-20260618/multimodelswarm/dev-worktree-tfep-troubleshoot-backend__lowercase-current__moved` | 29 |
| `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening/.dev/releases/current/MultiModelSwarm` | `/config/workspace/IronClaude/.dev/research/crash-recovery-cleanup-20260618/multimodelswarm/dev-worktree-troubleshoot-hardening__lowercase-current__moved` | 29 |
| `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/.dev/releases/current/MultiModelSwarm` | `/config/workspace/IronClaude/.dev/research/crash-recovery-cleanup-20260618/multimodelswarm/dev-worktree-troubleshoot-hardening-evals__lowercase-current__moved` | 29 |

## Copied but original preserved

Copied the untracked active-lane complete set from:

`/config/workspace/IronClaude/.claude/worktrees/mms-m8m9/.dev/releases/complete/MultiModelSwarm`

Archive copy:

`/config/workspace/IronClaude/.dev/research/crash-recovery-cleanup-20260618/multimodelswarm/claude-worktree-mms-m8m9__complete-untracked-4file-copy__copied-original-preserved`

Files copied:

- `merged-requirements.compressed.md`
- `tasklist/phase-8-cp1.md`
- `tasklist/phase-8-cp2.md`
- `tasklist/phase-9-tasklist.md`

The original 4 files remain in the `mms-m8m9` worktree.

## Preserved in place

- Root complete archive: `/config/workspace/IronClaude/.dev/releases/complete/MultiModelSwarm`
- Active/ambiguous M8/M9 lowercase current bundle: `/config/workspace/IronClaude/.claude/worktrees/mms-m8m9/.dev/releases/current/MultiModelSwarm`
- Active/ambiguous M8/M9 complete copy: `/config/workspace/IronClaude/.claude/worktrees/mms-m8m9/.dev/releases/complete/MultiModelSwarm`
- Uppercase recovered variant: `/config/workspace/IronClaude/.dev/worktrees/fix-sprint-rerun-pass-recovered/.dev/releases/Current/MultiModelSwarm`
- Uppercase recovered variant: `/config/workspace/IronClaude/.dev/worktrees/reflect-pass-recovered-artifacts/.dev/releases/Current/MultiModelSwarm`

## Remaining MultiModelSwarm states after cleanup

- `8df1f5f74613 FAIL` at `/config/workspace/IronClaude/.claude/worktrees/mms-m8m9/.dev/releases/current/MultiModelSwarm/.roadmap-state.json` — preserved because it is inside the active M8/M9 worktree.
- `8df1f5f74613 FAIL` at `/config/workspace/IronClaude/.dev/releases/complete/MultiModelSwarm/.roadmap-state.json` — preserved as root complete archive evidence.
- `732e68da4d19 PASS` at `/config/workspace/IronClaude/.dev/worktrees/fix-sprint-rerun-pass-recovered/.dev/releases/Current/MultiModelSwarm/.roadmap-state.json` — preserved as uppercase recovered-artifact variant.
- `732e68da4d19 PASS` at `/config/workspace/IronClaude/.dev/worktrees/reflect-pass-recovered-artifacts/.dev/releases/Current/MultiModelSwarm/.roadmap-state.json` — preserved as uppercase recovered-artifact variant.

## Remaining ambiguity / outstanding cleanup

1. `/config/workspace/IronClaude/.claude/worktrees/mms-m8m9/.dev/releases/current/MultiModelSwarm` still has the stale lowercase current signature, but it was not moved because the branch is the active MultiModelSwarm M8/M9 lane.
2. The original untracked 4-file complete copy in `/config/workspace/IronClaude/.claude/worktrees/mms-m8m9/.dev/releases/complete/MultiModelSwarm` remains in place and should be reconciled by the M8/M9 owner before deletion.
3. The root complete archive still contains a stale roadmap state by design; treat it as archival evidence, not live current state.
4. Uppercase `Current` recovered-artifact bundles were not normalized or moved because they are different later variants and are not duplicates of the stale lowercase bundles.

Machine-readable action log: `/config/workspace/IronClaude/.dev/research/crash-recovery-cleanup-20260618/multimodelswarm/cleanup-record.json`.
