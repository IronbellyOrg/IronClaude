observation-kind: trace
producer-count: 1 (scoped to the stated symptom: an empty plain tab that Orca starts about 2-3 s after an agent's `orca worktree create` without `--agent`; the observation is a UI state plus a daemon row, not a grep-able token, so rows are enumerated from source and captured joins, not from a token grep; grep-hit count n/a)

## Producers
| id | line | statement | exit statement | before/after started marker | wall-time compatible | cheap observable | surviving |
|----|------|-----------|----------------|-----------------------------|----------------------|------------------|-----------|
| P1 | /home/coder/workspaces/IronOrca/src/main/runtime/runtime-local-worktree-terminal-startup.ts:202 | `shouldSeedWorktreePrimaryTerminal(...)` true when the create carries no agent, then `ports.createTerminal(id, { surfaceOwner: false })` with no startup command: a plain shell (local IronOrca checkout HEAD dc57b3d6e8; equality with installed 1.4.245-aidev02 not proven; installed help N2 says "creates the worktree and its first terminal") | none cited | after the create command (daemon row 2-3 s later, N6/N8) | yes | daemon.log `startup-command-delivery hasCommand=false` (N8) | yes |

## Out of scope for this run (empty-tab producers from the prior run that do not follow a bare create)
Carried from .dev/troubleshoot/bug-orca-orchestrator-spawn-new-sessions-terminal-20261107235513/producers.md: `orca terminal create` (P2 there), UI New Terminal / Mod+T (P3 there), a failed or stalled `--agent` start (P4 there). They can explain empty tabs that have no preceding bare create (for example fix-flaky-parallel-thread-test term_ee0007a6/term_9fe9e46e beyond the first, Ironeye term_6c4f59e4) and are not part of this symptom. Not excluded, not ranked; outside this run's observation.

## Callers that reach P1 (not producers; why the bare create is issued)
| caller | evidence | instances |
|---|---|---|
| Agent following CLAUDE.md:308 / :320 for its own checkout, then `cd` into it | tier1-observation.md N1 | 11 of 17 |
| Agent bare create, then a separate new terminal for another session (`orca terminal create`, worker-start, prompt send) | N1 + N8 (seeded false row then a separate true row) | 5 observed in daemon log |
| /sc:issue claim, orca_worktree.py:594-610 bare create then :951-954 `agent launch` (design D2) | wave1_6-branch-A.md | 0 observed in this run's captures (pending) |
