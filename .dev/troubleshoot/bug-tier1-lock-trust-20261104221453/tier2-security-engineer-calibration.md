# Calibration Report

**Card under calibration**: .dev/troubleshoot/bug-tier1-lock-trust-20261104221453/tier2-security-engineer-hypothesis.md
**Rubric**: ~/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-04T22:30:13Z
(persisted by the orchestrator on receipt from the confidence-calibrator agent; content condensed, scores and verdict verbatim)

## Per-dimension scores

| Dimension | Score | Justification |
|---|---|---|
| Evidence grounding | 1.0 | E1 probe-lock-trust.out:6; E2 audit.log:19; E3 conflict-mechanical.md:84-90; E4 SKILL.md:228-230 (CI-wait import, extended by the card to the classifier runtime); E5 :31; E6 conflicts.py:16, :19-21; E8 confirmed by .gitignore:169, :222; E7 constant at :40, assertion at :514-538 |
| Runtime check | 0.5 | E1 supports the Tier 1 cause; E2 is a one-line parent summary; the card's own gaps (non-dev project lacks superclaude, -I and .pth, uv.toml/.python-version, list-of-tables shape) are not executed |
| Symptom coverage | 1.0 | the Codex C3 symptom and the owner's three triggers addressed; extra vectors labelled out of scope |
| Reproducibility fit | 1.0 | deterministic reproducer |
| Fix directness | 0.5 | exact site but multi-part; open assumption on the installed runtime at step 5; C4 cap (no change) |
| Domain coherence | 0.5 | protocol prose, uv/Python runtime, security, tests |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|---|---|---|
| arithmetic_mean(all_six) | 0.75 | |
| gate_M1: evidence_grounding + 0.30 | 1.30 | |
| gate_M2: runtime_check + 0.30 | 0.80 | |
| gated_min | 0.75 | |
| verdict_cap | none | |
| **calibrated** | 0.50 | C7 cap (binding) |
| spot_check_unverifiable | none | |
| structural_flags | no_prereg_falsifier, uncited | |

## Confidence

- **Self-reported (in card)**: 0.80
- **Calibrated (this report)**: 0.50
- **Formula applied**: min(0.75, 1.30, 0.80) = 0.75; C7 cap -> 0.50

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence`
- **Rubric rule fired**: rule 3 confidence < 0.85 (multi_domain also matches)
- **Execution restriction**: none

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | no | — | — | no enum token; 0.50 not below 0.50 |
| C2 | no | — | — | no enum exclusion |
| C3 | no | — | — | no control arm |
| C3b | no | — | — | runs-in known |
| C4 | yes | no_prereg_falsifier | Fix directness <= 0.5 (no change) | four pending probes without true/false predictions |
| C5 | no | — | — | no Timestamp value |
| C6 | no | — | — | no threshold |
| C7 | yes | uncited | calibrated <= 0.50 | environment properties (non-dev project lacks superclaude; -I processes .pth; dev checkout) without a 2x2 row |
| C8 | no | — | — | rows 1 and 2 exist |

## Notes

- Alternative C7 reading gives 0.75, still ESCALATE.
- .gitignore:99 also ignores .python-version in this repo.
- uv behaviours the card relies on have no behaviour-definition rows (project discovery by uv run, -I and .pth, list-of-tables, dynamic as a needed trigger).
