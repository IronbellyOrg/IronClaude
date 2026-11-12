# /sc:analyze orchestration --focus architecture --depth deep (issue #444)

- Scope: the coordinator/worker model a sub-orchestrator or coordinator mode would change. Files: `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/core/CLAUDE.md` (Orca block), `CLAUDE.md` (worktree rule), `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh`, `~/.claude/skills/orchestration/SKILL.md`, `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` section 7.7, and the decision record `.dev/orca-command-refactor/` (spec, D5, CR-01, APPROVED.md).
- Checked at: `origin/master` 0423fe5f (worktree HEAD 6f6c46aa), 2026-11-08.
- Tools: Glob, Grep and Read only. Codegraph and Auggie tools were not available to this worker. The Orca binary guide (`orca-ide skills get orchestration`) was not run, so Orca's runtime behaviour is cited only from the repo's own recorded evidence.
- Read-only. No source was changed.

## 1. What exists today

| Piece | Where | What it says |
|---|---|---|
| One coordinator, opened by the person | `WORKER-CONTRACT.md:69`; dev guide `:978` | "an Orca coordinator session the person opened". The dev guide adds "never one that Orca started as a worker". |
| Worker = one command, no fan-out | `WORKER-CONTRACT.md:5,62` | WC-13: the worker session never calls `worker-start`, `dispatch`, `task-create`, low-level dispatch, `worktree create --agent` or `agent launch`, "at any depth setting". Extra work goes in the `worker_done` body and the coordinator decides. |
| Commands never call Orca | `WORKER-CONTRACT.md:40` (WC-8); dev guide `:980,1005` | Fan-out inside a command stays as Agent-tool subagents. |
| Decision D5: nesting depth stays 1 | `.dev/orca-command-refactor/decisions/D5/RECOMMENDATION.md:7-10,44-50`; `APPROVED.md:12`; spec `:405` | Option (a) won 0.827 to 0.694. Option (b), "raise to exactly 2, scoped, `Sub-workers: allowed, max N` in the brief", is the closest earlier design to this issue's `--sub`. Revisit only when a composite brief type exists and run notes record a split that was knowable only at run time and whose extra round trip was material. |
| Revisit evidence is collected | `WORKER-CONTRACT.md:246` | The coordinator records each follow-up Task it created because a worker found unplanned work, with the extra time that cost. "This is the evidence decision D5's revisit trigger reads." |
| AC-0.7 trace done (P0) | `.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/p0-phase-report.md:18,27` | PASS. `task-create`, `worktree create --agent` and `agent launch` are not checked against depth in Orca's installed code. Only WC-13 and the 7.2 step-5 transcript check cover them. |
| PR #449: every worktree gets an agent | `src/superclaude/core/CLAUDE.md:55-59`; `CLAUDE.md:305,312`; hook `require-orca-worktree-agent.sh:2-8,354` | "The session that creates a worktree becomes its orchestrator, or a coordinator under another orchestrator, and owns its agent(s)." The hook enforces only `--agent`. Ownership and "no worktree for your own use" are instruction text only (hook `:7-8`). |
| Child worktrees are placement, not nesting | `WORKER-CONTRACT.md:91,218-225`; `CR-01-feature-worktree-hierarchy.md` | The coordinator starts workers in children with `worker-start --worktree new-child`, merges them back and removes them. Every worker stays at depth 1. |
| Orchestration skill | `~/.agents/skills/orchestration/SKILL.md:16-18,51-53` | Discovery stub only. The IronClaude rules are in the contract, not in this skill (dev guide `:981`). |
| Proposed `/sc:orchestrator` | issues #339 (v1), #423 (v2), #431 (liveness bug), all OPEN | No command, skill or spec file exists. #339 sketches an "orchestrator-of-orchestrators in version 2" with grant tokens that each level can only narrow. |

## 2. Findings (severity-rated)

### F1. HIGH: the role named in PR #449 has no definition in the contract

`src/superclaude/core/CLAUDE.md:55-59` (installed to every project) says a worktree's creator may be "a coordinator under another orchestrator". `WORKER-CONTRACT.md` section 4 binds only a person-opened coordinator (`:69`), and D5 makes "coordinator is a person-opened session" a precondition (`D5/RECOMMENDATION.md:9,47`). So two installed core files describe the hierarchy differently. A session launched by a top coordinator with `worktree create --agent` or `agent launch`, rather than `worker-start`, gets no Task or Dispatch ID. Under the contract's Terms it is therefore an "ordinary session" (`WORKER-CONTRACT.md:11`), not a worker. WC-13 does not bind it, and no coordinator rule binds it either. This is the gap the issue must close first: either define the sub-coordinator (a section 4 variant) or narrow the #449 wording.

### F2. HIGH: there is no channel for reporting upward from a session that can delegate downward

Lifecycle messages (`worker_done`, `ask`, `check`, heartbeats) exist only for a worker run (`WORKER-CONTRACT.md:11,59-65`). A sub-orchestrator started as a worker has the upward channel but is forbidden to delegate (WC-13). A sub-orchestrator launched as an ordinary agent can delegate (F3) but has no `worker_done` and no Task record the top coordinator can wait on. D5 also lists as unverified which mailbox receives a depth-2 worker's questions and `worker_done`; the sources point to the top coordinator's Run mailbox, not the parent's (`D5/RECOMMENDATION.md:84`). Any coordinator mode has to choose one of these channels and prove where its messages land.

