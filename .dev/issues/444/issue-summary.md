# Summary: #444 [FEATURE] Evaluate the value, implications and unlocks or rethinks related to /sc:orchestrator having a Sub-Orchestrator or Coordinator mode

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/444
- Type: feature
- Complexity: complex (rubric: `refs/claim.md`). It spans more than one subsystem: the worker contract, the installed core rules, the worktree hook, Orca's depth setting and the unbuilt `/sc:orchestrator` (#339).
- Effort estimate: 24 hours. This covers the evaluation only: research over the D5 debate, CR-01 and #339/#423, settling the PR #449 inconsistency, and a written proposal. Implementing any mode it recommends would be a separate, larger plan.

## What the issue asks for

The issue asks for an evaluation, not a build, of a sub-orchestrator or coordinator mode for the proposed `/sc:orchestrator`, possibly selected with `--sub`. Such a session would delegate work to its own sessions inside a worktree, while taking orders from and reporting to an orchestrator above. The evaluation must cover value, implications, unlocks and the rethinks needed, especially of rule WC-13, which bans a worker from starting other workers. The accuracy check found the issue out of date. PR #449 already names "a coordinator under another orchestrator" in the installed rules but never defines it. The issue also omits decision D5, which already chose to keep Orca nesting at depth 1 and rejected a scoped "Sub-workers: allowed" design that is close to `--sub`.

## Relevant files and systems (cheatsheet)

| Path or system | Why it matters |
|---|---|
| `src/superclaude/core/WORKER-CONTRACT.md` | WC-13 (`:62`) bans worker fan-out, including `worktree create --agent` and `agent launch`. Section 4 (`:67-283`) defines only a person-opened coordinator (`:69`). `:246` records the evidence D5's revisit trigger reads. |
| `src/superclaude/core/CLAUDE.md:55-59` (PR #449) | Installed rule: the creator of a worktree "becomes its orchestrator, or a coordinator under another orchestrator". It names the role the issue evaluates, without a definition. |
| `CLAUDE.md:305,312` (PR #449) | Project copy of the same worktree-ownership rule. |
| `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh` | PR #449 hook. It blocks `orca worktree create` without `--agent` and cannot tell a coordinator from a worker. Its plugin mirror and `tests/hooks/test_require_orca_worktree_agent.py` change with it. |
| `.dev/orca-command-refactor/decisions/D5/RECOMMENDATION.md` | Earlier decision to keep depth 1. Its losing option (b) is the closest prior design. It lists the revisit conditions and the open items (depth-2 mailbox, lowering the depth setting). |
| `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:405`, `decisions/APPROVED.md:12`, `changes/CR-01-feature-worktree-hierarchy.md` | The approved D5 text and the child-worktree placement model (children are placement, not nesting). |
| `.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/p0-phase-report.md:27` | AC-0.7 result: Orca does not depth-check `worktree create --agent` or `agent launch`. Only WC-13 guards them. |
| `~/.claude/skills/orchestration/SKILL.md` (symlink to `~/.agents/skills/orchestration`) | Orca discovery stub. The real guide comes from `orca-ide skills get orchestration` and was not inspected. |
| `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` section 7.7 (`:972`) | Developer summary of the coordinator/worker model. It says the coordinator is "never one that Orca started as a worker" (`:978`). |
| `tests/skills/test_worker_contract.py` | Pins the contract text, so any contract change found by the evaluation must update it. |
| Orca `nestedWorkerMaxDepth` (profile `local-default`) | Machine-wide depth setting, currently 1. Raising it affects every Orca run. |
| Issues #339, #423, #431 (all OPEN) | #339 is the unbuilt v1 `/sc:orchestrator` and sketches a narrowing grant token for sub-orchestrators. #423 is v2. #431 is the coordinator liveness bug. |

## Analysis

- [analysis/analyze-orchestration.md](analysis/analyze-orchestration.md): deep architecture pass, Glob, Grep and Read only, because codegraph and Auggie were unavailable. Findings: F1 HIGH, the #449 role is undefined in the contract; F2 HIGH, there is no upward reporting channel for a session that can delegate; F3 MEDIUM, Orca does not fence `agent launch` or `worktree create --agent`; F4 MEDIUM, the depth setting is machine-wide; F5 MEDIUM, grants, Rulings and merges are undefined for a middle layer; F6 LOW, the hook cannot tell a coordinator from a worker; F7 INFO, `/sc:orchestrator` (#339) is not built yet.
- [accuracy-check.md](accuracy-check.md): verdict out_of_date, with the evidence for each claim.
