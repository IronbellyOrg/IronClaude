# Hypothesis: the empty tab is the plain terminal Orca seeds on a bare `orca worktree create` (P1). The orchestrator's wait is a normal `check --wait` on a worker that sits in a second tab.

(Returned by troubleshoot-analyst, persisted by the parent; HTML entities decoded, wording kept, some Evidence lines tightened by the parent.)

**Agent**: quality-engineer (Tier 2, edge cases)
**Tier**: 2
**Timestamp**: 2026-11-08T00:12:39Z (parent-stamped; the worker has no clock)
**Cause class**: Config / env drift (instruction gap) combined with a misread of the wait symptom
**Claim class**: `runtime_behavior`
**Evidence class**: `source_static`
**Verdict direction**: `AFFIRM`
**Consistency with docs**: aligned. The bundled guide /tmp/orch-skill-guide.md:163-165 names `worker-start` as the normal path; it routes new-worktree placement to `references/placement-and-remote.md` (line 209), which the worker did not read.
runs-in=unknown

## Claim

The empty terminal comes from P1: a bare `orca worktree create` seeds one plain shell. If a `worker-start --agent claude` follows into that worktree, it opens a second tab titled `worker-<taskId>`. The seeded tab stays empty and the orchestrator waits legitimately for `worker_done` from the other tab. No Orca path was found where an orchestrator action puts a worker prompt into a plain shell and then blocks silently; those paths fail loudly. So "empty terminal + waiting orchestrator" does not show that Claude failed to start.

## Evidence

- Producer P1 (surviving, `producers.md` row P1), CLAUDE.md:308. Seeding rule: `shouldSeedWorktreePrimaryTerminal` and `runtime-local-worktree-terminal-startup.ts:202-214`, quoted in tier1-observation.md ("Behaviour definitions").
- Exit for "worker-start --terminal into a plain shell": `/home/coder/workspaces/IronOrca/src/main/runtime/rpc/methods/orchestration/worker/explicit-worker-terminal-validation.ts:49-54` throws `agent_unconfigured`; `local-worker-start.ts:122-130` calls it before any effect; `worker-start-validation.ts:59-63` rejects `--terminal` combined with `--agent`.
- Exit for "dispatch --inject into a plain shell": `/home/coder/workspaces/IronOrca/src/main/runtime/rpc/methods/orchestration/runs/dispatch-methods.ts:136-142`, comment "Require a detected agent before injection so a bare shell cannot execute the preamble", then `injectRejectedError(to, 'no_agent_detected')`.
- Second-tab mechanism: `/home/coder/workspaces/IronOrca/src/main/runtime/rpc/methods/orchestration/worker/worker-topology.ts:67-76`: for an existing worktree `createExistingWorktreeWorkerTerminal` calls `createTerminal` with `startupAgent: args.agent` and `title: worker-${taskId}`; it does not reuse the seeded tab.
- Wait cases: `worker-start-readiness-settlement.ts:107-147` returns `outcome_unknown` / `turn_start_unobserved` for a prompt whose turn start was not seen; the guide says keep waiting (/tmp/orch-skill-guide.md:145-161).
- No agent-facing New Terminal action: `tab.newTerminal` is Mod+T at `/home/coder/workspaces/IronOrca/src/shared/keybindings/definitions-core-2.ts:69-74`; its renderer users are `terminal-workspace-keydown.ts:71`, `use-tab-bar-runtime-model.ts:99` and floating-panel shortcut files; a grep of `src/main` finds no `newTerminal` outside daemon history metadata. `QuickLaunchButton.tsx:79` calls `launchAgentInNewTab` (launches agents, not plain terminals). The CLI path is the RPC `terminal.create` (`src/cli/handlers/terminal.ts:202`). `tab.newAgent` has no Linux default (definitions-core-2.ts:83-87). "Shortcut" is therefore a human keypress or a description of the tab type.
- behaviour-definition: rows 1, 2 and 3 (behaviour-definitions.md).

## Proposed Fix

Edit the worktree paragraph of the repo-root CLAUDE.md (lines 308 and 320): a worktree that will host a supervised Claude worker must not be made with a bare `orca worktree create`; use `orca orchestration worker-start --worktree new-top-level --name <n> --agent claude`, or `worktree create --agent claude`. Both suppress the seeded plain tab (the worker-created worktree passes `startupAgent`, `worker-worktree-creation.ts:85-93`, so `callerProvidesInitialSurface` is true).
- `/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/CLAUDE.md` — the added sentence.
- Verification: `grep -n -- "new-top-level" CLAUDE.md` shows the sentence; a fresh run leaves `orca terminal list --json` with no untitled plain tab beside the worker tab.

