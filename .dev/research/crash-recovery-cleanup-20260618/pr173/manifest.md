# PR173 stale-worktree cleanup manifest

Generated: 2026-06-18

## Inputs

- Handoff: `/config/workspace/IronClaude/.dev/research/crash-recovery-handoffs-20260617/04-pr173-monitor-blocked.md`
- Handoff: `/config/workspace/IronClaude/.dev/research/crash-recovery-handoffs-20260617/09-troubleshoot-hardening-stale.md`
- Worktree: `/config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12`
- Worktree: `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening`

## Archived artifacts

- Source: `/config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12/.dev/pr-monitor/pr-173-augment-remediation-2026-06-12/monitor-run-173.jsonl`
- Archived copy: `/config/workspace/IronClaude/.dev/research/crash-recovery-cleanup-20260618/pr173/wf_3cd03e8d-30a-12/.dev/pr-monitor/pr-173-augment-remediation-2026-06-12/monitor-run-173.jsonl`
- SHA256: `5a3aa7075db3a9ae3c645117fbd19b436ab46bf0c6184d20e033698fbf0076b8`
- Bytes: `573`

## PR state

- PR: `https://github.com/IronbellyOrg/IronClaude/pull/173`
- State: `MERGED`
- Head ref: `feat/troubleshoot-pipeline-hardening`
- Head SHA: `b9378c72e2d5acc12607316b10ef377110f7c5a3`
- Base: `master`
- Merge commit: `71f16e130d15c33670eabb1917a746848cd41ef5`

## Git checks

### `/config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12`

```text
## feat/troubleshoot-pipeline-hardening...origin/feat/troubleshoot-pipeline-hardening [gone]
 D .dev/releases/current/MultiModelSwarm/.roadmap-state.json
 D .dev/releases/current/MultiModelSwarm/anti-instinct-audit.md
 D .dev/releases/current/MultiModelSwarm/base-selection.err
 D .dev/releases/current/MultiModelSwarm/base-selection.md
 D .dev/releases/current/MultiModelSwarm/debate-transcript.err
 D .dev/releases/current/MultiModelSwarm/debate-transcript.md
 D .dev/releases/current/MultiModelSwarm/diff-analysis.err
 D .dev/releases/current/MultiModelSwarm/diff-analysis.md
 D .dev/releases/current/MultiModelSwarm/extraction.err
 D .dev/releases/current/MultiModelSwarm/extraction.md
 D .dev/releases/current/MultiModelSwarm/merged-requirements.compressed.md
 D .dev/releases/current/MultiModelSwarm/roadmap-haiku-architect.compressed.md
 D .dev/releases/current/MultiModelSwarm/roadmap-haiku-architect.err
 D .dev/releases/current/MultiModelSwarm/roadmap-haiku-architect.md
 D .dev/releases/current/MultiModelSwarm/roadmap-opus-architect.compressed.md
 D .dev/releases/current/MultiModelSwarm/roadmap-opus-architect.err
 D .dev/releases/current/MultiModelSwarm/roadmap-opus-architect.md
 D .dev/releases/current/MultiModelSwarm/roadmap.compressed.md
 D .dev/releases/current/MultiModelSwarm/roadmap.err
 D .dev/releases/current/MultiModelSwarm/roadmap.md
 D .dev/releases/current/MultiModelSwarm/tasklist/phase-1-cp5.md
 D .dev/releases/current/MultiModelSwarm/tasklist/phase-1-tasklist.md
 D .dev/releases/current/MultiModelSwarm/tasklist/phase-3-cp1.md
 D .dev/releases/current/MultiModelSwarm/tasklist/phase-3-cp4.md
 D .dev/releases/current/MultiModelSwarm/tasklist/phase-3-tasklist.md
 D .dev/releases/current/MultiModelSwarm/tasklist/phase-7-tasklist.md
 D .dev/releases/current/MultiModelSwarm/tasklist/phase-8-cp4.md
 D .dev/releases/current/MultiModelSwarm/tasklist/phase-9-tasklist.md
 D .dev/releases/current/MultiModelSwarm/wiring-verification.md
?? .dev/pr-monitor/

BRANCH=feat/troubleshoot-pipeline-hardening
HEAD=b9378c72e2d5acc12607316b10ef377110f7c5a3
REVLIST_ORIGIN_MASTER_HEAD=21	1
UNTRACKED:
.dev/pr-monitor/pr-173-augment-remediation-2026-06-12/monitor-run-173.jsonl
```

