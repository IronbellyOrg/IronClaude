# Hypothesis: a failed or stalled `--agent claude` start (P4/P5) cannot leave an empty plain terminal with an orchestrator that is not told. The empty shell is the P1 seed tab left beside the Claude tab by create-then-launch.

(Returned by troubleshoot-analyst, persisted by the parent; HTML entities decoded, wording kept, some Evidence lines tightened by the parent.)

**Agent**: root-cause-analyst (lens: Tier 2, complementary to the Tier 1 card)
**Tier**: 2
**Timestamp**: 2026-11-08T00:12:39Z (parent-stamped; the worker wrote "2026-11-08")
**Cause class**: Wrong producer assumed. The triage-checklist.md label is not verified, because the worker did not Read that file.
**Claim class**: `runtime_behavior`. The claim rests on Orca control flow and PTY semantics.
**Evidence class**: `source_static`. This worker has no shell, and the reporter's run was never supplied.
**Verdict direction**: `REFUTE` (of P4/P5 as the cause of an unreported empty tab)
**Consistency with docs**: aligned. The ccsession README says a Ctrl+C in the shim returns you to the shell. It also says Orca fails a supervised worker whose Claude is not ready within 60 seconds.
runs-in=unknown

## Claim

Every launch-failure route found through `worker-start --agent claude` or `agent launch --agent claude` returns a failure or unknown receipt to the caller. None leaves an empty terminal that the orchestrator is not told about. The only way a launch leaves a bare shell tab is that Claude exits after being typed into a shell Orca keeps alive; the receipt is then still `failed` or `outcome_unknown`. The next-most-likely source of an empty `hasCommand=false` tab is therefore the P1 seed shell from a bare `worktree create`. A later `worker-start` or `agent launch` into that worktree adds a new terminal and never adopts the seed. The "waiting orchestrator" is not explained by any Orca path read.

## Evidence

