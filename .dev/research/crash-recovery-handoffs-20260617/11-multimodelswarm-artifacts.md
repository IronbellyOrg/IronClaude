# MultiModelSwarm artifacts handoff

## Cross-worktree inventory

Scan date: 2026-06-17. Scope was read-only except this handoff. The recurring conflict is not multiple different live roadmap runs; it is mostly the same stale roadmap state copied into many worktrees plus one partial untracked M8/M9 artifact set in the `mms-m8m9` worktree.

### Registered worktrees with MultiModelSwarm state

| Root | Branch | MultiModelSwarm state | Classification signal |
|---|---|---|---|
| `/config/workspace/IronClaude` | `fix/pr-submit-defaults-monitor-timeout` | `/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/.roadmap-state.json` and `/config/workspace/IronClaude/.dev/releases/complete/MultiModelSwarm/.roadmap-state.json` | Both state files have identical hash `8df1f5f74613`; both point at missing `/config/workspace/IronClaude/.claude/worktrees/BareReview/...` paths. |
| `/config/workspace/IronClaude/.claude/worktrees/mms-m8m9` | `feat/sc-bare-review-m8m9-migration` | `/config/workspace/IronClaude/.claude/worktrees/mms-m8m9/.dev/releases/current/MultiModelSwarm/.roadmap-state.json` | Same stale state hash `8df1f5f74613`, but this worktree has the only relevant untracked complete-copy deltas for M8/M9 tasklists. |
| `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028` | `fix/swarm-normalize-perworker-status-fr028` | `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/.dev/releases/current/MultiModelSwarm/.roadmap-state.json` | Same stale state hash `8df1f5f74613`; worktree itself is clean. |
| `/config/workspace/IronClaude/.claude/worktrees/sc-cli-eval` | `feat/sc-cli-eval` | `/config/workspace/IronClaude/.claude/worktrees/sc-cli-eval/.dev/releases/current/MultiModelSwarm/.roadmap-state.json` | Same stale state hash `8df1f5f74613`; clean unrelated worktree. |
| `/config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12` | `feat/troubleshoot-pipeline-hardening` | `/config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12/.dev/releases/current/MultiModelSwarm/.roadmap-state.json` | Same stale state hash `8df1f5f74613`; unrelated branch. |
| `/config/workspace/IronClaude/.dev/worktrees/SprintRun429` | `SprintRun429` | `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/releases/current/MultiModelSwarm/.roadmap-state.json` | Same stale state hash `8df1f5f74613`; unrelated sprint recovery worktree. |
| `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2` | `fix/cli-eval-v2` | `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/.dev/releases/current/MultiModelSwarm/.roadmap-state.json` | Same stale state hash `8df1f5f74613`; unrelated cli-eval worktree. |
| `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend` | `feat/tfep-troubleshoot-backend` | `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/releases/current/MultiModelSwarm/.roadmap-state.json` | Same stale state hash `8df1f5f74613`; unrelated troubleshoot backend worktree. |
| `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening` | `feat/troubleshoot-pipeline-hardening` | `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening/.dev/releases/current/MultiModelSwarm/.roadmap-state.json` | Same stale state hash `8df1f5f74613`; unrelated hardening worktree. |
| `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals` | `feat/troubleshoot-hardening-evals` | `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/.dev/releases/current/MultiModelSwarm/.roadmap-state.json` | Same stale state hash `8df1f5f74613`; unrelated eval worktree. |
| `/config/workspace/IronClaude/.dev/worktrees/fix-sprint-rerun-pass-recovered` | `fix/sprint-rerun-pass-recovered` | Lowercase `current` has stale hash `8df1f5f74613`; uppercase `Current` has hash `732e68da4d19` | Uppercase `Current` is a later rerun variant: anti-instinct PASS, spec-fidelity FAIL, opus+sonnet agents, and paths under main repo uppercase `Current`. |
| `/config/workspace/IronClaude/.dev/worktrees/reflect-pass-recovered-artifacts` | `chore/reflect-pass-recovered-artifacts` | Lowercase `current` has stale hash `8df1f5f74613`; uppercase `Current` has hash `732e68da4d19` | Same later rerun variant as `fix-sprint-rerun-pass-recovered`: anti-instinct PASS, spec-fidelity FAIL. |

### Common stale state signature

The dominant `.roadmap-state.json` signature is:

- Hash: `8df1f5f74613`.
- `spec_file`: `/config/workspace/IronClaude/.claude/worktrees/BareReview/.dev/brainstorms/20260529-multimodel-swarm-COMPARE/merged-requirements.md`.
- Output files: `/config/workspace/IronClaude/.claude/worktrees/BareReview/.dev/releases/Current/MultiModelSwarm/...`.
- Agents: `opus` + `haiku`, persona `architect`.
- Steps: extract/generate/diff/debate/score/merge all PASS, `anti-instinct` FAIL, `wiring-verification` PASS.
- `last_run`: `2026-05-29T15:54:51.113749+00:00`.
- The referenced `BareReview` source and output paths are missing now.

The matching anti-instinct audit reports `undischarged_obligations: 6`, `uncovered_contracts: 0`, fingerprint coverage `0.88`, and flags M6/M9 stub/no-op wording around normalization and `sc-bare-review` migration. That is a roadmap-gate artifact, not evidence that a current worktree is actively blocked today.

### Current vs complete roots

| Root | File count / shape | Relationship |
|---|---:|---|
| `/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm` | 29 files | Stale roadmap-run bundle with generated roadmap, audit, and selected tasklists. Hashes match corresponding files in most worktree `current` copies. |
| `/config/workspace/IronClaude/.dev/releases/complete/MultiModelSwarm` | 247 files | Canonical large completed artifact bundle in the main repo. It includes the stale roadmap-state file plus phase result logs and tracked tasklists. Treat as archival evidence, not live `current`. |
| `/config/workspace/IronClaude/.claude/worktrees/mms-m8m9/.dev/releases/current/MultiModelSwarm` | 29 files | Same stale current bundle as main `current`. |
| `/config/workspace/IronClaude/.claude/worktrees/mms-m8m9/.dev/releases/complete/MultiModelSwarm` | 4 untracked files | Partial M8/M9 remediation artifact copy only: `merged-requirements.compressed.md`, `tasklist/phase-8-cp1.md`, `tasklist/phase-8-cp2.md`, and `tasklist/phase-9-tasklist.md`. Not a full complete bundle. |
| `/config/workspace/IronClaude/.dev/worktrees/fix-sprint-rerun-pass-recovered/.dev/releases/Current/MultiModelSwarm` and `/config/workspace/IronClaude/.dev/worktrees/reflect-pass-recovered-artifacts/.dev/releases/Current/MultiModelSwarm` | Uppercase `Current` state only inspected | Later rerun variant with `anti-instinct: PASS` and `spec-fidelity: FAIL`; preserve as recovered-artifact evidence until its owning lane confirms archival. |

Key file drift:

| File | Main `current` | Main `complete` | `mms-m8m9` `current` | `mms-m8m9` untracked `complete` | Meaning |
|---|---:|---:|---:|---:|---|
| `merged-requirements.compressed.md` | `16628ae11575` | `16628ae11575` | `16628ae11575` | `16628ae11575` | Same input compression everywhere. |
| `roadmap.md` | `3ad0a01a39c4` | `3ad0a01a39c4` | `3ad0a01a39c4` | missing | Same roadmap where present. |
| `tasklist/phase-8-cp1.md` | missing | `fa0630890daa` | missing | `4024d13ff3f3` | `mms-m8m9` copy differs and appears to be an earlier/generated checkpoint report tied to BareReview branch evidence. |
| `tasklist/phase-8-cp2.md` | missing | `f09108c53cbd` | missing | `71a62c61b9a5` | `mms-m8m9` differs from main complete. |
| `tasklist/phase-8-cp4.md` | `ea19ac315078` | missing | `ea19ac315078` | missing | Present only in stale current bundle copies. |
| `tasklist/phase-9-tasklist.md` | `baf36c4c05df` | `cf34d2d18f2a` | `baf36c4c05df` | `cf34d2d18f2a` | Main complete and `mms-m8m9` untracked complete agree; they include later M9 entry-gate remediation absent from stale current. |

## Which copies are active/stale/ambiguous

### Active / preserve

1. `/config/workspace/IronClaude/.claude/worktrees/mms-m8m9` is the only worktree whose branch name and status align with the MultiModelSwarm M8/M9 lane. Preserve it before any cleanup. It has untracked artifacts under `/config/workspace/IronClaude/.claude/worktrees/mms-m8m9/.dev/releases/complete/MultiModelSwarm/` that are not identical to main `current` and include M8/M9 checkpoint/tasklist material.
2. `/config/workspace/IronClaude/.dev/releases/complete/MultiModelSwarm` is the main-repo archival complete bundle. It is tracked in the main checkout and contains the large phase result set. Preserve as canonical archive unless a separate cleanup task decides `.dev/releases/complete/*` should be pruned by policy.
3. Uppercase `Current` rerun variants under `/config/workspace/IronClaude/.dev/worktrees/fix-sprint-rerun-pass-recovered/.dev/releases/Current/MultiModelSwarm` and `/config/workspace/IronClaude/.dev/worktrees/reflect-pass-recovered-artifacts/.dev/releases/Current/MultiModelSwarm` should be preserved temporarily as recovered-artifact evidence. They are not the same as the stale anti-instinct FAIL state; they show anti-instinct PASS and spec-fidelity FAIL.