Decision: `safe_to_remove: false` until the tracked deletions listed above are intentionally resolved or explicitly accepted by the main agent. The PR-monitor artifact was copied above, but current `git status --short --branch` shows tracked `.dev/releases/current/MultiModelSwarm/**` deletions in addition to the untracked monitor directory. Do not infer branch deletion from this worktree decision.

### `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening`

```text
## feat/troubleshoot-pipeline-hardening...origin/feat/troubleshoot-pipeline-hardening [gone]
 D .dev/releases/current/MultiModelSwarm/.roadmap-state.json
 D .dev/releases/current/MultiModelSwarm/anti-instinct-audit.md
 D .dev/releases/current/MultiModelSwarm/base-selection.err
 D .dev/releases/current/MultiModelSwarm/base-selection.md
 D .dev/releases/current/MultiModelSwarm/debate-transcript.err
 D .dev/releases/current/MultiModelSwarm/debate-transcript.md
 D .dev/releases/current/MultiModelSwarm/diff-analysis.err
 D .dev/releases/current/MultiModelSwarm/diff-analysis.md
 D .dev/releases/current/MultiModelSwarm/extraction.err
 D .dev/releases/current/MultiModelSwarm/extraction.md
 D .dev/releases/current/MultiModelSwarm/merged-requirements.compressed.md
 D .dev/releases/current/MultiModelSwarm/roadmap-haiku-architect.compressed.md
 D .dev/releases/current/MultiModelSwarm/roadmap-haiku-architect.err
 D .dev/releases/current/MultiModelSwarm/roadmap-haiku-architect.md
 D .dev/releases/current/MultiModelSwarm/roadmap-opus-architect.compressed.md
 D .dev/releases/current/MultiModelSwarm/roadmap-opus-architect.err
 D .dev/releases/current/MultiModelSwarm/roadmap-opus-architect.md
 D .dev/releases/current/MultiModelSwarm/roadmap.compressed.md
 D .dev/releases/current/MultiModelSwarm/roadmap.err
 D .dev/releases/current/MultiModelSwarm/roadmap.md
 D .dev/releases/current/MultiModelSwarm/tasklist/phase-1-cp5.md
 D .dev/releases/current/MultiModelSwarm/tasklist/phase-1-tasklist.md
 D .dev/releases/current/MultiModelSwarm/tasklist/phase-3-cp1.md
 D .dev/releases/current/MultiModelSwarm/tasklist/phase-3-cp4.md
 D .dev/releases/current/MultiModelSwarm/tasklist/phase-3-tasklist.md
 D .dev/releases/current/MultiModelSwarm/tasklist/phase-7-tasklist.md
 D .dev/releases/current/MultiModelSwarm/tasklist/phase-8-cp4.md
 D .dev/releases/current/MultiModelSwarm/tasklist/phase-9-tasklist.md
 D .dev/releases/current/MultiModelSwarm/wiring-verification.md

BRANCH=feat/troubleshoot-pipeline-hardening
HEAD=b9378c72e2d5acc12607316b10ef377110f7c5a3
REVLIST_ORIGIN_MASTER_HEAD=21	1
UNTRACKED:
```

Decision: `safe_to_remove: false` until the tracked deletions listed above are intentionally resolved or explicitly accepted by the main agent. Current `git status --short --branch` shows tracked `.dev/releases/current/MultiModelSwarm/**` deletions. Do not infer branch deletion from this worktree decision.

## Additional comparisons

- `git cherry -v origin/master HEAD`: `+ b9378c72e2d5acc12607316b10ef377110f7c5a3 feat(troubleshoot): Pipeline Hardening Closure mode (H0-H5 + waiver latch)`
- Path-limited diff against PR #173 merge commit `71f16e130d15c33670eabb1917a746848cd41ef5`: no output for troubleshoot deliverables excluding `tests/troubleshoot/backtest`.
- Path-limited diff against current `origin/master`: non-empty in `src/superclaude/commands/troubleshoot.md`, `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`, and `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`; this reflects later `origin/master` drift and is not a worktree-removal blocker.
- Files present in stale HEAD but absent from current `origin/master`: 5 paths under `src/superclaude/skills/sc-bare-review/`; branch deletion should be treated as a separate decision from worktree removal.

## Removal guidance

Main agent should not remove either worktree as a routine safe cleanup until the tracked `.dev/releases/current/MultiModelSwarm/**` deletions shown in current status are resolved or explicitly accepted for discard. The PR-monitor artifact from `/config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12` is archived, so that untracked monitor file is no longer the blocker. Keep branch deletion as a separate explicit decision because the local branch remains checked out by both worktrees until removal and has one commit not contained in current `origin/master`.
