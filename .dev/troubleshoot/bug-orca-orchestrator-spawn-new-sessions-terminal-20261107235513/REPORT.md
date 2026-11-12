# Troubleshoot Report

**Target**: An Orca orchestrator keeps opening plain terminal tabs instead of Claude sessions, leaving empty terminals and an orchestrator that waits.
**Type**: bug
**Tier reached**: 2
**Confidence**: 0.30
**Status**: partial
**Escalation reason**: low_confidence
**Test is wrong**: false
**Behavior is documented**: false
**Doc context card**: .dev/troubleshoot/bug-orca-orchestrator-spawn-new-sessions-terminal-20261107235513/doc-context.md
**Duration**: 1814
**Date**: 2026-11-08T00:25:28Z

---

## Summary

No unique cause is established: the report is partial. The reporter's failing orchestrator run was never supplied, and no captured record on this host shows an orchestrator choosing "new terminal" to start a Claude session. What the evidence does show is two verified gaps that make empty plain tabs likely: the repo's own worktree rule never mentions starting a Claude session, and the rule written for this problem (issue #412) is merged but not installed on this host. The missing observation is which `orca` command the failing orchestrator ran; Task 1 and the rows in Next Steps obtain it.

## Documentation Context

- **Relevant refs**: docs/designs/sc-issue-claim-pipeline-flag.md, docs/designs/sc-issue-launch-level-hook.md, docs/designs/sc-issue-command.md, docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md, docs/testing/v5.0.0/user/D08-ccsession.md, CLAUDE.md, docs/user-guide/commands.md, .dev/tasks/done/TASK-WF-fixIssue412SVeri-20261106-215543/
- **Documented behavior**: new Claude sessions are started with `orca agent launch` or `worktree create --agent`, never a plain terminal; `terminal create` is for shells; `/sc:issue --claim` deliberately creates its worktree without `--agent` and launches Claude in a second call.
- **Restrictions honored**: any fix keeps Orca-only worktree creation (CLAUDE.md:307, :312) and the supervised `worker-start` carve-out (src/superclaude/core/CLAUDE.md:52).
- **Restrictions overridden**: None
- **Card path**: .dev/troubleshoot/bug-orca-orchestrator-spawn-new-sessions-terminal-20261107235513/doc-context.md

## Diagnosability Context

**Verdict**: partial
**Complexity classification**: non-trivial
**Captured-bytes (failing run)**: n/a

Existing instrumentation: Orca's daemon log (tab start with or without a startup command) and Claude transcripts (every Bash call). Gap: nothing joins "tab created" to "who asked", and no transcript of a failing orchestrator run was supplied. Consequence: any statement about what the orchestrator chose is inference. No hard stop: failing_component is not localizable to code (S12), and the discriminator trigger raised the verdict to partial. Round 1 of 3.

(Full card: /home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/.dev/troubleshoot/bug-orca-orchestrator-spawn-new-sessions-terminal-20261107235513/diagnosability-context.md)
(Tasklist (informational): /home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/.dev/troubleshoot/bug-orca-orchestrator-spawn-new-sessions-terminal-20261107235513/diagnosability-tasklist.md)

## Diagnosis

**Root cause**: UNDETERMINED — among {CLAUDE.md:308, orca terminal create --help (tier1-observation.md O1), src/shared/keybindings/definitions-core-2.ts:69 (IronOrca), orca orchestration worker-start / agent launch --help (tier1-observation.md O1)}

**Cause class**: Config / env drift (instruction gap plus stale installed copy), unchanged from the Tier 1 card; not established as the cause.

**Falsifiers** (rows of diagnosability-tasklist.md, predictions copied unchanged):
- Core M-P1: observed. True-case value seen (one daemon session, hasCommand=false, no Claude session, for a worktree made with a bare `worktree create`). Consistent with P1 making an empty tab; it does not show any orchestrator waited on it.
- Core M-P2: observed. Zero real `orca terminal create` calls in the scanned transcripts; refutes P2 for those transcripts only.
- Core M-P3: pending (could-not-run: artifact-only). Predictions: true = no agent `orca` call within 10 s before each empty tab; false = such a call exists. Spot check for the 23:52:18Z empty tab found no matching call. Missing: the 24 h join.
- Core M-P4: pending (could-not-run: no failing run named). Predictions: true = the tab screen shows a bare shell; false = it shows Claude Code.
- Core M-QE: pending (could-not-run: failing worktree not identified). Reference-context value `true`, observed on worktree liveness-v1-contract (a live worker tab titled "· Claude Code", tier1-observation.md O3). Predictions: true = a tab titled "· Claude Code" exists in the affected worktree (A consistent, B refuted); false = A refuted, B consistent. A screen read of that tab is a supplementary check, not part of the boolean.
- Core M-USER: pending (needs the failing orchestrator's session or tab). Missing: its list of `orca` commands.
- Control M-C: observed, consistent (supervised worker tabs end "· Claude Code"); CONTROL-PROOF unknown.

**Detailed explanation**: rows M-P1, M-P2 and M-C were run this round (captured spans in .dev/troubleshoot/bug-orca-orchestrator-spawn-new-sessions-terminal-20261107235513/tier1-observation.md); M-P3, M-P4, M-QE and M-USER remain. No mechanism narrative is given for a producer that has not been discriminated.

## Evidence

1. `CLAUDE.md:308` — "Create it with `orca worktree create --name <name>`, adding `--repo <selector>`, `--base-branch <ref>`, and" and `CLAUDE.md:320` — `orca worktree create --name pm-agent --base-branch origin/master` (neither shows `--agent`).
2. `/home/coder/workspaces/IronOrca/src/shared/worktree-first-surface.ts:2-14` — `shouldSeedWorktreePrimaryTerminal` returns `!args.hasPrimarySurface && (!args.callerProvidesSurface || ...)`, so a create with no agent seeds a plain terminal (local IronOrca checkout; equality with the installed Orca 1.4.245-aidev02 is not proven).
3. `/home/coder/workspaces/IronOrca/src/main/runtime/rpc/methods/orchestration/worker/worker-topology.ts:67-76` — a `worker-start` into an existing worktree calls `createTerminal` with `startupAgent: args.agent` and `title: worker-${args.taskId}`, a new tab, not the seeded one.
4. `/home/coder/workspaces/IronOrca/src/main/runtime/rpc/methods/orchestration/worker/worker-start-receipt.ts:101` — `recovery: \`This start created a terminal that never ran the Task. Close it with: orca orchestration worker-release --dispatch ...\`` (a failed start is reported to the caller).
5. `/home/coder/workspaces/IronOrca/src/main/runtime/rpc/methods/orchestration/worker/explicit-worker-terminal-validation.ts:49-54` — `worker-start --terminal` onto a terminal that is not running an agent throws `agent_unconfigured`.
6. `src/superclaude/cli/install_core.py:70-72` — `if dest_file.exists() and not force: skipped.append(src_file.name); continue`.
7. `src/superclaude/core/CLAUDE.md:47` — "For a new ccsession-backed Claude session, choose **Claude (CLI)**, never **New Terminal**." (the #412 rule, lines 45-53).
8. Command: `grep -c "Orca session launches" ~/.claude/CLAUDE.md` → `0` (also 0 in ~/.claude/skills/ccsession-tag/README.md and in the pipx package built 2026-11-05).
9. Command: `jq` over ~/.config/orca/logs/daemon.log for sessions of worktree install-core-stale-warning → `2026-11-07T05:36:16.234Z startup-command-delivery false 0` and one `session-created`, no command-bearing session.
10. `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:27` — "``orca worktree create`` (no link flag, no agent flag)," and `:42` — "``orca agent launch --surface terminal`` with a prompt that starts with".
11. `/home/coder/workspaces/IronOrca/src/shared/keybindings/definitions-core-2.ts:69` — `id: 'tab.newTerminal'`, default binding `Mod+T` at line 74.

## Proposed Fix

No causal fix established. Next discriminating observation: the failing orchestrator's own `orca` commands (Task 1, rows M-USER and M-QE).

Conditional proposals, each with its validation prerequisite; none is applied and none is a causal fix:
- **F1 (instruction wording)**: add one sentence next to `CLAUDE.md:308` and `:320` saying a bare `orca worktree create` leaves only an empty plain terminal, and that a Claude session needs `--agent claude` or a following `orca agent launch --agent claude`, while allowing the `/sc:issue --claim` two-step path. Helps only if the reporter's run used a bare create (M-USER).
- **F2 (delivery)**: make `superclaude install` insert the marker-delimited Orca block into an existing ~/.claude/CLAUDE.md, since `install_core.py:70-72` skips it today. Helps only if the rule being absent changed the orchestrator's choice.
- **Operational, no code change**: reinstall the package from the fork, diff ~/.claude/CLAUDE.md against src/superclaude/core/CLAUDE.md, then run `superclaude update` (overwrites that file). A plain `superclaude install` does nothing for an existing file.

## Alternative Fixes Considered

- **No fix (the root-cause-analyst card)**: a failed `--agent claude` start does not leave an unreported empty tab (the receipt names a terminal "that never ran the Task"). Kept as a narrowing of P4, not an exclusion: the CLI client timeout and the `agent launch` path were not read.
- Wave 4 (adversarial debate) was not run: no two strong competing fixes exist (every card calibrated 0.30), F1 and F2 act on different layers, and P1 versus P4 is decided by the probe M-QE.

## Risk + Rollback

- **Likelihood of regression**: low in the instruction text (F1); medium in `install_core.py` (F2, edits a user-owned file).
- **Test coverage of the changed code**: none for F2 until a test is written; F1 is text only.
- **Rollback**: `git revert` for F1 and F2; for the `superclaude update` step, restore the diffed copy of ~/.claude/CLAUDE.md taken beforehand.

## Follow-up tasks

- Add `--agent claude` guidance to the worktree section of CLAUDE.md. Suggested type: docs. Evidence: CLAUDE.md:308.
- Make a plain `install` upsert marker-delimited blocks in existing core files. Suggested type: bug. Evidence: src/superclaude/cli/install_core.py:70-72.

## Grounding Gaps

- No transcript or tab of the reporter's failing orchestrator exists; nothing here was observed in it. Transcripts not on this host or deleted are unobserved.
- All Orca source citations are from the local IronOrca checkout (HEAD dc57b3d6e8); equality with the installed 1.4.245-aidev02 is not proven.
- auggie was not available in this session; grounding used Grep, Read and jq. The Wave 1.6 branch workers were not run (no localizable component).
- Not read: the Orca CLI client timeout path, `agent-launch-surfaces.ts`, `isTerminalRunningAgent`, the retirement dispatcher, how Claude's startup command and the ccsession-orca shim interact on this host.
- The `/tmp/orch-skill-guide.md` file used as "what orchestrators follow" is the bundled `orca skills get orchestration` text; the local IronOrca skill source differs.
- The pipx-installed package was checked only by grep for the rule text (0 matches), not read.
- Branch B currency verdicts rest on checkout-time mtimes (all equal), so "current" means no Status markers, not verified freshness.
- Evidence validation (evidence-validation.md; first attempt kept in evidence-validation-attempt1.md): 12 of 12 numbered file:line citations matched. Attempt 1 raised two structural failures (the M-QE reference value was not a single literal; the execution-locus run site was still unresolved). Both were repaired and did not recur. Assertion A5 (`consensus_on_unobserved`) fires under its literal reading because every calibration declares `source_static` evidence; it contributes `partial` and changes no claim here. One detail (the named reference worktree in row M-QE) lacked a recorded capture at validation time; the parent then recorded the capture in tier1-observation.md O3 without a third validation pass.
- The four calibration files still quote the earlier `RUN-SITE: pending-producers`; they predate the locus repair.

## Next Steps

Pending rows from diagnosability-tasklist.md (the report stays `partial` until they resolve):
- Core M-USER: the report stays `partial` until the failing orchestrator's `orca` command list shows a `worktree create` without `--agent` (then P1 holds), a `terminal create` call (then P2 holds), or no `orca` call at all (then P3, a human keypress, holds). Task 1 obtains it from the transcript.
- Core M-QE: the report stays `partial` until, for the affected worktree, a tab titled "· Claude Code" exists (then B, a failed start, is refuted) or none exists (then A is refuted for that worktree); read that tab's screen as a supplementary check.
- Core M-P3: pending the 24 h join of daemon `hasCommand=false` starts against transcript `orca` calls; no agent call within 10 s of an empty tab keeps P3 (a human keypress) alive.
- Core M-P4: pending a read of each `unverifiable` worker tab's screen; a bare shell prompt keeps P4 alive.
- Enabling Task 1 (name the failing orchestrator; links M-USER, M-P2, M-P3) and Task 2 (title every `orca terminal create` so tab titles show the caller; links M-P3). Rollback: remove the flag.

Recommended action: give this session the failing orchestrator's session id, or tell me which tab it is, so M-USER can run against its transcript. Meanwhile, apply F1 and the delivery step (reinstall from the fork, diff, then `superclaude update`) as housekeeping; neither is proven to be the cause. `--fix` was set, but Tier 3 is not offered because the status is `partial`, not `success`.

## Audit

- **Hypothesis cards**: .dev/troubleshoot/bug-orca-orchestrator-spawn-new-sessions-terminal-20261107235513/tier1-hypothesis.md, tier2-root-cause-analyst-hypothesis.md, tier2-quality-engineer-hypothesis.md, tier2-system-architect-hypothesis.md (same directory)
- **Adversarial artifacts** (Tier 2 only): Not invoked: no competing strong fixes
- **Self-review** (Tier 2 only): Not run (no merged proposal)
- **Task file** (Tier 3 only): none
- **Audit log**: .dev/troubleshoot/bug-orca-orchestrator-spawn-new-sessions-terminal-20261107235513/audit.log

## Pipeline Hardening Closure

Pipeline hardening not applicable: the diagnosis is UNDETERMINED and both candidate fixes change instruction text or install delivery, not a gate, parser, status enum, review selector or persisted resume state in this repo's pipelines.

Boundary scan (HC0):
- `CLI/subprocess` — producer: an LLM orchestrator; transformer: the `orca` CLI; consumer: Orca's tab creation. Evidence: tier1-observation.md O1, O4. Risk: a command choice can be satisfied by an adjacent proof (a created tab) while the real goal (a running Claude) fails. Decision: not_applicable. Rationale: the consumer is an external app with no in-repo contract to enumerate, and the repo-side change is wording. Re-run HC0 if a later diagnosis finds the defect in a repo script that shells out to `orca` (for example orca_worktree.py).
- `persisted-state` — producer: `superclaude install`; consumer: the loaded ~/.claude/CLAUDE.md. Evidence: install_core.py:70-72. Risk: a stale installed copy hides a fix. Decision: not_applicable. Rationale: it affects instruction delivery only; no gate, resume or review logic reads it.
- `sibling-pipeline` — `/sc:issue --claim` creates the worktree without `--agent` by design (docs/designs/sc-issue-claim-pipeline-flag.md D2). Decision: not_applicable. Rationale: it launches Claude in a second call and is unchanged by F1 or F2.
