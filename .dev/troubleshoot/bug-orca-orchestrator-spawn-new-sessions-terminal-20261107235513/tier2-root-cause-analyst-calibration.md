# Calibration Report

**Card under calibration**: .dev/troubleshoot/bug-orca-orchestrator-spawn-new-sessions-terminal-20261107235513/tier2-root-cause-analyst-hypothesis.md
**Rubric**: ~/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-08T00:14:12Z
(Returned by confidence-calibrator; persisted by the parent. Notes condensed by the parent; scores, trace and rule rows as returned.)

Declared: `claim_class: runtime_behavior`, `evidence_class: source_static`, `verdict_direction: REFUTE`.

## Per-dimension scores

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Evidence grounding | 0.5 | Cited ranges match on Read (agent-launch-executor.ts:94-107 and :177-182, worker-worktree-creation.ts:121-123, local-worker-start.ts:226-258 and :299-312, worker-start-receipt.ts:86-112, worker-start-readiness-settlement.ts:107-146, worker-topology.ts:67-76, coordinator.ts:257-264, orchestration-rpc-contract.ts:45, explicit-worker-terminal-validation.ts:49-54, local-pty-shell-ready-startup-command.ts:45, README 256-257). They show Orca returns receipts, not the reporter's symptom. The universal negative ("None leaves an empty terminal the orchestrator is not told about") rests on files the card says it did not read (CLI client timeout, agent-launch-surfaces.ts, the retirement dispatcher, isTerminalRunningAgent). E3 rests on a code comment (row 5, "recalled, not load-bearing"). |
| Runtime check | 0.0 | (`runtime_behavior`, `source_static`) = 0.0. No executed reproducer or named test. C3b cap 0.5 not binding. |
| Symptom coverage | 0.5 | Covers part of the empty-tab symptom (P1 seed is a candidate); "the 'waiting orchestrator' is not explained by any Orca path read". |
| Reproducibility fit | 0.0 | No reproducer attempted; depends on an LLM's command choice in an unidentified run; `SAME-ENV: unknown`, `re-run permitted: unknown`; local IronOrca may differ from installed 1.4.245-aidev02. The O2 pair is an observation, not a reproducer. |
| Fix directness | 0.5 | "Proposed Fix: Not applicable"; defers to the Tier 1 CLAUDE.md edit; M-P3, M-P4, M-USER pending. |
| Domain coherence | 0.5 | Orca launch/receipt code plus LLM-orchestrator behaviour, CLI timeout, shim, UI shortcut: two related domains. |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.33 | (0.5+0.0+0.5+0.0+0.5+0.5)/6 |
| gate_M1: evidence_grounding + 0.30 | 0.80 | |
| gate_M2: runtime_check + 0.30 | 0.30 | binding |
| gated_min | 0.30 | min(0.33, 0.80, 0.30) |
| verdict_cap | 0.70 | M3a (runtime_behavior, runtime_check 0.0, REFUTE); not binding |
| **calibrated** | 0.30 | C7 cap 0.5 not binding |
| spot_check_unverifiable | none (no remote URLs) | |
| structural_flags | headline_definite_low_confidence, locus_unknown, uncited | C1, C3b, C7 |

## Confidence

- **Self-reported (in card)**: 0.45 (not used as input)
- **Calibrated (this report)**: 0.30
- **Formula applied**: min(0.33, 0.80, 0.30) = 0.30; M3a 0.70 and C7 0.5 not binding.
- **Delta**: -0.15

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence`
- **Rubric rule fired**: refs/agent-assertions.md C1 (headline names the P1 seed tab; calibrated 0.30 < 0.50); rubric rule 3 (`confidence < 0.85`). `not_reproducible`, `source_only_dynamic_claim`, `multi_domain` also hold, later in the order.
- **Execution restriction**: none

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | yes | `headline_definite_low_confidence` | forced ESCALATE, reason `low_confidence` | card title names P1 seed tab; calibrated 0.30 |
| C2 | no | — | — | exclusions carry file:line (P6 orchestration-rpc-contract.ts:45, P7 explicit-worker-terminal-validation.ts:49-54); weak point: :45 is only the retirement set, enforcing dispatcher not read; no score effect |
| C3 | no | — | — | no control arm cited |
| C3b | yes | `locus_unknown` | Runtime check ≤ 0.5 (already 0.0) | card `runs-in=unknown`; execution-locus.md `RUN-SITE: pending-producers`, `SAME-ENV: unknown` |
| C4 | no | — | — | falsification standard gives false-conditions; tasklist rows carry predictions |
| C5 | no | — | — | Timestamp 2026-11-08T00:12:39Z earlier than card_mtime 00:13:35Z + 5 min |
| C6 | no | — | — | no numeric threshold or bracket headlined |
| C7 | yes | `uncited` | calibrated ≤ 0.5, not binding | card names environment properties (`agentCmdOverrides` is `{}`, local checkout vs installed Orca, shim not in launch path) with no 2x2 row |
| C8 | no | — | — | rows 2, 3, 4, 5 exist with non-empty Status; row 5 is "recalled, not load-bearing" |

## Notes

- Not verified by the calibrator: orchestration-contract-fence.test.ts:106-125 (guessed path missing), `/home/coder/.config/orca/profiles/local-default/orca-data.json`, triage-checklist.md (card did not read it), agent-launch-surfaces.ts:142.
- E1 imprecision: "Terminal mode publishes its surface at lines 94-107" is the `placed.startupTerminalHandle` branch (agent-first create); nothing cited shows what `recoverCreatedWorkspace` creates; the `recovery_shell` role is inferred from the call name and the effect role.
- The Claim sentence "only way a launch leaves a bare shell tab ..." depends on row 5 (a comment).
- Internal tension: Claim says every failure route returns a receipt; the coverage statement lists the CLI timeout, agent-launch-surfaces.ts and the retirement dispatcher as not inspected and able to flip the verdict.
- Pending measurements M-P3, M-P4, M-USER could confirm or flip this card.
