# Summary: #339 [Feature]:  Orchestrator - To Run and manage ALL sessions within a worktree

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/339
- Type: feature
- Complexity: complex (rubric: `refs/claim.md`): over 16 hours, more than one subsystem (worker contract and its tests, new commands and their registries, ccsession launch, output style), and a security change (cross-session trust layer).
- Effort estimate: 40 hours (version 1: `/sc:sweep` with the static report about 20, `/sc:close` with executed safety checks about 14, the comment-3 research and debate about 6). Version 2 (signed grants, orchestrator of orchestrators) is not included; Not known yet until the research picks a design.

## What the issue asks for

One orchestrator session that every other session reports its updates and questions through, so the person never has to open a child session, with a static report of all agents, sessions and worktrees (modelled on #409) that replaces the usual end-of-message table. Two new commands: `/sc:sweep` finds idle, stuck, timed-out or finished sessions over the last few hours (issue default 6) and says what each needs; `/sc:close` removes a worktree and branch only after strict checks that nothing of value is uncommitted or unpushed. Comment 1 adds that the orchestrator must never stop polling and must own cleanup; comment 2 proposes a trust layer for messages between sessions (same permission mode, fixed message types, signed narrow grants); comment 3 sends its open questions to `/tech-research` and an adversarial debate. Most of the base model already exists as the Orca coordinator/worker contract, so the work is extending that contract, not building a new protocol; local uncommitted brainstorm and research work for this issue already exists in this worktree.

## Relevant files and systems (cheatsheet)

| Path or system | Why it matters |
|---|---|
| `src/superclaude/core/WORKER-CONTRACT.md` | The coordinator/worker contract: the orchestrator's rules already live here (section 4 cleanup and git ownership, WC-6 retry, WC-10 liveness, never-as-worker list at line 23). Extend it; do not duplicate it. |
| `tests/skills/test_worker_contract.py` | Pins the contract text and the never-as-worker list (line 245); changes when `/sc:sweep` and `/sc:close` join that list. |
| `src/superclaude/core/HOW-WE-WORK.md` (lines 318-337 "Other commands", 396-405 "Orca coordination") | New command rows and coordination wording; must be byte-copied to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. |
| `tests/recommend/test_routing_refresh.py:33`, `tests/core/test_how_we_work_routing_table.py` | Registries that fail when a new command file is added without being listed. |
| `src/superclaude/commands/` and `src/superclaude/skills/` | Where `sweep.md` / `close.md` and their protocol skills would go; neither exists today. |
| `src/superclaude/skills/sc-crash-recovery/SKILL.md` | Existing read-only sweep (`--all`, `--since`, default 72 hours) to reuse for session signals. |
| `src/superclaude/skills/ccsession-tag/ccsession`, `README.md` | Session launch mode (`CCSESSION_PERMISSIONS`, lines 135-139) and `ccsession --list` as a sweep input. |
| `src/superclaude/output-styles/pragmatic.md:22` | Mandatory DONE / NEXT table; an orchestrator report needs an explicit exception. |
| `.dev/orca-command-refactor/` (`inventory/orca-capabilities.md`, `changes/CR-01-feature-worktree-hierarchy.md`, `decisions/APPROVED.md`) | Orca facts (`worker-list` attention and nextAction, liveness verdicts, message types), placement rule, and rollout state (P1 PASS, P2 open). |
| Orca CLI (`orca` / `orca-ide`, external) | `worker-list`, `check --wait`, `ask`/`reply`, `orca worktree rm`; syntax comes from the binary's guide, never copied into the repo. |
| Issue #409, branch `docs/409-orca-dashboard-designs` (commit 495eb96d) | Read-only observer design; the static report layout should follow it. Unmerged. |
| Open PR #422 | P2 edits `WORKER-CONTRACT.md` and 15 command files; contract edits for #339 should land after it. |
| `.dev/brainstorms/20261107-073115-orchestrator-mode/`, `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/` | Local, uncommitted brainstorm seed (records the owner's first-PR scope: read-only `/sc:sweep` plus static report) and four finished research scopes with no synthesis yet. |
| `src/superclaude/hooks/scripts/launch-job-identity.sh` (PR #414) | Same-user job identity only; not usable as the trust layer. |

## Analysis

- [analysis/analyze-worker-contract.md](analysis/analyze-worker-contract.md): `/sc:analyze --depth deep` on the worker contract and the systems above; 14 architecture findings and 5 security findings, with a three-phase recommendation.