## Confidence

Self-reported confidence: 0.40 (`runtime_behavior` with `source_static`, 0.65 cap, lowered: reporter's run never observed).
- Evidence grounding: 0.5 — exits and the second-tab path Read, not as the reporter's run.
- Runtime check: 0.0 — no executed reproducer; `locus_unknown` caps at 0.5.
- Symptom coverage: 0.5 — explains both halves, but "waiting" rests on the absence of any silent-stall path.
- Reproducibility fit: 0.5 — the seed is reproduced once (O3/O4); coexistence of an empty tab and a worker tab is not.
- Fix directness: 0.5 — targets the instruction, cannot force an LLM's choice.
- Domain coherence: 1.0 — fits O3/O4: all supervised worker tabs are Claude, the empty tabs belong to bare-created worktrees.

## Risks

If the reporter's worker really never started (P4 or `outcome_unknown`), the edit changes nothing for them. `/sc:issue --claim` deliberately creates without `--agent` (`orca_worktree.py:27,42` in `src/superclaude/skills/sc-issue-protocol/scripts/`), so the wording must allow that two-step path.

## If I'm wrong, it's probably because...

`worker-start` or `agent launch --agent claude` failed after the worktree existed; the recovery shell (`worker-start-agent-placement.ts:115-126`) left the empty tab, and the guide's "do not relaunch / keep waiting" rules (/tmp/orch-skill-guide.md:122-124, 145-147) kept the orchestrator blocked (P4, the Tier 1 alternative).

## Falsification standard

# Discriminator: does a worker tab exist beside the empty tab?
Hypothesis A (this card): a `worker-<taskId>` tab titled "Claude Code" exists in the same worktree as the empty plain tab, and the worker is alive.
Hypothesis B (Tier 1 / P4): no worker tab exists; the only tab is the plain one, or a `recovery_shell` effect appears in the `worker-start` receipt.
Observable that differs: presence of a tab titled `worker-<taskId>` in `orca terminal list --json` for that worktree (`worker-topology.ts:73` sets the title).
Exact probe: `orca terminal list --json` filtered to the affected worktree (read-only). A complete capture reduces to true or false; an empty or errored capture is unobserved.
Primitive under dispute, fetched verbatim: `createExistingWorktreeWorkerTerminal` at `worker-topology.ts:67-76` (tier1-observation.md, row 2).
Reference-context value: n/a (first instrumented run). Counter-case O3: `install-core-stale-warning` shows `false` (plain tab only).
| Probe result | A | B |
|---|---|---|
| true | consistent | refuted: a worker tab exists, so the worker started |
| false | refuted for that worktree | consistent (a user-created worktree with no worker also gives false) |
Falsifier: "If a `worker-<taskId>` tab exists in the worktree and its worker is live, B is false." If no such tab exists, A is false for that worktree.

## Evidence classification

- **Claim class**: `runtime_behavior`
- **Evidence class**: `source_static`
- **Runtime check performed?**: no — no shell, no failing-run capture.
- **If REFUTE verdict, coverage statement**: Not applicable (AFFIRM).

## Alternatives considered

- P2 (`orca terminal create` then `terminal send`): not excluded; only inject and `--terminal` into a plain shell are excluded, at the file:lines above.
- P3 (human Mod+T): not excluded; the only evidence is the absence of any main-process caller.
- P4: the strongest rival, under "If I'm wrong".

## Grounding gaps

- Cheapest observation: `orca terminal list --json` for the affected worktree (live state, no new run); the empty tabs should still exist. From Claude transcripts alone (`orca` Bash tool_use inputs in the 60 s before the tab appeared), P1, P2 and P4 are separable by command text (bare create / `terminal create` / `--agent claude` plus a non-zero receipt with `recovery_shell`). The reporter's session is not yet identified (O4: 9 bare creates and 0 `terminal create` since 11-05). daemon.log cannot separate them (no caller field, O2); P3 shows only as a `hasCommand=false` row with no matching Bash call within about 5 s.
- The local skill at `/home/coder/workspaces/IronOrca/skills/orchestration/SKILL.md` differs from the bundled guide at /tmp/orch-skill-guide.md (no `references/` directory; a grep for `--terminal|inject` returned nothing). The bundled guide was treated as what orchestrators follow.
- Only grep lines of `worker-worktree-creation.ts` were read; not `createWorkerWorktree`'s full body, `placement-and-remote.md`, or the `agent launch` CLI default for `--surface`.
- No transcript of the reporter's failing run exists; nothing is claimed from it. Diagnosability verdict: partial.