- Producers: P1 surviving (`producers.md` row P1). P4 and P5 are narrowed, not excluded, because a shell tab can survive an exited Claude (local-pty-shell-ready-startup-command.ts:45).
- E1, recovery shell (P5) is rare and reported. `/home/coder/workspaces/IronOrca/src/main/agent-launch/agent-launch-executor.ts:177-182` runs `recoverCreatedWorkspace` only when `!surfacePublished`, the target is not `existing`, and a worktree id is known; the block then does `throw error`. Terminal mode publishes its surface at lines 94-107, so no recovery shell is made there. `/home/coder/workspaces/IronOrca/src/main/runtime/rpc/methods/orchestration/worker/worker-worktree-creation.ts:121-123` throws when agent-first create returns no terminal, without a recovery shell.
- E2, the orchestrator is told. `/home/coder/workspaces/IronOrca/src/main/runtime/rpc/methods/orchestration/worker/local-worker-start.ts:226-258` throws "Agent did not become ready" with the status; lines 299-312 pass it to `failWorkerStartWithReceipt`. worker-start-receipt.ts:86-112 returns `state`, `failedStage`, `lastError`, `effects`, and a `worker-release` recovery hint. An unobserved turn returns `outcome_unknown` with `nextCommands` (worker-start-readiness-settlement.ts:107-146).
- E3, the tab survives an exited Claude. local-pty-shell-ready-startup-command.ts:45 says "Keep the interactive shell alive after agent exit". README (ccsession-tag/README.md:256-257): Ctrl+C makes `ccsession-orca` exit 130 and "you are back at the shell".
- E4, create-then-launch adds a tab. worker-topology.ts:67-76 calls `createTerminal` with `startupAgent`, so a new terminal is created; nothing in the files read adopts the seeded shell. tier1-observation.md O2 records a `hasCommand=false` session at 23:52:18 and a `hasCommand=true` session at 23:52:23 in the same worktree (parent-captured, not the reporter's run).
- E5, other producers excluded: the built-in coordinator makes a plain terminal at `/home/coder/workspaces/IronOrca/src/main/runtime/orchestration/coordinator.ts:257-264`, but its entry point `orchestration.run` is retired (`/home/coder/workspaces/IronOrca/src/shared/orchestration-rpc-contract.ts:45`; fence test orchestration-contract-fence.test.ts:106-125 expects `command_retired`; the worker Read the test, not the dispatcher). `worker-start --terminal` onto a plain shell is refused (explicit-worker-terminal-validation.ts:49-54).
- behaviour-definition: rows 2, 3, 4 and 5 (behaviour-definitions.md). Row 5 is `recalled, not load-bearing` (a code comment); no headline here depends on it.

## Proposed Fix

Not applicable. This is a refutation card; the Tier 1 CLAUDE.md edit already covers P1. The discriminating observation is below.

## Confidence

Self-reported confidence: 0.45. The card is `runtime_behavior` with `source_static` evidence (0.65 cap), lowered by the open items.
- Evidence grounding: 0.5 — source Read, reporter's run not seen.
- Runtime check: 0.0 — no executed reproducer; `runs-in=unknown` caps at 0.5.
- Symptom coverage: 0.5 — accounts for the empty tab, not for the orchestrator waiting.
- Reproducibility fit: 0.5 — the O2 pair has the right shape but cannot be tied to an orchestrator.
- Fix directness: 0.5 — no code fix, only a pending measurement.
- Domain coherence: 1.0 — fits the terminal and agent-launch separation in the Orca source.

## Risks

- If the reporter's CLI call timed out before Orca replied, the orchestrator never saw the receipt (`ORCHESTRATION_WORKER_START_CLIENT_GRACE_MS` and the CLI timeout path were not Read).
- `agent launch` for an existing worktree (`/home/coder/workspaces/IronOrca/src/main/runtime/rpc/methods/agent-launch-surfaces.ts:142`) was not Read; it may reuse an empty seed tab, which would weaken E4.

## If I'm wrong, it's probably because...

The orchestrator ignored a `failed` or `outcome_unknown` receipt, or timed out before it arrived, so P4 happened and went unnoticed; or the user opened the tab with Mod+T (P3).

## Falsification standard

Pre-registered, parent-run, read-only: list the reporter's `worker-start` receipts and `worker-list` states (`failed`, `start_unknown`, effects with `role: 'recovery_shell'`) for the failing window. The claim is false if a dispatch shows `recovery_shell`, `failedStage` or `outcome_unknown` at the time of the empty tab and the orchestrator transcript shows it never read the receipt; also false if a transcript shows a `worker-start` or `agent launch` with `--agent claude` and no `worktree create` before the empty tab.

## Evidence classification

- **Claim class**: `runtime_behavior`
- **Evidence class**: `source_static`
- **Runtime check performed?**: no — no shell, failing run missing.
- **If REFUTE verdict, coverage statement**: Inspected: the executor, the created-workspace recovery, both worker-start factories, `local-worker-start`, the receipt and readiness settlement, the worktree-create startup, typed-command delivery, the coordinator and its retirement, explicit-terminal validation. Not inspected: the CLI client timeout, `agent-launch-surfaces.ts`, the dispatcher that enforces the retirement fence, `isTerminalRunningAgent`. Any of these could flip the verdict.

## Alternatives considered

- Shim exits (ccsession-orca). `agentCmdOverrides` is `{}` in `/home/coder/.config/orca/profiles/local-default/orca-data.json` (one grep match); the shim may not be in the launch path on this host. A second profile and the sqlite export were not checked.
- A 30-second name question inside the 60-second window: a timeout there is reported as `Agent did not become ready`, so not silent.
- Mod+T (P3): open and unverified.

## Grounding gaps

- No transcript of the reporter's run exists; nothing here was observed in it.
- The local IronOrca checkout (HEAD `dc57b3d6e8`) may differ from the installed 1.4.245-aidev02.
- Suggested menu rows: P5 (recovery shell, narrowed with the E1 lines), P6 (retired coordinator, excluded at orchestration-rpc-contract.ts:45), P7 (`--terminal` onto a plain shell, excluded at explicit-worker-terminal-validation.ts:49-54).
- Diagnosability: partial. Rows M-P3, M-P4 and M-USER are pending.