### F3. MEDIUM: Orca does not fence the delegation paths a sub-orchestrator would use

AC-0.7 found that `worktree create --agent` and `agent launch` are not depth-checked by Orca (`p0-phase-report.md:27`). WC-13 is the only guard, and it is enforced after the fact by reading transcripts. This cuts both ways. It unlocks a sub-orchestrator without raising the machine-wide depth setting, through orca-cli launches. It also means nothing mechanical bounds the fan-out of such a sub-orchestrator. D5's "runaway fan-out" concern would then rest on instruction text and a new cap rule, which D5 says a parent running sub-workers would need (`D5/RECOMMENDATION.md:75`).

### F4. MEDIUM: raising the depth setting is machine-wide and possibly one-way

The `nestedWorkerMaxDepth` value is per Orca profile, applies to every run under that profile, and `local-default` is the only profile on this machine. Lowering it while deeper workers run is UNVERIFIED (`D5/RECOMMENDATION.md:38,45,81,83`). A `--sub` that relies on `worker-start` from a depth-1 session would need this raise. That would change the safety floor for every Orca run, not only IronClaude's.

### F5. MEDIUM: who holds authority (grants, Rulings, outward actions, merges) is undefined for a middle layer

- D4: a commit grant must quote the person's instruction word for word and covers one Task (`WORKER-CONTRACT.md:42,233`). Under a middle layer, the sub-orchestrator would write its sub-workers' briefs. D5 notes that whether an authorization passes down "would need a new rule" (`D5/RECOMMENDATION.md:71`).
- D2: only the person gives an `/sc:implement` Ruling. A relay through two coordinators is a second relay path D2 does not define (`WORKER-CONTRACT.md:57`; `D5/RECOMMENDATION.md:69`).
- Git: the coordinator does every push, PR, comment and merge-back, and removes child worktrees (`WORKER-CONTRACT.md:224-234`). A sub-orchestrator that merges its own children breaks WC-9 if it is a worker, and needs its own git-ownership rule if it is not.
- #339's narrowing grant-token model is a candidate answer that has not been designed yet.

### F6. LOW: the #449 hook cannot tell a coordinator from a worker

`require-orca-worktree-agent.sh` blocks any `orca worktree create` without `--agent`, in any session, subagents included (`:4-8`). It does not check who is creating. "The creator owns the agent" and the WC-13 ban on workers creating worktrees remain instruction text. The hook also has known gaps: `bash -c`, `xargs`, and scripts that call Orca as a subprocess all get past it (`:39-61`). A sub-orchestrator mode would need either an identity-aware check or an explicit statement that ownership is instruction-only.

### F7. INFO: the issue's premise depends on unbuilt v1 work

`/sc:orchestrator` (#339) does not exist, and #423 (v2) is explicitly scheduled after #339. Evaluating `--sub` therefore means evaluating a mode of a command that has no design document yet. The D5 debate (`.dev/orca-command-refactor/decisions/D5/debate/adversarial/`) and #339's grant-token sketch are the only prior design material.

## 3. Unlocks and rethinks, as evidence (no decision)

| Item | Evidence | What would have to change |
|---|---|---|
| Unlock: delegation below a feature-level coordinator without raising depth | F3; `CLAUDE.md:312` | Define the sub-coordinator in `WORKER-CONTRACT.md` section 4 with a fan-out cap and an upward reporting channel (F1, F2). |
| Unlock: fewer round trips when a split is only knowable at run time | D5 losing argument, `D5/RECOMMENDATION.md:20` | D5's revisit trigger: a composite brief type and recorded run-note evidence (`WORKER-CONTRACT.md:246`). Whether any such evidence has been recorded since P0 is not known yet. |
| Rethink: WC-13 "at any depth setting" | `WORKER-CONTRACT.md:62` | An exception for a brief that carries a sub-coordinator line, plus the 7.2 step-5 check updated to allow it. |
| Rethink: "coordinator is a person-opened session" | `WORKER-CONTRACT.md:69`; dev guide `:978`; D5 precondition | Either keep the rule and narrow the #449 wording, or allow an agent-launched coordinator and define its depth and mailbox. |
| Rethink: authority chain | F5 | A rule for passing grants down (possibly #339's narrowing tokens), a Ruling path, and merge ownership for the middle layer. |

## 4. Recommendations

1. Treat issue #444 as a design and evaluation task, not implementation: `/sc:brainstorm` or `/tech-research` over the D5 debate, CR-01, `WORKER-CONTRACT.md` section 4 and #339/#423, ending in a written D5-revisit proposal. Any later contract change goes through `/sc:workflow` (level 3), because it would touch `WORKER-CONTRACT.md`, `core/CLAUDE.md`, `CLAUDE.md`, the developer guide and `tests/skills/test_worker_contract.py`.
2. Resolve F1 first. It is a live inconsistency between two installed core files, whatever the evaluation decides.
3. Before relying on any depth-2 design, verify the open items from D5 that AC-0.7 did not close: the mailbox for depth-2 messages (`D5/RECOMMENDATION.md:84`), and whether lowering the depth setting is safe (`:83`).
4. Check the coordinator run notes for recorded follow-up-Task evidence (`WORKER-CONTRACT.md:246`). That evidence is D5's stated gate for reopening the question. Not known yet whether any exists.
