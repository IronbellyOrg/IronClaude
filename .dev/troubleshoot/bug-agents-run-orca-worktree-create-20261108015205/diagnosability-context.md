# Diagnosability Context Card

**Issue**: Agents run orca worktree create without --agent, leaving empty plain terminals
**failing_component**: CLAUDE.md:303-325 (worktree instruction; text) and the Orca create path it drives (IronOrca runtime-local-worktree-terminal-startup.ts:202-214, external); in-repo code caller src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
**Verdict**: partial
**Complexity**: trivial (score 0: type bug, no intermittent/performance keywords, no scope, cause class Other/instruction gap)
**Hard-stop fired**: false
**Round**: 1 of 3 (authoritative counter unchanged; discriminator-required: no)
**Captured bytes (failing run)**: n/a (audit-time only; external captures are transcripts and daemon.log, quoted in tier1-observation.md)

## 3-W's coverage

| W | Answerable | Evidence |
|---|------------|----------|
| When  | yes | Transcript Bash timestamps (N1) joined to daemon `startup-command-delivery` rows 2-3 s later (N6, N8); both are files that reach disk |
| Where | yes | The exact command and worktree in each transcript row (N1); the daemon row names the worktree in its sessionId (N8) |
| Why   | partial | The creating session's next commands show intent (11 of 17 `cd` into the checkout; 5 hand off in a new terminal); the agents' reasoning text was not read |

## Branch A — Log-call inventory

Total: 7 hits in orca_worktree.py (print: 1 | exception_handler: 5 | logger_call-like Outcome.fail: 1 counted with handlers; error_reporter_init: 0). Richness: rich 2 | minimal 5 | silent 0. CLAUDE.md is text with no instrumentation. The script never lists, reuses or closes the seeded terminal and drops the create's `--json` output on success (orca_worktree.py:594-613). `degraded`: true.

## Branch B — Log-config reachability

No logging config; env vars SC_ORCA_TIMEOUT and SC_ORCA_SHIM_INTERVAL only. Records (`.dev/issues/<N>/worktree.json`, launch mirror, return contract) reach disk but hold no terminal list. Reachability: reaches_sink 4 | filtered_out 1 (create --json at :608) | unknown 1. `degraded`: true.

## Sufficiency rubric application

Row fired: S4 (When yes, Where yes, Why partial; external sinks reach disk) → `sufficient` with caveat, then capped at `partial` because both branches are degraded (auggie unavailable). S14 does not apply: no layer hides the disputed datum; the daemon rows record it directly.

## Implication for diagnosis confidence

Existing instrumentation: Claude transcripts (every Bash call) and Orca's daemon.log (each tab start, with or without a command).
Gap: nothing in Orca or orca_worktree.py records which caller a seeded tab belongs to; the join is by worktree name and a 2-3 s gap.
Consequence: the mechanism (bare create seeds a plain tab that nothing uses) is directly observed in 7 instances; the agents' reasons are inferred from their next commands.
Next step: proceed to hypothesis formation; the pending rows concern the fix (closing the seeded tab), not the diagnosis.

## Tasklist reference

/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/.dev/troubleshoot/bug-agents-run-orca-worktree-create-20261108015205/diagnosability-tasklist.md
