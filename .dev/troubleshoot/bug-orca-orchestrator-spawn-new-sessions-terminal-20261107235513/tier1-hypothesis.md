# Hypothesis: the repo's worktree instruction (CLAUDE.md:308, 320) has orchestrators run `orca worktree create` with no `--agent`, which makes Orca seed an empty plain terminal and start no Claude session

**Agent**: root-cause-analyst
**Tier**: 1
**Timestamp**: 2026-11-08T00:05:30Z (parent-replaced: the worker wrote 2026-11-08T00:20:00Z, a time later than the receipt; protocol rule on model-generated timestamps)
**Cause class**: Config / env drift (an instruction gap plus a stale installed copy), per the triage-checklist.md:27 row. I only grepped that file.
**Claim class**: `runtime_behavior`. The claim depends on what Orca's create path does and on what an LLM chooses to run.
**Evidence class**: `source_static`. The Orca source and repo text were Read. The daemon.log and transcript facts come from the parent's capture and are not the reporter's run.
**Verdict direction**: `AFFIRM`
**Consistency with docs**: aligned. This matches the doc-context.md re-frame signals. CLAUDE.md:307 requires Orca worktrees and says nothing about `--agent`. The #412 rule at src/superclaude/core/CLAUDE.md:45-53 is not installed.
runs-in=unknown

## Claim

`orca worktree create --name <name>` with no `--agent` makes Orca seed one default plain terminal for the new worktree. No Claude session starts. An orchestrator that follows CLAUDE.md:308 and CLAUDE.md:320 literally ends up with an empty terminal tab and a worker that never starts, so it waits. The #412 rule that says "never New Terminal; use `agent launch` or `worktree create --agent`" has not reached the host's installed instructions. Nothing in this repo's own worktree instruction points the orchestrator at `--agent` either.

## Evidence

- Producer P1 (surviving, producers.md row P1, CLAUDE.md:308) — "Create it with `orca worktree create --name <name>`". CLAUDE.md:320 shows the same command with no `--agent` (both Read).
- `/home/coder/workspaces/IronOrca/src/main/runtime/runtime-local-worktree-terminal-startup.ts:202-214` — when there is no startup, setup or default tabs, `shouldSeedWorktreePrimaryTerminal({hasPrimarySurface, callerProvidesSurface})` leads to `ports.createTerminal("id:<worktree>", {surfaceOwner:false})`. That call has no `startupAgent`. `callerProvidesInitialSurface` (lines 259-269) is true only for `promisedAgentChat` or `createdWithAgent` with no activate/runHooks. A bare create has neither, so it seeds the plain shell. The worker did not Read `shouldSeedWorktreePrimaryTerminal` itself.
- Parent-captured, tier1-observation.md O3 and O4 and diagnosability-tasklist.md M-P1 — `install-core-stale-warning` was created without `--agent` (transcript 7fd4f558, 2026-11-07T05:36:13Z; the coordinator repeated the create at 06:15:04Z). The daemon log shows one session with hasCommand=false at 05:36:16Z, and the tab has no "· Claude Code" title. This reproduces the mechanism once. It is not the reporter's run.
- Parent-captured, O5 — ~/.claude/CLAUDE.md, the installed ccsession README and the pipx package all have 0 matches for "Orca session launches". The #412 rule is on origin/master but not installed here.
- behaviour-definition: row 1 (behaviour-definitions.md, status fetched:local-source) — the parent Read `shouldSeedWorktreePrimaryTerminal` at /home/coder/workspaces/IronOrca/src/shared/worktree-first-surface.ts:2-14: it returns `!hasPrimarySurface && (!callerProvidesSurface || ...)`, so a create with no agent seeds the plain terminal. Verbatim text is in tier1-observation.md under "Behaviour definitions". The local checkout's version equality with the installed Orca 1.4.245-aidev02 is not proven.

## Proposed Fix

Edit the worktree section of the repo-root CLAUDE.md (`CLAUDE.md:308` and the example at `CLAUDE.md:320`). Add one sentence: a bare `orca worktree create` leaves only an empty plain terminal. When a Claude session is wanted, add `--agent claude`, or follow with `orca agent launch --agent claude` as `/sc:issue --claim` does (orca_worktree.py:27,42). Never use `orca terminal create` for an agent. The "launch afterward" option is needed because docs/designs/sc-issue-claim-pipeline-flag.md D2 deliberately creates the worktree without `--agent`.
- `CLAUDE.md` (repo root) — the added sentence.
- Verification: `grep -n -- "--agent" CLAUDE.md` shows the new text in the worktree section. A fresh orchestrator then issues `worktree create --agent claude` or `agent launch --agent claude`. Running `superclaude install` so #415 lands in ~/.claude/CLAUDE.md is operational, not part of this edit.

## Confidence

Self-reported confidence: 0.55. The card is runtime_behavior with source_static evidence, so it is capped at 0.65, then lowered because the reporter's orchestrator was never observed.

