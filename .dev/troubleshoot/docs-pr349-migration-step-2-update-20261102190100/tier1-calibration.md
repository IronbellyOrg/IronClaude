# Calibration Report

**Card under calibration**: /home/coder/workspaces/worktrees/IronClaude/release-v5.0.0/.dev/troubleshoot/docs-pr349-migration-step-2-update-20261102190100/tier1-hypothesis.md
**Rubric**: /home/coder/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 1
**Timestamp**: 2026-11-02T19:14:22Z
**Provenance**: confidence-calibrator agent (returned as data; persisted by parent on receipt)

## Per-dimension scores

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Evidence grounding | 1.0 | Every cited range read and matching: v5.0.0.md:3, :69, :143, :146-147, :150, :152; main.py:340-429, :365-404, :407, :178-236, :246, :263; update.sh:7-8; doctor.py:158, :163-164; main.py:495-497; install_mcp.py:1082-1083, :1093-1099; test_update_command.py:318-333; phase-2 spec :848; mcp-installation.md:64, :70. Minor imprecision: 7 installer calls take force, wire_ccsession takes none (main.py:388, :209); not claim-affecting. |
| Runtime check | 1.0 | doc_contract with two tests cited by name and execution state declared; parent ran them on c0270283 ("9 passed, 11 deselected", tier1-observation.md Runtime evidence); stub at test_update_command.py:69-71 makes the assertion meaningful. Rubric test-assertion anchor. |
| Symptom coverage | 1.0 | Covers :147, :3, :69, :150 and the step-4 verification gap (:152; doctor.py:158, :163-164). |
| Reproducibility fit | 1.0 | Deterministic; pinned executed test reproduces the cited cause. M1 end-to-end probe pending. |
| Fix directness | 1.0 | Docs-only, one file, named lines with replacement text; replacement facts checked (main.py:246, :263; install_mcp.py:1088-1092; doctor.py:164; :227, :229 reference step 2). |
| Domain coherence | 1.0 | Single domain: release-note text vs pinned CLI behaviour. |

## Stage-2 trace

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 1.00 | |
| gate_M1: evidence_grounding + 0.30 | 1.30 | |
| gate_M2: runtime_check + 0.30 | 1.30 | |
| gated_min | 1.00 | |
| verdict_cap | none | doc_contract, runtime_check 1.0 |
| **calibrated** | 1.00 | no structural cap fired |
| spot_check_unverifiable | none | |
| structural_flags | none | |

## Confidence

- Self-reported (card): 0.92 (read, not used as input)
- **Calibrated (this report)**: 1.00
- Formula: min(mean 1.00, 1.30, 1.30) = 1.00
- Delta: +0.08 (Runtime check 0.5 → 1.0 from the parent's captured test run)

## Escalation recommendation

- **Verdict**: `STOP`
- **Reason**: none
- **Rubric rule fired**: Rule 4 (Default) — confidence ≥ 0.85, single-domain, reproducible → STOP at Tier 1.
- **Execution restriction**: none

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | no | — | — | tier1-hypothesis.md:1; calibrated 1.00 |
| C2 | no | — | — | tier1-hypothesis.md "Alternatives considered" are design options |
| C3 | no | — | — | execution-locus.md: no control arm cited |
| C3b | no | — | — | runs-in line matches execution-locus.md RUN-SITE |
| C4 | no | — | — | diagnosability-tasklist.md M1 has predictions + outcome mapping; Task 1 has verification/rollback |
| C5 | no | — | — | card Timestamp date-only, disclosed unobserved, not later than card_mtime + 5 min |
| C6 | no | — | — | no numeric threshold in headline; bracket.md absent, trigger not met |
| C7 | no | — | — | cause environment-independent; Risks mention is not attributed to the defect |
| C8 | no | — | — | behaviour-definition: row 1 exists with non-empty Status |

## Notes

- Runtime-check sensitivity: a strictly literal cross-tab read (doc_contract × source_static = 0.5) gives calibrated 0.80 → ESCALATE low_confidence; the calibrator chose the test-assertion anchor because the tests are cited by name with captured execution. The tests stub installers, so they pin update()'s control flow, not a real install; M1 remains pending.
- Unmentioned mitigation: update() prints update_notice() (main.py:408-413) when a removable legacy entry exists; partly softens impact; not score-affecting.
- C7 borderline: a strict read would cap at 0.5 and ESCALATE; judged not fired.
- Not independently verified: installation.md:56; /sc:graph status behaviour when codegraph is unregistered.
