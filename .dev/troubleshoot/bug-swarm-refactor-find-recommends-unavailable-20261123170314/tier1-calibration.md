# Calibration Report
**Card under calibration**: /home/coder/workspaces/worktrees/IronClaude/bug-swarm-refactor-find-recommends-unavailable-s/.dev/troubleshoot/bug-swarm-refactor-find-recommends-unavailable-20261123170314/tier1-hypothesis.md
**Rubric**: /home/coder/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 1
**Timestamp**: 2026-11-23T17:17:13Z

## Per-dimension scores
| Dimension | Score | Justification |
|---|---|---|
| Evidence grounding | 1.0 | Read all cited lines: lens:53, commands:2143, reduce:672-697, captured contract:64, contribution policy:287-292, adversarial skill:60-62. |
| Runtime check | 1.0 | mixed/runtime_repro cross-tab: production CLI stub capture exit 0, observation:18-37. |
| Symptom coverage | 1.0 | Explains unavailable command and literal existing-review prefix. |
| Reproducibility fit | 1.0 | Deterministic executed reproducer matches source. |
| Fix directness | 0.5 | Correct area, but lens/commands/docs/two tests and count gating need changes; patch/replacement not run. |
| Domain coherence | 1.0 | One domain: handoff generation. |

## Stage-2 trace
| Step | Value | Notes |
|---|---|---|
| arithmetic_mean(all_six) | 0.9166666667 | 5.5/6 |
| gate_M1: evidence_grounding + 0.30 | 1.30 | unconditional |
| gate_M2: runtime_check + 0.30 | 1.30 | unconditional |
| gated_min | 0.9166666667 | min above |
| verdict_cap | none | mixed class; runtime check 1.0, modifier not binding |
| **calibrated** | 0.92 | rounded to two decimals |
| spot_check_unverifiable | none | no remote URLs |
| structural_flags | none | nine C-rule rows, none fired |

## Confidence
- **Self-reported (in card)**: 0.50 (historical pre-binding signal, not scoring input).
- **Calibrated (this report)**: 0.92
- **Formula applied**: min(5.5/6, 1.30, 1.30) = 0.9166666667, rounded 0.92; no verdict or structural caps.
- **Delta**: +0.42; binding completed, executed repro and verified citations support higher score.

## Escalation recommendation
- **Verdict**: STOP
- **Reason**: none
- **Rubric rule fired**: Default rule 4: confidence >= 0.85, single-domain and reproducible. No depth/security/intermittency/split condition applies.
- **Execution restriction**: none for diagnosis; this report grants no fix or paid-run authority.

## Structural assertions
| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | no | - | - | 0.92 >= 0.50; headline not enum |
| C2 | no | - | - | no enum exclusion; alternatives not exit claims |
| C3 | no | - | - | no cited passing control; locus CONTROL-PROOF unknown |
| C3b | no | - | - | runs-in known local reduce.py:672 |
| C4 | no | - | - | tasklist has no measurement/enabling rows |
| C5 | no | - | - | card has no timestamp; supplied mtime 17:17:06Z |
| C6 | no | - | - | headline has no numeric threshold; 2-10 is proposed consumer input range |
| C7 | no | - | - | source-defined failure, not an environment-property mechanism; see note |
| C8 | no | - | - | behaviour-definitions.md row1 has fetched Status |

## Notes
- Independent calibrator Read all cited source snippets. Command absence relied on captured observation:8-11, not independent filesystem enumeration; commands/adversarial.md references in observation were not independently checked by this agent.
- C7 judgment: local .venv/installed absence are provenance/observations, not the explanatory environment-property mechanism. No 2x2 row exists; no cap applied. Raw worker hypothetical said a strict reading could cap 0.50 and escalate; parent notes C1 itself requires <0.50, while rubric low-confidence escalation would still apply at 0.50. This hypothetical is not a fired rule or retained independent bound.
- All optional paths supplied. Card classification mixed/runtime_repro valid. No timestamp to drop. Alternatives thin; replacement not executed; weakness reflected in directness 0.5.
- Parent normalized report headings to canonical markers and retained the independently computed scores/verdict unchanged. No retry or score increase after receipt.