Per-dimension self-assessment:
- Evidence grounding: 0.5 — the Orca seeding path and the repo text were Read. The reporter's commands were not seen.
- Runtime check: 0.0 — no executed reproducer. Only a parent-captured single case on another worktree. The 0.65 cap applies, and `locus_unknown` caps it at 0.5.
- Symptom coverage: 0.5 — it explains the empty terminal. It explains the waiting orchestrator only if the orchestrator then waits on a worker that was never started.
- Reproducibility fit: 0.5 — a bare create reproduces the empty tab. The orchestrator wait is not reproduced.
- Fix directness: 0.5 — the edit targets the instruction an orchestrator reads. It does not change the choice an LLM makes.
- Domain coherence: 1.0 — it fits the documented #412 gap and the P1 row.

## Risks

- If the cause is a failed `--agent claude` launch (see Alternatives), this edit changes nothing for the reporter.
- Telling agents to add `--agent` could conflict with the `/sc:issue --claim` two-step design. The wording must allow both.
- Native-chat mode would then create a chat session instead of Claude CLI. The #412 rule asks for Claude (CLI).

## If I'm wrong, it's probably because...

A `worker-start --worktree new-top-level --agent claude` or `agent launch` of a newly created worktree failed after the worktree existed, and Orca's recovery shell left the empty terminal.

## Falsification standard

Find the failing orchestrator's transcript (tasklist Task 1) and list its `orca` Bash calls. If it contains a `worker-start` or `agent launch` with `--agent claude` and no bare `worktree create` before the empty tab, P1 is false. If daemon.log shows hasCommand=false within 5 s of a `worktree create ... --agent claude` call, the premise is also false.

## Evidence classification

- **Claim class**: `runtime_behavior` — it depends on Orca's runtime seeding and on LLM command choice.
- **Evidence class**: `source_static` — Read source plus parent-captured logs from a different instance.
- **Runtime check performed?**: no — this worker has no shell, and the failing run was never supplied.
- **If REFUTE verdict, coverage statement**: Not applicable — this is an AFFIRM.

## Alternatives considered

- P2, `orca terminal create`: not excluded. The only evidence is the parent's observation of zero real calls in the transcripts on this host. No exit statement with a file:line, so P2 stays surviving.
- P3, UI New Terminal (Mod+T): not excluded. definitions-core-2.ts:69-75 binds `tab.newTerminal` to Mod+T, and lines 83-87 give `tab.newAgent` no Linux default. A user pressing Mod+T on Linux gets a plain terminal. This is a user-side action, not an orchestrator action.
- P4/P5, `--agent claude` that fails: `recoverCreatedWorkspace` (agent-launch-created-workspace.ts:62-71) calls `createRecoveryShell`. The worker-start factory builds that shell with `runtime.createTerminal("id:<worktree>", {surfaceOwner:false})` and no startup agent (worker-start-agent-placement.ts:115-126). `agent-launch-worktree-creation.ts:35-37` does the same for `agent launch`. The executor only calls it when `!surfacePublished`, the target is not `existing`, and a worktree id exists (agent-launch-executor.ts:177-182). The worker suggests adding this to the menu as P5 (recovery shell).

## Grounding gaps

- **Answer to the Orca-app question.** No path found where `worker-start --agent claude` or `agent launch --agent claude` opens a plain "New Terminal" tab on a successful launch.
  - The mode decision is `decideAgentLaunchMode` (agent-launch-mode.ts:98-165). `--surface terminal` gives a terminal agent (lines 109-115). A default that is not native chat gives a terminal agent with reason `user_default` (lines 122-129). Otherwise a structured chat session (lines 152-164).
  - The executor passes `startupAgent: intent.agent` when the mode is terminal and `undefined` when structured (agent-launch-executor.ts:221). The terminal route is `createTerminalAgent` → `createExistingWorktreeWorkerTerminal` with `startupAgent: args.agent` (worker-topology.ts:59-76).
  - An unset default-agent or "new agent tab" setting only affects the renderer `tab.newAgent` shortcut (terminal-agent-tab-shortcut.ts:32-49). `defaultTuiAgent` has 0 matches under `src/main/.../worker`, so the CLI path does not read it.
- **Not read.** How the Claude startup command string is built; how `agentCmdOverrides` (for example the ccsession-orca shim) is applied to a terminal agent; the `orca agent launch` CLI default for `--surface`. Whether a shim that exits at startup leaves a bare shell tab is unknown.
- No transcript of the reporter's failing orchestrator exists. Diagnosability verdict: partial, see diagnosability-context.md. Rows M-P3, M-P4 and M-USER are pending, so this hypothesis cannot be falsified at runtime until Task 1 runs.
- `shouldSeedWorktreePrimaryTerminal` was not Read by the worker; the parent has since Read it (behaviour-definition row 1).
