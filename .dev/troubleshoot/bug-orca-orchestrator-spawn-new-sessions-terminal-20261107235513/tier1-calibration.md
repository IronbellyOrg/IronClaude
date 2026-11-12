# Calibration Report

**Card under calibration**: .dev/troubleshoot/bug-orca-orchestrator-spawn-new-sessions-terminal-20261107235513/tier1-hypothesis.md
**Rubric**: ~/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 1
**Timestamp**: 2026-11-08T00:06:31Z
(Returned by confidence-calibrator; persisted by the parent on receipt. Notes condensed by the parent, scores and rules verbatim.)

## Per-dimension scores

| Dimension | Score | Justification (cite card content) |
|-----------|-------|-----------------------------------|
| Evidence grounding | 1.0 | Core citations match on Read: CLAUDE.md:308 and :320 hold the bare `orca worktree create --name ...` with no `--agent`; runtime-local-worktree-terminal-startup.ts:202-214 and :259-269 and worktree-first-surface.ts:2-14 show a plain createTerminal when no agent is attached; definitions-core-2.ts:69-75 and :83-87 match P3; triage-checklist.md:27 is the Config / env drift row. The Alternatives citations (agent-launch-*.ts) could not be resolved because the card gave bare filenames; they support the alternatives, not the headline. |
| Runtime check | 0.0 | `runtime_behavior` x `source_static` gives 0.0. No executed reproducer. The grep line only checks the fix text. The falsification standard is a procedure, not a command with captured output. The parent-captured daemon.log case is another worktree, not the reporter's run. |
| Symptom coverage | 0.5 | Explains the empty plain terminal. The waiting orchestrator only if the orchestrator ran a bare create, which was never observed. The reporter's wording ("new terminal session shortcut") also fits P3, which the card does not exclude. |
| Reproducibility fit | 0.5 | The mechanism (bare create gives hasCommand=false) is deterministic and was seen once on another worktree (O4). Which command the reporter's LLM orchestrator chose is nondeterministic and not reproduced (9 bare creates vs 3 with `--agent` since 11-05, per O4). |
| Fix directness | 0.5 | Targets CLAUDE.md:308 and :320; small. C4 caps this at 0.5. The edit does not change what an LLM chooses; the stale-install half is operational. |
| Domain coherence | 0.5 | Instruction-text gap, Orca runtime behaviour, stale installed copy and LLM command choice: two or three related domains. |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.50 | (1.0 + 0.0 + 0.5 + 0.5 + 0.5 + 0.5) / 6, Fix directness C4-capped |
| gate_M1: evidence_grounding + 0.30 | 1.30 | always applies |
| gate_M2: runtime_check + 0.30 | 0.30 | always applies |
| gated_min | 0.30 | M2 binding |
| verdict_cap | 0.84 | M3a applies (`runtime_behavior`, AFFIRM, runtime_check < 1.0); not binding |
| **calibrated** | 0.30 | after structural caps C7 (0.5, not binding) and C1 (no cap) |
| spot_check_unverifiable | none (no remote URLs); unresolved local paths in Notes | |
| structural_flags | `locus_unknown`, `no_prereg_falsifier`, `uncited`, `headline_definite_low_confidence` | C3b, C4, C7, C1; C1 forces ESCALATE |

## Confidence

- **Self-reported (in card)**: 0.55 (not used as input)
- **Calibrated (this report)**: 0.30
- **Formula applied**: `min(mean(all_six), evidence_grounding + 0.30, runtime_check + 0.30)` = min(0.50, 1.30, 0.30) = 0.30; M3a cap 0.84 and C7 cap 0.5 do not lower it; C1 fires because 0.30 < 0.50.
- **Delta**: -0.25

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence`
- **Rubric rule fired**: refs/agent-assertions.md C1 forces ESCALATE at calibrated 0.30; the rubric independently: § Escalation Decision rule 3 (`confidence < 0.85`). `source_only_dynamic_claim` and `multi_domain` would also match; `low_confidence` is listed first.
- **Execution restriction**: none (`no_escalate: false`, `depth: standard`)

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | yes | `headline_definite_low_confidence` | headline names one definite cause (P1); calibrated 0.30 < 0.50 forces ESCALATE `low_confidence` | tier1-hypothesis.md:1; calibrated 0.30 |
| C2 | no | — | — | card excludes no producer; P2-P5 stated "not excluded" |
| C3 | no | — | immaterial (Symptom coverage already 0.5) | card cites no control arm; M-C `CONTROL-PROOF: unknown` is a tasklist gap |
| C3b | yes | `locus_unknown` | Runtime check ≤ 0.5; already 0.0 | tier1-hypothesis.md `runs-in=unknown`; execution-locus.md `RUN-SITE: pending-producers`, `SAME-ENV: unknown` |
| C4 | yes | `no_prereg_falsifier` | Fix directness ≤ 0.5, applied | diagnosability-tasklist.md M-USER has per-producer true values but no explicit false value or outcome mapping; enabling Task 2 has a linked row and rollback but no verification line |
| C5 | no | — | — | card Timestamp 2026-11-08T00:05:30Z not later than card_mtime 00:06:26Z + 5 min and not T00:00:00Z |
| C6 | no | — | — | no numeric threshold or bracket asserted |
| C7 | yes | `uncited` | calibrated ≤ 0.5 cap, not binding | card names environment properties (stale installed copy, Orca 1.4.245-aidev02) citing O5 rather than a 2x2 row |
| C8 | no | — | — | behaviour-definition row 1 cited; behaviour-definitions.md has non-empty Status `fetched:local-source` |

## Notes

- Verified on Read: CLAUDE.md:303-324, the three IronOrca files above, definitions-core-2.ts:64-89, triage-checklist.md:27, the card's O4/O5 text. Verbatim quotes of the startup file and worktree-first-surface.ts match; branches above line 202 of the startup file were not checked.
- Not verified: the card cited agent-launch-created-workspace.ts, worker-start-agent-placement.ts, agent-launch-worktree-creation.ts, agent-launch-executor.ts, agent-launch-mode.ts by bare filename (the calibrator could not resolve them); also worker-topology.ts, terminal-agent-tab-shortcut.ts, orca_worktree.py:27,42, the pipeline-flag design D2 and core/CLAUDE.md:45-53. They support P4/P5 and the fix wording, not the headline.
- daemon.log, transcripts and installed-copy greps (O2-O5) were not independently read; parent-captured.
- Version gap: IronOrca checkout vs installed 1.4.245-aidev02 not proven equal.
- If the evidence class were `log_evidence`, Runtime check 0.5 gives calibrated 0.58, still < 0.85; the verdict would not change.