### Stale / safe candidates after owner confirmation

These are stale candidates because they have identical state hash `8df1f5f74613`, point to the deleted/missing BareReview worktree, and carry the old anti-instinct FAIL result from 2026-05-29:

- `/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm`
- `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/.dev/releases/current/MultiModelSwarm`
- `/config/workspace/IronClaude/.claude/worktrees/sc-cli-eval/.dev/releases/current/MultiModelSwarm`
- `/config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12/.dev/releases/current/MultiModelSwarm`
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/releases/current/MultiModelSwarm`
- `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/.dev/releases/current/MultiModelSwarm`
- `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend/.dev/releases/current/MultiModelSwarm`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening/.dev/releases/current/MultiModelSwarm`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/.dev/releases/current/MultiModelSwarm`
- Lowercase `current` copies in `/config/workspace/IronClaude/.dev/worktrees/fix-sprint-rerun-pass-recovered/.dev/releases/current/MultiModelSwarm` and `/config/workspace/IronClaude/.dev/worktrees/reflect-pass-recovered-artifacts/.dev/releases/current/MultiModelSwarm`

### Ambiguous

1. `/config/workspace/IronClaude/.claude/worktrees/mms-m8m9/.dev/releases/current/MultiModelSwarm` is stale by state hash but sits inside the active M8/M9 worktree. Do not delete until the M8/M9 owner confirms whether its current bundle is used as context for the branch.
2. `/config/workspace/IronClaude/.claude/worktrees/mms-m8m9/.dev/releases/complete/MultiModelSwarm/tasklist/phase-8-cp1.md` and `phase-8-cp2.md` differ from main complete. They may be superseded, but because they are untracked and lane-specific, archive or compare before deletion.
3. The `BareReview`-anchored paths in state files are stale references, not current filesystem roots. Do not recreate the deleted BareReview worktree just to satisfy these pointers.

## Cleanup/archival plan

No move/delete was performed. Recommended future cleanup criteria:

1. A MultiModelSwarm artifact root is eligible for stale cleanup only if all are true: its `.roadmap-state.json` hash is `8df1f5f74613`; its `spec_file` or `output_file` fields point under `/config/workspace/IronClaude/.claude/worktrees/BareReview/`; that BareReview path is absent; its owner worktree branch is not `feat/sc-bare-review-m8m9-migration`; and it has no untracked files under that root.
2. A root is active/preserve if any are true: it is in `/config/workspace/IronClaude/.claude/worktrees/mms-m8m9`; it is in `/config/workspace/IronClaude/.dev/releases/complete/MultiModelSwarm`; it has non-stale state hash `732e68da4d19`; it has untracked files; or its branch/status mentions swarm, bare-review, M8, M9, recovered artifacts, or a PR currently under review.
3. Before deleting any duplicate stale current bundle, record the root path, state hash, branch, `git status --short`, and whether the root has untracked files in a cleanup note or PR description.
4. For `mms-m8m9`, first reconcile the 4 untracked complete files: compare against main complete, decide whether the differing phase-8 checkpoint files are superseded or should be copied into the canonical archive, and only then remove any duplicate `current` bundle.
5. Do not treat `anti-instinct: FAIL` alone as a live blocker. It is live only if the referenced source/output paths exist in the same active worktree and the roadmap command is the current owner lane. Here the repeated FAIL is stale because the state paths point outside each worktree to a missing BareReview root.
6. Do not normalize uppercase `Current` to lowercase `current` automatically. The uppercase `Current` rerun variants represent a different later state (`anti-instinct: PASS`, `spec-fidelity: FAIL`) and should be reviewed under the sprint-rerun/reflect recovered-artifacts lanes.

## Validation commands

Read-only commands used or suitable for revalidation:

- `git -C /config/workspace/IronClaude worktree list --porcelain`
- `find /config/workspace/IronClaude /config/workspace/IronClaude/.claude/worktrees /config/workspace/IronClaude/.dev/worktrees -name '.roadmap-state.json' -path '*/MultiModelSwarm/*' -print 2>/dev/null | sort`
- `uv run python -c "from pathlib import Path; import json, hashlib; roots=[Path('/config/workspace/IronClaude'),Path('/config/workspace/IronClaude/.claude/worktrees'),Path('/config/workspace/IronClaude/.dev/worktrees')]; seen=[]; [seen.append(p) for root in roots if root.exists() for p in root.rglob('.roadmap-state.json') if '/MultiModelSwarm/' in str(p) and p not in seen]; [print(str(p), hashlib.sha256(p.read_bytes()).hexdigest()[:12], json.loads(p.read_text()).get('spec_file'), {k:(v.get('status') if isinstance(v,dict) else v) for k,v in json.loads(p.read_text()).get('steps',{}).items()}) for p in sorted(seen, key=str)]"`
- `uv run python -c "from pathlib import Path; import hashlib; roots={'main_current':Path('/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm'),'main_complete':Path('/config/workspace/IronClaude/.dev/releases/complete/MultiModelSwarm'),'mms_current':Path('/config/workspace/IronClaude/.claude/worktrees/mms-m8m9/.dev/releases/current/MultiModelSwarm'),'mms_complete':Path('/config/workspace/IronClaude/.claude/worktrees/mms-m8m9/.dev/releases/complete/MultiModelSwarm')}; files=['merged-requirements.compressed.md','roadmap.md','tasklist/phase-8-cp1.md','tasklist/phase-8-cp2.md','tasklist/phase-8-cp4.md','tasklist/phase-9-tasklist.md']; [print('FILE', f) or [print(name, (root/f).stat().st_size if (root/f).exists() else 'MISSING', hashlib.sha256((root/f).read_bytes()).hexdigest()[:12] if (root/f).exists() else '') for name,root in roots.items()] for f in files]"`
- `git -C /config/workspace/IronClaude/.claude/worktrees/mms-m8m9 status --short --untracked-files=all`
- `test -e /config/workspace/IronClaude/.claude/worktrees/BareReview/.dev/brainstorms/20260529-multimodel-swarm-COMPARE/merged-requirements.md && printf 'exists\n' || printf 'missing\n'`

## Risks

- False cleanup risk: the active `mms-m8m9` worktree contains a stale-looking `current` bundle and lane-specific untracked `complete` files. Cleanup based only on hash would delete context that may still explain the M8/M9 branch.
- Case drift risk: lowercase `current` and uppercase `Current` are separate paths on Linux. The uppercase rerun variants are not duplicates of the stale lowercase bundle.
- Stale-path risk: many state files contain absolute paths into the removed BareReview worktree. Re-running tools from those states without rebasing paths will mislead operators or fail.
- Git-index risk: `.dev/worktrees/*` are untracked from the main checkout. Do not run broad `git add -A` from `/config/workspace/IronClaude`; it would try to stage whole nested worktrees.
- Completion-semantics risk: `/config/workspace/IronClaude/.dev/releases/complete/MultiModelSwarm/.roadmap-state.json` still says `anti-instinct: FAIL`, even though the bundle lives under `complete`. Treat the directory name as archival placement, not proof every roadmap gate passed.
- Artifact-authority risk: phase-9 tasklists differ between stale `current` and `complete`. The complete version includes later M9 entry-gate remediation and is more authoritative than stale current for M9 planning, but the M8 checkpoint deltas in `mms-m8m9` still need owner review.

## New-session prompt

Continue crash recovery for MultiModelSwarm artifacts in `/config/workspace/IronClaude`: read `/config/workspace/IronClaude/.dev/research/crash-recovery-handoffs-20260617/11-multimodelswarm-artifacts.md`, then inspect `/config/workspace/IronClaude/.claude/worktrees/mms-m8m9` before touching any `.dev/releases/current/MultiModelSwarm` copy. Treat repeated `.roadmap-state.json` hash `8df1f5f74613` with `anti-instinct: FAIL` and `/config/workspace/IronClaude/.claude/worktrees/BareReview/...` paths as stale unless the referenced path exists in the active worktree. Preserve `/config/workspace/IronClaude/.dev/releases/complete/MultiModelSwarm`, preserve the `mms-m8m9` untracked complete files until compared, and do not delete or move artifacts without explicit approval. Revalidate with `git -C /config/workspace/IronClaude worktree list --porcelain` and `find /config/workspace/IronClaude /config/workspace/IronClaude/.claude/worktrees /config/workspace/IronClaude/.dev/worktrees -name '.roadmap-state.json' -path '*/MultiModelSwarm/*' -print 2>/dev/null | sort`.
