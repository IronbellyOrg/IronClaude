# Phase 1 scope confirmation

**Date:** 2026-11-20

## Confirmed in-scope
- Issue watcher package `src/superclaude/cli/issue_watch/` (cycle, github, record, launch, predicates, audit, cli, runner) and its design docs `issue-watcher.md`, `issue-watcher-setup.md`.
- `/sc:issue --claim` flow: command, `sc-issue-protocol` skill (refs, scripts incl. `orca_worktree.py`), worker agents, design docs `sc-issue-claim-pipeline-flag.md`, `sc-issue-command.md`.
- Launch-level guard stack: `launch-level-guard.sh`, `launch-job-identity.sh`, `launch-level-pre-push.sh`, `hooks.json`, `install_hooks.py`, ccsession shim coupling, design docs `sc-issue-launch-level-hook.md`, `issue-pipeline-guard-g2*.md`, `issue-pipeline-fu1.md`.
- Coordinator contract text in `src/superclaude/core/WORKER-CONTRACT.md`.
- Appendix "Removed on 2026-11-20": `src/superclaude/cli/issue_pipeline/` and WC-17 (commit 01e7a9e23, read via `git show 01e7a9e23^:<path>`).
- Tier: Standard, QA intensity standard.

## Out of scope
PR 686 and the rewrite design: exactly one sentence in Section 1 of the final document and nothing else.

## Directory existence
All present: research/, synthesis/, qa/, reviews/, scope/, phase-outputs/reports/ (created now), output directory `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/` (existed already).

## Git readability
`git -C /home/coder/workspaces/IronClaude cat-file -t 01e7a9e23` -> `commit`.
`git show 01e7a9e23^:src/superclaude/cli/issue_pipeline/cli.py | head -5` printed: `"""The ``superclaude issue-pipeline`` command group.` / blank / `Verbs only sequence calls into the package and print closed result words; no` / `verb prints file or GitHub text.` / `"""`.

## Snapshot fingerprint (before)
Command: `find /home/coder/.cache/ic-snap-20261120/master -type f -printf '%p %s %T@\n' | sort | sha256sum`
- sha256: `f20de643086d06b8c8cffb981676a619719094036d6fa386953b4bc777d49b74`
- regular file count: 2178
- snapshot root directory mtime at this moment: 2026-11-20 04:53 (epoch 1795150418.9). NOTE: an earlier QA agent (A.10.5 operational lens) reported creating and immediately removing a probe file `.probe_qa_ro` at the snapshot root while checking read-only status; that explains the root-directory mtime of 04:53 (the snapshot was exported at 02:26). The fingerprint covers regular files only, so it is unaffected. Nothing was left behind (`ls` shows no probe file).
- `cycle.py` exists: 52912 bytes, mtime Nov 20 02:26.
